# Demo 1: Run the Minimal Agent

**Course:** Claude Agent SDK Professional: Building and Evaluating Production Agents (Claude MasterClass Professional, Course 3)
**Demo:** 1 of 8
**Time:** about 10 minutes

> Part of **[Claude Agent SDK Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Run the smallest useful agent loop in Python and TypeScript, and read the messages it streams. Time: about 10 minutes. (Module 2)

**Files:** [`$FILES/python/demo1_minimal.py`](../demo-files/python/demo1_minimal.py), [`$FILES/typescript/src/demo1Minimal.ts`](../demo-files/typescript/src/demo1Minimal.ts), [`$FILES/data/sample_notes.md`](../demo-files/data/sample_notes.md).

**Context:** `query()` returns a stream of messages. The agent reads a file with the built-in `Read` tool, which is the only tool it has. The final `ResultMessage` carries a subtype, a turn count and a cost estimate.

**Steps:**

1. Open `demo1_minimal.py`. Point at four things in the options: `tools=["Read"]` (the only tool that exists), `allowed_tools=["Read"]` (auto-approved), `setting_sources=[]` (ignore settings files on this machine), and the turn and spend limits.
2. Run it:

```
cd $FILES/python
python3 demo1_minimal.py
```

3. Read the printed stream aloud: the `system` init message, the assistant `tool_use` for `Read`, the tool result, the assistant text, and the `result` line with `subtype`, `turns` and `cost_usd`.
4. Open `demo1Minimal.ts` beside it. Show the same options in camelCase and the same stream, then run it:

```
cd $FILES/typescript
npx tsx src/demo1Minimal.ts
```

5. Ask the room: which line would you change to give the agent a second tool? Answer: `tools` and `allowed_tools`.

**Expected result:** The agent calls `Read` on `sample_notes.md`, lists the three action items, and ends with `subtype=success`. Both languages show the same shape of stream.

> **Instructor note:** `tools`, `allowed_tools`, `setting_sources`, `max_turns`, `max_budget_usd` and `cwd` are confirmed in the Python reference, and the matching camelCase names in the TypeScript examples. In TypeScript, a message's content sits under `message.message.content`; in Python it is `message.content`. Say so once. Turn count and cost are estimates, and the spend cap can overshoot, so do not quote them as exact. **Fallback:** read the expected stream from the Expected result and run only `python3 preflight.py` live.

> **Why this matters:** Every later demo is this loop with something added. A student who can read the stream can debug every agent in the course.

---

**Next:** [Demo 2: A Tool the Agent Misuses](demo-2-a-tool-the-agent-misuses.md)


*Demo 1 of 8*
