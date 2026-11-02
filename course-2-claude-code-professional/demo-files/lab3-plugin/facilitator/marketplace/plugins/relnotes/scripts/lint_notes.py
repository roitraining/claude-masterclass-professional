#!/usr/bin/env python3
"""PostToolUse hook: lint RELEASE_NOTES.md after Claude writes or edits it.

Reads the hook event JSON on standard input. Exits 0 when the file is fine or is not
RELEASE_NOTES.md. Exits 2 with a message on standard error when the notes break a rule,
so the message goes back to Claude.
"""
import json
import re
import sys
from pathlib import Path

SECTIONS = ["Breaking changes", "Features", "Fixes", "Other changes"]
BULLET = re.compile(r"^- .+ \([0-9a-f]{7,}\)$")


def problems(text):
    out = []
    lines = text.splitlines()
    if not lines or not lines[0].startswith("# Release notes"):
        out.append('The first line must start with "# Release notes".')
    seen, current, counts = [], None, {}
    for n, ln in enumerate(lines, 1):
        if re.search(r"\b(TODO|TBD|FIXME)\b", ln):
            out.append(f"Line {n}: placeholder text ({ln.strip()[:40]}).")
        if ln.startswith("## "):
            current = ln[3:].strip()
            if current not in SECTIONS:
                out.append(f'Line {n}: unknown section "{current}". Use only {", ".join(SECTIONS)}.')
            seen.append(current)
            counts[current] = 0
        elif ln.startswith("- "):
            if current is None:
                out.append(f"Line {n}: a bullet before any section.")
                continue
            counts[current] += 1
            if not BULLET.match(ln):
                out.append(f"Line {n}: a bullet must end with the short commit hash in parentheses, for example (a1b2c3d).")
    order = [s for s in SECTIONS if s in seen]
    if [s for s in seen if s in SECTIONS] != order:
        out.append("Sections are out of order. Use: " + ", ".join(SECTIONS) + ".")
    for s, c in counts.items():
        if c == 0:
            out.append(f'Section "{s}" is empty. Remove it.')
    return out


def main():
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    path = (event.get("tool_input") or {}).get("file_path", "")
    if Path(path).name != "RELEASE_NOTES.md":
        return 0
    file = Path(path)
    if not file.exists():
        return 0
    found = problems(file.read_text(encoding="utf-8"))
    if found:
        print("RELNOTES-LINT: RELEASE_NOTES.md breaks the format:\n- " + "\n- ".join(found), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
