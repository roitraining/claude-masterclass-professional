# Lab 1: Wire Claude into CI Safely

**Course:** Claude Code Professional
**Duration:** 100 minutes
**Format:** Instructor-led, in-class hands-on lab (300 level)

> Part of **[Claude Code Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

## Prerequisites

<!-- setup-ref:start -->
> **New to this course, or on a fresh machine?** Install and sign in to Claude Code first: **[Setup: Install and Sign In to Claude Code](../../SETUP-CLAUDE-CODE.md)**. About 10 minutes, Linux and Windows. Courses can be taken in any order, so this lab does not assume another course set it up.
>
> **This course needs a paid account** — the free plan does not include Claude Code. Confirm with `claude --version` and `claude auth status`.
<!-- setup-ref:end -->
- [ ] Python 3.11 or later
- [ ] Git 2.31 or later, with your name and email set
- [ ] `claude` signed in to a paid Anthropic account
- [ ] Administrative access to a personal or sample GitHub or GitLab project that holds no real work — **Tracks A and B only**; Track C needs no remote
- [ ] `$FILES/lab1-ci` from your instructor: `tallybook/`, `starters/github/`, `starters/gitlab/`, `fixtures/`, `security_gate.py`, `gate-checklist-github.md`, `gate-checklist-gitlab.md`, `requirements.txt`
- [ ] On Windows, run the shell commands in Git Bash

> **Token cost.** Every live run in this lab is a full Claude session. Hold yourself to `--max-turns` 6 to 8 and a 10 to 15 minute timeout, and stop re-running once you get a clean run.

---

## Overview

`anthropics/claude-code-action@v1` runs in interactive mode when a workflow has no `prompt` input and waits for `@claude`. It runs in automation mode when a `prompt` is set, on any GitHub event. The action already checks that the actor has write access and rejects bots that are not listed in `allowed_bots`, so most of the risk in a pipeline sits in what you wrote around it. The starter files work, and they are not safe.

`security_gate.py` is a static checker. It scores a workflow file against a checklist, needs no GitHub access, and cannot see repository settings, so you audit those by hand.

**Pick a track before you start.** Track A is GitHub. Track B is GitLab. Track C is gate only: choose it if you will not store a credential in a project. Tracks A and B also use a credential that you store as a project secret, never in a file.

---

## Part 1: Set Up the Project (about 10 minutes)

Goal: a project of your own that contains the `tallybook` sample, with its two failing tests visible.

### Step 1: Copy the Tallybook Sample into Your Own Project

Copy `tallybook` into a new project you control and commit it. Run its tests with the command in `tallybook/README.md`, which creates its own venv — the lab venv from Step 3 does not carry pytest. **Tracks A and B** then push it to your own remote — the live trigger in Part 4 needs a hosted project. **Track C** commits locally and does not push. Run the tests locally.

**Expected result:** the test run completes and two tests fail. Those two failures are what Claude fixes later in the lab.

### Step 2: Add Your Credential as a Project Secret

Tracks A and B only. Track C students continue at Step 3.

- **Track A:** get the Claude GitHub App on the project. Quick setup is `/install-github-app` (github.com only, needs the GitHub CLI and administrative access), or install the app and add a secret by hand. Add your credential as the repository secret `ANTHROPIC_API_KEY`.
- **Track B:** add `ANTHROPIC_API_KEY` as a masked CI/CD variable.

**Expected result:** the credential exists as a project secret or masked variable, and appears nowhere in any file you committed.

> **Hint:** quick setup pushes workflow files of its own. You only need the app. You bring your own workflows from `starters/`.

---

## Part 2: Baseline the Starters (about 10 minutes)

Goal: a written baseline of what the gate says about the starters, before you change anything.

### Step 3: Run the Security Gate on the Starter Workflows

Install the gate's dependency, then run it against the starter workflow files, or against the GitLab starter.

```bash
python3 -m venv ~/.venvs/mc-ci        # skip if the class image already has it
. ~/.venvs/mc-ci/bin/activate
pip install pyyaml
python3 security_gate.py <starter-workflow-file>
```

The virtual environment is required: the class image refuses a system-wide or
`--user` install because its Python is externally managed (PEP 668). Keep this
shell active for the rest of the lab.

**Expected result:** the gate prints a score and a list of findings for each file you point it at.

### Step 4: Record Every Finding

Record each file's score and each finding. Read `gate-checklist-github.md` or `gate-checklist-gitlab.md`.

**Acceptance criteria:** a table of finding, line, and why it is dangerous in one sentence.

---

## Part 3: Harden the Workflows (about 40 minutes)

Goal: every Claude workflow in your project scores 90 or more with every CRITICAL check ok, and still does its job.

### Step 5: Sort Findings into File Fixes and Settings Checks

Sort every finding into one of two groups: fixable in the file, and needing a repository setting. Keep the second list for Step 11.

**Expected result:** two lists. Only the first one is work you do in Part 3.

### Step 6: Harden the Workflows Until Every File Passes

Work through the file-fixable findings. Run the gate after each fix, not once at the end.

**Acceptance criteria:**

- Both GitHub starters (or the GitLab job) pass the gate.
- `claude.yml` still responds to `@claude` in an issue or pull request comment.
- `claude-review.yml` still reviews pull requests from branches in your repository, and cannot be started by a stranger, pull request text, or a bot.
- Nothing removed is just deleted without a replacement of the same intent. If you removed a permission, you can say what breaks without it.

> **A passing gate is not proof your prompt is clean.** T5 looks for outsider
> text used **directly**. Route the same text through an `env:` variable first —
> at job, step or workflow level — or through a step **output**, and the gate
> still scores 100/100 while the prompt carries attacker-controlled text. The
> direct form scores 85, so the gate only tells you the direct form is gone.
> Read your prompt yourself and trace where every value in it comes from. This
> is a limit of the gate, not a trap planted in the starter files.

> **Hint:** a secret that is never printed on purpose can still reach a log. What else prints?

> **Hint:** ask who writes each piece of text that reaches the shell or the prompt. How do you give Claude a pull request to read without pasting its text into the prompt?

> **Hint:** ask what the action itself already refuses, and whether any input in the starter turns that off.

> **Hint:** think about which tools a review run needs, and which a fix run needs. They are not the same list.

> **Hint:** a commit pushed with the default `GITHUB_TOKEN` does not start other workflows. Which input produces that, and what does the action use when you omit it?

> **Common Pitfall:** be careful about over-correcting. Read the action's documentation before you remove a permission that looks unused.

---

## Part 4: Prove the Pipeline End to End (about 20 minutes)

Tracks A and B only. Track C students continue at Part 6.

Goal: show that the hardened pipeline works end to end.

### Step 7: Open the Seed Issue and Trigger Claude

Open an issue from `fixtures/ISSUE-001.md`. Ask Claude to fix it with an `@claude` comment (Track A), or trigger your job on a merge request (Track B).

**Expected result:** a run finishes, and a branch or pull request carries a fix, or an existing pull request is updated.

> **Troubleshooting:** workflow changes may need to be on the default branch before a comment event uses them. If Claude does not answer, check that the app is installed, the secret exists, the comment says `@claude` as a whole word, and you have write access.

### Step 8: Confirm CI Ran on Claude's Commit

**Acceptance criteria:**

- Your CI workflow ran on the commit Claude pushed, and the tests pass.
- The run stayed inside `--max-turns` and the job timeout.

> **Troubleshooting:** if CI did not run on Claude's commit, return to Step 6. The default `GITHUB_TOKEN` was probably passed in.

---

## Part 5: Test for Prompt Injection (about 10 minutes)

Tracks A and B only. Track C students continue at Part 6.

Goal: evidence that outsider text is treated as data.

### Step 9: Open the Injection Fixtures

Open an issue with the body from `fixtures/issue-body-injection.md`. For Track A also open a pull request using `fixtures/pr-description-injection.md` as its description. Comment `@claude please look at this` on the issue.

**Expected result:** a run starts and completes without acting on the planted instructions.

### Step 10: Collect Evidence That Outsider Text Was Treated as Data

**Acceptance criteria:** the run log and any comments show no environment dump, no secret, no workflow edit and no direct push to the default branch. Save the run link or a log excerpt.

> **Hint:** if something got through, treat that as the finding. Go back to Step 6 and decide which control should have stopped it.

---

## Part 6: Audit the Platform Settings (about 10 minutes)

Goal: the checks the gate cannot make.

### Step 11: Record What the Gate Cannot See

Using the second list from Step 5, write a short note for your platform covering each of: who has write access, whether the default branch is protected, how the secret is scoped, what token permissions the platform grants by default, and what a fork or outsider can trigger.

**Acceptance criteria:** a note recording what you looked at and what you saw, for every item above.

> **Hint:** these live in project settings, not in the file. Where each appears in your platform's screens is not covered by this course. Find them.

**Track C alternative.** Track C has no hosted project, so there are no settings
screens to read. Write the audit as a specification instead: for each of the
five items, state what the correct setting is for a repository that runs Claude
in CI, what an incorrect setting would permit, and which of your hardened
workflow lines would still hold if that setting were wrong. This earns the same
15 points.

> **Hint for Track C:** the point is which risks the file can absorb and which
> only a project setting can stop. Name at least one of each.

---

## Part 6b: Track C Only — Predict the Live Run (about 25 minutes)

Skip this part on Tracks A and B: you ran the pipeline for real in Part 4.

### Step 11b: Write What a Live Run Would Do on Your Hardened Files

You have no hosted project, so you cannot trigger Claude. Predict it instead,
from your hardened files and the gate output.

For each of your Claude workflow files, write:

- What event starts it, and what would **not** start it
- Which actors it accepts and which it refuses, and the line that decides
- What it is permitted to do once running: what it can write, push or open
- What the planted trap would have allowed before you fixed it
- For **each** of the two injection fixtures, `fixtures/issue-body-injection.md`
  and `fixtures/pr-description-injection.md`: **what it tries to do**, and which
  of your controls stops it, and which does not. Read both files — Track C skips
  running them in Part 5, so this is where that analysis happens.

**Acceptance criteria:** a written prediction covering every point above for
each hardened file. **One citation per bullet is enough** — a line in your file
or a gate finding — not one per sentence.

> **Hint:** a prediction that does not cite a line is a guess. The gate output
> from Step 6 and your baseline table from Step 4 are your evidence.

> **Common Pitfall:** predicting what you intended rather than what the file
> says. Read the file as a stranger would.

---

## Part 7: Checkpoint

### Step 12: Verify Your Progress

- [ ] The `tallybook` sample is in a project you control, and its two tests failed before Claude touched them
- [ ] Your credential is a project secret or masked variable, and is in no committed file
- [ ] You have a baseline table of findings for the starters, from before any change
- [ ] Every Claude file scores 90 or more with every CRITICAL check ok
- [ ] `claude.yml` still answers `@claude`
- [ ] `claude-review.yml` still reviews same-repository pull requests, and refuses strangers, pull request text and bots
- [ ] Tracks A and B only: a live run opened or updated a pull request (Track C cannot meet this)
- [ ] Tracks A and B only: your CI ran on Claude's commit and the tests pass (Track C cannot meet this)
- [ ] Tracks A and B only: injection evidence saved, showing no dump, secret, workflow edit or direct push (Track C does the written analysis in Step 11b instead)
- [ ] Settings audit written for all five items
- [ ] You can name each planted trap and the fix that removed it
- [ ] Gate output from your final files is saved

- [ ] Track C: a written prediction from Step 11b for every hardened file, each claim tied to a line or a gate finding

Track C substitutes a passed gate plus the written notes from Step 4, Step 11 and Step 11b.

---

## Troubleshooting Reference

| Issue | Symptom | Solution |
|---|---|---|
| Missing dependency | `PyYAML is required` | Activate the lab venv, then run `pip install pyyaml` in the environment you run the gate from |
| Gate skips the file | "No Claude step found. Skipped." | The file has no `anthropics/claude-code-action` step, or no `claude` command in a GitLab job. Deleting the Claude step to pass is not a fix |
| GitLab file always skipped | "No Claude step found. Skipped." on a file that clearly has a `claude` job, and the gate **exits 0** | The gate identifies GitLab config by filename, matching any name that **starts with** `.gitlab-ci` — so `.gitlab-ci.yml` and `.gitlab-ci.yaml` both work, while `gitlab-ci.yml`, `ci.yml` or `my-job.yml` are skipped. Either rename the file or pass `--platform gitlab` |
| Claude ignores the mention | No response to `@claude` | The app is missing, the secret is missing, the comment says `@claude-bot` or `/claude` instead of `@claude`, or the commenter lacks write access |
| Authentication breaks after hardening | Run fails at authentication | Default GitHub App authentication needs `id-token: write`. Restore it |
| CI silent on Claude's commit | No CI run appears | The default `GITHUB_TOKEN` was passed in. Remove the input, or use a custom app token |
| Fork pull request gets no secrets | Review workflow does nothing on a fork PR | GitHub behavior on public repositories. This is why the review workflow is for same-repository branches |
| Gate passes but the run leaks | Clean score, bad behavior | The gate reads a single file, and T5 only catches outsider text used directly — an `env:` variable or a step output still scores 100/100. Settings, the other workflows, and where each value in your prompt comes from are yours to check |
| Track B runner lacks tools | Install script fails | The job installs the CLI with the install script. If your runner image lacks `curl` or `bash`, install them as the starter does |

---

## Scoring Rubric (100 points)

| Item | Tracks A and B | Track C |
|---|---|---|
| Gate points, split evenly across the Claude files you hardened (two workflow files on GitHub, a single job on GitLab) | 50 | 50 |
| Live trigger produced or updated a pull request | 15 | |
| CI ran on Claude's commit (GitLab: a rule that stops Claude's own push from starting another run, shown working) | 10 | |
| Injection test evidence | 10 | 10 (Step 11b: what each fixture tries, and which control stops it) |
| Settings audit | 10 | 15 |
| Each planted trap named, with why it is dangerous and which fix removed it | 5 | 5 |
| Written prediction of what a live run would do on the hardened files (Step 11b) | | 20 |

