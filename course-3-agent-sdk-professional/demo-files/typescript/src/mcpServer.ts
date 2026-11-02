// Lab 2 server template: a standalone MCP server over stdio for Brightwater order notes.
// The agent starts this file as a child process and talks to it over stdin and stdout.
// Rules for a stdio server:
//   - Never write to stdout (no console.log). Stdout carries the protocol. Use console.error for logs.
//   - Keep every tool description specific: what it does, its input format, and when not to use it.
// Install: npm install @modelcontextprotocol/server zod
// The import paths below follow the library README at the time of writing. Check the README for your installed version.
// Your tasks are marked TODO.
import { appendFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { McpServer } from "@modelcontextprotocol/server";
import { StdioServerTransport } from "@modelcontextprotocol/server/stdio";
import * as z from "zod/v4";
import * as shop from "./shopData.js";

const REFUND_LOG = fileURLToPath(new URL("./refund_log.jsonl", import.meta.url));
const server = new McpServer({ name: "shopdesk", version: "1.0.0" });

server.registerTool(
  "get_order_notes",
  {
    description: "TODO: replace this line with a specific description.",
    inputSchema: z.object({ order_id: z.string() }), // TODO: describe the field and its format
  },
  async ({ order_id }) => {
    // TODO: use shop.getNotes(order_id).
    //   - Unknown order id: return a short, clear message (not a stack trace).
    //   - No notes: say so.
    //   - Otherwise return the notes as plain text, one per line.
    throw new Error("Lab 2: implement get_order_notes");
  },
);

server.registerTool(
  "issue_refund",
  {
    description: "Issue a refund for an order. Fake: appends a line to refund_log.jsonl next to this file and moves no money.",
    inputSchema: z.object({ order_id: z.string(), amount: z.number(), reason: z.string() }),
  },
  async ({ order_id, amount, reason }) => {
    appendFileSync(REFUND_LOG, JSON.stringify({ at: new Date().toISOString(), order_id, amount, reason }) + "\n");
    console.error(`refund recorded for ${order_id}`);
    return { content: [{ type: "text", text: `Refund of ${amount.toFixed(2)} recorded for ${order_id}.` }] };
  },
);

await server.connect(new StdioServerTransport());
