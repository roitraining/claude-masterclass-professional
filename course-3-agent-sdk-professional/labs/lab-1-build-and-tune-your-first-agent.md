# Lab 1: Build and Tune Your First Agent

**Course:** Claude Agent SDK Professional
**Duration:** 90 minutes
**Format:** Instructor-led, in-class hands-on lab (300 level)

> Part of **[Claude Agent SDK Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

## Prerequisites

- [ ] `ANTHROPIC_API_KEY` set in the shell you will run from. The SDK does not read `.env` files
- [ ] Python 3.11 or later, or Node with `npx tsx` if you take the TypeScript track
- [ ] Pick a language track before you start and stay on it
- [ ] Python files: `agent_core.py`, `shop_data.py`, `tools_inprocess.py`, `lab1_agent.py`, `check_prompts.py`
- [ ] TypeScript files: `src/agentCore.ts`, `src/shopData.ts`, `src/tools.ts`, `src/lab1Agent.ts`, `src/checkPrompts.ts`
- [ ] Shared files: `data/shop.json`, `tasks/lab1_prompts.json`

> **Token cost.** Every checker run is eight prompts against a live model, and `--runs 2` doubles that. Diagnose from one saved run rather than re-running to look again.

---

## Overview

You inherit the support agent for Brightwater Outfitters, a fictional outdoor retailer. A fake backend module stands in for the order system.

Three tools work correctly: `order_lookup`, `customer_lookup` and `policy_lookup`. **The agent still uses them badly.** Your job is to find out why from evidence, and fix it in the tool definitions before touching the system prompt.

---

## Part 1: Baseline the Starter Agent

### Step 1: Run a Single Prompt

```
python lab1_agent.py "Where is order BW-1003?"
```

TypeScript: `npx tsx src/lab1Agent.ts "Where is order BW-1003?"`

**Expected result:** the agent answers, and you can see which tools it called.

### Step 2: Run All Eight Prompts Twice and Save the Baseline

```
python check_prompts.py lab1 --runs 2
```

TypeScript: `npx tsx src/checkPrompts.ts lab1 --runs 2`

**Acceptance criteria:** a baseline tool-use score for each run, saved in your notes.

> **Hint:** the checker compares the tools the agent called with the key in `tasks/lab1_prompts.json`. Read the key first.

---

## Part 2: Diagnose the Defects

### Step 3: Find Three Defects with Evidence

Find at least three distinct defects, each with evidence from a run: the tool called, the input passed, and the error returned.

**Acceptance criteria:** a short note in `NOTES.md` listing each defect, which prompt exposed it, and the line of evidence.

> **Hint:** read every description as if you were the model and had no other information.

> **Hint:** compare parameter names with what the handler expects, and read the error messages the handlers return.

> **Hint:** note which prompts should need no tool at all, and what happens to them.

---

## Part 3: Fix the Tool Definitions

### Step 4: Rewrite the Three Descriptions

**Acceptance criteria:** in `tools_inprocess.py` (or `tools.ts`), each description says what the tool does, what input it takes, and when **not** to use it.

### Step 5: Fix the Parameter Names and Schemas

**Acceptance criteria:** each parameter name says what it holds. A parameter with a fixed set of values is an enum.

> **Hint:** in Python, a dict schema like `{"id": str}` cannot express an enum. Use full JSON Schema with `type`, `properties`, `enum` and `required`. In TypeScript use `z.enum([...])`.

> **Common Pitfall:** tools are allowed by full name, `mcp__{server}__{tool}`, so renaming a tool means updating `ALLOWED`.

---

## Part 4: Make the Agent Answer Directly

### Step 6: Stop the Needless Tool Calls

**Acceptance criteria:** the greeting prompt and the arithmetic prompt make no tool call.

> **Hint:** try to fix this in the descriptions first. Use the system prompt only for what the descriptions cannot say, and keep it short.

> **Common Pitfall:** a long system prompt that restates the tool rules hides the defect instead of fixing it, and fails the last rubric row.

---

## Part 5: Confirm the Limits

### Step 7: Verify the Limits and Say Why They Matter

**Acceptance criteria:** `lab1_agent.py` runs with a turn limit and a spend limit, a `tools` value that leaves no built-in tool available, and `setting_sources` empty. State in `NOTES.md` why each matters.

> **Hint:** `make_options` in `agent_core.py` already sets them. Read it. Removing them fails this step.

---

## Part 6: Prove It

### Step 8: Confirm 7 of 8 Across Two Runs

**Acceptance criteria:** the checker shows at least 7 of 8 correct tool-use results in each of two runs, and every answer in the key is right.

---

## Part 7: Checkpoint

### Step 9: Verify Your Progress

- [ ] A baseline tool-use score for two starter runs is saved in your notes
- [ ] `NOTES.md` names at least three defects, each with the prompt that exposed it and a line of evidence
- [ ] `NOTES.md` says which fix removed each defect
- [ ] Every tool description states what it does, what input it takes, and when not to use it
- [ ] Every parameter name says what it holds
- [ ] The policy topic is an enum, and the order id format is stated
- [ ] `ALLOWED` was updated for any tool you renamed
- [ ] The greeting prompt makes no tool call
- [ ] The arithmetic prompt makes no tool call
- [ ] Turn limit, spend limit, empty built-in `tools` and empty `setting_sources` are all still in place
- [ ] `NOTES.md` states why each limit matters
- [ ] `check_prompts.py lab1 --runs 2` shows tool use correct on at least 7 of 8 in **both** runs
- [ ] The system prompt is short and does not restate the tool descriptions

---

## Troubleshooting Reference

| Issue | Symptom | Solution |
|---|---|---|
| No tool ever called | The agent answers from nothing | The tool is not in `allowed_tools` by its full name, or the server name in `mcp_servers` differs from the name in the `mcp__` prefix |
| Enum ignored | `Invalid ... enum`, or your enum has no effect | In Python the simple `{"x": str}` mapping drops enums. Use a full JSON Schema dict |
| Unexpected ToolSearch call | A `ToolSearch` call appears before the first tool call | Tool search is on by default and defers tool schemas. The checker ignores it |
| Run ends early | `error_max_turns` | A handler error made the agent retry. Make the error text your handler returns say what a valid call looks like |
| Missing credential | `ANTHROPIC_API_KEY is not set` | Set it in this shell. The SDK does not read `.env` files |

---

## Scoring Rubric (100 points)

| Criterion | Points |
|---|---|
| Tool use correct on the 8 prompts, 5 points per prompt, counted in the weaker of two runs | 40 |
| Answers correct against the key | 10 |
| Descriptions: each says what, input, and when not to use; parameter names are meaningful | 15 |
| Schema: the policy topic is an enum, and the order id format is stated | 10 |
| Diagnosis note: at least 3 defects, each with evidence from a run | 15 |
| Limits kept, and the reason for each stated | 5 |
| Fix made in the tool definitions first, and the system prompt stays short and does not restate the tool descriptions | 5 |

---

## What You Built

In 90 minutes, you:

- Diagnosed an agent that called the wrong tools, using run evidence rather than guesswork
- Fixed the behavior in the tool definitions, where it belonged, instead of papering over it with a longer system prompt
- Learned that a parameter name and a description are the interface the model actually reads
- Got the agent to stop calling tools for a greeting and for arithmetic
- Held tool use at 7 of 8 or better across two independent runs, not just one lucky one

---

## What's Next

Lab 2, Add a Custom MCP Server, moves the tools out of process. The same description and schema discipline applies, with a protocol boundary in between.

---

## Facilitator Notes

*Where the traps are planted.* All in `tools_inprocess.py` (and `tools.ts`): (1) `order_lookup` is described as "Look up information." and its parameter is named `id`. (2) `customer_lookup` says "Look up information about a person or an order.", which overlaps `order_lookup` and invites an order id, but the handler expects an email. (3) `policy_lookup` says "Get details about anything the customer asks.", which draws a call on the greeting and the arithmetic prompts. Its `topic` is a free string, and the handler matches only `returns`, `shipping`, `warranty` and `price_match` and does not list the valid values in its error.

*Answer key (expected tool use).*

| ID | Prompt | Expected tools | Must not call | Answer contains |
|---|---|---|---|---|
| L1-1 | Where is order BW-1003? | `order_lookup` | customer, policy | in transit, NL-55377 or 2026-10-21 |
| L1-2 | What is your return window? | `policy_lookup` | order, customer | 30 days |
| L1-3 | Greeting: what can you help with? | none | all | any |
| L1-4 | Which orders has maya.ortiz@example.test placed? | `customer_lookup` | policy | BW-1001 and BW-1004 |
| L1-5 | What is 15 percent of 240? | none | all | 36 |
| L1-6 | Can I still return order BW-1005? | `order_lookup`, `policy_lookup` | customer | yes (delivered 2026-09-28, 21 days, window 30) |
| L1-7 | Loyalty tier of the customer on order BW-1002 | `order_lookup`, `customer_lookup` | policy | silver |
| L1-8 | Has order BW-9999 shipped? | `order_lookup` | customer, policy | not found, and no invented status |

The fixed reference solution is `python/facilitator/tools_inprocess.py`. Copy it over `tools_inprocess.py` to restore a working state for a student who is stuck. For TypeScript, the same fixes apply: rename `id` to `order_id` and `email`, rewrite the three descriptions, and use `z.enum(["returns","shipping","warranty","price_match"])`. Tools work without an `isError` change, but strong submissions make the not-found message say what a valid id looks like.

*What good looks like.* The student reads the failing run before editing, makes a single change at a time, and re-runs. Ask: which of your three fixes moved the score most? Watch for a student who writes a long system prompt that restates the tool rules. That hides the defect instead of fixing it and fails the last rubric row.

*Rehearse before the day.* The `ToolSearch` exclusion of the checker assumes that tool name. Confirm it on the class image. Python in-process tool decorators, the dict and JSON Schema forms, `create_sdk_mcp_server`, the `mcp__{server}__{tool}` naming, and the `tools=[]` effect are in the verified facts. Whether `readOnlyHint` changes parallel calls on your SDK version is not tested here; it is a stretch task only.

---

*Lab 1 Complete*
