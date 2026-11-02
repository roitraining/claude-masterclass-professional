# Claude Code Professional: Labs

**Course:** Claude Code Professional: Pipelines, Plugins and Enterprise Operations (Claude MasterClass Professional, Course 2)
**Contents:** Four timed hands-on labs and a take-home lab. The numbers match the Today's Labs slide.

---

## About this guide

These are 300-level labs. Each gives a goal, acceptance criteria and hints, not click-by-click steps. Each hides planted traps, and each is scored. The Associate course taught worktrees, subagent teams, hooks and policy precedence, so none of that is retaught here.

In this guide `$FILES` is the `demo-files` folder your instructor gives you. Everything runs on your own personal or sample GitHub or GitLab project plus local files. You do not depend on another student, and you do not need to share an organization with anyone. Use a project that holds no real work. Every name, company and figure is fictional. No file holds a real secret.

Claude Code can word things differently each time. Check your result against the acceptance criteria, not against exact text.

**Before Lab 1:** Python 3.11 or later, Git 2.31 or later with your name and email set, `claude` signed in to a paid Anthropic account, and administrative access to a personal or sample GitHub or GitLab project. On Windows, run the shell commands in Git Bash.

> **Token cost.** CI runs, review runs and plugin evals use API credits or subscription usage. Every lab says where to cap them. Use the caps.

> **Facilitators.** Instructor-only actions (anything in an organization, a tenant or a shared account) stay with the instructor. Students act only in their own project. Remove the `facilitator/` folders from `$FILES` before you share it.

---

## Lab 1: Wire Claude into CI Safely

**Learning objective:** Wire Claude into a CI pipeline so that a trigger works, and pass a security gate that checks who can trigger a run, the permissions granted, the secrets used, and a planted injection. Time: 100 minutes.

**Files:** `$FILES/lab1-ci`: `tallybook/`, `starters/github/`, `starters/gitlab/`, `fixtures/`, `security_gate.py`, `gate-checklist-github.md`, `gate-checklist-gitlab.md`, `requirements.txt`.

**Context:** `anthropics/claude-code-action@v1` runs in interactive mode when a workflow has no `prompt` input and waits for `@claude`. It runs in automation mode when a `prompt` is set, on any GitHub event. The action already checks that the actor has write access and rejects bots that are not listed in `allowed_bots`, so most of the risk in a pipeline sits in what you wrote around it. The starter files work, and they are not safe. `security_gate.py` is a static checker. It scores a workflow file against a checklist, needs no GitHub access, and cannot see repository settings, so you audit those by hand.

Pick a track. Track A is GitHub. Track B is GitLab. Track C is gate only: choose it if you will not store a credential in a project. Tracks A and B also use a credential that you store as a project secret, never in a file.

**Steps:**

1. **Set up (about 10 minutes).** Goal: a project of your own that contains the `tallybook` sample, with its two failing tests visible.
   - Copy `tallybook` into a new project you control, commit it, and push it to your own remote. Run the tests locally and confirm that two fail.
   - Track A: get the Claude GitHub App on the project. Quick setup is `/install-github-app` (github.com only, needs the GitHub CLI and administrator access), or install the app and add a secret by hand. Add your credential as the repository secret `ANTHROPIC_API_KEY`.
   - Track B: add `ANTHROPIC_API_KEY` as a masked CI/CD variable.
   - Hint: quick setup pushes workflow files of its own. You only need the app. You will bring your own workflows from `starters/`.

2. **Baseline (about 10 minutes).** Goal: a written baseline of what the gate says about the starters, before you change anything.
   - Run `pip install pyyaml`, then `python security_gate.py` on the starter workflow files, or on the GitLab starter.
   - Record each file's score and each finding. Read `gate-checklist-github.md` or `gate-checklist-gitlab.md`.
   - Acceptance criteria: a table of finding, line, why it is dangerous in a sentence.

