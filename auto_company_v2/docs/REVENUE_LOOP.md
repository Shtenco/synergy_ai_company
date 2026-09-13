# Revenue loop

## 1. Discover

Revenue Scout searches configured sources for fresh buyer demand. Prefer explicit budget, bounty, escrow, payment verification, named deliverable and deadline.

## 2. Normalize

Every lead becomes an `Opportunity` with source, URL, evidence, estimated value/cost, probability and time estimate.

## 3. Score

Prioritize fast, evidenced, positive-EV experiments. Unknown budget or no evidence lowers confidence; it does not become fake revenue.

## 4. Validate

A read-only Autopilot task checks:

- Is there a real buyer?
- Is the request still open?
- Is payment/budget evidenced?
- Can one of the 51 repositories create an advantage?
- What is the smallest deliverable that can be paid for?
- What concrete next action tests willingness to pay?

## 5. Propose

Sales/Product/Engineering prepare a proposal, demo, patch or MVP. Preparing is distinct from sending/publishing.

## 6. Risk gate

External communication, production deployment and any money/signing action go to approval according to `docs/RISK_POLICY.md`.

## 7. Execute via AI Autopilot

Autopilot receives the approved capability envelope and delegates to the relevant provider repository.

## 8. Verify

QA verifies deliverable acceptance criteria. Financial verification records payment evidence separately.

## 9. Evidence + canonical accounting

Forecast is never booked as revenue. A local `revenue` evidence event requires `external_ref` plus evidence, but it is still an operational observation. Canonical revenue/profit recognition belongs to `synergy_financial_os` after its own evidence validation and accounting rules.

## 10. Learn through Nexus

Nexus stores reusable lessons: source quality, buyer objections, successful proposals, delivery estimates, failed hypotheses and repo-specific strengths. Sensitive credentials and payment secrets do not enter semantic memory.

## Portfolio reward

The company should optimize over time for:

```text
canonical_recognized_profit (when Financial OS integration is active)
- refunds
- verified external costs
- AI/model costs
- risk penalties
- opportunity cost of engineer time
```

Not for commits, tokens, agent activity or theoretical gross revenue.
