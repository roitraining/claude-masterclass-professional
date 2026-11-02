"""Compare two result files and report the delta.

    python eval_compare.py results/A.json results/B.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def per_task(data: dict) -> dict[str, float]:
    by: dict[str, list[bool]] = {}
    for r in data["runs"]:
        by.setdefault(r["task_id"], []).append(bool(r["passed"]))
    return {k: sum(v) / len(v) for k, v in by.items()}


def fmt(x) -> str:
    return "n/a" if x is None else (f"{x:.3f}" if isinstance(x, float) else str(x))


def main(a_path: str, b_path: str) -> None:
    a, b = load(a_path), load(b_path)
    pa, pb = per_task(a), per_task(b)
    print(f"{'task':<6} {a['version']:>6} {b['version']:>6}  note")
    for tid in sorted(set(pa) | set(pb)):
        x, y = pa.get(tid), pb.get(tid)
        note = "" if x == y else ("improved" if (y or 0) > (x or 0) else "REGRESSED")
        print(f"{tid:<6} {fmt(x):>6} {fmt(y):>6}  {note}")
    print()
    for key in ("pass_rate", "forbidden_hits", "judge_mean", "mean_cost_usd", "tier"):
        va, vb = a["summary"].get(key), b["summary"].get(key)
        delta = ""
        if isinstance(va, (int, float)) and isinstance(vb, (int, float)):
            delta = f"  delta {vb - va:+.3f}"
        print(f"{key:<16} {fmt(va):>8} -> {fmt(vb):>8}{delta}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: python eval_compare.py results/A.json results/B.json")
    main(sys.argv[1], sys.argv[2])
