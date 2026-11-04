"""Demo 5: delegate to a subagent defined in code. Follows the documented AgentDefinition pattern.

    python3 demo5_subagent.py
"""
import asyncio
from pathlib import Path

from claude_agent_sdk import AgentDefinition

from agent_core import make_options, print_record, require_api_key, run_task

DOCS = Path(__file__).resolve().parent.parent / "retrieval" / "docs"


async def main() -> None:
    require_api_key()
    options = make_options(
        "You are a policy analyst for Brightwater Outfitters, a fictional retailer. Be concise.",
        allowed_tools=["Read", "Grep", "Glob", "Agent"],
        disallowed_tools=["Bash", "Write", "Edit", "WebFetch", "WebSearch", "NotebookEdit"],
        tools=None,  # default built-ins, minus the ones removed above; Agent stays available
        agents={
            "policy-reader": AgentDefinition(
                description="Reads policy documents in the working folder and reports what they say. Use for comparing or summarizing documents.",
                prompt="You read the Markdown documents you are pointed to and report their key rules accurately and briefly. Do not edit anything.",
                tools=["Read", "Grep", "Glob"],
            )
        },
        max_turns=10,
        max_budget_usd=0.40,
    )
    options.cwd = str(DOCS)
    prompt = (
        "Use the policy-reader agent to compare bw-returns-handbook.md with bw-returns-handbook-2024.md "
        "and report what changed in the return window and the refund method."
    )
    rec = await run_task(prompt, options)
    print_record(rec)
    spawns = rec.spawns()
    print(f"Agent tool_use blocks: {len(spawns)}")
    for s in spawns:
        print(f"  subagent_type={s.input.get('subagent_type')}  prompt (what the subagent received): {str(s.input.get('prompt'))[:200]}")
    print(f"tool calls made inside the subagent: {sum(c.in_subagent for c in rec.tool_calls)}")


if __name__ == "__main__":
    asyncio.run(main())
