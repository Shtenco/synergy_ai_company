from __future__ import annotations

import argparse
import json
from pathlib import Path
from .core.settings import Settings
from .core.store import Store
from .core.registry import CapabilityRegistry


def main() -> int:
    p = argparse.ArgumentParser(prog="synergy-company")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    sub.add_parser("status")
    sub.add_parser("repos")
    args = p.parse_args()

    s = Settings()
    store = Store(s.db_path)
    registry = CapabilityRegistry(Path(__file__).resolve().parent.parent / "config" / "repositories.json")
    if args.cmd == "init":
        print(json.dumps({"ok": True, "db": s.db_path, "repos": registry.summary()}, ensure_ascii=False, indent=2))
    elif args.cmd == "status":
        rev = store.realized_revenue_usd(); cost = store.realized_cost_usd()
        print(json.dumps({
            "mode": s.mode,
            "operational_revenue_evidence_usd": rev,
            "operational_cost_usd": cost,
            "operational_margin_usd": rev-cost,
            "financial_authority": "Shtenco/synergy_financial_os",
        }, ensure_ascii=False, indent=2))
    elif args.cmd == "repos":
        print(json.dumps(registry.summary(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
