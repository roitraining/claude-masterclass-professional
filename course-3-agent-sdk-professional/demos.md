# Claude Agent SDK Professional: Demos

**Course:** Claude Agent SDK Professional: Building and Evaluating Production Agents (Claude MasterClass Professional, Course 3)
**Contents:** 8 instructor-led demos. Each takes 15 minutes or less and has a learning objective. The numbers match the Today's Demos slide.

---

## About this guide

Run the demos in order. Each has the same layout: a learning objective, a time, a Files line when it uses files, a short context paragraph, steps, an Expected result, an Instructor note, and a Why this matters note.

This is a 300-level course. The demos assume Associate-level habits and do not re-teach subagent team design, hooks basics, or the Claude Code interface.

In this guide `$FILES` means the `demo-files` folder. Python is the primary language and every demo runs in Python. Demo 1 also has a TypeScript version. For Demos 2 to 6, the instructor shows Python and points to the matching TypeScript file structure in the labs.

- `$FILES/python`: agent core and demo scripts (`demo1_minimal.py` to `demo8_scorecard.py`).
- `$FILES/typescript`: the TypeScript starter (`src/demo1Minimal.ts`).
- `$FILES/retrieval`: the local retrieval MCP server and its documents (Demo 4, Demo 5).
- `$FILES/recorded`: recorded runs for the offline Demos 7 and 8.
- `$FILES/data`: fictional shop data and a sample note.

Every person, company, order and amount is fictional. Agent output varies from run to run, so check results against the Expected result and not against exact text.

> **Credentials.** Set `ANTHROPIC_API_KEY` as an environment variable in the shell where you run the demo (see `$FILES/README.md`). Never put it in a file or on a slide. API-key authentication only. claude.ai login is not used.

> **Cost.** Demos 1 to 6 make live model calls. Every script sets a turn limit and a spend limit. Demos 7 and 8 run offline from recorded data. Each live demo lists a recorded-transcript fallback in its Instructor note, so a network or key problem never stops the session.

---

## Setup: Install and check once

**Time:** about 5 minutes, before Demo 1.

1. Python:

```
cd $FILES/python
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python preflight.py
```

On Windows PowerShell use `py -m venv .venv` and `.venv\Scripts\Activate.ps1`.

2. TypeScript, for the Demo 1 comparison:

```
cd $FILES/typescript
npm install @anthropic-ai/claude-agent-sdk zod @modelcontextprotocol/server
npm install --save-dev tsx
npx tsx src/preflight.ts
```

**Expected result:** every line of `preflight.py` reads `[ok]`. The check never prints the key.

> **Instructor note:** The Python package is `claude-agent-sdk` and the TypeScript package is `@anthropic-ai/claude-agent-sdk`. Both bundle a native Claude Code binary on most platforms. An install that skips optional dependencies, or a platform with no wheel, needs a native Claude Code install; rehearse on the class image. Python needs 3.10 or later and Node.js 18 or later. The MCP server library (`mcp[cli]` for Python, `@modelcontextprotocol/server` for TypeScript) is **UNVERIFIED** against the class image: its module layout has changed between releases. The server scripts import with a fallback, and the exact `run()` call may need a one-line change. Pin versions after rehearsal.

---

## Demo 1: Run the Minimal Agent

**Learning objective:** Run the smallest useful agent loop in Python and TypeScript, and read the messages it streams. Time: about 10 minutes. (Module 2)

**Files:** `$FILES/python/demo1_minimal.py`, `$FILES/typescript/src/demo1Minimal.ts`, `$FILES/data/sample_notes.md`.

**Context:** `query()` returns a stream of messages. The agent reads a file with the built-in `Read` tool, which is the only tool it has. The final `ResultMessage` carries a subtype, a turn count and a cost estimate.

**Steps:**

1. Open `demo1_minimal.py`. Point at four things in the options: `tools=["Read"]` (the only tool that exists), `allowed_tools=["Read"]` (auto-approved), `setting_sources=[]` (ignore settings files on this machine), and the turn and spend limits.
2. Run it:

