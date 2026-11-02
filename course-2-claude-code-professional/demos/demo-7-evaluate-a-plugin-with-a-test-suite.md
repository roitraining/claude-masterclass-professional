# Demo 7: Evaluate a Plugin With a Test Suite

**Course:** Claude Code Professional: Pipelines, Plugins and Enterprise Operations (Claude MasterClass Professional, Course 2)
**Demo:** 7 of 9
**Time:** about 12 minutes

> Part of **[Claude Code Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Run an eval suite against a plugin, read the result, and explain what a pass bar means. Time: about 12 minutes.

**Files:** [`$FILES/lab3-plugin/relnotes-starter`](../demo-files/lab3-plugin/relnotes-starter) (the incomplete plugin), [`$FILES/lab3-plugin/facilitator/marketplace/plugins/relnotes`](../demo-files/lab3-plugin/facilitator/marketplace/plugins/relnotes) (the finished one), [`$FILES/demo7-eval/expected-run-outline.md`](../demo-files/demo7-eval/expected-run-outline.md).

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

**Instructor note:** Uses credits on the class account. `--scaffold` runs the case's Bash script on your machine, so read it first and say why it is off by default. The report is published to claude.ai by default when the account supports it, so `--no-publish` keeps it local. An exit code of 2 means a partial run, for example the cost ceiling. Whether a command is invoked through the Skill tool inside an eval, and whether the plugin's hook fires inside a run, are unconfirmed and need rehearsal. Cases that depend on either may score unpredictably. Fallback: [`$FILES/demo7-eval/expected-run-outline.md`](../demo-files/demo7-eval/expected-run-outline.md) and any report you saved during rehearsal. Never present numbers from the outline as real.

**Why this matters:** A plugin that nobody tests drifts. A suite with a pass bar turns "it seems to work" into something a team can gate a release on.

---

**Previous:** [Demo 6: Install a Plugin From a Marketplace](demo-6-install-a-plugin-from-a-marketplace.md) · **Next:** [Demo 8: Wire In a Language Server](demo-8-wire-in-a-language-server.md)


*Demo 7 of 9*
