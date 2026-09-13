from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from company_v2.core.settings import Settings
from company_v2.core.store import Store
from company_v2.core.risk import RiskPolicy
from company_v2.core.registry import CapabilityRegistry
from company_v2.core.orchestrator import Orchestrator
from company_v2.connectors.webhook import opportunity_from_payload
from company_v2.adapters.http_bridge import HttpJsonBridge
from company_v2.adapters.autopilot import AutopilotAdapter
from company_v2.adapters.nexus import NexusAdapter


settings = Settings()
store = Store(settings.db_path)
risk = RiskPolicy(settings.mode, settings.max_external_spend_usd, settings.max_daily_loss_usd, settings.max_financial_action_usd)
registry_path = Path(__file__).resolve().parent.parent / "config" / "repositories.json"
registry = CapabilityRegistry(registry_path)
autopilot = (
    AutopilotAdapter(
        HttpJsonBridge(settings.autopilot_url, settings.autopilot_token),
        settings.autopilot_task_path,
        settings.autopilot_status_path,
    )
    if settings.autopilot_enabled else None
)
nexus = (
    NexusAdapter(
        HttpJsonBridge(settings.nexus_url, settings.nexus_token),
        settings.nexus_search_path,
        settings.nexus_upsert_path,
    )
    if settings.nexus_enabled else None
)
orch = Orchestrator(store, risk, autopilot, settings.ai_daily_budget_usd)
app = FastAPI(title="Synergy AI Company 2.0", version="2.0.0a1")


def guard(authorization: str | None) -> None:
    if settings.api_token and authorization != f"Bearer {settings.api_token}":
        raise HTTPException(401, "invalid API token")


class LeadIn(BaseModel):
    title: str
    source: str
    description: str = ""
    url: str = ""
    expected_revenue_usd: float = 0.0
    estimated_cost_usd: float = 0.0
    probability: float = 0.0
    hours: float = 0.0
    evidence: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)


class ApprovalIn(BaseModel):
    actor: str
    reason: str = ""


class LedgerIn(BaseModel):
    kind: str
    amount_usd: float
    evidence: str
    opportunity_id: str | None = None
    external_ref: str | None = None


class UsageIn(BaseModel):
    provider: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    action_id: str | None = None


@app.get("/health")
def health():
    return {"ok": True, "mode": settings.mode, "paused": settings.paused or store.is_paused(), "repos": registry.summary()}


@app.get("/v1/status")
def status(authorization: str | None = Header(default=None)):
    guard(authorization)
    revenue = store.realized_revenue_usd()
    cost = store.realized_cost_usd()
    return {
        "mode": settings.mode,
        "paused": settings.paused or store.is_paused(),
        "autopilot_runtime_enabled": settings.autopilot_enabled,
        "nexus_runtime_enabled": settings.nexus_enabled,
        "operational_revenue_evidence_usd": revenue,
        "operational_cost_usd": cost,
        "operational_margin_usd": revenue - cost,
        "financial_authority": "Shtenco/synergy_financial_os",
        "ai_spend_today_usd": store.usage_today_usd(),
        "ai_daily_budget_usd": settings.ai_daily_budget_usd,
        "registry": registry.summary(),
    }


@app.post("/v1/pause")
def pause(body: ApprovalIn, authorization: str | None = Header(default=None)):
    guard(authorization); store.set_paused(True, body.actor); return {"ok": True, "paused": True}


@app.post("/v1/resume")
def resume(body: ApprovalIn, authorization: str | None = Header(default=None)):
    guard(authorization); store.set_paused(False, body.actor); return {"ok": True, "paused": False}


@app.get("/v1/repositories")
def repositories(authorization: str | None = Header(default=None)):
    guard(authorization)
    return [asdict(x) for x in registry.items]


@app.post("/v1/leads")
def ingest_lead(body: LeadIn, authorization: str | None = Header(default=None)):
    guard(authorization)
    o = opportunity_from_payload(body.model_dump())
    ranked = orch.ingest([o])
    action = orch.propose_validation(o)
    return {"opportunity": o.to_dict(), "score": ranked[0][1], "validation_action": action.to_dict()}


@app.get("/v1/opportunities")
def opportunities(authorization: str | None = Header(default=None)):
    guard(authorization)
    rows = store.list_rows("opportunities", 100)
    for r in rows:
        r["data"] = json.loads(r.pop("data_json"))
    return rows


@app.get("/v1/actions")
def actions(authorization: str | None = Header(default=None)):
    guard(authorization)
    rows = store.list_rows("actions", 100)
    for r in rows:
        r["data"] = json.loads(r.pop("data_json"))
    return rows


@app.post("/v1/actions/{action_id}/approve")
def approve(action_id: str, body: ApprovalIn, authorization: str | None = Header(default=None)):
    guard(authorization)
    try: store.approve(action_id, "approved", body.actor, body.reason)
    except KeyError: raise HTTPException(404, "action not found")
    return {"ok": True, "action_id": action_id, "state": "approved"}


@app.post("/v1/actions/{action_id}/reject")
def reject(action_id: str, body: ApprovalIn, authorization: str | None = Header(default=None)):
    guard(authorization)
    try: store.approve(action_id, "rejected", body.actor, body.reason)
    except KeyError: raise HTTPException(404, "action not found")
    return {"ok": True, "action_id": action_id, "state": "rejected"}


@app.post("/v1/actions/{action_id}/dispatch")
def dispatch(action_id: str, authorization: str | None = Header(default=None)):
    guard(authorization)
    try:
        return {"ok": True, "result": orch.dispatch_by_id(action_id)}
    except KeyError:
        raise HTTPException(404, "action not found")
    except (PermissionError, RuntimeError) as e:
        raise HTTPException(409, str(e))


@app.post("/v1/ledger")
def ledger(body: LedgerIn, authorization: str | None = Header(default=None)):
    guard(authorization)
    if body.kind not in {"revenue", "cost", "loss", "refund", "receivable"}:
        raise HTTPException(422, "unsupported ledger kind")
    try:
        store.ledger_add(body.kind, body.amount_usd, body.evidence, body.opportunity_id, body.external_ref)
    except ValueError as e:
        raise HTTPException(422, str(e))
    return {"ok": True}


@app.post("/v1/usage")
def usage(body: UsageIn, authorization: str | None = Header(default=None)):
    guard(authorization)
    if body.cost_usd < 0 or body.input_tokens < 0 or body.output_tokens < 0:
        raise HTTPException(422, "usage values must be non-negative")
    store.usage_add(body.provider, body.model, body.input_tokens, body.output_tokens, body.cost_usd, body.action_id)
    return {"ok": True, "ai_spend_today_usd": store.usage_today_usd()}


@app.post("/v1/nexus/search")
def nexus_search(body: dict, authorization: str | None = Header(default=None)):
    guard(authorization)
    if nexus is None:
        raise HTTPException(503, "NEXUS runtime is not enabled; current agi_nexus main exposes architecture/artifacts but no verified HTTP service")
    return nexus.search(str(body.get("query", "")), body.get("namespaces"), int(body.get("limit", 10)))
