#!/usr/bin/env python3
"""Minimal stdio MCP server stub for the Lab 3 project's approved servers.

Why this exists
---------------
`.mcp.json` registers two servers the brief lists as approved, `docs-search` and
`ticket-bridge`. Neither is part of the exercise — hardening the configuration
is. But both previously caused problems of their own:

  * `ticket-bridge` pointed at a stub that exited immediately, so a session
    reported `status: failed` and students chased a non-issue.
  * `docs-search` ran `npx -y @example/docs-search-mcp`, fetching an unpinned
    package **by name over the network**. Once Node was added to the class image
    that became a live fetch, which is the wrong thing to model in a lab about
    hardening a configuration.

This stub answers enough of the protocol to connect cleanly and advertise one
harmless tool, so the servers show as connected and the lab's attention stays on
the settings.

It is deliberately dependency-free: no `mcp` package, no network, no file
access. Usage:  python3 tools/mcp_stub.py <server-name>
"""
import json
import sys

PROTOCOL_VERSION = "2024-11-05"


def reply(msg_id, result):
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": result}) + "\n")
    sys.stdout.flush()


def error(msg_id, code, message):
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": msg_id,
                                 "error": {"code": code, "message": message}}) + "\n")
    sys.stdout.flush()


def main(name):
    # Protocol goes on stdout; anything else written there breaks it. Log to stderr.
    sys.stderr.write(f"{name}: local stub, not part of the Lab 3 exercise.\n")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError:
            continue

        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            reply(msg_id, {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {}},
                "serverInfo": {"name": name, "version": "0.0.1-stub"},
            })
        elif method == "tools/list":
            reply(msg_id, {"tools": [{
                "name": "stub_status",
                "description": (f"Returns a fixed line confirming the {name} stub is "
                                "reachable. This server is a stub for the lab and does "
                                "nothing else."),
                "inputSchema": {"type": "object", "properties": {}},
            }]})
        elif method == "tools/call":
            reply(msg_id, {"content": [{
                "type": "text",
                "text": f"{name} stub reachable. No real backend is attached.",
            }]})
        elif method and method.startswith("notifications/"):
            continue  # notifications carry no id and need no reply
        elif msg_id is not None:
            error(msg_id, -32601, f"method not implemented in stub: {method}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "stub")
