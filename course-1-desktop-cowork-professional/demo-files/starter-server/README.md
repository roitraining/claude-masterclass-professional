# Starter server

A small local MCP server for the Claude MasterClass Professional course. It uses the Python standard library only, so there is nothing to install beyond Python 3.11 or later.

## Files

- `server.py`: the stdio MCP server. It exposes two sample tools, `list_records` and `get_record`.
- `sample_data/records.csv`: four fictional records. R-002 is stale on purpose, and R-004 has an instruction planted in its title.
- `test_server.py`: starts the server the way Claude does and checks the protocol and each tool.
- `manifest.json`: an MCPB manifest for packaging the server as a Desktop extension (`type: python`).
- `pack_mcpb.py`: a fallback packer that uses only the standard library. Prefer `mcpb pack`.

## Run it

```
python test_server.py
```

You should see PASS on every line. To run against your own data folder:

```
# macOS or Linux
STARTER_DATA=/path/to/folder python test_server.py
# Windows PowerShell
$env:STARTER_DATA = "C:\path\to\folder"; python test_server.py
```

## Adapt it

1. Copy this folder into your plugin as `server/`.
2. Replace `list_records` and `get_record` with your own tools. A tool is a function that takes a dict and returns a string, plus a JSON Schema for its inputs. Register it in the `TOOLS` dict.
3. Return a clear error string when an id is unknown, so Claude can recover.
4. Log to stderr only. Writing anything else to stdout corrupts the protocol.
5. Read the data folder from an environment variable, and fall back to a folder next to the server.

## Wire it to a plugin

Declare it in the plugin's `.mcp.json`. The server name you choose becomes part of every tool name and of the `evals/mocks/<server>/` folder:

```json
{
  "mcpServers": {
    "starter": {
      "command": "python",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server/server.py"],
      "env": { "STARTER_DATA": "${CLAUDE_PLUGIN_ROOT}/data" }
    }
  }
}
```

On macOS and Linux the command may be `python3`. Say which in your `SETUP.md`.

## Package as a Desktop extension

```
npm install -g @anthropic-ai/mcpb
mcpb validate manifest.json
mcpb pack . starter-server-0.1.0.mcpb
```

Then in Claude Desktop open Settings, Extensions, Advanced settings, Install Extension, and choose the file. The bundle runs `python` from the user's machine, so Python must be on the path. If Node.js is not available, `python pack_mcpb.py . starter-server-0.1.0.mcpb` makes a zip with the same layout. That route is a fallback and has not been confirmed to install cleanly, so rehearse it.