```
cd $FILES/python
python demo1_minimal.py
```

3. Read the printed stream aloud: the `system` init message, the assistant `tool_use` for `Read`, the tool result, the assistant text, and the `result` line with `subtype`, `turns` and `cost_usd`.
4. Open `demo1Minimal.ts` beside it. Show the same options in camelCase and the same stream, then run it:

```
cd $FILES/typescript
npx tsx src/demo1Minimal.ts
```

5. Ask the room: which line would you change to give the agent a second tool? Answer: `tools` and `allowed_tools`.

**Expected result:** The agent calls `Read` on `sample_notes.md`, lists the three action items, and ends with `subtype=success`. Both languages show the same shape of stream.

> **Instructor note:** `tools`, `allowed_tools`, `setting_sources`, `max_turns`, `max_budget_usd` and `cwd` are confirmed in the Python reference, and the matching camelCase names in the TypeScript examples. In TypeScript, a message's content sits under `message.message.content`; in Python it is `message.content`. Say so once. Turn count and cost are estimates, and the spend cap can overshoot, so do not quote them as exact. **Fallback:** read the expected stream from the Expected result and run only `python preflight.py` live.

> **Why this matters:** Every later demo is this loop with something added. A student who can read the stream can debug every agent in the course.

---

## Demo 2: A Tool the Agent Misuses

**Learning objective:** Show a vague tool description making an agent pick the wrong tool, and a specific description fixing it. Time: about 12 minutes. (Module 3)

**Files:** `$FILES/python/demo2_misuse.py`.

**Context:** Two in-process tools, `convert` and `convert_value`, do real work: one converts physical units and the other converts currency. Only their descriptions differ between the two runs. A tool is a name, a description, an input schema and a handler, and the description is what Claude reads to decide when to call it.

**Steps:**

1. Open `demo2_misuse.py`. Show the `VARIANTS` table: the vague descriptions ("Convert a value.") and the clear ones, which say what the tool converts, which units it accepts and what it is not for.
2. Run the vague variant:

```
cd $FILES/python
python demo2_misuse.py vague
```

3. Watch the `TOOL` lines for each prompt. Point out any call that returns `[error]` (`Unsupported unit pair` or `Unsupported currency pair`), which means the agent picked the wrong tool and had to recover.
4. Run the clear variant:

```
python demo2_misuse.py clear
```

5. Compare the number of tool calls and the turn count between the two runs.
6. State the rule: a description says what the tool does, what input it takes, and when not to use it.

**Expected result:** With vague descriptions, the agent picks the wrong tool on at least one prompt in most runs, gets an error, and retries. With clear descriptions, each prompt uses the right tool on the first call, and the turn count drops.

> **Instructor note:** Model choice is not deterministic. Some runs pick the right tool even with vague descriptions, because the parameter values hint at the answer. Run the vague variant twice in rehearsal and keep the transcript of a run that misfires. If it will not misfire, say so and show that the agent got there by trial and error (the error lines). Tool search is on by default in the SDK and defers tool schemas, so a `ToolSearch` call may appear before the first conversion; the course harness ignores it. That name is confirmed in the MCP guide but its exact behavior for in-process tools needs rehearsal. **Fallback:** show a recorded vague run with one `[error]` line, then run the clear variant live, which costs little.

> **Why this matters:** Most "the agent is dumb" reports are tool descriptions that never said when to use the tool. Lab 1 starts from exactly this defect.

---

## Demo 3: Build a Standalone MCP Server

**Learning objective:** Build a small standalone MCP server over stdio, connect an agent to it, and say when a server is worth the overhead compared with an in-process tool. Time: about 15 minutes. (Module 5)

**Files:** `$FILES/python/demo3_rates_server.py`, `$FILES/python/demo3_agent.py`.

