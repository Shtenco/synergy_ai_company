# Auto-Company 2.0 integration

The new revenue-first company control plane is contained in [`auto_company_v2/`](auto_company_v2/README_AUTO_COMPANY_2.md) so it can coexist with the current `synergy_ai_company` implementation without destructive rewrites.

Key integration points:

- `agi_autopilot` → execution engine;
- `agi_nexus` → long-term semantic memory;
- all 51 Shtenco repositories → `config/repositories.json` capability federation;
- Telegram → human control/approvals/kill switch;
- SQLite operational audit/evidence store → actions, approvals, AI costs and local revenue evidence; canonical accounting remains in `synergy_financial_os`;
- default mode → paper/no real-money execution.

Run tests:

```bash
cd auto_company_v2
pip install -e '.[dev]'
pytest
```

Start API/worker:

```bash
python scripts/run_api.py
python -m company_v2.worker
```
