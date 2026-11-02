"""Lab 4 code graders. grade_answer is done. You write grade_tools and grade_limits.

A grader takes a golden task (one entry from tasks/golden_tasks.json) and a RunRecord, and returns a Grade.
Graders read the tool_use blocks the harness already collected in rec.tool_calls. Do not re-run the agent.
"""
from __future__ import annotations

from dataclasses import dataclass

from agent_core import RunRecord


@dataclass
class Grade:
    passed: bool
    detail: str = ""


def grade_answer(task: dict, rec: RunRecord) -> Grade:
    """Final-answer grader: every all_of group needs one alternative present, and nothing in none_of may appear."""
    spec = task.get("answer", {})
    low_final = rec.final_text.lower()
    for group in spec.get("all_of", []):
        if not any(alt.lower() in low_final for alt in group):
            return Grade(False, f"missing one of {group}")
    low_all = rec.all_text().lower()
    for bad in spec.get("none_of", []):
        if bad.lower() in low_all:
            return Grade(False, f"forbidden text present: {bad!r}")
    return Grade(True)


def grade_tools(task: dict, rec: RunRecord) -> Grade:
    """TODO: grade the tool calls.

    Use rec.used_tools() (short names, in call order, tool-search and subagent spawns excluded) and task["tools"]:
      - every name in tools.require must have been called
      - no name in tools.forbid may have been called
      - the number of calls must not exceed tools.max_calls
    Return Grade(False, "<what went wrong>") on the first violation so the report says why.
    """
    raise NotImplementedError("Lab 4: write grade_tools")


def grade_limits(task: dict, rec: RunRecord) -> Grade:
    """TODO: grade the run itself.

    The run must have ended with rec.subtype == "success" and used no more turns than task["max_turns_used"].
    """
    raise NotImplementedError("Lab 4: write grade_limits")