Each file earns its full share of the gate points when the score is 90 or more with every CRITICAL check ok, 60 percent of its share for 70 to 89 with every CRITICAL check ok, 20 percent when any CRITICAL check still fails, and 0 when the Claude step was removed.

---

## What You Built

In 100 minutes, you:

- Took two working but unsafe starter pipelines and hardened them to a passing security gate without breaking what they do
- Proved the hardened pipeline end to end: a mention triggered Claude, Claude pushed a fix, and your CI ran on that commit
- Fed outsider text to a live pipeline and collected evidence that it was treated as data, not instructions
- Wrote down the five controls a static file checker cannot see, and where they actually live

---

## What's Next

Lab 2, Tune and Score Code Review, moves from wiring Claude in safely to judging the quality of what it produces. You reuse the project you built here.

---

## Facilitator Notes

A good result is small diffs to each starter, a gate score of 100 or close, a real run, and a list of what the gate cannot see. The starters plant these traps:

| Trap | Where | Gate check |
|---|---|---|
| A trigger anyone can use | `claude.yml` line 30, `allowed_non_write_users: "*"`; line 14, a comment and issue trigger with no `if` guard on the job; `claude-review.yml` line 4, `pull_request_target`, with line 19 checking out the pull request head | T1 |
| Over-broad permissions | `claude.yml` line 11, `write-all`; `claude-review.yml` line 14, `actions: write` | T2 |
| A secret echoed into a log | `claude.yml` lines 23 and 24, an echo of the secret and a `printenv` dump; `claude-review.yml` line 26, a literal key (placeholder value) | T3 |
| A bot loop | `claude-review.yml` line 27, `allowed_bots: "*"` on a workflow that triggers on `synchronize` while Claude pushes to the branch, with no `concurrency` group | T4 |
| Injection hidden in outsider text | `claude-review.yml` line 22 (the title in a shell step) and line 31 (the description in the prompt); the live fixtures `fixtures/issue-body-injection.md` and `fixtures/pr-description-injection.md` | T5, plus T6 as the defense for the interactive workflow |
| Tools and limits | `claude.yml` line 32, bare `Bash`; `claude-review.yml` lines 33 and 34, `Bash(*)` and `--dangerously-skip-permissions`; no `--max-turns` and no `timeout-minutes` in either file; line 24, `@main` | T6, T7, T8 |
| A push that will not start CI | `claude.yml` line 29, `github_token: ${{ secrets.GITHUB_TOKEN }}` | T9 |

