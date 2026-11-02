#!/usr/bin/env python3
"""Self-test for a stdio MCP server. Starts server.py as Claude would and calls it.

Usage:  python test_server.py [path-to-server.py]
Set the data folder first if your server needs one, for example STARTER_DATA.
Prints PASS or FAIL for each check and exits non-zero on any failure.
"""
import json
import subprocess
import sys
from pathlib import Path

server = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("server.py")
proc = subprocess.Popen([sys.executable, str(server)], stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
failures = 0


def rpc(mid, method, params=None):
    msg = {"jsonrpc": "2.0", "id": mid, "method": method}
    if params is not None:
        msg["params"] = params
    proc.stdin.write(json.dumps(msg) + "\n")
    proc.stdin.flush()
    return json.loads(proc.stdout.readline())


def check(label, ok):
    global failures
    print(("PASS  " if ok else "FAIL  ") + label)
    failures += 0 if ok else 1


r = rpc(1, "initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                          "clientInfo": {"name": "selftest", "version": "0"}})
check("initialize returns serverInfo", "serverInfo" in r.get("result", {}))
proc.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n")
proc.stdin.flush()

r = rpc(2, "tools/list")
tools = r.get("result", {}).get("tools", [])
check(f"tools/list returns {len(tools)} tool(s)", len(tools) > 0)
check("every tool has a description and an inputSchema",
      all(t.get("description") and t.get("inputSchema") for t in tools))
for t in tools:
    print(f"      - {t['name']}: {t['description']}")

if tools:
    first = tools[0]
    required = first["inputSchema"].get("required", [])
    if not required:
        r = rpc(3, "tools/call", {"name": first["name"], "arguments": {}})
        res = r.get("result", {})
        check(f"tools/call {first['name']} returns text without error",
              res.get("isError") is False and res.get("content", [{}])[0].get("text"))

r = rpc(4, "tools/call", {"name": "no_such_tool", "arguments": {}})
check("unknown tool returns a JSON-RPC error", "error" in r)

proc.stdin.close()
proc.wait(timeout=5)
print("\nAll checks passed." if not failures else f"\n{failures} check(s) failed.")
sys.exit(1 if failures else 0)
