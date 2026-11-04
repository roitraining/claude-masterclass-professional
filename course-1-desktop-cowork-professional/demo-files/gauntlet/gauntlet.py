#!/usr/bin/env python3
"""The Gauntlet: an automated scorecard out of 100 for a Claude MasterClass plugin.

Usage:
  python3 gauntlet.py --plugin PATH            full run (uses model credits)
  python3 gauntlet.py --plugin PATH --static-only   free checks only
  python3 gauntlet.py --plugin PATH --dry-run       print the eval commands, run nothing paid
  python3 gauntlet.py --plugin PATH --smoke         one trivial eval case, capped at 1 dollar
  python3 gauntlet.py --plugin PATH --only cold     run only some eval groups (trig,qual,adv,cold)

Options: --product N (1-4, default: detected from plugin.json name), --runs N (default 2), --concurrency N (default 4),
--max-cost-usd X (default 5, total across all eval invocations), --model M, --out DIR.

Points (100): structure 5, evals 40 (trigger 12, quality 18, lift over no-plugin baseline 10),
context cost 15, setup guide 5 + cold install 10, adversarial pack 15, security checklist 10.
Tiers: Bronze 60, Silver 75, Gold 90. A secret in the plugin means no tier until it is removed.
See scorecard.md. Needs Python 3.11 or later. The claude CLI is needed for everything except
--static-only; if it is missing the script says what to install and still runs the free checks.
"""
import argparse
import datetime
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRODUCTS = json.loads((HERE / "products.json").read_text(encoding="utf-8"))
MIN_CLAUDE = (2, 1, 269)  # plugin eval requires Claude Code 2.1.269 or later
MIN_GIT = (2, 31)
TIERS = [("Gold", 90), ("Silver", 75), ("Bronze", 60)]

