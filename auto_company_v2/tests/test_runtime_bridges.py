from company_v2.adapters.autopilot import AutopilotAdapter

class FakeBridge:
    def __init__(self,status='ready'): self.calls=[]; self.initial=status
    def post(self,path,body):
        self.calls.append(('POST',path,body))
        if path=='/v1/tasks': return {'id':'t1','status':self.initial}
        if path.endswith('/approve'): return {'id':'t1','status':'approved'}
        if path.endswith('/execute'): return {'id':'t1','status':'succeeded','result':{'ok':True}}
        raise AssertionError(path)
    def get(self,path): self.calls.append(('GET',path,None)); return {'id':'t1','status':'succeeded'}

def action():
    return {'id':'a1','capability':'research.validate_revenue_opportunity','description':'validate','risk_class':'read_only','payload':{'opportunity':{'title':'x'}},'estimated_spend_usd':0,'max_loss_usd':0}

def test_ready_task_is_executed():
    b=FakeBridge('ready'); a=AutopilotAdapter(b); out=a.dispatch(action()); assert out['status']=='succeeded'; assert [x[1] for x in b.calls]==['/v1/tasks','/v1/tasks/t1/execute']; assert b.calls[0][2]['params']==action()['payload']

def test_approved_company_action_can_bridge_autopilot_approval():
    b=FakeBridge('needs_approval'); a=AutopilotAdapter(b); out=a.dispatch(action(),approved_by='synergy_ai_company:a1'); assert out['status']=='succeeded'; assert [x[1] for x in b.calls]==['/v1/tasks','/v1/tasks/t1/approve','/v1/tasks/t1/execute']
