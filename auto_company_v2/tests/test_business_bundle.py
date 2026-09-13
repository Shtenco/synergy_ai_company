from company_v2.core.models import Opportunity
from company_v2.core.orchestrator import Orchestrator
from company_v2.core.risk import RiskPolicy
from company_v2.core.store import Store
import tempfile


def test_validated_opportunity_creates_safe_business_bundle():
    f=tempfile.NamedTemporaryFile(suffix='.db',delete=False); f.close(); store=Store(f.name)
    o=Opportunity(title='AI SMM project',source='buyer',description='deliver content',expected_revenue_usd=500,estimated_cost_usd=100,probability=.7)
    orch=Orchestrator(store,RiskPolicy())
    actions=orch.propose_go_to_market_bundle(o,{'next_action':'prepare_bounded_proposal'})
    assert {a.capability for a in actions}=={'sales.compose_offer','smm.content_plan','video.storyboard','cfo.analyze_budget'}
    assert all(a.state.value=='approved' for a in actions)


def test_unvalidated_opportunity_creates_no_bundle():
    f=tempfile.NamedTemporaryFile(suffix='.db',delete=False); f.close(); store=Store(f.name)
    o=Opportunity(title='x',source='x')
    assert Orchestrator(store,RiskPolicy()).propose_go_to_market_bundle(o,{'next_action':'collect_more_evidence'})==[]
