# Claude Code Professional: Demos

**Course:** Claude Code Professional: Pipelines, Plugins and Enterprise Operations (Claude MasterClass Professional, Course 2)
**Contents:** 9 instructor-led demos. Each takes 15 minutes or less and has a learning objective. The numbers match the Today's Demos slide.

---

## About this guide

Run the demos in order. Each has the same layout: a learning objective, a time, a Files line when it uses files, a short context paragraph, steps, an Expected result, an Instructor note, and a Why this matters note.

These demos assume Associate 3. They do not re-teach worktrees, subagent team design, hooks basics or policy precedence. They do not teach CI fundamentals.

In this guide `$FILES` means the `demo-files` folder. Demos that touch a real GitHub or GitLab project, a cloud session, a routine or an Enterprise tenant (Demos 1, 3, 4 and 9) run on an ROI sandbox only, by the instructor, never on a student's account or a real customer project. Each has a fallback: a local simulation, a screenshot set, or a transcript outline. Demos 2, 5, 6, 7 and 8 run locally. Demos 1, 2, 3, 6 and 7 use credits when run live. Every person, company and figure in the files is fictional, and no file holds a real secret. Claude Code can word things differently each time, so check results against the Expected result and not against exact text.

> **Instructor-only.** Anything in an organization, a tenant, a routine or a cloud environment is shown by the instructor. Students watch.

> **Sandbox rule.** Never run a demo that pushes, comments or deploys against a project that is not the ROI sandbox. Pre-stage the sandbox before class and check it once.

> **Unconfirmed items.** Each Instructor note says what is unconfirmed or needs rehearsal. If an item is marked unconfirmed, say so to the class. Do not present it as fact.

---

## Demo 1: Auto-Fix From a Failing Check

**Learning objective:** Show Claude fixing a pull request whose CI check is failing, and name what lets it do that. Time: about 6 minutes.

**Files:** `$FILES/lab1-ci/tallybook` (the sample repository), staged in the ROI sandbox before class.

**Context:** `/autofix-pr` and the Auto-fix toggle watch a pull request and fix CI failures and review comments. They need the Claude GitHub App on the repository. A cloud session does the work, so the pull request must be on GitHub.

**Steps:**

1. Before class, in the ROI sandbox: copy `tallybook` into a sandbox repository, install the Claude GitHub App, add the CI workflow `.github/workflows/ci.yml`, and open a pull request that adds a small helper. CI fails on the two known failing tests.
2. In class, show the pull request with its red check. Name the two failing tests.
3. In a terminal in a clone of the sandbox repository, check out the pull request branch and start a session:

```
git checkout <pr-branch>
claude
```

4. Run `/autofix-pr` and let it attach to the pull request.
5. Wait for the new commit and the re-run of CI. Open the diff.
6. Ask the class what Claude was allowed to do, and what stopped it from merging.

**Expected result:** A new commit on the pull request branch changes `monthly_total` so the tests pass, and the check turns green. Claude does not merge the pull request.

**Instructor note:** Sandbox only, instructor only. The exact way `/autofix-pr` is pointed at a pull request, whether it asks you to choose one, and how long a fix takes are not in the verified facts. Rehearse once and time it. Fallback if it runs long or fails: a local simulation. In a local copy of `tallybook`, run `python3 -m pytest -q` to show the failures, tell Claude "make the failing tests pass and change nothing else", show the diff, and say the pipeline version of the same loop is the one you just described. A second fallback is a screenshot set of a previous run, taken during rehearsal.

**Why this matters:** Auto-fix is the first unattended action students meet. It acts on a signal (a red check) rather than on a request. That is exactly where permissions, who can trigger it, and a human review of the result need to be settled.

---

## Demo 2: Review a Pull Request With a Skill

**Learning objective:** Run a review on a pull request that has a planted bug, and read what the review found against what it should have. Time: about 8 minutes.

**Files:** `$FILES/lab2-review` (`build_fixture.py`, `facilitator/ANSWER-KEY.md`), `$FILES/demo2-review/claude-code-review.yml`.

**Context:** There are several ways to get a review: `/code-review` locally, your own CI, or the managed Code Review service. The local command reads `CLAUDE.md` files and not `REVIEW.md`. The service needs a Team or Enterprise plan, an Owner who turns it on, and GitHub. In CI, a review workflow needs `--comment` and an `--allowedTools` entry for the inline comment tool to post inline comments.

**Steps:**

1. Build the fixture and move to a bug branch:

```
python3 build_fixture.py ~/work/lending-demo
cd ~/work/lending-demo
git checkout pr-03-delete-member
```

