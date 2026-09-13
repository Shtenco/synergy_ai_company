# AI Autopilot integration

## Verified current state (2026-09-13)

The connected `Shtenco/agi_autopilot` `main` branch currently contains only `README.md` (`# agi_autopilot`). No executable service, task API, CLI contract or MCP server is present on that branch.

Therefore Auto-Company 2.0 **does not pretend an API exists**. `SYNERGY_AUTOPILOT_ENABLED=0` is the fail-closed default.

## Target role

Autopilot is the execution engine of the federation. `synergy_ai_company` decides **what may be done and under which budget/risk/approval envelope**; Autopilot may decide **how to execute that already-scoped task**.

The future compatibility contract is `synergy.capability.v1`:

- task submit: configurable `SYNERGY_AUTOPILOT_TASK_PATH`;
- task status: configurable `SYNERGY_AUTOPILOT_STATUS_PATH`;
- usage/cost must be returned to the company audit store;
- Autopilot may not expand its own capability or monetary scope;
- an executor sidecar is preferred over importing internals into this repository.

## Activation gate

Only after `agi_autopilot` exposes a reviewed runtime or sidecar:

```bash
SYNERGY_AUTOPILOT_ENABLED=1
SYNERGY_AUTOPILOT_URL=http://127.0.0.1:8120
SYNERGY_AUTOPILOT_TASK_PATH=/v1/tasks
SYNERGY_AUTOPILOT_STATUS_PATH=/v1/tasks/{task_id}
```

Until then, dispatch fails closed with `AI Autopilot adapter is not configured`. Research/opportunity ingestion, scoring, approvals, registry and audit functions can still run.
