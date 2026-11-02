# Demo 5: Find the Missing Checkpoint

**Course:** Claude Code Professional: Pipelines, Plugins and Enterprise Operations (Claude MasterClass Professional, Course 2)
**Demo:** 5 of 9
**Time:** about 10 minutes

> Part of **[Claude Code Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Find the step in an unattended pipeline where a human checkpoint is missing, and say where one does not belong. Time: about 10 minutes.

**Files:** [`$FILES/demo5-checkpoint/nightly-fix-and-ship.yml`](../demo-files/demo5-checkpoint/nightly-fix-and-ship.yml), [`$FILES/demo5-checkpoint/checkpoint-map.md`](../demo-files/demo5-checkpoint/checkpoint-map.md), [`$FILES/lab1-ci/security_gate.py`](../demo-files/lab1-ci/security_gate.py).

**Context:** Reviewing every change locally and acting on a pipeline's behalf with nobody watching are different risks. A pipeline that Claude runs nightly can be perfectly hygienic and still ship something no person has read.

**Steps:**

1. Hand out `checkpoint-map.md`. Read `nightly-fix-and-ship.yml` with the class: a nightly schedule, Claude fixes failing tests and moves dependencies, a pull request is opened and set to merge itself, a deploy job follows.
2. Run the gate: `python security_gate.py nightly-fix-and-ship.yml`. It scores 100. Ask what that tells you, and what it cannot tell you.
3. Let pairs mark the table for three minutes, then take answers.
4. Settle the answers (see the instructor note).
5. Ask the second question: which steps should not get a checkpoint, and why.

**Expected result:** The class finds that the pull request merges itself and the deploy follows, so a change reaches production with no person reading it. They propose a required human approval before merge and a required reviewer on the production environment, and they leave the schedule, Claude's work and its push alone.

**Instructor note:** The answer: the missing checkpoint is between "Claude's change" and "production". The merge sets itself to complete and the deploy follows, so nobody reads the diff. Place one checkpoint at the merge (a required human approval) and one before deploy to production (a required reviewer). A subtle one: Claude can "fix" a failing test by changing the test, so the pull request review should look at test edits first. Where a checkpoint does not belong: the trigger (a schedule starts nothing new), Claude's run itself (a person mid-run defeats unattended work, and Claude's push is isolated on a branch), and opening the pull request. Rules of thumb: put the checkpoint where the change gains the power to hurt someone, and make it cheap to pass when the change is small. Branch protection and environment reviewers are repository settings that the course facts do not cover. Show them in the sandbox only after rehearsal, and do not claim how a platform enforces them.

**Why this matters:** The most expensive pipeline failures are not leaked secrets. They are changes nobody read. Hygiene scores do not measure that.

---

**Previous:** [Demo 4: A Routine Versus an Actions Workflow](demo-4-a-routine-versus-an-actions-workflow.md) · **Next:** [Demo 6: Install a Plugin From a Marketplace](demo-6-install-a-plugin-from-a-marketplace.md)


*Demo 5 of 9*
