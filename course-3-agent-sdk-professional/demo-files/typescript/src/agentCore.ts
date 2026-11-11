// Shared plumbing for every lab: build options, run a task, record what happened.
// The SDK reads ANTHROPIC_API_KEY from the environment of the process. Never put a key in a file.
import { query } from "@anthropic-ai/claude-agent-sdk";

export const IGNORED_TOOLS = new Set(["ToolSearch"]);
// The subagent tool is "Agent" in tool_use blocks and "Task" in older versions.
export const SUBAGENT_TOOLS = new Set(["Agent", "Task"]);
// With Agent available, remove file, shell and web tools by name. A bare name in disallowedTools removes the tool.
// SendMessage is a built-in that can resume a stopped subagent. This list is
// passed as disallowedTools in Lab 3, so omitting it broke the turn bound.
export const BUILTIN_TOOLS = ["Bash", "Read", "Write", "Edit", "Glob", "Grep",
  "WebFetch", "WebSearch", "NotebookEdit", "SendMessage"];

export type ToolCall = { name: string; input: any; toolUseId: string; inSubagent: boolean; resultText: string; isError: boolean };
export type RunRecord = {
  prompt: string;
  finalText: string;
  subtype: string;
  numTurns: number;
  costUsd: number | null;
  toolCalls: ToolCall[];
  assistantText: string[];
  mcpStatus: any[];
  error: string | null;
};

export function requireApiKey(): void {
  if (!process.env.ANTHROPIC_API_KEY) {
    throw new Error("ANTHROPIC_API_KEY is not set. Set it as an environment variable in this shell (see README.md). Do not put the key in a file.");
  }
}

export const shortName = (name: string) => (name.startsWith("mcp__") ? name.split("__").pop()! : name);
export const usedTools = (rec: RunRecord) =>
  rec.toolCalls.filter((c) => !IGNORED_TOOLS.has(c.name) && !SUBAGENT_TOOLS.has(c.name)).map((c) => shortName(c.name));
export const spawns = (rec: RunRecord) => rec.toolCalls.filter((c) => SUBAGENT_TOOLS.has(c.name));
export const allText = (rec: RunRecord) => [rec.finalText, ...rec.assistantText].join("\n");

export type MakeOptionsArgs = {
  systemPrompt: string;
  mcpServers?: Record<string, any>;
  allowedTools?: string[];
  disallowedTools?: string[];
  tools?: string[] | undefined | null; // omit for no built-ins; null for the default built-ins
  agents?: Record<string, any>;
  env?: Record<string, string | undefined>;
  maxTurns?: number;
  maxBudgetUsd?: number;
};

// Defaults: no built-in tools, no filesystem settings, and hard limits.
// Limits come from LAB_MAX_TURNS and LAB_BUDGET_USD when set, else 12 turns and 0.50 USD.
// Set AGENT_MODEL to choose a model. Leave it unset to use the default.
export function makeOptions(a: MakeOptionsArgs): any {
  const opts: any = {
    systemPrompt: a.systemPrompt,
    tools: a.tools === undefined ? [] : a.tools === null ? undefined : a.tools,
    settingSources: [],
    mcpServers: a.mcpServers ?? {},
    allowedTools: a.allowedTools ?? [],
    disallowedTools: a.disallowedTools ?? [],
    maxTurns: a.maxTurns ?? Number(process.env.LAB_MAX_TURNS ?? "12"),
    maxBudgetUsd: a.maxBudgetUsd ?? Number(process.env.LAB_BUDGET_USD ?? "0.50"),
  };
  if (a.agents) opts.agents = a.agents;
  if (a.env) opts.env = a.env; // the TypeScript SDK REPLACES the subprocess environment with this
  if (process.env.AGENT_MODEL) opts.model = process.env.AGENT_MODEL;
  return opts;
}

const flatten = (content: any): string =>
  typeof content === "string" ? content : Array.isArray(content) ? content.map((p) => p?.text ?? "").join("\n") : "";

export async function runTask(prompt: string, options: any): Promise<RunRecord> {
  const rec: RunRecord = { prompt, finalText: "", subtype: "not_run", numTurns: 0, costUsd: null, toolCalls: [], assistantText: [], mcpStatus: [], error: null };
  const byId = new Map<string, ToolCall>();
  try {
    for await (const m of query({ prompt, options }) as AsyncIterable<any>) {
      if (m.type === "system" && m.subtype === "init") {
        rec.mcpStatus = m.mcp_servers ?? [];
      } else if (m.type === "assistant") {
        const inSub = Boolean(m.parent_tool_use_id);
        for (const b of m.message?.content ?? []) {
          if (b.type === "text" && !inSub) rec.assistantText.push(b.text);
          else if (b.type === "tool_use") {
            const call: ToolCall = { name: b.name, input: b.input ?? {}, toolUseId: b.id, inSubagent: inSub, resultText: "", isError: false };
            byId.set(b.id, call);
            rec.toolCalls.push(call);
          }
        }
      } else if (m.type === "user" && Array.isArray(m.message?.content)) {
        for (const b of m.message.content) {
          if (b.type === "tool_result" && byId.has(b.tool_use_id)) {
            const call = byId.get(b.tool_use_id)!;
            call.resultText = flatten(b.content);
            call.isError = Boolean(b.is_error);
          }
        }
      } else if (m.type === "result") {
        rec.subtype = m.subtype;
        rec.finalText = m.result ?? "";
        rec.numTurns = m.num_turns ?? 0;
        rec.costUsd = m.total_cost_usd ?? null;
      }
    }
  } catch (err: any) {
    // A single-shot query() throws after yielding an error result.
    rec.error = `${err?.name ?? "Error"}: ${err?.message ?? err}`;
  }
  return rec;
}

export function printRecord(rec: RunRecord): void {
  console.log(`\nPROMPT: ${rec.prompt}`);
  for (const c of rec.toolCalls) {
    console.log(`  TOOL ${c.name}${c.inSubagent ? " (inside subagent)" : ""} input=${JSON.stringify(c.input)}`);
    if (c.resultText) console.log(`       result${c.isError ? " [error]" : ""}: ${c.resultText.replace(/\n/g, " ").slice(0, 160)}`);
  }
  console.log(`ANSWER: ${rec.finalText.trim()}`);
  console.log(`RESULT: subtype=${rec.subtype} turns=${rec.numTurns} cost_usd=${rec.costUsd ?? "n/a"}`);
  if (rec.error) console.log(`ERROR: ${rec.error}`);
}
