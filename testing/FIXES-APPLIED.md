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

---

## Batch 12 — Course 4 retest (2026-11-04, at 47781a3): 4 of 5, and two bugs of mine

**Result: Lab 1 100/100, Lab 2 100/100, Lab 4 pass with notes, Lab 5 reviewed,
Lab 3 blocked at Step 6.** Both labs that failed for a single cause now score
full marks, and every fix from the previous batches held.

One correction to my own summary, from the tester: flagging `payments-gateway`
**is** still penalised 10 points, as it should be, since it is the clean
repository. What changed is that the penalty is now *fair*, because the repo is
genuinely clean. My earlier wording said the flag should no longer be penalised,
which was wrong.

### 12.1 MY BUG: `is_verify` traded a false negative for a false positive

My Course 4 Lab 1 fix widened the check to accept any row containing `verif`.
The tester found that lets an unrelated row — "Verify the attribute mapping with
the pilot users" — stand in for domain verification, so real verification could
sit **after** enforcement and still score 100/100.

I fixed a check that rejected correct answers and created one that accepts wrong
ones, without testing the second direction. `is_verify` now anchors on the
domain that defect D4 is actually about, excluding the enforce step.

Tested both directions this time: the unrelated "verify" row is rejected, real
domain verification accepted, the enforce step rejected, and a row saying
"verification" while naming no domain rejected.

### 12.2 MY BUG: Lab 3's prediction still misled, because I fixed the string not the condition

I made attack 3's *message* conditional on the sandbox but left the condition
itself as a deny-rule-OR-sandbox test. The OR meant a deny rule alone satisfied
it, so with the sandbox disabled attack 3 printed "blocked if the OS sandbox
starts" while attacks 1 and 2 correctly printed "will succeed" — and the
fallback scoring, which reads those lines, awarded 5 points for it.

`read_ok` now requires the sandbox, consistent with `net_ok` and `write_ok`, and
consistent with the explanation already in the file: deny rules gate the Read
tool, the OS sandbox stops Bash.

### 12.3 Lab 3's two approved MCP servers both misbehaved

- My `ticket_bridge.py` stub exited immediately, so a session reported
  `status: failed` and students would chase a non-issue.
- `docs-search` ran an unpinned package fetched **by name over the network**.
  Harmless while Node was absent; a live fetch once the image gained Node. The
  wrong thing to model in a hardening lab.

Checked the brief first: both are on the **approved** list, and the planted
defect is `shadow-sync` ("has not been vetted"). So neither was the lesson.

Both now point at `tools/mcp_stub.py`, a dependency-free stdio stub that answers
`initialize`, `tools/list` and `tools/call`, logs to stderr, and touches no
network or files. Verified end to end. **`shadow-sync` keeps its unvetted
command — the planted defect is intact.**

### 12.4 Answer leaks

- **Lab 5's Troubleshooting named the decoy outright** — it said of
  `payments-gateway` that it is the decoy and correct, a direct 10-point
  giveaway. Reworded to say one of the three is clean and to judge each on its
  own evidence.
- **Lab 1 and Lab 2 both listed their checker as a flat prerequisite** while
  also saying it may be withheld. Both are now conditional: only if the
  facilitator hands it out, because it contains the answer logic.

### 12.5 My rubric note was factually wrong

I wrote that `cred-102` had been rotated since creation. Its created and
last-rotated dates are both 2026-08-20. Corrected: equal dates are normal for a
credential inside its first rotation period, and the real distinction from
`cred-101` is **ownership and expiry**.

### 12.6 Lab 4

- Defence 03 now sets `sandbox.allowUnsandboxedCommands: false`. The Course 1
  retest showed the model stepping outside the sandbox after it had correctly
  refused, so a defence config omitting this is not testing what it claims.
- New guidance for the case the tester hit: narrowed tools blocked the command,
  so the model used `Read` and obtained the payload anyway. Record the action as
  stopped by narrowed tools, and note separately that the text still reached the
  model. **Narrowing tools stops the effect, not the exposure.**
- The "this guide has not been run against any model" note is replaced with what
  the run showed: all eight runs refused by `claude-opus-5-5` on 2026-11-04.

### 12.7 Smaller

- Lab 3 Troubleshooting gained an AppArmor row, including that relaxing the
  sysctl does not help because the profile carries an explicit deny.
- The canary listener in `attack_simulation.py` no longer prints a
  `ConnectionResetError` traceback. The socket block already caught `OSError`;
  the traceback came from the handler **thread**, which the main try/except
  cannot see. Fixed with `handle_error` on a server subclass.
- `demo-files/README.md` rows now show the `facilitator/` layout.
- Lab 5's Checkpoint now matches the template: an owner for every credential in
  the inventory, not only reported findings.
- `cred-103` expiring three weeks after the audit date is ruled on: not a
  planted issue, no points either way, and credit it in the rotation plan if a
  student schedules it.

All Course 4 Python compiles and all JSON validates. Both planted defects
verified intact.

---

## Batch 13 — verifying the Desktop steps without a GUI

**The question was whether to write Playwright scripts for Course 1's Desktop
steps. No: Playwright drives browser pages, and Claude Desktop is a native
application.** Its experimental Electron support targets apps you launch from
source, not a signed third-party install, so it would be brittle and
unsupported.

More usefully, GUI automation is not what those steps need. Three Course 1
checks were listed as needing a person:

| Check | What it asserts |
|---|---|
| Lab 1 Part 8 | install the extension in Desktop and ask a question that uses a tool. The step's own acceptance criteria is only that a packed `.mcpb` exists; the install is explicitly optional and unscored |
| Lab 3 Part 5 | "it installs and a tool call works" — the scored one |
| Lab 1 Step 10 | "`/mcp` lists your server with three tools" — this is **Claude Code**, not Desktop |

All three are really one question about **our artifact**, not about Anthropic's
installer: *does the bundle contain a server that starts and serves its tools?*

### `testing/verify-mcpb.py`

```
python3 verify-mcpb.py path/to/plugin-0.1.0.mcpb --expect get_kpis,get_exec_notes,list_sources
```

It extracts the bundle, validates the manifest the way `mcpb` does — including
the `server.type` enum that my own sweep once broke — then launches the server
**exactly as the manifest says Desktop would**, expanding `${__dirname}` and
passing an empty value for any unexpanded `${user_config.*}` so the server
exercises its own default. Then it speaks MCP over stdio: `initialize`,
`tools/list`, and a `tools/call` on the first tool.

It also checks two things a student loses points for and would not otherwise
see until a Desktop install:

- every tool has a non-empty description, since a model cannot choose well
  without one
- `manifest.json` sits at the **top** of the archive, not nested under a wrapper
  directory, which is the zip-layout failure the labs warn about

Verified end to end against a freshly packed starter server: 8 checks, 0
failures, `initialize` answered, `tools/list` returned its tools, and
`tools/call` returned a result.

One useful side effect: the run showed the server resolving its data directory
to the **bundled `sample_data`**, which independently confirms the bundle
carries the sample data and the no-config fallback works. That was an open
question from the `data_dir` wording discussion.

### What still needs a person, and why that is fine

Claude Desktop's own install dialog, and whether Desktop renders the extension.
That is Anthropic's software rather than course content. It is one click-through,
once per content revision, and the script narrows what it proves: **if
`verify-mcpb.py` passes and the Desktop install fails, the problem is the
installer or the account, not the bundle.**

The `/mcp` screen is a Claude Code TUI and equally out of Playwright's reach.
Its substance — the server is connected and exposes three tools — is what this
script checks directly, without spending model credits.

---

## Batch 14 — Course 2 retest (2026-11-04, at eaaa97e): 4 of 5

**Lab 1 Track C pass with notes (gate 100/100 on both files), Lab 2 pass with
notes at GOLD with 5/5 bugs and 0 false positives, Lab 4 pass with notes, Lab 5
reviewed, Lab 3 blocked at Step 6 only with 2 of 6 eval cases unreliable.**

