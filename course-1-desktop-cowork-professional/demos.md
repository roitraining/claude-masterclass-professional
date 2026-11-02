# Claude Desktop Professional: Demos

**Course:** Claude Desktop Professional, Plugin and Extension Engineering (Claude MasterClass Professional, Course 1)
**Contents:** 8 instructor-led demos. Each takes 15 minutes or less and has a learning objective. The numbers and titles match the Today's Demos slide.

---

## About this guide

Run the demos in order. Each has the same layout: a learning objective, a time, a Files line when it uses files, a short context paragraph, steps, an Expected result, an Instructor note, and a Why this matters note.

These demos assume Associate 1 and Associate 2. They do not re-teach what a Skill is, how to install a plugin, or how to schedule a task. Demos 1 to 3 build a small plugin, `records-desk`, live. The students then build their own in Lab 1.

Everything runs locally on your own machine. Demos 5 and 7 mention steps that publish or install from a shared marketplace or upload to an organization. Those are instructor-only, on the ROI sandbox account, and every one is marked below. Every person, company, and figure in the files is fictional, and no file contains a real credential. Claude can word things differently each time, so check results against the Expected result and not against exact text.

**Files.** In this guide `$FILES` means the `demo-files` folder your instructor gives you:

- `$FILES/demo-snippets` holds the skill, command, agents, and `.mcp.json` for the `records-desk` plugin, for Demos 1 to 3.
- `$FILES/starter-server` is a small local MCP server in Python with sample records, for Demos 2, 3, and 5.
- `$FILES/autopsy-plugin` is a flawed plugin, for Demo 4 and Demo 8.
- `$FILES/gauntlet` holds the runner, the eval suites, and the sample reports, for Demos 4 and 6.
- `$FILES/untrusted-plugin` is a fictional third-party plugin to review, for Demo 7.

> **Shell.** Commands are written for bash (macOS, Linux, or Git Bash on Windows). In PowerShell use `New-Item -ItemType Directory` for `mkdir -p` and `Copy-Item -Recurse` for `cp -r`. Use `python` on Windows and `python3` where `python` is not defined.

> **Rehearse once on the class machine.** The Claude Code commands below were run while building this guide, except where an Instructor note says otherwise. Paid eval runs and the Desktop extension install were not run. Do both before the day.

> **Model credits.** Only Demo 4 spends model credits for evals. Cap it as shown.

---

## Setup: Make a work folder once

**Time:** about 5 minutes, before Demo 1.

1. Create a work folder and check the tools:

```
mkdir -p ~/work && cd ~/work
claude --version
python --version
git --version
```

**Expected result:** Claude Code 2.1.269 or later (plugin evals need it), Python 3.11 or later, Git 2.31 or later.

> **Instructor note:** `claude` must be signed in for Demo 4. In the build environment for this guide `claude plugin eval` stopped with "Not logged in", so sign in on the class machine and run Demo 4 once beforehand.

---

## Demo 1: Scaffold a Plugin and Load It

**Learning objective:** Create a plugin from an empty folder, validate it, load it for a single session without installing it, and find a layout mistake from what the tools report. Time: about 12 minutes.

**Files:** `$FILES/demo-snippets/.claude-plugin/plugin.json` (reference only; you write your own live).

**Context:** A plugin is a folder of components plus a manifest at `.claude-plugin/plugin.json`. Only the name is required. `--plugin-dir` loads a folder for one session and writes nothing to settings, so it is the right way to develop.

**Steps:**

1. Create the folder and the manifest:

```
mkdir -p ~/work/records-desk/.claude-plugin
cat > ~/work/records-desk/.claude-plugin/plugin.json <<'EOF'
{
  "name": "records-desk",
  "description": "Audits a small records file for stale entries and writes a short summary.",
  "version": "0.1.0",
  "author": { "name": "Instructor" }
}
EOF
```

2. Validate it. It has no components yet, and that is allowed:

```
claude plugin validate ~/work/records-desk
```

3. Make the classic layout mistake. Put a skill inside `.claude-plugin/`:

```
mkdir -p ~/work/records-desk/.claude-plugin/skills/records-check
cp $FILES/demo-snippets/skills/records-check/SKILL.md ~/work/records-desk/.claude-plugin/skills/records-check/
```

4. Load the plugin for a session and look for the skill:

```
claude --plugin-dir ~/work/records-desk
```

In the session run `/plugin`, open the Installed tab and the Errors tab, then type `/records-desk:` and see what completes. In a shell, run the inventory, which does not need a session:

