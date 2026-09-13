from company_v2.worker import build


def test_worker_does_not_construct_autopilot_by_default(monkeypatch, tmp_path):
    monkeypatch.setenv("SYNERGY_COMPANY_DB", str(tmp_path / "worker.db"))
    monkeypatch.delenv("SYNERGY_AUTOPILOT_ENABLED", raising=False)
    monkeypatch.delenv("SYNERGY_ENABLE_AUTOPILOT_SCOUT", raising=False)
    _store, orch, connectors = build()
    assert orch.autopilot is None
    assert all(getattr(c, "name", "") != "autopilot_revenue_scout" for c in connectors)
