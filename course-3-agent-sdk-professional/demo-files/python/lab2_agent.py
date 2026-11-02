"""Lab 2: the Lab 1 agent plus the standalone MCP server.

    python lab2_agent.py "What do the notes on order BW-1002 say?"
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

import tools_inprocess
from agent_core import make_options, print_record, require_api_key, run_task

HERE = Path(__file__).resolve().parent

# Keep your Lab 1 prompt and tool fixes. The tools in tools_inprocess.py are unchanged except for your edits there.
SYSTEM_PROMPT = (
    "You are the support assistant for Brightwater Outfitters, a fictional outdoor retailer. "
    "Today's date is 2026-10-19. Use the tools to look up facts about orders, customers, policies and order notes. "
    "Be concise."
)

SHOPDESK_SERVER = {
    # sys.executable is the Python running this script, so the server uses the same virtual environment.
    "command": sys.executable,
    "args": [str(HERE / "mcp_server.py")],
}


def build_options(system_prompt: str = SYSTEM_PROMPT):
    return make_options(
        system_prompt,
        mcp_servers={"shop": tools_inprocess.SERVER, "shopdesk": SHOPDESK_SERVER},
        # Auto-approve the in-process tools and the notes server's tools.
        allowed_tools=[*tools_inprocess.ALLOWED, "mcp__shopdesk__*"],
    )


if __name__ == "__main__":
    require_api_key()
    prompt = " ".join(sys.argv[1:]) or "What do the notes on order BW-1002 say?"
    rec = asyncio.run(run_task(prompt, build_options()))
    print("MCP servers at init:", rec.mcp_status)
    print_record(rec)
