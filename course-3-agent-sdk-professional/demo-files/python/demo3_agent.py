"""Demo 3: connect an agent to the standalone server and show what the init message reports.

    python3 demo3_agent.py
"""
import asyncio
import sys
from pathlib import Path

from agent_core import make_options, print_record, require_api_key, run_task

HERE = Path(__file__).resolve().parent


async def main() -> None:
    require_api_key()
    options = make_options(
        "You are a shipping assistant. Use the tools for prices. Be concise.",
        mcp_servers={"rates": {"command": sys.executable, "args": [str(HERE / "demo3_rates_server.py")]}},
        allowed_tools=["mcp__rates__*"],  # all tools from this server; a wildcard is fine for a server you wrote and trust
        max_turns=6,
        max_budget_usd=0.25,
    )
    rec = await run_task("What does it cost to ship a 3.5 kilogram package to zone B?", options)
    print("MCP servers at init:", rec.mcp_status)
    print_record(rec)
    print("Expected price from the server: 13.80 dollars")


if __name__ == "__main__":
    asyncio.run(main())
