#!/usr/bin/env python3
"""Lab 1 security gate: a static, local check of a CI workflow that runs Claude.

Usage:
    python3 security_gate.py PATH [PATH ...] [--json] [--platform github|gitlab]

PATH is a workflow file, a .gitlab-ci.yml, or a directory (every *.yml / *.yaml
inside it is checked). No network, no GitHub or GitLab access, no model calls.

Needs PyYAML:  pip install pyyaml

Scoring: each check is worth a fixed number of points. A file PASSES when it
scores 90 or more AND every check marked CRITICAL passes. Exit code 0 when every
Claude workflow passes, 1 otherwise, 2 for a usage error.

This is a teaching checklist, not a security audit. A clean score means the file
avoids the traps in this lab. It does not mean the pipeline is safe in general.
"""
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is required: pip install pyyaml")

PASS_SCORE = 90

# Fields an outsider can write: text a stranger controls.
UNTRUSTED = (
    ".body", ".title", ".head_ref", "head.ref", "head.label", "head.repo",
    ".message", ".email", ".page_name", "comment.body", "review.body",
    "github.head_ref", "discussion.body", "discussion.title",
)
WRITE_OK = {"contents", "pull-requests", "issues"}      # may be write
CLAUDE_ACTION = "anthropics/claude-code-action"


class Check:
    def __init__(self, cid, name, points, critical=False):
        self.cid, self.name, self.points, self.critical = cid, name, points, critical
        self.findings = []      # (line or None, message)
        self.earned = points

    def fail(self, cost, message, line=None):
        self.earned = max(0, self.earned - cost)
        self.findings.append((line, message))

    @property
    def passed(self):
        return not self.findings


def load(path):
    text = Path(path).read_text(encoding="utf-8")
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        sys.exit(f"{path}: not valid YAML: {exc}")
    return text, data if isinstance(data, dict) else {}


def line_of(lines, pattern):
    rx = re.compile(pattern)
    for i, ln in enumerate(lines, 1):
        if not ln.lstrip().startswith("#") and rx.search(ln):
            return i
    return None


def untrusted_expr(block):
    """Return the first ${{ }} expression in block that reads an outsider-controlled field."""
    for m in re.finditer(r"\$\{\{(.*?)\}\}", block, re.S):
        expr = m.group(1)
        if "github." in expr and any(tok in expr for tok in UNTRUSTED):
            return expr.strip()
    return None


# ----------------------------------------------------------------------------- GitHub
def triggers(data):
    on = data.get("on", data.get(True))
    if isinstance(on, str):
        return {on: {}}
    if isinstance(on, list):
        return {t: {} for t in on}
    return on or {}


def claude_steps(job):
    return [s for s in (job.get("steps") or []) if CLAUDE_ACTION in str(s.get("uses", ""))]


