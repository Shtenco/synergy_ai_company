from __future__ import annotations
from shttps.bootstrap import production_stack
from shttps.transport import SHTTPSRPCClient

def build_company_clients(settings):
    provider,identity,trust,compression,config=production_stack("SYNERGY_COMPANY",roles=("AUTO_COMPANY",))
    autopilot=SHTTPSRPCClient(settings.autopilot_host,settings.autopilot_port,provider,identity,trust,config,compression=compression,expected_peer_node_id=settings.autopilot_expected_peer or None,timeout=settings.shttps_timeout)
    nexus=SHTTPSRPCClient(settings.nexus_host,settings.nexus_port,provider,identity,trust,config,compression=compression,expected_peer_node_id=settings.nexus_expected_peer or None,timeout=settings.shttps_timeout)
    return autopilot,nexus
