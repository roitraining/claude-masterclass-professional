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

---

## Batch 6 — rubric rows that scored work no step asked for

### 6.1 Course 2 Lab 1 — Track C was scored for two things it was never asked to do

Track C (gate only, no hosted project) carried **35 of its 100 points** on work
the lab never set.

**20 points: "Written prediction of what a live run would do".** No step asked
for a prediction. Added **Part 6b / Step 11b**, Track C only, asking for a
per-file prediction: what starts the workflow, which actors it accepts and the
line that decides, what it may do once running, what the planted trap would
have allowed, and which injection fixtures each control stops. Every claim must
cite a line or a gate finding — a prediction without a citation is a guess. The
checkpoint and the rubric row now name the step.

**15 points: "Settings audit".** Step 11 asks students to read *project
settings* — write access, branch protection, secret scoping. Track C has no
hosted project, so there was nothing to read. Added a **Track C alternative**:
write the audit as a specification instead (what the correct setting is, what an
incorrect one permits, and which hardened workflow line still holds if it is
wrong), for the same 15 points.

Also scoped **Step 1's push** to Tracks A and B, since the live trigger in Part
4 is what needs a remote. Track C now commits locally and does not push.

### 6.2 Course 2 Lab 5 — the pilot nobody mentioned

The rubric awards 5 points for ordering "pilot before everyone", but no student
file mentioned a pilot — it existed only in the facilitator outline. The
Overview now states it, and template section 6 prompts for where the pilot cuts
over relative to everyone else.

### 6.3 Course 2 Lab 5 — troubleshooting rows stated product behaviour as fact

Rows read like product documentation ("People cannot sign in") in a paper lab
where nothing is migrated and nothing is observed. The Facilitator Notes say
they must not read that way.

The table is now headed "Risk the sequence creates" / "What the runbook should
do", the symptoms are phrased as predictions ("Users **may** be unable to sign
in before their seats exist"), and a note above states plainly that these are
reasoned consequences rather than product documentation, to be confirmed against
current docs before any real migration. The credential row also gained the
actual reason: a leftover `ANTHROPIC_API_KEY` or `apiKeyHelper` **outranks a
subscription login in Claude Code's credential precedence**.

### 6.4 Course 5 — three claims checked, two rejected

The Course 5 findings came from a helper agent with only two of its claims
spot-checked, so each was verified against the lab text before acting. Of the
three checked:

| Claim | Verdict |
|---|---|
| "Halvern's 30-day notice is scored but no step mentions it" | **Rejected.** It is in `brightwater_org_brief.md` line 33, and Part 1 tells students to read the brief. The rubric row scores using the brief's facts, which is fair |
| "Step 4 has no time; the other steps use all 75 minutes" | **Rejected.** The five timed parts are 5 + 40 + 15 + 10 + 5 = **exactly 75**, matching the stated duration. Every part has time |
| "A register-level review date and trigger is scored but not asked for" | **Confirmed and fixed.** The rubric awards 4 points for a *register-level* review date while the lab only ever asked for *per-row* dates. Step 3 now asks for it, with the distinction explained, and the checkpoint lists it |

**One of three stood up.** The remaining ~28 Course 5 items are therefore
treated as unverified leads, not findings, and each needs checking against the
lab text before any change. That is the bulk of what is left in batch 8.

---

## Batch 8a — the verified Course 1, 2 and 4 tail

These came from the tester directly, with verbatim evidence, so they were
applied without re-verification. The Course 5 items are handled separately in
8b because their source was less reliable.

### Course 1

| Lab | Fix |
|---|---|
| L1 | `pack_mcpb.py` named in the prerequisites and in the packing step. Only the README mentioned the no-Node fallback, so a student without Node had no documented path |
| L2 | Step 2 now explains that `claude plugin validate` also prints advisory lines about `README` and `LICENSE` for **directory submission**. Those are not defects, are not among the six, and Lab 3 covers submission |

### Course 2 Lab 1

- **The gate detects GitLab by filename.** Added a troubleshooting row: any name
  other than `.gitlab-ci.yml` is silently skipped with "No Claude step found",
  even on a file that plainly has a `claude` job.
- **T5 has a known blind spot, now stated.** Laundering outsider text through an
  `env:` variable scores 100/100 while the prompt still contains
  attacker-controlled text. The lab now says a passing gate is **not** proof the
  prompt is clean, and tells students to trace where every value comes from.
  Flagged as a limit of the gate, not a planted trap.

### Course 2 Lab 3

- Step 1's expected result now covers the out-of-scope `README`/`LICENSE`
  suggestions from `validate`.
