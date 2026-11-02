// Demo 1: the minimal agent. Prints every message so the loop is visible.
//   npx tsx src/demo1Minimal.ts
import { fileURLToPath } from "node:url";
import { query } from "@anthropic-ai/claude-agent-sdk";
import { requireApiKey } from "./agentCore.js";

requireApiKey();
const dataDir = fileURLToPath(new URL("../../data/", import.meta.url));

for await (const m of query({
  prompt: "Read sample_notes.md and list its three action items, one per line.",
  options: {
    systemPrompt: "You are a concise assistant.",
    tools: ["Read"], // the only built-in tool that exists for this agent
    allowedTools: ["Read"], // auto-approve it
    settingSources: [], // ignore settings files on this machine
    cwd: dataDir,
    maxTurns: 4,
    maxBudgetUsd: 0.25,
  },
}) as AsyncIterable<any>) {
  if (m.type === "system") console.log(`[system] subtype=${m.subtype}`);
  else if (m.type === "assistant") {
    for (const b of m.message?.content ?? []) {
      if (b.type === "text") console.log(`[assistant text] ${b.text.trim()}`);
      else if (b.type === "tool_use") console.log(`[assistant tool_use] ${b.name} ${JSON.stringify(b.input)}`);
    }
  } else if (m.type === "user") console.log("[tool_result]");
  else if (m.type === "result") {
    console.log(`[result] subtype=${m.subtype} turns=${m.num_turns} cost_usd=${m.total_cost_usd}`);
    console.log(m.result);
  }
}