2. Start `claude` and run `/code-review`, naming the branch as the target.
3. Compare the findings with the answer key for `pr-03-delete-member`: a handler that never calls `require_role`.
4. Open `$FILES/demo2-review/claude-code-review.yml`. Point at the two lines that decide where the review goes: `--comment` and the `claude_args` line with `--allowedTools`. Say the workflow is the documented example and is not run in class.
5. Optional: run `python3 $FILES/lab1-ci/security_gate.py $FILES/demo2-review/claude-code-review.yml`. It scores 85: no turn limit, no timeout and no concurrency group. A documented example is a start, not a finished pipeline.

**Expected result:** The review reports the missing role check on the delete handler. It may also report extra items. Count them: they are the lead-in to Lab 2.

**Instructor note:** The exact target and effort-level arguments `/code-review` accepts, and its output format, are unconfirmed. Rehearse and adjust step 2. The review uses credits. Fallback: show `$FILES/lab2-review/sample-findings.json` and run `python3 score_review.py sample-findings.json`, which needs no model. Do not demo the managed service live unless the sandbox organization is on a Team or Enterprise plan with the service turned on. If it is, `@claude review` on a sandbox pull request, by someone with write access, starts one. Zero Data Retention, HIPAA and customer-managed key configurations do not support it.

**Why this matters:** A review is only worth running if you can say what it caught and what it raised in error. This demo sets up Lab 2, where students score that.

---

## Demo 3: Start a Cloud Session and Teleport It

**Learning objective:** Start work in a cloud session from the terminal, queue a follow-up to it, and bring it back to the terminal. Time: about 10 minutes.

**Files:** None. Use the sandbox repository from Demo 1, with the branch pushed.

**Context:** `claude --cloud "<task>"` starts a session on Anthropic's cloud. It clones the GitHub remote at your current branch, so push first. `claude --teleport` (or `/teleport`, `/tp`) pulls a cloud session into your terminal. Teleport needs a clean git state, the same repository, a pushed branch and the same claude.ai account. Handoff is one way from the command line. Cloud sessions are not available through Bedrock, Vertex or other providers.

**Steps:**

1. Check the branch is pushed and the working tree is clean: `git status`.
2. Start a cloud session:

```
claude --cloud "Add a biggest_income helper to tallybook with a test. Do not change anything else."
```

3. Copy the session ID that it prints, or find the session on claude.ai.
4. Queue a follow-up to the running session from another terminal:

```
claude -p "Also add one line to the README describing the helper" --cloud <session-id>
```

5. When the session has made progress, bring it back: `claude --teleport`, choose the session, and look at the branch it checked out.
6. Say what you cannot do: hand a local session up to the cloud mid-conversation.

**Expected result:** A session runs without your terminal, accepts a queued message, and appears in your terminal after `--teleport` with its branch and conversation.

**Instructor note:** Sandbox account only. Uses cloud session usage. The cloud environment's network access, variables and setup script are set per environment, and whether the sandbox's environment lets this task finish is unknown until you rehearse. Teleport refuses on a dirty tree or a different account. The `--remote` spelling is a deprecated alias for `--cloud`. If the live run fails or is slow, use a screenshot set from rehearsal, or a transcript outline: command, session ID, queued message, teleport, resulting branch. Plugin language servers do not start in cloud sessions, which matters again in Demo 8.

**Why this matters:** Where a task runs decides what it can reach and who sees it. A cloud session is not your laptop, and moving between them is one way.

---

## Demo 4: A Routine Versus an Actions Workflow

**Learning objective:** Compare a routine and an Actions workflow that react to the same GitHub event, and choose between them. Time: about 8 minutes.

**Files:** `$FILES/demo4-routine-vs-actions/comparison.md`, `$FILES/lab1-ci/facilitator/github/claude-review.yml`.

**Context:** Routines are a research preview. They run on Anthropic infrastructure, need no workflow file, belong to a single account, can run on a schedule (one hour minimum), through an API call, or on a GitHub event, and have no permission-mode picker. An Actions workflow runs on a GitHub runner, from a file in the repository, with your secrets and your permissions block.

**Steps:**

1. Take the trigger "a pull request is opened". Open the hardened workflow `claude-review.yml` and name what governs it: permissions, who can trigger, secrets, limits.
2. In the sandbox account, show the routine's configuration screen for a GitHub event trigger. Do not save one that acts.
3. Fill in the right-hand column of `comparison.md` from what you see on screen, and the left from the course facts.
4. Ask the class to choose for three cases: a team review that must be auditable, a personal morning summary, and a pipeline whose output must start CI.
5. End on the owner question: who owns a routine when its account holder leaves.

