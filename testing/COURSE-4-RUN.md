# Course 4 Test Run — RVC, new image (2026-11-11)

**This is your brief. You are a Claude Code session inside the ROI Virtual Classroom
(RVC) VM, on a newly built image.**

Your job is to test the **Course 4** labs as a student would, and write down what
actually happens. You are testing the labs, not completing a course — nobody is grading
your lab answers. **The deliverable is the log.**

---

## 0. Read first

- **[`HANDOFF.md`](HANDOFF.md)** — the rules for this run. Read all of it. It governs
  everything below.
- **[`IMAGE-REQUIREMENTS.md`](IMAGE-REQUIREMENTS.md)** — what the previous image was
  missing, and why.
- **[`../course-4-enterprise-deployment-professional/labs/README.md`](../course-4-enterprise-deployment-professional/labs/README.md)**
  — the course preamble.

In every lab, `$FILES` means `course-4-enterprise-deployment-professional/demo-files/`.

---

## 1. Phase 0 — prove the image, before any lab

```bash
cd testing
./provision-rvc.sh --check   2>&1 | tee ~/before.txt
./provision-rvc.sh --install 2>&1 | tee ~/install.txt
./provision-rvc.sh --check   2>&1 | tee ~/after.txt
```

`--check` changes nothing and needs no sudo. Write `testing/results/00-setup.md` with:

1. `claude --version`
2. `claude auth status` — what account tier is the class account?
3. Do you have `sudo`?
4. Did the browser login flow complete inside the VM, or was `claude setup-token` needed?
5. The section 10 version block from `after.txt` (OS, kernel, Claude Code, venv contents).
6. **The headline question for this image: does the sandbox probe PASS?** On the previous
   image it failed with
   `apply-seccomp: write /proc/self/setgroups (nested userns is capability-restricted...)`.
   Paste the probe's verdict verbatim either way.

If the sandbox still fails, run `./sandbox-apparmor.sh --diagnose` (read-only) and paste
the output. Do **not** apply an AppArmor change without recording that you did; `--revert`
anything that does not work. `local-override` is already known to fail — do not retry it.

**If setup fails, write that log before doing anything else.** It is the most valuable
result in the run.

---

## 2. Test order

In `course-4-enterprise-deployment-professional/labs/`:

| # | Lab | Stated duration |
|---|---|---|
| 1 | **Lab 3** — Harden a Sample Repository | 90 min |
| 2 | **Lab 4** — Prompt Injection Detection | 75 min |
| 3 | **Lab 1** — Configure Identity and Access | 90 min |
| 4 | **Lab 2** — Pull Compliance Data, Set a Control | 90 min |
| 5 | **Lab 5** — Credential Audit (take-home) | 60 min |

Labs 3 and 4 go first because they are the only two that depend on the image. Find image
problems while there is still time to report them.

Each lab opens with `## Prerequisites` and ends with a `## Part N: Checkpoint`. Those two
sections are your test plan: confirm the prerequisites, run the lab, check every
Checkpoint item.

---

## 3. What to watch for, per lab

### Labs 1 and 2 — take the OFFLINE path

No sandbox Claude organization has been provisioned for you, and no Compliance API key.
Both labs are designed so the offline path is complete. **State which path you took.**
Anything touching a tenant or a shared organization is instructor-only: log it
`NOT TESTED` with the reason, do not improvise.

### Lab 3 — the ceiling moves, the lab does not get blocked

Line 153 defines fallback scoring: Part A is 60 points and works everywhere; attacks 1–3
score 5 each from the checker's *predicted* outcomes; attack 4 is always scored live.
**Maximum is 85 without a working sandbox, and that is a known platform limit, not a
FAIL.**

Three specific things to answer:

- Does `check_settings.py` still score the *unhardened* starter **0 of 60**, with every
  planted trap detected and all four attack predictions reading "will succeed"?
