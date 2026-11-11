# Course 4 Test Run — RVC new image, run 3 (retest, 2026-11-11)

**This is your brief. You are a Claude Code session inside the ROI Virtual Classroom
(RVC) VM.**

Your job is to test the **Course 4** labs as a student would, and write down what
actually happens. You are testing the labs, not completing a course — nobody is grading
your lab answers. **The deliverable is the log.**

**This is the third run.** Run 2 confirmed seven of nine fixes and found that two of my
own corrections were wrong — both about `allowedMcpServers`, one of which had become a
new false pass worth 8 points. Batch 22 fixes those. Your job is to confirm batch 22
holds and check that nothing regressed. The sandbox question is closed — see section 2.

Baselines:

| Lab | Run 1 | Run 2 |
|---|---|---|
| Lab 3 | FAIL | PASS WITH NOTES (85/85 fallback, no deviation) |
| Lab 4 | PASS WITH NOTES | PASS WITH NOTES (65/65 mechanical) |
| Lab 2 | 99/100 | 100/100 |
| Lab 5 | REVIEWED | REVIEWED |
| Lab 1 | 100/100 | 100/100 |
| Phase 0 | sandbox FAIL | sandbox FAIL; AppArmor settled out-of-band on 2026-11-11 |

---

## 0. Read first

- **[`HANDOFF.md`](HANDOFF.md)** — the rules for this run. Read all of it. It governs
  everything below.
- **[`IMAGE-REQUIREMENTS.md`](IMAGE-REQUIREMENTS.md)** — what the image is still missing.
- **[`FIXES-APPLIED.md`](FIXES-APPLIED.md) batches 21 and 22** — what changed and why.
  Batch 22 is this run's target; read it before you touch Lab 3 or Lab 5.
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

Two things earlier runs left open here:

- **`--install` has never run** — refused by the tester's own tool-permission layer in
  both runs ("Code from External"). If yours refuses too, **say so in the log rather than
  skipping it silently**, and record what `--check` says is still missing.
- **The `$HOME/.local/bin` FAIL was ours.** Fixed in batch 21.7 and confirmed in run 2:
  `[ OK ] claude resolves on PATH at /usr/bin/claude`, `OK 21 FAIL 4`, all four expected
  (three sandbox, one API key). Confirm it still reads that way.

---

## 2. The sandbox — settled, do not re-attempt

**All three AppArmor options have been tested. Do not run `--try` again.** On
2026-11-11 the operator ran them by hand:

- `local-override` — cannot work (`unpriv_bwrap` carries `audit deny capability`).
- `claude-profile` — applied and reverted, not adopted. The denial is raised in
  `unpriv_bwrap`, which `/usr/bin/bwrap` transitions *into*, so confining the `claude`
  binary changes nothing.
- `disable-profile` — **works**: `PROBE_FAIL` → `PROBE_PASS`. Reverted immediately.

So the image is unchanged and **your run has no working sandbox.** That is expected, it
is not a finding, and `IMAGE-REQUIREMENTS.md` item 1 now carries the decision for the
image owner rather than an open question.

What this means for you: take the fallback paths everywhere, exactly as a student on this
image would. Lab 3's ceiling is 85 and Lab 4's config 03 cannot be exercised. Record the
probe's `PROBE_FAIL` in `00-setup.md` as confirmation, and move on — **do not spend any
of this run on the sandbox.**

---

## 3. Test order

| # | Lab | Stated | Run 2 |
|---|---|---|---|
| 1 | **Lab 3** — Harden a Sample Repository | 90 min | PASS WITH NOTES |
| 2 | **Lab 5** — Credential Audit (take-home) | 60 min | reviewed |
| 3 | **Lab 4** — Prompt Injection Detection | 75 min | pass with notes |
| 4 | **Lab 2** — Pull Compliance Data, Set a Control | 90 min | 100/100 |
| 5 | **Lab 1** — Configure Identity and Access | 90 min | 100/100 |

Lab 3 first because every batch 22 fix but one is in it. Lab 5 second because its C4 was
reframed. Labs 4, 2 and 1 are regression checks — nothing in them changed since run 2, so
confirm the run 2 scores still stand and keep those result files short.

Each lab opens with `## Prerequisites` and ends with a `## Part N: Checkpoint`. Those two
sections are your test plan.

---

## 4. What changed, and what to check

Batch 22 of `FIXES-APPLIED.md` is this run's target. Read it first.

### Lab 3 — the MCP table and checker were wrong, twice

Two earlier batches got `allowedMcpServers` wrong in opposite directions: 20.4 deleted it
as a key that "does not exist", and 21.1 restored it while asserting it "does not restrict
servers declared in a project `.mcp.json`" and takes an array of strings. **Both of those
assertions were fabricated** — neither is on the settings reference page. What the page
says is that Claude Code blocks any server that does not match an entry **wherever it is
defined**, and the type is an array of **single-key objects**, `{"serverName": "github"}`.

Check all of this against the page itself, not a summary of it:

- Does Step 3's table match the reference, including the value-shape column?
- `check_settings.py` must score the **unhardened starter 0 of 60**, with every planted
  trap detected and all four predictions reading "will succeed".
- Harden it properly → **60/60**.
- `allowedMcpServers` as **objects**, with `shadow-sync` still declared → should be
  **60/60**, because the allowlist blocks it. Confirm at runtime that `shadow-sync` does
  not connect while the two approved servers do.
- `allowedMcpServers` as **bare strings** → must **not** pass. The checker should say the
  shape is wrong. Confirm at runtime that this shape starts a session with
  `mcp_servers: []` — every server blocked, approved ones included. This was scored 8/8
  before batch 22 and is the single most important thing to re-check.
- Pre-approval only (`enabledMcpjsonServers`, `shadow-sync` still declared) → **55/60**,
  losing exactly the 5 enforcement points.

**Step 6 and the attack script.** Run 2 confirmed the terminal fallback works with no
deviation. New in batch 22: the script now prints the fallback total out of 25 when the
sandbox is down, instead of a bare `ATTACK SCORE: 10 / 40` that reads as failure. Confirm
the number it prints matches what the lab's fallback scoring says.

**Still open:** if the sandbox starts after section 2, does
`sandbox.allowUnsandboxedCommands: false` stop the retry *on a working sandbox*? Run 2
settled it as far as is possible without one — with `true` the retry left the sandbox and
hit the permission layer, with `false` it was kept inside — but not on a machine where
the sandbox works.

### Lab 5 — C4 reframed

Batch 21.4 gave `cred-101` a one-year lifetime, which collided with the Checkpoint: the
clean `cred-102` has the same lifetime, so "replace the long-lived token" became the very
thing the Checkpoint forbids. C4 is now about **ownership and rotation**. Check that C1–C5
are all still findable, that C4 reads as a real defect on those grounds, that
`payments-gateway` is still genuinely clean, and that the rubric, the Checkpoint and the
lab text agree on what a good replacement looks like.

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
- **Do not change this machine.** Section 2 is settled; there is nothing to apply or revert in this run.
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
