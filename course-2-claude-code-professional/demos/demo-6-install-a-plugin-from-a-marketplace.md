# Demo 6: Install a Plugin From a Marketplace

**Course:** Claude Code Professional: Pipelines, Plugins and Enterprise Operations (Claude MasterClass Professional, Course 2)
**Demo:** 6 of 9
**Time:** about 12 minutes

> Part of **[Claude Code Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Install a plugin from a git marketplace, read what it contains before trusting it, and see what it costs in the context window. Time: about 12 minutes.

**Files:** [`$FILES/lab3-plugin/facilitator/marketplace`](../demo-files/lab3-plugin/facilitator/marketplace) (a marketplace named `team-tools` holding the plugin `relnotes`), [`$FILES/lab3-plugin/relnotes-starter/evals/groups-by-type/scaffold.sh`](../demo-files/lab3-plugin/relnotes-starter/evals/groups-by-type/scaffold.sh).

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

**Previous:** [Demo 5: Find the Missing Checkpoint](demo-5-find-the-missing-checkpoint.md) · **Next:** [Demo 7: Evaluate a Plugin With a Test Suite](demo-7-evaluate-a-plugin-with-a-test-suite.md)


*Demo 6 of 9*
