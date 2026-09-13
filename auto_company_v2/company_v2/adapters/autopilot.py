from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from .http_bridge import HttpJsonBridge


@dataclass(slots=True)
class AutopilotAdapter:
    """Exact client for the agi_autopilot synergy.capability.v1 task runtime."""
    bridge: HttpJsonBridge
    task_path: str = "/v1/tasks"
    status_path: str = "/v1/tasks/{task_id}"
    execute_path: str = "/v1/tasks/{task_id}/execute"
    approve_path: str = "/v1/tasks/{task_id}/approve"

    def dispatch(self, action: dict[str, Any], approved_by: str | None = None) -> dict[str, Any]:
        request = {
            "capability": action["capability"],
            "params": action.get("payload", {}),
            "idempotency_key": action["id"],
            "metadata": {
                "protocol": "synergy.capability.v1",
                "source": "synergy_ai_company",
                "action_id": action["id"],
                "description": action["description"],
                "risk_class": action["risk_class"],
                "estimated_spend_usd": action.get("estimated_spend_usd", 0.0),
                "max_loss_usd": action.get("max_loss_usd", 0.0),
            },
        }
        task = self.bridge.post(self.task_path, request)
        task_id = task.get("id")
        if not task_id:
            return task
        if task.get("status") == "needs_approval" and approved_by:
            task = self.bridge.post(self.approve_path.format(task_id=task_id), {"actor": approved_by})
        if task.get("status") in {"ready", "approved"}:
            task = self.bridge.post(self.execute_path.format(task_id=task_id), {})
        return task

    def status(self, task_id: str) -> dict[str, Any]:
        return self.bridge.get(self.status_path.format(task_id=task_id))
