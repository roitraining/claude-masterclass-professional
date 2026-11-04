"""Preflight: confirms the environment is ready. Makes no model call and never prints the key.

Run from this folder:  python3 preflight.py
"""
import importlib
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ok = True


def check(label: str, passed: bool, fix: str = "") -> None:
    global ok
    ok = ok and passed
    print(f"[{'ok' if passed else 'FAIL'}] {label}" + ("" if passed else f"  -> {fix}"))


check("Python 3.10 or later", sys.version_info >= (3, 10), "install a newer Python")
check("ANTHROPIC_API_KEY is set (value not shown)", bool(os.environ.get("ANTHROPIC_API_KEY")),
      "set it as an environment variable in this shell; never put it in a file")
for mod, fix in (("claude_agent_sdk", "pip install claude-agent-sdk"), ("mcp", 'pip install "mcp[cli]"')):
    try:
        importlib.import_module(mod)
        check(f"import {mod}", True)
    except Exception as exc:  # noqa: BLE001
        check(f"import {mod}", False, f"{fix} ({type(exc).__name__})")
for rel in ("../data/shop.json", "../data/order_notes.json", "../tasks/golden_tasks.json"):
    check(f"found {rel}", (HERE / rel).exists(), "the demo-files folder is incomplete")
print("\nReady." if ok else "\nFix the items marked FAIL, then run this again.")
sys.exit(0 if ok else 1)
