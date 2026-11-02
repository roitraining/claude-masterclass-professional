# Lab 5 (take-home): Capstone

> Part of **[Claude Agent SDK Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

**Learning objective:** Combine an agent, its tools, a standalone MCP server, a subagent and an evaluation harness into a single deployed-style solution, and write a one-page release note covering limits, data reach and the score. Time: take-home, plan for 4 to 6 hours over the week after class.

**Files:** Your Lab 1 to Lab 4 work, plus `$FILES/capstone/release_note_template.md`, `$FILES/tasks/success_criteria_template.md`, `$FILES/tasks/golden_tasks.json`.

**Context:** The class labs each proved a piece in isolation. The capstone asks for the whole: an agent that uses its tools, reaches data through a standalone server, delegates part of its work, runs inside limits, and is measured. You may keep the Brightwater domain or choose a small fictional domain of your own. Use only fictional data. Keep every key in the environment, never in a file.

**Steps:**

1. **Goal: scope it.**
   - Acceptance: a success-criteria file filled from the template, before you build further.
2. **Goal: the agent and its tools.**
   - Acceptance: at least 3 in-process tools with specific descriptions and schemas, and the Lab 1 prompts still pass.
3. **Goal: the standalone MCP server.**
   - Acceptance: a standalone stdio server with at least 2 tools, connected by explicit full tool names with no wildcard. If it serves text written by people or fetched from outside, include a planted injection and show it contained.
4. **Goal: a subagent and limits.**
   - Acceptance: one subagent defined in code, used for a task that benefits from a fresh context window. Turn, depth, concurrency and spend limits are set and justified from measurements. A runaway fixture of your own design is stopped by those limits.
5. **Goal: the harness.**
   - Acceptance: at least 15 golden tasks with keys derived from your data, code graders over the answer and the tool calls, a calibrated judge for one open-ended output, two compared versions, a tier, and at least 2 repeats on the risky tasks.
6. **Goal: the release note.**
   - Acceptance: one page from `release_note_template.md` covering limits, data reach, human review, the score, and at least 2 known gaps. Every claim is backed by a result you can point to.
7. **Goal: a short README.**
   - Acceptance: how to set the key as an environment variable, how to install, how to run the agent, how to run the harness.

**Checkpoint:** A fresh clone runs: the setup commands in the README work, the agent answers a task, and the harness prints a tier.

**Common problems:**

- The harness grades the agent against its own output: derive keys from the data by hand.
- A wildcard allow-list on a server that has a write tool: list explicit names.
- A passing tier with one run per task: add repeats before you claim it.
- The release note lists intentions, not controls: say what enforces each limit, not what you hope.
- A key in a file or a commit: remove it, rotate it, and use the environment variable.

**Scoring rubric (100 points):**

| Criterion | Points |
|---|---|
| Agent and tools: specific descriptions and schemas, correct tool use on the prompts | 15 |
| Standalone MCP server: works, explicit allow-list, injection contained with a control | 15 |
| Subagent and limits: delegation works, limits set from measurements, a runaway stopped | 15 |
| Harness: 15 or more golden tasks, tool-call graders, calibrated judge, two versions, repeats, tier | 25 |
| Release note: limits, data reach, human review and score are specific and supported | 20 |
| Hygiene: no secrets in files, README runs from a fresh clone, fictional data only | 10 |

**Facilitator note:** Use the Lab 1 to Lab 4 answer keys for spot checks. Strong capstones show a regression between versions and a gap they chose not to hide. Read the release note first: a vague data-reach section ("it can access order data") is the most common weakness, and the fix is to name each tool, say whether it reads or writes, and say what it can reach. Penalize a note that states a score the results file does not show. Reject any submission that contains a key or token, and tell the student to rotate it. There is no automated checker for the capstone. Plan instructor time to read them.
