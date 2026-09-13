from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from company_v2.adapters.http_bridge import HttpJsonBridge
from company_v2.core.registry import CapabilityRegistry


@dataclass(slots=True)
class FederationBus:
    """Dispatch Synergy capability envelopes without importing sibling repos.

    Only repositories with an explicit transport entry can execute. Merely being
    registered never grants process/network access.
    """
    registry: CapabilityRegistry
    transports_path: str | Path

    def _config(self) -> dict[str, Any]:
        p = Path(self.transports_path)
        if not p.exists():
            return {"repositories": {}}
        return json.loads(p.read_text(encoding="utf-8"))

    def invoke(self, repo_name: str, envelope: dict[str, Any]) -> dict[str, Any]:
        self.registry.get(repo_name)  # fail closed on unknown repos
        cfg = self._config().get("repositories", {}).get(repo_name)
        if not cfg:
            raise RuntimeError(f"no transport configured for {repo_name}")
        if cfg.get("kind") != "http":
            raise RuntimeError("only HTTP sidecars are enabled by default; CLI execution is intentionally not implicit")
        token = os.getenv(cfg.get("token_env", ""), "") if cfg.get("token_env") else ""
        bridge = HttpJsonBridge(cfg["base_url"], token)
        return bridge.post(cfg.get("invoke_path", "/v1/capabilities/invoke"), envelope)
