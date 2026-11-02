# Demo 1: Auto-Fix From a Failing Check

**Course:** Claude Code Professional: Pipelines, Plugins and Enterprise Operations (Claude MasterClass Professional, Course 2)
**Demo:** 1 of 9
**Time:** about 6 minutes

> Part of **[Claude Code Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Show Claude fixing a pull request whose CI check is failing, and name what lets it do that. Time: about 6 minutes.

**Files:** [`$FILES/lab1-ci/tallybook`](../demo-files/lab1-ci/tallybook) (the sample repository), staged in the ROI sandbox before class.

**Context:** `/autofix-pr` and the Auto-fix toggle watch a pull request and fix CI failures and review comments. They need the Claude GitHub App on the repository. A cloud session does the work, so the pull request must be on GitHub.

**Steps:**

1. Before class, in the ROI sandbox: copy `tallybook` into a sandbox repository, install the Claude GitHub App, add the CI workflow `.github/workflows/ci.yml`, and open a pull request that adds a small helper. CI fails on the two known failing tests.
2. In class, show the pull request with its red check. Name the two failing tests.
3. In a terminal in a clone of the sandbox repository, check out the pull request branch and start a session:

```
git checkout <pr-branch>
claude
```

4. Run `/autofix-pr` and let it attach to the pull request.
5. Wait for the new commit and the re-run of CI. Open the diff.
6. Ask the class what Claude was allowed to do, and what stopped it from merging.

**Expected result:** A new commit on the pull request branch changes `monthly_total` so the tests pass, and the check turns green. Claude does not merge the pull request.

**Instructor note:** Sandbox only, instructor only. The exact way `/autofix-pr` is pointed at a pull request, whether it asks you to choose one, and how long a fix takes are not in the verified facts. Rehearse once and time it. Fallback if it runs long or fails: a local simulation. In a local copy of `tallybook`, run `python -m pytest -q` to show the failures, tell Claude "make the failing tests pass and change nothing else", show the diff, and say the pipeline version of the same loop is the one you just described. A second fallback is a screenshot set of a previous run, taken during rehearsal.

**Why this matters:** Auto-fix is the first unattended action students meet. It acts on a signal (a red check) rather than on a request. That is exactly where permissions, who can trigger it, and a human review of the result need to be settled.

---

**Next:** [Demo 2: Review a Pull Request With a Skill](demo-2-review-a-pull-request-with-a-skill.md)


*Demo 1 of 9*
