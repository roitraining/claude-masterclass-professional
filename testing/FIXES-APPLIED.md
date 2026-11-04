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

---

## Batch 2 — virtual environments before every `pip install` (shared blocker 3)

**Finding:** PEP 668 makes the image's Python externally managed, so
`pip install` is refused outside a venv — including `pip install --user`.

Seven bare `pip install` calls now create and activate a venv first. The venv
names match the ones `provision-rvc.sh` pre-creates (`~/.venvs/mc-ci`,
`~/.venvs/mc-lsp`), so a provisioned image only needs the activate line and the
commands still work on an unprovisioned one.

| File | Change |
|---|---|
| `course-2/labs/lab-4-...language-server-plugin.md` Step 1 | venv commands added **before** pip, in the right order |
| same, Step 2 hint | activation changed from conditional to required |
| `course-2/labs/lab-1-wire-claude-into-ci-safely.md` Step 3 | venv commands added, plus a note to keep the shell active |
| same, troubleshooting row | now says to activate the venv first |
| `course-2/demo-files/lab1-ci/gate-checklist-github.md` | activate line added |
| `course-2/demo-files/lab1-ci/gate-checklist-gitlab.md` | activate line added |
| `course-2/demo-files/README.md` | activate line added |
| `course-2/demos.md` and `demos/demo-8-wire-in-a-language-server.md` | activate line added |

**Course 2 Lab 4 had its steps in the wrong order.** The venv was mentioned at
line 55 — *after* the pip install at line 38 — and Step 1's expected result said
the install completes "in a virtual environment **or your user environment**".
The user environment does not work on this image. Step 1 now states that a venv
is required and why.

Course 3 and `tallybook/README.md` already created a venv immediately before
their pip step and were left unchanged.

## Batch 4 — git identity (shared blocker 6)

**Finding:** no global git identity on the image; commits fail with
`Author identity unknown`.

Two places actually run `git commit`, and both now set an identity first:

- `course-4/demo-files/lab3-harden/lab3_brief.md` — the baseline copy block
  (the tester asked for this one specifically)
- `course-4/labs/lab-4-prompt-injection-detection.md` — its baseline block

The added lines are **guarded**, so a student working on their own machine does
not get their real identity overwritten:

```bash
git config --global user.name  >/dev/null 2>&1 || git config --global user.name  "RVC Student"
git config --global user.email >/dev/null 2>&1 || git config --global user.email "student@rvc.local"
```

Course 2's labs already name a set identity in their prerequisites and only run
`git branch`, `git diff` and `git log`, so they need nothing.

Verified: no `git commit` anywhere in the course material now lacks an identity
step or prerequisite.

---

## Batch 3 — leaked answer keys (shared blocker 4)

**Finding:** answer keys ship inside student folders.

Each case turned out to be different, so they were not treated alike. A blanket
move would have broken two labs.

### 3.1 Three clean moves into `facilitator/`

`facilitator/` is the convention in every other course; Course 4 used
`instructor/` for one folder. Standardised, with `git mv` so history survives.

| Was | Now | Why it is safe to move |
|---|---|---|
| `lab1-identity/live_path_scorecard.md` | `lab1-identity/facilitator/` | Its own header says "(instructor use)", and the lab already told students it was instructor-only while shipping it anyway |
| `lab5-audit/rubric.md` | `lab5-audit/facilitator/` | Titled "Rubric (100 points) **and Answer Key**", says "Instructor use. Hold back until the audit is submitted". Referenced only from facilitator notes, never a student step |
| `lab2-compliance/instructor/make_activity_export.py` | `lab2-compliance/facilitator/` | Its docstring says verbatim: "Do not give this file to students: it contains the planted anomalies" — and it listed every DECOY and PLANTED marker |

Four references updated; no stale paths remain.

### 3.2 Two that could NOT be moved — the lab requires them

**Course 2 Lab 2.** The tester's suggested fix was to move
`facilitator/answer_key.json` out of `facilitator/`. That would hand students
every planted bug: the key carries each bug's title, file, marker and keywords.

The real problem was a documentation gap, not a path. `demo-files/README.md`
already instructed facilitators correctly — *"give students the scorer and key
together only after they have a findings file, or run the scorer yourself"* —
but the **student-facing lab never said so**, so students and the tester hit a
wall with no instruction. Steps 4 and 6 now state that the key comes from the
facilitator, show the `--key` argument, and say to ask rather than go looking.
No answer file moved.

**Course 4 Lab 2.** Same shape. `check_lab2.py` names the planted actors and
approved UUIDs, its docstring says to hand it out after submission, yet Step 7
tells students to run it. Step 7 now says the facilitator runs it or hands it
over after submission. `demo-files/README.md` now names all three Course 4
checkers that hold answer logic.

### Residual design question for the course owner

Both labs ask students to **self-score**, and scoring inherently needs the real
answers. So there are only two honest end states, and this is a teaching
decision rather than a bug:

1. **Facilitator-scored rounds** — preserves the exercise, costs facilitator
   time during the iteration loop (Course 2 Lab 2 allows up to three rounds).
2. **Hand the key over at scoring time** — self-service, but a student who
   reads it has the answers.

The fixes above implement option 1, because it matches what the facilitator
README already said. Switching to option 2 is a one-line change in each lab.

**Course 5 is not done.** Its Facilitator Notes are printed inside the
student-facing lab files, which is a larger restructure than a file move, and
those findings came from a helper agent with only two claims spot-checked. It is
handled in a later batch after verification.
