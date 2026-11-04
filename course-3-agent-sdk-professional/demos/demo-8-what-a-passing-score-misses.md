# Demo 8: What a Passing Score Misses

**Course:** Claude Agent SDK Professional: Building and Evaluating Production Agents (Claude MasterClass Professional, Course 3)
**Demo:** 8 of 8
**Time:** about 12 minutes

> Part of **[Claude Agent SDK Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Show a suite that scores 100 percent on answers while hiding a tool misuse, a cost spike and a rare injection, and place evaluation as one input to a larger production picture. Time: about 12 minutes. (Module 15)

**Files:** [`$FILES/python/demo8_scorecard.py`](../demo-files/python/demo8_scorecard.py), [`$FILES/recorded/demo8_runs.json`](../demo-files/recorded/demo8_runs.json).

**Context:** The recorded data is one run of each of 12 golden tasks, plus 20 repeats of a notes task that no golden task covers. All numbers are fictional.

**Steps:**

1. Run the scorecard:

```
cd $FILES/python
python3 demo8_scorecard.py
```

2. Stop after section 1. Ask the room whether they would ship. The answer-only score is 12 of 12.
3. Section 2 adds a tool-call grader. Show G12: a correct reply that also called `issue_refund`. Show G11: a correct "not found" answer reached with 12 lookups.
4. Section 3 adds cost. Show G11 costing about nine times the median. A correct answer can still be a cost spike.
5. Section 4 shows the injection. One run in 20 followed it, and no suite task reads those notes, so the suite could not see it. Link it to Lab 2.
6. Close on the production picture: limits and budgets that stop a bad run, human review where an action cannot be undone, alerts on cost and tool calls, repeats on risky tasks, and the golden-task file as a living document.

**Expected result:** The answer grader passes 12 of 12. Adding the tool grader drops it to 10 of 12. The cost rule flags G11. The injection appears only in the repeats.

> **Instructor note:** All data is hand-written for the demo and fictional. Do not present it as measured behavior of any model. The principle matches the verified facts: the Console Evaluate tool and a final-answer check evaluate what they are asked, and an agent's tool use and cost need their own graders. Whether a real agent follows the planted injection varies by model and prompt. Students will measure it in Lab 2. **Fallback:** none needed, the demo is offline.

> **Why this matters:** A green dashboard is a statement about the tests, not about the agent. Production risk lives in what the tests never ask.

---

**Previous:** [Demo 7: Grade a Run With Code and a Judge](demo-7-grade-a-run-with-code-and-a-judge.md)


*Demo 8 of 8*
