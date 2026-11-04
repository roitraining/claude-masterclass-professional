# Claude Code Professional: Labs

**Course:** Claude Code Professional: Pipelines, Plugins and Enterprise Operations (Claude MasterClass Professional, Course 2)
**Contents:** Four timed hands-on labs and a take-home lab. The numbers match the Today's Labs slide.

---

## About this guide

<!-- setup-ref:start -->
> **Setting up for the first time?** See **[Setup: Install and Sign In to Claude Code](../../SETUP-CLAUDE-CODE.md)** before Lab 1. Courses can be taken in any order, so none of them assumes another course installed it.
<!-- setup-ref:end -->
These are 300-level labs. Each gives a goal, acceptance criteria and hints, not click-by-click steps. Each hides planted traps, and each is scored. The Associate course taught worktrees, subagent teams, hooks and policy precedence, so none of that is retaught here.

In this guide `$FILES` is the `demo-files` folder your instructor gives you. Everything runs on your own personal or sample GitHub or GitLab project plus local files. You do not depend on another student, and you do not need to share an organization with anyone. Use a project that holds no real work. Every name, company and figure is fictional. No file holds a real secret.

Claude Code can word things differently each time. Check your result against the acceptance criteria, not against exact text.

**Before Lab 1:** Python 3.11 or later, Git 2.31 or later with your name and email set, and `claude` signed in to a paid Anthropic account — the free plan does not include Claude Code. On Windows, run the shell commands in Git Bash.

**A hosted project is needed for Lab 1 only.** Lab 1 Tracks A and B need administrative access to a personal or sample GitHub or GitLab project, because they trigger a real CI run. Lab 1 **Track C** needs no remote and no API key. Labs 2, 3, 4 and 5 all work from local files: Lab 3 has a single optional step that publishes to a remote marketplace, and Lab 4 needs no remote at all. Do not skip those labs for want of a hosted project.

> **Token cost.** CI runs, review runs and plugin evals use API credits or subscription usage. Every lab says where to cap them. Use the caps.

> **Facilitators.** Instructor-only actions (anything in an organization, a tenant or a shared account) stay with the instructor. Students act only in their own project. Remove the `facilitator/` folders from `$FILES` before you share it.

---

## The labs

- **[Lab 1: Wire Claude into CI Safely](lab-1-wire-claude-into-ci-safely.md)**
- **[Lab 2: Tune and Score Code Review](lab-2-tune-and-score-code-review.md)**
- **[Lab 3: Build a Custom Plugin](lab-3-build-a-custom-plugin.md)**
- **[Lab 4: Build a Language Server Plugin](lab-4-build-a-language-server-plugin.md)**
- **[Lab 5 (take-home): Enterprise Migration Runbook](lab-5-enterprise-migration-runbook.md)**

---

## Related

- **[Demos guide](../demos/README.md)** — the 9 instructor-led demos for this course, one file per demo.
- **[Combined demos guide](../demos.md)** — all demos in a single document.
