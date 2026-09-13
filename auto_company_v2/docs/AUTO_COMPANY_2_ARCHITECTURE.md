# Auto-Company 2.0 architecture

## Objective

Turn the Synergy ecosystem into an autonomous **revenue-seeking operating system** without turning 51 repositories into one fragile monolith.

The company optimizes for **verified realized profit**, not the amount of generated code, number of agent messages, or speculative revenue.

## Control-plane architecture

```text
                       Human / Telegram
                              |
                       Approval + Kill switch
                              |
                  +-----------v-----------+
                  | synergy_ai_company 2.0 |
                  | CEO / CFO / Risk / Rev |
                  +----+-------------+-----+
                       |             |
               audited |             | semantic
                events |             | memory
                       v             v
                SQLite/Postgres   agi_nexus
                       |
                       | approved capability envelope
                       v
                  agi_autopilot
                       |
                 execution planner
                       |
      +----------------+-----------------------------+
      |                |               |             |
   ai_coder       synergy_app    finance repos   trading repos ...
      |                |               |             |
      +----------------+---------------+-------------+
                       |
               result + evidence
                       |
                       v
             Verification / Ledger
```

## Why federation instead of a monorepo

1. Every existing project keeps its own lifecycle, dependencies, tests and release cadence.
2. A broken trading robot cannot break the memory system simply because it shares imports.
3. Credentials are scoped by service rather than copied into one giant runtime.
4. Risk classes can be assigned at the repository boundary.
5. `synergy_ai_company` can orchestrate old and new implementations behind a stable protocol.

## Runtime layers

### 1. Opportunity plane

Sources produce normalized `Opportunity` objects. The first implementation includes GitHub issues plus an Autopilot revenue-scout task and a generic webhook. More sources can enter through public/official APIs, RSS, connected tools or a sidecar.

### 2. Decision plane

Each opportunity is ranked by evidence, expected value, probability and time-to-test. The score is a prioritization heuristic, **not** a claim of profitability.

### 3. Risk plane

Every executable action has one of:

- `read_only`
- `code_write`
- `external_side_effect`
- `financial`
- `trading`
- `blockchain`

The risk engine runs before dispatch. Money/signing categories are disabled in paper mode and have hard caps in live mode.

### 4. Execution plane

`agi_autopilot` is the preferred executor. The company sends an envelope, never unrestricted prose plus implicit machine access. Autopilot can delegate to the specialized repository that owns the requested capability.

### 5. Memory plane

Local database = immutable-ish operational audit/state.

Nexus = semantic recall, knowledge compaction, experiment lessons and cross-project context.

If Nexus is down, financial/audit state is not lost and execution can fail closed.

### 6. Financial plane

There are three separate concepts:

- forecast/expected revenue on an opportunity;
- receivable or accepted work;
- realized revenue backed by payment/invoice/transaction evidence.

The local control plane may track the last item as operational revenue evidence, but canonical revenue/profit recognition is owned by `synergy_financial_os`.

## Agent organization

Agent definitions live in `config/agents.json`. Agents are **policy roles**, not magical independent processes. Autopilot may instantiate them as separate model sessions, but permissions come from capabilities and risk gates, not from role names.

## Failure model

- connector failure → event logged, other connectors continue;
- Nexus failure → semantic memory degraded, audit state remains;
- Autopilot failure → no action is marked successful;
- AI budget exhausted → dispatch circuit breaker;
- daily loss threshold reached → loss-bearing actions blocked;
- pause flag → worker stops dispatching;
- missing transport → repository remains registered but non-executable.