def check_github(path, text, data):
    lines = text.splitlines()
    trig = triggers(data)
    jobs = data.get("jobs") or {}
    checks = []

    # T1 trigger
    t1 = Check("T1", "Who can trigger a run", 15, critical=True)
    if "pull_request_target" in trig:
        t1.fail(15, "pull_request_target runs with secrets on code and text from outsiders. "
                    "Use pull_request.", line_of(lines, r"pull_request_target"))
    for jname, job in jobs.items():
        for step in claude_steps(job):
            w = step.get("with") or {}
            if "allowed_non_write_users" in w:
                t1.fail(15, "allowed_non_write_users lets people without write access trigger a run.",
                        line_of(lines, r"allowed_non_write_users"))
        comment_like = {"issue_comment", "pull_request_review_comment", "issues",
                        "pull_request_review"} & set(trig)
        if comment_like and claude_steps(job) and not job.get("if"):
            t1.fail(5, f"Job '{jname}' has no 'if' guard on a comment or issue trigger, "
                       "so every event starts a runner.", line_of(lines, rf"^\s*{re.escape(jname)}:"))
    checks.append(t1)

    # T2 permissions
    t2 = Check("T2", "Permissions granted", 10)
    perms = [("workflow", data.get("permissions"))] + \
            [(f"job {n}", j.get("permissions")) for n, j in jobs.items() if claude_steps(j)]
    if not any(p for _, p in perms):
        t2.fail(10, "No permissions block. The repository default may grant write access.")
    for where, p in perms:
        if p in ("write-all",):
            t2.fail(10, f"{where}: permissions: write-all.", line_of(lines, r"write-all"))
        elif isinstance(p, dict):
            for scope, level in p.items():
                if level == "write" and scope not in WRITE_OK and scope != "id-token":
                    t2.fail(5, f"{where}: '{scope}: write' is more than a review or fix workflow needs.",
                            line_of(lines, rf"{re.escape(scope)}:\s*write"))
    checks.append(t2)

    # T3 secrets
    t3 = Check("T3", "Secrets handling", 15, critical=True)
    for jname, job in jobs.items():
        for step in job.get("steps") or []:
            run = str(step.get("run") or "")
            if re.search(r"secrets\.", run):
                t3.fail(15, "A secret is expanded inside a run step, where it can reach the log.",
                        line_of(lines, r"secrets\.\w+.*(echo|printf)|(echo|printf).*secrets\."))
            if re.search(r"(^|[\s;&|])(printenv|env)\s*($|[|;&])|set\s+-x|echo\s+\$\w*(KEY|TOKEN|SECRET)", run, re.M):
                t3.fail(10, "A run step dumps the environment or echoes a credential variable.",
                        line_of(lines, r"printenv|^\s*-?\s*env\b|set -x"))
        for step in claude_steps(job):
            w = step.get("with") or {}
            for key in ("anthropic_api_key", "claude_code_oauth_token"):
                if key in w and not str(w[key]).strip().startswith("${{"):
                    t3.fail(15, f"'{key}' is a literal value. Reference a repository secret.",
                            line_of(lines, rf"{key}:"))
    checks.append(t3)

    # T4 bot loop
    t4 = Check("T4", "Bot loop control", 10)
    allowed_bots = None
    for job in jobs.values():
        for step in claude_steps(job):
            allowed_bots = (step.get("with") or {}).get("allowed_bots", allowed_bots)
    if allowed_bots is not None and str(allowed_bots).strip() in ("*", "'*'", '"*"'):
        t4.fail(5, "allowed_bots: '*' lets any bot, including Claude's own commits, start a run.",
                line_of(lines, r"allowed_bots"))
    has_conc = bool(data.get("concurrency")) or any(j.get("concurrency") for j in jobs.values())
    if not has_conc:
        t4.fail(5, "No concurrency group, so overlapping or looping runs are not capped.")
    checks.append(t4)

    # T5 injection
    t5 = Check("T5", "Untrusted text in a command or prompt", 15, critical=True)
    for jname, job in jobs.items():
        for step in job.get("steps") or []:
            run = str(step.get("run") or "")
            expr = untrusted_expr(run)
            if expr:
                t5.fail(15, f"Outsider-controlled text '{expr}' is expanded inside a run step "
                            "(shell injection).", line_of(lines, re.escape(expr.split()[0])[:40]))
            prompt = str((step.get("with") or {}).get("prompt") or "")
            expr = untrusted_expr(prompt)
            if expr:
                t5.fail(15, f"Outsider-controlled text '{expr}' is pasted into the prompt "
                            "(prompt injection).", line_of(lines, re.escape(expr.split()[0])[:40]))
    checks.append(t5)

    # T6 tools
    t6 = Check("T6", "Tool grants", 10)
    for job in jobs.values():
        for step in claude_steps(job):
            args = str((step.get("with") or {}).get("claude_args") or "")
            if "--allowedTools" not in args and "--allowed-tools" not in args:
                t6.fail(5, "No --allowedTools. State exactly which tools a run may use.")
            m = re.search(r"--allowed-?[tT]ools\s+(\"[^\"]*\"|'[^']*'|\S+)", args)
            if m:
                for tool in re.split(r"[,\s]+", m.group(1).strip("\"'")):
                    if tool == "Bash" or tool in ("Bash(*)", "Bash(*:*)"):
                        t6.fail(5, "Bare Bash grants any shell command. Scope it, for example Bash(python3 -m pytest *).",
                                line_of(lines, r"allowedTools"))
                        break
            if "--dangerously-skip-permissions" in args or "bypassPermissions" in args:
                t6.fail(10, "Permission checks are switched off.",
                        line_of(lines, r"dangerously-skip-permissions|bypassPermissions"))
    checks.append(t6)

    # T7 limits
    t7 = Check("T7", "Cost and runtime limits", 10)
    for jname, job in jobs.items():
        if not claude_steps(job):
            continue
        if not job.get("timeout-minutes"):
            t7.fail(5, f"Job '{jname}' has no timeout-minutes.")
        args = " ".join(str((s.get("with") or {}).get("claude_args") or "") for s in claude_steps(job))
        if "--max-turns" not in args:
            t7.fail(5, f"Job '{jname}' has no --max-turns in claude_args.")
    checks.append(t7)

    # T8 pin
    t8 = Check("T8", "Action reference", 5)
    for job in jobs.values():
        for step in claude_steps(job):
            ref = str(step["uses"]).split("@", 1)[1] if "@" in str(step["uses"]) else ""
            if not (ref == "v1" or re.fullmatch(r"[0-9a-f]{40}", ref)):
                t8.fail(5, f"anthropics/claude-code-action@{ref or '(none)'} is not the v1 release "
                           "or a full commit SHA.", line_of(lines, CLAUDE_ACTION))
    checks.append(t8)

    # T9 token
    t9 = Check("T9", "Pushes that start CI", 10)
    for job in jobs.values():
        for step in claude_steps(job):
            tok = str((step.get("with") or {}).get("github_token") or "")
            if "secrets.GITHUB_TOKEN" in tok:
                t9.fail(10, "Passing the default GITHUB_TOKEN means CI will not run on Claude's commits.",
                        line_of(lines, r"github_token"))
        for step in job.get("steps") or []:
            if re.search(r"git\s+push", str(step.get("run") or "")):
                t9.fail(5, "A run step pushes with the default token; those commits do not start CI.",
                        line_of(lines, r"git\s+push"))
    checks.append(t9)
    return checks