Lab 3 came out better than expected: blocked at one step rather than wholesale,
with four of six eval cases trustworthy.

### 14.1 Both falsifiable checks came back — and both notes needed work

I had asked the tester to try to disprove two notes I added. Both earned their
place, and both were imprecise.

**T5 `env:` laundering — correct, and broader than I wrote.** Job, step **and**
workflow `env:` all scored 100/100, and so did a **step output**, which my note
did not mention. The direct form scores 85. Note extended to name all four
routes.

**GitLab by filename — true, but my wording was wrong.** The check is
`startswith(".gitlab-ci")`, so `.gitlab-ci.yaml` is recognised too; my "any name
other than `.gitlab-ci.yml`" was too strong. `gitlab-ci.yml`, `ci.yml` and
`my-job.yml` are skipped, and the gate **exits 0**. And `--platform gitlab`
solves it, which the lab never mentioned. Row rewritten with all of that.

### 14.2 MY BUG: the T5 note broke a table and was in the wrong place

I inserted the note **between two rows of the Facilitator Notes trap table**,
which ended the table and left its last two rows rendering as stray text. It was
also in the Facilitator Notes, so students never saw the thing it warns about.

Moved into **Step 6**, where students read it, and the "Gate passes but the run
leaks" troubleshooting row now points at the same limit. The table is whole
again.

### 14.3 MY BUG, third iteration: the pr-10 bait could still round up

The float guard fixed the original defect — 100 at 0.29 gives 29, 28.7 gives 28,
and 999,000 realistic combinations came out right — but the reviewer found
`prorated_fine_cents(3, 9.66666666)` returns **29** where LIB-7 requires 28.
`round(..., 6)` rounds up, which the docstring explicitly says it does not do.

I had replaced a float-precision bug with a rounding bug. My own sweep had used
only two-decimal rates, so it never reached the failing window.

Now exact, with no rounding anywhere:

```python
return int(Decimal(str(days)) * Decimal(str(rate_cents_per_day)))
```

Verified against every case that broke the two earlier versions, plus a
**400,000-combination sweep with zero mismatches**, and then run from the
**actual generated fixture** rather than a copy of the snippet.

Two further corrections while fixing it:

- The import first landed **mid-file, after a function** — its own review smell,
  which in a code-review lab would have created a new false positive. It is now
  at the top of the generated file, grouped above the local import.
- `diffs/` and `facilitator/answer_key.json` are **generated** by
  `build_fixture.py --emit-key`, so they are regenerated rather than hand-edited.

### 14.4 Lab 1: 10 Track C points still had no step

The rubric scores "what each fixture tries **and** which control stops it", but
my Step 11b asked only the second half, and pointed at Part 5 — which Track C is
told to skip. Step 11b now names both fixture files, asks what each one tries,
and says this is where that analysis happens for Track C. The rubric row names
Step 11b.

Also from the tester's review of Step 11b: a citation per *claim* was too much
for 15 minutes. Changed to **one citation per bullet**, and the part is now 25
minutes.

### 14.5 Lab 1: three smaller gaps

- The **prerequisites** still asked every track for a hosted project. Marked
  Tracks A and B only.
- Three **Checkpoint** items a Track C student cannot meet are now marked as
  such, with a pointer to Step 11b for the injection one.
