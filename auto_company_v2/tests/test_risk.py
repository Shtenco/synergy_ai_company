from company_v2.core.models import ProposedAction, RiskClass, ActionState
from company_v2.core.risk import RiskPolicy


def test_read_only_can_run():
    a = ProposedAction("research", "x", "research.x", RiskClass.READ_ONLY)
    d = RiskPolicy(mode="paper", max_external_spend_usd=0).apply(a)
    assert d.allowed and a.state == ActionState.APPROVED


def test_real_money_blocked_in_paper():
    a = ProposedAction("trade", "x", "trade.x", RiskClass.TRADING, max_loss_usd=1)
    d = RiskPolicy(mode="paper").apply(a)
    assert not d.allowed and not d.approval_required and a.state == ActionState.BLOCKED


def test_external_side_effect_needs_approval():
    a = ProposedAction("deploy", "x", "deploy.x", RiskClass.EXTERNAL)
    d = RiskPolicy(mode="live", max_external_spend_usd=10).apply(a)
    assert d.approval_required and a.state == ActionState.APPROVAL_REQUIRED


def test_spend_limit_needs_approval():
    a = ProposedAction("buy", "x", "external.purchase", RiskClass.CODE_WRITE, estimated_spend_usd=2)
    d = RiskPolicy(mode="live", max_external_spend_usd=1).apply(a)
    assert d.approval_required

def test_live_financial_action_still_hard_capped():
    a = ProposedAction("payment", "x", "payment.send", RiskClass.FINANCIAL, estimated_spend_usd=11)
    d = RiskPolicy(mode="live", max_financial_action_usd=10, max_daily_loss_usd=10).apply(a)
    assert not d.allowed and not d.approval_required and a.state == ActionState.BLOCKED


def test_live_financial_within_cap_requires_human():
    a = ProposedAction("payment", "x", "payment.send", RiskClass.FINANCIAL, estimated_spend_usd=5)
    d = RiskPolicy(mode="live", max_financial_action_usd=10, max_daily_loss_usd=10).apply(a)
    assert d.approval_required and a.state == ActionState.APPROVAL_REQUIRED
