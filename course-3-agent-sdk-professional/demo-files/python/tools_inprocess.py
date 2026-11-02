"""Lab 1 starter: three custom tools wrapped in an in-process MCP server.

The tools work. The agent still uses them badly. Find out why, then fix it.
You may change anything in this file except the data behind it (shop_data.py).
"""
from __future__ import annotations

import json
from typing import Any

from claude_agent_sdk import create_sdk_mcp_server, tool

import shop_data


def _text(payload: Any, is_error: bool = False) -> dict[str, Any]:
    body = payload if isinstance(payload, str) else json.dumps(payload)
    out: dict[str, Any] = {"content": [{"type": "text", "text": body}]}
    if is_error:
        out["is_error"] = True
    return out


@tool("order_lookup", "Look up information.", {"id": str})
async def order_lookup(args: dict[str, Any]) -> dict[str, Any]:
    rec = shop_data.get_order(args["id"])
    if rec is None:
        return _text(f"No order found for id {args['id']!r}. Order ids look like BW-1001.", is_error=True)
    return _text(rec)


@tool("customer_lookup", "Look up information about a person or an order.", {"id": str})
async def customer_lookup(args: dict[str, Any]) -> dict[str, Any]:
    rec = shop_data.get_customer(args["id"])
    if rec is None:
        return _text(f"No customer found for id {args['id']!r}.", is_error=True)
    return _text(rec)


@tool("policy_lookup", "Get details about anything the customer asks.", {"topic": str})
async def policy_lookup(args: dict[str, Any]) -> dict[str, Any]:
    text = shop_data.get_policy(args["topic"])
    if text is None:
        return _text(f"Unknown topic {args['topic']!r}.", is_error=True)
    return _text(text)


SERVER = create_sdk_mcp_server(
    name="shop",
    version="1.0.0",
    tools=[order_lookup, customer_lookup, policy_lookup],
)

# Tools are allowed by full name: mcp__{server}__{tool}.
ALLOWED = [
    "mcp__shop__order_lookup",
    "mcp__shop__customer_lookup",
    "mcp__shop__policy_lookup",
]
