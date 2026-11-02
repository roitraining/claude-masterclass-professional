"""Demo 8: what a passing score misses. Offline: reads recorded runs, no model call.

    python demo8_scorecard.py
"""
import json
from pathlib import Path

DATA = json.loads((Path(__file__).resolve().parent.parent / "recorded" / "demo8_runs.json").read_text(encoding="utf-8"))
suite = DATA["suite"]

answer_pass = sum(r["answer_ok"] for r in suite)
print(f"1. Final-answer grader: {answer_pass}/{len(suite)} pass  ({answer_pass / len(suite):.0%})")
print("   Looks ready to ship.\n")

forbid, cap = set(DATA["tool_rules"]["forbid"]), DATA["tool_rules"]["max_calls"]
print("2. Add a grader over the tool calls (forbidden tools, call cap):")
tool_fail = 0
for r in suite:
    reasons = []
    if forbid & set(r["tools"]):
        reasons.append(f"forbidden tool {sorted(forbid & set(r['tools']))}")
    if len(r["tools"]) > cap:
        reasons.append(f"{len(r['tools'])} calls, cap {cap}")
    if reasons:
        tool_fail += 1
        print(f"   {r['task_id']}: {'; '.join(reasons)}   (answer grader said {'pass' if r['answer_ok'] else 'fail'})")
print(f"   {len(suite) - tool_fail}/{len(suite)} pass both graders\n")

limit = DATA["cost_rule"]["max_cost_usd"]
costs = sorted(r["cost_usd"] for r in suite)
median = costs[len(costs) // 2]
print("3. Look at cost, not only correctness:")
print(f"   median cost per task {median:.3f}")
for r in suite:
    if r["cost_usd"] > limit:
        print(f"   {r['task_id']} cost {r['cost_usd']:.3f}, {r['cost_usd'] / median:.0f}x the median, over the {limit:.2f} rule")
print()

inj = DATA["injection_repeats"]
print("4. Rare failures need repeats and tasks aimed at them:")
print(f"   {inj['task']}")
print(f"   {inj['followed_injection']} of {inj['runs']} runs followed the injection. {inj['note']}")
print("\nA suite scores what it asks. It does not score what it never asks, or what happens once in twenty runs.")
