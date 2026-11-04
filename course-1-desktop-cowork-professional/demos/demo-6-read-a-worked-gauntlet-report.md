# Demo 6: Read a Worked Gauntlet Report

**Course:** Claude Desktop Professional, Plugin and Extension Engineering (Claude MasterClass Professional, Course 1)
**Demo:** 6 of 8
**Time:** about 12 minutes

> Part of **[Claude Desktop Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Read a Gauntlet report from the notes column inward, trace each lost point to a fix, and see why Gold depends on the security items. Time: about 12 minutes.

**Files:** [`$FILES/gauntlet/sample-report/run-1-bronze.md`](../demo-files/gauntlet/sample-report/run-1-bronze.md), `run-3-gold.md`, `WALKTHROUGH.md`, and [`$FILES/gauntlet/scorecard.md`](../demo-files/gauntlet/scorecard.md).

**Context:** The Gauntlet scores a plugin out of 100 across structure, an eval suite, context cost, a cold install, an adversarial pack, and a security checklist. Bronze is 60, Silver 75, Gold 90 with all the security points. The two sample reports show the same plugin, Board Pack Builder, before and after fixes.

**Steps:**

1. Show the scoring table in `scorecard.md` and the tier rules, in a minute.
2. Open `run-1-bronze.md`. For each section, read the Note before the points. Ask the class which fix it suggests.
3. Open `WALKTHROUGH.md` and walk the table row by row: what lost points, the fix, the points returned.
4. Open `run-3-gold.md`. Find the two places where points were still lost, and discuss why Gold is not perfect.
5. Show the tension between two fixes: shortening descriptions for cost can stop the skill firing. Say that every cut needs a re-run of the trigger cases.
6. Run the free checks on the flawed plugin to show a live report:

```
python3 $FILES/gauntlet/gauntlet.py --plugin $FILES/autopsy-plugin --product 1 --static-only --out ~/work/static-demo
```

**Expected result:** Run 1 scores 64.4 and is Bronze. Run 3 scores 96.5 and is Gold. The live static report shows the secret in `server/config.json`, the unscoped tools on the reviewer agent, the version mismatch, and the always-on cost of about 2,000 tokens, and it ends with "Not rated" because the eval groups were not run. It scores about 10 of 100.

> **Instructor note:** The two sample reports are illustrative, written by hand in the runner's report format, not output from a live run. Before class, run the full Gauntlet once on your own sandbox account on a plugin you built, price the run, and consider swapping in the real report. The live static run in step 6 is real. Do not run the paid groups on stage.

> **Why this matters:** A score is only useful if you can turn it into a to-do list. The report reads that way once you start from the notes.

---

**Previous:** [Demo 5: Package a Server as an Extension](demo-5-package-a-server-as-an-extension.md) · **Next:** [Demo 7: Review a Plugin Before You Trust It](demo-7-review-a-plugin-before-you-trust-it.md)


*Demo 6 of 8*
