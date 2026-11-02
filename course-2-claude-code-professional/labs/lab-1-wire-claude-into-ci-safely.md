# Lab 1: Wire Claude into CI Safely

> Part of **[Claude Code Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

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
