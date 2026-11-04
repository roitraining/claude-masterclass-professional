# Claude Desktop Professional: Labs

**Course:** Claude Desktop Professional, Plugin and Extension Engineering (Claude MasterClass Professional, Course 1)
**Contents:** Two timed hands-on labs and a take-home lab. The numbers match the Today's Labs slide.

---

## About this guide

<!-- setup-ref:start -->
> **Setting up for the first time?** See **[Setup: Install and Sign In to Claude Code](../../SETUP-CLAUDE-CODE.md)** before Lab 1. Courses can be taken in any order, so none of them assumes another course installed it.
<!-- setup-ref:end -->
You run these labs yourself, solo, on your own machine, in the order below. They assume Associate 1 and Associate 2: what a Skill is, how to install a plugin, and how to schedule a task are not retaught. This is a Professional course, so the steps state a goal and the acceptance criteria and give hints. How you get there is yours to work out.

In this guide `$FILES` is the `demo-files` folder your instructor gives you. Everything is local and uses fictional data. No lab needs a credential or a cloud account. Anything that publishes or uploads to a shared account is done by the instructor on the ROI sandbox account, not by you.

Claude can word things differently each time. Check your result against the Checkpoint, not against exact text.

**Before Lab 1:**

- Python 3.11 or later and Git 2.31 or later. Check with `python3 --version` and `git --version`.
- `claude` (Claude Code 2.1.269 or later). Check with `claude --version`.
- Node.js and the MCPB tool for packaging an extension: `npm install -g @anthropic-ai/mcpb`. If Node is not available, use `pack_mcpb.py` in the starter server instead.
- Claude Desktop, with plugins enabled, **signed in to the same account as Claude Code** — needed only for Lab 1 Part 8 (optional) and Lab 3 Part 5. A plugin is saved to an account, so a mismatch means the plugin you packed will not appear in Desktop. Everything else in this course is command line: without Desktop you can still complete Lab 1 Parts 1 to 7 and all of Lab 2.

> **Model credits.** Lab 2 Part 2 runs evals, which spend model credits. The Gauntlet script caps spend. Do not raise the cap without asking.

---

## The labs

- **[Lab 1: Build the Plugin](lab-1-build-the-plugin.md)**
- **[Lab 2: Autopsy, Then the Gauntlet](lab-2-autopsy-then-the-gauntlet.md)**
- **[Lab 3 (take-home): Submit and Distribute](lab-3-submit-and-distribute.md)**

---

## Related

- **[Demos guide](../demos/README.md)** — the 8 instructor-led demos for this course, one file per demo.
- **[Combined demos guide](../demos.md)** — all demos in a single document.
