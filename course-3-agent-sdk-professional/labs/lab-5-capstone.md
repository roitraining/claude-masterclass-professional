# Lab 5 (take-home): Capstone

**Course:** Claude Agent SDK Professional
**Duration:** 4 to 6 hours, spread over the week after class
**Format:** Take-home capstone. No automated checker — an instructor reads this one

> Part of **[Claude Agent SDK Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

## Prerequisites

- [ ] Labs 1 through 4 completed — the capstone builds on all four
- [ ] `ANTHROPIC_API_KEY` set in the environment, never in a file
- [ ] `$FILES/capstone/release_note_template.md`, `$FILES/tasks/success_criteria_template.md`, `$FILES/tasks/golden_tasks.json`
- [ ] Fictional data only. Do not use real customer, employee or financial records

> **Token cost.** A 15-task harness across two versions with repeats is the largest spend in this course. Set your cost target in Part 1 and smoke test every stage before a full run.

---

## Overview

The class labs each proved a piece in isolation. The capstone asks for the whole: an agent that uses its tools, reaches data through a standalone server, delegates part of its work, runs inside limits, and is measured.

You may keep the Brightwater domain or choose a small fictional domain of your own. Use only fictional data. Keep every key in the environment, never in a file.

---

## Part 1: Scope the Build

### Step 1: Write the Success Criteria First

Fill the template before you build anything further.

**Acceptance criteria:** a success-criteria file complete, including a cost target, before any more code is written.

---

## Part 2: Build the Agent and Its Tools

### Step 2: Ship at Least Three In-Process Tools

**Acceptance criteria:** at least 3 in-process tools with specific descriptions and schemas, and the Lab 1 prompts still pass.

---

## Part 3: Add the Standalone Server

### Step 3: Connect a Stdio Server by Explicit Tool Name

**Acceptance criteria:** a standalone stdio server with at least 2 tools, connected by explicit full tool names with no wildcard.

> **Note:** if the server returns text written by people or fetched from outside, include a planted injection and show it contained by a control, not by a prompt rule.

---

## Part 4: Add a Subagent and Set Limits

### Step 4: Delegate Work That Benefits from a Fresh Context Window

**Acceptance criteria:** one subagent defined in code, used for a task that genuinely benefits from a fresh context window.

### Step 5: Set and Justify the Limits Against a Runaway of Your Own

**Acceptance criteria:** turn, depth, concurrency and spend limits are set and justified from measurements, and a runaway fixture of your own design is stopped by those limits.

> **Hint:** measure the real task first, then set each cap with margin. A limit chosen without a measurement behind it scores nothing in the rubric.

---

## Part 5: Build the Harness

### Step 6: Score Two Versions Across at Least Fifteen Tasks

**Acceptance criteria:** at least 15 golden tasks with keys derived from your data, code graders over the answer **and** the tool calls, a calibrated judge for one open-ended output, two compared versions, a tier, and at least 2 repeats on the risky tasks.

> **Key Insight:** derive every key from the data by hand. A harness built from agent output grades the agent against itself and always passes.

---

## Part 6: Write the Release Note

### Step 7: One Page, Every Claim Backed by a Result

**Acceptance criteria:** one page from `release_note_template.md` covering limits, data reach, human review, the score, and at least 2 known gaps. Every claim is backed by a result you can point to.

> **Common Pitfall:** a vague data-reach section ("it can access order data") is the most common weakness. Name each tool, say whether it reads or writes, and say what it can reach.

> **Common Pitfall:** state what *enforces* each limit, not what you hope. Intentions are not controls.

---

## Part 7: Write the README

### Step 8: Make It Runnable from a Fresh Clone

**Acceptance criteria:** how to set the key as an environment variable, how to install, how to run the agent, and how to run the harness.

---

## Part 8: Checkpoint

### Step 9: Verify Your Progress

- [ ] Success criteria written before the build, with a cost target
- [ ] At least 3 in-process tools with specific descriptions and schemas
- [ ] The Lab 1 prompts still pass
- [ ] A standalone stdio server with at least 2 tools
- [ ] The server is allowed by explicit full tool names, with no wildcard
- [ ] Any people-written or externally fetched text carries a planted injection, shown contained by a control
- [ ] One subagent defined in code, used where a fresh context window helps
- [ ] Turn, depth, concurrency and spend limits all set, each justified from a measurement
- [ ] A runaway fixture of your own design is stopped by those limits
- [ ] At least 15 golden tasks, with keys derived by hand from your data
- [ ] Graders cover the answer **and** the tool calls
- [ ] A judge calibrated and used for exactly one open-ended output
- [ ] Two versions compared, with a tier and at least 2 repeats on the risky tasks
- [ ] A one-page release note covering limits, data reach, human review, score and 2 known gaps
- [ ] Every release-note claim traceable to a result file
- [ ] No key or token in any file or commit
- [ ] Fictional data only
- [ ] A fresh clone runs: the README setup works, the agent answers a task, and the harness prints a tier

---

## Troubleshooting Reference

| Issue | Symptom | Solution |
|---|---|---|
| Harness always passes | Every task green on the first try | It is grading the agent against its own output. Derive keys from the data by hand |
| Write tool reachable | A wildcard allow-list on a server that has a write tool | List explicit full tool names. Remove what the agent does not need |
| Tier not trustworthy | A passing tier from one run per task | Add repeats before you claim it. A single run proves little |
| Release note reads as a wish list | Reviewer cannot tell what is enforced | Say what enforces each limit. Name the control, not the intention |
| Secret committed | A key in a file or in git history | Remove it, rotate it, and use the environment variable. A submission containing a key is rejected |

---

## Scoring Rubric (100 points)

| Criterion | Points |
|---|---|
| Agent and tools: specific descriptions and schemas, correct tool use on the prompts | 15 |
| Standalone MCP server: works, explicit allow-list, injection contained with a control | 15 |
| Subagent and limits: delegation works, limits set from measurements, a runaway stopped | 15 |
| Harness: 15 or more golden tasks, tool-call graders, calibrated judge, two versions, repeats, tier | 25 |
| Release note: limits, data reach, human review and score are specific and supported | 20 |
| Hygiene: no secrets in files, README runs from a fresh clone, fictional data only | 10 |

---

## What You Built

Over 4 to 6 hours, you:

- Assembled the four isolated lab pieces into one solution: tools, a standalone server, a subagent, limits and a harness
- Set every limit from a measurement rather than a guess, and proved them against a runaway you designed yourself
- Built a harness large enough to be worth trusting, with keys derived by hand so it cannot grade the agent against itself
- Wrote a release note where every claim points at a result, and named the gaps you chose not to hide
- Made it runnable by someone else from a fresh clone, with no secret anywhere in the repository

---

## What's Next

This is the final lab in Claude Agent SDK Professional. The habit worth keeping is the release note: limits, data reach, human review, score, known gaps. It is the document that makes an agent reviewable by someone who did not build it.

---

## Facilitator Notes

Use the Lab 1 to Lab 4 answer keys for spot checks. Strong capstones show a regression between versions and a gap the student chose not to hide.

Read the release note first: a vague data-reach section ("it can access order data") is the most common weakness, and the fix is to name each tool, say whether it reads or writes, and say what it can reach. Penalize a note that states a score the results file does not show.

Reject any submission that contains a key or token, and tell the student to rotate it.

There is no automated checker for the capstone. Plan instructor time to read them.

---

*Lab 5 Complete*
