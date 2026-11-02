"""FACILITATOR SOLUTION for Lab 1: copy over python/tools_inprocess.py.

Fixes: each description says what the tool does, the input format, and when NOT to use it.
The parameter is renamed to say what it holds. The policy topic is an enum (enums need full JSON Schema in Python).
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


@tool(
    "order_lookup",
    "Fetch one order by its order id: status, items, total, carrier, tracking, delivery date or ETA, and the customer's email. "
    "Use when the customer asks about a specific order such as BW-1003. "
    "Do not use for policy questions, for listing a customer's orders (use customer_lookup), or for anything not tied to an order id.",
    {
        "type": "object",
        "properties": {"order_id": {"type": "string", "description": "Order id in the form BW-1234 (BW, a hyphen, four digits)."}},
        "required": ["order_id"],
    },
)
async def order_lookup(args: dict[str, Any]) -> dict[str, Any]:
    rec = shop_data.get_order(args["order_id"])
    if rec is None:
        return _text(f"No order found for id {args['order_id']!r}. Order ids look like BW-1001.", is_error=True)
    return _text(rec)


@tool(
    "customer_lookup",
    "Fetch one customer by email address: name, loyalty tier, and the ids of their orders. "
    "Use when you have a customer's email and need their tier or their list of orders. "
    "Do not use with an order id; call order_lookup first to get the email.",
    {
        "type": "object",
        "properties": {"email": {"type": "string", "description": "The customer's email address, for example maya.ortiz@example.test."}},
        "required": ["email"],
    },
)
async def customer_lookup(args: dict[str, Any]) -> dict[str, Any]:
    rec = shop_data.get_customer(args["email"])
    if rec is None:
        return _text(f"No customer found for email {args['email']!r}.", is_error=True)
    return _text(rec)


@tool(
    "policy_lookup",
    "Fetch the text of one store policy: returns, shipping, warranty or price_match. "
    "Use only when the answer depends on Brightwater's written policy, such as the return window or warranty length. "
    "Do not use for greetings, arithmetic, general knowledge, or questions about a specific order's status.",
    {
        "type": "object",
        "properties": {"topic": {"type": "string", "enum": shop_data.POLICY_TOPICS, "description": "Which policy to fetch."}},
        "required": ["topic"],
    },
)
async def policy_lookup(args: dict[str, Any]) -> dict[str, Any]:
    text = shop_data.get_policy(args["topic"])
    if text is None:
        return _text(f"Unknown topic {args['topic']!r}. Valid topics: {', '.join(shop_data.POLICY_TOPICS)}.", is_error=True)
    return _text(text)


SERVER = create_sdk_mcp_server(name="shop", version="1.0.0", tools=[order_lookup, customer_lookup, policy_lookup])

ALLOWED = ["mcp__shop__order_lookup", "mcp__shop__customer_lookup", "mcp__shop__policy_lookup"]
