# Demo 4: A Routine Versus an Actions Workflow

**Course:** Claude Code Professional: Pipelines, Plugins and Enterprise Operations (Claude MasterClass Professional, Course 2)
**Demo:** 4 of 9
**Time:** about 8 minutes

> Part of **[Claude Code Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Compare a routine and an Actions workflow that react to the same GitHub event, and choose between them. Time: about 8 minutes.

**Files:** [`$FILES/demo4-routine-vs-actions/comparison.md`](../demo-files/demo4-routine-vs-actions/comparison.md), [`$FILES/lab1-ci/facilitator/github/claude-review.yml`](../demo-files/lab1-ci/facilitator/github/claude-review.yml).

**Context:** Routines are a research preview. They run on Anthropic infrastructure, need no workflow file, belong to a single account, can run on a schedule (one hour minimum), through an API call, or on a GitHub event, and have no permission-mode picker. An Actions workflow runs on a GitHub runner, from a file in the repository, with your secrets and your permissions block.

**Steps:**

1. Take the trigger "a pull request is opened". Open the hardened workflow `claude-review.yml` and name what governs it: permissions, who can trigger, secrets, limits.
2. In the sandbox account, show the routine's configuration screen for a GitHub event trigger. Do not save one that acts.
3. Fill in the right-hand column of `comparison.md` from what you see on screen, and the left from the course facts.
4. Ask the class to choose for three cases: a team review that must be auditable, a personal morning summary, and a pipeline whose output must start CI.
5. End on the owner question: who owns a routine when its account holder leaves.

**Expected result:** The class picks a workflow for the shared, auditable cases, and a routine only for personal automation. They name the owner as a risk.

**Instructor note:** Instructor and sandbox account only. How a routine is created and what its screens show are not confirmed in the verified facts, so the table's routine cells marked "check on screen" must be filled live or left blank. Fallback: screenshots of both configurations, or the table with only the documented rows filled in. Do not claim what a routine can or cannot grant until you have seen it.

**Why this matters:** Teams pick a place to run automation by habit. The choice decides who can review it, who can trigger it, and what happens when a person leaves.

---

**Previous:** [Demo 3: Start a Cloud Session and Teleport It](demo-3-start-a-cloud-session-and-teleport-it.md) · **Next:** [Demo 5: Find the Missing Checkpoint](demo-5-find-the-missing-checkpoint.md)


*Demo 4 of 9*
