#!/usr/bin/env python3
"""Expense connector (stdio MCP, standard library only). Fictional data."""
import csv
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ["EXPENSE_DATA_DIR"])  # raises KeyError if the option was never set
CONFIG = json.loads((HERE / "config.json").read_text(encoding="utf-8"))


def summarize(args):
    with (DATA_DIR / "expenses.csv").open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    total = sum(float(r["amount"]) for r in rows)
    by_cat = {}
    for r in rows:
        by_cat[r["category"]] = by_cat.get(r["category"], 0) + float(r["amount"])
    lines = [f"{len(rows)} expenses, total {total:.2f} {CONFIG['currency']}"]
    lines += [f"{c}: {v:.2f}" for c, v in sorted(by_cat.items())]
    return "\n".join(lines)


TOOLS = {"summarize_expenses": {
    "description": "Summarize expenses.csv by category.",
    "inputSchema": {"type": "object", "properties": {}},
    "handler": summarize}}


def handle(msg):
    method, mid, params = msg.get("method"), msg.get("id"), msg.get("params") or {}
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": mid, "result": {
            "protocolVersion": params.get("protocolVersion", "2025-06-18"),
            "capabilities": {"tools": {}}, "serverInfo": {"name": "expenses", "version": "1.2.1"}}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": [
            {"name": n, "description": t["description"], "inputSchema": t["inputSchema"]} for n, t in TOOLS.items()]}}
    if method == "tools/call":
        t = TOOLS.get(params.get("name"))
        if not t:
            return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32602, "message": "Unknown tool"}}
        return {"jsonrpc": "2.0", "id": mid, "result": {
            "content": [{"type": "text", "text": t["handler"](params.get("arguments") or {})}], "isError": False}}
    if method == "ping":
        return {"jsonrpc": "2.0", "id": mid, "result": {}}
    return None if mid is None else {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": "Method not found"}}


if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            resp = handle(json.loads(line))
            if resp is not None:
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
