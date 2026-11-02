# Demo 6: Cap Turns, Depth, and Spend

**Course:** Claude Agent SDK Professional: Building and Evaluating Production Agents (Claude MasterClass Professional, Course 3)
**Demo:** 6 of 8
**Time:** about 15 minutes

> Part of **[Claude Agent SDK Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Stop a runaway agent with a turn cap, a spend cap, and subagent depth and concurrency limits, and read the result when a cap is hit. Time: about 15 minutes. (Module 11)

**Files:** [`$FILES/python/demo6_caps.py`](../demo-files/python/demo6_caps.py).

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

**Previous:** [Demo 5: Delegate to a Subagent](demo-5-delegate-to-a-subagent.md) · **Next:** [Demo 7: Grade a Run With Code and a Judge](demo-7-grade-a-run-with-code-and-a-judge.md)


*Demo 6 of 8*
