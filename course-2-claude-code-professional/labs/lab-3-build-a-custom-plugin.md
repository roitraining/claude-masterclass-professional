# Lab 3: Build a Custom Plugin

> Part of **[Claude Code Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

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
