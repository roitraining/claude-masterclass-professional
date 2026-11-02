"""FACILITATOR SOLUTION for Lab 4: copy over python/eval_graders.py."""
from __future__ import annotations

from dataclasses import dataclass

from agent_core import RunRecord


@dataclass
class Grade:
    passed: bool
    detail: str = ""


def grade_answer(task: dict, rec: RunRecord) -> Grade:
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
    spec = task.get("tools", {})
    used = rec.used_tools()
    for name in spec.get("require", []):
        if name not in used:
            return Grade(False, f"required tool not called: {name}")
    for name in spec.get("forbid", []):
        if name in used:
            return Grade(False, f"forbidden tool called: {name}")
    cap = spec.get("max_calls")
    if cap is not None and len(used) > cap:
        return Grade(False, f"{len(used)} tool calls, cap is {cap}")
    return Grade(True)


def grade_limits(task: dict, rec: RunRecord) -> Grade:
    if rec.subtype != "success":
        return Grade(False, f"run ended with {rec.subtype}")
    cap = task.get("max_turns_used")
    if cap is not None and rec.num_turns > cap:
        return Grade(False, f"{rec.num_turns} turns, cap is {cap}")
    return Grade(True)
