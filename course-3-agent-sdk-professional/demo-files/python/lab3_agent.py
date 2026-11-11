"""Lab 3: a plan-delegate-incorporate agent with one subagent, plus the runaway loop fixture.

    python3 lab3_agent.py digest
    python3 lab3_agent.py loop

Your tasks are marked TODO.
"""
from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from claude_agent_sdk import AgentDefinition

import loop_fixture
import tools_inprocess  # use your fixed Lab 1 tools here
from agent_core import BUILTIN_TOOLS, make_options, print_record, require_api_key, run_task

HERE = Path(__file__).resolve().parent
TASKS = json.loads((HERE.parent / "tasks" / "lab3_tasks.json").read_text(encoding="utf-8"))

# TODO 1: write the parent's plan-delegate-incorporate instructions.
#   Say: plan first, fetch the data with tools, delegate the eligibility and refund arithmetic to the subagent
#   (pass it everything it needs in the Agent tool's prompt, because it starts with a fresh context window),
#   then check and incorporate its result into the final digest.
DIGEST_SYSTEM_PROMPT = (
    "You are the returns-desk agent for Brightwater Outfitters, a fictional outdoor retailer. "
    "Today's date is 2026-10-19. Use the tools to answer."
)

# TODO 2: define the subagent. A weak description means the parent may never delegate.
# AgentDefinition fields keep camelCase spelling in Python (maxTurns, disallowedTools). A snake_case keyword raises TypeError.
RETURNS_ANALYST = AgentDefinition(
    description="Helper.",
    prompt="Help with the task you are given.",
    # tools=[...],
    # maxTurns=...,
)

# TODO 3: set the limits you will defend. These two numbers are deliberately wrong for the task.
MAX_TURNS = 3
BUDGET_USD = 5.00
# TODO 4: choose depth and concurrency limits for subagents. Both are passed as environment variables.
SUBAGENT_DEPTH = None  # example: "1"
SUBAGENT_CONCURRENCY = None  # example: "2"
# TODO 5: bound the loop subagent's own turns. max_turns above limits the PARENT's
# turns, not the tool calls a subagent makes inside one of them, so on its own it
# cannot stop the runaway. The subagent is defined in the fixture, which you must
# not edit, so set the limit here and it is applied for you.
LOOP_SUBAGENT_MAX_TURNS = None  # example: 4


def _env() -> dict[str, str]:
    env: dict[str, str] = {}
    if SUBAGENT_DEPTH is not None:
        env["CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH"] = str(SUBAGENT_DEPTH)
    if SUBAGENT_CONCURRENCY is not None:
        env["CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS"] = str(SUBAGENT_CONCURRENCY)
    return env  # the Python SDK merges this on top of the inherited environment


def build_options(mode: str = "digest"):
    # Agent must be available, so built-ins are not emptied. Remove the file, shell and web tools by name instead.
    if mode == "loop":
        return make_options(
            loop_fixture.LOOP_SYSTEM_PROMPT,
            mcp_servers={"dock": loop_fixture.SERVER},
            allowed_tools=[*loop_fixture.ALLOWED, "Agent"],
            disallowed_tools=BUILTIN_TOOLS,
            tools=None,
            agents={"manifest-watcher": loop_fixture.loop_subagent(LOOP_SUBAGENT_MAX_TURNS)},
            env=_env(),
            max_turns=MAX_TURNS,
            max_budget_usd=BUDGET_USD,
        )
    return make_options(
        DIGEST_SYSTEM_PROMPT,
        mcp_servers={"shop": tools_inprocess.SERVER},
        allowed_tools=[*tools_inprocess.ALLOWED, "Agent"],
        disallowed_tools=BUILTIN_TOOLS,
        tools=None,
        agents={"returns-analyst": RETURNS_ANALYST},
        env=_env(),
        max_turns=MAX_TURNS,
        max_budget_usd=BUDGET_USD,
    )


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["digest", "loop"])
    args = ap.parse_args()
    require_api_key()
    prompt = TASKS[args.mode]["prompt"]
    rec = asyncio.run(run_task(prompt, build_options(args.mode)))
    print_record(rec)
    print(f"subagent spawns: {len(rec.spawns())}")
    if args.mode == "loop":
        print(f"check_manifest calls: {loop_fixture.CALLS['n']}")
