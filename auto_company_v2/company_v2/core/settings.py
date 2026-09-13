from __future__ import annotations

from dataclasses import dataclass
import os


def _float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, str(default)))
    except ValueError:
        return default


def _bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


@dataclass(frozen=True, slots=True)
class Settings:
    db_path: str = os.getenv("SYNERGY_COMPANY_DB", "var/synergy_company.db")
    mode: str = os.getenv("SYNERGY_COMPANY_MODE", "paper")
    paused: bool = os.getenv("SYNERGY_COMPANY_PAUSED", "0") == "1"
    ai_daily_budget_usd: float = _float("SYNERGY_AI_DAILY_BUDGET_USD", 10.0)
    max_external_spend_usd: float = _float("SYNERGY_MAX_EXTERNAL_SPEND_USD", 0.0)
    max_financial_action_usd: float = _float("SYNERGY_MAX_FINANCIAL_ACTION_USD", 0.0)
    max_daily_loss_usd: float = _float("SYNERGY_MAX_DAILY_LOSS_USD", 0.0)
    api_token: str = os.getenv("SYNERGY_API_TOKEN", "")
    bind_host: str = os.getenv("SYNERGY_BIND_HOST", "127.0.0.1")
    bind_port: int = _int("SYNERGY_BIND_PORT", 8788)

    autopilot_enabled: bool = _bool("SYNERGY_AUTOPILOT_ENABLED", False)
    autopilot_url: str = os.getenv("SYNERGY_AUTOPILOT_URL", "http://127.0.0.1:8120")
    autopilot_task_path: str = os.getenv("SYNERGY_AUTOPILOT_TASK_PATH", "/v1/tasks")
    autopilot_status_path: str = os.getenv("SYNERGY_AUTOPILOT_STATUS_PATH", "/v1/tasks/{task_id}")
    autopilot_execute_path: str = os.getenv("SYNERGY_AUTOPILOT_EXECUTE_PATH", "/v1/tasks/{task_id}/execute")
    autopilot_approve_path: str = os.getenv("SYNERGY_AUTOPILOT_APPROVE_PATH", "/v1/tasks/{task_id}/approve")
    autopilot_token: str = os.getenv("SYNERGY_AUTOPILOT_TOKEN", "")

    nexus_enabled: bool = _bool("SYNERGY_NEXUS_ENABLED", False)
    nexus_url: str = os.getenv("SYNERGY_NEXUS_URL", "http://127.0.0.1:8130")
    nexus_search_path: str = os.getenv("SYNERGY_NEXUS_SEARCH_PATH", "/v1/memory/search")
    nexus_upsert_path: str = os.getenv("SYNERGY_NEXUS_UPSERT_PATH", "/v1/memory/upsert")
    nexus_token: str = os.getenv("SYNERGY_NEXUS_TOKEN", "")
