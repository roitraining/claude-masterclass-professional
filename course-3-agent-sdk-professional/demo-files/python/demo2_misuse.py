"""Demo 2: a tool the agent misuses. Two converter tools, with vague or clear descriptions.

    python3 demo2_misuse.py vague
    python3 demo2_misuse.py clear

Everything is local and fictional. The class rate table is invented.
"""
import asyncio
import sys
from typing import Any

from claude_agent_sdk import create_sdk_mcp_server, tool

from agent_core import make_options, print_record, require_api_key, run_task

UNITS = {("kg", "lb"): 2.20462, ("lb", "kg"): 1 / 2.20462, ("km", "mi"): 0.621371, ("mi", "km"): 1 / 0.621371}
RATES = {("USD", "EUR"): 0.90, ("EUR", "USD"): 1 / 0.90, ("USD", "GBP"): 0.78, ("GBP", "USD"): 1 / 0.78}

VARIANTS = {
    "vague": {
        "convert": "Convert a value.",
        "convert_value": "Convert a value between formats.",
    },
    "clear": {
        "convert": "Convert a physical measurement between units: kg and lb, km and mi. Not for money.",
        "convert_value": "Convert an amount of money between currencies: USD, EUR, GBP, using the fixed class rate table. Not for physical units.",
    },
}


def _reply(text: str, error: bool = False) -> dict[str, Any]:
    out: dict[str, Any] = {"content": [{"type": "text", "text": text}]}
    if error:
        out["is_error"] = True
    return out


def build(variant: str):
    desc = VARIANTS[variant]

    @tool("convert", desc["convert"], {"amount": float, "from_unit": str, "to_unit": str})
    async def convert(args: dict[str, Any]) -> dict[str, Any]:
        key = (args["from_unit"].lower(), args["to_unit"].lower())
        if key not in UNITS:
            return _reply(f"Unsupported unit pair {key}.", error=True)
        return _reply(f"{args['amount'] * UNITS[key]:.2f} {key[1]}")

    @tool("convert_value", desc["convert_value"], {"amount": float, "from_unit": str, "to_unit": str})
    async def convert_value(args: dict[str, Any]) -> dict[str, Any]:
        key = (args["from_unit"].upper(), args["to_unit"].upper())
        if key not in RATES:
            return _reply(f"Unsupported currency pair {key}.", error=True)
        return _reply(f"{args['amount'] * RATES[key]:.2f} {key[1]}")

    return create_sdk_mcp_server(name="conv", version="1.0.0", tools=[convert, convert_value])


async def main(variant: str) -> None:
    require_api_key()
    options = make_options(
        "You are a conversion assistant. Use the tools for conversions. Be concise.",
        mcp_servers={"conv": build(variant)},
        allowed_tools=["mcp__conv__convert", "mcp__conv__convert_value"],
        max_turns=6,
        max_budget_usd=0.25,
    )
    print(f"=== variant: {variant} ===")
    for prompt in ("How many pounds is 12 kilograms?", "Convert 250 USD to EUR using the class rate table."):
        print_record(await run_task(prompt, options))


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in VARIANTS:
        raise SystemExit("usage: python3 demo2_misuse.py vague|clear")
    asyncio.run(main(sys.argv[1]))