**Context:** An in-process tool runs inside your Python or TypeScript program. A standalone server is a separate process the agent starts and talks to over stdin and stdout. Choose a server when another team or language owns the tool, when several agents share it, when it needs its own dependencies or permissions, or when the tool must return structured content (Python in-process tools forward only `content` and `is_error`).

**Steps:**

1. Open `demo3_rates_server.py`. Walk through three parts: the server object, two decorated tools with specific docstrings, and `mcp.run(transport="stdio")`. Say that stdout carries the protocol, so the server logs to stderr.
2. Open `demo3_agent.py`. Show the `mcp_servers` entry: a `command` (the current Python) and `args` (the server file). Show `allowed_tools=["mcp__rates__*"]` and explain the naming form `mcp__{server}__{tool}`.
3. Run it:

```
cd $FILES/python
python demo3_agent.py
```

4. Read the `MCP servers at init` line. Point at the status for `rates`.
5. Read the `TOOL mcp__rates__quote_shipping` line and compare the answer with the expected 13.80 dollars.
6. Break it on purpose: change `quote_shipping` to print to stdout, run again, and show the connection failing. Revert.
7. Ask the room: which of your current tools would you move out of process, and why?

**Expected result:** The init message lists the `rates` server as connected, the agent calls `mcp__rates__quote_shipping` with `weight_kg` 3.5 and `zone` B, and the answer is 13.80 dollars.

> **Instructor note:** The tool naming, the `mcpServers` shape with `command` and `args`, the init message `status` values (`connected`, `failed`, `needs-auth`, `pending`) and the `allowedTools` wildcard are confirmed in the official MCP guide. The 30-second default connection wait (`MCP_TIMEOUT`) is also documented, which matters if a server is slow to start. **UNVERIFIED:** the standalone server library. The scripts use the official `mcp` Python package and try two import paths. Whether a tool docstring becomes the tool description, and the exact `run()` call, need rehearsal on the installed version. Whether a library tool can return structured content is also unconfirmed for the installed version; say only that Python in-process tools cannot, which is documented. Step 6 is optional: skip it if the room is slow. **Fallback:** show the server file and a recorded init line, and run only the server by itself to show it waits silently on stdin.

> **Why this matters:** A server turns a tool into a contract that any agent can use. It also moves the tool's permissions out of the agent, which Lab 2 puts to the test.

---

## Demo 4: Retrieval Through an MCP Server

**Learning objective:** Connect an agent to a retrieval source through an MCP server, so retrieval sits behind a tool call, and state that this is an integration pattern and not a first-party Anthropic feature. Time: about 15 minutes. (Module 7)

**Files:** `$FILES/retrieval/server.py`, `$FILES/retrieval/docs/`, `$FILES/retrieval/README.md`, `$FILES/python/demo4_retrieval_agent.py`.

**Context:** The retrieval server is a local stand-in. It does TF-IDF keyword search over nine fictional Markdown documents and exposes two tools, `search_docs` and `read_doc`. A real vector store would sit behind the same two tools. The agent sees only a tool.

**Steps:**

1. Show the `docs/` folder. Point out `bw-returns-handbook-2024.md`, marked superseded, next to the current handbook.
2. Open `server.py`. Show the tool signatures and say that the body of `Index.search` is the only thing a vector store replaces.
3. Run the agent:

```
cd $FILES/python
python demo4_retrieval_agent.py
```

4. For the first prompt, read the `TOOL` lines: `search_docs`, then `read_doc`, then the answer with a cited `doc_id`.
5. For the second prompt (the return window), show that search returns both the current and the superseded handbook, and that the agent should cite the current one (30 days, not 14).
6. Run a question the knowledge base cannot answer and show the agent saying so:

```
python demo4_retrieval_agent.py "What is the warranty on a canoe?"
```

7. State plainly: retrieval here is an MCP integration the course supplies. It is a supported pattern, not a first-party Anthropic feature.

**Expected result:** The agent searches, reads the best document, and answers with a `doc_id`. For the return window it answers 30 days. For the canoe it says the knowledge base has nothing relevant.

