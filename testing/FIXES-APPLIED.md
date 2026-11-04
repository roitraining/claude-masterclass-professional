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

---

## Batch 5 — defects that penalized correct student answers

These are the two worst findings in the report: in both cases a student who
reasoned correctly lost points.

### 5.1 Course 2 Lab 2 — the `pr-10-prorated-fine` bait was genuinely wrong

The branch is a **bait**: it should look like a float-truncation bug while
actually being correct under policy LIB-7 ("truncate to whole cents, never round
up"). It was not correct. `100 * 0.29` is `28.999999999999996` in float, so
`int(...)` returned **28** when the exact answer is 29. A student flagging it
was right, and the answer key marked them wrong.

Fixed by guarding the float representation error before truncating:

```python
-    return int(days * rate_cents_per_day)
+    return int(round(days * rate_cents_per_day, 6))
```

This keeps the bait valid rather than removing it: the line still *looks* like
truncation, and still truncates — verified `28.7 → 28`, `3 × 9.5 → 28`,
`0.5 → 0` — but `100 × 0.29` now gives 29. Policy LIB-7 is preserved; nothing
rounds up.

Applied in three places plus the key: `build_fixture.py`,
`diffs/pr-10-prorated-fine.diff`, and `facilitator/answer_key.json` (both the
`marker`, which the scorer matches against, and `why_fine`, so a facilitator can
defend the bait).

### 5.2 Course 4 Lab 5 — the `payments-gateway` decoy contradicted itself

`payments-gateway` is the clean repository and the rubric awards 10 points for
*not* reporting it. But its credential `cred-102` was a **setup token owned by a
person** (`a.mensah@example.org`) used for CI — which Course 2 Lab 5 teaches
against. A careful student lost 10 points for spotting it.

Fixed by making the repository genuinely clean rather than penalizing the flag.
`cred-102` is now owned by `payments-team@example.org`, matching the
`platform-team@example.org` convention already used by `cred-103`.

The clean/defective distinction is now coherent:

| Credential | Owner | Expires | Rotated | Verdict |
|---|---|---|---|---|
| `cred-101` | a person | **none** | **never** | defective |
| `cred-102` | a team | 2027-02-20 | 2026-08-20 | clean |
| `cred-103` | a team | 2026-11-02 | 2026-05-02 | clean |

A note was added to the rubric so a facilitator can defend the 10 points, and it
explicitly says **not** to deduct from a student who raises the
person-tied-token question and then concludes the repository is clean. That
reasoning is correct even though the conclusion is "clean".

## Batch 7 — the false-safety prediction and two checker bugs

### 7.1 Course 4 Lab 3 told students an attack was blocked when it was not

The most serious finding in the report. `check_settings.py` printed attack 3 as
unconditionally `blocked`, while attacks 1 and 2 correctly said "blocked **if
the OS sandbox starts**". With the sandbox down the tester watched the secrets
file get read anyway (`read 83 bytes from config/secrets.env`).

Attack 3 is now conditional like the others, with two lines explaining why,
because the reason is a real teaching point:

> deny rules gate Claude's Read tool. A shell command run through Bash is
> stopped by the OS sandbox, so with the sandbox down this file can still be read.

A lab that reports a control as working when it is not is worse than a lab that
fails, which is why this was prioritised over the wording backlog.

### 7.2 Course 4 Lab 3 — `.mcp.json` pointed at a missing file

The project registered a `ticket-bridge` MCP server at
`tools/ticket_bridge.py`, which did not exist. Added as an explicit stub that
documents itself as not part of the exercise and exits immediately, so the MCP
configuration resolves instead of failing in a way that masked the real
exercise.

### 7.3 Course 4 Lab 1 — `fix_d4` scored a correct fix 0/10

The check required the strings `verif` **and** `domain` in the same CSV cell, so
a correctly reworded row failed. A verification row is now identified by naming
a domain and not being the enforce step:

```python
def is_verify(r):
    a = low(r["action"])
    if "enforce" in a:
        return False
    return "verif" in a or ".example.net" in a or ".example.org" in a
```

All three scripts compile.

---

## Batch 6 — fixes to the provisioning script itself (2026-11-04 test run)

The provisioning test found three bugs in `provision-rvc.sh`. One of them was
worse than a bug: the script was **manufacturing false evidence**.

### 6.1 The sandbox probe gave a false pass — the serious one

The probe ran `claude -p` with **no sandbox setting**, so Bash was never
sandboxed. It printed `a sandboxed Bash call succeeded` on every run, including
with the restriction fully active. The final `--check` therefore showed the
sandbox as OK when it was broken.

This is the opposite of what the script exists for. A verification tool that
reports success regardless of state is worse than no tool, because its output
gets handed to the team as proof.

Fixed by forcing the sandbox on in the probe, using the settings the tester
confirmed reproduce the real error:

```
--settings '{"sandbox":{"enabled":true,"failIfUnavailable":true}}'
```

The probe now also prints the matching lines from the failure output
(`seccomp`, `setgroups`, `userns`, `CAP_SYS_ADMIN`, `denied`) so the evidence
travels with the result.

### 6.2 `npm install -g` ran without sudo

Failed with `EACCES: permission denied, mkdir '/usr/local/lib/node_modules'`.
The package itself is fine — the tester installed it to a temporary prefix
successfully (`added 55 packages`). Changed to `$SUDO npm install -g`.

### 6.3 The `--allow-sandbox-fix` hint printed when the sandbox was not the problem

It appeared even when only the API key and `mcpb` remained outstanding. Removed,
along with the flag's behaviour — see below.

### 6.4 The sysctl "fix" was disproven, so it has been retired

**This corrects a recommendation I made.** `IMAGE-REQUIREMENTS.md` offered
relaxing `kernel.apparmor_restrict_unprivileged_userns` as the simple option.
The tester applied it and **the error did not change**.

The `bwrap-userns-restrict` AppArmor profile stays loaded and enforcing; the
sysctl does not turn it off. It moves everything `bwrap` launches into
`unpriv_bwrap`, which carries `audit deny capability`. The kernel kept denying
after the sysctl was relaxed:

```
apparmor="DENIED" operation="capable" class="cap" profile="unpriv_bwrap"
  comm="3" capability=21 capname="sys_admin"
```

Changes made:

- `--allow-sandbox-fix` still parses but does nothing, and prints why. Leaving
  the behaviour in would relax a security setting for no benefit.
- Section 8 is now **diagnostic only**: it reports the sysctl as informational,
  detects `bwrap-userns-restrict`, checks `aa-status` for `unpriv_bwrap`, and
  flags a leftover `/etc/sysctl.d/99-claude-sandbox.conf` with the revert
  commands.
- `IMAGE-REQUIREMENTS.md` item 1 is rewritten: AppArmor is the only path, the
  sysctl is documented as disproven with the kernel evidence, and the summary
  table marks item 1 as not scriptable.
- The expected-FAIL note now names **three** items that legitimately fail after
  a good run, not two: the sandbox joins the API key and the Desktop account.

### Action for the VM

The sysctl change from the test run is still applied and should be reverted —
it relaxes security and fixes nothing:

```bash
sudo rm /etc/sysctl.d/99-claude-sandbox.conf
sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=1   # or reboot
```
