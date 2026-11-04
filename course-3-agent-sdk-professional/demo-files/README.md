# Demo files: Claude Agent SDK Professional

Everything here is fictional: Brightwater Outfitters, its customers, orders, notes and documents. The `.test` email domain is reserved and never resolves. Nothing needs a cloud account. Every file is plain text, Python, TypeScript, JSON or Markdown.

## Layout

| Folder | Holds |
|---|---|
| `data/` | The fake backend (`shop.json`), the Lab 2 injection fixture (`order_notes.json`), and a sample meeting note for Demo 1 |
| `tasks/` | Answer keys and fixtures: `lab1_prompts.json`, `lab2_prompts.json`, `lab3_tasks.json`, `golden_tasks.json`, `judge_rubric.json`, `success_criteria_template.md` |
| `prompts/` | System prompt variants A and B, and a CSV of test cases for the Console prompt comparison |
| `python/` | Primary starter, complete. Agent core, Lab 1 to 4 starters, MCP server template, harness skeleton, demo scripts |
| `python/facilitator/` | Solutions to copy over starter files. Instructors only |
| `typescript/` | Parallel starter with the same structure and file purposes (camelCase names) |
| `retrieval/` | Local stand-in retrieval MCP server and nine fictional documents (Day 1 Module 7, Demo 4) |
| `recorded/` | Recorded runs for the offline Demos 7 and 8 |
| `capstone/` | One-page release note template for the take-home lab |

## Set the API key (environment variable only)

The SDK reads `ANTHROPIC_API_KEY` from the environment of the process. It does not read `.env` files. Never put the key in a file, a prompt or a commit.

macOS or Linux:

```
export ANTHROPIC_API_KEY="<the key your instructor issued>"
```

Windows PowerShell:

```
$env:ANTHROPIC_API_KEY = "<the key your instructor issued>"
```

Use API-key authentication only. claude.ai login is not used in this course.

## Python setup

```
cd python
python3 -m venv .venv && . .venv/bin/activate          # Windows: py -m venv .venv ; .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python3 preflight.py
```

## TypeScript setup

```
cd typescript
npm install @anthropic-ai/claude-agent-sdk zod @modelcontextprotocol/server
npm install --save-dev tsx
npx tsx src/preflight.ts
```

## Limits that apply to every run

`agent_core.make_options` (and `makeOptions` in TypeScript) sets no built-in tools, ignores filesystem settings, and applies a turn limit and a spend limit to every agent run. Defaults are 12 turns and 0.50 USD. Your instructor may change them through the `LAB_MAX_TURNS` and `LAB_BUDGET_USD` environment variables. Set `AGENT_MODEL` to choose a model and `JUDGE_MODEL` to choose a different one for the Lab 4 judge. Leave them unset to use the default.

## Version note for the instructor

Packages are unpinned. Rehearse on the class image, then pin the Agent SDK, the MCP server library and zod in `requirements.txt` and in a `package.json` dependencies block. The MCP server library layout has changed between releases, so the servers import with a fallback. See each guide's Instructor notes.
