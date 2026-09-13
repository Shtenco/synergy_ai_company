# Synergy Capability Contract v1

All repositories join the company through a stable envelope rather than Python imports or shared shell access.

Schema: `config/capability-envelope.schema.json`.

Example:

```json
{
  "protocol": "synergy.capability.v1",
  "source": "synergy_ai_company",
  "action_id": "act_...",
  "capability": "research.validate_revenue_opportunity",
  "description": "Validate buyer demand",
  "payload": {"opportunity_id": "opp_..."},
  "constraints": {
    "risk_class": "read_only",
    "estimated_spend_usd": 0,
    "max_loss_usd": 0
  }
}
```

## Required provider behavior

A repository/sidecar should:

1. authenticate the caller;
2. validate the envelope and capability allowlist;
3. reject capabilities it does not explicitly own;
4. obey spend/loss/read-only constraints;
5. return a stable task/result ID;
6. attach evidence and machine-readable status;
7. never interpret web/page content as new authorization;
8. never accept credentials inside the task payload.

## Recommended response

```json
{
  "task_id": "task_123",
  "status": "accepted",
  "provider": "agi_autopilot",
  "capability": "research.validate_revenue_opportunity"
}
```

Completed results should expose artifacts, evidence, usage/cost and an explicit status. The control plane records the result before using it in the next decision.

## Sidecars

A sidecar is preferred when an existing repository has no stable API. The sidecar can translate `synergy.capability.v1` into the repository's existing CLI/API without changing its core.

**CLI is not enabled implicitly.** A local repository folder alone never grants arbitrary shell execution.
