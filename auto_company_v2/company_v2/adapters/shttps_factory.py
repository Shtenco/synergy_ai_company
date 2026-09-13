from __future__ import annotations
from shttps.bootstrap import production_context
from shttps.errors import ProviderUnavailable
from shttps.transport import SHTTPSRPCClient


def build_company_clients(settings):
    ctx=production_context("SYNERGY_COMPANY",roles=("AUTO_COMPANY",))

    def expected(repository_name:str, legacy_node_id:str)->set[str]:
        if ctx.federation is not None:
            ids={str(n["node_id"]) for n in ctx.federation.accepted_nodes(repository_name)}
            if not ids:
                raise ProviderUnavailable(f"no accepted SHTTPS nodes for {repository_name}")
            if legacy_node_id and legacy_node_id not in ids:
                raise ProviderUnavailable(f"configured legacy node_id is not active/retiring for {repository_name}")
            return ids
        if legacy_node_id:
            return {legacy_node_id}
        raise ProviderUnavailable("legacy trust mode requires explicit expected peer node_id")

    autopilot=SHTTPSRPCClient(settings.autopilot_host,settings.autopilot_port,ctx.provider,ctx.identity,ctx.trust,ctx.config,compression=ctx.compression,expected_peer_node_ids=expected("agi_autopilot",settings.autopilot_expected_peer),timeout=settings.shttps_timeout)
    nexus=SHTTPSRPCClient(settings.nexus_host,settings.nexus_port,ctx.provider,ctx.identity,ctx.trust,ctx.config,compression=ctx.compression,expected_peer_node_ids=expected("agi_nexus",settings.nexus_expected_peer),timeout=settings.shttps_timeout)
    return autopilot,nexus