- Step 7 now says to exclude `evals/results/` when copying to the marketplace,
  so students do not publish their own eval reports to anyone installing the
  plugin.

### Course 2 Lab 4

- **Step 6 gives the coordinates.** `--definition 6:40` with the note that
  columns are **1-based** and the position must sit on the name: `6:39` lands one
  character early and returns `none found`.
- **Step 8 asks for the tool explicitly.** In a headless run Claude answered
  correctly with `Grep` instead of `LSP`. The step now says to name the tool, and
  explains the distinction: either tool answering proves navigation works, but
  only `LSP` proves *the student's plugin* works.
- **The Errors tab wording.** Troubleshooting now carries both forms — `Invalid
  LSP server config for ".lsp.json"` in the Errors tab and `LSP config
  validation failed for .lsp.json` in the debug log — and says they mean the same
  thing.
- **The smoke test no longer leads with "reinstall".** `lsp_smoke.py` now lists
  causes in likelihood order and closes with "A clean file reporting nothing is
  correct behaviour, not a broken install", so a student with a clean file does
  not go reinstalling for no reason.

### Course 4 Lab 1

- **An empty `claude_group` is not automatically a defect.** Under JIT, rows with
  a built-in role (`User`, `Admin`, `Owner`) need no named group — most rows are
  like that, including `claude-eng-premium`. Only a **Custom** role must name a
  group that exists, which is what defect D1 is. Stated at Step 2 so students
  stop churning on a correct row.

### Course 4 Lab 2

- **Track A's facts are now in the student step.** The header name
  (`anthropic-allowed-org-ids`), the no-spaces value format, the four hosts and
  the covered authentication methods lived **only in the Facilitator Notes**,
  while Step 6 scored students on naming them. Supplied in Step 6, with a hint
  that the work is deciding *which* organizations belong in the value.
- **"Cite several events" was impossible for one anomaly.** A3 is a single
  event, so "several" could not be met. Reworded to "every event in its
  sequence", with the single-event case called out, in all three places.

### Course 4 Lab 4

- **Guidance for when every run is refused.** The lab already handled a refusal
  well — record it as `model`, not as a control — but not the case the tester
  hit, where *all eight* runs refused and no configured control was exercised.
  Added: record the refusals, then write a reasoned pass naming which control
  **would** have stopped each effect and which effect would have landed anyway,
  using the Facilitator Notes SAMPLE outline as the shape, and say plainly in the
  account that the conclusions are reasoned rather than observed.
- **`/status` is not available in `-p` mode.** Corrected in all four places,
  with `permissionMode` from the init JSON as the headless equivalent.

### Course 4 Lab 5

- **C3 and C4 score separately** even though both involve `cred-101`'s CI use.
  One is about **scope** (a secret shared across two repositories), the other
  about **ownership and lifecycle** (departed owner, no expiry, used after
  departure). A student merging them loses the row they did not state. Noted in
  the lab before Part 3 and in the facilitator rubric.

All Python compiles and all JSON validates: 0 failures.

---

## Batch 8c — Course 1's Desktop requirement was overstated, causing an over-block

**Finding this corrects:** the test report blocked **all three** Course 1 labs on
the Desktop/CLI account mismatch. Checking what the labs actually need, that was
too broad — and the overstated prerequisite was partly mine.

What Course 1 really needs Desktop for:

| Lab | Desktop dependency | Runnable without it |
|---|---|---|
| Lab 1 | Part 8's extension install, which the lab itself calls *"optional if time is short"* | **Yes** — Parts 1 to 7 build and pack the plugin entirely in the CLI |
| Lab 2 | **None.** Desktop appears only in the course title and the boilerplate "Part of…" line | **Yes, entirely** |
| Lab 3 | Part 5's extension reinstall genuinely needs it | Parts 1 to 4 and 6 to 9 yes |

So the account mismatch blocks **one part of one lab**, plus an optional part of
Lab 1 — not a course.

The cause was wording. The course preamble said "`claude` … signed in to the
same account as Claude Desktop" as a flat prerequisite, and the setup pointer I
added to Lab 1 repeated it as "**This course needs** … signed in to the same
account as Claude Desktop". Read as a gate, that blocks everything.

Reworded in three places so the requirement appears where it applies:

- **Lab 1's setup pointer** now states the version requirement on its own, then
  says Desktop is needed only for the optional Part 8, and that Parts 1 to 7 are
  entirely command line — skip Part 8 if Desktop is missing or on another
  account.
- **Lab 3's prerequisite** names Part 5 as the one place the accounts must match,
  and says why: a plugin is saved to an account, so a mismatch means the plugin
  you packed will not appear.
