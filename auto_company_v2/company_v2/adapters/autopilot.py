from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(slots=True)
class AutopilotAdapter:
    client: Any
    def dispatch(self, action:dict[str,Any], approved_by:str|None=None)->dict[str,Any]:
        request={"capability":action["capability"],"params":action.get("payload",{}),"idempotency_key":action["id"],"metadata":{"protocol":"synergy.capability.v1","source":"synergy_ai_company","action_id":action["id"],"description":action["description"],"risk_class":action["risk_class"],"estimated_spend_usd":action.get("estimated_spend_usd",0.0),"max_loss_usd":action.get("max_loss_usd",0.0)}}
        task=self.client.call_sync("autopilot","submit",request)
        tid=task.get("id") if isinstance(task,dict) else None
        if not tid:return task
        if task.get("status")=="needs_approval" and approved_by:
            task=self.client.call_sync("autopilot","approve",{"task_id":tid,"actor":approved_by},sensitive=True)
        if task.get("status") in {"ready","approved"}:
            task=self.client.call_sync("autopilot","execute",{"task_id":tid})
        return task
    def status(self,task_id:str)->dict[str,Any]: return self.client.call_sync("autopilot","status",{"task_id":task_id})
