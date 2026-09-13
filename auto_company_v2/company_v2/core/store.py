from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from contextlib import contextmanager
from typing import Any, Iterator
from datetime import datetime, timezone


SCHEMA = """
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,
  type TEXT NOT NULL,
  aggregate_id TEXT,
  payload_json TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_events_type_ts ON events(type, ts);

CREATE TABLE IF NOT EXISTS opportunities (
  id TEXT PRIMARY KEY,
  source TEXT NOT NULL,
  title TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'new',
  score REAL NOT NULL DEFAULT 0,
  data_json TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS actions (
  id TEXT PRIMARY KEY,
  state TEXT NOT NULL,
  risk_class TEXT NOT NULL,
  capability TEXT NOT NULL,
  data_json TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS approvals (
  action_id TEXT PRIMARY KEY,
  decision TEXT NOT NULL,
  actor TEXT NOT NULL,
  reason TEXT,
  ts TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ledger (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,
  kind TEXT NOT NULL,
  amount_usd REAL NOT NULL,
  currency TEXT NOT NULL DEFAULT 'USD',
  external_ref TEXT,
  evidence TEXT NOT NULL,
  opportunity_id TEXT
);

CREATE TABLE IF NOT EXISTS usage (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,
  provider TEXT NOT NULL,
  model TEXT NOT NULL,
  input_tokens INTEGER NOT NULL DEFAULT 0,
  output_tokens INTEGER NOT NULL DEFAULT 0,
  cost_usd REAL NOT NULL DEFAULT 0,
  action_id TEXT
);
CREATE INDEX IF NOT EXISTS idx_usage_ts ON usage(ts);

CREATE TABLE IF NOT EXISTS memories (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT NOT NULL,
  namespace TEXT NOT NULL,
  key TEXT NOT NULL,
  value_json TEXT NOT NULL,
  UNIQUE(namespace, key)
);
"""


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Store:
    def __init__(self, path: str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as cx:
            cx.executescript(SCHEMA)

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        cx = sqlite3.connect(self.path)
        cx.row_factory = sqlite3.Row
        try:
            yield cx
            cx.commit()
        finally:
            cx.close()

    def event(self, type_: str, payload: dict[str, Any], aggregate_id: str | None = None) -> None:
        with self.connect() as cx:
            cx.execute(
                "INSERT INTO events(ts,type,aggregate_id,payload_json) VALUES(?,?,?,?)",
                (now(), type_, aggregate_id, json.dumps(payload, ensure_ascii=False, sort_keys=True)),
            )

    def upsert_opportunity(self, data: dict[str, Any], score: float) -> None:
        ts = now()
        with self.connect() as cx:
            cx.execute(
                """INSERT INTO opportunities(id,source,title,status,score,data_json,created_at,updated_at)
                   VALUES(?,?,?,?,?,?,?,?)
                   ON CONFLICT(id) DO UPDATE SET score=excluded.score,data_json=excluded.data_json,updated_at=excluded.updated_at""",
                (data["id"], data["source"], data["title"], "new", score, json.dumps(data, ensure_ascii=False), ts, ts),
            )

    def save_action(self, data: dict[str, Any]) -> None:
        ts = now()
        with self.connect() as cx:
            cx.execute(
                """INSERT INTO actions(id,state,risk_class,capability,data_json,created_at,updated_at)
                   VALUES(?,?,?,?,?,?,?)
                   ON CONFLICT(id) DO UPDATE SET state=excluded.state,data_json=excluded.data_json,updated_at=excluded.updated_at""",
                (data["id"], data["state"], data["risk_class"], data["capability"], json.dumps(data, ensure_ascii=False), ts, ts),
            )

    def set_action_state(self, action_id: str, state: str) -> None:
        with self.connect() as cx:
            row = cx.execute("SELECT data_json FROM actions WHERE id=?", (action_id,)).fetchone()
            if not row:
                raise KeyError(action_id)
            data = json.loads(row["data_json"])
            data["state"] = state
            cx.execute("UPDATE actions SET state=?,data_json=?,updated_at=? WHERE id=?", (state, json.dumps(data), now(), action_id))

    def approve(self, action_id: str, decision: str, actor: str, reason: str = "") -> None:
        if decision not in {"approved", "rejected"}:
            raise ValueError("decision must be approved or rejected")
        with self.connect() as cx:
            cx.execute(
                "INSERT OR REPLACE INTO approvals(action_id,decision,actor,reason,ts) VALUES(?,?,?,?,?)",
                (action_id, decision, actor, reason, now()),
            )
        self.set_action_state(action_id, decision)
        self.event("approval.recorded", {"decision": decision, "actor": actor, "reason": reason}, action_id)

    def ledger_add(self, kind: str, amount_usd: float, evidence: str, opportunity_id: str | None = None, external_ref: str | None = None) -> None:
        if amount_usd < 0:
            raise ValueError("ledger amount must be non-negative; use the kind field for direction")
        if not evidence.strip():
            raise ValueError("ledger entries require evidence")
        if kind == "revenue" and not external_ref:
            raise ValueError("realized revenue requires external_ref (payment/invoice/transaction evidence)")
        with self.connect() as cx:
            cx.execute(
                "INSERT INTO ledger(ts,kind,amount_usd,external_ref,evidence,opportunity_id) VALUES(?,?,?,?,?,?)",
                (now(), kind, amount_usd, external_ref, evidence, opportunity_id),
            )
        self.event("ledger.entry", {"kind": kind, "amount_usd": amount_usd, "evidence": evidence}, opportunity_id)

    def realized_revenue_usd(self) -> float:
        with self.connect() as cx:
            row = cx.execute("SELECT COALESCE(SUM(amount_usd),0) AS x FROM ledger WHERE kind='revenue'").fetchone()
            return float(row["x"])

    def realized_cost_usd(self) -> float:
        with self.connect() as cx:
            row = cx.execute("SELECT COALESCE(SUM(amount_usd),0) AS x FROM ledger WHERE kind IN ('cost','loss','refund')").fetchone()
            usage = cx.execute("SELECT COALESCE(SUM(cost_usd),0) AS x FROM usage").fetchone()
        return float(row["x"]) + float(usage["x"])

    def loss_today_usd(self) -> float:
        with self.connect() as cx:
            row = cx.execute("SELECT COALESCE(SUM(amount_usd),0) AS x FROM ledger WHERE kind='loss' AND date(ts)=date('now')").fetchone()
        return float(row["x"])

    def usage_total_usd(self) -> float:
        with self.connect() as cx:
            row = cx.execute("SELECT COALESCE(SUM(cost_usd),0) AS x FROM usage").fetchone()
        return float(row["x"])


    def usage_add(self, provider: str, model: str, input_tokens: int, output_tokens: int, cost_usd: float, action_id: str | None = None) -> None:
        with self.connect() as cx:
            cx.execute(
                "INSERT INTO usage(ts,provider,model,input_tokens,output_tokens,cost_usd,action_id) VALUES(?,?,?,?,?,?,?)",
                (now(), provider, model, int(input_tokens), int(output_tokens), float(cost_usd), action_id),
            )
        self.event("usage.recorded", {"provider": provider, "model": model, "cost_usd": float(cost_usd)}, action_id)

    def usage_today_usd(self) -> float:
        with self.connect() as cx:
            row = cx.execute("SELECT COALESCE(SUM(cost_usd),0) AS x FROM usage WHERE date(ts)=date('now')").fetchone()
        return float(row["x"])

    def get_action_data(self, action_id: str) -> dict[str, Any]:
        with self.connect() as cx:
            row = cx.execute("SELECT data_json FROM actions WHERE id=?", (action_id,)).fetchone()
        if not row:
            raise KeyError(action_id)
        return json.loads(row["data_json"])

    def approval_decision(self, action_id: str) -> str | None:
        with self.connect() as cx:
            row = cx.execute("SELECT decision FROM approvals WHERE action_id=?", (action_id,)).fetchone()
        return None if not row else str(row["decision"])

    def memory_set(self, namespace: str, key: str, value: Any) -> None:
        with self.connect() as cx:
            cx.execute(
                "INSERT INTO memories(ts,namespace,key,value_json) VALUES(?,?,?,?) "
                "ON CONFLICT(namespace,key) DO UPDATE SET ts=excluded.ts,value_json=excluded.value_json",
                (now(), namespace, key, json.dumps(value, ensure_ascii=False)),
            )

    def memory_get(self, namespace: str, key: str, default: Any = None) -> Any:
        with self.connect() as cx:
            row = cx.execute("SELECT value_json FROM memories WHERE namespace=? AND key=?", (namespace, key)).fetchone()
        return default if not row else json.loads(row["value_json"])

    def is_paused(self) -> bool:
        return bool(self.memory_get("system", "paused", False))

    def set_paused(self, value: bool, actor: str) -> None:
        self.memory_set("system", "paused", bool(value))
        self.event("system.paused" if value else "system.resumed", {"actor": actor})

    def list_rows(self, table: str, limit: int = 100) -> list[dict[str, Any]]:
        if table not in {"opportunities", "actions", "approvals", "ledger", "events", "memories", "usage"}:
            raise ValueError("unsupported table")
        with self.connect() as cx:
            rows = cx.execute(f"SELECT * FROM {table} ORDER BY rowid DESC LIMIT ?", (limit,)).fetchall()
        return [dict(r) for r in rows]
