// Score Lab 3: the digest task and the runaway loop, against the limits you set in lab3Agent.ts.
//   npx tsx src/lab3Check.ts
// Two model runs. Each carries the turn and spend limits from lab3Agent.ts.
import { printRecord, requireApiKey, runTask, spawns } from "./agentCore.js";
import * as lab3 from "./lab3Agent.js";
import * as loop from "./loopFixture.js";

requireApiKey();
const HEADROOM = 1.5; // the spend cap is a client-side estimate and can overshoot, so allow headroom
const results: [string, boolean, string][] = [];

const d = lab3.TASKS.digest;
const rec = await runTask(d.prompt, lab3.buildOptions("digest"));
printRecord(rec);
results.push(["digest: finished with success", rec.subtype === "success", rec.subtype]);
results.push(["digest: delegated to the subagent (Agent tool_use)", spawns(rec).length > 0, `${spawns(rec).length} spawn(s)`]);
results.push(["digest: total refund 403 in the final answer", d.must_contain_all.every((s: string) => rec.finalText.includes(s)), "looked for '403'"]);
results.push(["digest: cost within budget plus headroom", (rec.costUsd ?? 0) <= lab3.BUDGET_USD * HEADROOM, `${rec.costUsd}`]);

const lp = lab3.TASKS.loop;
loop.CALLS.n = 0;
const rec2 = await runTask(lp.prompt, lab3.buildOptions("loop"));
printRecord(rec2);
const stopped = lp.pass_if_subtype_in.includes(rec2.subtype);
const honest = rec2.subtype === "success" && lp.or_pass_if_success_and_final_text_contains_any.some((s: string) => rec2.finalText.toLowerCase().includes(s));
results.push(["loop: stopped by a cap or reported honestly", stopped || honest, rec2.subtype]);
results.push(["loop: check_manifest calls within bound", loop.CALLS.n <= lp.max_check_manifest_calls, `${loop.CALLS.n} call(s)`]);
results.push(["loop: cost within budget plus headroom", (rec2.costUsd ?? 0) <= lab3.BUDGET_USD * HEADROOM, `${rec2.costUsd}`]);

console.log("\n=== Lab 3 checks ===");
for (const [label, ok, detail] of results) console.log(`[${ok ? "PASS" : "FAIL"}] ${label}  (${detail})`);
console.log(`${results.filter((r) => r[1]).length}/${results.length} checks passed`);