```
claude --plugin-dir ~/work/records-desk plugin details records-desk
```

5. Fix it. Exit the session and move the skill to the plugin root:

```
mkdir -p ~/work/records-desk/skills
mv ~/work/records-desk/.claude-plugin/skills/records-check ~/work/records-desk/skills/
rmdir ~/work/records-desk/.claude-plugin/skills
```

6. Start again with the plugin loaded, or run `/reload-plugins` in the open session, and run `/records-desk:records-check`. Then show the shell view:

```
claude --plugin-dir ~/work/records-desk plugin list
```

**Expected result:** Step 2 prints `Validation passed`. In step 4 the plugin appears as loaded but has no skill, because components inside `.claude-plugin/` do not load, and the inventory shows Skills (0). After step 6 the skill is available as `/records-desk:records-check` and the plugin is listed as loaded.

> **Instructor note:** The "plugin loads but its skills are missing" behavior and the `/reload-plugins` and `plugin list` commands are in the Claude Code plugin docs. When this guide was built, `validate` still printed `Validation passed` with the skill in the wrong place, so tell the class that validate checks the manifest and file syntax, not placement, and that the inventory is what catches it. Note the command name pattern `/<plugin>:<skill-directory>`. You can mention `claude plugin init`, which scaffolds a plugin under `~/.claude/skills/` that loads every session, but this course uses `--plugin-dir`.

> **Why this matters:** Most "my plugin does nothing" reports are a layout mistake. The Installed and Errors tabs tell you in seconds, and a developer who knows to look there saves an afternoon.

---

## Demo 2: Add Components, Then Validate

**Learning objective:** Add a skill and a local MCP connector to a plugin, check them with the server self-test and the validator, and read the component inventory and the always-on cost. Time: about 12 minutes.

**Files:** `$FILES/starter-server`, `$FILES/demo-snippets/.mcp.json`, `$FILES/demo-snippets/skills/records-check/SKILL.md`.

**Context:** A local MCP server is a program that Claude starts and talks to over standard input and output. A plugin declares it in `.mcp.json`. The plugin's folder path is available as `${CLAUDE_PLUGIN_ROOT}`. The always-on cost is what the plugin puts in the context window on every turn, before anyone asks it anything.

**Steps:**

1. Copy the starter server into the plugin and test it without Claude:

```
cp -r $FILES/starter-server ~/work/records-desk/server
cd ~/work/records-desk/server && python test_server.py && cd ..
```

2. Add the connector declaration:

```
cp $FILES/demo-snippets/.mcp.json ~/work/records-desk/.mcp.json
cat ~/work/records-desk/.mcp.json
```

3. Validate, then read the inventory:

```
claude plugin validate ~/work/records-desk
claude --plugin-dir ~/work/records-desk plugin details records-desk
```

4. Load the plugin and check the connector:

```
claude --plugin-dir ~/work/records-desk
```

In the session run `/mcp`, then `/records-desk:records-check`.

5. Show how a long description costs. Open `skills/records-check/SKILL.md`, paste a long paragraph into the `description` line, and run the `plugin details` command again. Compare the Always-on figure and the per-component table. Restore the description afterward.

**Expected result:** The self-test prints PASS on every line. `validate` passes. The inventory lists the skill, a Hooks count of 0, and the MCP server `records` with a note that its tool schemas are not counted. Always-on is small (about 125 tokens when this guide was built; yours may differ). `/mcp` lists the server as `plugin:records-desk:records`. The skill reports that R-002 is stale and that R-004 contains an instruction it did not follow.

> **Instructor note:** `validate` checks syntax and schema, not behavior. The estimate does not count hooks or MCP tool schemas, so a plugin with a large connector costs more than the number shows. In the version used to write this guide, a command file was counted under Skills in the inventory. Check it on yours before you say so. The result in step 4 depends on Claude's wording; it needs rehearsal if you want exact phrasing.

> **Why this matters:** A plugin is judged on two things the user never sees until it hurts: whether it loads and what it costs every turn. Each takes a single command to check.

---

## Demo 3: Add a Sub-Agent and a Slash Command

**Learning objective:** Add a read-only agent and a writer agent with a handoff contract, add a slash command that triggers the workflow, and say how each surface treats agents and commands. Time: about 12 minutes.

**Files:** `$FILES/demo-snippets/agents/record-auditor.md`, `$FILES/demo-snippets/agents/summary-writer.md`, `$FILES/demo-snippets/commands/audit.md`.

