# Federated AUTOPILOT + NEXUS runtime

The verified integration line is now:

```text
buyer opportunity
  -> synergy_ai_company scoring/risk
  -> agi_autopilot research.validate_revenue_opportunity
  -> NEXUS memory/context
  -> safe go-to-market bundle
       AI_SALES offer
       AI_SMM plan
       AI_VIDEO storyboard
       AI_CFO economics
  -> explicit approval for any later external write / paid API
  -> external evidence
  -> synergy_financial_os canonical recognition
```

## Services

AUTOPILOT branch: `Shtenco/agi_autopilot:feat/capability-runtime-v1`

```bash
python -m pip install -e '.[test]'
python -m agi_autopilot
# 127.0.0.1:8120
```

NEXUS branch: `Shtenco/agi_nexus:feat/http-sidecar-memory-v1`

```bash
python -m pip install -e '.[http,test]'
nexus-http
# 127.0.0.1:8130
```

Auto-Company:

```bash
set -a
. config/federated.env.example
set +a
python -m company_v2.worker
```

`federated.env.example` turns on the two internal runtimes, but keeps external spend, financial execution and loss budgets at zero. AUTOPILOT itself should keep `AUTOPILOT_EXTERNAL_EFFECTS=0` until a human intentionally enables a reviewed publishing/CRM/paid-provider capability.

NEXUS memory is operational context only. Financial recognition remains in `Shtenco/synergy_financial_os`.