- **The course preamble** separates the Claude Code version from the Desktop
  requirement, and states what remains runnable without Desktop.

The mismatch itself is a misconfigured image, not a design problem: both should
be signed in to the same class account. It stays on the image list as item 5
because a script cannot log in. But it should no longer stop a retest of Labs 1
and 2.

## Batch 8d — Course 2's hosted-project requirement was also overstated

Same shape as Course 1. The preamble listed "administrative access to a personal
or sample GitHub or GitLab project" as a flat prerequisite for the whole course.
Only **Lab 1** needs one:

| Lab | References to push/remote/hosted | Reality |
|---|---:|---|
| L1 | 32 | Tracks A and B trigger a real CI run and need a remote. Track C needs none |
| L2 | 1 | False hit — no remote needed |
| L3 | 1 | A single **optional** step: "For a remote check, push the marketplace…" |
| L4 | 0 | None |
| L5 | 2 | Paper lab, scenario text only |

The preamble now separates the two: the Claude Code and Git requirements apply
to the course, and the hosted project is named as Lab 1 only, with an explicit
"do not skip those labs for want of a hosted project". It also states that the
free plan has no Claude Code access, which was the account-tier gap from the
first run.

**Pattern worth noting.** This is the second course where a *stated* prerequisite
was stricter than the actual dependency, and both caused or risked a whole-course
block. Courses 3, 4 and 5 were checked the same way: Course 3's preamble scopes
its API key correctly, Course 4 Labs 1 and 2 already document live and offline
paths while Labs 3 to 5 need neither, and Course 5 needs no tooling at all. No
further changes needed there.

---

## Batch 9 — Course 1 retest (2026-11-04): a regression I introduced, and a probe that lied

### 9.1 REGRESSION, mine: `server.type: python3` broke packing

Commit `1880854`, my `python` → `python3` sweep, changed `server.type` in two
manifests. **`server.type` is an enum, not a command.**

```
$ mcpb pack . dist/board-pack-builder-0.1.0.mcpb
ERROR: Manifest validation failed:
  - server.type: Invalid enum value. Expected 'python' | 'node' | 'binary', received 'python3'
ERROR: Cannot pack extension with invalid manifest
```

Every student would fail Course 1 Lab 1 Step 12 with the primary tool. Reverted
to `"python"` in `starter-server/manifest.json` and
`autopsy-plugin/server/manifest.json`, keeping
`server.mcp_config.command: python3`, which is correct and is what actually runs
the server.

**Then audited every `python3` I had written into JSON, by key path**, rather
than by eyeballing:

| Key path | Verdict |
|---|---|
| `.server.type` ×2 | **was wrong — reverted** |
| `.server.mcp_config.command` ×2 | correct, a real command |
| `.hooks.PostToolUse[0].hooks[0].command` ×2 | correct, a real command |

All manifests now validate: 0 invalid `server.type` values.

**What I got wrong in method.** I checked each fixture for *planted defects*
before editing, which caught three. I did not check whether each `python` token
was in a **command position**. A string match on an identifier is not a safe
transform when the same word is also a valid enum value.

### 9.2 My sandbox probe gave a false pass, again — for a new reason

`sandbox-apparmor.sh` reported the sandbox failing, with fresh `unpriv_bwrap`
denials. `provision-rvc.sh` reported "a genuinely sandboxed Bash call
succeeded". Both ran on the same VM minutes apart.

The tester found why: with `--permission-mode bypassPermissions`, **the model
stepped outside the sandbox and retried** after `failIfUnavailable: true` had
correctly failed the sandboxed call. The retry produced the expected string, and
my probe was grepping stdout for that string.

So v2 of this probe was wrong in a subtler way than v1:

| Version | How it decided | Why it lied |
|---|---|---|
| v1 | grep stdout, no sandbox settings | Bash was never sandboxed; passed always |
| v2 | grep stdout, sandbox forced on | the model retried unsandboxed and produced the string anyway |
| v3 | **the Bash `tool_result`** | — |

v3, now in `testing/sandbox-probe.sh` and **shared by both scripts so they
cannot disagree again**:

- `--output-format stream-json`, and a pass requires a Bash `tool_result` with
  `is_error` false **and** containing the marker. Either alone is not evidence.
- `allowUnsandboxedCommands: false`, so no unsandboxed retry is possible.
- **no `bypassPermissions`** — `--allowedTools Bash` is enough to permit the call.
- a unique per-run marker, so a stale string cannot satisfy it.