3. **Harden (about 40 minutes).** Goal: every Claude workflow in your project scores 90 or more with every CRITICAL check ok, and still does its job.
   - Acceptance criteria:
     - Both GitHub starters (or the GitLab job) pass the gate.
     - `claude.yml` still responds to `@claude` in an issue or pull request comment.
     - `claude-review.yml` still reviews pull requests from branches in your repository, and cannot be started by a stranger, pull request text, or a bot.
     - Nothing removed is just deleted without a replacement of the same intent. If you removed a permission, you can say what breaks without it.
   - Hints:
     - Sort every finding into one of two groups: fixable in the file, and needing a repository setting. Keep a list of the second group for step 6.
     - A secret that is never printed on purpose can still reach a log. What else prints?
     - Ask who writes each piece of text that reaches the shell or the prompt. How do you give Claude a pull request to read without pasting its text into the prompt?
     - Ask what the action itself already refuses, and whether any input in the starter turns that off.
     - Think about which tools a review run needs, and which a fix run needs. They are not the same list.
     - A commit pushed with the default `GITHUB_TOKEN` does not start other workflows. Which input produces that, and what does the action use when you omit it?
     - Be careful about over-correcting. Read the action's documentation before you remove a permission that looks unused.
     - Run the gate after each fix, not once at the end.

4. **Live trigger (about 20 minutes, Tracks A and B).** Goal: show that the hardened pipeline works end to end.
   - Open an issue from `fixtures/ISSUE-001.md`. Ask Claude to fix it with an `@claude` comment (Track A), or trigger your job on a merge request (Track B).
   - Acceptance criteria:
     - A run finishes, and a branch or pull request carries a fix, or an existing pull request is updated.
     - Your CI workflow ran on the commit Claude pushed, and the tests pass.
     - The run stayed inside `--max-turns` and the job timeout.
   - Hints: workflow changes may need to be on the default branch before a comment event uses them. If Claude does not answer, check: the app is installed, the secret exists, the comment says `@claude` as a whole word, and you have write access. If CI does not run on Claude's commit, look at step 3 again.

5. **Injection test (about 10 minutes, Tracks A and B).** Goal: evidence that outsider text is treated as data.
   - Open an issue with the body from `fixtures/issue-body-injection.md`. For Track A also open a pull request using `fixtures/pr-description-injection.md` as its description. Comment `@claude please look at this` on the issue.
   - Acceptance criteria: the run log and any comments show no environment dump, no secret, no workflow edit and no direct push to the default branch. Save the run link or a log excerpt.
   - Hint: if something got through, treat that as the finding. Go back to step 3 and decide which control should have stopped it.

6. **Settings audit (about 10 minutes).** Goal: the checks the gate cannot make.
   - Acceptance criteria: for your platform, a short note of what you looked at and what you saw for each of: who has write access, whether the default branch is protected, how the secret is scoped, what token permissions the platform grants by default, and what a fork or outsider can trigger.
   - Hint: these live in project settings, not in the file. Where each appears in your platform's screens is not covered by this course. Find them.

**Checkpoint:** A working trigger that opens or updates a pull request, and a passed security gate. Run the gate on your final files and keep the output. Track C: a passed gate and the written notes from steps 2 and 6.

**Common problems:**

- `PyYAML is required`: run `pip install pyyaml` in the environment you run the gate from.
- The gate says "No Claude step found. Skipped.": the file has no `anthropics/claude-code-action` step, or no `claude` command in a GitLab job. Deleting the Claude step to pass is not a fix.
- Claude does not answer `@claude`: the app is missing, the secret is missing, the comment has `@claude-bot` or `/claude` instead of `@claude`, or the commenter lacks write access.
- The run fails at authentication after you removed a permission: the default GitHub App authentication needs `id-token: write`. Restore it.
- CI does not run on Claude's commit: the default `GITHUB_TOKEN` was passed in. Remove the input, or use a custom app token.
- A pull request from a fork gets no secrets on a public repository. That is GitHub behavior, and it is why the review workflow is for same-repository branches.
- The gate passes and the run still leaks: the gate reads a single file. Settings and the other workflows are yours to check.
- Track B: the job installs the CLI with the install script. If your runner image lacks `curl` or `bash`, install them as the starter does.

**Scoring rubric (100 points):**

