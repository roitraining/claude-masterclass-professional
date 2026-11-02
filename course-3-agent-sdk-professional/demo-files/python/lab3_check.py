"""Score Lab 3: the digest task and the runaway loop, against the limits you set in lab3_agent.py.

    python lab3_check.py

Two model runs. Each carries the turn and spend limits from lab3_agent.py.
"""
from __future__ import annotations

import asyncio
import json
from pathlib import Path

import lab3_agent
import loop_fixture
from agent_core import print_record, require_api_key, run_task

HERE = Path(__file__).resolve().parent
TASKS = json.loads((HERE.parent / "tasks" / "lab3_tasks.json").read_text(encoding="utf-8"))
HEADROOM = 1.5  # the spend cap is a client-side estimate and can overshoot, so allow headroom


async def main() -> None:
    require_api_key()
    results: list[tuple[str, bool, str]] = []

    # Digest: plan, delegate, incorporate, inside the limits.
    d = TASKS["digest"]
    rec = await run_task(d["prompt"], lab3_agent.build_options("digest"))
    print_record(rec)
    delegated = bool(rec.spawns())
    answer_ok = all(s in rec.final_text for s in d["must_contain_all"])
    finished = rec.subtype == "success"
    within_cost = (rec.cost_usd or 0) <= lab3_agent.BUDGET_USD * HEADROOM
    results.append(("digest: finished with success", finished, rec.subtype))
    results.append(("digest: delegated to the subagent (Agent tool_use)", delegated, f"{len(rec.spawns())} spawn(s)"))
    results.append(("digest: total refund 403 in the final answer", answer_ok, "looked for '403'"))
    results.append(("digest: cost within budget plus headroom", within_cost, f"{rec.cost_usd}"))

    # Loop: the runaway must be stopped, and the stop must be honest.
    lp = TASKS["loop"]
    loop_fixture.CALLS["n"] = 0
    rec2 = await run_task(lp["prompt"], lab3_agent.build_options("loop"))
    print_record(rec2)
    stopped_by_cap = rec2.subtype in lp["pass_if_subtype_in"]
    honest = rec2.subtype == "success" and any(s in rec2.final_text.lower() for s in lp["or_pass_if_success_and_final_text_contains_any"])
    calls = loop_fixture.CALLS["n"]
    # Calls made inside a subagent run in the same process only for in-process tools, so the counter is a floor, not a promise.
    results.append(("loop: stopped by a cap or reported honestly", stopped_by_cap or honest, rec2.subtype))
    results.append(("loop: check_manifest calls within bound", calls <= lp["max_check_manifest_calls"], f"{calls} call(s)"))
    results.append(("loop: cost within budget plus headroom", (rec2.cost_usd or 0) <= lab3_agent.BUDGET_USD * HEADROOM, f"{rec2.cost_usd}"))

    print("\n=== Lab 3 checks ===")
    for label, passed, detail in results:
        print(f"[{'PASS' if passed else 'FAIL'}] {label}  ({detail})")
    print(f"{sum(p for _, p, _ in results)}/{len(results)} checks passed")


if __name__ == "__main__":
    asyncio.run(main())
