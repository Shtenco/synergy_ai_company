from __future__ import annotations

from dataclasses import dataclass
from .models import ProposedAction, RiskClass, ActionState


@dataclass(frozen=True, slots=True)
class RiskDecision:
    allowed: bool
    approval_required: bool
    reason: str


@dataclass(slots=True)
class RiskPolicy:
    mode: str = "paper"
    max_external_spend_usd: float = 0.0
    max_daily_loss_usd: float = 0.0
    max_financial_action_usd: float = 0.0

    def evaluate(self, action: ProposedAction, realized_daily_loss_usd: float = 0.0) -> RiskDecision:
        money_risks = {RiskClass.FINANCIAL, RiskClass.TRADING, RiskClass.BLOCKCHAIN}
        if self.mode != "live" and action.risk_class in money_risks:
            return RiskDecision(False, False, f"{action.risk_class.value} disabled outside live mode")

        if action.risk_class in money_risks:
            if self.max_financial_action_usd <= 0:
                return RiskDecision(False, False, "real-money cap is zero; live money execution is hard-disabled")
            if action.estimated_spend_usd > self.max_financial_action_usd:
                return RiskDecision(False, False, "hard per-action financial cap exceeded")
            if action.max_loss_usd > self.max_daily_loss_usd:
                return RiskDecision(False, False, "hard daily loss cap exceeded by proposed action")
            return RiskDecision(False, True, "real-money/signing action requires explicit human approval")

        if action.estimated_spend_usd > self.max_external_spend_usd:
            return RiskDecision(False, True, "external spend exceeds autonomous spend limit")

        if action.max_loss_usd > 0 and self.max_daily_loss_usd <= 0:
            return RiskDecision(False, True, "loss-bearing action requires a configured daily loss budget")

        if realized_daily_loss_usd + max(action.max_loss_usd, 0.0) > self.max_daily_loss_usd > 0:
            return RiskDecision(False, False, "daily loss circuit breaker")

        if action.risk_class == RiskClass.EXTERNAL:
            return RiskDecision(False, True, "external side effects require approval by default")

        return RiskDecision(True, False, "within autonomous policy")

    def apply(self, action: ProposedAction, realized_daily_loss_usd: float = 0.0) -> RiskDecision:
        d = self.evaluate(action, realized_daily_loss_usd)
        if d.approval_required:
            action.state = ActionState.APPROVAL_REQUIRED
        elif not d.allowed:
            action.state = ActionState.BLOCKED
        else:
            action.state = ActionState.APPROVED
        return d
