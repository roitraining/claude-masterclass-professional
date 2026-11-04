# Claude Agent SDK Professional: Labs

**Course:** Claude Agent SDK Professional: Building and Evaluating Production Agents (Claude MasterClass Professional, Course 3)
**Contents:** Four timed hands-on labs and a take-home capstone. The numbers match the Today's Labs slide.

---

## About this guide

<!-- setup-ref:start -->
> **Setting up for the first time?** See **[Setup: Install and Sign In to Claude Code](../../SETUP-CLAUDE-CODE.md)** before Lab 1. Courses can be taken in any order, so none of them assumes another course installed it.
<!-- setup-ref:end -->
These are 300-level labs. Each states a goal, acceptance criteria and hints, and does not give click-by-click steps. Each plants a trap, and each is scored. You work solo and locally, in Python or TypeScript. Pick a language on Day 1 and keep it. Python is the primary starter and is complete. The TypeScript starter has the same structure and file purposes.

In this guide `$FILES` is the `demo-files` folder your instructor gives you. Work in your own copy. Everything is local and every name, order and amount is fictional. The labs do not re-teach Associate content: subagent team design and hooks basics are assumed.

**Credentials.** Set `ANTHROPIC_API_KEY` as an environment variable in the shell where you run the agent (see `$FILES/README.md`). Never put it in a file or a prompt. Use API-key authentication only.

**Cost and limits.** Every run is a model call and spends credits from your class key. The starters set a turn limit and a spend limit on every agent run (12 turns and a per-run spend cap by default). Do not remove them. Your instructor may change the defaults through `LAB_MAX_TURNS` and `LAB_BUDGET_USD`.

**Scoring.** Each lab is scored out of 100. Bands: 90 and above is Gold, 75 to 89 is Silver, 60 to 74 is Bronze. The instructor reviews your files and your written notes against the rubric. Model output varies between runs, so check your result against the acceptance criteria and not against exact text.

**Before Lab 1:** `python3 preflight.py` (or `npx tsx src/preflight.ts`) prints `Ready.` in `$FILES/python` or `$FILES/typescript`.

**Run commands from the language folder.** Python: `cd $FILES/python`. TypeScript: `cd $FILES/typescript`.

---

## The labs

- **[Lab 1: Build and Tune Your First Agent](lab-1-build-and-tune-your-first-agent.md)**
- **[Lab 2: Add a Custom MCP Server](lab-2-add-a-custom-mcp-server.md)**
- **[Lab 3: Multi-Step Agent With a Subagent](lab-3-multi-step-agent-with-a-subagent.md)**
- **[Lab 4: Build an Evaluation Harness](lab-4-build-an-evaluation-harness.md)**
- **[Lab 5 (take-home): Capstone](lab-5-capstone.md)**

---

## Related

- **[Demos guide](../demos/README.md)** — the 8 instructor-led demos for this course, one file per demo.
- **[Combined demos guide](../demos.md)** — all demos in a single document.
