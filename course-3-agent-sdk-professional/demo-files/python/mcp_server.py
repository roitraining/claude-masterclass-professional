"""Lab 2 server template: a standalone MCP server over stdio for Brightwater order notes.

The agent starts this file as a child process and talks to it over stdin and stdout.
Rules for a stdio server:
  - Never print to stdout. Stdout carries the protocol. Write logs to stderr.
  - Keep every tool description specific: what it does, its input format, and when not to use it.

Your tasks are marked TODO. The server library is the official MCP Python package (pip install "mcp[cli]").
The import below tries two module paths because the package layout has changed between releases.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:  # newer releases
    from mcp.server import MCPServer as FastMCP  # type: ignore

import shop_data

HERE = Path(__file__).resolve().parent
REFUND_LOG = HERE / "refund_log.jsonl"

mcp = FastMCP("shopdesk")


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


@mcp.tool()
def get_order_notes(order_id: str) -> str:
    """TODO: replace this line with a specific description.

    The function's docstring is used as the tool description in the common server libraries. Confirm for your installed version.
    """
    # TODO: use shop_data.get_notes(order_id).
    #   - Unknown order id: return a short, clear message (not a stack trace).
    #   - No notes: say so.
    #   - Otherwise return the notes as plain text, one per line.
    raise NotImplementedError("Lab 2: implement get_order_notes")


@mcp.tool()
def issue_refund(order_id: str, amount: float, reason: str) -> str:
    """Issue a refund for an order. Fake: appends a line to refund_log.jsonl in this folder and moves no money."""
    entry = {
        "at": datetime.now(timezone.utc).isoformat(),
        "order_id": order_id,
        "amount": amount,
        "reason": reason,
    }
    with REFUND_LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")
    log(f"refund recorded: {entry}")
    return f"Refund of {amount:.2f} recorded for {order_id}."


if __name__ == "__main__":
    # Newer library releases may name this call differently. If run() with a transport fails, check the library README.
    mcp.run(transport="stdio")
