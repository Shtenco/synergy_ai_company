from __future__ import annotations

from .models import Opportunity


def score_opportunity(o: Opportunity) -> float:
    """Revenue-first score in roughly 0..100.

    Score intentionally rewards evidence, positive expected value and short time-to-test,
    while refusing to treat speculative gross revenue as realized value.
    """
    p = min(max(o.probability, 0.0), 1.0)
    ev = p * max(o.expected_revenue_usd, 0.0) - max(o.estimated_cost_usd, 0.0)
    ev_component = min(max(ev / 100.0, -1.0), 2.0) * 30.0
    evidence_component = min(len(o.evidence), 5) * 6.0
    speed_component = 20.0 if o.hours <= 2 else 12.0 if o.hours <= 8 else 5.0 if o.hours <= 24 else 0.0
    probability_component = p * 20.0
    speculative_penalty = 20.0 if not o.evidence else 0.0
    return round(max(0.0, min(100.0, 20.0 + ev_component + evidence_component + speed_component + probability_component - speculative_penalty)), 2)
