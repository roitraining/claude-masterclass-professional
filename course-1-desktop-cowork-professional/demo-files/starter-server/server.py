#!/usr/bin/env python3
"""Starter local MCP server (stdio, standard library only).

Speaks newline-delimited JSON-RPC 2.0 on stdin/stdout, the MCP stdio transport.
Implements: initialize, notifications/initialized, ping, tools/list, tools/call.

How to adapt it:
  1. Set DATA_DIR (env var STARTER_DATA, or the sample_data folder beside this file).
  2. Replace the sample tools at the bottom with your own. Each tool is a Python
     function that takes a dict of arguments and returns a string, plus a JSON
     Schema describing its inputs.
  3. Log to stderr only. Anything else written to stdout breaks the protocol.

Run the self-test (no Claude needed):  python test_server.py
"""
import csv
import json
import os
import sys
from pathlib import Path

SERVER_NAME = "starter"
SERVER_VERSION = "0.1.0"
DEFAULT_PROTOCOL = "2025-06-18"

HERE = Path(__file__).resolve().parent
_env = (os.environ.get("STARTER_DATA") or "").strip()
if _env.startswith("${"):  # an unsubstituted placeholder means the option was never set
    _env = ""
DATA_DIR = Path(_env) if _env else HERE / "sample_data"


def log(msg):
    print(f"[{SERVER_NAME}] {msg}", file=sys.stderr, flush=True)


# ---------------------------------------------------------------- tools ----
def read_records():
    path = DATA_DIR / "records.csv"
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def tool_list_records(args):
    """Return every record as id and title, one per line."""
    return "\n".join(f"{r['id']}: {r['title']}" for r in read_records())


def tool_get_record(args):
    """Return one record as JSON. Raises ValueError for an unknown id."""
    wanted = str(args.get("id", "")).strip()
    for r in read_records():
        if r["id"] == wanted:
            return json.dumps(r, indent=2)
    raise ValueError(f"No record with id '{wanted}'. Call list_records for valid ids.")


TOOLS = {
    "list_records": {
        "description": "List the ids and titles of all sample records.",
        "inputSchema": {"type": "object", "properties": {}},
        "handler": tool_list_records,
    },
    "get_record": {
        "description": "Get one sample record by id, including its last_updated date.",
        "inputSchema": {
            "type": "object",
            "properties": {"id": {"type": "string", "description": "Record id, for example R-001"}},
            "required": ["id"],
        },
        "handler": tool_get_record,
    },
}


# ------------------------------------------------------------- protocol ----
def handle(msg):
    """Return a response dict for a request, or None for a notification."""
    method = msg.get("method")
    mid = msg.get("id")
    params = msg.get("params") or {}

    if method == "initialize":
        return {"jsonrpc": "2.0", "id": mid, "result": {
            "protocolVersion": params.get("protocolVersion", DEFAULT_PROTOCOL),
            "capabilities": {"tools": {}},
            "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
        }}
    if method == "ping":
        return {"jsonrpc": "2.0", "id": mid, "result": {}}
    if method == "tools/list":
        tools = [{"name": n, "description": t["description"], "inputSchema": t["inputSchema"]}
                 for n, t in TOOLS.items()]
        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": tools}}
    if method == "tools/call":
        name = params.get("name")
        tool = TOOLS.get(name)
        if tool is None:
            return {"jsonrpc": "2.0", "id": mid,
                    "error": {"code": -32602, "message": f"Unknown tool: {name}"}}
        try:
            text = tool["handler"](params.get("arguments") or {})
            return {"jsonrpc": "2.0", "id": mid,
                    "result": {"content": [{"type": "text", "text": text}], "isError": False}}
        except Exception as exc:  # report tool failures to the model, do not crash
            log(f"tool {name} failed: {exc}")
            return {"jsonrpc": "2.0", "id": mid,
                    "result": {"content": [{"type": "text", "text": f"Error: {exc}"}], "isError": True}}
    if mid is None:
        return None  # notification such as notifications/initialized
    return {"jsonrpc": "2.0", "id": mid,
            "error": {"code": -32601, "message": f"Method not found: {method}"}}


def main():
    log(f"starting, data dir {DATA_DIR}")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            log("ignoring a line that is not JSON")
            continue
        resp = handle(msg)
        if resp is not None:
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
