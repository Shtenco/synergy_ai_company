from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from .http_bridge import HttpJsonBridge


@dataclass(slots=True)
class AutopilotAdapter:
    """Transport adapter for agi_autopilot.

    The paths are configuration, not assumptions about internal implementation.
    This lets the existing repo expose a small compatibility route or sidecar.
    """
    bridge: HttpJsonBridge
    task_path: str = "/v1/tasks"
    status_path: str = "/v1/tasks/{task_id}"

    def dispatch(self, action: dict[str, Any]) -> dict[str, Any]:
        envelope = {
            "protocol": "synergy.capability.v1",
            "source": "synergy_ai_company",
            "action_id": action["id"],
            "capability": action["capability"],
            "description": action["description"],
            "payload": action.get("payload", {}),
            "constraints": {
                "risk_class": action["risk_class"],
                "estimated_spend_usd": action.get("estimated_spend_usd", 0.0),
                "max_loss_usd": action.get("max_loss_usd", 0.0),
            },
        }
        return self.bridge.post(self.task_path, envelope)

    def status(self, task_id: str) -> dict[str, Any]:
        return self.bridge.get(self.status_path.format(task_id=task_id))
