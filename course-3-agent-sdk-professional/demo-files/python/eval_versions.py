"""The two agent versions Lab 4 compares. Both use the same tools. They differ in the system prompt.

Version A: prompts/system_a.txt (terse). Version B: prompts/system_b.txt (tuned).
Edit B, or add a version C, to test your own change. Change one thing at a time so the delta means something.
"""
from __future__ import annotations

from pathlib import Path

import lab2_agent  # swap for your own agent module if you built a different one in Lab 3

PROMPTS = Path(__file__).resolve().parent.parent / "prompts"
VERSIONS = {"A": "system_a.txt", "B": "system_b.txt"}


def options_for(version: str):
    system_prompt = (PROMPTS / VERSIONS[version]).read_text(encoding="utf-8")
    return lab2_agent.build_options(system_prompt)
