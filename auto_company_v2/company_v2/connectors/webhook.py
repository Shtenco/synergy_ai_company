from __future__ import annotations

from company_v2.core.models import Opportunity


def opportunity_from_payload(payload: dict) -> Opportunity:
    required = {"title", "source"}
    missing = required - payload.keys()
    if missing:
        raise ValueError(f"missing fields: {sorted(missing)}")
    return Opportunity(
        title=str(payload["title"]),
        source=str(payload["source"]),
        description=str(payload.get("description", "")),
        url=str(payload.get("url", "")),
        expected_revenue_usd=float(payload.get("expected_revenue_usd", 0.0)),
        estimated_cost_usd=float(payload.get("estimated_cost_usd", 0.0)),
        probability=float(payload.get("probability", 0.0)),
        hours=float(payload.get("hours", 0.0)),
        evidence=[str(x) for x in payload.get("evidence", [])],
        tags=[str(x) for x in payload.get("tags", [])],
    )
