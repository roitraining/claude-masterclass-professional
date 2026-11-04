"""Demo 7: grade recorded runs with code, then with a judge. Offline by default: no model call.

    python3 demo7_grade.py                  # code graders and the recorded judge verdict
    python3 demo7_grade.py --live-judge     # also asks a live judge (one model call)

Graders here are deliberately tiny. Lab 4 builds the full set.
"""
import argparse
import asyncio
import json
from pathlib import Path

RUNS = Path(__file__).resolve().parent.parent / "recorded" / "demo7_runs.json"


def grade_answer(spec: dict, text: str) -> tuple[bool, str]:
    low = text.lower()
    for group in spec["answer_all_of"]:
        if not any(a in low for a in group):
            return False, f"missing one of {group}"
    return True, ""


def grade_tools(spec: dict, calls: list[str]) -> tuple[bool, str]:
    for t in spec["tools_require"]:
        if t not in calls:
            return False, f"required tool not called: {t}"
    for t in spec["tools_forbid"]:
        if t in calls:
            return False, f"forbidden tool called: {t}"
    return True, ""


async def main(live_judge: bool) -> None:
    data = json.loads(RUNS.read_text(encoding="utf-8"))
    for i, run in enumerate(data["runs"], 1):
        spec = data["golden"][run["task_id"]]
        a_ok, a_why = grade_answer(spec, run["final_text"])
        t_ok, t_why = grade_tools(spec, run["tool_calls"])
        print(f"run {i} {run['task_id']}  answer:{'PASS' if a_ok else 'FAIL'} {a_why}  tools:{'PASS' if t_ok else 'FAIL'} {t_why}")
        if "judge_min" in spec:
            if live_judge:
                import eval_judge  # needs ANTHROPIC_API_KEY; one model call
                verdict = await eval_judge.judge_reply("empathetic_delay_reply", run["final_text"])
            else:
                verdict = run["recorded_judge"]
            ok = verdict["score"] is not None and verdict["score"] >= spec["judge_min"]
            print(f"       judge score {verdict['score']} (min {spec['judge_min']}): {'PASS' if ok else 'FAIL'}  {verdict['reason']}")
    print("\nRead the pattern: run 2 answers correctly without checking the order (tool grader fails); run 3 is wrong (answer grader fails);")
    print("run 4 passes every code grader and still fails the judge, which is the only grader that can see tone.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--live-judge", action="store_true")
    asyncio.run(main(ap.parse_args().live_judge))
