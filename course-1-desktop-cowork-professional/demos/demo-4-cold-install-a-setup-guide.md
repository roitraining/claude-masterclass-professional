# Demo 4: Cold-Install a Setup Guide

**Course:** Claude Desktop Professional, Plugin and Extension Engineering (Claude MasterClass Professional, Course 1)
**Demo:** 4 of 8
**Time:** about 12 minutes

> Part of **[Claude Desktop Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Find the step a setup guide leaves out by having Claude follow it as a new hire with no author present, then fix the guide and confirm the stall is gone. Time: about 12 minutes.

**Files:** [`$FILES/autopsy-plugin/SETUP.md`](../demo-files/autopsy-plugin/SETUP.md), [`$FILES/autopsy-plugin/.mcp.json`](../demo-files/autopsy-plugin/.mcp.json), [`$FILES/autopsy-plugin/.claude-plugin/plugin.json`](../demo-files/autopsy-plugin/.claude-plugin/plugin.json), [`$FILES/gauntlet/gauntlet.py`](../demo-files/gauntlet/gauntlet.py), [`$FILES/gauntlet/evals/1-board-pack-builder/cold-1-install/prompt.md`](../demo-files/gauntlet/evals/1-board-pack-builder/cold-1-install/prompt.md).

**Context:** A setup guide that works for its author proves nothing. The author already has the data folder set. A cold install is a walk-through by someone, or something, that has only the plugin folder and the guide. The Gauntlet's cold-install case gives Claude a copy of the plugin and asks it to mark each step OK or STUCK.

**Steps:**

1. Read the guide, then read where the plugin needs a setting. Ask the class what a new hire must do that the guide does not say:

```
cat $FILES/autopsy-plugin/SETUP.md
cat $FILES/autopsy-plugin/.mcp.json
```

2. Run the cold-install case only, one run, capped at 1 dollar:

```
python $FILES/gauntlet/gauntlet.py --plugin $FILES/autopsy-plugin --product 1 --only cold --runs 1 --max-cost-usd 1 --out ~/work/cold-run-1
```

3. Open the HTML report that `claude plugin eval` wrote under `~/work/cold-run-1/claude-eval-results` and read each STEP line and the grader verdicts.
4. Fix a copy of the guide. Copy the plugin, add a Configure section that says to set `data_dir` (the plugin's setting `${user_config.data_dir}`), give the command, and add an expected result to Verify:

```
cp -r $FILES/autopsy-plugin ~/work/autopsy-fixed
```

5. Run the same command against the copy, with `--out ~/work/cold-run-2`, and compare.

**Fallback if the eval run does not behave:** open a clean `claude` session in an empty folder, copy the plugin folder in, and paste the prompt from `cold-1-install/prompt.md`, replacing `plugin-copy` with the copied folder name.

**Expected result:** The first run reports a STUCK line at the step that should set the data folder, `RESULT: STUCK`, and the graders for no stuck steps and for readiness fail. After the fix the run reports `RESULT: READY`.

> **Instructor note:** The case relies on `context.add_dirs` giving Claude read access to the copied folder, and on `claude plugin eval` accepting the case files as written. Both follow the eval documentation, and neither could be run here because the build environment was not signed in, so treat this as needing rehearsal. The case cannot run commands. It checks that each step is stated and unambiguous, not that it works on a machine. Say that out loud. The setting is also relevant to surfaces: a plugin whose MCP server uses `${user_config.*}` with no default loads and prompts in Claude Code, but Cowork ignores it without a default and does not prompt. That is the most common real cause of a cold-install failure in Cowork.

> **Why this matters:** The first person to install your plugin is not you. A guide that survives a stranger is cheaper than the support messages it prevents.

---

**Previous:** [Demo 3: Add a Sub-Agent and a Slash Command](demo-3-add-a-sub-agent-and-a-slash-command.md) · **Next:** [Demo 5: Package a Server as an Extension](demo-5-package-a-server-as-an-extension.md)


*Demo 4 of 8*
