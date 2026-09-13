from __future__ import annotations

from typing import Protocol
from company_v2.core.models import Opportunity


class OpportunityConnector(Protocol):
    name: str
    def discover(self) -> list[Opportunity]: ...
