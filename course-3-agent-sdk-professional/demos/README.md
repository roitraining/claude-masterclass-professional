# Claude Agent SDK Professional: Demos

**Course:** Claude Agent SDK Professional: Building and Evaluating Production Agents (Claude MasterClass Professional, Course 3)
**Contents:** 8 instructor-led demos. Each takes 15 minutes or less and has a learning objective. The numbers match the Today's Demos slide.

---

## About this guide

Run the demos in order. Each has the same layout: a learning objective, a time, a Files line when it uses files, a short context paragraph, steps, an Expected result, an Instructor note, and a Why this matters note.

This is a 300-level course. The demos assume Associate-level habits and do not re-teach subagent team design, hooks basics, or the Claude Code interface.

In this guide `$FILES` means the `demo-files` folder. Python is the primary language and every demo runs in Python. Demo 1 also has a TypeScript version. For Demos 2 to 6, the instructor shows Python and points to the matching TypeScript file structure in the labs.

- [`$FILES/python`](../demo-files/python): agent core and demo scripts (`demo1_minimal.py` to `demo8_scorecard.py`).
- [`$FILES/typescript`](../demo-files/typescript): the TypeScript starter (`src/demo1Minimal.ts`).
- [`$FILES/retrieval`](../demo-files/retrieval): the local retrieval MCP server and its documents (Demo 4, Demo 5).
- [`$FILES/recorded`](../demo-files/recorded): recorded runs for the offline Demos 7 and 8.
- [`$FILES/data`](../demo-files/data): fictional shop data and a sample note.

Every person, company, order and amount is fictional. Agent output varies from run to run, so check results against the Expected result and not against exact text.

> **Credentials.** Set `ANTHROPIC_API_KEY` as an environment variable in the shell where you run the demo (see [`$FILES/README.md`](../demo-files/README.md)). Never put it in a file or on a slide. API-key authentication only. claude.ai login is not used.

> **Cost.** Demos 1 to 6 make live model calls. Every script sets a turn limit and a spend limit. Demos 7 and 8 run offline from recorded data. Each live demo lists a recorded-transcript fallback in its Instructor note, so a network or key problem never stops the session.

---

## Setup: Install and check once

**Time:** about 5 minutes, before Demo 1.

1. Python:

```
cd $FILES/python
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python3 preflight.py
```

On Windows PowerShell use `py -m venv .venv` and `.venv\Scripts\Activate.ps1`.

2. TypeScript, for the Demo 1 comparison:

```
cd $FILES/typescript
npm install @anthropic-ai/claude-agent-sdk zod @modelcontextprotocol/server
npm install --save-dev tsx
npx tsx src/preflight.ts
```

**Expected result:** every line of `preflight.py` reads `[ok]`. The check never prints the key.

> **Instructor note:** The Python package is `claude-agent-sdk` and the TypeScript package is `@anthropic-ai/claude-agent-sdk`. Both bundle a native Claude Code binary on most platforms. An install that skips optional dependencies, or a platform with no wheel, needs a native Claude Code install; rehearse on the class image. Python needs 3.10 or later and Node.js 18 or later. The MCP server library (`mcp[cli]` for Python, `@modelcontextprotocol/server` for TypeScript) is **UNVERIFIED** against the class image: its module layout has changed between releases. The server scripts import with a fallback, and the exact `run()` call may need a one-line change. Pin versions after rehearsal.

---

## The demos

- **[Demo 1: Run the Minimal Agent](demo-1-run-the-minimal-agent.md)**
- **[Demo 2: A Tool the Agent Misuses](demo-2-a-tool-the-agent-misuses.md)**
- **[Demo 3: Build a Standalone MCP Server](demo-3-build-a-standalone-mcp-server.md)**
- **[Demo 4: Retrieval Through an MCP Server](demo-4-retrieval-through-an-mcp-server.md)**
- **[Demo 5: Delegate to a Subagent](demo-5-delegate-to-a-subagent.md)**
- **[Demo 6: Cap Turns, Depth, and Spend](demo-6-cap-turns-depth-and-spend.md)**
- **[Demo 7: Grade a Run With Code and a Judge](demo-7-grade-a-run-with-code-and-a-judge.md)**
- **[Demo 8: What a Passing Score Misses](demo-8-what-a-passing-score-misses.md)**

---

The combined guide remains at [`../demos.md`](../demos.md) and is still the source of record. These per-demo files are split out of it for easier reading and review.

---

## Related

- **[Labs guide](../labs/README.md)** — the 5 hands-on labs for this course, one file per lab.
