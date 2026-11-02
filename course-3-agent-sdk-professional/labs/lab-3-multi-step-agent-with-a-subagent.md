# Lab 3: Multi-Step Agent With a Subagent

> Part of **[Claude Agent SDK Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

**Learning objective:** Extend the agent into a plan-delegate-incorporate loop with a subagent defined in code, and stop a planted runaway loop with a turn cap, subagent depth and concurrency limits, and a spend cap. Time: 90 minutes.

**Files:** Python: `lab3_agent.py`, `lab3_check.py`, `loop_fixture.py`, `tools_inprocess.py`, `agent_core.py`. TypeScript: `src/lab3Agent.ts`, `src/lab3Check.ts`, `src/loopFixture.ts`. Shared: `tasks/lab3_tasks.json`.

**Context:** Two tasks. The digest task asks for a returns digest across five delivered orders: it needs several lookups, arithmetic against a return window, and a final summary. The loop task is the runaway: a `check_manifest` tool never returns `RECONCILED`, and the system prompt tells the agent never to stop and to spawn another subagent if one gives up. The starter ships limits that are deliberately wrong. A subagent starts with a fresh context window and receives only the prompt string the parent writes, and only its final message comes back.

**Steps:**

1. **Goal: run both tasks on the starter and read the results.**
   - Acceptance: you record the result subtype, turn count and cost of each run in `NOTES.md`.
   - Commands: `python lab3_agent.py digest` and `python lab3_agent.py loop`.
   - Hint: the starter limits are in `lab3_agent.py`. Notice what each limit does to each task before you change anything.
2. **Goal: build the plan-delegate-incorporate loop for the digest.**
   - Acceptance: the parent plans, fetches the five orders with its tools, delegates the eligibility and refund arithmetic to a subagent, checks the result, and presents the digest. The `Agent` tool is called at least once, and the final digest states 3 returnable orders and a total refund of 403.
   - Hints: a description such as "Helper." gives the parent no reason to delegate. Name the subagent in the parent prompt if the description alone is not enough. Pass the subagent the order records and the return window in the Agent tool's prompt, because it cannot see the parent's conversation. Limit its tools to what it needs. `AgentDefinition` fields keep camelCase spelling in Python (`maxTurns`, not `max_turns`). Match both `Agent` and `Task` when you read `tool_use` names.
3. **Goal: stop the runaway loop.**
   - Acceptance: `python lab3_agent.py loop` ends with `error_max_turns` or `error_max_budget_usd`, or ends with a success result whose answer honestly says the manifest did not reconcile. The `check_manifest` count stays at or under 15 and the spend stays within the spend cap plus 50 percent headroom.
   - Hints: set `max_turns` and `max_budget_usd`. Limit subagent depth with `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` and concurrency with `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`, both through the `env` option. Do not edit the fixture to remove the loop.
4. **Goal: keep the real task working inside the limits.**
   - Acceptance: with your limits in place, the digest still ends with `success`. Limits tight enough to stop the loop but loose enough for the digest are the point.
   - Hint: measure the digest's turns and cost first, then set the cap with margin. The spend cap is a client-side estimate and can overshoot, so leave headroom.
5. **Goal: read a capped result as a user would.**
   - Acceptance: in `NOTES.md`, say what your application should show the user and who should be alerted when the loop run ends on a cap.
6. **Goal: score it.** `python lab3_check.py` runs both tasks and prints seven checks.

**Checkpoint:** `python lab3_check.py` shows all seven checks passing. The digest delegates to the subagent and reports 403. The loop run is stopped by a limit or reports honestly that it did not finish.

**Common problems:**

- `TypeError` on `AgentDefinition(max_turns=...)`: Python subagent fields are camelCase. Use `maxTurns` and `disallowedTools`.
- The parent never calls `Agent`: the description is vague, or `Agent` is not in `allowed_tools`, or the built-in `Agent` tool was removed by a restrictive `tools` list. The starter leaves built-ins at default and disallows the file, shell and web tools by name.
- The subagent returns nonsense: it only saw the prompt string. Put the data in it.
- TypeScript only: after you add depth or concurrency variables, the run fails with an authentication error or cannot find a binary. The TypeScript SDK replaces the subprocess environment with `env`, so spread `process.env` into it. Python merges.
- The digest ends with `error_max_turns` on the starter: that is the planted `MAX_TURNS = 3`.
- The cost shows above the cap: the cap is an estimate. Leave headroom.

**Scoring rubric (100 points):**

| Criterion | Points |
|---|---|
| Digest completes with `success`, 3 returnable orders, total 403 | 20 |
| Subagent: a specific description, a prompt that says what the subagent returns, tools limited to what it needs, `Agent` tool_use present | 20 |
| Parent prompt expresses plan, delegate, incorporate, and the parent checks the subagent's arithmetic | 10 |
| Loop stopped by a cap or honest report, within the call bound and the spend bound | 20 |
| Depth and concurrency limits set through `env`, with a reason for each value | 10 |
| Limits tuned against measurements (the digest still succeeds) | 10 |
| Capped-result note: what the user sees and who is alerted | 10 |

**Facilitator note:**

*Where the traps are planted.* (1) `lab3_agent.py` and `lab3Agent.ts` ship `MAX_TURNS = 3` (too low for the digest, which needs several lookups) and `BUDGET_USD = 5.00` (far too high to protect anything). (2) `RETURNS_ANALYST` has the description "Helper." (3) `loop_fixture.py` and `loopFixture.ts`: `check_manifest` never reconciles, and `LOOP_SYSTEM_PROMPT` says never to stop and to spawn another subagent if one gives up. (4) Python `AgentDefinition` camelCase fields. (5) TypeScript: any `env` you pass replaces the whole environment, so adding the depth variable without `...process.env` breaks authentication.

*Answer key for the digest* (as of 2026-10-19, window 30 days):

| Order | Days since delivery | Returnable | Refund |
|---|---|---|---|
| BW-1001 | 47 | No | 0 |
| BW-1005 | 21 | Yes | 129.00 |
| BW-1006 | 9 | Yes | 50.00 |
| BW-1009 | 4 | Yes | 224.00 |
| BW-1010 | 50 | No | 0 |

Returnable count 3, total refund 403.00. For the loop, any of `error_max_turns`, `error_max_budget_usd`, or an honest success is a pass. A success that claims the shipment reconciled is a fail: the tool never says so.

*What good looks like.* Limits such as 10 to 15 parent turns, a spend cap a few times the measured digest cost, depth 1 and concurrency 2 or lower, with the reasons given. Ask the student: what happens to the real task if a customer's order list is ten times longer?

*Rehearse before the day, and flag as unconfirmed.* The `AgentDefinition` fields and their Python casing, the depth and concurrency variables and their defaults, the spend cap behavior and the `error_max_budget_usd` subtype, and the `env` difference between SDKs are confirmed in the subagents guide. **Needs rehearsal:** (1) whether an in-process SDK tool name such as `mcp__shop__order_lookup` is honored in a subagent's `tools` list (the starter does not restrict the subagent's tools, so a subagent that cannot reach the tools will answer from the prompt only; the solution passes data in the prompt for that reason); (2) the exact subtype and result text when `max_turns` is reached, since the Python reference lists `error_max_turns` only in a comment; (3) whether a model that tends to loop does so with your model choice, so run the loop fixture before the day and keep a transcript; (4) the in-process `CALLS` counter includes calls made inside subagents only if they run in the same process, which is expected and unconfirmed; (5) subagents run in the background by default, so timing in the stream needs a rehearsal run; (6) behavior at the depth limit is described in the docs as leaving the bottom subagent unable to spawn, which students should not be told is an error.
