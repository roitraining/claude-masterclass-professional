// Lab 1: the support agent. Run one prompt:  npx tsx src/lab1Agent.ts "Where is order BW-1003?"
import { fileURLToPath } from "node:url";
import { makeOptions, printRecord, requireApiKey, runTask } from "./agentCore.js";
import * as tools from "./tools.js";

export const SYSTEM_PROMPT =
  "You are the support assistant for Brightwater Outfitters, a fictional outdoor retailer. " +
  "Today's date is 2026-10-19. Use the tools to look up facts about orders, customers and policies. " +
  "Be concise.";

export function buildOptions(systemPrompt: string = SYSTEM_PROMPT): any {
  return makeOptions({
    systemPrompt,
    mcpServers: { shop: tools.SERVER },
    allowedTools: tools.ALLOWED,
  });
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  requireApiKey();
  const prompt = process.argv.slice(2).join(" ") || "Where is order BW-1003?";
  printRecord(await runTask(prompt, buildOptions()));
}