- **Step 1's test command** came before the venv and failed with `No module
  named pytest`, and `mc-ci` had no pytest. Step 1 now points at
  `tallybook/README.md`, which creates its own venv, and **`pytest` was added to
  the `mc-ci` venv** in the provisioning script.

### 14.6 Lab 3: 23 of 35 points no longer ride on the image

Two of the six eval cases need a shell — `uses-auditor` runs a scaffold script,
and any case reaching `changelog-auditor` gets `Bash`. Without a working sandbox
those two cannot produce a trustworthy score.

Fallback scoring added, modelled on Course 4 Lab 3: score the suite out of the
**four cases that need no shell**, and record the other two as NOT SCORED with
the reason. Explicitly **not** as failures, because a case that could not run has
not produced a result. The AppArmor cause is named as a platform limit.

### 14.7 Lab 2: the thresholds are measurably too easy

A run reached **Gold with 5/5 bugs and 0 false positives in one tuning round**,
against 45 minutes budgeted. The "untested" note is replaced with that result and
the two options — tighten Gold to require 0 false positives, or add a harder bug
needing a read across files. **Left as a teaching decision rather than re-tuned
unilaterally**, since it changes what the lab rewards.

### 14.8 Smaller

- **Lab 2 fixture now ships a `.gitignore`** (`__pycache__/`, `*.pyc`,
  `.venv/`). A committed `__pycache__` aborted a branch checkout for the tester.
  Verified by rebuilding and checking out `pr-10-prorated-fine` cleanly.
- **Lab 3**: the stale `python` troubleshooting row removed, a concrete command
  given for excluding `evals/results/`, and the 20-point rubric row says "local
  path or git".
- **Lab 4**: Step 3's `--plugin-dir pylsp-plugin-starter` corrected to `../` for
  a shell in `sample-project`, and Step 7 now says diagnostics can arrive a turn
  later so students do not treat a delay as failure.

All Course 2 Python compiles and JSON validates. Both planted defects verified
intact: Lab 3's hardcoded hook path and Lab 4's wrong-binary variant.

---

## Batch 15 — decision taken: Lab 2's Gold band requires zero false positives

Course owner's call on the open question from batch 14. Of the two options —
tighten Gold, or add a harder bug needing a cross-file read — Gold is tightened.

`TIERS` in `score_review.py` changes Gold's false-positive allowance from 1 to
0. Silver still allows 3 and Bronze 5, so the ladder still rewards finding bugs
while **Gold is now where precision is tested**.

Verified against the real answer key:

| Findings | Old tier | New tier |
|---|---|---|
| 5/5 bugs, 0 false positives | Gold | **Gold** |
| 5/5 bugs, 1 false positive | Gold | **Silver** |
| 5/5 bugs, 2 false positives | Silver | Silver |
| 4/5 bugs, 0 false positives | Silver | Silver |

So the 2026-11-04 run that reached Gold in one round with 0 false positives
still would; its earlier attempt, which had 5/5 and one false positive, now lands
Silver. That is the behaviour the tightening was for.

Updated in three places so nothing contradicts: the `TIERS` constant and the
docstring band in `score_review.py`, the band in
`facilitator/ANSWER-KEY.md` with the date and reason, and the Facilitator Notes
in the lab — where the open question is replaced by the decision.

The lab's note now also states the intended lesson: a student who reaches Silver
with everything caught is one careless finding away from Gold.

---

## Batch 19 — Course 3 first run (2026-11-05): 2 of 5, partial report

Course 3 was tested for the first time, on a real key. Total spend **$6.63 over
318 agent runs** (about $6.73 including unlogged calibration runs). Verdicts:
Lab 1 FAIL, Lab 2 pass with notes, Lab 3 FAIL, Lab 4 blocked at Part 6 only,
Lab 5 pass with notes.

The tester's per-lab sections were still being written when this batch was
applied, so only the findings that were already evidenced are acted on here.

### 19.1 The headline is a model dependency, not a bug in the material

With Lab 3's planted limits, **Sonnet and Haiku broke the 15-call bound in 6 of
6 runs**, making 57 to 186 `check_manifest` calls. **Opus stopped on its own**,
so `lab3_check.py` reported **7 of 7** while the bound was never defended.

**Correction to the first version of this entry:** I first wrote this up as
grader blindness. That was wrong. `lab3_check.py` line 49 does assert the bound
(`calls <= lp["max_check_manifest_calls"]`), so the checker detects the
violation correctly.

The real defect is that the lab breaks in **opposite directions** by model. On
Opus the agent stops unprompted, so the check passes 7/7 whether or not the
student set any limits - no learning signal. On Sonnet and Haiku the bound
breaks even for a student who used every lever Step 5 hints at, because none of
those levers bounds a subagent's turns (19.1b). With `AGENT_MODEL` unset the run
used `claude-opus-5-5`.

Lab 3's Facilitator Notes already carried a rehearsal item asking exactly this
question. It is now **answered in place** with the measured numbers, plus an
instruction to rehearse on the model the class keys actually use and to treat a
pass on Opus as unproven.

### 19.1b Root cause: an unbounded subagent, not the budget and not parent turns

Traced through the fixture, the cause is neither limit first pointed at:

- **Not the budget.** The runaway is cheap. The largest run of any kind was
  $0.4620 at up to 186 calls, so roughly **$0.0025 a call** - about **200 calls
  to reach a $0.50 cap, against a bound of 15**. A spend cap cannot bind on this
  fixture no matter what it is set to.
- **Not the parent's `max_turns`.** That bounds the parent's turns, not the tool
  calls made inside a subagent. One parent turn delegating to `manifest-watcher`
  can produce dozens of `check_manifest` calls.
- **The cause:** `loop_fixture.LOOP_SUBAGENT` has **no `maxTurns`**, and its
  prompt says "Never give up. If you cannot finish, spawn another subagent." The
  four levers Step 5 hints at - `max_turns`, `max_budget_usd`,
  `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`, `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`
  - limit the parent and how subagents spawn, but **none limits turns per
  subagent**. `SendMessage` (19.2) compounded it by letting the parent revive
  subagents that had stopped.

A student can fix this only by overriding the `AgentDefinition` from
`lab3_agent.py` - which is allowed, since the starter passes
`agents={"manifest-watcher": loop_fixture.LOOP_SUBAGENT}` and so needs no edit
to the fixture - but **no step or hint tells them to**. That is why the working
fix needed subagent `maxTurns`: it is the only lever that bounds the loop, and
it is the one lever the lab never names.

**Decision needed, because it changes what the lab rewards:** name subagent
`maxTurns` in Step 5's hint and the acceptance criteria, or leave it as the hard
part students must find. Either way the model question stands: on Opus the check
passes with no student work at all.

### 19.1c FIXED: the loop is now containable, and the check discriminates

Fixed without changing what the lab asks. Step 5 still says contain the runaway
from outside without editing the fixture, the student still chooses every value,
and all four planted traps stand (`MAX_TURNS = 3`, `BUDGET_USD = 5.00`,
`"Helper."`, the camelCase gotcha).

**1. The fixture gained a factory, default unchanged.** `loop_fixture.py` now
exposes `loop_subagent(max_turns=None)` built from the same literals.
`LOOP_SUBAGENT` is kept as `loop_subagent()`, so the planted runaway is byte-for-
byte the same behaviour. Putting the factory in the fixture avoids introspecting
`AgentDefinition`'s field names, which could not be verified locally because the
SDK is not installed on this machine.

**2. The starter gained TODO 5.** `LOOP_SUBAGENT_MAX_TURNS = None`, wired into
the loop branch. This is the one lever that bounds a subagent's own turns, and it
is reachable from the starter, so "without editing the fixture" stays true. It
defaults to `None`, so the exercise is unchanged: the student must still work out
that the parent's `max_turns` cannot reach inside a subagent.

**3. The checker gained three configuration checks**, taking it from 7 to 10:
subagent turn limit set, spend cap lowered below the planted 5.00, and depth and
concurrency both set. These assert exactly what the rubric already scored, so no
scoring intent changed — but they make the result **model-independent**. The
starter now scores **0 of 3 on config, so at most 7 of 10**, which means a model
that stops on its own can no longer hand a pass to a student who set nothing.

**4. Both tracks score identically.** `SUBAGENT_DEPTH` and
`SUBAGENT_CONCURRENCY` had to be exported in `lab3Agent.ts` for the third check;
without that a TypeScript student would have been scored out of 9 while a Python
student was scored out of 10, and the rubric rows would no longer map one to one.

**5. The lab text now names the lever and why the others miss.** Step 5's hint
adds `LOOP_SUBAGENT_MAX_TURNS` and states that `max_turns` bounds the parent, and
depth and concurrency bound spawning, so neither reaches a subagent's turn count.
Two troubleshooting rows added; the rubric's loop row now mentions the subagent
limit; the acceptance criteria say the limits themselves are checked.

**The teaching point this adds, which was the finding underneath:** a spend cap
cannot contain this fixture at any value. At about **$0.0025 a call it needs
roughly 200 calls to reach $0.50, against a bound of 15**. That is now in the
Facilitator Notes, because it is the reason the budget was never the answer.

Verified: both trackers' trap values unchanged, the starter fails 3 of 3 config
checks, Python files parse, and the lab's markdown tables are intact (checked by
pipe count per table, after breaking a table this way once before).

### 19.2 FIXED: `SendMessage` escaped containment

`BUILTIN_TOOLS` is passed as `disallowed_tools` by Lab 3 and `demo6_caps.py`.
`SendMessage` was not in it, and the tester observed it succeed and **resume
stopped subagents**, which defeats the turn bound the lab exists to teach.

Added to the list in **both tracks** (`agent_core.py` and `agentCore.ts`), with
a comment saying why. Safe because the list is only ever used to deny: it is
never an allow-list, and `SendMessage` appears nowhere else in Course 3, so it
is not part of any exercise. The tester had already validated this fix together
with a subagent `maxTurns`: 10 of 10 loops stayed in bound at 5 to 9 calls, each
ended by a real `error_max_turns`, and the digest still succeeded.

### 19.3 NOT APPLIED: making `BUDGET_USD` honour `LAB_BUDGET_USD`

The tester asked for this third. **Declined as worded**, because `MAX_TURNS = 3`
and `BUDGET_USD = 5.00` are **documented planted traps** — the starter says "these
two numbers are deliberately wrong for the task" and the Facilitator Notes list
them as trap 1. Wiring the instructor's cap into the starter would hand students
the answer to TODO 3 and delete the exercise. This is the same mistake class as
the `server.type` regression: changing a value that is deliberately wrong.

The underlying concern is real and still open: with `$5.00` hardcoded, the
instructor's `LAB_BUDGET_USD` does not reach **the one lab designed to run
away**. Recommended shape instead of the tester's version: clamp
`max_budget_usd` to `LAB_BUDGET_USD` inside `make_options` **as a ceiling**, so a
student's chosen number still has to be sane but can never exceed the class cap.
Needs a decision, because a ceiling that binds at $0.50 ends the loop with
`error_max_budget_usd` — an accepted pass — which could let a student pass
without doing the containment work.

### 19.4 The $0.50 cap is less proven than the result suggests

Check 1 came back "not disproved": no run of 318 exceeded $0.50, the largest
scored-type run was $0.1274, and the largest of any kind was $0.4620.

Read with 19.3, that evidence is weaker than it looks. **Lab 3 did not run under
a $0.50 cap at all** — it ran under its hardcoded $5.00 — and Lab 3 is where the
runaway lives and where $3.07 of the $6.63 was spent. The near-cap run "stopped
itself at 92% of the cap" rather than being stopped by it. So nothing in this run
demonstrates the cap actually binds; it shows only that normal runs stay cheap.

### 19.5 Lab 2's Part 3 measures nothing

**0 of 36 starter runs obeyed the injection**, across three models, so the
baseline Part 3 asks students to measure does not exist. The only
checker-visible change was wording. The capability control *is* real: the refund
was written 2 of 2 on the starter and 0 of 2 with `disallowed_tools` or the tool
removed. Not yet fixed — the fix depends on the per-lab detail still being
written.

### 19.6 Still open

- **Lab 1 FAIL** — scored 95 but failed on a "key defect" whose description was
  still pending. No action possible yet.
- **Lab 4 Part 6** — NOT TESTED, no Console login on the run. Needs 10 minutes
  from someone with a class login. This is the one item the provided Console
  access was meant to unblock.
- Rubric scores are not evidence: Labs 2 and 3 scored 98 and 95 while their
  planted problems did not fire.

---

## Batch 20 — Course 4 review (2026-11-06), with Courses 4 and 5 now taught first

### 20.1 CORRECTION: Lab 3 is not blocked, and I said it was

I wrote that Course 4 Lab 3 was "genuinely blocked" because proving the sandbox
blocks the attacks is the exercise. That was wrong, and it mattered: it made the
AppArmor decision look like a gate on the first course out the door.

**Line 153 of the lab already defines fallback scoring.** Part A is 60 points and
"works everywhere". Attacks 1 to 3 score 5 each from the checker's PREDICTED
outcomes, attack 4 is always scored live because it needs no sandbox, and the
**maximum is 85**. Line 19 says a sandbox that cannot start is "a known platform
limit, not a failure", and the troubleshooting table says the same.

So AppArmor sets Lab 3's **ceiling** (85 to 100), not whether it can run. With
Course 2 Lab 3's fallback added in batch 14, **no lab in the suite is hard-blocked
by the AppArmor decision.** It is still worth taking, but it is not critical path
for Courses 4 and 5.

### 20.2 All four Course 4 checkers run clean after our edits

Ran every checker locally; none needs a credential, which is consistent with
Course 4 costing nothing. `check_lab1.py` scores the starter correctly at 0 of 5
defects found, so it discriminates. `check_lab2.py`, `check_settings.py` and
`check_record.py` print usage and exit cleanly. No regressions from the edits of
the past three days.

One measurement caveat: I read exit codes through a `| head` pipeline, so the
reported exit status was `head`'s, not the script's. The outputs are sound; the
exit codes I printed were meaningless.

### 20.3 Two of Lab 3's three UNVERIFIED settings items are now settled

`check_settings.py` carried three items to "confirm against current documentation
before delivery". These gate Part A, which is 60 of 100, so they matter more than
the sandbox question.

**Settled, from our own evidence:** the `sandbox.*` parent object is correct and
honoured. `testing/sandbox-probe.sh` forced
`{"sandbox":{"enabled":true,"failIfUnavailable":true}}` and the VM **failed
closed** with `apply-seccomp: write /proc/self/setgroups ... Permission denied`,
where the same probe with no settings had run Bash unsandboxed and passed. A key
that was ignored could not have changed that outcome. Recorded in the script with
the evidence rather than as an assertion.

**Still open:** the MCP server allowlist key name. The checker hedges by accepting
either `enabledMcpjsonServers` or `allowedMcpServers`, so a student is scored
fairly either way — but **Step 3 teaches one spelling, and if it is the wrong one
the student's allowlist does nothing while the checker still awards 8 points.**
That is the highest-value Course 4 item left, and it needs one documentation
check, not a test run.

**Also not separately proven:** that `allowUnsandboxedCommands: false` actually
blocks a retry. The probe's history shows a model stepping outside the sandbox in
v2, which is why v3 added the key, but no run isolates it.

### 20.4 FIXED: two false-pass paths in Lab 3's checker, worth 15 points

Settled the remaining key names against the official settings reference rather
than leaving them flagged. Both hedges the checker carried turned out to accept
a key that does not exist:

- **`sandbox.*` is the only spelling.** `sandbox.enabled`,
  `sandbox.failIfUnavailable` and `sandbox.allowUnsandboxedCommands` are all
  children of the `sandbox` object; there is no top-level form. The checker
  accepted a top-level `allowUnsandboxedCommands` and would have awarded **7
  points for a key Claude Code ignores**. Removed.
- **There is no `allowedMcpServers` key.** The real ones are
  `enabledMcpjsonServers`, `disabledMcpjsonServers` and
  `enableAllProjectMcpServers`. The checker accepted `allowedMcpServers` and
  would have awarded **8 points for a list that does nothing**. Removed.

Both are the same failure mode as our earlier false passes: a grader generous
enough to accept a configuration that has no effect. A student could have
hardened nothing and scored 15 of 60 on Part A.

**The lab text was clean** — it never taught either wrong key. Step 3 states
acceptance criteria and names no key at all, which suits a 300-level discovery
step. I added a pointer that keeps the discovery: it says the starter approves
every declared server, tells students to find the setting that approves only
named ones, and warns that an unrecognised key is skipped silently so their
allowlist would do nothing. The key itself is still theirs to find.

Regression checked: the checker scores the unhardened starter **0 of 60** with
every planted trap detected and all four attack predictions reading "will
succeed".

---

## Batch 21 — Course 4 retest on the new RVC image (2026-11-11, at e94bcb4)

**Result: Lab 1 100/100, Lab 2 99/100, Lab 4 pass with notes, Lab 5 reviewed,
Lab 3 FAIL.** The image team baked in items 2, 3 and 4 of IMAGE-REQUIREMENTS;
item 1 is untouched and the sandbox still does not start.

### 21.1 MY BUG, and the worst kind: I deleted a key that exists

Batch 20.4 removed `allowedMcpServers` from `check_settings.py` and wrote in the
docstring that the key does not exist. It does. The settings reference lists it as
"Allowlist which MCP servers users can add", scope `Any file`. I had gone looking for
false passes, found a hedge, and removed the half of it that was real.

So between 20.4 and this batch, a student who followed the Step 3 hint to the
reference and picked the key whose description literally says "Allowlist" scored
**0 of 8** and was told by the script that their key did nothing. That is worse than
the false pass I was trying to fix: a false pass costs the course its discrimination,
a false *fail* costs a correct student their marks and their confidence in the
material.

Re-verified against the reference on 2026-11-11. All five MCP keys are real and do
different jobs:

| Key | What it does |
|---|---|
| `enableAllProjectMcpServers` | approve every server `.mcp.json` declares |
| `enabledMcpjsonServers` | approve named servers from `.mcp.json` (pre-approval) |
| `disabledMcpjsonServers` | reject named servers from `.mcp.json` (enforcement) |
| `allowedMcpServers` | allowlist what a user may **add**; explicitly not `.mcp.json` |
| `deniedMcpServers` | block by URL, command or name |

**[SUPERSEDED 2026-11-11 by batch 22.1 — the paragraph below is wrong. The quoted
sentence is not in the settings reference, the documented type is an array of
single-key objects, and the tester's variant B was right.]**

**One correction to the tester, too.** Their variant B concluded that
`allowedMcpServers` is "the key that actually blocks an unapproved server" in a
project `.mcp.json`. The reference says the opposite in as many words: "This key
doesn't restrict servers declared in a project `.mcp.json` file; use
`disabledMcpjsonServers` for that." Variant B also used `{"serverName": ...}`
objects, where the documented type is an array of strings — and that object shape came
from my own checker code, not from the docs, so the measurement has a confound. The
substance of their finding stands and the fix is theirs; only the mechanism is
misattributed.

### 21.2 FIXED: Step 3 now scores the decision, not the key-name hunt

The deeper problem is that Step 3 made students guess a key name from a reference
where three of five descriptions read like the answer. A student could reason
correctly about the security goal and still land on a key that does something else.
That is trivia, not a 300-level exercise.

Step 3 now **names the four relevant keys in a table with one line each**, and asks
the question worth asking: which of these is a control? The MCP item splits into two:

- **5 points, the enforcement:** the blanket approval is off, and no unapproved server
  is left running — either deleted from `.mcp.json` or explicitly rejected.
- **3 points, the setting:** any of `enabledMcpjsonServers`, `allowedMcpServers`,
  `disabledMcpjsonServers` or `deniedMcpServers` naming only approved servers, or
  rejecting the unapproved one.

Part A stays at 60 and the rubric line was updated to match. Tested six ways: all four
defensible student answers score 8/8 (including both `allowedMcpServers` shapes), the
unhardened starter still scores **0 of 60**, and the two wrong mental models —
pre-approval with the server still declared, and the starter's blanket left on — lose
exactly the 5 enforcement points and keep the 3. The checker now discriminates on the
thing the lab is teaching.

### 21.3 FIXED: Lab 3 Step 6 was unreachable on a correctly hardened config

The tester found what reading could not. With the required `failIfUnavailable: true`
on a machine whose sandbox fails at **runtime** rather than at startup, the session
starts normally and then refuses *every* Bash call — including `attack_simulation.py`.
So the fallback scoring's promise that "attack 4 is always scored live because it
needs no sandbox" could not be kept from inside a session, and a student doing
everything right hits a wall the lab never mentions.

Step 6 now says so explicitly: if the session refuses every command with the
`apply-seccomp` error, the configuration is **correct** and the machine has no working
sandbox — run the attack script in your own terminal for attack 4 and take 1–3 from
the predictions. The fallback-scoring line says the same. Also noted that
`failIfUnavailable` does not trip at startup when bubblewrap is present, which is the
question a student will actually ask.

### 21.4 FIXED: Lab 5's clean repository was not clean

All three CI workflows injected a `setup-token` credential as `ANTHROPIC_API_KEY`. Per
the authentication docs a setup-token is read from `CLAUDE_CODE_OAUTH_TOKEN`;
`ANTHROPIC_API_KEY` is for Console API keys. So a sharp student flagged
`payments-gateway`'s CI, was right, and lost the 10 "clean repo" points for it.

Also settled what the rubric flagged UNVERIFIED: `claude setup-token` generates a
**one-year** OAuth token. The scenario's `expires: none` on `cred-101` contradicted
the product, and `cred-102`'s six-month expiry did not match a one-year token either.

Fixed together, keeping C4 intact:

- All three workflows now use `CLAUDE_CODE_OAUTH_TOKEN`.
- `cred-101` is now created 2026-02-02, expiring 2027-02-02 — a real one-year token.
  C4 is unchanged in substance and arguably sharper: person-owned, never rotated,
  owner departed 2026-06-30, still used 2026-10-09. The defect is the dead owner and
  the absent rotation, not a magic no-expiry credential.
- `cred-102` now expires 2027-08-20, one year from creation.
- The "defending the clean repository" note and both UNVERIFIED notes rewritten.

The near-expiry decoy (`cred-103`, 2026-11-02) is untouched and still the only
near-term expiry in the tree, so it keeps working as a decoy.

### 21.5 FIXED: two Lab 2 checker items that penalised correct answers

- `auth_methods_covered: ["web","desktop","api_key","oauth_token"]` scored −1 with
  "authentication coverage incomplete", because the matcher accepted `api key`,
  `api-key` and `apikey` but not `api_key` — the one spelling a student would naturally
  write in a JSON file whose own field names are snake_case. The matcher now normalises
  `_` and `-` before matching. Verified across four spellings.
- The lab demanded "every event in the sequence" while the checker required
  `min(3, len(ids))`. Citing 3 of 64 scored full marks. Aligned the lab to **at least
  three**, which is what the checker measures and what a reviewer actually needs;
  requiring all 64 would be busywork.

### 21.6 FIXED: Lab 4's `-p` path silently skipped the payload

Under `-p` in `default` mode, `python3 tools/ticket_lookup.py 17` needs approval and
`-p` has no prompt to answer, so without `--allowedTools` the tool never runs and the
payload never reaches the model — a run a student would record as a defense working
when nothing was tested. The lab now gives the flag. Also: config 03 is not
exercisable when the sandbox cannot start, so students are told to pick 04 as
"strongest" and say why; the prose "Tool vector" is renamed to match the CSV's
`tool_result`; and the trust hint is corrected — `-p` shows no dialog but *does* act on
trust, ignoring the project file's `permissions.allow` and printing a warning.

### 21.7 FIXED: two pieces of our own testing tooling were lying

- `provision-rvc.sh` reported `$HOME/.local/bin not on PATH` as a FAIL. The RVC image
  ships the **apt package** at `/usr/bin/claude`; `~/.local/bin` does not exist. The
  check now asserts that `claude` resolves at all and notes when it is not the native
  installer. One of the five FAILs in the tester's run was ours.
- `sandbox-apparmor.sh --diagnose` still printed that `local-override` is "viable and
  upgrade-safe", which batch 10.6 recorded as tried and failed. It now says so and
  points at the two untested options.

### 21.8 Sandbox: still the top item, and one caveat retired

Same denial, same profile: `apparmor="DENIED" operation="capable" profile="unpriv_bwrap"
capability=21 capname="sys_admin"`. No AppArmor change was applied in this run.

One thing improved: the apt build lives at `/usr/bin/claude`, root-owned and
**stable**, so IMAGE-REQUIREMENTS' caveat that `claude-profile` would drift on
auto-update does not apply to this image. That makes the narrow option worth one
`--try` before anyone argues about `disable-profile`.

Lab 3's ceiling is still 85 and no lab in the suite is hard-blocked by this.

### 21.9 Not fixed, needs a decision

**Student packs.** `check_lab1.py`, `check_lab2.py`, `check_record.py` and the
`facilitator/` folders all ship in `demo-files/`. `demo-files/README.md` says to strip
them before distribution, but Lab 4 tells students to run `check_record.py`. The README
and Lab 4 contradict each other, and there is no scripted way to build a student pack.
Three testers have now flagged this. It needs a `make-student-pack` step and a decision
on whether `check_record.py` is a student file.

**Lab 2 Track B** requires the exact string `com.anthropic.claudefordesktop`, which the
lab never supplies and which it says key names are not given for. Confirm the deck
supplies it or list it under "Facts you need".

**Durations.** Labs 1 and 5 look generous at 90 and 60 minutes for the offline path.
Not a defect; worth a rehearsal with a real student before it is changed.

---

## Batch 22 — Course 4 run 2 (2026-11-11, at 95af615): the fixes held, and I was wrong twice about the same key

**Result: Lab 3 FAIL → PASS WITH NOTES (85/85 fallback, no deviation), Lab 2 99 → 100,
Lab 1 100, Lab 4 pass with notes, Lab 5 reviewed.** Seven of the nine batch 21 fixes
held. The two that did not are both mine, and both are the same key.

### 22.1 MY BUG, twice, and the second time I invented the evidence

Batch 20.4 deleted `allowedMcpServers`, saying it does not exist. Batch 21.1 restored it
but asserted two things about it:

> "This key doesn't restrict servers declared in a project `.mcp.json` file; use
> `disabledMcpjsonServers` for that."
>
> "its type is an array of strings"

**Neither sentence is in the documentation.** I checked the page itself this time,
in the browser, rather than a summary of it:

```
hasDoesntRestrict : false
typeLine          : "**Type**: array of objects, each with exactly one key.
                     Use `serverName`, a string limited to letters, numbers,
                     hyphens, and underscores; `serverCommand`, an arr…"
