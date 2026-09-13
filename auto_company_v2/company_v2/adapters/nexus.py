from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from .http_bridge import HttpJsonBridge


@dataclass(slots=True)
class NexusAdapter:
    """NEXUS semantic/episodic bridge. SQLite is operational audit only; canonical accounting remains in synergy_financial_os."""
    bridge: HttpJsonBridge
    search_path: str = "/v1/memory/search"
    upsert_path: str = "/v1/memory/upsert"

    def search(self, query: str, namespaces: list[str] | None = None, limit: int = 10) -> dict[str, Any]:
        return self.bridge.post(self.search_path, {"query": query, "namespaces": namespaces or [], "limit": limit})

    def upsert(self, key: str, content: str, namespace: str, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.bridge.post(self.upsert_path, {
            "key": key,
            "content": content,
            "namespace": namespace,
            "metadata": metadata or {},
            "source": "synergy_ai_company",
        })