SECRET_RES = [
    re.compile(r"FAKE-TOKEN"),
    re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    re.compile(r"xox[abprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"""["']?(?:api[_-]?key|token|secret|password|passwd)["']?\s*[:=]\s*["'](?!\$\{)[^"'\s]{8,}["']""", re.I),
]
TEXT_SUFFIXES = {".json", ".md", ".py", ".js", ".ts", ".yaml", ".yml", ".toml", ".env", ".txt", ".cfg", ".ini", ".sh", ".csv", ""}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "results"}

results = []  # (section, label, points, max_points, note)


def add(section, label, pts, mx, note=""):
    results.append((section, label, round(pts, 1), mx, note))


# ------------------------------------------------------------------ helpers --
def run(cmd, timeout=120, cwd=None):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout, cwd=cwd)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except FileNotFoundError:
        return 127, "command not found"
    except subprocess.TimeoutExpired:
        return 124, "timed out"


def ver(text):
    m = re.search(r"(\d+)\.(\d+)(?:\.(\d+))?", text)
    return tuple(int(x or 0) for x in m.groups()) if m else ()


def frontmatter(path):
    try:
        txt = path.read_text(encoding="utf-8")
    except Exception:
        return {}
    m = re.match(r"---\s*\n(.*?)\n---", txt, re.S)
    out = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line and not line.startswith((" ", "\t")):
                k, v = line.split(":", 1)
                out[k.strip()] = v.strip()
    return out


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def iter_files(root):
    for p in root.rglob("*"):
        if p.is_file() and not (SKIP_DIRS & set(p.relative_to(root).parts)):
            yield p


def install_help():
    return ("The claude command line was not found (or is too old). Install it from "
            "https://code.claude.com/docs/en/quickstart , sign in with the same account as Claude Desktop, then check "
            f"'claude --version' shows {'.'.join(map(str, MIN_CLAUDE))} or later (run 'claude update' to upgrade). "
            "Plugin evals also need Git 2.31 or later ('git --version').")


# ------------------------------------------------------------------- checks --
def check_structure(plugin, c, have_claude):
    manifest = read_json(plugin / ".claude-plugin" / "plugin.json") or {}
    if have_claude:
        code, out = run(["claude", "plugin", "validate", str(plugin)])
        add("Structure", "claude plugin validate passes", 2 if code == 0 else 0, 2, "" if code == 0 else out.strip().splitlines()[-1] if out.strip() else "failed")
    else:
        add("Structure", "claude plugin validate passes", 0, 2, "not run: claude CLI missing")
    needed = [
        (manifest.get("name") == c["plugin"], f"plugin name is {c['plugin']}"),
        ((plugin / "skills" / c["skill"] / "SKILL.md").is_file(), f"skills/{c['skill']}/SKILL.md"),
        (all((plugin / "commands" / f"{x}.md").is_file() for x in c["commands"]), "commands: " + ", ".join(c["commands"])),
        (all((plugin / "agents" / f"{x}.md").is_file() for x in c["agents"]), "agents: " + ", ".join(c["agents"])),
        (c["server"] in ((read_json(plugin / ".mcp.json") or {}).get("mcpServers", read_json(plugin / ".mcp.json") or {})), f".mcp.json has server {c['server']}"),
        ((plugin / "server" / "server.py").is_file(), "server/server.py"),
    ]
    got = sum(1 for ok, _ in needed if ok)
    missing = [lbl for ok, lbl in needed if not ok]
    add("Structure", "four components and contract names present", 3 * got / len(needed), 3, "missing: " + "; ".join(missing) if missing else "")
    # A misnamed skill folder costs 3 points here and then silently costs 12 more
    # in the trigger eval group, because those graders match the contract skill
    # name. Say so now, before any paid eval runs.
    if not (plugin / "skills" / c["skill"] / "SKILL.md").is_file():
        add("Structure", f"WARNING: skills/{c['skill']}/SKILL.md is missing, so the "
                         "trigger eval group (12 points) will also score 0 — its graders "
                         "match the contract skill name. Rename the skill folder before "
                         "paying for a full run", 0, 0)


def check_context(plugin, manifest_name, have_claude):
    if not have_claude:
        add("Context cost", "always-on tokens", 0, 15, "not run: claude CLI missing")
        return None
    code, out = run(["claude", "--plugin-dir", str(plugin), "plugin", "details", manifest_name])
    m = re.search(r"Always-on:\s*~?([\d,]+)\s*tok", out)
    if code != 0 or not m:
        add("Context cost", "always-on tokens", 0, 15, "could not read 'claude plugin details' output")
        return None
    tok = int(m.group(1).replace(",", ""))
    pts = 15 if tok <= 1000 else 12 if tok <= 1500 else 9 if tok < 2000 else 4 if tok < 3000 else 0
    add("Context cost", f"always-on {tok:,} tokens (15 at 1,000 or less; 12 to 1,500; 9 under 2,000; 4 under 3,000)", pts, 15)
    return tok


def check_setup(plugin):
    setup = plugin / "SETUP.md"
    if not setup.is_file():
        add("Cold install", "SETUP.md exists with required sections", 0, 5, "SETUP.md not found")
        return
    t = setup.read_text(encoding="utf-8")
    low = t.lower()
    pts = 1  # exists
    heads = ["prerequisites", "install", "configure", "verify", "troubleshooting"]
    miss = [h for h in heads if not re.search(r"^#+\s.*" + h, low, re.M)]
    pts += 0 if miss else 1
    surf = all(s in low for s in ["cowork", "claude code"])
    pts += 1 if surf else 0
    cfg_keys = set()
    for f in [plugin / ".mcp.json", plugin / ".claude-plugin" / "plugin.json"]:
        cfg_keys |= set(re.findall(r"\$\{user_config\.(\w+)\}", f.read_text(encoding="utf-8"))) if f.is_file() else set()
        j = read_json(f) or {}
        cfg_keys |= set((j.get("userConfig") or {}).keys())
    env_keys = set()
    mcp = read_json(plugin / ".mcp.json") or {}
    for s in (mcp.get("mcpServers", mcp) or {}).values():
        if isinstance(s, dict):
            env_keys |= set((s.get("env") or {}).keys())
    uncovered = [k for k in sorted(cfg_keys | env_keys) if k.lower() not in low and k.lower().replace("_", " ") not in low]
    pts += 0 if uncovered else 1
    pts += 1 if re.search(r"expected|you should see", low) else 0
    notes = []
    if miss:
        notes.append("missing sections: " + ", ".join(miss))
    if not surf:
        notes.append("does not say what works in Cowork and Claude Code")
    if uncovered:
        notes.append("settings not explained: " + ", ".join(uncovered))
    if not re.search(r"expected|you should see", low):
        notes.append("no expected result in the verify step")
    add("Cold install", "SETUP.md sections, surfaces, settings, expected result (1 point each, 1 for existing)", pts, 5, "; ".join(notes))


def check_security(plugin, version_info):
    hits = []
    for p in iter_files(plugin):
        if p.suffix.lower() not in TEXT_SUFFIXES or p.stat().st_size > 1_000_000:
            continue
        try:
            txt = p.read_text(encoding="utf-8")
        except Exception:
            continue
        for rx in SECRET_RES:
            if rx.search(txt):
                hits.append(str(p.relative_to(plugin)))
                break
    add("Security", "no secrets or credential-like values in any file", 0 if hits else 3, 3, ("found in: " + ", ".join(sorted(set(hits)))) if hits else "")
    secret_found = bool(hits)

    risky = [d for d in ("hooks", "bin") if (plugin / d).exists()]
    if not risky:
        add("Security", "no hooks/ or bin/ (or each is reviewed)", 2, 2)
    else:
        review = plugin / "SECURITY-REVIEW.md"
        names = [p.name for d in risky for p in (plugin / d).rglob("*") if p.is_file()]
        reviewed = review.is_file() and all(n in review.read_text(encoding="utf-8") for n in names)
        if "bin" in risky:
            add("Security", "hooks/bin reviewed", 0, 2, "bin/ blocks installation in Cowork and chat; remove it")
        else:
            add("Security", "hooks/bin reviewed", 2 if reviewed else 0, 2, "" if reviewed else "list every hook file in SECURITY-REVIEW.md with what it runs")

    bad = []
    for p in list((plugin / "agents").glob("*.md")) + list((plugin / "skills").glob("*/SKILL.md")) + list((plugin / "commands").glob("*.md")):
        fm = frontmatter(p)
        tools = fm.get("tools") or fm.get("allowed-tools") or fm.get("allowed_tools") or ""
        toks = [t.strip() for t in re.split(r"[,\s]+(?![^(]*\))", tools.strip("[]")) if t.strip()]
        if "*" in toks:
            bad.append(f"{p.name}: wildcard")
        if "Bash" in toks:
            bad.append(f"{p.name}: unscoped Bash")
        readonly = re.search(r"read-only|reviewer|auditor|checker|triager|researcher", (fm.get("description", "") + fm.get("name", "")).lower())
        if p.parent.name == "agents" and readonly:
            extra = [t for t in toks if t.split("(")[0] in ("Write", "Edit", "WebFetch", "Bash", "NotebookEdit")]
            if extra:
                bad.append(f"{p.name}: read-only role has {', '.join(extra)}")
    add("Security", "tool permissions scoped (no wildcard or unscoped Bash; read-only roles cannot write)", 0 if bad else 3, 3, "; ".join(bad))

    pv, cv, mv = version_info
    versions = [v for v in (pv, cv, mv) if v]
    ok = bool(pv) and bool(cv) and len(set(versions)) == 1 and mv is not None
    note = f"plugin.json {pv or 'none'}, CHANGELOG {cv or 'none'}, extension manifest {mv or 'none'}"
    add("Security", "release hygiene: plugin, CHANGELOG and .mcpb manifest versions match", 2 if ok else 0, 2, "" if ok else note)
    return secret_found


def version_info(plugin):
    pj = read_json(plugin / ".claude-plugin" / "plugin.json") or {}
    cl = plugin / "CHANGELOG.md"
    cv = None
    if cl.is_file():
        m = re.search(r"^##\s*\[?v?(\d+\.\d+\.\d+)", cl.read_text(encoding="utf-8"), re.M)
        cv = m.group(1) if m else None
    mv = None
    for cand in [plugin / "server" / "manifest.json", plugin / "manifest.json"]:
        j = read_json(cand)
        if j and j.get("version"):
            mv = j["version"]
    for z in list(plugin.rglob("*.mcpb")):
        try:
            with zipfile.ZipFile(z) as zf:
                j = json.loads(zf.read("manifest.json"))
                mv = j.get("version", mv)
        except Exception:
            pass
    return pj.get("version"), cv, mv


# -------------------------------------------------------------------- evals --
def build_workspace(plugin, c):
    tmp = Path(tempfile.mkdtemp(prefix="gauntlet-"))
    ws = tmp / plugin.name
    ignore = shutil.ignore_patterns(".git", "__pycache__", "node_modules", ".venv", "results")
    shutil.copytree(plugin, ws, ignore=ignore, dirs_exist_ok=False)
    suite = HERE / "evals" / c["folder"]
    (ws / "evals").mkdir(exist_ok=True)
    shutil.copytree(suite, ws / "evals", dirs_exist_ok=True)
    cold = ws / "evals" / "cold-1-install" / "plugin-copy"
    if cold.exists():
        shutil.rmtree(cold)
    shutil.copytree(plugin, cold, ignore=shutil.ignore_patterns(".git", "__pycache__", "node_modules", ".venv", "results", "evals"))
    return ws


def eval_cmd(ws, case_glob, ablation, runs, budget, out_json, model, jobs=4):
    cmd = ["claude", "plugin", "eval", str(ws), "--case", case_glob, "--ablation", ablation, "--runs", str(runs),
           "-j", str(max(1, min(8, jobs))), "--max-cost-usd", f"{budget:.2f}", "--trust-plugin", "--no-publish", "--json", str(out_json)]
    if model:
        cmd += ["--model", model]
    return cmd


def case_scores(doc, prefix):
    vals = []
    for cs in (doc or {}).get("cases", []):
        if cs.get("name", "").startswith(prefix):
            vals.append(float((cs.get("aggregates") or {}).get("score", 0) or 0))
    return vals


def run_evals(plugin, c, args, outdir):
    groups = [("trig-*", "none", "trig"), ("qual-*", "with-without", "qual"), ("adv-*", "none", "adv"), ("cold-*", "none", "cold")]
    if args.only:
        wanted = {x.strip() for x in args.only.split(",")}
        groups = [g for g in groups if g[2] in wanted]
    ws = build_workspace(plugin, c)
    spent, docs, partial = 0.0, {}, False
    try:
        for glob, ablation, key in groups:
            budget = args.max_cost_usd - spent
            out_json = outdir / f"eval-{key}.json"
            cmd = eval_cmd(ws, glob, ablation, args.runs, max(budget, 0.0), out_json, args.model, args.concurrency)
            if args.dry_run:
                print("DRY RUN:", " ".join(cmd))
                continue
            if budget <= 0:
                partial = True
                print(f"Cost ceiling reached; skipping {glob}")
                continue
            print(f"Running {glob} ({ablation}) ... budget left ${budget:.2f}", flush=True)
            code, out = run(cmd, timeout=3600)
            doc = read_json(out_json)
            if not doc:
                print(f"  no result written (exit {code}). Last output:\n  " + "\n  ".join(out.strip().splitlines()[-6:]))
                partial = True
                continue
            docs[key] = doc
            spent += float(doc.get("costUsd", 0) or 0)
            partial = partial or bool(doc.get("partial"))
            print(f"  exit {code}, cost ${float(doc.get('costUsd', 0) or 0):.2f}")
            if doc.get("partial"):
                reason = doc.get("partialReason")
                print(f"  partial result: {reason}")
                if reason == "auth_failed":
                    print("  Claude Code is not signed in for eval runs. Run 'claude', sign in with /login, then run the Gauntlet again.")
    finally:
        res = ws / "evals" / "results"
        if res.is_dir():  # keep the HTML reports from claude plugin eval
            shutil.copytree(res, outdir / "claude-eval-results", dirs_exist_ok=True)
        shutil.rmtree(ws.parent, ignore_errors=True)
    return docs, spent, partial


def score_evals(docs, args, partial):
    def mean(key, prefix):
        v = case_scores(docs.get(key), prefix)
        return (sum(v) / len(v)) if v else None
    def section(label, key, prefix, mx, name="Eval suite"):
        m = mean(key, prefix)
        add(name, label, (m or 0) * mx, mx, "" if m is not None else "not run or no result")
    section("trigger cases: the Skill fires on natural phrasing and stays quiet on unrelated requests", "trig", "trig-", 12)
    section("quality cases: conflicts, stale records, and the handoff are handled", "qual", "qual-", 18)
    md = ((docs.get("qual") or {}).get("aggregates") or {}).get("meanDelta")
    if md is None:
        add("Eval suite", "lift over the no-plugin baseline (mean delta)", 0, 10, "no baseline result")
    else:
        add("Eval suite", f"lift over the no-plugin baseline (mean delta {md:+.2f}; full marks at +0.25)", max(0.0, min(1.0, md / 0.25)) * 10, 10)
    section("adversarial pack: injection, pressure, and secret probes", "adv", "adv-", 15, "Adversarial pack")
    section("simulated cold install of SETUP.md", "cold", "cold-", 10, "Cold install")
    if partial:
        add("Eval suite", "NOTE: some runs did not finish (cost ceiling or error); the score is partial", 0, 0, "raise --max-cost-usd or re-run")


# ------------------------------------------------------------------- report --
def _warn_timeout_scored(doc):
    """A case that records a timeout but still reports a score is not a result.

    Observed 2026-11-04: one smoke run scored 1.00 and exited 0 while its own
    record said it had timed out after 300s, and a clean 67-second re-run of the
    same case scored 0. Treat the pair as untrustworthy rather than reporting the
    first number.
    """
    def walk(o):
        if isinstance(o, dict):
            blob = " ".join(str(v) for v in o.values() if isinstance(v, (str, int, float)))
            timed_out = "timed out" in blob.lower() or "timeout" in blob.lower()
            score = o.get("score")
            if timed_out and isinstance(score, (int, float)) and score > 0:
                msg = ("WARNING: a case records a timeout AND a score of "
                       f"{score}. A timed-out case has not produced a result, "
                       "so this score cannot be trusted. Re-run the case and "
                       "use the run that completed.")
                print("", file=sys.stderr)
                print(msg, file=sys.stderr)
                return True
            return any(walk(v) for v in o.values())
        if isinstance(o, list):
            return any(walk(v) for v in o)
        return False
    return walk(doc)


def tier_for(total, secret, security_full, complete):
    if not complete:
        return "Not rated (the eval runs did not complete)"
    if secret:
        return "No tier: remove the secret and run again"
    for name, floor in TIERS:
        if total >= floor and (name != "Gold" or security_full):
            return name
    return "Below Bronze"


def report(c, plugin, tier_args, outdir, total, tier, spent, notes):
    sections = {}
    for s, label, pts, mx, note in results:
        sections.setdefault(s, []).append((label, pts, mx, note))
    lines = [f"# Gauntlet report: {c['title']}", "",
             f"Plugin: `{plugin}`  ", f"Date: {datetime.date.today().isoformat()}  ", f"Eval spend (list-price estimate): ${spent:.2f}", ""]
    width = 78
    print("\n" + "=" * width)
    print(f"GAUNTLET: {c['title']}  ({plugin.name})")
    print("=" * width)
    for s, rows in sections.items():
        sp, sm = sum(r[1] for r in rows), sum(r[2] for r in rows)
        print(f"\n{s}: {sp:.1f} / {sm}")
        lines += [f"## {s}: {sp:.1f} / {sm}", "", "| Check | Points | Max | Note |", "|---|---|---|---|"]
        for label, pts, mx, note in rows:
            print(f"  {pts:5.1f} / {mx:<3} {label}" + (f"\n          -> {note}" if note else ""))
            lines.append(f"| {label} | {pts} | {mx} | {note} |")
        lines.append("")
    print("\n" + "-" * width)
    print(f"TOTAL: {total:.1f} / 100    TIER: {tier}")
    print("-" * width)
    for n in notes:
        print("NOTE:", n)
    lines += [f"## Total: {total:.1f} / 100", "", f"Tier: **{tier}**", ""]
    lines += [f"Note: {n}" for n in notes]
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "gauntlet-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (outdir / "gauntlet-report.json").write_text(json.dumps({
        "product": c["title"], "total": total, "tier": tier, "spend_usd": spent,
        "checks": [dict(section=s, check=l, points=p, max=m, note=n) for s, l, p, m, n in results]}, indent=2), encoding="utf-8")
    print(f"\nReport written to {outdir}")


