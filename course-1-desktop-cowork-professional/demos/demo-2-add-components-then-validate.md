# Demo 2: Add Components, Then Validate

**Course:** Claude Desktop Professional, Plugin and Extension Engineering (Claude MasterClass Professional, Course 1)
**Demo:** 2 of 8
**Time:** about 12 minutes

> Part of **[Claude Desktop Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Add a skill and a local MCP connector to a plugin, check them with the server self-test and the validator, and read the component inventory and the always-on cost. Time: about 12 minutes.

**Files:** [`$FILES/starter-server`](../demo-files/starter-server), [`$FILES/demo-snippets/.mcp.json`](../demo-files/demo-snippets/.mcp.json), [`$FILES/demo-snippets/skills/records-check/SKILL.md`](../demo-files/demo-snippets/skills/records-check/SKILL.md).

**Context:** A local MCP server is a program that Claude starts and talks to over standard input and output. A plugin declares it in `.mcp.json`. The plugin's folder path is available as `${CLAUDE_PLUGIN_ROOT}`. The always-on cost is what the plugin puts in the context window on every turn, before anyone asks it anything.

**Steps:**

1. Copy the starter server into the plugin and test it without Claude:

```
cp -r $FILES/starter-server ~/work/records-desk/server
cd ~/work/records-desk/server && python3 test_server.py && cd ..
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

**Previous:** [Demo 1: Scaffold a Plugin and Load It](demo-1-scaffold-a-plugin-and-load-it.md) · **Next:** [Demo 3: Add a Sub-Agent and a Slash Command](demo-3-add-a-sub-agent-and-a-slash-command.md)


*Demo 2 of 8*
