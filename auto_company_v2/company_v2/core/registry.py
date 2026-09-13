from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class RepoCapability:
    name: str
    repo: str
    domain: str
    risk_class: str
    role: str
    integration: str
    enabled: bool


class CapabilityRegistry:
    def __init__(self, path: str | Path):
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        self.version = raw["version"]
        self.items = [RepoCapability(**item) for item in raw["repositories"]]

    def get(self, name: str) -> RepoCapability:
        for item in self.items:
            if item.name == name:
                return item
        raise KeyError(name)

    def enabled(self) -> list[RepoCapability]:
        return [x for x in self.items if x.enabled]

    def by_domain(self, domain: str) -> list[RepoCapability]:
        return [x for x in self.items if x.domain == domain]

    def summary(self) -> dict[str, Any]:
        domains: dict[str, int] = {}
        risks: dict[str, int] = {}
        for x in self.items:
            domains[x.domain] = domains.get(x.domain, 0) + 1
            risks[x.risk_class] = risks.get(x.risk_class, 0) + 1
        return {"total": len(self.items), "enabled": len(self.enabled()), "domains": domains, "risk_classes": risks}
