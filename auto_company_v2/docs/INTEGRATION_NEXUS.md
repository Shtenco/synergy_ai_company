# NEXUS integration

## Verified current state (2026-09-13)

`Shtenco/agi_nexus` is the canonical NEXUS intelligence core and currently contains architecture, generation/record directories and benchmark/migration artifacts. Its README explicitly defines NEXUS as an inference/forecast/hypothesis/policy/risk reasoning engine and explicitly withholds financial authorization, payment authority, ledger mutation, blockchain consensus, production deployment and scientific-truth authority.

No verified HTTP inference or memory service is exposed on the checked `main` branch. Therefore `SYNERGY_NEXUS_ENABLED=0` is the default and `/v1/nexus/search` returns 503 until a reviewed runtime or sidecar is configured.

## Correct authority boundary

Memory hierarchy:

1. Auto-Company operational audit/event store — actions, approvals, opportunity evidence, AI usage.
2. NEXUS — semantic/episodic retrieval, inference, risk and policy proposals.
3. `synergy_financial_os` — canonical accounting and economic fact recognition.
4. payment/blockchain repositories — settlement/trust in their own authority domains.

NEXUS retrieval can influence a proposal; it can never itself authorize money or mutate canonical accounting.

## Future activation

After NEXUS exposes a versioned API or reviewed sidecar:

```bash
SYNERGY_NEXUS_ENABLED=1
SYNERGY_NEXUS_URL=http://127.0.0.1:8130
SYNERGY_NEXUS_SEARCH_PATH=/v1/memory/search
SYNERGY_NEXUS_UPSERT_PATH=/v1/memory/upsert
```

The adapter stays intentionally thin so the NEXUS repository remains the intelligence authority instead of being copied into the company repo.
