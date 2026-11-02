# Demo 5: Package a Server as an Extension

**Course:** Claude Desktop Professional, Plugin and Extension Engineering (Claude MasterClass Professional, Course 1)
**Demo:** 5 of 8
**Time:** about 15 minutes

> Part of **[Claude Desktop Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Package the starter server as a `.mcpb` Desktop extension, install it from Advanced settings, and say what it can reach and how a team would distribute it. Time: about 15 minutes.

**Files:** [`$FILES/starter-server`](../demo-files/starter-server): `manifest.json`, `server.py`, `sample_data/records.csv`, `pack_mcpb.py`.

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

**Previous:** [Demo 4: Cold-Install a Setup Guide](demo-4-cold-install-a-setup-guide.md) · **Next:** [Demo 6: Read a Worked Gauntlet Report](demo-6-read-a-worked-gauntlet-report.md)


*Demo 5 of 8*