> **Instructor note:** The MCP wiring is confirmed in the MCP guide. The retrieval design (an agent reaching a vector store or search through an MCP server) is in the verified facts. The ranking is a crude keyword score: the superseded handbook can rank first for some queries, which is a useful teaching moment about retrieval quality and not a defect to hide. Module 7 is instructor-provisioned, so you may swap in a real store behind the same tool signatures. The server library caveats from Demo 3 apply (**UNVERIFIED** import path and `run()` call). **Fallback:** show the `search_docs` JSON output by running the retrieval index directly (`python` with `from server import INDEX`, then `INDEX.search("return window", 3)`), then read the expected tool sequence from the Expected result.

> **Why this matters:** Teams often ask for "RAG" as a product. It is a tool call. Seeing that removes the mystery and shows where retrieval quality, and prompt injection from documents, can enter.

---

## Demo 5: Delegate to a Subagent

**Learning objective:** Define a subagent in code, watch the parent delegate to it, and see that only the subagent's final message returns. Time: about 12 minutes. (Module 11)

**Files:** `$FILES/python/demo5_subagent.py`, `$FILES/retrieval/docs/`.

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

## Demo 6: Cap Turns, Depth, and Spend

**Learning objective:** Stop a runaway agent with a turn cap, a spend cap, and subagent depth and concurrency limits, and read the result when a cap is hit. Time: about 15 minutes. (Module 11)

**Files:** `$FILES/python/demo6_caps.py`.

**Context:** The demo tool `poll_job` never returns DONE, so the agent would poll forever. Four limits stop it: `max_turns`, `max_budget_usd`, and two environment variables, `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` (default 3) and `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` (default 20). Hitting a cap ends the run with an error subtype, and a single-shot `query()` raises after yielding it.

**Steps:**

1. Run with a turn cap:

```
cd $FILES/python
python demo6_caps.py turns
```

2. Read the `RESULT` line. Show `subtype=error_max_turns` and the `poll_job calls` count. Point out the exception message printed under `ERROR`, and that the script still captured the result before the exception.
3. Run with a spend cap:

```
python demo6_caps.py budget
```

4. Show `subtype=error_max_budget_usd` and a cost at or slightly above the cap. State that the cap is a client-side estimate and can overshoot, so leave headroom.
5. Run the concurrency case:

```
python demo6_caps.py concurrency
```

6. Look for a tool result carrying `Concurrent subagent limit reached` in the printed limit lines. Show where depth and concurrency are set (the `env` option) and that Python merges `env` into the inherited environment while TypeScript replaces it, so TypeScript code must spread `process.env`.
7. Read the result as a user would: the run did not finish the work. Ask what your application tells the user, and who is alerted.

**Expected result:** The turn-cap run ends with `error_max_turns` after a few polls. The spend-cap run ends with `error_max_budget_usd`. The concurrency run may show a refused spawn.

> **Instructor note:** The caps, the environment variable names and defaults, the `error_max_budget_usd` subtype, the overshoot warning, the `Concurrent subagent limit reached` and `Budget limit reached` messages, and the Python and TypeScript `env` difference are confirmed in the subagents guide. `error_max_turns` appears in the Python reference. The limits section of the guide describes SDK releases bundling Claude Code v2.1.219 or later, so check the installed version. The concurrency run depends on the model choosing to spawn four subagents; it may not, and a refused spawn is not guaranteed. Rehearse it. The caps shown (4 turns, 0.03 dollars, 2 concurrent) are demo values, not recommendations. **Fallback:** run `turns` only (it costs very little) and read the other two results from the Expected result.

> **Why this matters:** Agents spend money while they decide what to do next. A cap is the only control that works when the model's own judgment is the thing that failed.

---

## Demo 7: Grade a Run With Code and a Judge

**Learning objective:** Grade recorded agent runs with code graders over the final answer and the tool calls, then add a judge for an open-ended answer. Time: about 12 minutes. (Module 13)

