# Lab 3: Multi-Step Agent With a Subagent

**Course:** Claude Agent SDK Professional
**Duration:** 90 minutes
**Format:** Instructor-led, in-class hands-on lab (300 level)

> Part of **[Claude Agent SDK Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

## Prerequisites

- [ ] Labs 1 and 2 completed
- [ ] `ANTHROPIC_API_KEY` set in the shell you will run from
- [ ] Python files: `lab3_agent.py`, `lab3_check.py`, `loop_fixture.py`, `tools_inprocess.py`, `agent_core.py`
- [ ] TypeScript files: `src/lab3Agent.ts`, `src/lab3Check.ts`, `src/loopFixture.ts`
- [ ] Shared file: `tasks/lab3_tasks.json`

> **Token cost.** The loop task is a deliberate runaway. Set a spend cap **before** you run it loose, and remember the cap is a client-side estimate that can overshoot. Leave headroom.

---

## Overview

Two tasks:

- **The digest task** asks for a returns digest across five delivered orders. It needs several lookups, arithmetic against a return window, and a final summary.
- **The loop task** is the runaway. A `check_manifest` tool never returns `RECONCILED`, and the system prompt tells the agent never to stop and to spawn another subagent if one gives up.

**The starter ships limits that are deliberately wrong.** A subagent starts with a fresh context window and receives only the prompt string the parent writes, and only its final message comes back.

---

## Part 1: Baseline Both Tasks

### Step 1: Run the Digest and the Loop on the Starter

```
python3 lab3_agent.py digest
python3 lab3_agent.py loop
```

**Expected result:** the digest fails early and the loop runs away. Both are planted.

> **Hint:** the starter limits are in `lab3_agent.py`. Notice what each limit does to each task before you change anything.

### Step 2: Record the Result Subtype, Turns and Cost

**Acceptance criteria:** the result subtype, turn count and cost of each run are recorded in `NOTES.md`.

---

## Part 2: Build the Plan-Delegate-Incorporate Loop

### Step 3: Define the Subagent So the Parent Will Use It

**Acceptance criteria:** the subagent has a specific description, tools limited to what it needs, and a prompt that says what it returns.

> **Hint:** a description such as "Helper." gives the parent no reason to delegate. Name the subagent in the parent prompt if the description alone is not enough.

> **Common Pitfall:** `AgentDefinition` fields keep camelCase spelling in Python — `maxTurns`, not `max_turns`.

### Step 4: Write the Parent Prompt and Check the Result

The parent plans, fetches the five orders with its tools, delegates the eligibility and refund arithmetic to the subagent, checks the result, and presents the digest.

**Acceptance criteria:** the `Agent` tool is called at least once, and the final digest states **3 returnable orders and a total refund of 403**.

> **Hint:** pass the subagent the order records and the return window in the prompt of the Agent tool. It cannot see the conversation of the parent.

> **Hint:** match both `Agent` and `Task` when you read `tool_use` names.

---

## Part 3: Stop the Runaway Loop

### Step 5: Cap the Loop Without Editing the Fixture

**Acceptance criteria:** `python3 lab3_agent.py loop` ends with `error_max_turns` or `error_max_budget_usd`, or ends with a success result whose answer honestly says the manifest did not reconcile. The `check_manifest` count stays at or under 15 and the spend stays within the spend cap plus 50 percent headroom. `lab3_check.py` also checks that you set the limits, not only that the run came out well: a model that happens to stop on its own does not count as containment.

> **Hint:** set `max_turns` and `max_budget_usd`. Limit subagent depth with `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` and concurrency with `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`, both through the `env` option. Then set `LOOP_SUBAGENT_MAX_TURNS` (TODO 5).
>
> Work out what each limit can and cannot reach before you pick values. `max_turns` bounds the **parent's** turns, not the tool calls a subagent makes inside one of them. Depth and concurrency bound how subagents **spawn**, not how long each one runs. So one subagent can still call `check_manifest` indefinitely until you give the subagent its own turn limit.

> **Common Pitfall:** do not edit the fixture to remove the loop. The point is containing it from outside.

> **Common Pitfall:** a success result claiming the shipment reconciled is a failure. The tool never says that.

---

## Part 4: Keep the Real Task Working

### Step 6: Tune the Limits Against Your Measurements

**Acceptance criteria:** with your limits in place, the digest still ends with `success`. Limits tight enough to stop the loop but loose enough for the digest are the point of this part.

> **Hint:** measure the turns and cost of the digest first, then set the cap with margin. The spend cap is a client-side estimate and can overshoot.

---

## Part 5: Read a Capped Result as a User

### Step 7: Say What the User Sees and Who Is Alerted

**Acceptance criteria:** in `NOTES.md`, say what your application should show the user, and who should be alerted, when the loop run ends on a cap.

---

## Part 6: Score It

### Step 8: Run the Checker

```
python3 lab3_check.py
```

**Acceptance criteria:** all seven checks pass.

---

## Part 7: Checkpoint

### Step 9: Verify Your Progress

- [ ] Starter baselines recorded: result subtype, turns and cost for both tasks
- [ ] The subagent has a specific description, not "Helper."
- [ ] The subagent receives the order records and the return window in its prompt
- [ ] The subagent tool list is limited to what it needs
- [ ] An `Agent` (or `Task`) tool_use appears in the digest run
- [ ] The parent prompt expresses plan, delegate, incorporate
- [ ] The parent checks the arithmetic of the subagent rather than trusting it
- [ ] The digest ends with `success`, reporting 3 returnable orders and a total refund of 403
- [ ] The loop run is stopped by a cap, or reports honestly that it did not reconcile
- [ ] `check_manifest` calls stay at or under 15
- [ ] Spend stays within the cap plus 50 percent headroom
- [ ] Depth and concurrency limits are set through `env`, with a reason recorded for each value
- [ ] The fixture was not edited to remove the loop
- [ ] `NOTES.md` says what the user sees and who is alerted on a capped run
- [ ] `python3 lab3_check.py` shows all seven checks passing

---

## Troubleshooting Reference

| Issue | Symptom | Solution |
|---|---|---|
| Subagent field rejected | `TypeError` on `AgentDefinition(max_turns=...)` | Python subagent fields are camelCase. Use `maxTurns` and `disallowedTools` |
| Parent never delegates | No `Agent` tool call | The description is vague, or `Agent` is not in `allowed_tools`, or the built-in `Agent` tool was removed by a restrictive `tools` list. The starter leaves built-ins at default and disallows the file, shell and web tools by name |
| Subagent returns nonsense | Answer unrelated to the data | It only saw the prompt string. Put the data in it |
| TypeScript auth breaks after adding env vars | Authentication error, or a binary cannot be found | The TypeScript SDK replaces the subprocess environment with `env`. Spread `process.env` into it. Python merges |
| Digest dies immediately | `error_max_turns` on the starter | That is the planted `MAX_TURNS = 3` |
| Loop still runs away with every limit set | `check_manifest` count in the dozens or hundreds | `LOOP_SUBAGENT_MAX_TURNS` is still `None`. The parent's `max_turns` cannot bound a subagent's own turns |
| Loop stops cleanly but checks still fail | `config:` lines marked FAIL | The run came out well without you setting the limits. Set TODO 4 and TODO 5 and lower `BUDGET_USD` |
| Cost exceeds the cap | Reported cost above your `max_budget_usd` | The cap is a client-side estimate. Leave headroom |

---

## Scoring Rubric (100 points)

| Criterion | Points |
|---|---|
| Digest completes with `success`, 3 returnable orders, total 403 | 20 |
| Subagent: a specific description, a prompt that says what the subagent returns, tools limited to what it needs, `Agent` tool_use present | 20 |
| Parent prompt expresses plan, delegate, incorporate, and the parent checks the arithmetic of the subagent | 10 |
| Loop stopped by a cap or honest report, within the call bound and the spend bound, with a turn limit set on the loop subagent | 20 |
| Depth and concurrency limits set through `env`, with a reason for each value | 10 |
| Limits tuned against measurements (the digest still succeeds) | 10 |
| Capped-result note: what the user sees and who is alerted | 10 |

---

## What You Built

In 90 minutes, you:

- Built a plan-delegate-incorporate loop where the parent checks the work of the subagent instead of trusting it
- Learned the hard way that a subagent sees only the prompt string you write, and nothing of the conversation above it
- Contained a deliberate runaway with turn, spend, depth and concurrency limits, without touching the fixture that caused it
- Tuned those limits against measurements so they stop the loop and still let the real task finish
- Decided what a capped run should show a user, and who gets alerted

---

## What's Next

Lab 4, Build an Evaluation Harness, replaces your own judgment of these runs with a repeatable scored harness.

---

## Facilitator Notes

*Where the traps are planted.* (1) `lab3_agent.py` and `lab3Agent.ts` ship `MAX_TURNS = 3` (too low for the digest, which needs several lookups) and `BUDGET_USD = 5.00` (far too high to protect anything), and `LOOP_SUBAGENT_MAX_TURNS = None`, which leaves the loop subagent unbounded. **The spend cap cannot contain this fixture at any value:** the loop costs about $0.0025 a call, so roughly 200 calls to reach $0.50 against a bound of 15. Turn limits are the only lever that works, and the subagent's own limit is the only one that reaches inside a subagent. Students who set everything except TODO 5 will see the runaway continue on a model that does not self-terminate. (2) `RETURNS_ANALYST` has the description "Helper." (3) `loop_fixture.py` and `loopFixture.ts`: `check_manifest` never reconciles, and `LOOP_SYSTEM_PROMPT` says never to stop and to spawn another subagent if one gives up. (4) Python `AgentDefinition` camelCase fields. (5) TypeScript: any `env` you pass replaces the whole environment, so adding the depth variable without `...process.env` breaks authentication.

*Answer key for the digest* (as of 2026-10-19, window 30 days):

| Order | Days since delivery | Returnable | Refund |
|---|---|---|---|
| BW-1001 | 47 | No | 0 |
| BW-1005 | 21 | Yes | 129.00 |
| BW-1006 | 9 | Yes | 50.00 |
| BW-1009 | 4 | Yes | 224.00 |
| BW-1010 | 50 | No | 0 |

Returnable count 3, total refund 403.00. For the loop, any of `error_max_turns`, `error_max_budget_usd`, or an honest success is a pass. A success that claims the shipment reconciled is a fail: the tool never says so.

*What good looks like.* Limits such as 10 to 15 parent turns, a spend cap a few times the measured digest cost, depth 1 and concurrency 2 or lower, with the reasons given. Ask the student: what happens to the real task if the order list of a customer is ten times longer?

*Rehearse before the day, and flag as unconfirmed.* The `AgentDefinition` fields and their Python casing, the depth and concurrency variables and their defaults, the spend cap behavior and the `error_max_budget_usd` subtype, and the `env` difference between SDKs are confirmed in the subagents guide. **Needs rehearsal:** (1) whether an in-process SDK tool name such as `mcp__shop__order_lookup` is honored in the `tools` list of a subagent (the starter does not restrict the tools of the subagent, so a subagent that cannot reach the tools will answer from the prompt only; the solution passes data in the prompt for that reason); (2) the exact subtype and result text when `max_turns` is reached, since the Python reference lists `error_max_turns` only in a comment; (3) **ANSWERED 2026-11-05 - the model decides this lab's outcome.** With the planted limits, Sonnet and Haiku broke the 15-call bound in 6 of 6 runs (57 to 186 `check_manifest` calls). Opus stopped on its own, so `lab3_check.py` reported 7/7 even though the bound was never defended. Run the loop fixture on **the model your class keys actually use** before the day, and treat a pass on Opus as unproven. Two linked gaps found in the same run: `SendMessage` was not in `BUILTIN_TOOLS`, so a contained agent could resume its own stopped subagents (now fixed); and subagent `maxTurns` is unset, which is the student's job but is not named in Step 5's hint; (4) the in-process `CALLS` counter includes calls made inside subagents only if they run in the same process, which is expected and unconfirmed; (5) subagents run in the background by default, so timing in the stream needs a rehearsal run; (6) behavior at the depth limit is described in the docs as leaving the bottom subagent unable to spawn, which students should not be told is an error.

---

*Lab 3 Complete*
