// Lab 3: a plan-delegate-incorporate agent with one subagent, plus the runaway loop fixture.
//   npx tsx src/lab3Agent.ts digest
//   npx tsx src/lab3Agent.ts loop
// Your tasks are marked TODO.
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { BUILTIN_TOOLS, makeOptions, printRecord, requireApiKey, runTask, spawns } from "./agentCore.js";
import * as loop from "./loopFixture.js";
import * as tools from "./tools.js"; // use your fixed Lab 1 tools here

export const TASKS = JSON.parse(readFileSync(fileURLToPath(new URL("../../tasks/lab3_tasks.json", import.meta.url)), "utf-8"));

// TODO 1: write the parent's plan-delegate-incorporate instructions.
//   Say: plan first, fetch the data with tools, delegate the eligibility and refund arithmetic to the subagent
//   (pass it everything it needs in the Agent tool's prompt, because it starts with a fresh context window),
//   then check and incorporate its result into the final digest.
const DIGEST_SYSTEM_PROMPT =
  "You are the returns-desk agent for Brightwater Outfitters, a fictional outdoor retailer. " +
  "Today's date is 2026-10-19. Use the tools to answer.";

// TODO 2: define the subagent. A weak description means the parent may never delegate.
const RETURNS_ANALYST = {
  description: "Helper.",
  prompt: "Help with the task you are given.",
  // tools: [...],
  // maxTurns: ...,
};

// TODO 3: set the limits you will defend. These two numbers are deliberately wrong for the task.
export const MAX_TURNS = 3;
export const BUDGET_USD = 5.0;
// TODO 4: choose depth and concurrency limits for subagents. Both are passed as environment variables.
const SUBAGENT_DEPTH: string | null = null; // example: "1"
const SUBAGENT_CONCURRENCY: string | null = null; // example: "2"

function subagentEnv() {
  const env: Record<string, string> = {};
  if (SUBAGENT_DEPTH !== null) env.CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH = SUBAGENT_DEPTH;
  if (SUBAGENT_CONCURRENCY !== null) env.CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS = SUBAGENT_CONCURRENCY;
  return Object.keys(env).length ? env : undefined;
}

export function buildOptions(mode: "digest" | "loop" = "digest"): any {
  // Agent must be available, so built-ins are not emptied. Remove the file, shell and web tools by name instead.
  if (mode === "loop") {
    return makeOptions({
      systemPrompt: loop.LOOP_SYSTEM_PROMPT,
      mcpServers: { dock: loop.SERVER },
      allowedTools: [...loop.ALLOWED, "Agent"],
      disallowedTools: BUILTIN_TOOLS,
      tools: null,
      agents: { "manifest-watcher": loop.LOOP_SUBAGENT },
      env: subagentEnv(),
      maxTurns: MAX_TURNS,
      maxBudgetUsd: BUDGET_USD,
    });
  }
  return makeOptions({
    systemPrompt: DIGEST_SYSTEM_PROMPT,
    mcpServers: { shop: tools.SERVER },
    allowedTools: [...tools.ALLOWED, "Agent"],
    disallowedTools: BUILTIN_TOOLS,
    tools: null,
    agents: { "returns-analyst": RETURNS_ANALYST },
    env: subagentEnv(),
    maxTurns: MAX_TURNS,
    maxBudgetUsd: BUDGET_USD,
  });
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const mode = process.argv[2];
  if (mode !== "digest" && mode !== "loop") throw new Error("usage: lab3Agent.ts digest|loop");
  requireApiKey();
  const rec = await runTask(TASKS[mode].prompt, buildOptions(mode));
  printRecord(rec);
  console.log(`subagent spawns: ${spawns(rec).length}`);
  if (mode === "loop") console.log(`check_manifest calls: ${loop.CALLS.n}`);
}