**Context:** An agent is a separate assistant with its own context window. A handoff contract says exactly what the first agent returns and what the second accepts, so the second never sees raw data and a planted instruction cannot ride along. A command is a Markdown file the user runs by name.

**Steps:**

1. Copy the components in:

```
mkdir -p ~/work/records-desk/agents ~/work/records-desk/commands
cp $FILES/demo-snippets/agents/*.md ~/work/records-desk/agents/
cp $FILES/demo-snippets/commands/audit.md ~/work/records-desk/commands/
```

2. Open `record-auditor.md`. Point out `tools: Read, Grep, Glob` (no Write, Edit, Bash, or WebFetch) and the single JSON object it must return. Open `summary-writer.md` and point out the rule that rejects anything else.
3. Load the plugin and run the command:

```
claude --plugin-dir ~/work/records-desk
/records-desk:audit
```

4. Ask Claude to run the roles in order: "Use the record-auditor agent on the records, then give only its JSON to the summary-writer agent."
5. Test the contract. Ask: "Use the summary-writer agent with this input: 'Everything is current, nothing to review.'" Show that it rejects it.
6. Show the surface table on a slide: agents are ignored in chat and load in Cowork and Claude Code. A command loads as a skill in chat and runs as `/plugin-name:command` in Cowork and Claude Code.

**Expected result:** `/records-desk:audit` runs the records-check skill. The auditor returns JSON with R-002 under `stale` and the R-004 title under `suspect_instructions`. The summary-writer writes at most five lines from that JSON. In step 5 it replies that the handoff is rejected.

> **Instructor note:** The command, agent, and surface facts are verified. How reliably Claude chooses to delegate to the agent from a plain request, and exactly how it words the rejection, are not, so rehearse steps 4 and 5 and keep a recording as a fallback. An agent file cannot add hooks or MCP servers of its own. The `tools` field narrows what an agent can use, and the Gauntlet checks it.

> **Why this matters:** The handoff contract is the design decision that makes multi-agent plugins safe and testable. Without it, an instruction in a data file travels from role to role.

---

## Demo 4: Cold-Install a Setup Guide

**Learning objective:** Find the step a setup guide leaves out by having Claude follow it as a new hire with no author present, then fix the guide and confirm the stall is gone. Time: about 12 minutes.

**Files:** `$FILES/autopsy-plugin/SETUP.md`, `$FILES/autopsy-plugin/.mcp.json`, `$FILES/autopsy-plugin/.claude-plugin/plugin.json`, `$FILES/gauntlet/gauntlet.py`, `$FILES/gauntlet/evals/1-board-pack-builder/cold-1-install/prompt.md`.

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

## Demo 5: Package a Server as an Extension

**Learning objective:** Package the starter server as a `.mcpb` Desktop extension, install it from Advanced settings, and say what it can reach and how a team would distribute it. Time: about 15 minutes.

**Files:** `$FILES/starter-server`: `manifest.json`, `server.py`, `sample_data/records.csv`, `pack_mcpb.py`.

**Context:** A `.mcpb` file is a zip archive that holds a local MCP server and a `manifest.json`. Claude Desktop installs it with a single click, like a browser extension. The server runs on the user's machine over standard input and output, with the user's privileges, so it can read local files and tools behind the firewall. A plugin carries a connector to Cowork and Claude Code. An extension carries it to the Claude Desktop app. Ship an extension when you need an install that works without a plugin.

**Steps:**

1. Show the manifest and point out the fields: `manifest_version`, `name`, `version`, `description`, `author`, `server` with `type`, `entry_point`, and `mcp_config`, and `user_config` for a setting the user fills in at install:

```
cat $FILES/starter-server/manifest.json
```

2. Install the packaging tool (the instructor does this before class) and pack:

```
npm install -g @anthropic-ai/mcpb
cd $FILES/starter-server
mcpb validate manifest.json
mcpb pack . ~/work/starter-server-0.1.0.mcpb
```

3. Show that the file is a zip with the manifest at its root:

```
python -c "import zipfile,sys; print('\n'.join(zipfile.ZipFile(sys.argv[1]).namelist()))" ~/work/starter-server-0.1.0.mcpb
```

