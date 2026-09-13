# Synergy AI Company 2.0

Revenue-first, risk-gated control plane for the 51-repository `Shtenco` Synergy federation.

This is deliberately **not** a monorepo merge. Existing repositories remain independently deployable. `synergy_ai_company` becomes the company control plane and talks to them through `synergy.capability.v1` adapters/sidecars.

## Core roles

- **synergy_ai_company** — CEO/Risk/Revenue control plane, operational audit log, approvals and opportunity pipeline; it is not the canonical accounting ledger.
- **agi_autopilot** — target execution engine. Its current `main` has no verified runtime API, so the adapter is disabled by default and activates only after a reviewed sidecar/API exists.
- **agi_nexus** — intelligence/semantic-memory proposal layer. Its current `main` has no verified HTTP runtime; it never receives monetary/accounting authority.
- **the other 49 repositories** — federated capability providers registered in `config/repositories.json`.

## The revenue loop

`Discover → Normalize → Score → Validate → Propose → Risk Gate → Execute → Verify → Ledger → Learn`

The crucial invariant is: **predicted revenue is never treated as realized revenue**. Local revenue evidence requires an external reference; canonical accounting recognition belongs to `synergy_financial_os`.

## Safe defaults

- `SYNERGY_COMPANY_MODE=paper`
- real-money actions are hard-disabled in paper mode
- external side effects require human approval
- per-action financial cap defaults to zero
- daily loss cap defaults to zero
- API binds to loopback unless an API token is configured
- AI spend has a daily circuit breaker
- web/research tasks explicitly treat external content as untrusted data
- repositories do not receive permissions merely because they are present in the registry

## Quick start

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
cp .env.example .env
synergy-company init
pytest
python scripts/run_api.py
```

In another shell:

```bash
python -m company_v2.worker
```

Optional Telegram controller:

```bash
export TELEGRAM_BOT_TOKEN=...
export TELEGRAM_ALLOWED_CHAT_IDS=123456789
python -m company_v2.telegram.bot
```

## AI Autopilot

Current checked `main` is contract-only. After a reviewed runtime/sidecar exists, set:

```bash
SYNERGY_AUTOPILOT_ENABLED=1
```

Then set:

```bash
SYNERGY_AUTOPILOT_URL=http://127.0.0.1:8120
SYNERGY_AUTOPILOT_TASK_PATH=/v1/tasks
```

If Autopilot exposes another route, change the path — the company does not import Autopilot internals.

## Nexus

Current checked `main` exposes architecture/artifacts but no verified HTTP service. After a reviewed runtime/sidecar exists, set:

```bash
SYNERGY_NEXUS_ENABLED=1
```

Then set:

```bash
SYNERGY_NEXUS_URL=http://127.0.0.1:8130
SYNERGY_NEXUS_SEARCH_PATH=/v1/memory/search
SYNERGY_NEXUS_UPSERT_PATH=/v1/memory/upsert
```

A compatibility sidecar can be used if Nexus currently has a different API.

## Telegram commands

`/status`, `/opportunities`, `/approve ID`, `/reject ID`, `/dispatch ID`, `/pause`, `/resume`, `/repos`.

Approval and dispatch are separate on purpose. An accidental `/approve` does not execute the action.

## Where to read next

- `docs/AUTO_COMPANY_2_ARCHITECTURE.md`
- `docs/CAPABILITY_CONTRACT.md`
- `docs/RISK_POLICY.md`
- `docs/REVENUE_LOOP.md`
- `docs/INTEGRATION_AI_AUTOPILOT.md`
- `docs/INTEGRATION_NEXUS.md`
- `docs/REPO_FEDERATION_51.md`
- `docs/AUTHORITY_MAP.md`
