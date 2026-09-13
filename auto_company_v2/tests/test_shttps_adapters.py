from company_v2.adapters.autopilot import AutopilotAdapter
from company_v2.adapters.nexus import NexusAdapter
class Fake:
    def __init__(self):self.calls=[]
    def call_sync(self,s,m,p,**kw):
        self.calls.append((s,m,p,kw))
        if m=="submit":return {"id":"t1","status":"ready"}
        if m=="execute":return {"id":"t1","status":"succeeded"}
        if m=="memory.search":return {"items":[]}
        if m=="memory.upsert":return {"ok":True}
        return {"id":"t1","status":"ready"}
def test_autopilot_uses_shttps_methods():
    f=Fake(); out=AutopilotAdapter(f).dispatch({"id":"a1","capability":"cfo.analyze_budget","payload":{},"description":"x","risk_class":"READ_ONLY"}); assert out["status"]=="succeeded"; assert [x[1] for x in f.calls]==["submit","execute"]
def test_nexus_uses_shttps_methods():
    f=Fake(); n=NexusAdapter(f); n.search("x"); n.upsert("k","v","n"); assert [x[1] for x in f.calls]==["memory.search","memory.upsert"]
