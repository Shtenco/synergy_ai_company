from __future__ import annotations

import os
import httpx
from company_v2.core.models import Opportunity


class GitHubIssuesConnector:
    name = "github_issues"

    def __init__(self, query: str | None = None, token: str | None = None):
        self.query = query or os.getenv("GITHUB_SEARCH_QUERY", 'is:issue is:open label:"help wanted" no:assignee')
        self.token = token if token is not None else os.getenv("GITHUB_TOKEN", "")

    def discover(self) -> list[Opportunity]:
        headers = {"Accept": "application/vnd.github+json", "User-Agent": "SynergyAICompany/2"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        with httpx.Client(timeout=20.0, headers=headers) as client:
            r = client.get("https://api.github.com/search/issues", params={"q": self.query, "sort": "created", "order": "desc", "per_page": 30})
            r.raise_for_status()
            items = r.json().get("items", [])
        out: list[Opportunity] = []
        for x in items:
            labels = [l.get("name", "") for l in x.get("labels", [])]
            out.append(Opportunity(
                title=x.get("title", "GitHub issue"),
                source=self.name,
                description=(x.get("body") or "")[:4000],
                url=x.get("html_url", ""),
                probability=0.15,
                expected_revenue_usd=0.0,
                estimated_cost_usd=0.0,
                hours=4.0,
                evidence=[x.get("html_url", "")],
                tags=[t for t in labels if t],
            ))
        return out