| Item | Tracks A and B | Track C |
|---|---|---|
| Gate points, split evenly across the Claude files you hardened (two workflow files on GitHub, a single job on GitLab) | 50 | 50 |
| Live trigger produced or updated a pull request | 15 | |
| CI ran on Claude's commit (GitLab: a rule that stops Claude's own push from starting another run, shown working) | 10 | |
| Injection test evidence | 10 | 10 (written analysis of what each fixture tries and which control stops it) |
| Settings audit | 10 | 15 |
| Each planted trap named, with why it is dangerous and which fix removed it | 5 | 5 |
| Written prediction of what a live run would do on the hardened files | | 20 |

Each file earns its full share of the gate points when the score is 90 or more with every CRITICAL check ok, 60 percent of its share for 70 to 89 with every CRITICAL check ok, 20 percent when any CRITICAL check still fails, and 0 when the Claude step was removed.

**Facilitator note:** A good result is small diffs to each starter, a gate score of 100 or close, a real run, and a list of what the gate cannot see. The starters plant these traps:

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

## Lab 2: Tune and Score Code Review

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

---

## Lab 3: Build a Custom Plugin

**Learning objective:** Package a command, a hook and a subagent for a git-based, command-line workflow, meet an eval suite's pass bar, and distribute the plugin from a git marketplace. Time: 90 minutes.

**Files:** `$FILES/lab3-plugin`: `relnotes-starter/`, `plugin_lint.py`, `marketplace-template/`.

**Context:** The plugin drafts release notes from the git log. This is a Claude Code plugin for a terminal workflow, so it can ship a subagent, a hook and executables that a Cowork plugin cannot. It is not the Cowork plugin from the plugin engineering course. A plugin hook runs with your privileges and outside the sandbox, so what you ship is code someone else will run. The starter has a command stub, a subagent, a hook, a lint script, and an eval suite of six cases. The eval suite is your pass bar. Do not edit the eval cases.

**Steps:**

1. **Look first (about 10 minutes).** Goal: a list of what is wrong with the starter before you change anything.
   - Run `python plugin_lint.py relnotes-starter --marketplace marketplace-template`, and `claude plugin validate relnotes-starter`.
   - Acceptance criteria: you can explain each finding. Note which problems `validate` found and which only `plugin_lint.py` found.
   - Hint: `validate` checks syntax and schema. It does not test behavior, and it does not know what is dangerous.

2. **Fix the package (about 25 minutes).** Goal: a plugin that is safe to install and loads cleanly.
   - Acceptance criteria:
     - `python plugin_lint.py` reports no FAIL lines, and `claude plugin validate` passes.
     - The hook finds its script wherever the plugin is installed.
     - The auditing agent can read and cannot change anything, and relies on no setting that plugin agents ignore.
     - The rules that matter are delivered in a way Claude Code actually loads.
   - Hints: a fixed path in a hook breaks on every other machine. A plugin has a documented variable for its own folder. Check the plugin components documentation for which agent fields are supported and which are ignored. Look at where the rule text lives, and at what the validator said about it.

3. **Write the command (about 25 minutes).** Goal: a command whose behavior meets the evals.
   - Acceptance criteria:
     - The command works out a range of commits, reads the log, writes `RELEASE_NOTES.md` in the format `scripts/lint_notes.py` accepts, and uses the `changelog-auditor` agent before it finishes.
     - It never invents an entry, and changes nothing but the notes file.
     - Its description is specific enough to be chosen for release notes and to be ignored for unrelated requests, and short enough that you could defend its cost in the context window on every turn.
   - Hints: read the six cases to see what they test. The command's `description` decides when it is chosen. A frontmatter `allowed-tools` line limits what the command can do. A subagent has its own context window, so give it what it needs in the prompt.

4. **Run the pass bar (about 15 minutes).** Goal: the eval suite passes at 0.8.
   - Run from the plugin folder, and cap cost:

