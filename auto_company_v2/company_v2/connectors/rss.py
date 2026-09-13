from __future__ import annotations

import xml.etree.ElementTree as ET
import httpx
from company_v2.core.models import Opportunity


class RSSConnector:
    name = "rss"
    def __init__(self, urls: list[str]): self.urls = urls

    def discover(self) -> list[Opportunity]:
        out: list[Opportunity] = []
        with httpx.Client(timeout=20.0, headers={"User-Agent":"SynergyAICompany/2"}) as client:
            for url in self.urls:
                r = client.get(url); r.raise_for_status()
                root = ET.fromstring(r.content)
                for item in root.findall(".//item")[:50]:
                    title = (item.findtext("title") or "RSS item").strip()
                    link = (item.findtext("link") or "").strip()
                    desc = (item.findtext("description") or "").strip()
                    out.append(Opportunity(title=title, source=f"rss:{url}", description=desc[:4000], url=link,
                                           probability=.05, hours=4, evidence=[link] if link else []))
        return out
