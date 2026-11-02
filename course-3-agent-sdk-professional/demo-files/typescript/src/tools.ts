// Lab 1 starter: three custom tools wrapped in an in-process MCP server.
// The tools work. The agent still uses them badly. Find out why, then fix it.
// You may change anything in this file except the data behind it (shopData.ts).
import { createSdkMcpServer, tool } from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";
import * as shop from "./shopData.js";

const text = (payload: unknown, isError = false) => ({
  content: [{ type: "text" as const, text: typeof payload === "string" ? payload : JSON.stringify(payload) }],
  ...(isError ? { isError: true } : {}),
});

export const orderLookup = tool("order_lookup", "Look up information.", { id: z.string() }, async (args) => {
  const rec = shop.getOrder(args.id);
  return rec ? text(rec) : text(`No order found for id '${args.id}'. Order ids look like BW-1001.`, true);
});

export const customerLookup = tool("customer_lookup", "Look up information about a person or an order.", { id: z.string() }, async (args) => {
  const rec = shop.getCustomer(args.id);
  return rec ? text(rec) : text(`No customer found for id '${args.id}'.`, true);
});

export const policyLookup = tool("policy_lookup", "Get details about anything the customer asks.", { topic: z.string() }, async (args) => {
  const t = shop.getPolicy(args.topic);
  return t ? text(t) : text(`Unknown topic '${args.topic}'.`, true);
});

export const SERVER = createSdkMcpServer({ name: "shop", version: "1.0.0", tools: [orderLookup, customerLookup, policyLookup] });

// Tools are allowed by full name: mcp__{server}__{tool}.
export const ALLOWED = ["mcp__shop__order_lookup", "mcp__shop__customer_lookup", "mcp__shop__policy_lookup"];
