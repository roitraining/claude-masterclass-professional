# Plugin security checklist

Read this before you trust a plugin or publish your own. The Gauntlet automates the starred items; do the rest by hand.

An installed plugin can run code with your privileges. Hooks, MCP and LSP servers, and a mod run outside the sandbox. Skills, commands, and agents enter the context window as instructions, so they can steer Claude but cannot run code by themselves.

## Before you install someone else's plugin

- [ ] Where did the marketplace come from? Run `claude plugin marketplace list` and check the source.
- [ ] Read the plugin's details pane in `/plugin`, or list its contents with `claude --plugin-dir <dir> plugin details <name>`.
- [ ] Read `hooks/hooks.json`. Every hook is a command that runs on an event. Know what each runs.
- [ ] Read `.mcp.json` and the server code it starts. A local server runs as you and can read what you can read.
- [ ] Read everything under `bin/`. Executables there run in Claude Code with your privileges.
- [ ] Read each agent's `tools` line. A read-only role should not list Write, Edit, Bash, or WebFetch.
- [ ] Read the skill and command bodies for instructions that send data somewhere or ignore the user.
- [ ] Is auto-update on? Reviewed files can change on the next update.

## Before you publish your own

- [ ] * No secrets in any file: tokens, keys, passwords, private URLs. Keep real values in the extension's user configuration, marked sensitive, never in the folder.
- [ ] * No `hooks/` or `bin/`, or each one is explained in `SECURITY-REVIEW.md`. `bin/` also blocks installation in Cowork and chat.
- [ ] * Tool permissions scoped: no wildcard, no unscoped Bash, read-only roles cannot write.
- [ ] * Versions match across `plugin.json`, the changelog, and the extension manifest.
- [ ] Text from data is treated as information. Your skill says so, and your adversarial cases prove it.
- [ ] The connector reads only the folder it is given. No network calls the user did not expect.
- [ ] The extension's manifest lists what it needs from the user, and nothing else.
- [ ] Your SETUP.md says what the plugin can reach once installed.