# ----------------------------------------------------------------------------- GitLab
def script_text(job):
    parts = []
    for key in ("before_script", "script", "after_script"):
        v = job.get(key) or []
        parts.extend(v if isinstance(v, list) else [v])
    return "\n".join(str(p) for p in parts)


def gitlab_claude_jobs(data):
    return {n: j for n, j in data.items() if isinstance(j, dict) and "claude" in script_text(j)
            and re.search(r"(^|\s)claude\s", script_text(j) + " ")}


def check_gitlab(path, text, data):
    lines = text.splitlines()
    jobs = gitlab_claude_jobs(data)
    checks = []
    SECRET_VAR = r"\$\{?(\w*(KEY|TOKEN|SECRET|PASSWORD)\w*)\}?"
    UNTRUSTED_VARS = ("CI_MERGE_REQUEST_DESCRIPTION", "CI_MERGE_REQUEST_TITLE", "CI_COMMIT_MESSAGE",
                      "CI_COMMIT_DESCRIPTION", "CI_COMMIT_TITLE", "CI_MERGE_REQUEST_SOURCE_BRANCH_NAME",
                      "AI_FLOW_INPUT", "AI_FLOW_CONTEXT")

    l1 = Check("L1", "Rules and who can start a job", 20, critical=True)
    for n, j in jobs.items():
        rules = j.get("rules")
        if not rules:
            l1.fail(20, f"Job '{n}' has no rules, so any pipeline source runs it.")
            continue
        conds = " ".join(str(r.get("if", "")) for r in rules if isinstance(r, dict))
        if "merge_request_event" in conds and "CI_MERGE_REQUEST_SOURCE_PROJECT_PATH" not in conds:
            l1.fail(10, f"Job '{n}' runs on merge request events with no fork guard "
                        "($CI_MERGE_REQUEST_SOURCE_PROJECT_PATH == $CI_PROJECT_PATH).",
                    line_of(lines, r"merge_request_event"))
        if re.search(r'CI_PIPELINE_SOURCE\s*==\s*"(trigger|api|pipeline)"', conds) and \
                "CI_COMMIT_REF_PROTECTED" not in conds:
            l1.fail(10, f"Job '{n}' runs from the trigger API with no protected-ref condition.",
                    line_of(lines, r'"trigger"|"api"|"pipeline"'))
    checks.append(l1)

    l2 = Check("L2", "Secrets handling", 20, critical=True)
    for n, j in jobs.items():
        st = script_text(j)
        if "ANTHROPIC_API_KEY" in (j.get("variables") or {}) or "ANTHROPIC_API_KEY" in (data.get("variables") or {}):
            l2.fail(20, "ANTHROPIC_API_KEY is defined in the YAML. Use a masked CI/CD variable.",
                    line_of(lines, r"ANTHROPIC_API_KEY:"))
        if re.search(rf"\b(echo|printf)\b[^\n]*{SECRET_VAR}", st):
            l2.fail(15, "A script line prints a credential variable.", line_of(lines, r"echo.*KEY|echo.*TOKEN"))
        if re.search(r"(^|\n)\s*(printenv|env)\s*($|\||;)|set\s+-x", st):
            l2.fail(10, "A script line dumps the environment.", line_of(lines, r"^\s*-\s*(env|printenv)\b|set -x"))
    checks.append(l2)

    l3 = Check("L3", "Untrusted text in the claude command", 20, critical=True)
    for n, j in jobs.items():
        st = script_text(j)
        for var in UNTRUSTED_VARS:
            if re.search(rf"\$\{{?{var}\b", st):
                l3.fail(20, f"${var} is outsider-controlled text pasted into the command line or prompt.",
                        line_of(lines, rf"\${{?{var}"))
                break
    checks.append(l3)

    l4 = Check("L4", "Tool grants", 15)
    for n, j in jobs.items():
        st = script_text(j)
        m = re.search(r"--allowed-?[tT]ools\s+(\"[^\"]*\"|'[^']*'|\S+)", st)
        if not m:
            l4.fail(8, f"Job '{n}' has no --allowedTools.")
        else:
            toks = re.split(r"[,\s]+", m.group(1).strip("\"'"))
            if any(t in ("Bash", "Bash(*)") for t in toks):
                l4.fail(8, "Bare Bash grants any shell command. Scope it, for example Bash(git diff *).",
                        line_of(lines, r"allowedTools"))
        if "--dangerously-skip-permissions" in st:
            l4.fail(15, "Permission checks are switched off.", line_of(lines, r"dangerously-skip"))
    checks.append(l4)

    l5 = Check("L5", "Cost and runtime limits", 10)
    for n, j in jobs.items():
        if "--max-turns" not in script_text(j):
            l5.fail(5, f"Job '{n}' has no --max-turns.")
        if not j.get("timeout"):
            l5.fail(5, f"Job '{n}' has no timeout.")
    checks.append(l5)

    l6 = Check("L6", "Loop and overlap control", 15)
    for n, j in jobs.items():
        if not j.get("resource_group"):
            l6.fail(8, f"Job '{n}' has no resource_group, so runs can overlap.")
        rules = " ".join(str(r.get("if", "")) for r in (j.get("rules") or []) if isinstance(r, dict))
        if "CI_COMMIT_MESSAGE" not in rules and "CI_COMMIT_AUTHOR" not in rules and "GITLAB_USER_LOGIN" not in rules:
            l6.fail(7, f"Job '{n}' has no rule that skips commits Claude made, so its own push can start another run.")
    checks.append(l6)
    return checks


