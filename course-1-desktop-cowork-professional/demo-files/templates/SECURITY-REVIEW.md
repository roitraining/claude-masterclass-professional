# Security review: <plugin-name> <version>

Only needed if the plugin has `hooks/` or ships other code beyond the connector. Remove `bin/`: a plugin with a `bin/` folder cannot be installed in Cowork or chat.

## Hooks

| File | Event | Command it runs | Why it is needed | What it can touch |
|---|---|---|---|---|
| hooks/hooks.json | <event> | <command> | <reason> | <files or network> |

## Connector

- Server: `<server>`, started by `.mcp.json` with `<command and args>`.
- Reads: <folders>. Writes: <none or list>. Network: <none or list>.
- Settings it needs from the user: <list>. Sensitive values are stored by the extension settings, never in the folder.

## Reviewer

Reviewed by <name> on <date>. Files read: <list>.
