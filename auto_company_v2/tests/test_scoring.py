from company_v2.core.models import Opportunity
from company_v2.core.scoring import score_opportunity


def test_evidenced_positive_ev_scores_higher():
    a = Opportunity("a", "x", expected_revenue_usd=100, estimated_cost_usd=10, probability=.5, hours=2, evidence=["buyer post"])
    b = Opportunity("b", "x", expected_revenue_usd=100, estimated_cost_usd=10, probability=.5, hours=2, evidence=[])
    assert score_opportunity(a) > score_opportunity(b)
