"""Demo 6: cap turns, subagent depth, concurrency and spend, and read the result when a cap is hit.

    python3 demo6_caps.py turns          # max_turns=4
    python3 demo6_caps.py budget         # max_budget_usd=0.03
    python3 demo6_caps.py concurrency    # depth 1 and concurrency 2, asks for four parallel subagents

The tool never finishes, so every run needs a cap. The caps below are demo values.
"""
import asyncio
import sys
from typing import Any

from claude_agent_sdk import AgentDefinition, create_sdk_mcp_server, tool

from agent_core import BUILTIN_TOOLS, make_options, print_record, require_api_key, run_task

CALLS = {"n": 0}


@tool("poll_job", "Check whether a batch job has finished. Input: a job id such as J-1. Returns RUNNING or DONE.", {"job_id": str})
async def poll_job(args: dict[str, Any]) -> dict[str, Any]:
    CALLS["n"] += 1
    return {"content": [{"type": "text", "text": f"RUNNING: job {args['job_id']} has not finished (poll {CALLS['n']})."}]}


SERVER = create_sdk_mcp_server(name="jobs", version="1.0.0", tools=[poll_job])
SYSTEM = "You monitor batch jobs. A job is done only when poll_job returns DONE. Keep polling until it does."
POLLER = AgentDefinition(
    description="Polls one batch job until it is DONE.",
    prompt="Poll the job you are given with poll_job until it returns DONE.",
    tools=["mcp__jobs__poll_job"],
)


async def main(mode: str) -> None:
    require_api_key()
    kwargs: dict[str, Any] = {}
    prompt = "Wait for job J-1 to finish, polling until it completes."
    if mode == "turns":
        kwargs["max_turns"] = 4
    elif mode == "budget":
        kwargs["max_budget_usd"] = 0.03
    elif mode == "concurrency":
        kwargs["env"] = {"CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH": "1", "CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS": "2"}
        kwargs["max_turns"] = 10
        kwargs["max_budget_usd"] = 0.30
        prompt = "Start four poller subagents in parallel, one each for jobs J-1, J-2, J-3 and J-4, and report when they finish."
    options = make_options(
        SYSTEM,
        mcp_servers={"jobs": SERVER},
        allowed_tools=["mcp__jobs__poll_job", "Agent"],
        disallowed_tools=BUILTIN_TOOLS,
        tools=None,
        agents={"poller": POLLER},
        **kwargs,
    )
    rec = await run_task(prompt, options)
    print_record(rec)
    print(f"poll_job calls: {CALLS['n']}   subagent spawns: {len(rec.spawns())}")
    refused = [c for c in rec.tool_calls if "limit reached" in c.result_text.lower()]
    for c in refused:
        print(f"  limit message in a tool result: {c.result_text[:120]}")
    print("Read the subtype first. error_max_turns and error_max_budget_usd mean a cap stopped the run, not that the work finished.")


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("turns", "budget", "concurrency"):
        raise SystemExit("usage: python3 demo6_caps.py turns|budget|concurrency")
    asyncio.run(main(sys.argv[1]))