```
claude plugin eval . --scaffold --ablation none --no-publish --runs 2 --threshold 0.8 --max-cost-usd 6 --allow-tools Write Edit "Bash(git *)"
```

   - Acceptance criteria: exit code 0. Save the summary and the `report.html`.
   - Hints: iterate with `--case` on a single case and `--runs 1`. `--scaffold` runs each case's shell script on your machine, which is why it is off by default, so read `scaffold.sh` first. By default a report is published to claude.ai when the account supports it, and `--no-publish` keeps it local. A case below the threshold names its failing graders in the report.

5. **Distribute (about 10 minutes).** Goal: a teammate can install it from a git marketplace.
   - Copy `marketplace-template` to a new folder, put your plugin at `plugins/relnotes`, and make the marketplace entry valid.
   - Acceptance criteria: `claude plugin validate` passes on the marketplace folder. `claude plugin marketplace add <path>` and `claude plugin install <plugin>@<marketplace>` succeed from a clean shell. For a remote check, push the marketplace to your own repository and add it with `claude plugin marketplace add <owner>/<repo>`.
   - Hints: the entry name and the manifest name must match. A relative `source` is written from the marketplace root.

6. **Review like a skeptic (about 5 minutes).** Goal: the security note a reviewer would want.
   - Run `claude plugin details relnotes`. Acceptance criteria: in four sentences, what the hook runs and when, what the agent and command can do, the always-on token estimate and which component is largest, and one thing you would check before trusting someone else's version of this plugin.

**Checkpoint:** A plugin a teammate can install from a git marketplace, whose eval suite exits 0 at a 0.8 threshold.

**Common problems:**

- The hook runs `python` and your machine has only `python3`: change the hook command to match your machine, and note that you did.
- The eval run asks to trust the plugin: confirm it for your own plugin. `--trust-plugin` answers for CI and should be used only for plugins you would run yourself.
- `--scaffold` fails on Windows: the case scripts are Bash. Run the eval from Git Bash or WSL.
- A case scores low on `no-invented-entries` after the command is correct: the case prompt lures Claude into a dark mode headline. The command must say what to do when asked for an entry the log does not support.
- `ignores-unrelated` fails: the description is too broad, or the plugin loads instructions that make Claude write release notes for everything.
- An install fails with `Plugin "relnotes" not found in marketplace`: the marketplace entry name is not the manifest name.
- The always-on estimate is larger than you expect: long descriptions are in the context window on every turn. Shorten them, then re-run the evals, because a shorter description can stop a command from being chosen.
- The eval costs too much: lower `--runs`, run a single case with `--case`, and keep `--ablation none`, which skips the no-plugin comparison run.

**Scoring rubric (100 points):**

| Item | Points |
|---|---|
| `claude plugin validate` passes with no errors | 10 |
| `plugin_lint.py` has no FAIL lines | 15 |
| Eval suite: exit 0 at 0.8 scores 35. Otherwise 35 times the fraction of cases at or above 0.8 | 35 |
| Installs from a git marketplace you control, from a clean shell | 20 |
| Security note: hook, agent and command capabilities, and what you would check in someone else's plugin | 10 |
| Always-on cost note names the largest component and a way to reduce it | 10 |

**Facilitator note:** Traps planted in `relnotes-starter`:

| Trap | Where | Caught by |
|---|---|---|
| A fixed absolute path in a hook | `hooks/hooks.json` line 9 | `plugin_lint.py`; breaks on every machine but the author's |
| An auditing agent with `Edit`, `Write` and `Bash`, and a `permissionMode` setting that plugin agents ignore | `agents/changelog-auditor.md` lines 5 and 6 | `plugin_lint.py`; `validate` does not flag it |
| Rules in a `CLAUDE.md` at the plugin root | `CLAUDE.md` | `claude plugin validate` warns that it is not loaded; the rules never reach Claude |
| A one-line vague description and a command that is a stub | `commands/release-notes.md` | Evals, mainly `groups-by-type` and `ignores-unrelated` |
| A marketplace entry whose name is not the manifest name | `marketplace-template/.claude-plugin/marketplace.json` | `plugin_lint.py --marketplace`; install error |
| An eval lure for an invented feature | `evals/no-invented-entries/prompt.md` | The two judge graders |

