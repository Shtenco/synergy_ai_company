# SYNERGY authority map

Auto-Company 2.0 follows the existing `Shtenco/synergy_system` constitution: federation instead of destructive monorepo, one authority per fact, evidence before authority, and AI proposals constrained by deterministic policy.

| Domain | Canonical owner | Auto-Company 2.0 relationship |
|---|---|---|
| Architecture / federation constitution | `synergy_system` | consume and enforce boundaries |
| Company opportunity/action orchestration | `synergy_ai_company` | authority |
| AI execution | `agi_autopilot` target | contract-only until runtime exists |
| Intelligence / inference / semantic memory | `agi_nexus` | proposal/retrieval only |
| Accounting / external-profit recognition / HardNAV | `synergy_financial_os` | canonical financial authority |
| Payments | `synergy_pay_system` | settlement capability, gated |
| Blockchain trust/state | `synergy_ai_blockchain` / chain repos | trust capability, gated |
| Trading | MIDAS / trading repos | bounded capability, never company-wide authority |
| Runtime/node orchestration | `synergy_meta_os` | infrastructure consumer/provider |
| Network | `synergynet` | transport |
| Host isolation | `turbo_linux` | host substrate |

The local SQLite `ledger` table is an **operational evidence/risk view**. It must not be presented as the ecosystem's canonical accounting ledger. Canonical revenue/profit recognition must be reconciled through `synergy_financial_os` when its integration contract is activated.