example           : { "serverName": "github" }
```

What the reference actually says: *"Allowlist the MCP servers people can add. Claude
Code blocks any server that doesn't match an entry **wherever it's defined**, including
plugin servers, servers a user passes with `--mcp-config`, and servers from claude.ai."*
Built-in, CLI-configured and Claude Tag servers are exempt; in-process `type: "sdk"`
servers are exempt from both lists.

So `allowedMcpServers` **does** block an unapproved server declared in `.mcp.json`.
**Run 1's variant B was right, and batch 21.1's correction of it was wrong.** I told a
tester their measurement had a confound, on the strength of a quotation that does not
exist, and wrote that into the lab, the checker docstring and the run brief.

The mechanism worth remembering: batch 20.4 read the docs through a summarising fetch
and got a key deleted; batch 21.1 read them the same way and got a fabricated sentence
plus a wrong type. Twice is a pattern. **Settle a key name or a value shape by looking
at the page, not at something that read the page for you.** Run 2's tester checked both
and caught it; the run 1 tester had the behaviour right from a live run on the first
pass.

### 22.2 FIXED: that error had already become a new false pass worth 8 points

Because batch 21 believed the type was strings, the checker accepted
`allowedMcpServers: ["docs-search", "ticket-bridge"]` and scored it **8/8, 60/60**. At
runtime that shape matches nothing, so it blocks **every** MCP server including the two
approved ones — the tester's session started with `mcp_servers: []`. A student could
score full marks on a configuration that silently broke their whole toolchain.

The checker now takes the documented shapes:

- `allowedMcpServers` / `deniedMcpServers` — arrays of single-key objects. A bare string
  is rejected with the reason spelled out, rather than scored.
- `enabledMcpjsonServers` / `disabledMcpjsonServers` — plain names.
- A well-formed allowlist naming only approved servers now **counts as enforcement**,
  so leaving `shadow-sync` declared behind a correct allowlist scores 60/60. That also
  retires the misleading `still running` message run 2 flagged: the server is blocked,
  and the checker no longer says otherwise.

Tested across every shape. Objects + still declared 60/60; `disabledMcpjsonServers`
60/60; delete-from-`.mcp.json` 60/60; **strings 52/60 with the shape explained**;
pre-approval with the server declared 55/60; blanket left on 55/60; unhardened starter
still **0/60**.

### 22.3 FIXED: Step 3's table carried the same wrong claim

Row 4 said `allowedMcpServers` "does **not** restrict `.mcp.json`". It now says it
blocks any non-matching server wherever it is defined, the table gained a **value shape**
column so the object form is visible before a student writes it, and there is a pitfall
note for the failure that is otherwise invisible — a string list that starts a session
with no MCP servers at all.

### 22.4 FIXED: Lab 5's C4 collided with its own Checkpoint

Batch 21.4 gave `cred-101` a real one-year lifetime. But the clean `cred-102` has the
same one-year lifetime, so "replace the long-lived token" became "replace a long-lived
token with another long-lived token" — which the Checkpoint explicitly forbids. The
rubric also said "an expiry fourteen months out … owner left four months ago"; measured
from the 2026-10-12 audit date it is about **3.7 months** and **3.5 months**. I had
computed from the creation date.

C4 is now framed as **ownership and rotation**, which is what actually separates it from
the clean credential: nobody owns `cred-101` and nobody has ever rotated it. The pitfall
and Checkpoint rows now say a replacement with the same lifetime is fine when it names
an owner and a rotation date, and the lab says outright that the clean credential shares
the lifetime so lifetime is not the tell.

### 22.5 FIXED: the attack script read as a failure under fallback scoring

With no sandbox the script printed `ATTACK SCORE: 10 / 40` and stopped, which looks like
a near-total failure for a student whose configuration is correct. It now adds, when
attacks 1–3 were not blocked, that this is the expected result on a machine without the
sandbox and prints the fallback total out of 25. `tools/mcp_stub.py`, which `.mcp.json`
points at, was missing from the Prerequisites list and is now there.

### 22.6 What held

| Fix | Held |
|---|---|
| 21.3 Lab 3 Step 6 terminal fallback | **Yes** — attack table produced with no deviation; 60 + 15 + 10 = 85 |
| 21.2 Step 3 scoring split | **Yes in the checker** — wrong model 55/60, starter 0/60, hardened 60/60 |
| 21.6 Lab 4 `--allowedTools`, 04-as-strongest, `tool_result`, trust hint | **Yes, all four** |
| 21.5 Lab 2 separator normalisation | **Yes** — `api_key` / `oauth_token` → 100/100 |
| 21.5 Lab 2 "at least three" | **Yes** — lab and checker agree |
| 21.4 Lab 5 scenario data | **Yes**, with the C4 side effect above |
| 21.7 `provision-rvc.sh` PATH check | **Yes** — `[ OK ] claude resolves on PATH at /usr/bin/claude`, OK 21 FAIL 4, all four expected |

### 22.7 Settled: `allowUnsandboxedCommands` does stop the retry

Run 1 could not isolate this. Run 2 did, as far as is possible without a working sandbox:
with `true`, the model's `dangerouslyDisableSandbox: true` retry left the sandbox and
reached the permission layer (`Error: Run outside of the sandbox`); with `false`, the
same retry was kept inside and failed with the same seccomp error. Not yet tested on a
machine where the sandbox works.

### 22.8 The AppArmor attempt did not happen, and not because of the machine

`sudo` is passwordless and the brief authorised it, but the tester's own permission layer
refused `./sandbox-apparmor.sh --try claude-profile` ("judged this action dangerous") and
refused `provision-rvc.sh --install` as "Code from External". The tester did not work
around either refusal and recorded the pre-state, so nothing needs reverting.

**This needs a human at a terminal**, or a session granted a Bash permission rule for
`./sandbox-apparmor.sh`:

```bash
cd testing
./sandbox-apparmor.sh --try claude-profile  2>&1 | tee ~/try-claude-profile.txt
./sandbox-apparmor.sh --revert
./sandbox-apparmor.sh --try disable-profile 2>&1 | tee ~/try-disable-profile.txt
./sandbox-apparmor.sh --revert
```

The tester's prediction, unverified: `claude-profile` puts the `claude` binary in an
unconfined profile with `userns`, but the denial is raised in `unpriv_bwrap`, which
`/usr/bin/bwrap` transitions into — so the child may still transition and only
`disable-profile` will pass. That matches what batch 10.6 found for `local-override`.

### 22.9 Still open after run 2

- **The sandbox.** Unchanged, and now the only item on the critical path for a Lab 3
  score above 85.
- **Student packs** (carried from 21.9). Lab 4 tells students to run `check_record.py`
  while `demo-files/README.md` says to strip it. Needs a `make-student-pack` step and a
  decision.
- **Lab 2 Track B's `com.anthropic.claudefordesktop`** (carried). Confirm the deck
  supplies it.
- **Lab 2 smaller:** the new "ids must show the pattern" sentence is guidance, not
  enforced by the checker, and A4's sequence is still undefined in the Facilitator Notes.
- **Lab 5 smaller:** the rubric says "every credential involved" where the Checkpoint
  says "every credential in the inventory", and the rotation-state representation is
  asymmetric.
- **Lab 4 smaller:** one line on non-payload permission denials.

---

## Batch 23 — the sandbox question is answered (2026-11-11, operator-run)

**`disable-profile` works. `claude-profile` does not. The investigation is over and
what remains is a decision.**

The operator ran the attempts by hand, after two test sessions were refused by their own
tool-permission layers (batch 22.8). Verbatim:

```
== Reverting every change this script makes
  [ OK ] removed /etc/apparmor.d/claude-code-sandbox
  [ OK ] reverted. A reboot guarantees a clean state.