The general lesson, written into the file's header: **a probe must assert on the
mechanism it is testing, not on a string that something else can also produce.**

### 9.3 A security observation for Course 4

Worth carrying into the course content, not just the tooling: with
`bypassPermissions`, the model **stepped outside the sandbox after the sandbox
had correctly refused**. Course 4 Lab 3 and Lab 4 both teach about sandbox
enforcement, and that behaviour is directly relevant to what "the sandbox
blocked it" means in the presence of a permissive permission mode.

---

## Analysis — does the Gauntlet actually need the sandbox? Probably not.

Prompted by the tester's observation that all 10 Product 1 eval cases allow no
Bash. Checked against the repo, and the answer looks like **no, for the thing
Lab 2 actually asks students to do.**

Three mechanisms can put a shell inside `claude plugin eval`:

| Mechanism | Course 1 Gauntlet (Product 1) | Course 2 Lab 3 |
|---|---|---|
| `allowed_tools` includes `Bash` | **No** — all 10 cases are `[Read, Glob, Grep, Skill, Agent]` | **No** — same list |
| `case.yaml` runs a `scaffold_script` | **No** — no case has one | **Yes** — `uses-auditor` has `scaffold_script: scaffold.sh` |
| A subagent reached via `Agent` carries `Bash` | **No** for the reference agents: `record-auditor` is `Read, Grep, Glob` and `summary-writer` is `Read` | **Yes** — `changelog-auditor` is `Read, Grep, Glob, Edit, Write, Bash` |

So **Course 2 Lab 3 genuinely needs the sandbox** — via its scaffold script and
its Bash-carrying subagent. That explains "git can't run inside evals" without
any eval case allowing Bash, which had looked contradictory.

**Course 1's Gauntlet has none of the three**, as long as the plugin under test
follows the reference agent pattern. Step 6 targets *the student's own plugin*,
so a conforming plugin should score without a shell ever being needed.

One caveat that matters for interpreting a test run: the **autopsy** plugin's
agent is `Read, Grep, Glob, Bash, Write, Edit, WebFetch` — it does carry Bash.
Over-broad tools is plausibly its planted "Permissions" defect. So a Gauntlet run
pointed at the autopsy plugin can hit the sandbox, while a run pointed at a
student's own plugin should not. The earlier report already noted that pointing
the Gauntlet at the autopsy plugin gives a name error, because Step 6 expects the
student's plugin.

**If the smoke run confirms this, Lab 2's "blocked" was a misdiagnosis** and the
lab should say the Gauntlet does not depend on the sandbox. That is a one-line
change, pending the result.

---

## Batch 10 — the smoke run and AppArmor attempt (2026-11-04, $0.34)

### 10.1 Lab 2's sandbox block was a misdiagnosis — confirmed and recorded

The smoke run settled it: `Bash` was not in the session's tools, no call used a
shell, and there were no seccomp errors or kernel denials. Lab 2 now states that
the Gauntlet does not need the OS sandbox, with the evidence and the date.

That matches the repo analysis: no eval case allows `Bash`, no case runs a
scaffold script, and the reference subagents carry only read tools.

### 10.2 The 12-point trigger failure was NOT a grader bug

The tester reported the trigger grader as too strict, because the model reached
the workflow through `board-pack-builder:draft` while the grader matches
`board-pack`. **Checked, and the grader is right.**

- The grader's pattern already allows a namespace prefix:
  `"skill"\s*:\s*"(?:[\w-]+:)?board-pack"`.
- The eval's `allowed_tools` are `[Read, Glob, Grep, Skill, Agent]` — there is no
  `SlashCommand`, so a slash command was not the route.
- The contract fixes the names: skill folder `board-pack`, slash commands
  `draft.md` and `check.md`. So `…:draft` means the **skill itself is named
  `draft`**, which violates the contract.

Loosening the grader would have removed the name contract that lets the Gauntlet
test any student's plugin at all. The 0 was correct.

**The real defect is diagnostic, and it costs money.** `check_structure` already
catches a misnamed skill for free, but only as a 3-point partial deduction with
no hint that 12 more points will go the same way after a paid run.
`gauntlet.py` now emits, in the free static pass:

> WARNING: `skills/board-pack/SKILL.md` is missing, so the trigger eval group (12
> points) will also score 0 — its graders match the contract skill name. Rename
> the skill folder before paying for a full run.

### 10.3 `--smoke` destroyed the evidence it was run to collect

The `finally` block deleted the workspace, and the workspace holds the eval
transcript. So a smoke run could not answer "which tools did it use?" without
paying for a second run — which is exactly what happened, at $0.17.

