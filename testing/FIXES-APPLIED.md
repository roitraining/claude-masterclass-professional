# Fixes Applied — RVC 2026-11 Test Findings

**Branch:** `lab-testing/rvc-2026-11`
**Source of findings:** the 2026-11-03 RVC test run (`testing/results/`, and the
"RVC 2026-11 Lab Test Results: Fix List" doc)

One entry per fix, in the order applied. Each says what changed, why, and which
finding it answers, so the retest can verify against this file rather than
re-reading the whole results doc.

**What is deliberately NOT changed:** planted defects. Every lab plants faults
students are meant to find. Where a tester finding touched something planted,
it was left alone and the reason is recorded.

---

## Batch 1 — `python` → `python3` (shared blocker 3)

**Finding:** the RVC image has no `python` command, only `python3`. Nearly every
lab's first command fails.

**Scope decision.** `python3` is used everywhere rather than installing
`python-is-python3` alone, because `python3` resolves correctly in *both*
contexts: outside a venv, and inside an activated one (venv creates `python`,
`python3` and `pythonX.Y`). The image package is still worth installing as a
belt-and-braces measure — see `IMAGE-REQUIREMENTS.md` item 2 — but the course
material no longer depends on it.

### 1.1 Markdown: 127 replacements across 58 files

Lab steps, demo steps, course READMEs, briefs and starter READMEs across all
five courses.

**Not changed — Windows lines (1).**
`course-1/demo-files/starter-server/README.md:25` keeps bare `python` because
the line is PowerShell (`$env:STARTER_DATA = "C:\path\to\folder"; python
test_server.py`) and Windows has no `python3`. Course 1's demo guide already
carries the cross-platform note: *"Use `python` on Windows and `python3` where
`python` is not defined."*

### 1.2 JSON configs: 7 files — the silent failures

These are the ones the tester saw fail without an error message, because a
hook or MCP server whose `command` does not exist simply does not run.

| File | Was | Now |
|---|---|---|
| `course-1/demo-files/autopsy-plugin/.mcp.json` | `"command": "python"` | `python3` |
| `course-1/demo-files/autopsy-plugin/server/manifest.json` | `"command": "python"` | `python3` |
| `course-1/demo-files/demo-snippets/.mcp.json` | `"command": "python"` | `python3` |
| `course-1/demo-files/starter-server/manifest.json` | `"command": "python"` | `python3` |
| `course-2/demo-files/lab3-plugin/facilitator/.../relnotes/hooks/hooks.json` | `"command": "python ..."` | `python3` |
| `course-2/demo-files/lab3-plugin/relnotes-starter/hooks/hooks.json` | `"command": "python C:/Users/student/..."` | `python3 C:/Users/student/...` |
| `course-4/demo-files/lab3-harden/vuln-app/.mcp.json` | `"command": "python"` | `python3` |

All course JSON re-validated after editing: 0 invalid files.

### Planted defects preserved

Checked before editing, and left in place:

- **Course 2 Lab 3 — the hardcoded hook path.** `relnotes-starter/hooks/hooks.json`
  still points at `C:/Users/student/plugins/relnotes/scripts/lint_notes.py`.
  Only the interpreter changed. Part 2 Step 3's hint is *"a fixed path in a hook
  breaks on every other machine. A plugin has a documented variable for its own
  folder"* — replacing that path **is the exercise**.
- **Course 2 Lab 4 — `lsp.variant-b-wrong-binary.json`** untouched. Its
  `"command": "python-lsp-server"` is wrong on purpose; the correct binary is
  `pylsp`.
- **Course 1 Lab 2 — the autopsy plugin's six defects.** Confirmed from
  `AUTOPSY-WORKSHEET.md` that the six areas are Trigger, Permissions, Setup,
  Context cost, Secrets and Versioning. The interpreter is not among them, so
  changing it erases nothing students are meant to find.

### Verification

```
# no bare `python` left in student-facing material except the one Windows line
grep -rnE '(^|[^a-zA-Z0-9_./-])python( |$)' --include='*.md' . | grep -v validation/
```

Returns exactly one hit: the PowerShell line above.
