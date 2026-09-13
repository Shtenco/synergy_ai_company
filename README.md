# SYNERGY AI Company 2.0

Revenue-first, risk-gated business control plane for the federated SYNERGY ecosystem.

This repository does **not** merge the other SYNERGY repositories into a monolith. It coordinates them through capability contracts while preserving the authority boundaries defined by `Shtenco/synergy_system`.

## Core topology

```text
synergy_system (architecture constitution)
        │
        ├── synergy_ai_company  ← business/revenue control plane
        │       ├── opportunity discovery + scoring
        │       ├── approvals + risk gates + kill switch
        │       ├── operational audit/events + AI-cost budget
        │       └── capability federation
        │
        ├── agi_autopilot       ← target executor (runtime not yet present on main)
        ├── agi_nexus           ← intelligence/memory proposals (no monetary authority)
        ├── synergy_financial_os← canonical accounting/profit recognition
        └── remaining repos     ← bounded capability providers
```

Start with [`AUTO_COMPANY_2.md`](AUTO_COMPANY_2.md) and [`auto_company_v2/README_AUTO_COMPANY_2.md`](auto_company_v2/README_AUTO_COMPANY_2.md).

Safe defaults: paper mode, real-money caps zero, Autopilot/NEXUS runtime adapters disabled until verified, external side effects require approval.
