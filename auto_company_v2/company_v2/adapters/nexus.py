from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(slots=True)
class NexusAdapter:
    client: Any
    def search(self,query:str,namespaces:list[str]|None=None,limit:int=10)->dict[str,Any]: return self.client.call_sync("nexus","memory.search",{"query":query,"namespaces":namespaces or [],"limit":limit})
    def upsert(self,key:str,content:str,namespace:str,metadata:dict[str,Any]|None=None)->dict[str,Any]: return self.client.call_sync("nexus","memory.upsert",{"key":key,"content":content,"namespace":namespace,"metadata":metadata or {},"source":"synergy_ai_company"})