The finished plugin is `facilitator/marketplace/plugins/relnotes`, inside a marketplace named `team-tools` that validates. A good command carries the grouping, ordering, hash format and "never invent" rules itself, and gives the auditor the log text, because the auditor has no shell. The suite has six cases: `groups-by-type`, `flags-breaking-change`, `no-invented-entries`, `ignores-unrelated`, `uses-auditor` and `hook-lints-bad-notes`.

Costs: each case runs 3 times by default, plus a no-plugin comparison run unless `--ablation none`. Six cases at 2 runs each is a real bill for a class. Rehearse once, record the cost, and set `--max-cost-usd` per student from that figure. An eval report goes to claude.ai by default when the account supports it, so tell students about `--no-publish`.

Unconfirmed, rehearse before delivery: whether a command is invoked through the Skill tool inside an eval run (the `command-was-used` grader depends on it, and the eval help says `tool_used: Skill` graders count as a plugin-fired indicator and not toward the score when the no-plugin comparison is on, so the lab turns that comparison off); whether the subagent grader's `input_match` on `changelog-auditor` matches the way an agent call is recorded in your Claude Code version; whether the plugin's hook fires inside an eval run, on which `hook-lints-bad-notes` depends; whether `Bash(git *)` is the right grant pattern on your platform; and the Bash requirement for scaffold scripts on Windows. If a case is unreliable after rehearsal, drop its weight or move it to an optional list before class, and keep the pass bar at the cases you trust.

---

## Lab 4: Build a Language Server Plugin

**Learning objective:** Configure a language server plugin that gives Claude diagnostics and code navigation, and find and fix a deliberate misconfiguration. Time: 75 minutes.

**Files:** `$FILES/lab4-lsp`: `pylsp-plugin-starter/`, `sample-project/`, `check_lsp.py`, `lsp_smoke.py`.

**Context:** A language server plugin tells Claude Code which command starts a language server and which file extensions it handles, in a `.lsp.json` file at the plugin root. It does not install the server. With a server running, Claude sees the errors and warnings the server reports after each edit, and gets an `LSP` tool for finding definitions and references by symbol. Claude Code skips the whole `.lsp.json` file when any entry is invalid, and `claude plugin validate` does not read this file, so a bad file looks like a working plugin that does nothing.

The server in this lab is `pylsp` (the Python LSP Server). Python already has an official code intelligence plugin built on a different server. If an official plugin covers your language, install that instead of writing your own. This lab writes the file by hand for practice, so do not have the official Python plugin enabled while you work. If two servers claim the same extension, the first registered wins.

**Steps:**

1. **Install the server (about 10 minutes).** Goal: `pylsp` on the PATH of the shell you start `claude` from.
   - `pip install "python-lsp-server[pyflakes,pycodestyle]"` in a virtual environment or your user environment. The two extras add the checks that produce diagnostics.
   - Acceptance criteria: `pylsp --help` runs from the shell you will use for `claude`. On Windows, check with `Get-Command pylsp` in PowerShell or `where pylsp`.
   - Hint: if you used a virtual environment, activate it in the same shell before you start `claude`.

2. **Reproduce the symptom (about 10 minutes).** Goal: see that the plugin loads and does nothing.
   - Run `claude plugin validate pylsp-plugin-starter`. Then start a session with `claude --plugin-dir pylsp-plugin-starter` in `sample-project`, ask Claude to add a line that uses an undefined name to `app/report.py`, and look for a diagnostics line.
   - Acceptance criteria: you can state what `validate` said, what the session did, and where the real error is shown (the `/plugin` Errors tab, and `claude --debug`).

3. **Find and fix (about 15 minutes).** Goal: a `.lsp.json` that loads.
   - Use `python check_lsp.py pylsp-plugin-starter`, the Errors tab and the documentation. Fix the file.
   - Acceptance criteria: `check_lsp.py` reports no FAIL lines. A root-cause note of two sentences: what was wrong, and why the whole file was skipped.
   - Hint: read the plugin components documentation for the exact shape of `extensionToLanguage`.

