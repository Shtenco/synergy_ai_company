from __future__ import annotations
from dataclasses import dataclass
from .store import Store


@dataclass(frozen=True, slots=True)
class FinancialSnapshot:
    realized_revenue_usd: float
    realized_cost_usd: float
    realized_profit_usd: float
    margin: float | None


def snapshot(store: Store) -> FinancialSnapshot:
    revenue = store.realized_revenue_usd()
    cost = store.realized_cost_usd()
    profit = revenue - cost
    margin = None if revenue <= 0 else profit / revenue
    return FinancialSnapshot(revenue, cost, profit, margin)
