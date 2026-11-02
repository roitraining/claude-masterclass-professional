# Demo 7: Grade a Run With Code and a Judge

**Course:** Claude Agent SDK Professional: Building and Evaluating Production Agents (Claude MasterClass Professional, Course 3)
**Demo:** 7 of 8
**Time:** about 12 minutes

> Part of **[Claude Agent SDK Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Grade recorded agent runs with code graders over the final answer and the tool calls, then add a judge for an open-ended answer. Time: about 12 minutes. (Module 13)

**Files:** [`$FILES/python/demo7_grade.py`](../demo-files/python/demo7_grade.py), [`$FILES/recorded/demo7_runs.json`](../demo-files/recorded/demo7_runs.json), [`$FILES/tasks/judge_rubric.json`](../demo-files/tasks/judge_rubric.json).

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

**Previous:** [Demo 6: Cap Turns, Depth, and Spend](demo-6-cap-turns-depth-and-spend.md) · **Next:** [Demo 8: What a Passing Score Misses](demo-8-what-a-passing-score-misses.md)


*Demo 7 of 8*
