"""Demo 1: the minimal agent. Prints every message so the loop is visible.

    python demo1_minimal.py
"""
import asyncio
from pathlib import Path

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    SystemMessage,
    TextBlock,
    ToolResultBlock,
    ToolUseBlock,
    UserMessage,
    query,
)

from agent_core import require_api_key

DATA = Path(__file__).resolve().parent.parent / "data"


async def main() -> None:
    require_api_key()
    options = ClaudeAgentOptions(
        system_prompt="You are a concise assistant.",
        tools=["Read"],            # the only built-in tool that exists for this agent
        allowed_tools=["Read"],    # auto-approve it
        setting_sources=[],        # ignore settings files on this machine
        cwd=str(DATA),
        max_turns=4,
        max_budget_usd=0.25,
    )
    prompt = "Read sample_notes.md and list its three action items, one per line."
    async for m in query(prompt=prompt, options=options):
        if isinstance(m, SystemMessage):
            print(f"[system] subtype={m.subtype}")
        elif isinstance(m, AssistantMessage):
            for b in m.content:
                if isinstance(b, TextBlock):
                    print(f"[assistant text] {b.text.strip()}")
                elif isinstance(b, ToolUseBlock):
                    print(f"[assistant tool_use] {b.name} {b.input}")
        elif isinstance(m, UserMessage) and isinstance(m.content, list):
            for b in m.content:
                if isinstance(b, ToolResultBlock):
                    print(f"[tool_result] for {b.tool_use_id[:8]}...")
        elif isinstance(m, ResultMessage):
            print(f"[result] subtype={m.subtype} turns={m.num_turns} cost_usd={m.total_cost_usd}")
            print(m.result)


if __name__ == "__main__":
    asyncio.run(main())