**Expected result:** The class picks a workflow for the shared, auditable cases, and a routine only for personal automation. They name the owner as a risk.

**Instructor note:** Instructor and sandbox account only. How a routine is created and what its screens show are not confirmed in the verified facts, so the table's routine cells marked "check on screen" must be filled live or left blank. Fallback: screenshots of both configurations, or the table with only the documented rows filled in. Do not claim what a routine can or cannot grant until you have seen it.

**Why this matters:** Teams pick a place to run automation by habit. The choice decides who can review it, who can trigger it, and what happens when a person leaves.

---

## Demo 5: Find the Missing Checkpoint

**Learning objective:** Find the step in an unattended pipeline where a human checkpoint is missing, and say where one does not belong. Time: about 10 minutes.

**Files:** `$FILES/demo5-checkpoint/nightly-fix-and-ship.yml`, `$FILES/demo5-checkpoint/checkpoint-map.md`, `$FILES/lab1-ci/security_gate.py`.

**Context:** Reviewing every change locally and acting on a pipeline's behalf with nobody watching are different risks. A pipeline that Claude runs nightly can be perfectly hygienic and still ship something no person has read.

**Steps:**

1. Hand out `checkpoint-map.md`. Read `nightly-fix-and-ship.yml` with the class: a nightly schedule, Claude fixes failing tests and moves dependencies, a pull request is opened and set to merge itself, a deploy job follows.
2. Run the gate: `python3 security_gate.py nightly-fix-and-ship.yml`. It scores 100. Ask what that tells you, and what it cannot tell you.
3. Let pairs mark the table for three minutes, then take answers.
4. Settle the answers (see the instructor note).
5. Ask the second question: which steps should not get a checkpoint, and why.

**Expected result:** The class finds that the pull request merges itself and the deploy follows, so a change reaches production with no person reading it. They propose a required human approval before merge and a required reviewer on the production environment, and they leave the schedule, Claude's work and its push alone.

**Instructor note:** The answer: the missing checkpoint is between "Claude's change" and "production". The merge sets itself to complete and the deploy follows, so nobody reads the diff. Place one checkpoint at the merge (a required human approval) and one before deploy to production (a required reviewer). A subtle one: Claude can "fix" a failing test by changing the test, so the pull request review should look at test edits first. Where a checkpoint does not belong: the trigger (a schedule starts nothing new), Claude's run itself (a person mid-run defeats unattended work, and Claude's push is isolated on a branch), and opening the pull request. Rules of thumb: put the checkpoint where the change gains the power to hurt someone, and make it cheap to pass when the change is small. Branch protection and environment reviewers are repository settings that the course facts do not cover. Show them in the sandbox only after rehearsal, and do not claim how a platform enforces them.

**Why this matters:** The most expensive pipeline failures are not leaked secrets. They are changes nobody read. Hygiene scores do not measure that.

---

## Demo 6: Install a Plugin From a Marketplace

**Learning objective:** Install a plugin from a git marketplace, read what it contains before trusting it, and see what it costs in the context window. Time: about 12 minutes.

**Files:** `$FILES/lab3-plugin/facilitator/marketplace` (a marketplace named `team-tools` holding the plugin `relnotes`), `$FILES/lab3-plugin/relnotes-starter/evals/groups-by-type/scaffold.sh`.

**Context:** A marketplace is a repository with `.claude-plugin/marketplace.json`. An installed plugin can run code with your privileges. Hooks and servers run outside the sandbox, and commands and agents enter the context window as instructions. Review before installing.

**Steps:**

1. Validate the marketplace, then register it from a local path:

```
claude plugin validate $FILES/lab3-plugin/facilitator/marketplace
claude plugin marketplace add $FILES/lab3-plugin/facilitator/marketplace
claude plugin marketplace list
```

2. Before installing, read what it would run: `hooks/hooks.json` and the agent file in the plugin folder. Say what the hook runs and when.
3. Install and confirm:

```
claude plugin install relnotes@team-tools
claude plugin list
claude plugin details relnotes
```

4. Read the component inventory and the always-on token estimate. Ask which component is largest.
5. Build a small repository with commits, then run the command:

```
mkdir -p ~/work/relnotes-demo && cd ~/work/relnotes-demo
bash $FILES/lab3-plugin/relnotes-starter/evals/groups-by-type/scaffold.sh
claude
```

   In the session run `/relnotes:release-notes` and look at `RELEASE_NOTES.md`.
6. Clean up: `claude plugin marketplace remove team-tools`.

