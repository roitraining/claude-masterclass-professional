#!/usr/bin/env python3
"""Run a print-mode Claude review over every pr-* branch of the Lab 2 fixture and
merge the results into one findings.json for score_review.py.

Usage:
    python3 run_reviews.py REPO [--out findings.json] [--max-turns 8] [--max-budget-usd 1.00]
                          [--model NAME] [--only pr-03] [--dry-run] [--claude-cmd claude]

REPO is the folder you built with build_fixture.py. Run it from any folder. The script
starts `claude -p` once per branch, with the repository as the working directory, so
Claude reads CLAUDE.md and can read the files around the change. The diff of the branch
against main goes in on standard input.

Each run uses model credits. --dry-run prints the commands and calls nothing.
Review REVIEW.md on the main branch of REPO before each round. REVIEW.md is read
because the prompt tells Claude to read it. It is not applied automatically in a local
run, so keep the instruction in the prompt below.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

PROMPT = """You are reviewing one pull request for a small Python service. The pull request diff is on standard input.
First read REVIEW.md and CLAUDE.md in the repository root and follow them. You may read other files in the repository
to understand the change. Do not edit anything.

Reply with ONLY a JSON object, no prose and no code fence, in exactly this shape:
{"findings": [{"pr": "%(branch)s", "file": "path/in/repo", "line": 12, "severity": "important", "title": "short title", "detail": "one or two sentences"}]}
Use severity "important" or "nit". "line" is the line number in the file on the pull request branch.
If you find nothing worth reporting, reply with {"findings": []}."""


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", **kw)


def branches(repo, only):
    out = run(["git", "branch", "--format=%(refname:short)"], cwd=repo).stdout.split()
    names = sorted(b for b in out if b.startswith("pr-"))
    return [b for b in names if not only or b.startswith(only)]


def extract_json(text):
    """Find the findings object in the reply, with or without the --output-format json envelope."""
    try:
        outer = json.loads(text)
        if isinstance(outer, dict):
            if "findings" in outer:
                return outer
            for k in ("structured_output", "result"):
                v = outer.get(k)
                if isinstance(v, dict) and "findings" in v:
                    return v
                if isinstance(v, str):
                    text = v
    except json.JSONDecodeError:
        pass
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        return None
    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        return None


def main(argv):
    opts = {"--out": "findings.json", "--max-turns": "8", "--max-budget-usd": "1.00",
            "--model": None, "--only": None, "--claude-cmd": "claude"}
    args, i = [], 0
    dry = "--dry-run" in argv
    while i < len(argv):
        a = argv[i]
        if a in opts:
            opts[a] = argv[i + 1]
            i += 2
        elif a == "--dry-run":
            i += 1
        else:
            args.append(a)
            i += 1
    if len(args) != 1:
        print(__doc__)
        return 2
    repo = Path(args[0]).resolve()
    if not (repo / ".git").exists():
        print(f"{repo} is not a git repository. Build it with build_fixture.py first.")
        return 2
    exe = shutil.which(opts["--claude-cmd"]) or opts["--claude-cmd"]
    merged, failures = [], []
    for b in branches(repo, opts["--only"]):
        diff = run(["git", "diff", "-U25", f"main...{b}"], cwd=repo).stdout
        cmd = [exe, "-p", PROMPT % {"branch": b},
               "--allowedTools", "Read,Grep,Glob",
               "--max-turns", opts["--max-turns"],
               "--max-budget-usd", opts["--max-budget-usd"],
               "--no-session-persistence"]
        if opts["--model"]:
            cmd += ["--model", opts["--model"]]
        if dry:
            print(f"[dry run] {b}: cwd={repo}\n    " + " ".join(cmd[:2] + ['<prompt>'] + cmd[3:]) + f"\n    stdin: git diff -U25 main...{b} ({len(diff.splitlines())} lines)")
            continue
        print(f"Reviewing {b} ...", flush=True)
        res = run(cmd, input=diff, cwd=repo)
        data = extract_json(res.stdout)
        if res.returncode != 0 or data is None:
            failures.append(b)
            print(f"   no usable JSON (exit {res.returncode}). First 200 characters of output: {res.stdout[:200]!r}")
            if res.stderr.strip():
                print(f"   stderr: {res.stderr.strip()[:200]}")
            continue
        for f in data.get("findings", []):
            f.setdefault("pr", b)
            merged.append(f)
        print(f"   {len(data.get('findings', []))} finding(s)")
    if dry:
        return 0
    Path(opts["--out"]).write_text(json.dumps({"findings": merged}, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(merged)} finding(s) to {opts['--out']}")
    if failures:
        print("Re-run these with --only: " + ", ".join(failures))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
