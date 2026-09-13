# Risk policy

## Default: paper company

The default configuration can research, score, plan, write local code and prepare artifacts. It cannot move real money, place live trades or sign blockchain transactions.

## Hard gates

| Action | Autonomous default | Human approval | Additional hard limit |
|---|---:|---:|---|
| Read/search | yes | no | AI daily budget |
| Local code/test | yes | no | capability allowlist |
| Send message/post/apply | no | yes | provider policy |
| Production deploy | no | yes | scoped deploy credential |
| External purchase | no | yes | external spend cap |
| Payment/transfer | no | yes | live mode + per-action cap |
| Live trading | no | yes | live mode + action cap + daily loss cap |
| Blockchain signing | no | yes | live mode + action cap + scoped signer |

## Environment limits

- `SYNERGY_AI_DAILY_BUDGET_USD`
- `SYNERGY_MAX_EXTERNAL_SPEND_USD`
- `SYNERGY_MAX_FINANCIAL_ACTION_USD`
- `SYNERGY_MAX_DAILY_LOSS_USD`

A limit of zero means **disabled**, not unlimited.

## Approval is not a magic bypass

Approval can authorize an action that policy marks `approval_required`. It cannot override:

- paper mode;
- zero/oversized financial hard cap;
- daily-loss circuit breaker;
- exhausted AI budget;
- company pause;
- missing capability transport.

## Prompt injection boundary

Any content from web pages, issues, messages, documents or social networks is untrusted data. It cannot grant permissions or instruct an executor to reveal secrets, run shell commands, alter accounts, send messages, spend money or disable controls.

Credentials stay in the provider/service environment and are never placed in opportunity descriptions or model prompts.
