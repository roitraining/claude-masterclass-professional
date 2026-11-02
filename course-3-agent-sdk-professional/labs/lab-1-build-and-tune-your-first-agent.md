# Lab 1: Build and Tune Your First Agent

> Part of **[Claude Agent SDK Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

**Learning objective:** Build a minimal agent with custom tools, diagnose why it calls the wrong tool or no tool, and fix the tool descriptions and schemas. Time: 90 minutes.

**Files:** Python: `agent_core.py`, `shop_data.py`, `tools_inprocess.py`, `lab1_agent.py`, `check_prompts.py`. TypeScript: `src/agentCore.ts`, `src/shopData.ts`, `src/tools.ts`, `src/lab1Agent.ts`, `src/checkPrompts.ts`. Shared: `data/shop.json`, `tasks/lab1_prompts.json`.

**Context:** You inherit the support agent for Brightwater Outfitters, a fictional outdoor retailer. A fake backend module stands in for the order system. Three tools work correctly: `order_lookup`, `customer_lookup` and `policy_lookup`. The agent still uses them badly. Your job is to find out why from evidence, and fix it in the tool definitions before touching the system prompt.

**Steps:**

1. **Goal: run the starter and capture a baseline.**
   - Run one prompt, then all eight, twice:

```
python lab1_agent.py "Where is order BW-1003?"
python check_prompts.py lab1 --runs 2
```

   TypeScript: `npx tsx src/lab1Agent.ts "Where is order BW-1003?"` and `npx tsx src/checkPrompts.ts lab1 --runs 2`.
   - Acceptance: you have a baseline tool-use score for each run, saved in your notes.
   - Hint: the checker compares the tools the agent called with the key in `tasks/lab1_prompts.json`. Read the key first.
2. **Goal: diagnose.** Find at least three distinct defects, each with evidence from a run (the tool called, the input passed, the error returned).
   - Acceptance: a short note in `NOTES.md` listing each defect, which prompt exposed it, and the line of evidence.
   - Hints: read every description as if you were the model and had no other information. Compare parameter names with what the handler expects. Read the error messages the handlers return. Note which prompts should need no tool and what happens to them.
3. **Goal: fix the tool definitions.**
   - Acceptance: in `tools_inprocess.py` (or `tools.ts`), each description says what the tool does, what input it takes, and when not to use it. Each parameter name says what it holds. A parameter with a fixed set of values is an enum.
   - Hints: in Python, a dict schema like `{"id": str}` cannot express an enum. Use full JSON Schema (`type`, `properties`, `enum`, `required`). In TypeScript use `z.enum([...])`. Tools are allowed by full name, `mcp__{server}__{tool}`, so renaming a tool means updating `ALLOWED`.
4. **Goal: make the agent answer directly when it should.**
   - Acceptance: the greeting and the arithmetic prompts make no tool call.
   - Hint: first try to fix it in the descriptions. Use the system prompt only for what the descriptions cannot say, and keep it short.
5. **Goal: confirm the limits.**
   - Acceptance: `lab1_agent.py` runs with a turn limit and a spend limit, a `tools` value that leaves no built-in tool available, and `setting_sources` empty. Say in `NOTES.md` why each matters.
   - Hint: `make_options` in `agent_core.py` already sets them. Read it. A student who removes them fails this step.
6. **Goal: prove it.**
   - Acceptance: the checker shows at least 7 of 8 correct tool-use results in each of two runs, and every answer in the key is right.

**Checkpoint:** `python check_prompts.py lab1 --runs 2` shows tool use correct on at least 7 of 8 in both runs. `NOTES.md` names at least three defects with evidence and says which fix removed each.

**Common problems:**

- The agent never calls a tool: the tool is not in `allowed_tools` by its full name, or the server name in `mcp_servers` differs from the name in the `mcp__` prefix.
- `Invalid ... enum` or a schema that ignores your enum: in Python the simple `{"x": str}` mapping drops enums. Use a full JSON Schema dict.
- A ToolSearch call appears before the first tool call: tool search is on by default and defers tool schemas. The checker ignores it.
- The run ends with `error_max_turns`: a handler error made the agent retry. Read the error text your handler returns and make it say what a valid call looks like.
- `ANTHROPIC_API_KEY is not set`: set it in this shell. The SDK does not read `.env` files.

**Scoring rubric (100 points):**

| Criterion | Points |
|---|---|
| Tool use correct on the 8 prompts, 5 points per prompt, counted in the weaker of two runs | 40 |
| Answers correct against the key | 10 |
| Descriptions: each says what, input, and when not to use; parameter names are meaningful | 15 |
| Schema: the policy topic is an enum, and the order id format is stated | 10 |
| Diagnosis note: at least 3 defects, each with evidence from a run | 15 |
| Limits kept, and the reason for each stated | 5 |
| Fix made in the tool definitions first, and the system prompt stays short and does not restate the tool descriptions | 5 |

**Facilitator note:**

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

*Rehearse before the day.* The checker's `ToolSearch` exclusion assumes that tool name. Confirm it on the class image. Python in-process tool decorators, the dict and JSON Schema forms, `create_sdk_mcp_server`, the `mcp__{server}__{tool}` naming, and the `tools=[]` effect are in the verified facts. Whether `readOnlyHint` changes parallel calls on your SDK version is not tested here; it is a stretch task only.
