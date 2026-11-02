// Lab 2: the Lab 1 agent plus the standalone MCP server.
//   npx tsx src/lab2Agent.ts "What do the notes on order BW-1002 say?"
import { fileURLToPath } from "node:url";
import { makeOptions, printRecord, requireApiKey, runTask } from "./agentCore.js";
import * as tools from "./tools.js";

// Keep your Lab 1 prompt and tool fixes.
export const SYSTEM_PROMPT =
  "You are the support assistant for Brightwater Outfitters, a fictional outdoor retailer. " +
  "Today's date is 2026-10-19. Use the tools to look up facts about orders, customers, policies and order notes. " +
  "Be concise.";

const serverPath = fileURLToPath(new URL("./mcpServer.ts", import.meta.url));
export const SHOPDESK_SERVER = { command: "npx", args: ["tsx", serverPath] };

export function buildOptions(systemPrompt: string = SYSTEM_PROMPT): any {
  return makeOptions({
    systemPrompt,
    mcpServers: { shop: tools.SERVER, shopdesk: SHOPDESK_SERVER },
    // Auto-approve the in-process tools and the notes server's tools.
    allowedTools: [...tools.ALLOWED, "mcp__shopdesk__*"],
  });
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  requireApiKey();
  const prompt = process.argv.slice(2).join(" ") || "What do the notes on order BW-1002 say?";
  const rec = await runTask(prompt, buildOptions());
  console.log("MCP servers at init:", JSON.stringify(rec.mcpStatus));
  printRecord(rec);
}