GitLab starter: line 11 defines the key in YAML; lines 12 to 15 add a trigger rule and a merge request rule with no fork guard; lines 22 and 23 print the key and dump the environment; lines 26 to 29 paste the title, description and `$AI_FLOW_INPUT` into the prompt; line 31 grants bare `Bash`; there is no `--max-turns`, `timeout`, `resource_group` or rule that skips Claude's own commits. The facilitator reference files in `facilitator/` score 100.

Watch for students who:

- remove the Claude step or the triggers to pass. The rubric gives zero for that.
- fix the gate and not the risk, for example hiding `${{ github.event.pull_request.body }}` in an intermediate variable that is still pasted into the prompt. Ask what the prompt contains at run time.
- pass the injection test because the model happened to refuse. Ask which control would stop it if the model complied.
- strip `id-token: write` and break authentication.

Costs: each run is a full Claude session. Hold each student to `--max-turns` 6 to 8 and a 10 to 15 minute timeout, and tell them to stop re-running after the first clean run.

Unconfirmed, rehearse before delivery: whether `allowed_non_write_users` accepts the value `"*"` (the documentation names the input and says to pass your own `github_token`; the gate only checks that the key is present); what the quick setup pushes and in what order on the day; whether a comment event needs the workflow on the default branch in your sandbox; the exact screens for the settings audit on GitHub and GitLab; and any GitLab mention-driven setup beyond the documented webhook pattern. The GitLab checks for the fork guard, the protected-ref condition and the skip rule are lab design rules, stricter than the documentation's example job, and the lab does not claim they are product requirements.

---

*Lab 1 Complete*
