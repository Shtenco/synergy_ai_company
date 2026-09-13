from company_v2.core.settings import Settings


def test_external_ai_runtimes_fail_closed_by_default(monkeypatch):
    monkeypatch.delenv("SYNERGY_AUTOPILOT_ENABLED", raising=False)
    monkeypatch.delenv("SYNERGY_NEXUS_ENABLED", raising=False)
    s = Settings()
    assert s.autopilot_enabled is False
    assert s.nexus_enabled is False
