# Lab 2: Tune and Score Code Review

> Part of **[Claude Code Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

**Learning objective:** Tune the scope and instructions of an automated review against pull requests with planted bugs and false-positive bait, and measure the result for bugs caught and false positives raised. Time: 90 minutes.

**Files:** `$FILES/lab2-review`: `build_fixture.py`, `diffs/`, `REVIEW.md`, `run_reviews.py`, `score_review.py`, `findings.schema.json`, `sample-findings.json`.

**Context:** The fixture is a small fictional Python lending service with a `main` branch and eleven pull request branches. Some contain planted bugs. Some contain code that looks wrong and is fine. One is a clean change. You write review instructions in `REVIEW.md`, produce findings as JSON, and a scorer reports bugs caught, false positives and a tier. The managed Code Review service reads `REVIEW.md` and `CLAUDE.md` from the base or default branch, never from the pull request. The local `/code-review` command reads `CLAUDE.md` and not `REVIEW.md`. In this lab the prompt in `run_reviews.py` tells Claude to read both files, so what you tune here carries to the service, and rules you want in every tool belong in `CLAUDE.md`.

> **Facilitators.** The managed Code Review service needs a Team or Enterprise plan with an Owner who turns it on, and it works on GitHub only. Most students will not have it. The lab works for everyone with print-mode `claude -p` and needs no plan beyond the one the student already has.

**Steps:**

1. **Build the fixture (about 5 minutes).** Goal: a local repository with `main` and the pull request branches.
   - `python build_fixture.py ~/work/lending-review`, then check the branches with `git branch`.
   - Copy `REVIEW.md` from `$FILES/lab2-review` into the repository root on `main` and commit it. Do not edit `CLAUDE.md`'s existing rules. You may add to it.
   - Acceptance criteria: `python -m unittest` passes on `main`.

2. **Baseline (about 15 minutes).** Goal: a scored review using the starter `REVIEW.md` unchanged.
   - Produce findings with `run_reviews.py`, or by hand (see "How to get findings as JSON" below). Score them with `python score_review.py findings.json`.
   - Acceptance criteria: you have a baseline tier, a count of bugs caught, and a count of false positives, written down.

3. **Tune (about 45 minutes).** Goal: reach Silver, and Gold if you can, with instructions that would work on another repository.
   - Acceptance criteria:
     - At least Silver on the scorer, from a fresh run of every pull request branch after your last edit.
     - A round log with three rounds at most: the change you made, the score before and after.
     - `REVIEW.md` names no branch, no file and no line from this fixture, and does not list the planted bugs.
   - Hints:
     - Define what Important means for this service, and what is a Nit at most. Cap the nits.
     - Tell the reviewer what not to report, and what must be checked before a finding is raised. A rule that asks for evidence cuts false positives without hiding bugs.
     - The repository's own rules live in `CLAUDE.md`. Some bait is cleared by a rule the reviewer can already read. Why was it flagged anyway?
     - A narrower `REVIEW.md` lowers false positives and can lose bugs. Check both numbers every round.
     - Two planted bugs are covered by a passing test. "Tests pass" is not evidence.
     - Iterate on a single branch with `--only pr-03`, then finish with a full run.

4. **Compare with `/code-review` (about 10 minutes, optional).** Goal: see how the local command differs.
   - In a session in the repository, check out a bug branch and run `/code-review`. Note what it reports against what your print-mode run reported.
   - Acceptance criteria: two sentences on what differed and why, including which of your two files it read.

5. **Explain (about 10 minutes).** Goal: show you understand the numbers.
   - Acceptance criteria: for a miss, or a false positive that remains, the pull request, what the reviewer saw, and the rule you would add. For each rule that removed a false positive, the rule and the false positive it removed.

**How to get findings as JSON.** The scorer reads this shape (the file `findings.schema.json` describes it):

```
{"findings": [
  {"pr": "pr-03-delete-member", "file": "lending/api.py", "line": 32,
   "severity": "important", "title": "Missing role check", "detail": "..."}
]}
```

`severity` is `important` or `nit`. `pr` is the branch name or its `pr-NN` prefix. `line` is the line on the pull request branch, and may be null.

- Easiest: `python run_reviews.py ~/work/lending-review --out findings.json`. It runs `claude -p` once per branch, passes the diff on standard input, allows only `Read,Grep,Glob`, sets `--max-turns` and `--max-budget-usd`, and merges the replies. `--dry-run` prints the commands and calls nothing.
- By hand for a single branch: `git diff -U25 main...pr-03-delete-member | claude -p "<your prompt>" --allowedTools "Read,Grep,Glob" --max-turns 8`, with a prompt that asks for only the JSON object above.
- With a schema: print mode accepts `--json-schema` with a JSON Schema, and returns validated JSON. Add `--output-format json` if you want the full result object. Look at what comes back once. `run_reviews.py` already accepts a top-level `findings` object, a `structured_output` field or a `result` field.
- No model at all: `python score_review.py sample-findings.json` runs the scorer on a hand-written sample. Use it to learn the shape and the tier rules.

**Checkpoint:** A scored review that catches the planted bugs with an acceptable false-positive rate: at least Silver, which is at least 4 of 5 bugs and at most 3 false positives, from a run made after your last edit to `REVIEW.md`.

**Common problems:**

- `claude` is not found by `run_reviews.py`: pass `--claude-cmd` with the full path.
- A branch returns no JSON: the reply had prose around it, or `--max-turns` was too low. Re-run it with `--only`, and raise `--max-turns`.
- A score looks wrong after you edited `REVIEW.md` on a branch: `REVIEW.md` must be on `main` for the run to read it. The driver runs from `main` and reads the diff of each branch.
- Everything is a false positive on the first run: that is the point of the baseline. Tune.
- The scorer does not match a finding you think is right: the finding's `file` must match the bug's file, and its `line` must be within 3 lines of the bug. A finding with no line must mention a keyword from the key.
- The reviewer flags the guarded admin route: it judged from the diff and did not open `lending/web.py`. Allow it to read, and tell it to.
- Costs climbing: use `--only` while iterating, and keep `--max-budget-usd` low.

**Scoring rubric (100 points):**

| Item | Points |
|---|---|
| Tier from a fresh full run: Gold 50, Silver 40, Bronze 25, none 0 | 50 |
| Precision (caught divided by caught plus false positives): 0.8 or more 10, 0.6 to 0.79 6, below 0.6 2 | 10 |
| `REVIEW.md` quality: defines Important and Nit, caps nits, lists what not to report, requires evidence, cites the repository's own rules. Score 0 for this row if it names a branch, file or line from the fixture or lists the planted bugs, and ask how it would behave on a new repository | 20 |
| Round log shows a hypothesis and a score change in each round | 10 |
| Explanation of a remaining miss or false positive, and of what each rule removed | 10 |

**Facilitator note:** `facilitator/ANSWER-KEY.md` lists the planted bugs and the bait with files and lines, why each is planted, and what a good tuning looks like. In brief: bugs are a logic error (`pr-01`, `or` for `and` in a waiver), an off-by-one (`pr-02`, a slice one item too long), a missing authorization check (`pr-03`, a handler with no `require_role`), a hard-coded secret (`pr-04`, a placeholder password in source) and a SQL injection (`pr-05`). Bait is generated SQL placeholders (`pr-06`), a test-only placeholder password (`pr-07`), a correct `n - 1` loop (`pr-08`), a handler guarded by its router (`pr-09`) and policy-driven truncation (`pr-10`). `pr-11` is a clean change.

Traps to watch: students who excuse a bug because tests pass; a `REVIEW.md` that says "report fewer things", which trades bugs for quiet; a `REVIEW.md` that names a branch. Ask them for the rule that clears the bait and to show it would not hide a real unguarded handler elsewhere.

Remind the room that this scorer is a local teaching tool. The managed service does not return this JSON, and its check run never fails or approves a pull request.

Unconfirmed, rehearse: the tier thresholds (they are untested against real model runs, and the numbers at the top of `score_review.py` are meant to be adjusted); the output envelope that `claude -p --output-format json` returns when `--json-schema` is used (the driver tolerates three shapes); the exact target and level arguments `/code-review` takes (the skill's description names a branch or pull request target and an effort level, and neither has been confirmed for this lab); and how many branches a student's account can review in the time allowed, which depends on rate limits.
