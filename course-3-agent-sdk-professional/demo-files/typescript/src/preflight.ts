// Preflight: confirms the environment is ready. Makes no model call and never prints the key.
//   npx tsx src/preflight.ts
import { existsSync } from "node:fs";
import { fileURLToPath } from "node:url";

let ok = true;
const check = (label: string, passed: boolean, fix = "") => {
  ok = ok && passed;
  console.log(`[${passed ? "ok" : "FAIL"}] ${label}${passed ? "" : `  -> ${fix}`}`);
};

check("Node.js 18 or later", Number(process.versions.node.split(".")[0]) >= 18, "install a newer Node.js");
check("ANTHROPIC_API_KEY is set (value not shown)", Boolean(process.env.ANTHROPIC_API_KEY), "set it as an environment variable in this shell; never put it in a file");
for (const [mod, fix] of [["@anthropic-ai/claude-agent-sdk", "npm install @anthropic-ai/claude-agent-sdk"], ["zod", "npm install zod"]] as const) {
  try { await import(mod); check(`import ${mod}`, true); } catch { check(`import ${mod}`, false, fix); }
}
for (const rel of ["data/shop.json", "data/order_notes.json", "tasks/golden_tasks.json"]) {
  check(`found ${rel}`, existsSync(fileURLToPath(new URL(`../../${rel}`, import.meta.url))), "the demo-files folder is incomplete");
}
console.log(ok ? "\nReady." : "\nFix the items marked FAIL, then run this again.");
process.exit(ok ? 0 : 1);