4. **Test the server without Claude (about 10 minutes).** Goal: show that the server and your config work before you blame Claude Code.
   - `python lsp_smoke.py pylsp-plugin-starter sample-project/app/report.py`, then ask for a definition with `--definition LINE:COL` at a use of `rate_for` in `app/billing.py`.
   - Acceptance criteria: diagnostics for `app/report.py` include an unused import and an undefined name. A definition lookup for `rate_for` points at `app/tax.py`.

5. **Prove it inside a session (about 20 minutes).** Goal: diagnostics and navigation in Claude Code.
   - Restart the session with `claude --plugin-dir`. Ask Claude to make an edit that introduces an error, then fix it. Ask where `rate_for` is defined and what calls it.
   - Acceptance criteria:
     - After an edit, the conversation shows a `Found N new diagnostic issues` line. Open it with Ctrl+O and read the issue.
     - For the navigation question, the transcript shows Claude using the `LSP` tool instead of searching text. Capture it.
   - Hints: the server starts the first time Claude edits a file with one of your extensions. If the binary was missing when the session started, start a new session from a shell where it is on the PATH.

6. **Stretch (about 10 minutes, optional).** Goal: meet the conflict case.
   - Add a second entry that claims `.py` and read the warning the Errors tab shows. Restore the file.
   - Acceptance criteria: you can say which server handles `.py` files and why.

**Checkpoint:** Working diagnostics and navigation inside a session, with the evidence from steps 4 and 5.

**Common problems:**

- No diagnostics and no error line: the server is not on the PATH of the shell that started `claude`, or `pylsp` was installed without its checks. `claude --debug` logs `LSP server <name> failed to start` when the binary is missing.
- `Executable not found in $PATH` in the Errors tab: the same cause. Install the server, then start a new session from a shell where it is found.
- `Invalid LSP server config for ".lsp.json"` in the Errors tab: an entry is invalid and the whole file was skipped.
- `claude plugin validate` passes and nothing works: it does not read `.lsp.json`.
- Edits to `.lsp.json` do nothing: restart the session, or run `/reload-plugins` where it applies.
- Diagnostics appear in the smoke test and not in the session: the shell that started `claude` has a different PATH from the one you tested in.
- A cloud session shows no diagnostics: Claude Code does not start plugin language servers in cloud sessions. Use a terminal session.
- The server prints logs to standard output and Claude Code disconnects it: a language server must log to standard error.

**Scoring rubric (100 points):**

| Item | Points |
|---|---|
| Root cause stated correctly, with the reason the whole file was skipped | 15 |
| `check_lsp.py` has no FAIL lines | 20 |
| Smoke test shows the diagnostics and the definition | 15 |
| In-session diagnostics line shown, and the issue read | 20 |
| In-session navigation shown through the `LSP` tool | 15 |
| Explains why `validate` passed, and where an invalid file is reported | 10 |
| Stretch: conflict warning read and explained | 5 |

**Facilitator note:** The default misconfiguration (variant A) is in `pylsp-plugin-starter/.lsp.json`: the keys of `extensionToLanguage` are `py` and `pyi`, with no leading dot. That makes the whole file invalid, so the plugin loads with no language server. `facilitator/lsp.fixed.json` is the fix. For a second round or a class that finishes early, swap in `facilitator/lsp.variant-b-wrong-binary.json`, whose `command` is `python-lsp-server`, a name that is not on the PATH, so the symptom is `LSP server python-pylsp failed to start` in the debug log. `check_lsp.py` reports both.

Confirmed locally while building this lab: `pylsp` started with no arguments serves the protocol on standard input and output, and with `python-lsp-server` 1.15.0 and its pyflakes and pycodestyle extras the smoke test reports `'json' imported but unused`, `'os' imported but unused` and `undefined name 'grand_total'` for `app/report.py`, and a definition for `rate_for` in `app/tax.py`. Rehearse the in-session part on your class machines: the `Found N new diagnostic issues` line is documented, and the `LSP` tool is documented, and neither has been run for this lab.

