"""Lab 1: the support agent. Run one prompt:

    python3 lab1_agent.py "Where is order BW-1003?"
"""
from __future__ import annotations

import asyncio
import sys

import tools_inprocess
from agent_core import make_options, print_record, require_api_key, run_task

SYSTEM_PROMPT = (
    "You are the support assistant for Brightwater Outfitters, a fictional outdoor retailer. "
    "Today's date is 2026-10-19. Use the tools to look up facts about orders, customers and policies. "
    "Be concise."
)


def build_options(system_prompt: str = SYSTEM_PROMPT):
    return make_options(
        system_prompt,
        mcp_servers={"shop": tools_inprocess.SERVER},
        allowed_tools=tools_inprocess.ALLOWED,
    )


if __name__ == "__main__":
    require_api_key()
    prompt = " ".join(sys.argv[1:]) or "Where is order BW-1003?"
    print_record(asyncio.run(run_task(prompt, build_options())))
