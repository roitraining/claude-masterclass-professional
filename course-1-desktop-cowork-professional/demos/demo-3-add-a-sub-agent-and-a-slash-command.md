# Demo 3: Add a Sub-Agent and a Slash Command

**Course:** Claude Desktop Professional, Plugin and Extension Engineering (Claude MasterClass Professional, Course 1)
**Demo:** 3 of 8
**Time:** about 12 minutes

> Part of **[Claude Desktop Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Add a read-only agent and a writer agent with a handoff contract, add a slash command that triggers the workflow, and say how each surface treats agents and commands. Time: about 12 minutes.

**Files:** [`$FILES/demo-snippets/agents/record-auditor.md`](../demo-files/demo-snippets/agents/record-auditor.md), [`$FILES/demo-snippets/agents/summary-writer.md`](../demo-files/demo-snippets/agents/summary-writer.md), [`$FILES/demo-snippets/commands/audit.md`](../demo-files/demo-snippets/commands/audit.md).

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

**Previous:** [Demo 2: Add Components, Then Validate](demo-2-add-components-then-validate.md) · **Next:** [Demo 4: Cold-Install a Setup Guide](demo-4-cold-install-a-setup-guide.md)


*Demo 3 of 8*
