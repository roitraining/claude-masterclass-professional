# Demo 3: Build a Standalone MCP Server

**Course:** Claude Agent SDK Professional: Building and Evaluating Production Agents (Claude MasterClass Professional, Course 3)
**Demo:** 3 of 8
**Time:** about 15 minutes

> Part of **[Claude Agent SDK Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Build a small standalone MCP server over stdio, connect an agent to it, and say when a server is worth the overhead compared with an in-process tool. Time: about 15 minutes. (Module 5)

**Files:** [`$FILES/python/demo3_rates_server.py`](../demo-files/python/demo3_rates_server.py), [`$FILES/python/demo3_agent.py`](../demo-files/python/demo3_agent.py).

**Context:** An in-process tool runs inside your Python or TypeScript program. A standalone server is a separate process the agent starts and talks to over stdin and stdout. Choose a server when another team or language owns the tool, when several agents share it, when it needs its own dependencies or permissions, or when the tool must return structured content (Python in-process tools forward only `content` and `is_error`).

**Steps:**

1. Open `demo3_rates_server.py`. Walk through three parts: the server object, two decorated tools with specific docstrings, and `mcp.run(transport="stdio")`. Say that stdout carries the protocol, so the server logs to stderr.
2. Open `demo3_agent.py`. Show the `mcp_servers` entry: a `command` (the current Python) and `args` (the server file). Show `allowed_tools=["mcp__rates__*"]` and explain the naming form `mcp__{server}__{tool}`.
3. Run it:

```
cd $FILES/python
python3 demo3_agent.py
```

4. Read the `MCP servers at init` line. Point at the status for `rates`.
5. Read the `TOOL mcp__rates__quote_shipping` line and compare the answer with the expected 13.80 dollars.
6. Break it on purpose: change `quote_shipping` to print to stdout, run again, and show the connection failing. Revert.
7. Ask the room: which of your current tools would you move out of process, and why?

**Expected result:** The init message lists the `rates` server as connected, the agent calls `mcp__rates__quote_shipping` with `weight_kg` 3.5 and `zone` B, and the answer is 13.80 dollars.

> **Instructor note:** The tool naming, the `mcpServers` shape with `command` and `args`, the init message `status` values (`connected`, `failed`, `needs-auth`, `pending`) and the `allowedTools` wildcard are confirmed in the official MCP guide. The 30-second default connection wait (`MCP_TIMEOUT`) is also documented, which matters if a server is slow to start. **UNVERIFIED:** the standalone server library. The scripts use the official `mcp` Python package and try two import paths. Whether a tool docstring becomes the tool description, and the exact `run()` call, need rehearsal on the installed version. Whether a library tool can return structured content is also unconfirmed for the installed version; say only that Python in-process tools cannot, which is documented. Step 6 is optional: skip it if the room is slow. **Fallback:** show the server file and a recorded init line, and run only the server by itself to show it waits silently on stdin.

> **Why this matters:** A server turns a tool into a contract that any agent can use. It also moves the tool's permissions out of the agent, which Lab 2 puts to the test.

---

**Previous:** [Demo 2: A Tool the Agent Misuses](demo-2-a-tool-the-agent-misuses.md) · **Next:** [Demo 4: Retrieval Through an MCP Server](demo-4-retrieval-through-an-mcp-server.md)


*Demo 3 of 8*
