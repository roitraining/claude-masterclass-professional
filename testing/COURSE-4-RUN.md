# Course 4 Test Run — RVC new image, run 2 (retest, 2026-11-11)

**This is your brief. You are a Claude Code session inside the ROI Virtual Classroom
(RVC) VM.**

Your job is to test the **Course 4** labs as a student would, and write down what
actually happens. You are testing the labs, not completing a course — nobody is grading
your lab answers. **The deliverable is the log.**

**This is a retest.** Run 1 happened earlier today and found nine defects; eight are
fixed on this branch. Your job is to confirm the fixes hold, catch anything they broke,
and settle the two open questions in section 2. Run 1's results are the baseline:
Lab 1 100/100, Lab 2 99/100, Lab 3 **FAIL**, Lab 4 pass with notes, Lab 5 reviewed.

---

## 0. Read first

- **[`HANDOFF.md`](HANDOFF.md)** — the rules for this run. Read all of it. It governs
  everything below.
- **[`IMAGE-REQUIREMENTS.md`](IMAGE-REQUIREMENTS.md)** — what the image is still missing.
- **[`FIXES-APPLIED.md`](FIXES-APPLIED.md) batch 21** — exactly what changed since run 1
  and why. Read this before you touch Lab 3 or Lab 5; the scenario data moved.
- **[`../course-4-enterprise-deployment-professional/labs/README.md`](../course-4-enterprise-deployment-professional/labs/README.md)**
  — the course preamble.

In every lab, `$FILES` means `course-4-enterprise-deployment-professional/demo-files/`.

---

## 1. Phase 0 — the image

```bash
cd testing
./provision-rvc.sh --check   2>&1 | tee ~/before.txt
./provision-rvc.sh --install 2>&1 | tee ~/install.txt
./provision-rvc.sh --check   2>&1 | tee ~/after.txt
```

`--check` changes nothing and needs no sudo. Write `testing/results/00-setup.md` with
`claude --version`, `claude auth status` (which tier?), whether you have `sudo`, the
section 10 version block from `after.txt`, and the sandbox probe's verdict verbatim.

Two things run 1 left open here:

- **`--install` was never run** — the tester's tool-permission layer refused it. If yours
  refuses too, **say so in the log rather than skipping it silently**, and record what
  `--check` says is still missing.
- **The `$HOME/.local/bin` FAIL was ours, not the image's.** This image ships the apt
  package at `/usr/bin/claude`. The check was rewritten to assert that `claude` resolves
  at all. Confirm it no longer reports a false FAIL. Run 1 saw `OK 20 FAIL 5`; three of
  those five were real (all sandbox), one was the API key (expected), one was ours.

---

## 2. The AppArmor attempt — do this before the labs

The sandbox has never started on this image. `local-override` was tried on 2026-11-04
and cannot work: `unpriv_bwrap` carries `audit deny capability`, and an AppArmor deny
beats any allow. **Do not retry it.** The two remaining options are untested and you are
authorised to try them.

```bash
sudo -v
./sandbox-apparmor.sh --try claude-profile  2>&1 | tee ~/try-claude-profile.txt
# if the verdict says it did NOT work:
./sandbox-apparmor.sh --revert
./sandbox-apparmor.sh --try disable-profile 2>&1 | tee ~/try-disable-profile.txt
```

The script probes with the sandbox forced on before and after each attempt and decides
from the Bash **tool result**, not from stdout text — it has given a false pass twice
before by reading strings, so trust its verdict line and paste it verbatim.

- `claude-profile` is the narrow option and is worth more than IMAGE-REQUIREMENTS
  suggests: the apt binary at `/usr/bin/claude` is root-owned and **stable**, so the
  "auto-update moves the path" caveat does not apply to this image.
- `disable-profile` removes the restriction image-wide. A PASS there is **evidence for a
  change request, not a fix to keep.**

**When you are finished either way, run `./sandbox-apparmor.sh --revert` and confirm
with a final `--try`-free probe that the image is back as you found it.** Record what you
applied, what the verdict was, and that you reverted. If one of them works, paste the
exact change the script prints for the image team.

Then say in `00-setup.md` whether the rest of your run had a working sandbox or not. It
changes what Lab 3 and Lab 4 can show.

---

## 3. Test order

| # | Lab | Stated | Run 1 |
|---|---|---|---|
| 1 | **Lab 3** — Harden a Sample Repository | 90 min | FAIL |
| 2 | **Lab 4** — Prompt Injection Detection | 75 min | pass with notes |
| 3 | **Lab 2** — Pull Compliance Data, Set a Control | 90 min | 99/100 |
| 4 | **Lab 5** — Credential Audit (take-home) | 60 min | reviewed |
| 5 | **Lab 1** — Configure Identity and Access | 90 min | 100/100 |

Lab 3 first because it was the FAIL and it took the largest change. Lab 1 last because
nothing in it changed — re-run it only to confirm it still scores 100/100.

Each lab opens with `## Prerequisites` and ends with a `## Part N: Checkpoint`. Those two
sections are your test plan.

---

## 4. What changed, and what to check

### Lab 3 — rewritten Step 3 and Step 6

**Step 3 no longer asks you to guess a key name.** It now gives a table of the four
relevant MCP settings and asks which of them is a control. The 8 MCP points split into
5 for the enforcement (blanket approval off, no unapproved server left running) and 3 for
naming the approved servers with any documented key. Check:

- Does the table match the current settings reference?
- Is it now clear from the lab alone which key is a control and which is pre-approval?
  That was the thing a student could get wrong while reasoning correctly.
- Does `check_settings.py` still score the **unhardened starter 0 of 60**, with every
  planted trap detected and all four predictions reading "will succeed"?
