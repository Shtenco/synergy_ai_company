from __future__ import annotations

import os
import time
from company_v2.core.settings import Settings
from company_v2.core.store import Store
from company_v2.core.risk import RiskPolicy
from company_v2.core.orchestrator import Orchestrator
from company_v2.adapters.http_bridge import HttpJsonBridge
from company_v2.adapters.autopilot import AutopilotAdapter
from company_v2.connectors.github_issues import GitHubIssuesConnector
from company_v2.connectors.autopilot_scout import AutopilotRevenueScout
from pathlib import Path


def build() -> tuple[Store, Orchestrator, list]:
    s = Settings()
    store = Store(s.db_path)
    autopilot = (
        AutopilotAdapter(
            HttpJsonBridge(s.autopilot_url, s.autopilot_token),
            s.autopilot_task_path,
            s.autopilot_status_path,
        )
        if s.autopilot_enabled else None
    )
    orch = Orchestrator(store, RiskPolicy(s.mode, s.max_external_spend_usd, s.max_daily_loss_usd, s.max_financial_action_usd), autopilot, s.ai_daily_budget_usd)
    connectors = [GitHubIssuesConnector()]
    if autopilot is not None and os.getenv("SYNERGY_ENABLE_AUTOPILOT_SCOUT", "0") == "1":
        sources = Path(__file__).resolve().parent.parent / "config" / "opportunity_sources.json"
        connectors.append(AutopilotRevenueScout(autopilot, sources))
    return store, orch, connectors


def run_once() -> dict:
    store, orch, connectors = build()
    if store.is_paused():
        return {"paused": True, "ingested": 0, "dispatched": 0}
    all_opps = []
    for c in connectors:
        try:
            all_opps.extend(c.discover())
        except Exception as e:
            store.event("connector.error", {"connector": getattr(c, "name", type(c).__name__), "error": str(e)})
    ranked = orch.ingest(all_opps)
    dispatched = 0
    # Validate only the strongest fresh candidates. Validation itself is read-only.
    for o, score in ranked[:5]:
        if score < float(os.getenv("SYNERGY_MIN_VALIDATION_SCORE", "20")):
            continue
        action = orch.propose_validation(o)
        if action.state.value == "approved":
            try:
                orch.dispatch(action); dispatched += 1
            except Exception as e:
                store.event("dispatch.error", {"error": str(e)}, action.id)
    return {"paused": False, "ingested": len(ranked), "dispatched": dispatched}


def main():
    interval = max(60.0, float(os.getenv("SYNERGY_DISCOVERY_INTERVAL_SECONDS", "900")))
    while True:
        run_once()
        time.sleep(interval)


if __name__ == "__main__": main()