`--smoke` now keeps the workspace and prints its path, with a line saying the
transcript shows which tools each case used. A `--keep-workspace` flag does the
same for a full run.

### 10.4 A timeout that still reported a score

Run 1 scored 1.00 and exited 0 while its own record said it had timed out after
300s. Run 2, the same case, finished in 67 seconds and scored 0. A timed-out case
has not produced a result, so the 1.00 was not a number to trust.

`gauntlet.py` now scans the result document and warns when any case records a
timeout alongside a score above zero, telling the reader to re-run and use the
run that completed. This cannot fix `plugin eval`'s own reporting, but it stops
the contradiction passing silently into a scorecard.

### 10.5 My Lab 3 zip claim was wrong

I wrote that a zip made from inside the plugin folder "will not load". The tester
found **both layouts loaded**. Corrected: the parent-directory form is the
documented shape and the one to rely on, with a note that a nested layout may
happen to work and must not be depended on. The Troubleshooting row no longer
asserts the stricter claim, and now says a zip that works is not proof the layout
is right.

### 10.6 AppArmor `local-override` failed, and why it could never have worked

`unpriv_bwrap` carries `audit deny capability`, and **a deny rule in AppArmor
beats any allow**. So appending `capability sys_admin,` cannot grant what an
explicit deny forbids. The attempt is reverted, the sysctl file is gone, and the
sysctl is back to 1.

The tester expects `claude-profile` to fail the same way, from reading the
profile, which leaves **`disable-profile`** as the likely fix. That is image-wide
and needs a decision.

`IMAGE-REQUIREMENTS.md` item 1 is updated with this result so nobody retries the
local override.

---

## Batch 11 — the Course 1 open-items doc (written at cf591e2)

Two of its six items were already fixed in `ec8cce4`, which postdates that test
run: the Lab 3 zip wording, and `--smoke` keeping its trace.

### 11.1 Strengthened: a timed-out case no longer reports success

`ec8cce4` warned on a timeout-with-score. The doc asked for more — don't count a
timed-out case as complete. `--smoke` now **exits 1** when a case records a
timeout, whatever `plugin eval`'s own exit code said, and prints the report path
(which the doc noted was being printed and then deleted).

### 11.2 `manifest.json` data_dir description

Reworded to be true whichever packer was used. It now says the extension falls
back to the bundled `sample_data` folder *if the bundle includes it*, notes that
`pack_mcpb.py` includes it and now fails when it is missing, and tells the user
to set the folder explicitly if the extension starts with no records.

### 11.3 NOT DONE, needs the format confirmed: `mocks/<server>/_tools.json`

The doc asks for `mocks/boardpack/_tools.json`, because without it the model sees
a permissive schema and no tool descriptions. No product ships one.

**I am not authoring this blind.** The mock tool files use `type: fixed`
frontmatter and carry no schema, so `_tools.json` is a separate manifest whose
shape `claude plugin eval` defines, and I do not know it. Three unverified fixes
have already cost a cycle each in this effort — the sysctl, the sandbox probe,
and `server.type` — and all three were me asserting a format or behaviour I had
not checked.

What is needed: the expected `_tools.json` schema. The tester has `plugin eval`
available and can establish it cheaply. Once the shape is known, the content is
straightforward, because each BRIEF already fixes the tool names and behaviours —
for Product 1 that is `get_kpis`, `get_exec_notes` and `list_sources`.

### 11.4 Still disputed: the trigger grader

The doc repeats the request to "accept the contract commands too". I did not do
that in `ec8cce4` and have not now, because the analysis says the grader is
right:

- its pattern already allows a namespace prefix
- `trig-1-natural` allows `[Read, Glob, Grep, Skill, Agent]` and **no
  `SlashCommand`**, so a slash command was not the route
- the contract fixes the skill folder as `board-pack`; `draft` is a command

`Skill called 0x` means the Skill tool was never invoked. The likeliest path is
that the model read `commands/draft.md` with Read or Grep and followed it by
hand. If so the skill genuinely did not trigger, which is exactly what
`trig-1-natural` exists to detect, and accepting commands would mask a skill
whose description does not fire.

**One question decides it:** does the plugin under test contain
`skills/board-pack/SKILL.md`?

- **Yes** → the skill exists and did not fire. The 0 is correct and the lesson is
  the skill description. Nothing to change in the grader.
- **No** → the skill is misnamed, violating the contract. The 0 is still correct,
  and the new `check_structure` warning in `ec8cce4` now predicts it for free
  before any paid run.

Either way the grader stands. Raised here so the disagreement is on the record
rather than silently unresolved.