== Before: probe with the sandbox forced on
      apply-seccomp: write /proc/self/setgroups (nested userns is capability-restricted;
      caller must provide CAP_SYS_ADMIN): Permission denied
  result: PROBE_FAIL

== Applying option: disable-profile
  [ OK ] disabled bwrap-userns-restrict
  [INFO] this removes the restriction for everything on the image, not just Claude Code

== After: the same probe
  result: PROBE_PASS

== Verdict
  [ OK ] option 'disable-profile' WORKS. The sandbox starts.

== Reverting every change this script makes
  [ OK ] re-enabled bwrap-userns-restrict
  [ OK ] reverted. A reboot guarantees a clean state.
```

The first block is the `claude-profile` attempt being reverted —
`/etc/apparmor.d/claude-code-sandbox` is the file that option writes, so it had been
applied. **Its own verdict line was not captured**; it was not adopted, and the
structural reason it cannot work is the one run 2's tester predicted: the denial is
raised in `unpriv_bwrap`, which `/usr/bin/bwrap` transitions *into*, so confining the
`claude` binary does not change what its child transitions to. If anyone wants that on
the record properly, `~/try-claude-profile.txt` on the VM has the verdict line.

**The image is unmodified.** Both attempts were reverted and the final probe state is
the original one.

### What changed in the repo

`IMAGE-REQUIREMENTS.md` item 1 is rewritten. It no longer asks for "an AppArmor change"
from "someone who knows AppArmor on Ubuntu 26.04" — that work is done. It now states the
one change that works, that it is image-wide, and what it costs to decline:

| | With the profile disabled | As the image ships today |
|---|---|---|
| Course 4 Lab 3 | 100 | 85 (fallback scoring) |
| Course 4 Lab 4 config 03 | exercisable | cannot be exercised; 04 is "strongest" |
| Course 2 Lab 3 | full | fallback added in batch 14 |

Nothing is blocked. Item 1 moved from **blocker** to **ceiling**, and from *Scriptable:
No* to *Decision*.

`sandbox-apparmor.sh`'s header now records all three outcomes so nobody re-runs a
settled experiment, and `COURSE-4-RUN.md` section 2 tells the next session the sandbox is
closed, to take the fallback paths, and to spend none of its run on it.

### The decision, stated plainly for whoever owns the image

> Disable the `bwrap-userns-restrict` AppArmor profile on the classroom image.

It lifts the unprivileged-user-namespace restriction for everything on the machine, not
just Claude Code. That is a genuine reduction in the image's security posture and it is
not ours to make. Two things worth weighing: these are short-lived single-purpose
classroom VMs, and the mechanism being unblocked is the same one the course spends
Course 4 teaching students to rely on — a sandbox the classroom image cannot run is an
awkward thing to teach. Against that, "we turned off an AppArmor profile image-wide to
make a lab score 100 instead of 85" is a thin justification on its own, and the labs
already run honestly without it.

If the answer is no, nothing further is needed: the fallback scoring is in place, run 2
confirmed a student reaches 85 with no improvisation, and the labs say so in their own
text rather than pretending the sandbox worked.

---

## Batch 24 — students switch the sandbox on themselves, so the image change is optional

Batch 23 settled that disabling `bwrap-userns-restrict` is the only thing that works, and
left it as a decision for whoever owns the image. That left Lab 3 capped at 85 and Lab 4's
configuration 03 unexercisable for however long the decision took.

It does not need to wait. The students have passwordless `sudo` on the VM, so they can
make the change themselves for the length of the lab and put it back afterwards.

### `demo-files/lab3-harden/classroom-sandbox.sh`

```
./classroom-sandbox.sh --check     is the sandbox blocked? (changes nothing, no sudo)
./classroom-sandbox.sh --on        let the sandbox start (needs sudo)
./classroom-sandbox.sh --off       put the machine back as you found it
```

It mirrors exactly what the operator ran: symlink the profile into
`/etc/apparmor.d/disable/`, `apparmor_parser -R` to unload it, and the reverse to restore
it. If `apparmor_parser` refuses, it removes the symlink again so the machine is never
left half-changed. It declines politely on macOS (Seatbelt needs no change) and on a
machine where the profile is absent, and `--on` / `--off` are both idempotent.

### Teaching the trade rather than hiding it

The obvious way to ship this is a one-line "run this to fix the sandbox". That would be a
bad lesson in a course about enterprise security controls, because the command is not a
fix — it is a trade, and a bad one outside a classroom.

So Lab 3 gains a **Step 0** that puts the decision in front of the student before they
run anything. It says plainly that `--on` does *not* grant the permission to Claude Code:
the profile is machine-wide, so every process on the VM gains what it lifts. It says the
narrower options were tried and cannot work, and why — the denial is raised inside
`unpriv_bwrap`, which `/usr/bin/bwrap` transitions into, so confining the caller changes
nothing about its child. It offers doing nothing as a legitimate choice with the 85
ceiling attached. And Step 7 now asks a student who ran `--on` to write one line on what
they would have needed before doing that on a machine that mattered.

That turns the image's limitation into the lab's first real security decision, which is
closer to the point of Course 4 than a clean sandbox would have been.

Lab 4's configuration 03 note points at the same script, and asks students to record
which path they took — "the control was not exercised" and "the control held" are
different results and should not be logged the same way.

### What this changes about the image ask

`IMAGE-REQUIREMENTS.md` item 1 moves from **Decision** to **Optional**:

| | Image disables it | Student runs `--on` | Nobody does anything |
|---|---|---|---|
| Course 4 Lab 3 | 100 | 100 | 85 (fallback) |
| Course 4 Lab 4 config 03 | exercisable | exercisable | not exercisable |
| Course 2 Lab 3 | full | full | fallback from batch 14 |

The middle column depends on `sudo`, which the current image grants passwordless. **If a
future image removes `sudo`, the student route closes** and the image change becomes the
only way to reach 100. That dependency is recorded in item 1.

### Untested, and it is the next run's first job

The script has been syntax-checked and its usage and non-Linux paths exercised, but
**nothing has run `--on` on the VM**. `sandbox-apparmor.sh --try disable-profile` did the
equivalent by hand and worked, and this script performs the same operations, but that is
reasoning rather than evidence.

Run 3's brief now opens on it: `--check`, `--on`, confirm the probe flips to PASS, run
Lab 3 and Lab 4 **with a working sandbox for the first time**, then `--off` and confirm
the machine is back. Two things that run should settle and no run has yet:

- Whether `sandbox.allowUnsandboxedCommands: false` stops a retry on a sandbox that
  actually works. Run 2 settled it only for a sandbox that fails at runtime.
- Whether Lab 3 scores 100 cleanly, and whether attacks 1–3 are genuinely blocked rather
  than merely predicted blocked.

One real risk: both previous runs had their own tool-permission layer refuse this class of
command. The brief tells run 3 to log the refusal and fall back rather than work around
it, because "a session cannot reach the student path" is itself something the operator
needs to know — a student with a terminal is not a session with a permission layer.

---

## Batch 25 — Course 4 run 3 (2026-11-11, at 43a70ab): batch 22 held, verified at runtime

**Lab 3 PASS WITH NOTES 85/85, Lab 2 100, Lab 1 100, Lab 4 pass with notes, Lab 5
reviewed.** Run 3 tested at `43a70ab`, so it predates batches 23 and 24 — the student
sandbox script has still never been run on the VM.

Every batch 22 fix held, and this run checked them **at runtime** rather than only in the
checker, which is what the previous two could not do:

| Shape | Checker | Runtime |
|---|---|---|
| `allowedMcpServers` as objects, `shadow-sync` still declared | 60/60 | `shadow-sync` blocked, approved two connected |
| `allowedMcpServers` as bare strings | 52/60, shape explained | `mcp_servers: []` — every server blocked |
| pre-approval only, `shadow-sync` declared | 55/60 | `shadow-sync` connects, so the 5 lost points are deserved |
| unhardened starter | 0/60 | all four predictions "will succeed" |

The tester also checked the Step 3 table against the raw `settings-reference.md`:
*"wherever it's defined" and the one-key-object type are there. The batch 21.1 sentence
appears 0 times.* That independently confirms batch 22.1.

### 25.1 MY BUG, on the operator's machine: `--revert` reported a revert it had not done

The worst finding in the run, because it left state behind on a live VM.
`sandbox-apparmor.sh --revert` deleted `/etc/apparmor.d/claude-code-sandbox` and reloaded
AppArmor — but **a reload does not unload a profile whose file is already gone.**
`claude-code-sandbox (unconfined)` stayed loaded in the kernel and attached to every new
`/usr/bin/claude` for hours after the script printed `[ OK ] reverted`.

Operator fix, given to the user immediately:

```bash
echo -n claude-code-sandbox | sudo tee /sys/kernel/security/apparmor/.remove
```

Script fix: the revert branch now unloads with `apparmor_parser -R` **before** `rm -f`,
falls back to the `.remove` interface, then checks `aa-status` and says
`revert INCOMPLETE` with the removal command if the profile is still there. A script that
reports success it has not verified is the same failure mode as a grader that passes a
configuration it has not checked.

Also confirmed by the operator's own run, with the verdict lines run 2's output lacked:
**`claude-profile`: FAIL** — the denial is still raised in `profile="unpriv_bwrap"`,
exactly as predicted. **`disable-profile`: PASS.**

### 25.2 FIXED: the attack script told an unhardened student they had 15/25

Batch 22.5's fallback line hard-coded *"attacks 1-3 predicted 5 each = 15"* and called it
"the expected result". But attacks 1–3 score 5 each **only where `check_settings.py`
predicts them blocked**, which for an unhardened config is none of them. So the
unhardened starter printed `15 / 25` next to a Part A of 0/60.

I fixed a line that under-reported by adding one that over-reports. The script no longer
computes a total: it states what the fallback is, prints attack 4's live score, and tells
the student to read the checker's PREDICTED block and add them up — *"do not assume 15."*

### 25.3 FIXED: the lab still demanded "no longer declared" where the checker said "cannot start"

Batch 22 taught the checker that a blocking allowlist is enforcement, but three places
still told students the unapproved server must be **removed from `.mcp.json`**: Step 3's
acceptance criterion, the Checkpoint, and the Troubleshooting row (which also omitted
`allowedMcpServers` from the list of things that stop a server). A student using a correct
allowlist scored 60/60 while the lab text said they had not met the criterion.

All three now say the server **cannot start** — removed, rejected, or shut out by an
allowlist — and Step 3's prose no longer claims only one key blocks.

### 25.4 FIXED: the malformed-shape message was wrong for two of three shapes

It printed "blocks EVERY server, approved included" for any malformed entry. True for an
allowlist made only of strings. **False** for `deniedMcpServers` as strings, which matches
nothing and so blocks nothing — run 3 confirmed `shadow-sync` still connects — and false
for a mixed allowlist, where only the string entry is ignored. The scores were right; the
explanation was wrong. The message is now per-list and says what each shape actually does.

That also retires the `still running` line properly: it now prints only when it is true,
instead of alongside `MALFORMED`.

### 25.5 FIXED: C4 rested on "never rotated" with no policy to measure against

Batch 22.4 reframed C4 as ownership and rotation. But nothing in the tree said what the
rotation expectation was, so "never rotated" was an assertion a student could not check.

`harbor-org/README.md` now carries Harbor's credential policy: named owner, re-issue to a
team when the owner leaves, rotate at least every **180 days**, CI secrets scoped to one
repository.

180 is deliberate. Against the 2026-10-12 audit date, `cred-101` is 252 days since
creation and never rotated — the only breach, which is exactly C4. `cred-102` is 53 days
and `cred-103` is 163, both compliant. **A 90-day policy would have made `cred-103` a real
finding and destroyed it as a decoy**, which is the kind of second-order damage this
sequence of batches keeps producing. The arithmetic is recorded in the rubric so the next
person changing a date can see what it would break.

Smaller, same area: the rubric no longer quotes the superseded Checkpoint wording, and the
student-facing callout says "whether anyone rotates it" rather than "whether it expires".

### 25.6 Smaller

- Lab 3's Facilitator "Needs rehearsal" list still named the MCP setting names as
  unconfirmed. They are confirmed and runtime-verified now; the list says so and keeps
  only what is genuinely unrehearsed (live sandbox behaviour, `sandbox.filesystem`
  nesting, deny-rule syntax, loopback for attack 2).
- The run brief named result files `-run2.md`; it now says `-run<N>.md`.

### 25.7 Still open

- **The sandbox.** `disable-profile` is the only thing that works. Batch 24 lets students
  do it themselves; **that script has still never been run on the VM** and is run 4's
  first job.
- **Student packs** and **Lab 2 Track B's `com.anthropic.claudefordesktop`** (carried from
  21.9, now three runs old). Both need a decision, not a test.
- **Lab 2:** the "ids must show the pattern" sentence is guidance the checker does not
  enforce; A4's sequence is still undefined in the Facilitator Notes.
- **Lab 4:** no rule for whether "[passage omitted]" counts as `model_flagged`. Run 3 saw
  both issue-vector runs name the injection where run 1 saw one and run 2 saw none — on
  the same model and version. Flagging is not stable across runs, which is worth saying
  in the lab rather than leaving students to wonder.
- **Lab 5:** "every credential involved" vs "every credential in the inventory" is still
  unresolved between rubric and Checkpoint.

---

## Batch 26 — four decisions taken (2026-11-11)

Four items had been carried for up to three runs because they needed a person, not a
test. Taken now, with the reasoning, so they stop reappearing as findings.

### 26.1 `check_record.py` is a student file

`demo-files/README.md` said it "names planted items" and must be withheld, while Lab 4
Part 4 told students to run it. The README was simply wrong about that file: it scores
completeness (25), consistency (15) and evidence fields (25) — filled columns, legal
values, a defense named where `stopped_by` requires one. It contains no planted item and
there is no right answer for it to leak, because the result is whatever the model did.

The withheld list is now explicit and justified per file:

| Withheld | Why |
|---|---|
| `lab1-identity/check_lab1.py` | names all five planted defects |
| `lab2-compliance/check_lab2.py` | names the four anomalies and their event ids |
| `lab1-identity/facilitator/`, `lab2-compliance/facilitator/`, `lab5-audit/facilitator/` | scorecard, export generator, C1–C5 rubric |

| Shipped | Why |
|---|---|
| `lab3-harden/check_settings.py` | scores a configuration against stated criteria; Step 5 says to run it repeatedly |
| `lab3-harden/classroom-sandbox.sh` | Lab 3 Step 0 |
| `lab4-injection/check_record.py` | completeness and consistency only |

`demo-files/make-student-pack.sh` builds the pack: `--list` shows what would go, and a
build refuses to finish if anything named `check_lab*.py` or `facilitator` survives the
prune. A file not on the withheld list ships, so the failsafe catches the case where
someone adds a checker and forgets the list. Tested: exactly the three intended student
files remain.

### 26.2 `model_flagged` requires the model to NAME the injection

Run 3 saw the model elide the payload as "[passage omitted]" without saying why. All
three testers recorded that as `no` on their own judgement; the lab never said.

It is `no`. Silently doing the right thing is not flagging, and an unexplained elision
shows the model noticed something while giving the student nothing a control could be
built on. The lab now says this, and says why it matters: "the model refused" and "the
model said nothing" call for different responses.

The column keeps two values. A third (`elided`) would be more faithful but changes
`record_sheet.csv` and `check_record.py`'s consistency rules for a distinction the
written account already carries.

### 26.3 Lab 1 and Lab 5 keep their durations until a real pilot

Every run has called 90 minutes for Lab 1's offline path and 60 for Lab 5 generous, on
the strength of finishing them in about three minutes. That is agent time and it is a
poor proxy: the sessions skip the reading, the deliberation and the writing that are most
of a student's work. Flagged for the first pilot to measure with a stopwatch and a human.
No change.

### 26.4 The operator switches the sandbox on; the session uses it

Three runs in a row had their own tool-permission layer refuse `--try`, `--install` or
`--on`. Rather than fight it a fourth time, Lab 3's Step 0 is run by the operator before
the session starts and reverted after. The brief's section 2 now tells the session to
*detect* which state it is in and report it, and forbids it from changing the machine.

This also means the student path in `classroom-sandbox.sh` still has not been exercised
by a session — only by a person, which is who it is for. Worth remembering if that script
is ever expected to work from inside an agent.
