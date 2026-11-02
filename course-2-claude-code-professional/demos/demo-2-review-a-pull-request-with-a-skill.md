# Demo 2: Review a Pull Request With a Skill

**Course:** Claude Code Professional: Pipelines, Plugins and Enterprise Operations (Claude MasterClass Professional, Course 2)
**Demo:** 2 of 9
**Time:** about 8 minutes

> Part of **[Claude Code Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Run a review on a pull request that has a planted bug, and read what the review found against what it should have. Time: about 8 minutes.

**Files:** [`$FILES/lab2-review`](../demo-files/lab2-review) (`build_fixture.py`, `facilitator/ANSWER-KEY.md`), [`$FILES/demo2-review/claude-code-review.yml`](../demo-files/demo2-review/claude-code-review.yml).

**Context:** There are several ways to get a review: `/code-review` locally, your own CI, or the managed Code Review service. The local command reads `CLAUDE.md` files and not `REVIEW.md`. The service needs a Team or Enterprise plan, an Owner who turns it on, and GitHub. In CI, a review workflow needs `--comment` and an `--allowedTools` entry for the inline comment tool to post inline comments.

**Steps:**

1. Build the fixture and move to a bug branch:

```
python build_fixture.py ~/work/lending-demo
cd ~/work/lending-demo
git checkout pr-03-delete-member
```

2. Start `claude` and run `/code-review`, naming the branch as the target.
3. Compare the findings with the answer key for `pr-03-delete-member`: a handler that never calls `require_role`.
4. Open [`$FILES/demo2-review/claude-code-review.yml`](../demo-files/demo2-review/claude-code-review.yml). Point at the two lines that decide where the review goes: `--comment` and the `claude_args` line with `--allowedTools`. Say the workflow is the documented example and is not run in class.
5. Optional: run `python $FILES/lab1-ci/security_gate.py $FILES/demo2-review/claude-code-review.yml`. It scores 85: no turn limit, no timeout and no concurrency group. A documented example is a start, not a finished pipeline.

**Expected result:** The review reports the missing role check on the delete handler. It may also report extra items. Count them: they are the lead-in to Lab 2.

**Instructor note:** The exact target and effort-level arguments `/code-review` accepts, and its output format, are unconfirmed. Rehearse and adjust step 2. The review uses credits. Fallback: show [`$FILES/lab2-review/sample-findings.json`](../demo-files/lab2-review/sample-findings.json) and run `python score_review.py sample-findings.json`, which needs no model. Do not demo the managed service live unless the sandbox organization is on a Team or Enterprise plan with the service turned on. If it is, `@claude review` on a sandbox pull request, by someone with write access, starts one. Zero Data Retention, HIPAA and customer-managed key configurations do not support it.

**Why this matters:** A review is only worth running if you can say what it caught and what it raised in error. This demo sets up Lab 2, where students score that.

---

**Previous:** [Demo 1: Auto-Fix From a Failing Check](demo-1-auto-fix-from-a-failing-check.md) · **Next:** [Demo 3: Start a Cloud Session and Teleport It](demo-3-start-a-cloud-session-and-teleport-it.md)


*Demo 2 of 9*