- Harden it properly and confirm **60/60**. Then try the wrong mental model on purpose —
  name the approved servers but leave `shadow-sync` declared — and confirm it loses the
  5 enforcement points and keeps the 3.

**Step 6 now has a documented fallback.** Run 1's FAIL was that a correctly hardened
config refuses *every* Bash call on this image, so attack 4 could not be scored live from
inside a session, and the lab never said where else to run it. Step 6 now says to run
`python3 attack_simulation.py` in your own terminal and explains that this means your
config is right. Confirm a student following the lab as written can now produce the full
attack table and reach the 85 ceiling — **without any deviation of their own.**

Also still open from run 1: **if the sandbox starts** after section 2, does
`sandbox.allowUnsandboxedCommands: false` actually stop an unsandboxed retry? Run 1 got
partial evidence only (the model declined to retry when the sandbox failed at runtime).
Isolating this is worth the run.

### Lab 4 — three notes added

- The tool-result vector under `-p` needs
  `--allowedTools "Bash(python3 tools/ticket_lookup.py 17)"`, which the lab now says.
  Run 1 had to improvise this; confirm the instruction is enough.
- If the sandbox cannot start, the lab now tells you to pick `04_narrowed_tools` as your
  strongest defense and say why 03 was not testable.
- The prose vector name now matches the CSV's `tool_result`, and the trust hint says that
  `-p` ignores the project file's `permissions.allow` in an untrusted folder.

Record the permission mode you actually ran in. Run 1 saw `default` in all eight runs,
and all eight were stopped by the model with no canary fired, at about $0.93. If yours
diverges from that, say so — it is a model-behaviour data point, not a defect.

### Lab 2 — two scoring fixes

- `auth_methods_covered: ["web","desktop","api_key","oauth_token"]` cost a point in run 1.
  The matcher now normalises `_` and `-`. Write it in snake_case deliberately and confirm
  you reach **100/100**.
- The lab asked for "every event in the sequence" while the checker wanted three. It now
  says **at least three**. Confirm the lab and the checker agree.

### Lab 5 — the scenario data moved

The "clean" repository was not clean: all three CI workflows passed a `setup-token`
credential as `ANTHROPIC_API_KEY`, which is the Console API key variable. They now use
`CLAUDE_CODE_OAUTH_TOKEN`. And `setup-token` is a documented **one-year** token, so
`cred-101` (which had `expires: none`) is now created 2026-02-02 and expires 2027-02-02,
and `cred-102` expires 2027-08-20. Check:

- Are all five planted issues (C1–C5) still findable, and is **C4 still a real defect**?
  It should now read as person-owned, never rotated, owner departed 2026-06-30, used
  2026-10-09 — rather than "a credential with no expiry".
- Is `payments-gateway` now genuinely clean, such that a careful student finds nothing
  wrong with it?
- Is `cred-103` (2026-11-02) still the only near-term expiry, so it still works as the
  decoy the Facilitator Notes describe?
- Do the rubric and the Facilitator Notes still agree with each other and with the lab?

### Lab 1 — unchanged

Nothing was touched. Re-run the offline path and confirm it still scores 100/100. If it
does, a one-paragraph result file is enough.

### Paths and cost

Take the **OFFLINE path** for Labs 1 and 2 unless an instructor has provisioned a sandbox
organization — say which you took. Course 4 needs no Anthropic API key; if
`ANTHROPIC_API_KEY` is set, note it, because it outranks subscription login.

---

## 5. Hard rules

- **The environment is ground truth. The lab text is the thing under test.**
- **Do not edit any lab, demo, or `SETUP-CLAUDE-CODE.md`.** Report it; a human decides the
  fix. Project files a lab tells you to create go in a scratch directory outside the repo.
- **If you deviated from the written steps to proceed, that is a FAIL or a BLOCKED**, with
  the deviation recorded. Never PASS because you found a way to make it work that the lab
  never told the student to do. This matters most for Lab 3 Step 6 — the whole point of
  the fix is that no deviation should now be needed.
- **Never raise a spend cap.** If a lab stops because it hit one, that is a result.
- **Never push to any remote.** No `git push`, no PR, no remote of any kind.
- **Never write a credential into a result file** — replace it with `REDACTED`.
- **Section 2 is the only place you may change this machine**, and you revert it.
- **Do not loop on a failing command.** A clear blocker is a useful result; a fabricated
  pass is worse than no result.

---

## 6. How to log

Copy `testing/results/_TEMPLATE.md` to
`testing/results/course-4-enterprise-deployment-professional-<lab-file-slug>-run2.md`.

Verdicts, and only these: `PASS`, `PASS WITH NOTES`, `FAIL`, `BLOCKED`, `REVIEWED`,
`NOT TESTED`.

For every lab, give run 1's verdict and yours, and say which of batch 21's fixes you
exercised. Also record:

- **Verbatim output for every failure** — the actual command and the actual error. A
  reviewer outside the VM cannot reproduce it.
- **Wall-clock time versus the stated duration**, and say plainly that your time is agent
  time, not student time, if that is what it is.
- **Anything a student would ask that the lab does not answer.**

**Save after each lab, not at the end.** Keep `testing/results/00-INDEX-run2.md` current:

```markdown
| Lab | Run 1 | Run 2 | Tested | Result file |
|---|---|---|---|---|
| Course 4 Lab 3 | FAIL | PASS WITH NOTES | 2026-11-11 18:40 | ...-lab-3-...-run2.md |
```

Finish with `testing/results/99-summary-run2.md`: the verdict table, which fixes held and
which did not, the AppArmor outcome, the blockers in the order they should be fixed, and
anything about this image the setup guide should say and does not.

Write **only** inside `testing/results/`. The operator collects that folder from the VM.
