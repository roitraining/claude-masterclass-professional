"""Shared plumbing for every lab and demo: build options, run a task, record what happened.

The SDK reads ANTHROPIC_API_KEY from the environment of the process. Never put a key in a file.
"""
from __future__ import annotations

import os
from dataclasses import asdict, dataclass, field
from typing import Any

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

# The Agent SDK defers tool schemas behind a search step by default. Graders ignore that step.
IGNORED_TOOLS = {"ToolSearch"}
# The subagent tool is named "Agent" in tool_use blocks and "Task" in older versions and in the init tool list.
SUBAGENT_TOOLS = {"Agent", "Task"}
# Used when you want Agent available but no file, shell or web tools. A bare name in disallowed_tools removes the tool.
# SendMessage is listed because it is a built-in that can resume a stopped
# subagent. Lab 3 passes this list as disallowed_tools, so leaving it out let a
# contained agent restart its own subagents and break the turn bound.
BUILTIN_TOOLS = ["Bash", "Read", "Write", "Edit", "Glob", "Grep", "WebFetch",
                 "WebSearch", "NotebookEdit", "SendMessage"]

_UNSET = object()


def require_api_key() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit(
            "ANTHROPIC_API_KEY is not set. Set it as an environment variable in this shell "
            "(see README.md). Do not put the key in a file."
        )


def short_name(name: str) -> str:
    """mcp__shop__order_lookup -> order_lookup. Built-in names are returned unchanged."""
    return name.split("__")[-1] if name.startswith("mcp__") else name


@dataclass
class ToolCall:
    name: str
    input: dict[str, Any]
    tool_use_id: str
    in_subagent: bool = False
    result_text: str = ""
    is_error: bool = False

    @property
    def short(self) -> str:
        return short_name(self.name)


@dataclass
class RunRecord:
    prompt: str
    final_text: str = ""
    subtype: str = "not_run"
    num_turns: int = 0
    cost_usd: float | None = None
    tool_calls: list[ToolCall] = field(default_factory=list)
    assistant_text: list[str] = field(default_factory=list)
    mcp_status: list[dict[str, Any]] = field(default_factory=list)
    error: str | None = None

    def used_tools(self) -> list[str]:
        """Short names of every tool called, in order, excluding the tool-search step and subagent spawns."""
        return [c.short for c in self.tool_calls if c.name not in IGNORED_TOOLS and c.name not in SUBAGENT_TOOLS]

    def spawns(self) -> list[ToolCall]:
        return [c for c in self.tool_calls if c.name in SUBAGENT_TOOLS]

    def all_text(self) -> str:
        return "\n".join([self.final_text, *self.assistant_text])

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def make_options(
    system_prompt: str,
    mcp_servers: dict[str, Any] | None = None,
    allowed_tools: list[str] | None = None,
    disallowed_tools: list[str] | None = None,
    tools: Any = _UNSET,
    agents: dict[str, Any] | None = None,
    env: dict[str, str] | None = None,
    max_turns: int | None = None,
    max_budget_usd: float | None = None,
) -> ClaudeAgentOptions:
    """Options every lab shares. Defaults: no built-in tools, no filesystem settings, and hard limits.

    Limits come from LAB_MAX_TURNS and LAB_BUDGET_USD when set, else 12 turns and 0.50 USD.
    The instructor may change them to fit the class key's spend limit.
    Set AGENT_MODEL to choose a model. Leave it unset to use the default.
    """
    return ClaudeAgentOptions(
        system_prompt=system_prompt,
        tools=[] if tools is _UNSET else tools,
        setting_sources=[],
        mcp_servers=mcp_servers or {},
        allowed_tools=allowed_tools or [],
        disallowed_tools=disallowed_tools or [],
        agents=agents,
        env=env or {},
        max_turns=max_turns if max_turns is not None else int(os.environ.get("LAB_MAX_TURNS", "12")),
        max_budget_usd=max_budget_usd if max_budget_usd is not None else float(os.environ.get("LAB_BUDGET_USD", "0.50")),
        model=os.environ.get("AGENT_MODEL") or None,
    )


def _flatten(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    return "\n".join(p.get("text", "") for p in content if isinstance(p, dict))


async def run_task(prompt: str, options: ClaudeAgentOptions) -> RunRecord:
    """Run one prompt to completion and return everything a grader needs."""
    rec = RunRecord(prompt=prompt)
    by_id: dict[str, ToolCall] = {}
    try:
        async for m in query(prompt=prompt, options=options):
            if isinstance(m, SystemMessage) and m.subtype == "init":
                rec.mcp_status = list(m.data.get("mcp_servers", []) or [])
            elif isinstance(m, AssistantMessage):
                in_sub = bool(m.parent_tool_use_id)
                for b in m.content:
                    if isinstance(b, TextBlock) and not in_sub:
                        rec.assistant_text.append(b.text)
                    elif isinstance(b, ToolUseBlock):
                        call = ToolCall(b.name, dict(b.input or {}), b.id, in_sub)
                        by_id[b.id] = call
                        rec.tool_calls.append(call)
            elif isinstance(m, UserMessage) and isinstance(m.content, list):
                for b in m.content:
                    if isinstance(b, ToolResultBlock) and b.tool_use_id in by_id:
                        by_id[b.tool_use_id].result_text = _flatten(b.content)
                        by_id[b.tool_use_id].is_error = bool(b.is_error)
            elif isinstance(m, ResultMessage):
                rec.subtype = m.subtype
                rec.final_text = m.result or ""
                rec.num_turns = m.num_turns
                rec.cost_usd = m.total_cost_usd
    except Exception as exc:  # A single-shot query() raises after yielding an error result.
        rec.error = f"{type(exc).__name__}: {exc}"
    return rec


def print_record(rec: RunRecord) -> None:
    """Readable summary of one run."""
    print(f"\nPROMPT: {rec.prompt}")
    for c in rec.tool_calls:
        where = " (inside subagent)" if c.in_subagent else ""
        print(f"  TOOL {c.name}{where} input={c.input}")
        if c.result_text:
            snippet = c.result_text.replace("\n", " ")[:160]
            print(f"       result{' [error]' if c.is_error else ''}: {snippet}")
    print(f"ANSWER: {rec.final_text.strip()}")
    cost = f"{rec.cost_usd:.4f}" if rec.cost_usd is not None else "n/a"
    print(f"RESULT: subtype={rec.subtype} turns={rec.num_turns} cost_usd={cost}")
    if rec.error:
        print(f"ERROR: {rec.error}")
