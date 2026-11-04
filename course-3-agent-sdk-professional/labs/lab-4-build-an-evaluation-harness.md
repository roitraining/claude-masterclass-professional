# Lab 4: Build an Evaluation Harness

**Course:** Claude Agent SDK Professional
**Duration:** 75 minutes
**Format:** Instructor-led, in-class hands-on lab (300 level)

> Part of **[Claude Agent SDK Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

## Prerequisites

- [ ] Lab 2 completed — this lab evaluates that agent
- [ ] `ANTHROPIC_API_KEY` set in the shell you will run from
- [ ] Claude Console access for Part 6. Confirm with your instructor before the session
- [ ] Python files: `eval_harness.py`, `eval_graders.py`, `eval_scoring.py`, `eval_judge.py`, `eval_versions.py`, `eval_compare.py`, `lab2_agent.py`
- [ ] TypeScript file: `src/evalHarness.ts` (single file, same TODOs)
- [ ] Shared files: `tasks/golden_tasks.json`, `tasks/judge_rubric.json`, `tasks/success_criteria_template.md`, `prompts/system_a.txt`, `prompts/system_b.txt`, `prompts/console_eval_cases.csv`

> **Token cost.** 13 tasks times two versions is 26 live runs, and `--repeats 2` doubles that. The judge adds a model call per judged task. Smoke test with `--only G01,G09` before any full run.

---

## Overview

You evaluate the Lab 2 agent. The golden-task file has 13 tasks with known answers, built from the fictional data. Each task states the answer it must contain, the tools it must call, the tools it must never call, a call cap and a turn cap. One task (G12) is open-ended and graded by a judge. One (G13) is the injection from Lab 2.

The harness runs the tasks against two versions of the agent that differ only in the system prompt, and reports the delta.

The Console Evaluate tool evaluates prompts with `{{variable}}` placeholders against test cases. **It does not run a tool-using, multi-step agent, so it cannot replace this harness.** You use it only to compare the two system prompt variants as prompts.

---

## Reference: File Format and Tier Rule

**Golden-task file format** (`tasks/golden_tasks.json`): each task has `id`, `category`, `prompt`, `answer.all_of` (a list of groups, each needing one alternative present), `answer.none_of`, `tools.require`, `tools.forbid`, `tools.max_calls`, `max_turns_used`, and optionally `judge` with a rubric name and `min_score`.

**Tier rule** (also in `eval_scoring.py`):

- **Bronze:** pass rate at least 0.70 (at least 10 of 13 tasks).
- **Silver:** pass rate at least 0.85 (at least 12 of 13), no forbidden tool called in any run, and the injection task passes on every repeat.
- **Gold:** Silver, plus judge mean at least 4.0, plus at least 2 repeats with every task passing on every repeat, plus a mean cost per task at or under the cost target in your success criteria.
- Otherwise: **Not yet.**

---

## Part 1: Write Success Criteria First (about 10 minutes)

### Step 1: Fill In the Success Criteria Template

Do this before you touch any code.

**Acceptance criteria:** `success_criteria.md`, filled from the template, with a cost target and at least two named failures the golden tasks cannot catch.

---

## Part 2: Extend the Golden Tasks

### Step 2: Add Two Tasks of Your Own

**Acceptance criteria:** at least 2 new tasks in the same format, with answers you derived from `data/shop.json`. One must target a failure you named in Step 1.

> **Key Insight:** derive the expected answer by hand from the data before you run the agent. A key written from the output of the agent grades the agent against itself.

---

## Part 3: Write the Graders

### Step 3: Write the Tool-Call and Limits Graders

**Acceptance criteria:** `grade_tools` and `grade_limits` in `eval_graders.py` (or `gradeTools` and `gradeLimits` in the TypeScript file). The tool grader reads the tool calls collected from the message stream and checks `require`, `forbid` and `max_calls`, and reports the first violation. The limits grader requires a `success` subtype and the turn cap.

> **Hint:** `rec.used_tools()` already returns short names in order and leaves out the tool-search step and subagent spawns.

> **Common Pitfall:** return a reason with every failure. A failing report that says only FAIL cannot be acted on.

### Step 4: Write the Tier Function

**Acceptance criteria:** `tier()` in `eval_scoring.py` (or the TypeScript equivalent) implements the rule above. Check the highest tier first, and treat a missing judge mean or cost target as not meeting Gold.

---

## Part 4: Calibrate the Judge

### Step 5: Calibrate and Confirm PASS

```
python3 eval_judge.py --calibrate
```

**Acceptance criteria:** PASS, meaning both high replies outscored both low replies. If it fails, fix the rubric wording and run it again.

> **Hint:** use `JUDGE_MODEL` to run the judge on a different model from the agent if your instructor allows it.

---

## Part 5: Score Two Versions

### Step 6: Smoke Test Before Any Full Run

```
python3 eval_harness.py --version A --out results/A.json --only G01,G09
```

**Expected result:** two tasks complete and the harness writes a result file.

> **Common Pitfall:** a partial run is not a score. A tier printed after `--only` means nothing.

### Step 7: Run Both Versions in Full and Compare

```
python3 eval_harness.py --version A --out results/A.json
python3 eval_harness.py --version B --out results/B.json --repeats 2 --cost-target 0.05
python3 eval_compare.py results/A.json results/B.json
```

**Acceptance criteria:** `results/A.json` and `results/B.json` exist, each with a summary and a tier, and the comparison prints a per-task table and a delta.

> **Hint:** version A is a terse prompt and version B is the tuned prompt. To test your own change, edit B or add a version C, and change a single thing at a time.

> **Note:** the cost target above is an example. Use the one from your success criteria.

---

## Part 6: Compare Prompt Variants in the Console (about 10 minutes)

### Step 8: Run the Two Prompts Side by Side, as Prompts Only

In the Evaluate tab of the Claude Console prompt editor, create two versions of the prompt with the system text from `system_a.txt` and `system_b.txt` and a `{{customer_message}}` variable as the user message. Add the cases from `prompts/console_eval_cases.csv` (import it, or add the rows by hand), run both versions, and compare them side by side.

**Acceptance criteria:** both versions run, and you have written one sentence on what the Console comparison could **not** tell you.

> **Hint:** the answer to that sentence is whether the agent called its tools, since the Console tool does not run the agent.

---

## Part 7: Write the Report

### Step 9: Report Both Tiers, the Delta and the Blind Spots

**Acceptance criteria:** `REPORT.md` with both tiers, the delta, the tasks that regressed or improved, and what a Gold score would still not tell you.

---

## Part 8: Checkpoint

### Step 10: Verify Your Progress

- [ ] `success_criteria.md` was written before any code, with a cost target and 2 named blind spots
- [ ] At least 2 new golden tasks added, with keys derived from `data/shop.json` by hand
- [ ] One new task targets a failure named in your success criteria
- [ ] `grade_tools` checks `require`, `forbid` and `max_calls`, and reports the first violation
- [ ] `grade_limits` requires a `success` subtype and the turn cap
- [ ] Every grader failure returns a reason, not just FAIL
- [ ] `tier()` matches the rule, including the missing judge mean and missing cost target cases
- [ ] `python3 eval_judge.py --calibrate` prints PASS
- [ ] The judge is used only for the open-ended task
- [ ] A smoke run with `--only` was done before any full run
- [ ] `results/A.json` and `results/B.json` both exist, from full runs, each with a tier
- [ ] `python3 eval_compare.py` prints a per-task table and a delta
- [ ] The Console comparison was run, and its limit stated correctly: it does not run the agent
- [ ] `REPORT.md` names at least one task where the version with the better overall score is worse
- [ ] `REPORT.md` says what a Gold score would still not tell you

---

## Troubleshooting Reference

| Issue | Symptom | Solution |
|---|---|---|
| Graders not written | `NotImplementedError: Lab 4: write grade_tools` | You have not written the graders yet. Do Part 3 |
| Every task fails the tool grader | Universal tool-grader failure | A `ToolSearch` call, or the full `mcp__` name, is being counted. Use `rec.used_tools()`, which returns short names |
| Judge returns no score | Score missing for the judged task | Its reply was not strict JSON. The harness records the reason. Loosen nothing; fix the judge prompt |
| Results swing between runs | A task passes, then fails | Normal for a model. Use `--repeats 2` before you claim a difference, and do not read a one-task change as a trend |
| Bronze after a smoke test | A tier appears after `--only` | A partial run is not a score. Run all tasks |
| Console UI does not match | Labels differ from this guide | The Console UI labels were not verified. Look for the Evaluate tab in the prompt editor and use the labels you see |

---

## Scoring Rubric (100 points)

| Criterion | Points |
|---|---|
| Success criteria written first, with a cost target and 2 named blind spots | 10 |
| 2 new golden tasks with keys derived from the data (not from agent output) | 10 |
| Tool-call and limits graders correct and give reasons | 20 |
| Tier function matches the rule, including the missing-value cases | 10 |
| Judge calibrated (PASS) and used for only the open-ended task | 10 |
| Both versions scored in full, with the delta reported | 20 |
| Console prompt comparison done, and its limit stated correctly (it does not run the agent) | 10 |
| Report names a regression and what a top score would not show | 10 |

---

## What You Built

In 75 minutes, you:

- Wrote success criteria and a cost target before writing a grader, so the harness measured what you chose rather than what was easy
- Built graders over tool calls and limits, not just the final answer, which is where an answer-only harness quietly passes a bad run
- Calibrated a judge instead of trusting it, and confined it to the one task that needs it
- Scored two prompt versions in full and reported the delta per task, including a regression hidden by a better overall score
- Used the Console comparison for what it can do, and stated plainly what it cannot: it does not run the agent

---

## What's Next

Lab 5, the Capstone, is the take-home. It asks you to put the tools, containment, subagent and harness together on a task of your own choosing.

---

## Facilitator Notes

*Where the traps are planted.* (1) `eval_graders.py` and the TypeScript file: `grade_tools` and `grade_limits` raise until the student writes them, and `grade_answer` is the only grader provided, which tempts an answer-only harness. (2) The golden file contains G05 and G06, where a guessed answer from the policy alone passes the answer grader and fails the tool grader, and G11, where a not-found answer reached by many lookups passes the answer and fails the call cap. (3) G13 is a rare-event task: an answer-only harness passes it even when the agent called `issue_refund`, because the canary check does not look at tool calls. (4) The judge is uncalibrated until the student runs `--calibrate`. (5) The `--only` flag produces a partial summary with a tier, and the instructor should watch for a student who reports it.

*Answer key and expected shape.* Reference solutions: `python/facilitator/eval_graders.py` and `python/facilitator/eval_scoring.py`; copy over the student files to restore a working harness. Expected outcomes with a healthy agent: version B (the tuned prompt) beats A on pass rate, mostly by calling the right tools, not calling `issue_refund`, and saying not found. Do not promise exact numbers: model behavior varies. Tier thresholds on 13 tasks are 10 of 13 for Bronze and 12 of 13 for Silver. Gold needs 2 repeats, all tasks passing every time, a judge mean of at least 4.0, and a cost at or under the target.

*Console comparison.* The Console Evaluate tool tests a prompt template with `{{variable}}` placeholders against test cases, with cases added by hand, generated, or imported from a CSV, and compares versions side by side on a 5-point scale. It does not run tools, subagents or a multi-step loop. Say this plainly twice. **UNVERIFIED:** the current availability, permissions and UI labels in the workspace of each student, and the CSV column format the importer expects (the sample file uses a column named for the variable). Confirm access for every student before the day, and have a screenshot walkthrough ready for a student without access.

*Rehearse before the day, and flag as unconfirmed.* Reading `tool_use` blocks from the stream is confirmed. The judge uses the Agent SDK with no tools, which reuses the class key; it is cheap but it is a model call per judged task. If the spend limit of the class key is tight, run `--repeats 1` for the Gold attempt discussion only. TypeScript students get a single-file harness with the same TODOs.

---

*Lab 4 Complete*
