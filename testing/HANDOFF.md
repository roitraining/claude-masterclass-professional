# Lab Testing Handoff — ROI Virtual Classroom

**Read this first. You are starting with no prior context.**

You are a Claude Code session running inside the ROI Virtual Classroom (RVC)
virtual machine. Your job is to work through this repository's labs as a student
would, record what actually happens, and write the results to files a reviewer
outside the VM can read.

You are **testing the labs**, not completing a course. Nobody is grading your
lab output. The deliverable is the log.

---

## 1. The one rule that matters

**The environment is ground truth. The lab text is the thing under test.**

When a lab says something that the VM contradicts — a command that does not
exist, a menu path that has moved, a version that is too old, an account tier
that is refused — that is a **defect in the lab**, and you record it.

Do **not**:

- Edit a lab file to match what you found. Report it; a human decides the fix.
- Work around a blocker silently and carry on as if it passed.
- Mark something PASS because you found a way to make it work that the lab
  never told the student to do.

If you had to deviate from the written steps to proceed, that is a **FAIL** or
a **BLOCKED**, with the deviation recorded.

---

## 2. Safety constraints

These are hard limits. Do not exceed them.

- **Never write a credential into a result file.** Not an API key, not a
  token, not a password.
  If a log would contain one, replace it with `REDACTED`. Check every file you
  write before you save it.
- **Never raise a spend cap.** Several labs run model evaluations and set turn
  and budget limits (`LAB_MAX_TURNS`, `LAB_BUDGET_USD`, and caps inside the
  Gauntlet script). If a lab stops because it hit a cap, that is a result —
  log it and move on. Do not increase the cap to get further.
- **Never push to any remote.** You do not have permission to, and must not
  try. Results are local files only — see section 6. Labs that say to commit
  locally mean locally.
- **Stop and report rather than improvise** if a step would change an
  organization, a tenant, or a shared account. Those are instructor-only
  actions. Log them as NOT TESTED with the reason.

---

## 3. Where things are

```
<repo root>/
├── SETUP-CLAUDE-CODE.md           install and login instructions
├── course-1-desktop-cowork-professional/
│   ├── labs/
│   │   ├── README.md              guide preamble, prerequisites, lab index
│   │   └── lab-N-<slug>.md        one file per lab
│   ├── demos/                     one file per demo (not under test)
│   ├── demos.md                   combined demo guide (not under test)
│   └── demo-files/                the assets labs refer to as $FILES
├── course-2-claude-code-professional/
├── course-3-agent-sdk-professional/
├── course-4-enterprise-deployment-professional/
├── course-5-governance-professional/
└── testing/
    ├── HANDOFF.md                 this file
    └── results/
        ├── _TEMPLATE.md           copy this per lab
        └── <course>-<lab>.md      your logs
```

In every lab, **`$FILES` means that course's `demo-files` folder.**

Each lab opens with a `## Prerequisites` checklist and ends with a
`## Part N: Checkpoint` containing a verification checklist. Those two sections
are your test plan: confirm the prerequisites, run the lab, then check each
Checkpoint item.

---

## 4. What to test, and in what order

Start with setup, then work by risk. Highest-risk first, because a
provisioning failure found early changes everything after it.

**Phase 0 — Setup (do this first, log it)**

Follow `SETUP-CLAUDE-CODE.md` exactly as written and log every deviation.
This file has four things explicitly marked as unverified against the RVC
image. Answer them:

1. Is Claude Code already installed, and at what version?
   (`claude --version`)
2. Do you have `sudo`?
3. Does the browser login flow complete inside the VM, or is
   `claude setup-token` needed?
4. What account tier is the class account? (`claude auth status`)

Record the answers in `testing/results/00-setup.md`. **If setup fails, stop
and write that log before doing anything else** — it is the most valuable
result in the run.

**Phase 1 — Course 3, Agent SDK (5 labs).** API-key authentication, a
preflight check, and the most unresolved documentation drift in the program.
Most likely to fail.

