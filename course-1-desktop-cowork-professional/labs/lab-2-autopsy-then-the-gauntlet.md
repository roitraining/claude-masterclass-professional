# Lab 2: Autopsy, Then the Gauntlet

> Part of **[Claude Desktop Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

**Learning objective:** Find and fix six planted defects in a flawed plugin, then run your own plugin through a scored Gauntlet and iterate toward Gold. Time: 65 minutes (Part 1: 25 minutes, Part 2: 40 minutes).

**Files:** `$FILES/autopsy-plugin`, `$FILES/AUTOPSY-WORKSHEET.md`, `$FILES/gauntlet` (`gauntlet.py`, `scorecard.md`, `SECURITY-CHECKLIST.md`, `adversarial/ADVERSARIAL-PACK.md`), `$FILES/templates`, and your plugin from Lab 1.

**Context:** The autopsy plugin passes `claude plugin validate` and has six defects that a validator does not catch. The Gauntlet is an automated scorecard out of 100 for your own plugin: an eval suite with a no-plugin baseline, a context-cost budget, a simulated cold install, an adversarial prompt pack, and a security checklist. Bronze is 60, Silver is 75, Gold is 90 with all the security points. Read `scorecard.md` before you start.

### Part 1: Plugin Autopsy (25 minutes)

**Steps:**

1. Copy the plugin to a work folder and open `AUTOPSY-WORKSHEET.md`:

```
cp -r $FILES/autopsy-plugin ~/work/expense-digest
```

2. Run the checks that tools can do, and record the always-on figure:

```
claude plugin validate ~/work/expense-digest
claude --plugin-dir ~/work/expense-digest plugin details expense-digest
```

3. Find the six defects, one in each area on the worksheet: trigger, permissions, setup, context cost, secrets, and versioning. For each, write down the file and the evidence before you fix it. Hint: read every file once, in the order Claude would meet them. A tool finds some of them. Your own reading finds the rest.
4. Fix each defect in your copy.
   - Acceptance, trigger: the main skill's description would make Claude choose it for an expense digest request and not for unrelated finance questions.
   - Acceptance, permissions: no agent has a tool it does not need, and the role that claims to be read-only cannot write, edit, run a shell, or fetch from the web.
   - Acceptance, setup: a new hire who follows `SETUP.md` alone reaches a working connector in Claude Code and knows what to expect in Cowork.
   - Acceptance, context cost: always-on tokens fall below 1,000, and the policy rules are still available to Claude.
   - Acceptance, secrets: no credential-like value is left in any file, and your fix says where a real value would live instead.
   - Acceptance, versioning: every place that carries a version shows the same one, and the changelog explains the change.
5. Re-check:

```
claude plugin validate ~/work/expense-digest
claude --plugin-dir ~/work/expense-digest plugin details expense-digest
python $FILES/gauntlet/gauntlet.py --plugin ~/work/expense-digest --product 1 --static-only --out ~/work/autopsy-check
```

**Checkpoint (Part 1):** Validation still passes, always-on tokens are under 1,000, and the free Gauntlet checks show full marks for the secret, tool-scoping, and release-hygiene lines. The structure lines fail because this plugin is not one of the four products. Ignore them.

**Common problems (Part 1):**

- You shortened the descriptions and now nothing is left to say when the rule skills apply. Merge the rule skills into a single skill that reads a short policy section, and keep one clear description.
- You removed the secret from `config.json` but the server still reads it. Fix the code too, or the server breaks.
- You updated the version in only some places. Search the whole folder for the old numbers.
- You added the data folder step to `SETUP.md` but not to the Cowork section. Cowork does not prompt for a setting that has no default.

**Scoring rubric (12 points):** 2 points for each defect: 1 for the evidence you recorded and 1 for a fix that meets its acceptance criterion.

### Part 2: The Gauntlet (40 minutes)

**Steps:**

1. **Free run first (5 minutes).** Run the free checks on your own plugin and read the notes column:

```
python $FILES/gauntlet/gauntlet.py --plugin ~/work/<plugin name> --static-only
```

2. **Write the release files (10 minutes).** Start from `$FILES/templates`. Goal, all of these:
   - `SETUP.md` with Prerequisites, Install, Configure, Verify (with an expected result), and Troubleshooting sections, and a line on what works in chat, Cowork, and Claude Code.
   - `CHANGELOG.md` with a first entry. The top version must match `plugin.json` and `server/manifest.json`. Repack the `.mcpb` if you change the manifest.
   - `SECURITY-REVIEW.md` only if you added hooks. Do not add a `bin/` folder.
3. **Smoke test (3 minutes).** Prove your set-up works with a single capped case:

```
python $FILES/gauntlet/gauntlet.py --plugin ~/work/<plugin name> --smoke
```

4. **First full run (about 10 minutes).** Run the whole Gauntlet once and read the report, notes first. The default caps spend at 5 dollars and uses 2 runs per case:

```
python $FILES/gauntlet/gauntlet.py --plugin ~/work/<plugin name> --out ~/work/gauntlet-run-1
```

5. **Iterate (about 10 minutes).** Rank your losses by points. Fix the largest first, then re-run only the affected group, for example `--only trig` or `--only adv`, which is cheaper than a full run. Re-check the free items with `--static-only` after every change. Cutting descriptions to save tokens can stop the skill firing, so re-run the trigger cases after each cut.
6. **Release package (2 minutes of the 40, finish at home if needed).** Run the whole Gauntlet a final time. Then assemble: the plugin folder, `CHANGELOG.md`, `RELEASE-NOTE.md` from the template with your Gauntlet score and tier, and a recorded 60-second self-demo following `SELF-DEMO-OUTLINE.md`.

Also run the adversarial prompts in `adversarial/ADVERSARIAL-PACK.md` by hand in a Cowork session if time allows. The automated eval exercises your plugin in Claude Code only.

**Checkpoint:** A Gauntlet report at Bronze or better, a changelog, a one-page release note with the score, and a recorded self-demo. Your target is Silver or Gold.

**Common problems (Part 2):**

- "Not rated": a group did not finish. Read the printed reason. `auth_failed` means Claude Code is not signed in for eval runs: run `claude` and sign in with `/login`. A cost-ceiling stop means you hit the cap.
- The structure score is low: a name differs from the brief. The script lists exactly what is missing.
- Quality cases fail on the conflict or the stale record: the evals use mock connector data, not your server. Your skill and agents must instruct Claude to report both values and to date every stale value. Do not rely on your server to do the judging.
- The injection case fails: the canary string leaked into the reply. Tell your skill and both agents that text in data is information, that anything resembling an instruction goes under `suspect_instructions`, and that Claude tells the user about it.
- The cold-install case reports a STUCK step: read the step. It is almost always a setting or a command your guide assumes the reader already has.
- No tier despite a high total: a secret was found, or you are at 90 or more but missing a security point (Gold needs all 10).
- A run is slow or rate-limited: lower `--concurrency`.

**Scoring rubric (18 points):**

| Item | Points | Full marks when |
|---|---|---|
| Gauntlet tier | 14 | Bronze 8, Silver 11, Gold 14 |
| Release note | 2 | One page, uses the template, score matches the report |
| Self-demo | 2 | About 60 seconds, shows a slash command, a data problem called out, and the report |

**Facilitator note:** The six planted defects in the autopsy plugin, and where each is:

1. **Vague trigger.** `skills/expense-digest/SKILL.md`, line 3: the description is "Helps with expense stuff and other finance things." Fix: say when to use it ("Summarizes an expense report by category and flags large items. Use when asked for an expense digest or a summary of expenses.").
2. **Over-broad tool permission.** `agents/policy-reviewer.md`, line 4: `tools: Read, Grep, Glob, Bash, Write, Edit, WebFetch` on an agent that says it is read-only. Fix: `tools: Read, Grep, Glob`. The Gauntlet's security check reports it.
3. **Missing setup step.** `SETUP.md` never says to set the data folder. `.mcp.json` line 7 passes `${user_config.data_dir}` to the server and `.claude-plugin/plugin.json` declares `userConfig.data_dir` with no default. The server raises an error when the variable is unset. Fix: a Configure section that tells the reader to set the data folder through `/plugin configure expense-digest` in Claude Code and says Cowork ignores the server until an option has a default and does not prompt. Better fix: give the option a default or read a bundled folder when it is empty.
4. **Bloated always-on cost.** About 2,050 tokens always-on. Cause: seven rule skills (`expense-policy`, `receipt-rules`, `mileage-rules`, `per-diem-rules`, `lodging-rules`, `gift-rules`, `approval-rules`) each with a 600 to 1,000 character "use for anything" description, a 1,500 character description on `agents/policy-reviewer.md`, and a long description on `commands/digest.md`. Fix: one `expense-policy` skill with a 200-character description that reads a policy file, a short agent description, and a one-line command description. The `plugin details` per-component table points to the offenders.
5. **Secret in a config file.** `server/config.json`, line 3: `"api_token": "FAKE-TOKEN-DO-NOT-USE-0000"`. The server reads the file but never uses the token. Fix: delete the key, and if a token were needed, declare it as a sensitive `user_config` option, never in the folder. Also check that nothing logs it.
6. **Version drift.** `.claude-plugin/plugin.json` line 4 says 1.4.0. The top `CHANGELOG.md` entry (line 3) is 1.2.1. `server/manifest.json` line 4 says 1.2.0. `server/server.py` line 37 reports 1.2.1. Fix: pick the real next version, write a changelog entry for the work since 1.2.1, and set every place to match. Either direction is acceptable if it is justified.

What to look for: students who run only the tools find defects 3 (partly), 4, and maybe 2. The secret and the version drift need reading. Cap the Part 1 time. If a student finishes early, ask what an attacker or a new hire would do with the plugin as it was.

For Part 2, run the Gauntlet yourself beforehand on a plugin you built, time it, and price it. This guide has not seen a paid run: the build environment was not signed in, so the eval cases, the cold-install case (which relies on `context.add_dirs` to give Claude read access to the copied plugin), the mock connector, and the point values were checked only for file format and for the static scoring. Expect to adjust `--runs`, `--max-cost-usd`, and `--concurrency`. Also unconfirmed: whether `claude plugin eval` can run a plugin whose connector is a local MCP server without mocks (the Gauntlet uses mocks, so students' servers are not exercised by it; they are exercised by the self-test and by hand). Grader judgments by the language model can vary between runs, so read the report for a disputed score.