- Step 3 was rewritten on 2026-11-11. It now names the four relevant MCP keys in a table
  and scores the *decision* — the blanket approval off and no unapproved server left
  running — separately from which key the student picks. Confirm the table matches the
  current settings reference, and that a student can tell from the lab which of the keys
  is a control. (An earlier version of this brief said `allowedMcpServers` does not exist.
  It does. What it does not do is restrict servers declared in a project `.mcp.json`;
  `disabledMcpjsonServers` is the documented key for that.)
- **If the sandbox starts on this image:** does `sandbox.allowUnsandboxedCommands: false`
  actually stop an unsandboxed retry? This has never been isolated in a run. If you can
  prove it either way, that is a result worth having.

### Lab 4 — spends tokens, needs `claude` signed in

Record the permission mode you actually ran in (`/status`, or the `permissionMode` field
of the init JSON under `-p`). Config `03_sandbox_network.json` depends on the sandbox; if
the sandbox cannot start, log that for config 03 and still run the other three. Outcomes
are model-dependent and not guaranteed — **record what happened, not what should have
happened.** The payload is a benign loopback canary; nothing leaves the machine.

### Lab 5 — paper only

Log it `REVIEWED`, not `PASS`: confirm every file it references exists, that the
acceptance criteria are answerable from the provided material, and that the Facilitator
Notes answer key is consistent with the lab's own instructions. One of the three
repositories (`payments-gateway`) is deliberately clean — reporting it as defective is
supposed to cost points.

### Cost

Course 4 needs no Anthropic API key. If `ANTHROPIC_API_KEY` is set in the environment,
note it in `00-setup.md` — it outranks subscription login and would make these labs bill
against it silently.

---

## 4. Hard rules

- **The environment is ground truth. The lab text is the thing under test.** A command
  that does not exist, a moved menu path, a version too old, a refused account tier —
  that is a defect in the lab, and you record it.
- **Do not edit any lab, demo, or `SETUP-CLAUDE-CODE.md`.** Report it; a human decides the
  fix. If a lab tells you to create project files, put them in a scratch directory
  outside the repository.
- **If you deviated from the written steps to proceed, that is a FAIL or a BLOCKED,** with
  the deviation recorded. Never PASS because you found a way to make it work that the lab
  never told the student to do.
- **Never raise a spend cap.** If a lab stops because it hit one, that is a result.
- **Never push to any remote.** No `git push`, no PR, no remote of any kind. Labs that say
  commit mean commit locally.
- **Never write a credential into a result file** — replace with `REDACTED`. Check every
  file before you save it.
- **Do not loop on a failing command.** A clear blocker is a useful result; a fabricated
  pass is worse than no result.

---

## 5. How to log

Copy `testing/results/_TEMPLATE.md` to
`testing/results/course-4-enterprise-deployment-professional-<lab-file-slug>.md`.

Verdicts, and only these: `PASS`, `PASS WITH NOTES`, `FAIL`, `BLOCKED`, `REVIEWED`,
`NOT TESTED`.

For every lab also record:

- **Verbatim output for every failure** — the actual command and the actual error, not a
  paraphrase. A reviewer outside the VM cannot reproduce it.
- **Wall-clock time versus the lab's stated duration.** These are timed classroom labs; a
  90-minute lab that takes 150 is a finding.
- **Anything a student would ask that the lab does not answer.**

**Save after each lab, not at the end.** Finish a lab, write its file, then start the
next. Keep `testing/results/00-INDEX.md` current after every lab:

```markdown
| Lab | Verdict | Tested | Result file |
|---|---|---|---|
| Course 4 Lab 3 | PASS WITH NOTES | 2026-11-11 14:20 | course-4-...-lab-3-....md |
```

When you finish, write `testing/results/99-summary.md`: the verdict table, the blockers in
the order they should be fixed, and anything about this new RVC image that the setup guide
should say and does not.

Write **only** inside `testing/results/`. The operator collects that folder from the VM —
you do not need to transmit anything.
