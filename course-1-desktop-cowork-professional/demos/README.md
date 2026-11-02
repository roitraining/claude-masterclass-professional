# Claude Desktop Professional: Demos

**Course:** Claude Desktop Professional, Plugin and Extension Engineering (Claude MasterClass Professional, Course 1)
**Contents:** 8 instructor-led demos. Each takes 15 minutes or less and has a learning objective. The numbers and titles match the Today's Demos slide.

---

## About this guide

Run the demos in order. Each has the same layout: a learning objective, a time, a Files line when it uses files, a short context paragraph, steps, an Expected result, an Instructor note, and a Why this matters note.

These demos assume Associate 1 and Associate 2. They do not re-teach what a Skill is, how to install a plugin, or how to schedule a task. Demos 1 to 3 build a small plugin, `records-desk`, live. The students then build their own in Lab 1.

Everything runs locally on your own machine. Demos 5 and 7 mention steps that publish or install from a shared marketplace or upload to an organization. Those are instructor-only, on the ROI sandbox account, and every one is marked below. Every person, company, and figure in the files is fictional, and no file contains a real credential. Claude can word things differently each time, so check results against the Expected result and not against exact text.

**Files.** In this guide `$FILES` means the `demo-files` folder your instructor gives you:

- [`$FILES/demo-snippets`](../demo-files/demo-snippets) holds the skill, command, agents, and `.mcp.json` for the `records-desk` plugin, for Demos 1 to 3.
- [`$FILES/starter-server`](../demo-files/starter-server) is a small local MCP server in Python with sample records, for Demos 2, 3, and 5.
- [`$FILES/autopsy-plugin`](../demo-files/autopsy-plugin) is a flawed plugin, for Demo 4 and Demo 8.
- [`$FILES/gauntlet`](../demo-files/gauntlet) holds the runner, the eval suites, and the sample reports, for Demos 4 and 6.
- [`$FILES/untrusted-plugin`](../demo-files/untrusted-plugin) is a fictional third-party plugin to review, for Demo 7.

> **Shell.** Commands are written for bash (macOS, Linux, or Git Bash on Windows). In PowerShell use `New-Item -ItemType Directory` for `mkdir -p` and `Copy-Item -Recurse` for `cp -r`. Use `python` on Windows and `python3` where `python` is not defined.

> **Rehearse once on the class machine.** The Claude Code commands below were run while building this guide, except where an Instructor note says otherwise. Paid eval runs and the Desktop extension install were not run. Do both before the day.

> **Model credits.** Only Demo 4 spends model credits for evals. Cap it as shown.

---

## Setup: Make a work folder once

**Time:** about 5 minutes, before Demo 1.

1. Create a work folder and check the tools:

```
mkdir -p ~/work && cd ~/work
claude --version
python --version
git --version
```

**Expected result:** Claude Code 2.1.269 or later (plugin evals need it), Python 3.11 or later, Git 2.31 or later.

> **Instructor note:** `claude` must be signed in for Demo 4. In the build environment for this guide `claude plugin eval` stopped with "Not logged in", so sign in on the class machine and run Demo 4 once beforehand.

---

## The demos

- **[Demo 1: Scaffold a Plugin and Load It](demo-1-scaffold-a-plugin-and-load-it.md)**
- **[Demo 2: Add Components, Then Validate](demo-2-add-components-then-validate.md)**
- **[Demo 3: Add a Sub-Agent and a Slash Command](demo-3-add-a-sub-agent-and-a-slash-command.md)**
- **[Demo 4: Cold-Install a Setup Guide](demo-4-cold-install-a-setup-guide.md)**
- **[Demo 5: Package a Server as an Extension](demo-5-package-a-server-as-an-extension.md)**
- **[Demo 6: Read a Worked Gauntlet Report](demo-6-read-a-worked-gauntlet-report.md)**
- **[Demo 7: Review a Plugin Before You Trust It](demo-7-review-a-plugin-before-you-trust-it.md)**
- **[Demo 8: Read a Plugin's Cost and Usage](demo-8-read-a-plugin-s-cost-and-usage.md)**

---

The combined guide remains at [`../demos.md`](../demos.md) and is still the source of record. These per-demo files are split out of it for easier reading and review.

---

## Related

- **[Labs guide](../labs/README.md)** — the 3 hands-on labs for this course, one file per lab.
