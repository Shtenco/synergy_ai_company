from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any
import hashlib


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


class RiskClass(str, Enum):
    READ_ONLY = "read_only"
    CODE_WRITE = "code_write"
    EXTERNAL = "external_side_effect"
    FINANCIAL = "financial"
    TRADING = "trading"
    BLOCKCHAIN = "blockchain"


class ActionState(str, Enum):
    PROPOSED = "proposed"
    APPROVAL_REQUIRED = "approval_required"
    APPROVED = "approved"
    DISPATCHED = "dispatched"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    REJECTED = "rejected"
    BLOCKED = "blocked"


@dataclass(slots=True)
class Opportunity:
    title: str
    source: str
    description: str = ""
    url: str = ""
    expected_revenue_usd: float = 0.0
    estimated_cost_usd: float = 0.0
    probability: float = 0.0
    hours: float = 0.0
    evidence: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    id: str = ""
    created_at: str = field(default_factory=utcnow)

    def __post_init__(self) -> None:
        if not self.id:
            raw = f"{self.source}\n{self.url or self.title}".encode("utf-8", "ignore")
            self.id = "opp_" + hashlib.sha256(raw).hexdigest()[:16]

    @property
    def expected_value_usd(self) -> float:
        return self.probability * self.expected_revenue_usd - self.estimated_cost_usd

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["expected_value_usd"] = self.expected_value_usd
        return d


@dataclass(slots=True)
class ProposedAction:
    kind: str
    description: str
    capability: str
    risk_class: RiskClass = RiskClass.READ_ONLY
    estimated_spend_usd: float = 0.0
    max_loss_usd: float = 0.0
    opportunity_id: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)
    id: str = ""
    state: ActionState = ActionState.PROPOSED
    created_at: str = field(default_factory=utcnow)

    def __post_init__(self) -> None:
        if not self.id:
            raw = f"{self.kind}\n{self.capability}\n{self.opportunity_id or ''}\n{self.created_at}".encode()
            self.id = "act_" + hashlib.sha256(raw).hexdigest()[:16]

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["risk_class"] = self.risk_class.value
        d["state"] = self.state.value
        return d
