import tempfile
from company_v2.core.models import ProposedAction,RiskClass
from company_v2.core.orchestrator import Orchestrator
from company_v2.core.risk import RiskPolicy
from company_v2.core.store import Store

class FakeAutopilot:
    def dispatch(self,action,approved_by=None): return {'id':'t','status':'succeeded','approved_by':approved_by}

def make_store():
    f=tempfile.NamedTemporaryFile(suffix='.db',delete=False); f.close(); return Store(f.name)

def test_external_human_approval_promotes_action():
    s=make_store(); a=ProposedAction(kind='send',description='send approved message',capability='telegram.send_message',risk_class=RiskClass.EXTERNAL,payload={'text':'hello'})
    RiskPolicy().apply(a); s.save_action(a.to_dict()); assert a.state.value=='approval_required'
    s.approve(a.id,'approved','owner','ok')
    out=Orchestrator(s,RiskPolicy(),FakeAutopilot()).dispatch_by_id(a.id)
    assert out['status']=='succeeded'; assert out['approved_by'].startswith('synergy_ai_company:')

def test_human_approval_cannot_override_paper_money_block():
    s=make_store(); a=ProposedAction(kind='pay',description='pay',capability='payment.execute',risk_class=RiskClass.FINANCIAL,estimated_spend_usd=1)
    RiskPolicy().apply(a); s.save_action(a.to_dict()); s.approve(a.id,'approved','owner','try')
    try: Orchestrator(s,RiskPolicy(),FakeAutopilot()).dispatch_by_id(a.id)
    except PermissionError: pass
    else: raise AssertionError('paper-mode financial action must stay blocked')
