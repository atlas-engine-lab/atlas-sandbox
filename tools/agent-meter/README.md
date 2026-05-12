# Agent Meter (Prototype)

Agent-facing API to score output usefulness and catch low-value responses before delivery.

## Why this exists
Agents and developers need fast QA gates that are cheaper than full human review.

## MVP endpoints
- `GET /health`
- `POST /v1/validate`

## Run
```bash
pip install -r requirements.txt
python -m uvicorn app:app --host 0.0.0.0 --port 8787
```

## Monetization path
- Free tier: limited requests/day
- Paid tier: per-request billing via x402/USDC (when approved infra is ready)
