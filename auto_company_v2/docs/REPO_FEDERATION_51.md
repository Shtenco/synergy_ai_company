# Federation map — 51 Shtenco repositories

Every repository is registered as a capability provider. `enabled=true` means it is part of the federation registry; **execution still requires an explicit transport configuration and risk approval**.

| # | Repository | Domain | Role | Risk class | Integration |
|---:|---|---|---|---|---|
| 1 | `binary_quantum_theory` | research | research_provider | `read_only` | `synergy.capability.v1` |
| 2 | `ai_language` | ai_core | language_engine | `code_write` | `synergy.capability.v1` |
| 3 | `synergy_pay_system` | payments | payment_provider | `financial` | `synergy.capability.v1` |
| 4 | `synergy_system` | core | platform_core | `code_write` | `synergy.capability.v1` |
| 5 | `midas_ai` | trading | market_agent | `trading` | `synergy.capability.v1` |
| 6 | `agi_olga` | agents | specialist_agent | `code_write` | `synergy.capability.v1` |
| 7 | `synergy_financial_os` | finance | finance_os | `financial` | `canonical_accounting:contract_or_sidecar` |
| 8 | `synergy_graph_print_money` | revenue | revenue_research | `trading` | `synergy.capability.v1` |
| 9 | `ai_financial_system` | finance | finance_provider | `financial` | `synergy.capability.v1` |
| 10 | `ai_compress` | infrastructure | compression_provider | `code_write` | `synergy.capability.v1` |
| 11 | `synergy_meta_os` | core | meta_os | `code_write` | `synergy.capability.v1` |
| 12 | `crypto_pump` | trading | market_strategy | `trading` | `synergy.capability.v1` |
| 13 | `turbo_linux` | infrastructure | runtime_os | `code_write` | `synergy.capability.v1` |
| 14 | `midas_ai_trading_system` | trading | trading_provider | `trading` | `synergy.capability.v1` |
| 15 | `synergychain.github.io` | frontend | chain_site | `external_side_effect` | `synergy.capability.v1` |
| 16 | `synergychain` | blockchain | chain_provider | `blockchain` | `synergy.capability.v1` |
| 17 | `agi_nexus` | memory | memory | `code_write` | `contract_only:inference_memory_sidecar_required` |
| 18 | `qr_compress` | infrastructure | compression_provider | `code_write` | `synergy.capability.v1` |
| 19 | `synergynet` | network | network_provider | `external_side_effect` | `synergy.capability.v1` |
| 20 | `synergy_ai_blockchain` | blockchain | ai_chain_provider | `blockchain` | `synergy.capability.v1` |
| 21 | `cold_nuclear` | research | research_provider | `read_only` | `synergy.capability.v1` |
| 22 | `synergy_app` | app | app_provider | `external_side_effect` | `synergy.capability.v1` |
| 23 | `usds` | finance | asset_provider | `financial` | `synergy.capability.v1` |
| 24 | `cashero` | finance | finance_app | `financial` | `synergy.capability.v1` |
| 25 | `shtencoauantai.github.io` | frontend | website | `external_side_effect` | `synergy.capability.v1` |
| 26 | `blochain_budget` | finance | budget_provider | `financial` | `synergy.capability.v1` |
| 27 | `dlp_solver` | research | math_provider | `read_only` | `synergy.capability.v1` |
| 28 | `synergy_eurasian` | app | regional_provider | `external_side_effect` | `synergy.capability.v1` |
| 29 | `synergy_project` | core | project_provider | `code_write` | `synergy.capability.v1` |
| 30 | `nexus_science_agent` | research | science_agent | `read_only` | `synergy.capability.v1` |
| 31 | `ai_trade_terminal` | trading | trade_terminal | `trading` | `synergy.capability.v1` |
| 32 | `3D_bars_market_structure` | trading | market_analytics | `read_only` | `synergy.capability.v1` |
| 33 | `motherboard_xpu_xml` | infrastructure | hardware_provider | `code_write` | `synergy.capability.v1` |
| 34 | `agi_autopilot` | execution | executor | `code_write` | `contract_only:executor_sidecar_required` |
| 35 | `synergy_metachain` | blockchain | chain_provider | `blockchain` | `synergy.capability.v1` |
| 36 | `ai_coder` | development | coder | `code_write` | `synergy.capability.v1` |
| 37 | `print_money_synergychain` | revenue | chain_revenue | `blockchain` | `synergy.capability.v1` |
| 38 | `synergy_matrix_sota` | ai_core | model_provider | `code_write` | `synergy.capability.v1` |
| 39 | `sinergy-super-app` | app | super_app | `external_side_effect` | `synergy.capability.v1` |
| 40 | `midas_lite` | trading | market_agent | `trading` | `synergy.capability.v1` |
| 41 | `computer_vision_trading_metatrader_5` | trading | cv_trading | `trading` | `synergy.capability.v1` |
| 42 | `multi_threaded_trading_robot_with_machine_learning_python` | trading | ml_trading | `trading` | `synergy.capability.v1` |
| 43 | `cross_forex_arbitrage_trading_metatrader_5` | trading | arbitrage_provider | `trading` | `synergy.capability.v1` |
| 44 | `swap_arbitrage_metatrader_5` | trading | arbitrage_provider | `trading` | `synergy.capability.v1` |
| 45 | `global_liquidity_dataminer` | data | market_data | `read_only` | `synergy.capability.v1` |
| 46 | `shtenco.github.io` | frontend | website | `external_side_effect` | `synergy.capability.v1` |
| 47 | `synergy_chain_print_money` | revenue | chain_revenue | `blockchain` | `synergy.capability.v1` |
| 48 | `synergy_app_family` | app | family_app | `external_side_effect` | `synergy.capability.v1` |
| 49 | `algotrading_graph_system` | trading | trading_analytics | `trading` | `synergy.capability.v1` |
| 50 | `sinergy_app` | app | app_provider | `external_side_effect` | `synergy.capability.v1` |
| 51 | `quantum-trading_metatrader5` | trading | quant_trading | `trading` | `synergy.capability.v1` |

## Central topology

- `synergy_ai_company` (this repository): company control plane.
- `agi_autopilot`: target execution/planning provider; current checked `main` has no verified runtime, so execution remains disabled until a reviewed sidecar/API exists.
- `agi_nexus`: intelligence and semantic/episodic memory proposal provider; current checked `main` has no verified HTTP runtime and has no monetary/accounting authority.
- Every other repository: federated provider behind `synergy.capability.v1`.

## High-risk domains

Trading, finance, payments and blockchain repositories remain useful in paper/simulation/read-only modes, but real-money and signing operations are disabled by default and require both live-mode hard caps and human approval.
