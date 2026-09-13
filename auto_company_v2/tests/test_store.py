from company_v2.core.store import Store


def test_ledger_requires_evidence(tmp_path):
    s = Store(str(tmp_path / "x.db"))
    try:
        s.ledger_add("revenue", 10, "")
        assert False
    except ValueError:
        pass
    s.ledger_add("revenue", 10, "payment confirmed", external_ref="stripe:pi_test")
    assert s.realized_revenue_usd() == 10

def test_negative_ledger_amount_rejected(tmp_path):
    s = Store(str(tmp_path / "x.db"))
    try:
        s.ledger_add("cost", -10, "bad")
        assert False
    except ValueError:
        pass


def test_ai_usage_is_real_cost(tmp_path):
    s = Store(str(tmp_path / "x.db"))
    s.usage_add("provider", "model", 10, 5, 1.25)
    assert s.realized_cost_usd() == 1.25
