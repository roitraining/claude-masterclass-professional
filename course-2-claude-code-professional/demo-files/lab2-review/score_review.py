#!/usr/bin/env python3
"""Score a set of review findings against the Lab 2 answer key.

Usage:
    python3 score_review.py findings.json [--key facilitator/answer_key.json] [--json]

Findings file shape (see findings.schema.json):
    {"findings": [
        {"pr": "pr-03-delete-member", "file": "lending/api.py", "line": 41,
         "severity": "important", "title": "Missing role check", "detail": "..."}
    ]}
A bare list of findings is accepted too. "pr" may be the full branch name or just
its number prefix ("pr-03"). "severity" is "important" or "nit". "line" may be null.

Rules:
  * A nit is never a catch and never a false positive. Nits are only counted.
  * An important finding CATCHES a planted bug when its pr and file match and its line is
    within the key's tolerance of the bug line. If "line" is missing it must mention a
    keyword from the key. Extra findings on the same bug are duplicates, not penalties.
  * Any other important finding is a FALSE POSITIVE: on a bait pull request, on the clean
    pull request, or on a bug pull request but not at the bug.

Tiers (a starting point, calibrate in rehearsal):
    Gold    all bugs caught, NO false positives, at most 6 nits
    Silver  at least 4 bugs caught, at most 3 false positives
    Bronze  at least 3 bugs caught, at most 5 false positives
Exit code 0 for Bronze or better, 1 otherwise, 2 for a usage error.
"""
import json
import re
import sys
from pathlib import Path

DEFAULT_KEY = Path(__file__).parent / "facilitator" / "answer_key.json"
TIERS = [("Gold", 99, 0, 6), ("Silver", 4, 3, 999), ("Bronze", 3, 5, 999)]


def norm_pr(value):
    m = re.search(r"pr-?(\d+)", str(value or "").lower())
    return f"pr-{int(m.group(1)):02d}" if m else str(value or "").lower()


def norm_file(value):
    return str(value or "").replace("\\", "/").lstrip("./").lower()


def load_findings(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    items = data.get("findings") if isinstance(data, dict) else data
    if not isinstance(items, list):
        sys.exit("findings must be a list, or an object with a 'findings' list")
    return items


def score(findings, key):
    tol = key.get("tolerance_lines", 3)
    bugs = {b["id"]: dict(b, caught_by=None) for b in key["bugs"]}
    bait_prs = {norm_pr(b["pr"]) for b in key["bait"]}
    clean_prs = {norm_pr(c["pr"]) for c in key["clean"]}
    known_prs = {norm_pr(b["pr"]) for b in key["bugs"]} | bait_prs | clean_prs
    false_pos, nits, dups, unknown = [], [], [], []

    for f in findings:
        sev = str(f.get("severity", "important")).lower()
        if sev in ("nit", "minor", "low"):
            nits.append(f)
            continue
        pr = norm_pr(f.get("pr"))
        if pr not in known_prs:
            unknown.append(f)
            continue
        hit = None
        for b in bugs.values():
            if norm_pr(b["pr"]) != pr or norm_file(b["file"]) != norm_file(f.get("file")):
                continue
            line = f.get("line")
            if isinstance(line, int):
                ok = abs(line - b["line"]) <= tol
            else:
                text = (str(f.get("title", "")) + " " + str(f.get("detail", ""))).lower()
                ok = any(k.lower() in text for k in b.get("keywords", []))
            if ok:
                hit = b
                break
        if hit is None:
            kind = "bait" if pr in bait_prs else "clean" if pr in clean_prs else "bug pull request, wrong place"
            false_pos.append((f, kind))
        elif hit["caught_by"] is None:
            hit["caught_by"] = f
        else:
            dups.append(f)

    caught = sum(1 for b in bugs.values() if b["caught_by"])
    total = len(bugs)
    fp = len(false_pos)
    tier = "Not yet"
    for name, need_caught, max_fp, max_nits in TIERS:
        need = total if name == "Gold" else need_caught
        if caught >= need and fp <= max_fp and len(nits) <= max_nits:
            tier = name
            break
    important = caught + fp + len(dups)
    precision = round(caught / (caught + fp), 2) if (caught + fp) else None
    return dict(caught=caught, total=total, false_positives=fp, nits=len(nits), duplicates=len(dups),
                unknown_pr=len(unknown), important=important, precision=precision, tier=tier,
                bugs=bugs, fp_detail=false_pos)


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    key_path = DEFAULT_KEY
    if "--key" in argv:
        key_path = Path(argv[argv.index("--key") + 1])
        args = [a for a in args if a != str(key_path)]
    if len(args) != 1:
        print(__doc__)
        return 2
    if not Path(key_path).exists():
        print(f"Answer key not found: {key_path}. Your facilitator holds it.")
        return 2
    key = json.loads(Path(key_path).read_text(encoding="utf-8"))
    r = score(load_findings(args[0]), key)
    if "--json" in argv:
        out = {k: v for k, v in r.items() if k not in ("bugs", "fp_detail")}
        out["bugs"] = {i: bool(b["caught_by"]) for i, b in r["bugs"].items()}
        print(json.dumps(out, indent=2))
    else:
        print(f"Bugs caught       {r['caught']}/{r['total']}")
        for bid, b in r["bugs"].items():
            mark = "caught" if b["caught_by"] else "MISSED"
            print(f"   {bid}  {b['category']:<28} {b['pr']:<24} {mark}")
        print(f"False positives   {r['false_positives']}")
        for f, kind in r["fp_detail"]:
            print(f"   {f.get('pr')} {f.get('file')}:{f.get('line')}  [{kind}]  {str(f.get('title', ''))[:60]}")
        print(f"Nits              {r['nits']}   (not scored, tier caps them for Gold)")
        if r["duplicates"]:
            print(f"Duplicate hits    {r['duplicates']}   (extra findings on a bug already caught)")
        if r["unknown_pr"]:
            print(f"Unknown pr        {r['unknown_pr']}   (finding names a pull request that is not in the set)")
        if r["precision"] is not None:
            print(f"Precision         {r['precision']}   (caught / (caught + false positives))")
        print(f"TIER              {r['tier']}")
    return 0 if r["tier"] != "Not yet" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