**Expected result:** The marketplace validates, the plugin installs, `details` lists a command, an agent and a hook with a token estimate, and the command writes grouped release notes with commit hashes.

**Instructor note:** To show a remote marketplace, push `facilitator/marketplace` to the ROI sandbox repository, then `claude plugin marketplace add <owner>/<repo>`. Local is the default because it needs no sandbox. Steps 1 to 4 and 6 use no credits. If credits or time are short, skip step 5. The command's behavior in step 5 is what Lab 3's evals test, and has not been run end to end in this session, so rehearse it. Windows: use Git Bash for the scaffold script, and the hook runs `python`, so use a machine where that name exists. Plugin-level marketplace auto-update means reviewed files can change later. Mention it.

**Why this matters:** A plugin is code that teammates install and depend on. Reading its hooks before trusting it is the habit that keeps a marketplace safe.

---

## Demo 7: Evaluate a Plugin With a Test Suite

**Learning objective:** Run an eval suite against a plugin, read the result, and explain what a pass bar means. Time: about 12 minutes.

**Files:** `$FILES/lab3-plugin/relnotes-starter` (the incomplete plugin), `$FILES/lab3-plugin/facilitator/marketplace/plugins/relnotes` (the finished one), `$FILES/demo7-eval/expected-run-outline.md`.

**Context:** `claude plugin eval` runs the cases in a plugin's `evals/` folder. A case is a directory with `prompt.md`, optionally `case.yaml`, and `graders/*.md`. Each case runs three times by default. Grader types include `tool_used`, `tool_order`, `regex`, `file_exists`, an LLM judge, and a baseline. `--threshold` sets the pass bar, and the exit code says whether the suite passed. Evals use credits and need Git 2.31 or later. `claude plugin validate` checks syntax and schema and does not test behavior.

**Steps:**

1. Show the case layout in `evals/groups-by-type`: `prompt.md`, `case.yaml` (with the scaffold script), and the graders. Open a `regex` grader and an `llm` grader. Say which costs nothing.
2. Run a single case against the incomplete starter plugin, with a cost cap:

```
cd $FILES/lab3-plugin/relnotes-starter
claude plugin eval evals/groups-by-type/prompt.md --scaffold --runs 1 --ablation none --no-publish --max-cost-usd 2 --allow-tools Write Edit "Bash(git *)"
```

3. Read the result: the command is a stub, so the graders for the file and its format fail.
4. Run the same case in the finished plugin, in `facilitator/marketplace/plugins/relnotes`. Compare.
5. Say why `ignores-unrelated` exists: a plugin must also stay quiet when it is not wanted.
6. Say what the pass bar is: the fraction of graders a case must reach to count, set with `--threshold`, and the exit code.

**Expected result:** The starter scores low and exits 1. The finished plugin scores at or near the threshold and exits 0.

**Instructor note:** Uses credits on the class account. `--scaffold` runs the case's Bash script on your machine, so read it first and say why it is off by default. The report is published to claude.ai by default when the account supports it, so `--no-publish` keeps it local. An exit code of 2 means a partial run, for example the cost ceiling. Whether a command is invoked through the Skill tool inside an eval, and whether the plugin's hook fires inside a run, are unconfirmed and need rehearsal. Cases that depend on either may score unpredictably. Fallback: `$FILES/demo7-eval/expected-run-outline.md` and any report you saved during rehearsal. Never present numbers from the outline as real.

**Why this matters:** A plugin that nobody tests drifts. A suite with a pass bar turns "it seems to work" into something a team can gate a release on.

---

## Demo 8: Wire In a Language Server

**Learning objective:** Configure a language server plugin, show diagnostics and navigation working, and show that `claude plugin validate` does not read `.lsp.json`. Time: about 13 minutes.

**Files:** `$FILES/lab4-lsp/facilitator/pylsp-plugin-fixed`, `$FILES/lab4-lsp/sample-project`, `$FILES/lab4-lsp/check_lsp.py`, `$FILES/lab4-lsp/lsp_smoke.py`.

**Context:** A language server plugin is an `.lsp.json` file at the plugin root. It maps a server name to a `command` (a binary found on your PATH), optional `args`, and `extensionToLanguage`. It does not install the server. With a server running, Claude gets diagnostics after edits and an `LSP` tool for code navigation. If an official code intelligence plugin covers your language, install that instead. This demo writes the file by hand to show what is inside it.

**Steps:**

1. Install the server:

```
. ~/.venvs/mc-lsp/bin/activate   # or: python3 -m venv ~/.venvs/mc-lsp && . ~/.venvs/mc-lsp/bin/activate
pip install "python-lsp-server[pyflakes,pycodestyle]"
pylsp --help
```