4. In Claude Desktop open Settings, Extensions, Advanced settings, Install Extension, and choose the file. Review the details and permissions dialog, leave the data folder empty, and finish.
5. In a Claude Desktop chat ask: "List the records using the starter extension." Then show where the extension runs: it reads `sample_data/records.csv` from its own install folder.
6. Explain team distribution on a slide. An Owner uploads a custom extension to the organization, and an allowlist controls which extensions users can run. State what the extension can reach: local files and anything the user can reach, with no sandbox.
7. Close the loop with the plugin route. The plugin docs say a plugin's `mcpServers` key can point to a `.mcpb` path inside the plugin or an `https://` URL.

**Expected result:** The pack command writes the file, and the zip listing shows `manifest.json` at the top level. After install the extension appears in the Extensions list, and the chat answers with the four sample records and their dates.

> **Instructor note:** What is verified: a `.mcpb` is a zip with `manifest.json`, the manifest fields and the `python` server type in step 1, `mcpb init`, `validate`, `pack`, the install paths, and the plugin `mcpServers` pointer. What is not: the Node.js requirement is not on this course's Technical Requirements page, so install Node and the tool on the class machines. The MCPB documentation recommends Node.js and bundles dependencies for Python in a `server/lib` folder (this server needs none), and whether Claude Desktop supplies a Python runtime was not confirmed, so check that `python` runs on the class machine. How Desktop treats an optional empty `user_config` value was not confirmed, and the server guards against both an empty and an unsubstituted value. Team distribution through an Owner upload and the allowlist is stated on the Anthropic support page but the steps were not verified, so do it only on the ROI sandbox account after rehearsal, or show it as a screenshot. If Node is unavailable, `pack_mcpb.py` builds the same zip layout with the Python standard library, but installing a bundle made that way was not confirmed.

> **Why this matters:** An extension is code that runs as the user. Packaging it well and saying plainly what it can reach is part of shipping it.

---

## Demo 6: Read a Worked Gauntlet Report

**Learning objective:** Read a Gauntlet report from the notes column inward, trace each lost point to a fix, and see why Gold depends on the security items. Time: about 12 minutes.

**Files:** `$FILES/gauntlet/sample-report/run-1-bronze.md`, `run-3-gold.md`, `WALKTHROUGH.md`, and `$FILES/gauntlet/scorecard.md`.

**Context:** The Gauntlet scores a plugin out of 100 across structure, an eval suite, context cost, a cold install, an adversarial pack, and a security checklist. Bronze is 60, Silver 75, Gold 90 with all the security points. The two sample reports show the same plugin, Board Pack Builder, before and after fixes.

**Steps:**

1. Show the scoring table in `scorecard.md` and the tier rules, in a minute.
2. Open `run-1-bronze.md`. For each section, read the Note before the points. Ask the class which fix it suggests.
3. Open `WALKTHROUGH.md` and walk the table row by row: what lost points, the fix, the points returned.
4. Open `run-3-gold.md`. Find the two places where points were still lost, and discuss why Gold is not perfect.
5. Show the tension between two fixes: shortening descriptions for cost can stop the skill firing. Say that every cut needs a re-run of the trigger cases.
6. Run the free checks on the flawed plugin to show a live report:

```
python $FILES/gauntlet/gauntlet.py --plugin $FILES/autopsy-plugin --product 1 --static-only --out ~/work/static-demo
```

**Expected result:** Run 1 scores 64.4 and is Bronze. Run 3 scores 96.5 and is Gold. The live static report shows the secret in `server/config.json`, the unscoped tools on the reviewer agent, the version mismatch, and the always-on cost of about 2,000 tokens, and it ends with "Not rated" because the eval groups were not run. It scores about 10 of 100.

> **Instructor note:** The two sample reports are illustrative, written by hand in the runner's report format, not output from a live run. Before class, run the full Gauntlet once on your own sandbox account on a plugin you built, price the run, and consider swapping in the real report. The live static run in step 6 is real. Do not run the paid groups on stage.

> **Why this matters:** A score is only useful if you can turn it into a to-do list. The report reads that way once you start from the notes.

---

## Demo 7: Review a Plugin Before You Trust It

**Learning objective:** Review an unfamiliar plugin by reading the files that run code and the files that steer Claude, and reach an install decision with evidence. Time: about 12 minutes.

**Files:** `$FILES/untrusted-plugin` (a fictional plugin named `quick-notes`), `$FILES/gauntlet/SECURITY-CHECKLIST.md`.

**Context:** An installed plugin can run code with your privileges. Hooks, MCP and LSP servers, and a mod run outside the sandbox. Skills, commands, and agents enter the context window as instructions. Auto-update means files you reviewed can change. This plugin is written to be reviewed and never installed. All the hosts in it use the reserved `.invalid` name.