# ----------------------------------------------------------------------------- driver
def gate(path, platform=None):
    text, data = load(path)
    name = Path(path).name
    plat = platform or ("gitlab" if name.startswith(".gitlab-ci") else "github")
    if plat == "github":
        is_claude = any(claude_steps(j) for j in (data.get("jobs") or {}).values() if isinstance(j, dict))
        checks = check_github(path, text, data) if is_claude else []
    else:
        checks = check_gitlab(path, text, data) if gitlab_claude_jobs(data) else []
    if not checks:
        return dict(path=str(path), platform=plat, skipped=True, score=None, passed=True, checks=[])
    score = sum(c.earned for c in checks)
    passed = score >= PASS_SCORE and all(c.passed for c in checks if c.critical)
    return dict(path=str(path), platform=plat, skipped=False, score=score, passed=passed, checks=checks)


def collect(paths):
    files = []
    for p in paths:
        p = Path(p)
        if p.is_dir():
            files += sorted([*p.rglob("*.yml"), *p.rglob("*.yaml")])
        elif p.exists():
            files.append(p)
        else:
            sys.exit(f"Not found: {p}")
    return files


def to_json(res):
    out = dict(res)
    out["checks"] = [dict(id=c.cid, name=c.name, points=c.points, earned=c.earned, critical=c.critical,
                          findings=[dict(line=l, message=m) for l, m in c.findings]) for c in res["checks"]]
    return out


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    as_json = "--json" in argv
    plat = None
    if "--platform" in argv:
        i = argv.index("--platform")
        plat = argv[i + 1]
        args = [a for a in args if a != plat]
    if not args:
        print(__doc__)
        return 2
    results = [gate(f, plat) for f in collect(args)]
    if as_json:
        print(json.dumps([to_json(r) for r in results], indent=2))
    else:
        for r in results:
            print(f"\n=== {r['path']}  ({r['platform']})")
            if r["skipped"]:
                print("    No Claude step found. Skipped.")
                continue
            for c in r["checks"]:
                tag = "CRITICAL" if c.critical else "        "
                mark = "ok  " if c.passed else "FAIL"
                print(f"  [{mark}] {c.cid} {c.name:<42} {c.earned:>3}/{c.points:<3} {tag}")
                for line, msg in c.findings:
                    where = f"line {line}: " if line else ""
                    print(f"         - {where}{msg}")
            verdict = "PASS" if r["passed"] else "NOT YET"
            print(f"  SCORE {r['score']}/100   {verdict}  (pass needs {PASS_SCORE}+ and every CRITICAL check ok)")
    return 0 if all(r["passed"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
