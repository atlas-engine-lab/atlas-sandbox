# MCP Schema Tester (Agent Reliability Suite)

Deterministic scanner for MCP tool schema reliability risks.

## What it detects
- Missing required fields in tool definitions
- Weak descriptions that break tool routing
- Unsafe broad permissions
- Ambiguous input/output schemas

## CLI usage
```bash
python mcp_schema_tester.py --file examples/failing_schema.json
python mcp_schema_tester.py --file examples/fixed_schema.json
```

## API usage
```bash
python mcp_schema_tester.py --serve --port 8791
curl -s -X POST http://localhost:8791/v1/mcp/schema/test \
  -H 'Content-Type: application/json' \
  --data @examples/failing_schema.json
```

## Concrete paid use-case
A hosted CI gate for MCP tools that blocks deploys when critical schema or permission risks are found, priced per scan. This prevents expensive agent-chain failures in production.

## Measurable utility
- `critical + error` issue count per schema
- pass/fail deploy gate signal
- trend in failures prevented before production deploy