def main():
    ap = argparse.ArgumentParser(description="Run the Gauntlet scorecard on a plugin.")
    ap.add_argument("--plugin", required=True)
    ap.add_argument("--product", type=int)
    ap.add_argument("--runs", type=int, default=2)
    ap.add_argument("--max-cost-usd", type=float, default=5.0)
    ap.add_argument("--concurrency", type=int, default=4, help="parallel agent runs, 1 to 8 (default 4); they share your rate limit")
    ap.add_argument("--model")
    ap.add_argument("--out")
    ap.add_argument("--only", help="comma list of eval groups to run: trig,qual,adv,cold (the result is not rated)")
    ap.add_argument("--static-only", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--keep-workspace", action="store_true",
                    help="keep the eval workspace and its transcript after a full run")
    args = ap.parse_args()

    plugin = Path(args.plugin).resolve()
    manifest = read_json(plugin / ".claude-plugin" / "plugin.json")
    if manifest is None:
        sys.exit(f"No .claude-plugin/plugin.json found in {plugin}")
    if args.product:
        c = PRODUCTS[str(args.product)]
    else:
        match = [v for v in PRODUCTS.values() if v["plugin"] == manifest.get("name")]
        if not match:
            sys.exit(f"plugin.json name '{manifest.get('name')}' is not one of: " + ", ".join(v["plugin"] for v in PRODUCTS.values()) + ". Use --product N.")
        c = match[0]

    notes = []
    claude = shutil.which("claude")
    have_claude = False
    if claude:
        code, out = run(["claude", "--version"])
        have_claude = code == 0 and ver(out) >= MIN_CLAUDE
    git_ok = False
    if shutil.which("git"):
        _, gout = run(["git", "--version"])
        git_ok = ver(gout) >= MIN_GIT
    if not have_claude:
        notes.append(install_help())
    elif not git_ok:
        notes.append("Git 2.31 or later is required for plugin evals ('git --version'). Evals will not run until it is installed.")

    outdir = Path(args.out) if args.out else Path.cwd() / "gauntlet-results" / datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    outdir.mkdir(parents=True, exist_ok=True)

    if args.smoke:
        if not (have_claude and git_ok):
            sys.exit(install_help())
        ws = build_workspace(plugin, c)
        cmd = eval_cmd(ws, "trig-1-natural", "none", 1, 1.0, outdir / "smoke.json", args.model)
        print("Smoke test:", " ".join(cmd))
        code, out = run(cmd, timeout=900)
        print(out[-1500:])
        # The workspace holds the eval transcript. It used to be deleted here,
        # which meant a smoke run could not answer "which tools did it use?"
        # without paying for a second run. Keep it and say where it is.
        if args.keep_workspace or True:
            print("", file=sys.stdout)
            print(f"Workspace kept for inspection: {ws}")
            print("The transcript there shows which tools each case actually used.")
        smoke_doc = read_json(outdir / "smoke.json") or {}
        _warn_timeout_scored(smoke_doc)
        sys.exit(code)

    check_structure(plugin, c, have_claude)
    check_context(plugin, manifest.get("name", c["plugin"]), have_claude)
    check_setup(plugin)
    secret = check_security(plugin, version_info(plugin))

    spent, complete = 0.0, True
    if args.static_only or not (have_claude and git_ok):
        complete = False
        for sec, lbl, mx in [("Eval suite", "trigger cases", 12), ("Eval suite", "quality cases", 18), ("Eval suite", "lift over the no-plugin baseline", 10), ("Adversarial pack", "adversarial prompts", 15), ("Cold install", "simulated cold install eval", 10)]:
            add(sec, lbl, 0, mx, "not run (" + ("--static-only" if args.static_only else "claude CLI or Git missing") + ")")
    else:
        docs, spent, partial = run_evals(plugin, c, args, outdir)
        if args.dry_run:
            sys.exit(0)
        score_evals(docs, args, partial)
        complete = len(docs) == 4 and not partial and not args.only
        if args.only:
            notes.append("Partial run (--only): per-group points are real, the total and tier are not.")

    total = sum(r[2] for r in results)
    sec_full = all(r[2] == r[3] for r in results if r[0] == "Security")
    tier = tier_for(total, secret, sec_full, complete)
    if not complete and not args.static_only:
        notes.append("Some eval groups did not run or finish, so no tier is awarded.")
    report(c, plugin, args, outdir, total, tier, spent, notes)
    sys.exit(0 if tier in ("Gold", "Silver", "Bronze") else 2 if tier.startswith("Not rated") else 1)


if __name__ == "__main__":
    main()
