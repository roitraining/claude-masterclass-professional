# Demo 1: Scaffold a Plugin and Load It

**Course:** Claude Desktop Professional, Plugin and Extension Engineering (Claude MasterClass Professional, Course 1)
**Demo:** 1 of 8
**Time:** about 12 minutes

> Part of **[Claude Desktop Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Create a plugin from an empty folder, validate it, load it for a single session without installing it, and find a layout mistake from what the tools report. Time: about 12 minutes.

**Files:** [`$FILES/demo-snippets/.claude-plugin/plugin.json`](../demo-files/demo-snippets/.claude-plugin/plugin.json) (reference only; you write your own live).

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

**Next:** [Demo 2: Add Components, Then Validate](demo-2-add-components-then-validate.md)


*Demo 1 of 8*
