"""Lab 4 harness: run golden tasks against one agent version, grade, and write results.

    python eval_harness.py --version A --out results/A.json
    python eval_harness.py --version B --out results/B.json --repeats 2 --cost-target 0.05
    python eval_harness.py --version A --only G01,G09        # a quick smoke test

Every run is a model call. Each agent run keeps the turn and spend limits from agent_core.make_options.
"""
from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

import eval_graders
import eval_judge
import eval_scoring
import eval_versions
from agent_core import require_api_key, run_task

HERE = Path(__file__).resolve().parent
GOLDEN = HERE.parent / "tasks" / "golden_tasks.json"
REFUND_LOG = HERE / "refund_log.jsonl"


async def grade_task(task: dict, rec) -> dict:
    answer = eval_graders.grade_answer(task, rec)
    tools = eval_graders.grade_tools(task, rec)
    limits = eval_graders.grade_limits(task, rec)
    judge_score = None
    judge_ok = True
    judge_reason = ""
    if task.get("judge") and answer.passed:
        verdict = await eval_judge.judge_reply(task["judge"]["rubric"], rec.final_text)
        judge_score = verdict["score"]
        judge_reason = verdict["reason"]
        judge_ok = judge_score is not None and judge_score >= task["judge"]["min_score"]
    forbidden = set(task.get("tools", {}).get("forbid", []))
    return {
        "task_id": task["id"],
        "category": task.get("category"),
        "answer_ok": answer.passed,
        "tools_ok": tools.passed,
        "limits_ok": limits.passed,
        "judge_score": judge_score,
        "passed": answer.passed and tools.passed and limits.passed and judge_ok,
        "why": "; ".join(g.detail for g in (answer, tools, limits) if not g.passed) or judge_reason,
        "cost_usd": rec.cost_usd,
        "num_turns": rec.num_turns,
        "tools_used": rec.used_tools(),
        "subtype": rec.subtype,
        "forbidden_hit": bool(forbidden & set(rec.used_tools())),
    }


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", required=True, choices=sorted(eval_versions.VERSIONS))
    ap.add_argument("--out", required=True)
    ap.add_argument("--repeats", type=int, default=1)
    ap.add_argument("--cost-target", type=float, default=None)
    ap.add_argument("--only", default="", help="comma-separated task ids")
    args = ap.parse_args()
    require_api_key()

    tasks = json.loads(GOLDEN.read_text(encoding="utf-8"))["tasks"]
    if args.only:
        wanted = set(args.only.split(","))
        tasks = [t for t in tasks if t["id"] in wanted]

    runs: list[dict] = []
    for repeat in range(1, args.repeats + 1):
        for task in tasks:
            rec = await run_task(task["prompt"], eval_versions.options_for(args.version))
            row = await grade_task(task, rec)
            row["repeat"] = repeat
            runs.append(row)
            print(f"{task['id']} r{repeat}  {'PASS' if row['passed'] else 'FAIL'}  {row['why']}")

    summary = eval_scoring.summarize(runs, args.repeats)
    summary["tier"] = eval_scoring.tier(summary, args.cost_target)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"version": args.version, "summary": summary, "runs": runs}, indent=2), encoding="utf-8")
    print(f"\nversion {args.version}: pass_rate={summary['pass_rate']:.2f} tier={summary['tier']} -> {out}")


if __name__ == "__main__":
    asyncio.run(main())