**Files:** `$FILES/python/demo7_grade.py`, `$FILES/recorded/demo7_runs.json`, `$FILES/tasks/judge_rubric.json`.

**Context:** Four recorded runs show four different outcomes. The script grades them offline with two small code graders. For the open-ended reply it uses a recorded judge verdict, or a live judge if you pass `--live-judge`.

**Steps:**

1. Show `demo7_runs.json`: the golden task id, the tools called, and the final answer for each run.
2. Run the offline grading:

```
cd $FILES/python
python demo7_grade.py
```

3. Walk through the four lines. Run 1 passes both graders. Run 2 answers correctly without calling `order_lookup` (the tool grader fails: the answer is right and the process is wrong). Run 3 gives a wrong warranty (the answer grader fails). Run 4 passes both code graders and fails the judge on tone.
4. Open `tasks/judge_rubric.json`. Show the criteria and the four calibration replies. Say why you calibrate a judge first.
5. Optional, one model call: run the live judge and compare its score with the recorded one:

```
python demo7_grade.py --live-judge
```

6. State the rule: grade the final answer and the tool calls with code first, because code is fast and repeatable. Use a judge only for what code cannot see, and test the judge.

**Expected result:** Run 1 passes everything. Run 2 fails the tool grader only. Run 3 fails the answer grader only. Run 4 passes both code graders and fails the judge.

> **Instructor note:** The grading approaches (code-based is fastest and most reliable and lacks nuance, LLM-based is fast and flexible and its reliability should be tested first) come from Anthropic's test-and-evaluate guidance in the verified facts. Reading `tool_use` blocks from the message stream is confirmed in the MCP and subagents guides. The recorded runs and the judge verdict are hand-written and fictional. A live judge score will vary from the recorded one; that variation is the lesson. **Fallback:** the default run is already offline and needs no key.

> **Why this matters:** A final-answer check alone passes run 2, which guessed the return policy without looking at the order. The tool-call grader is how you catch that.

---

## Demo 8: What a Passing Score Misses

**Learning objective:** Show a suite that scores 100 percent on answers while hiding a tool misuse, a cost spike and a rare injection, and place evaluation as one input to a larger production picture. Time: about 12 minutes. (Module 15)

**Files:** `$FILES/python/demo8_scorecard.py`, `$FILES/recorded/demo8_runs.json`.

**Context:** The recorded data is one run of each of 12 golden tasks, plus 20 repeats of a notes task that no golden task covers. All numbers are fictional.

**Steps:**

1. Run the scorecard:

```
cd $FILES/python
python demo8_scorecard.py
```

2. Stop after section 1. Ask the room whether they would ship. The answer-only score is 12 of 12.
3. Section 2 adds a tool-call grader. Show G12: a correct reply that also called `issue_refund`. Show G11: a correct "not found" answer reached with 12 lookups.
4. Section 3 adds cost. Show G11 costing about nine times the median. A correct answer can still be a cost spike.
5. Section 4 shows the injection. One run in 20 followed it, and no suite task reads those notes, so the suite could not see it. Link it to Lab 2.
6. Close on the production picture: limits and budgets that stop a bad run, human review where an action cannot be undone, alerts on cost and tool calls, repeats on risky tasks, and the golden-task file as a living document.

**Expected result:** The answer grader passes 12 of 12. Adding the tool grader drops it to 10 of 12. The cost rule flags G11. The injection appears only in the repeats.

> **Instructor note:** All data is hand-written for the demo and fictional. Do not present it as measured behavior of any model. The principle matches the verified facts: the Console Evaluate tool and a final-answer check evaluate what they are asked, and an agent's tool use and cost need their own graders. Whether a real agent follows the planted injection varies by model and prompt. Students will measure it in Lab 2. **Fallback:** none needed, the demo is offline.

> **Why this matters:** A green dashboard is a statement about the tests, not about the agent. Production risk lives in what the tests never ask.
