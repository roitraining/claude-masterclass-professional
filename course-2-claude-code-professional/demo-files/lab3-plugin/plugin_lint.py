#!/usr/bin/env python3
"""Cheap local checks for a Claude Code plugin, to run before you spend credits on an eval.

Usage:
    python3 plugin_lint.py PLUGIN_DIR [--marketplace MARKETPLACE_DIR]

This does NOT replace `claude plugin validate`, and it does not test behavior (that is
what `claude plugin eval` is for). It checks the traps this lab plants: a hook that does
not use the plugin path variable, a subagent with more tools than it needs, fields that a
plugin agent ignores, a root CLAUDE.md that never loads, a manifest name that does not
match the marketplace entry, and descriptions that cost context on every turn.

Exit code 0 when there are no FAIL lines, 1 otherwise.
"""
import json
import re
import sys
from pathlib import Path

MAX_DESCRIPTION = 300          # lab rule of thumb, not a product limit
IGNORED_AGENT_FIELDS = ("permissionMode", "hooks", "mcpServers", "initialPrompt")   # per the plugin components docs
WRITE_TOOLS = {"Edit", "Write", "Bash", "NotebookEdit"}
results = []


def out(level, msg):
    results.append(level)
    print(f"[{level:<4}] {msg}")


def frontmatter(path):
    text = Path(path).read_text(encoding="utf-8")
    m = re.match(r"---\s*\n(.*?)\n---\s*\n", text, re.S)
    fields = {}
    if m:
        for ln in m.group(1).splitlines():
            if ":" in ln and not ln.startswith((" ", "\t", "-")):
                k, v = ln.split(":", 1)
                fields[k.strip()] = v.strip()
    return fields, bool(m)


def main(argv):
    mk = None
    rest = list(argv)
    if "--marketplace" in rest:
        i = rest.index("--marketplace")
        mk = Path(rest[i + 1])
        del rest[i:i + 2]
    args = [a for a in rest if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__)
        return 2
    root = Path(args[0])
    manifest_path = root / ".claude-plugin" / "plugin.json"
    name = None
    if not manifest_path.exists():
        out("FAIL", "No .claude-plugin/plugin.json")
    else:
        try:
            name = json.loads(manifest_path.read_text(encoding="utf-8")).get("name")
        except json.JSONDecodeError as exc:
            out("FAIL", f"plugin.json is not valid JSON: {exc}")
        if name:
            out("ok", f"Manifest name is '{name}'")
        elif manifest_path.exists():
            out("FAIL", "plugin.json has no name")

    # hooks
    hooks_file = root / "hooks" / "hooks.json"
    if hooks_file.exists():
        text = hooks_file.read_text(encoding="utf-8")
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            data = {}
            out("FAIL", f"hooks/hooks.json is not valid JSON: {exc}")
        if re.search(r"[A-Za-z]:[\\/]|/(home|Users)/", text):
            out("FAIL", "hooks/hooks.json contains a fixed absolute path. Use ${CLAUDE_PLUGIN_ROOT}.")
        commands = [h.get("command", "") for ev in (data.get("hooks") or {}).values()
                    for grp in ev for h in grp.get("hooks", [])]
        for c in commands:
            if "scripts/" in c and "${CLAUDE_PLUGIN_ROOT}" not in c:
                out("FAIL", f"Hook command does not use ${{CLAUDE_PLUGIN_ROOT}}: {c}")
            for m in re.finditer(r"\$\{CLAUDE_PLUGIN_ROOT\}/([\w./-]+)", c):
                if not (root / m.group(1)).exists():
                    out("FAIL", f"Hook points at {m.group(1)}, which does not exist in the plugin")
        if commands and "FAIL" not in results[-3:]:
            out("ok", "Hook commands use the plugin path variable and point at real files")
    else:
        out("WARN", "No hooks/hooks.json")

    # agents
    for f in sorted((root / "agents").glob("*.md")) if (root / "agents").exists() else []:
        fm, has = frontmatter(f)
        if not has:
            out("FAIL", f"{f.name}: no frontmatter, so the agent loads with every field ignored")
            continue
        for k in IGNORED_AGENT_FIELDS:
            if k in fm:
                out("FAIL", f"{f.name}: '{k}' is ignored in a plugin agent. Remove it, and do not rely on it.")
        tools = {t.strip().split("(")[0] for t in fm.get("tools", "").split(",") if t.strip()}
        if re.search(r"audit|review|check", fm.get("name", "") + fm.get("description", ""), re.I) and tools & WRITE_TOOLS:
            out("FAIL", f"{f.name}: a checking agent has write-capable tools: {', '.join(sorted(tools & WRITE_TOOLS))}")
        if not fm.get("tools") and not fm.get("disallowedTools"):
            out("WARN", f"{f.name}: no tools or disallowedTools, so the agent inherits everything")
        d = fm.get("description", "")
        if len(d) > MAX_DESCRIPTION:
            out("WARN", f"{f.name}: description is {len(d)} characters. It is in the context window on every turn.")

    # commands
    for f in sorted((root / "commands").glob("*.md")) if (root / "commands").exists() else []:
        fm, has = frontmatter(f)
        d = fm.get("description", "")
        if not d:
            out("FAIL", f"{f.name}: no description, so Claude cannot tell when it applies")
        elif len(d) < 40:
            out("WARN", f"{f.name}: description is only {len(d)} characters. A vague description can stop the command from being chosen.")
        elif len(d) > MAX_DESCRIPTION:
            out("WARN", f"{f.name}: description is {len(d)} characters. It is in the context window on every turn.")
        if "TODO" in f.read_text(encoding="utf-8"):
            out("FAIL", f"{f.name}: still contains TODO")

    # root CLAUDE.md
    if (root / "CLAUDE.md").exists():
        out("FAIL", "A CLAUDE.md at the plugin root is not loaded as project context. Move its rules into a command or skill.")

    # evals
    ev = root / "evals"
    if ev.exists():
        for case in sorted(p for p in ev.iterdir() if p.is_dir() and p.name != "results"):
            has_case = (case / "prompt.md").exists() or (case / "case.yaml").exists()
            has_grader = any((case / "graders").glob("*.md")) if (case / "graders").exists() else False
            if has_case and not has_grader:
                out("FAIL", f"evals/{case.name}: no grader, so the case fails to load")
        out("ok", "Every eval case has at least one grader") if "FAIL" not in results[-1:] else None

    # marketplace
    if mk:
        mf = mk / ".claude-plugin" / "marketplace.json"
        if not mf.exists():
            out("FAIL", f"No marketplace.json at {mf}")
        else:
            entries = json.loads(mf.read_text(encoding="utf-8")).get("plugins", [])
            names = [e.get("name") for e in entries]
            if name and name not in names:
                out("FAIL", f"No marketplace entry named '{name}' (entries: {names}). Entry name and manifest name must match.")
            for e in entries:
                src = e.get("source")
                if isinstance(src, str):
                    if ".." in src:
                        out("FAIL", f"Entry '{e.get('name')}': source contains '..'")
                    elif not (mk / src).exists():
                        out("FAIL", f"Entry '{e.get('name')}': source path {src} does not exist under the marketplace")
            if name in names:
                out("ok", "Marketplace entry name matches the manifest name")

    fails = results.count("FAIL")
    print(f"\n{fails} FAIL, {results.count('WARN')} WARN. Now run: claude plugin validate {root}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