2. Show `.lsp.json` in `pylsp-plugin-fixed`. Point at the command, and the dots on the extensions. Run `claude plugin validate` on the plugin and note that it passes. Say it did not read this file.
3. `python3 check_lsp.py $FILES/lab4-lsp/facilitator/pylsp-plugin-fixed`
4. Test the server with no Claude involved:

```
python3 lsp_smoke.py $FILES/lab4-lsp/facilitator/pylsp-plugin-fixed $FILES/lab4-lsp/sample-project/app/report.py
```

5. In `sample-project`, start `claude --plugin-dir $FILES/lab4-lsp/facilitator/pylsp-plugin-fixed`. Ask Claude to add a line using an undefined name to `app/report.py`. Look for the `Found N new diagnostic issues` line and press Ctrl+O.
6. Ask where `rate_for` is defined and what calls it. Show that Claude uses the `LSP` tool and not a text search.
7. Break it on purpose: remove a dot from an extension in a copy, run `check_lsp.py`, and show the `/plugin` Errors tab.

**Expected result:** The smoke test prints `'json' imported but unused`, `'os' imported but unused` and `undefined name 'grand_total'` for `app/report.py`. In the session an edit produces the diagnostics line, and the navigation question is answered from the language server.

**Instructor note:** Steps 1 to 4 and 7 use no credits. Steps 5 and 6 use credits. The smoke test was run while building the files, with `python-lsp-server` 1.15.0. The in-session steps have not been run. Rehearse them, and note what the `LSP` tool reports on your version. The documentation names diagnostics and code navigation. Do not name specific protocol operations, because the old outline's list of nine is unconfirmed. Plugin language servers do not start in cloud sessions. Fallback with no model: steps 1 to 4 and 7 alone. Without an installed server, show the smoke test output from a rehearsal run.

**Why this matters:** Claude with a language server sees the type error before the build does, and navigates by symbol. The file is short and easy to get subtly wrong, and nothing but the Errors tab tells you.

---

## Demo 9: Plan a Console to Enterprise Cutover

**Learning objective:** Walk the cutover steps for a fictional team in the right order, and say what breaks if a step happens early. Time: about 15 minutes.

**Files:** `$FILES/demo9-cutover/cutover-checklist.md`, `managed-settings-snippet.json`, `leftover_credentials_check.py`.

**Context:** In a move from Console to Enterprise, identity moves to the identity provider, and seats are assigned through SCIM group mappings. The steps are: provision seats and SCIM mappings and sync; confirm Claude Code is enabled and set `forceLoginOrgUUID` in managed settings; remove leftover Console credentials; `/login`, choose the Enterprise organization, and verify with `/status`; move CI to a `claude setup-token` credential or keep Console keys for automation; remove migrated users from the Console organization. Analytics and API keys do not carry over, so export Console reporting first. CLI session history is local and needs no migration. Spend limits are covered in Professional 4, not here.

**Steps:**

1. Open `cutover-checklist.md`. Introduce Harbor Lane Studios: 12 engineers, a SAML provider, two repositories running Claude in Actions.
2. Fill the table with the class, one row at a time. For each row ask what breaks if it runs earlier.
3. Show `managed-settings-snippet.json` and say the id is a placeholder.
4. Show leftover credentials. In a throwaway shell:

```
export ANTHROPIC_API_KEY="FAKE-TOKEN-DO-NOT-USE"
python3 $FILES/demo9-cutover/leftover_credentials_check.py
unset ANTHROPIC_API_KEY
```

   The check lists names only, never values.
5. Show how a person verifies: `/login`, choose the Enterprise organization, then `/status`. `claude auth status --text` also shows how the session is authenticated.
6. In the ROI sandbox tenant, if available, show where seats and group mappings are configured. The instructor only.
7. State what is out of scope: caps and the wider policy decision.

**Expected result:** The class produces an order with reasons: export first, provision and sync, pilot, lock sign-in, remove leftover credentials, verify, move CI, and remove users from Console last. They name what does not carry over.

**Instructor note:** Instructor and sandbox tenant only. Which screens hold the seat and mapping settings is not in the verified facts, so step 6 needs rehearsal, and a screenshot set is the fallback. The "what breaks if it runs early" reasons are operational reasoning, not documented product behavior, so label them as reasoning. Contribution-metric definitions, spend-alert thresholds and pooled group budgets are unconfirmed. Do not teach them.

**Why this matters:** The risk in a migration is order. A correct list in the wrong order locks people out, loses reporting or breaks a nightly pipeline.
