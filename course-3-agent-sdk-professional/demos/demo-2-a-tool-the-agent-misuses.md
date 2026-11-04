# Demo 2: A Tool the Agent Misuses

**Course:** Claude Agent SDK Professional: Building and Evaluating Production Agents (Claude MasterClass Professional, Course 3)
**Demo:** 2 of 8
**Time:** about 12 minutes

> Part of **[Claude Agent SDK Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Show a vague tool description making an agent pick the wrong tool, and a specific description fixing it. Time: about 12 minutes. (Module 3)

**Files:** [`$FILES/python/demo2_misuse.py`](../demo-files/python/demo2_misuse.py).

**Context:** Two in-process tools, `convert` and `convert_value`, do real work: one converts physical units and the other converts currency. Only their descriptions differ between the two runs. A tool is a name, a description, an input schema and a handler, and the description is what Claude reads to decide when to call it.

**Steps:**

1. Open `demo2_misuse.py`. Show the `VARIANTS` table: the vague descriptions ("Convert a value.") and the clear ones, which say what the tool converts, which units it accepts and what it is not for.
2. Run the vague variant:

```
cd $FILES/python
python3 demo2_misuse.py vague
```

3. Watch the `TOOL` lines for each prompt. Point out any call that returns `[error]` (`Unsupported unit pair` or `Unsupported currency pair`), which means the agent picked the wrong tool and had to recover.
4. Run the clear variant:

```
python3 demo2_misuse.py clear
```

5. Compare the number of tool calls and the turn count between the two runs.
6. State the rule: a description says what the tool does, what input it takes, and when not to use it.

**Expected result:** With vague descriptions, the agent picks the wrong tool on at least one prompt in most runs, gets an error, and retries. With clear descriptions, each prompt uses the right tool on the first call, and the turn count drops.

> **Instructor note:** Model choice is not deterministic. Some runs pick the right tool even with vague descriptions, because the parameter values hint at the answer. Run the vague variant twice in rehearsal and keep the transcript of a run that misfires. If it will not misfire, say so and show that the agent got there by trial and error (the error lines). Tool search is on by default in the SDK and defers tool schemas, so a `ToolSearch` call may appear before the first conversion; the course harness ignores it. That name is confirmed in the MCP guide but its exact behavior for in-process tools needs rehearsal. **Fallback:** show a recorded vague run with one `[error]` line, then run the clear variant live, which costs little.

> **Why this matters:** Most "the agent is dumb" reports are tool descriptions that never said when to use the tool. Lab 1 starts from exactly this defect.

---

**Previous:** [Demo 1: Run the Minimal Agent](demo-1-run-the-minimal-agent.md) · **Next:** [Demo 3: Build a Standalone MCP Server](demo-3-build-a-standalone-mcp-server.md)


*Demo 2 of 8*
