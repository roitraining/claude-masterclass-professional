# Demo 5: Delegate to a Subagent

**Course:** Claude Agent SDK Professional: Building and Evaluating Production Agents (Claude MasterClass Professional, Course 3)
**Demo:** 5 of 8
**Time:** about 12 minutes

> Part of **[Claude Agent SDK Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Define a subagent in code, watch the parent delegate to it, and see that only the subagent's final message returns. Time: about 12 minutes. (Module 11)

**Files:** [`$FILES/python/demo5_subagent.py`](../demo-files/python/demo5_subagent.py), [`$FILES/retrieval/docs/`](../demo-files/retrieval/docs).

**Context:** A subagent is an `AgentDefinition` passed in the `agents` option. Claude invokes it through the `Agent` tool, which must be allowed. The subagent starts with a fresh context window and receives only the prompt string the parent writes. Its intermediate tool calls stay inside it.

**Steps:**

1. Open `demo5_subagent.py`. Show the `AgentDefinition`: a `description` that says when to use it, a `prompt`, and `tools` limited to `Read`, `Grep` and `Glob`. Show `"Agent"` in `allowed_tools`.
2. Run it:

```
cd $FILES/python
python demo5_subagent.py
```

3. Read the output: the `Agent` tool call with its `subagent_type`, the prompt the subagent received, any `(inside subagent)` tool calls, and the parent's final answer.
4. Ask: what did the subagent know when it started? Answer: only the prompt string. Ask: what did the parent see from the subagent's `Read` calls? Answer: nothing, only the final message.
5. Edit the description to "Helper." and run again. Show that the parent may answer on its own instead of delegating.

**Expected result:** The parent calls `Agent` with `subagent_type` `policy-reader`. The summary reports a change from 14 days to 30 days and from store credit to the original payment method.

> **Instructor note:** `AgentDefinition` fields, the `Agent` tool name (it appears as `Task` in the init tool list and in older versions, so match both), the fresh context window, the final-message-only return, and the `parent_tool_use_id` marker are confirmed in the subagents guide. The Python field names that are multi-word keep camelCase (`disallowedTools`, `maxTurns`); a snake_case keyword raises `TypeError`. Subagents run in the background by default. The parent usually waits for the result, but the exact timing in the stream is not confirmed here, so say "the parent continues" only after you have watched a rehearsal run. The subagent scan for instruction-shaped text is documented for Claude Code v2.1.210 and later; mention it only if your installed version is at least that. **Fallback:** show the expected `Agent` call from the Expected result and run the step 5 edit only if you have time.

> **Why this matters:** Delegation protects the parent's context window and narrows tool access. Lab 3 depends on writing a prompt string that carries everything the subagent needs.

---

**Previous:** [Demo 4: Retrieval Through an MCP Server](demo-4-retrieval-through-an-mcp-server.md) · **Next:** [Demo 6: Cap Turns, Depth, and Spend](demo-6-cap-turns-depth-and-spend.md)


*Demo 5 of 8*
