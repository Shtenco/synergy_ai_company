from __future__ import annotations
from dataclasses import dataclass
import os

def _float(name,default):
    try:return float(os.getenv(name,str(default)))
    except ValueError:return default
def _bool(name,default=False):
    raw=os.getenv(name); return default if raw is None else raw.strip().lower() in {"1","true","yes","on"}
def _int(name,default):
    try:return int(os.getenv(name,str(default)))
    except ValueError:return default

@dataclass(frozen=True,slots=True)
class Settings:
    db_path:str=os.getenv("SYNERGY_COMPANY_DB","var/synergy_company.db")
    mode:str=os.getenv("SYNERGY_COMPANY_MODE","paper")
    paused:bool=os.getenv("SYNERGY_COMPANY_PAUSED","0")=="1"
    ai_daily_budget_usd:float=_float("SYNERGY_AI_DAILY_BUDGET_USD",10.0)
    max_external_spend_usd:float=_float("SYNERGY_MAX_EXTERNAL_SPEND_USD",0.0)
    max_financial_action_usd:float=_float("SYNERGY_MAX_FINANCIAL_ACTION_USD",0.0)
    max_daily_loss_usd:float=_float("SYNERGY_MAX_DAILY_LOSS_USD",0.0)
    api_token:str=os.getenv("SYNERGY_API_TOKEN","")
    bind_host:str=os.getenv("SYNERGY_BIND_HOST","127.0.0.1")
    bind_port:int=_int("SYNERGY_BIND_PORT",8788)
    autopilot_enabled:bool=_bool("SYNERGY_AUTOPILOT_ENABLED",False)
    autopilot_host:str=os.getenv("SYNERGY_AUTOPILOT_SHTTPS_HOST","127.0.0.1")
    autopilot_port:int=_int("SYNERGY_AUTOPILOT_SHTTPS_PORT",8120)
    autopilot_expected_peer:str=os.getenv("SYNERGY_AUTOPILOT_SHTTPS_EXPECTED_PEER","")
    nexus_enabled:bool=_bool("SYNERGY_NEXUS_ENABLED",False)
    nexus_host:str=os.getenv("SYNERGY_NEXUS_SHTTPS_HOST","127.0.0.1")
    nexus_port:int=_int("SYNERGY_NEXUS_SHTTPS_PORT",8130)
    nexus_expected_peer:str=os.getenv("SYNERGY_NEXUS_SHTTPS_EXPECTED_PEER","")
    shttps_timeout:float=_float("SYNERGY_SHTTPS_TIMEOUT",15.0)