Why Python and `pylsp`: students already have Python, and the server is a free install. An official Python plugin exists, so say plainly that in real work you would install it, and that this lab is about authoring the file. For a student who works in another language, let them pick it if a free server exists, and then make the one deliberate misconfiguration yourself.

Unconfirmed: the nine LSP operation names in the old outline. Do not teach them. The documentation names diagnostics and code navigation, and the course sticks to those words. Rehearse what the `LSP` tool reports on your version and say that it is read-only.

---

## Lab 5 (take-home): Enterprise Migration Runbook

**Learning objective:** Draft the cutover plan for a fictional team moving from Console to Enterprise, covering identity, roles, managed settings, credentials, CI, and export of Console reporting. Time: about 60 minutes at home.

**Files:** `$FILES/lab5-migration`: `scenario-sheet.md`, `runbook-template.md`, `rubric.md`.

**Context:** The scenario sheet describes Larkspur Freight Software: team size, an identity provider, CI on GitHub Actions and GitLab, managed settings needs, and five credentials in use. You write the runbook a teammate could run on cutover day. The steps come from the course: provision seats and SCIM group mappings and sync; confirm Claude Code is enabled and set `forceLoginOrgUUID` in managed settings; remove leftover Console credentials such as API key variables and `apiKeyHelper`; `/login`, choose the Enterprise organization, and verify with `/status`; move CI to a `claude setup-token` credential or keep Console keys for automation; remove migrated users from the Console organization. Analytics and API keys do not carry over, so export Console reporting first. CLI session history is local and needs no migration. Spend limits are out of scope. This lab is about the order of the steps and what breaks if you do them early.

**Steps:**

1. Read `scenario-sheet.md` and list every constraint and every trap you can find, before you write.
2. Fill in `runbook-template.md`. Goal: a runbook that is exact about order, owner, time and the check that proves each step.
3. Score it yourself against `rubric.md`. Fix the lowest area.
4. Optional: bring it to the next session, or send it to your instructor.

Acceptance criteria and hints:

- Every credential C1 to C5 has a decision, a reason and a step.
- Every ordering in the plan has its reason stated. Ask, for each step, what fails if it runs first.
- Where you need a product detail you cannot source, write "to confirm". Do not invent product behavior or role names.
- Ask which credentials are tied to a person, and what happens when that person leaves.
- Ask what a subscription token is tied to, and whether it fits a secret shared by 14 repositories.
- Ask what you can enforce on a laptop the company does not manage.

**Checkpoint:** A completed runbook that scores at least 75 on the rubric.

**Common problems:**

- A runbook that lists tasks and no order: the rubric gives its largest share to order and reasons.
- A plan that removes users from Console first: reporting is lost and CI can break.
- A plan that locks sign-in to the Enterprise organization before seats are provisioned and synced: people cannot sign in.
- A plan that leaves `ANTHROPIC_API_KEY` or `apiKeyHelper` in place: an old credential can keep working instead of the new sign-in.
- A plan that designs spend caps: out of scope here.

**Scoring rubric:** See `rubric.md`. It is out of 100, with deductions for scope creep and for unsourced claims presented as fact.

**Facilitator note:** `facilitator/model-answer-outline.md` lists the traps and what a strong answer does. The traps are: the export must come first, the sign-in lock must follow provisioning, the contractors are not in the identity provider and use unmanaged laptops, three tokens are tied to people who are leaving or are contractors, an organization-wide secret should be an API key, the Console organization may need to stay for CI until each pipeline has moved, and leftover credentials must go. Instructor-only: any demonstration in a tenant or an organization. This lab is paper only.

Some ordering reasons in the rubric are operational reasoning about what fails if a step runs early. The verified facts list the steps and what does not carry over. They do not list failure behavior, so do not present that reasoning as product documentation. Unconfirmed items students may meet: contribution-metric definitions and how they attach to GitHub, spend-alert thresholds, pooled group budgets, and GitLab mention-driven trigger setup beyond the documented webhook pattern. Mark answers that state these as fact.

For students who want to check a laptop in their own life, `$FILES/demo9-cutover/leftover_credentials_check.py` lists the names of leftover credentials without printing values.