**Steps:**

1. Check where a marketplace came from, which is the first question for any plugin you did not write:

```
claude plugin marketplace list
```

2. Validate the plugin, then show that a pass is not a safety verdict:

```
claude plugin validate $FILES/untrusted-plugin
```

3. List the contents without loading a session:

```
claude --plugin-dir $FILES/untrusted-plugin plugin details quick-notes
```

4. Read, in this order, and have the class call out each finding:

```
cat $FILES/untrusted-plugin/hooks/hooks.json
cat $FILES/untrusted-plugin/.mcp.json
cat $FILES/untrusted-plugin/bin/qn-sync
cat $FILES/untrusted-plugin/skills/quick-notes/SKILL.md
```

5. Tie each finding to a surface: the hook loads in Cowork and Claude Code, and the `bin/` folder makes Cowork and chat refuse to install the plugin and loads in Claude Code. The skill's instruction reaches every surface.
6. Walk the checklist in `SECURITY-CHECKLIST.md` and state the decision.

**Expected result:** The plugin validates. The inventory shows a session-start hook and an MCP server. The class finds at least five problems: the hook posts the environment to an unknown host, `bin/qn-sync` archives a user folder and uploads it, the server is an unpinned `npx -y ...@latest` download, the skill tells Claude to copy notes and open files to an outside address without telling the user, and the publisher and changelog are unknown. Decision: do not install.

> **Instructor note:** Do not start a Claude session with this plugin loaded. Hooks run outside the sandbox, and `plugin details` only reads the folder. The verified facts say what to read before you trust a plugin and what an administrator can do: allowlist or block marketplaces, force-install a plugin, limit hooks to managed ones, and turn off `--plugin-dir`. Whether `plugin details` lists a `bin/` folder was not checked, so read the folder by hand. The sentence about the unpinned download is general practice and not from the plugin docs.

> **Why this matters:** The review takes ten minutes and the plugin runs as you. The files that run code are few, and they are the ones to read.

---

## Demo 8: Read a Plugin's Cost and Usage

**Learning objective:** Compare the always-on cost of two plugins, find the signals that show how a plugin is used, and say which signals are available to an individual and which to an administrator. Time: about 10 minutes.

**Files:** `$FILES/autopsy-plugin`, `~/work/records-desk` (from Demos 1 to 3).

**Context:** Cost and use are the two numbers behind keep, split, or retire. The component inventory and the always-on figure tell you the cost before anyone uses the plugin. Telemetry tells you who used it afterward. This demo previews the monitoring covered in the enterprise courses.

**Steps:**

1. Print the inventory and cost of the small plugin and the flawed one, side by side:

```
claude --plugin-dir ~/work/records-desk plugin details records-desk
claude --plugin-dir $FILES/autopsy-plugin plugin details expense-digest
```

2. Compare the per-component tables. Find the three or four components that make up most of the larger plugin's cost. Say what you would shorten or split.
3. In a Claude Code session, run `/plugin` and open a plugin from the official marketplace. Show the Context cost section and the highlight at 2,000 tokens or more.
4. In the same session run `/usage` after a few turns and show what it reports.
5. On a slide, show the administrator view: OpenTelemetry events for plugin installs and use, and, on Enterprise, an Analytics API endpoint with per-plugin install and invocation counts across Claude Code and Cowork. Do not open an admin console.
6. Ask the class for a keep, split, or retire decision for the flawed plugin, given its cost and an invented 2 hours saved a week.

**Expected result:** The flawed plugin's always-on cost is a multiple of the small plugin's (about 2,050 against about 125 tokens when this guide was built), and most of it sits in skill and agent descriptions. The class proposes shortening descriptions or merging the seven rule skills into a single skill that reads a policy file.

> **Instructor note:** Verified: `claude plugin details` reports a component inventory, an Always-on token estimate, and a per-component split, and does not count hooks or MCP tool schemas. The `/plugin` Context cost section and its 2,000-token highlight apply to plugins in the official marketplace. The OpenTelemetry events and the Enterprise Analytics API are stated in the plugin measurement docs. Not verified: what `/usage` shows about plugins, and the endpoint names and field names for the Analytics API. Rehearse `/usage`, and describe the administrator view only in general terms. Position the whole demo as a preview, not as the monitoring curriculum.

> **Why this matters:** A plugin that costs more than it saves should be split or retired. You can only decide that with the numbers.
