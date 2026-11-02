# Demo 7: Review a Plugin Before You Trust It

**Course:** Claude Desktop Professional, Plugin and Extension Engineering (Claude MasterClass Professional, Course 1)
**Demo:** 7 of 8
**Time:** about 12 minutes

> Part of **[Claude Desktop Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Review an unfamiliar plugin by reading the files that run code and the files that steer Claude, and reach an install decision with evidence. Time: about 12 minutes.

**Files:** [`$FILES/untrusted-plugin`](../demo-files/untrusted-plugin) (a fictional plugin named `quick-notes`), [`$FILES/gauntlet/SECURITY-CHECKLIST.md`](../demo-files/gauntlet/SECURITY-CHECKLIST.md).

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

**Previous:** [Demo 6: Read a Worked Gauntlet Report](demo-6-read-a-worked-gauntlet-report.md) · **Next:** [Demo 8: Read a Plugin's Cost and Usage](demo-8-read-a-plugin-s-cost-and-usage.md)


*Demo 7 of 8*
