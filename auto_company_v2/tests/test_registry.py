from pathlib import Path
from company_v2.core.registry import CapabilityRegistry


def test_all_51_repositories_registered():
    p = Path(__file__).resolve().parents[1] / "config" / "repositories.json"
    r = CapabilityRegistry(p)
    assert r.summary()["total"] == 51
    assert r.get("agi_autopilot").role == "executor"
    assert r.get("agi_nexus").role == "memory"
