# Lab 2: Tune and Score Code Review

**Course:** Claude Code Professional
**Duration:** 90 minutes
**Format:** Instructor-led, in-class hands-on lab (300 level)

> Part of **[Claude Code Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

## Prerequisites

- [ ] Lab 1 completed, or an equivalent working Claude Code setup
- [ ] Python 3.11 or later
- [ ] Git 2.31 or later, with your name and email set
- [ ] `claude` signed in to a paid Anthropic account
- [ ] `$FILES/lab2-review` from your instructor: `build_fixture.py`, `diffs/`, `REVIEW.md`, `run_reviews.py`, `score_review.py`, `findings.schema.json`, `sample-findings.json`
- [ ] On Windows, run the shell commands in Git Bash

> **Token cost.** Each review run is a full Claude session. Iterate with `--only` on a single branch and keep `--max-budget-usd` low. Save the full run for the end.

---

## Overview

The fixture is a small fictional Python lending service with a `main` branch and eleven pull request branches. Some contain planted bugs. Some contain code that looks wrong and is fine. One is a clean change. You write review instructions in `REVIEW.md`, produce findings as JSON, and a scorer reports bugs caught, false positives and a tier.

The managed Code Review service reads `REVIEW.md` and `CLAUDE.md` from the base or default branch, never from the pull request. The local `/code-review` command reads `CLAUDE.md` and not `REVIEW.md`. In this lab the prompt in `run_reviews.py` tells Claude to read both files, so what you tune here carries to the service, and rules you want in every tool belong in `CLAUDE.md`.

> **Facilitators.** The managed Code Review service needs a Team or Enterprise plan with an Owner who turns it on, and it works on GitHub only. Most students will not have it. The lab works for everyone with print-mode `claude -p` and needs no plan beyond the one the student already has.

---

## Reference: Producing Findings as JSON

You need this in Part 2 and again in Part 3. The scorer reads this shape, which `findings.schema.json` describes:

```
{"findings": [
  {"pr": "pr-03-delete-member", "file": "lending/api.py", "line": 32,
   "severity": "important", "title": "Missing role check", "detail": "..."}
]}
```

`severity` is `important` or `nit`. `pr` is the branch name or its `pr-NN` prefix. `line` is the line on the pull request branch, and may be null.

Four ways to produce it, easiest first:

- **Driver script.** `python run_reviews.py ~/work/lending-review --out findings.json`. It runs `claude -p` once per branch, passes the diff on standard input, allows only `Read,Grep,Glob`, sets `--max-turns` and `--max-budget-usd`, and merges the replies. `--dry-run` prints the commands and calls nothing.
- **By hand, one branch.** `git diff -U25 main...pr-03-delete-member | claude -p "<your prompt>" --allowedTools "Read,Grep,Glob" --max-turns 8`, with a prompt that asks for only the JSON object above.
- **With a schema.** Print mode accepts `--json-schema` with a JSON Schema and returns validated JSON. Add `--output-format json` for the full result object. Look at what comes back once. `run_reviews.py` already accepts a top-level `findings` object, a `structured_output` field or a `result` field.
- **No model at all.** `python score_review.py sample-findings.json` runs the scorer on a hand-written sample. Use it to learn the shape and the tier rules.

---

## Part 1: Build the Fixture (about 5 minutes)

Goal: a local repository with `main` and the pull request branches.

### Step 1: Build the Lending Fixture

```bash
python build_fixture.py ~/work/lending-review
git branch
```

**Expected result:** `git branch` lists `main` plus eleven `pr-NN-*` branches.

### Step 2: Add REVIEW.md to main

Copy `REVIEW.md` from `$FILES/lab2-review` into the repository root on `main` and commit it. Do not edit `CLAUDE.md`'s existing rules. You may add to it.

**Acceptance criteria:** `python -m unittest` passes on `main`.

> **Common Pitfall:** `REVIEW.md` must be on `main` for a run to read it. The driver runs from `main` and reads the diff of each branch, so editing `REVIEW.md` on a branch has no effect on the score.

---

## Part 2: Baseline the Starter Review (about 15 minutes)

Goal: a scored review using the starter `REVIEW.md` unchanged.

### Step 3: Produce Findings with the Starter REVIEW.md

Produce findings using any method from the reference section above. Change nothing in `REVIEW.md` first.

**Expected result:** a `findings.json` containing findings for the pull request branches.

### Step 4: Score the Baseline and Write It Down

```bash
python score_review.py findings.json
```

**Acceptance criteria:** a baseline tier, a count of bugs caught, and a count of false positives, all written down.

> **Note:** if nearly everything is a false positive on this first run, that is the expected baseline. Tuning is Part 3.

---

## Part 3: Tune the Review Instructions (about 45 minutes)

Goal: reach Silver, and Gold if you can, with instructions that would work on another repository.

### Step 5: Tune REVIEW.md Across at Most Three Rounds

Iterate on a single branch with `--only pr-03` while you work, and keep a log of each round.

**Acceptance criteria:**

- A round log with three rounds at most: the change you made, and the score before and after.
- `REVIEW.md` names no branch, no file and no line from this fixture, and does not list the planted bugs.

> **Hint:** define what Important means for this service, and what is a Nit at most. Cap the nits.

> **Hint:** tell the reviewer what not to report, and what must be checked before a finding is raised. A rule that asks for evidence cuts false positives without hiding bugs.

> **Hint:** the repository's own rules live in `CLAUDE.md`. Some bait is cleared by a rule the reviewer can already read. Why was it flagged anyway?

> **Hint:** two planted bugs are covered by a passing test. "Tests pass" is not evidence.

> **Common Pitfall:** a narrower `REVIEW.md` lowers false positives and can lose bugs. Check both numbers every round.

### Step 6: Confirm with a Fresh Full Run

Run every pull request branch after your last edit, then score it.

**Acceptance criteria:** at least Silver on the scorer, from a fresh full run made after your last edit to `REVIEW.md`.

---

## Part 4: Compare With the Local Command (about 10 minutes, optional)

Goal: see how the local command differs from print mode.

### Step 7: Run /code-review on a Bug Branch

In a session in the repository, check out a bug branch and run `/code-review`. Note what it reports against what your print-mode run reported.

**Acceptance criteria:** two sentences on what differed and why, including which of your two files it read.

---

## Part 5: Explain the Numbers (about 10 minutes)

Goal: show you understand the result, not just the score.

### Step 8: Account for Every Miss and Remaining False Positive

**Acceptance criteria:**

- For each miss, or false positive that remains: the pull request, what the reviewer saw, and the rule you would add.
- For each rule that removed a false positive: the rule, and the false positive it removed.

---

## Part 6: Checkpoint

### Step 9: Verify Your Progress

- [ ] The fixture is built and `python -m unittest` passes on `main`
- [ ] `REVIEW.md` is committed on `main`, not on a branch
- [ ] A baseline tier, bugs-caught count and false-positive count are written down
- [ ] A round log shows at most three rounds, each with a change and a score before and after
- [ ] `REVIEW.md` names no branch, file or line from the fixture, and does not list the planted bugs
- [ ] A fresh full run after your last edit scores at least Silver
- [ ] Silver means at least 4 of 5 bugs caught and at most 3 false positives
- [ ] Every miss and remaining false positive is explained with the rule you would add
- [ ] Each rule you added is paired with the false positive it removed

---

## Troubleshooting Reference

| Issue | Symptom | Solution |
|---|---|---|
| Driver cannot find Claude | `claude` is not found by `run_reviews.py` | Pass `--claude-cmd` with the full path |
| A branch returns no JSON | One branch missing from the findings | The reply had prose around it, or `--max-turns` was too low. Re-run with `--only` and raise `--max-turns` |
| Edits appear to have no effect | Score unchanged after editing `REVIEW.md` | `REVIEW.md` must be on `main`. The driver runs from `main` and reads each branch's diff |
| Everything is a false positive | Baseline run is all noise | Expected. That is what the baseline is for. Tune in Part 3 |
| Scorer rejects a correct finding | A finding you believe is right does not match | The finding's `file` must match the bug's file and its `line` must be within 3 lines. A finding with no line must mention a keyword from the key |
| Guarded route flagged | Reviewer reports the guarded admin route | It judged from the diff and did not open `lending/web.py`. Allow it to read, and tell it to |
| Costs climbing | Spend rising across rounds | Use `--only` while iterating and keep `--max-budget-usd` low |

---

## Scoring Rubric (100 points)

| Item | Points |
|---|---|
| Tier from a fresh full run: Gold 50, Silver 40, Bronze 25, none 0 | 50 |
| Precision (caught divided by caught plus false positives): 0.8 or more 10, 0.6 to 0.79 6, below 0.6 2 | 10 |
| `REVIEW.md` quality: defines Important and Nit, caps nits, lists what not to report, requires evidence, cites the repository's own rules. Score 0 for this row if it names a branch, file or line from the fixture or lists the planted bugs, and ask how it would behave on a new repository | 20 |
| Round log shows a hypothesis and a score change in each round | 10 |
| Explanation of a remaining miss or false positive, and of what each rule removed | 10 |

---

## What You Built

In 90 minutes, you:

- Took an untuned reviewer from a noisy baseline to at least Silver on a fixture with both planted bugs and false-positive bait
- Wrote review instructions general enough to carry to another repository, with no fixture branch, file or line named in them
- Kept a round log tying each instruction change to a measured move in bugs caught and false positives
- Explained every remaining miss and false positive, and which rule removed which

---

## What's Next

Lab 3, Build a Custom Plugin, moves from tuning Claude's judgment to packaging your own capability for a team to install.

---

## Facilitator Notes

`facilitator/ANSWER-KEY.md` lists the planted bugs and the bait with files and lines, why each is planted, and what a good tuning looks like. In brief: bugs are a logic error (`pr-01`, `or` for `and` in a waiver), an off-by-one (`pr-02`, a slice one item too long), a missing authorization check (`pr-03`, a handler with no `require_role`), a hard-coded secret (`pr-04`, a placeholder password in source) and a SQL injection (`pr-05`). Bait is generated SQL placeholders (`pr-06`), a test-only placeholder password (`pr-07`), a correct `n - 1` loop (`pr-08`), a handler guarded by its router (`pr-09`) and policy-driven truncation (`pr-10`). `pr-11` is a clean change.

Traps to watch: students who excuse a bug because tests pass; a `REVIEW.md` that says "report fewer things", which trades bugs for quiet; a `REVIEW.md` that names a branch. Ask them for the rule that clears the bait and to show it would not hide a real unguarded handler elsewhere.

Remind the room that this scorer is a local teaching tool. The managed service does not return this JSON, and its check run never fails or approves a pull request.

Unconfirmed, rehearse: the tier thresholds (they are untested against real model runs, and the numbers at the top of `score_review.py` are meant to be adjusted); the output envelope that `claude -p --output-format json` returns when `--json-schema` is used (the driver tolerates three shapes); the exact target and level arguments `/code-review` takes (the skill's description names a branch or pull request target and an effort level, and neither has been confirmed for this lab); and how many branches a student's account can review in the time allowed, which depends on rate limits.

---

*Lab 2 Complete*
