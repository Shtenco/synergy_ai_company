from __future__ import annotations

from dataclasses import dataclass
from typing import Any
import httpx


@dataclass(slots=True)
class HttpJsonBridge:
    base_url: str
    token: str = ""
    timeout: float = 30.0

    def _headers(self) -> dict[str, str]:
        h = {"Accept": "application/json", "Content-Type": "application/json"}
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h

    def post(self, path: str, body: dict[str, Any]) -> dict[str, Any]:
        with httpx.Client(base_url=self.base_url, headers=self._headers(), timeout=self.timeout) as client:
            r = client.post(path, json=body)
            r.raise_for_status()
            return r.json()

    def get(self, path: str) -> dict[str, Any]:
        with httpx.Client(base_url=self.base_url, headers=self._headers(), timeout=self.timeout) as client:
            r = client.get(path)
            r.raise_for_status()
            return r.json()
