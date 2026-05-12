#!/usr/bin/env python3
import argparse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, List

WEAK_DESCRIPTION_TERMS = {"tool", "does stuff", "helper", "utility", "generic", "misc"}
BROAD_PERMISSION_PATTERNS = ["*", "all", "full_access", "admin", "root", "write_any", "network:any"]


def add_issue(issues: List[Dict[str, Any]], severity: str, code: str, path: str, message: str, recommendation: str):
    issues.append({
        "severity": severity,
        "code": code,
        "path": path,
        "message": message,
        "recommendation": recommendation,
    })


def validate_tool(tool: Dict[str, Any], idx: int) -> List[Dict[str, Any]]:
    issues: List[Dict[str, Any]] = []
    pfx = f"tools[{idx}]"

    for field in ["name", "description", "inputSchema"]:
        if field not in tool:
            add_issue(issues, "error", "missing_required_field", f"{pfx}.{field}", f"Missing required field '{field}'", f"Add '{field}' to the tool definition")

    desc = str(tool.get("description", "")).strip().lower()
    if desc:
        if len(desc) < 30 or desc in WEAK_DESCRIPTION_TERMS or any(term == desc for term in WEAK_DESCRIPTION_TERMS):
            add_issue(issues, "warning", "weak_description", f"{pfx}.description", "Description is too weak/short for reliable tool routing", "Provide a specific description including inputs, side effects, and constraints")

    perms = tool.get("permissions", [])
    if isinstance(perms, list):
        for perm in perms:
            perm_l = str(perm).lower()
            if any(p in perm_l for p in BROAD_PERMISSION_PATTERNS):
                add_issue(issues, "critical", "unsafe_broad_permission", f"{pfx}.permissions", f"Permission '{perm}' appears overly broad", "Scope permissions to least privilege, e.g. resource-specific read/write")
    elif perms:
        add_issue(issues, "warning", "permissions_not_list", f"{pfx}.permissions", "Permissions should be a list for auditable scope", "Use a list of explicit permission strings")

    in_schema = tool.get("inputSchema")
    if in_schema is not None:
        if not isinstance(in_schema, dict):
            add_issue(issues, "error", "invalid_input_schema", f"{pfx}.inputSchema", "inputSchema must be an object", "Provide a JSON Schema object")
        else:
            if in_schema.get("type") != "object":
                add_issue(issues, "warning", "ambiguous_input_schema", f"{pfx}.inputSchema.type", "Input schema should usually be type=object", "Set inputSchema.type to 'object'")
            props = in_schema.get("properties")
            if not isinstance(props, dict) or len(props) == 0:
                add_issue(issues, "warning", "ambiguous_input_schema", f"{pfx}.inputSchema.properties", "Input schema has no properties", "Define explicit input properties and required fields")
            if "required" not in in_schema:
                add_issue(issues, "warning", "missing_required_array", f"{pfx}.inputSchema.required", "No required array specified", "Define required fields to prevent runtime ambiguity")

    out_schema = tool.get("outputSchema")
    if out_schema is not None:
        if not isinstance(out_schema, dict):
            add_issue(issues, "error", "invalid_output_schema", f"{pfx}.outputSchema", "outputSchema must be an object", "Provide a JSON Schema object")
        else:
            if out_schema.get("type") != "object":
                add_issue(issues, "warning", "ambiguous_output_schema", f"{pfx}.outputSchema.type", "Output schema should be type=object for machine use", "Set outputSchema.type to 'object' and define properties")
            if not isinstance(out_schema.get("properties", {}), dict) or len(out_schema.get("properties", {})) == 0:
                add_issue(issues, "warning", "ambiguous_output_schema", f"{pfx}.outputSchema.properties", "Output schema has no properties", "Define stable output properties for downstream agents")

    return issues


def test_schema(doc: Dict[str, Any]) -> Dict[str, Any]:
    issues: List[Dict[str, Any]] = []
    tools = doc.get("tools")

    if not isinstance(tools, list):
        add_issue(issues, "error", "missing_tools_array", "tools", "Schema must contain a tools array", "Add tools: [] with MCP tool definitions")
        tools = []

    for i, tool in enumerate(tools):
        if not isinstance(tool, dict):
            add_issue(issues, "error", "invalid_tool_definition", f"tools[{i}]", "Tool definition must be an object", "Replace with an object containing name/description/inputSchema")
            continue
        issues.extend(validate_tool(tool, i))

    summary = {
        "total_issues": len(issues),
        "critical": sum(1 for x in issues if x["severity"] == "critical"),
        "error": sum(1 for x in issues if x["severity"] == "error"),
        "warning": sum(1 for x in issues if x["severity"] == "warning"),
        "pass": len([x for x in issues if x["severity"] in {"critical", "error"}]) == 0,
    }
    return {"summary": summary, "issues": issues}


class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, payload: Dict[str, Any]):
        b = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_POST(self):
        if self.path != "/v1/mcp/schema/test":
            return self._send(404, {"error": "not_found"})
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)
        try:
            data = json.loads(raw.decode("utf-8"))
        except Exception:
            return self._send(400, {"error": "invalid_json"})
        result = test_schema(data)
        return self._send(200, result)


def run_cli(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(json.dumps(test_schema(data), indent=2))


def run_server(port: int):
    srv = HTTPServer(("0.0.0.0", port), Handler)
    print(json.dumps({"ok": True, "service": "mcp-schema-tester", "port": port}))
    srv.serve_forever()


def main():
    ap = argparse.ArgumentParser(description="MCP Schema Tester")
    ap.add_argument("--file", help="Path to MCP schema JSON file")
    ap.add_argument("--serve", action="store_true", help="Run HTTP API server")
    ap.add_argument("--port", type=int, default=8791)
    args = ap.parse_args()

    if args.file:
        run_cli(args.file)
    elif args.serve:
        run_server(args.port)
    else:
        ap.error("Use --file <path> or --serve")


if __name__ == "__main__":
    main()