**Phase 2 — Course 2, Claude Code (5 labs).** Needs a paid account and admin
access to a personal GitHub or GitLab project. Lab 1 is 100 minutes.

**Phase 3 — Course 4, Enterprise Deployment (5 labs).** Labs 1 and 2 each
offer a LIVE path and an OFFLINE path. **Take the OFFLINE path** unless an
instructor has provisioned a sandbox organization for you, and say which path
you took.

**Phase 4 — Course 1, Desktop (3 labs).** Needs Claude Desktop installed and
signed in to the **same account** as Claude Code, and Claude Code 2.1.269 or
later. If Claude Desktop is not on the VM, log all three as BLOCKED with that
reason and do not attempt them.

**Phase 5 — Course 5, Governance (3 labs).** Paper only — no software, account
or credential. You can assess these by reading: confirm every file the lab
references exists in `demo-files`, that the acceptance criteria are answerable
from the provided material, and that the Facilitator Notes answer key is
consistent with the lab's own instructions. Log as REVIEWED, not PASS.

---

## 5. How to log

Copy `testing/results/_TEMPLATE.md` to
`testing/results/<course-folder>-<lab-file-slug>.md` and fill it in.

Use these verdicts, and only these:

| Verdict | Means |
|---|---|
| `PASS` | Every step worked as written; every Checkpoint item satisfied |
| `PASS WITH NOTES` | Completed as written, but something is worth fixing (wording, timing, a confusing step) |
| `FAIL` | A step did not work as written, or a Checkpoint item could not be satisfied |
| `BLOCKED` | Could not start or could not continue for an environmental reason (missing software, account tier, no credential) |
| `REVIEWED` | Paper lab assessed by reading, not executed |
| `NOT TESTED` | Deliberately skipped — say why |

**Record verbatim output for every failure.** Paste the actual command and the
actual error, not a paraphrase. A reviewer outside the VM cannot reproduce it
and is relying entirely on what you captured. Redact credentials.

Also record, for every lab:

- **Wall-clock time** you took versus the lab's stated duration. These are
  timed classroom labs; if a 45-minute lab takes 90, that is a finding.
- **Anything a student would ask** that the lab does not answer.

---

## 6. Recording results — local files only

**You do not have permission to push to GitHub. Do not try.** No `git push`,
no pull request, no remote of any kind. Everything you produce stays on this
VM as files.

Write each result to:

```
testing/results/<course-folder>-<lab-file-slug>.md
```

**Save after each lab, not at the end.** If the VM dies or the session ends,
anything you have not written to disk is gone. Finish a lab, write its file,
then start the next one.

Keep a running index at `testing/results/00-INDEX.md` and update it after every
lab, so the state of the run is readable from one file:

```markdown
| Lab | Verdict | Tested | Result file |
|---|---|---|---|
| Course 3 Lab 1 | FAIL | 2026-11-03 14:20 | course-3-...-lab-1-....md |
```

Before you write anything, check it for credentials — API keys, tokens,
passwords — and replace them with `REDACTED`. These files get read and shared
outside the VM.

Write **only** inside `testing/results/`. Do not edit any lab, demo, or
`SETUP-CLAUDE-CODE.md`. If a lab told you to create project files, put them in
a scratch directory outside this repository.

To hand the results back, the operator collects the `testing/results/` folder
from the VM. You do not need to transmit anything.

---

## 7. When you finish, or get stuck

Write `testing/results/99-summary.md` with:

- A table of every lab and its verdict (the same table as `00-INDEX.md`)
- The blockers, in the order they should be fixed
- Anything about the RVC image itself that the setup guide should say and
  does not

If you hit something you cannot resolve — ambiguous instructions, a step that
needs an account you do not have, a failure you cannot interpret — **stop,
write it up to a file, and say so plainly in the summary.** Do not guess your way
forward and do not loop on a failing command. A clear blocker is a useful
result; a fabricated pass is worse than no result.
