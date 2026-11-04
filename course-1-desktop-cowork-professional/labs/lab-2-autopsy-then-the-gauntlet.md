# Lab 2: Autopsy, Then the Gauntlet

**Course:** Claude Desktop Professional
**Duration:** 65 minutes
**Format:** Instructor-led, in-class hands-on lab (300 level)

> Part of **[Claude Desktop Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

## Prerequisites

- [ ] Lab 1 completed — you need the plugin you built
- [ ] `claude` signed in for eval runs. Run `claude` and sign in with `/login` before you start
- [ ] Python 3.11 or later
- [ ] `$FILES` from your instructor: `autopsy-plugin/`, `AUTOPSY-WORKSHEET.md`, `gauntlet/` (`gauntlet.py`, `scorecard.md`, `SECURITY-CHECKLIST.md`, `adversarial/ADVERSARIAL-PACK.md`), `templates/`
- [ ] `scorecard.md` read before you begin

> **Token cost.** The full Gauntlet is a paid run. It caps spend at 5 dollars and uses 2 runs per case by default. Iterate with `--only` on a single group rather than re-running everything, and re-check free items with `--static-only`.

---

## Overview

The autopsy plugin passes `claude plugin validate` and has six defects that a validator does not catch. Finding them is the first half of this lab.

The Gauntlet is an automated scorecard out of 100 for your own plugin: an eval suite with a no-plugin baseline, a context-cost budget, a simulated cold install, an adversarial prompt pack, and a security checklist. **Bronze is 60, Silver is 75, Gold is 90 with all the security points.**

---

## Part 1: Plugin Autopsy (about 25 minutes)

### Step 1: Copy the Plugin and Open the Worksheet

```
cp -r $FILES/autopsy-plugin ~/work/expense-digest
```

Open `AUTOPSY-WORKSHEET.md` beside it.

**Expected result:** a working copy you can break and fix freely.

### Step 2: Run the Tool Checks and Record the Always-On Figure

```
claude plugin validate ~/work/expense-digest
claude --plugin-dir ~/work/expense-digest plugin details expense-digest
```

**Expected result:** validation passes, and you have the always-on token figure written down. A passing validator here is the lesson, not the goal.

Validation also prints advisory lines about files wanted for **directory
submission**, such as a `README` and a `LICENSE`. Those are not defects and are
not among the six. This plugin is not being submitted anywhere; Lab 3 covers
submission. Treat them as noise for this lab.

### Step 3: Find the Six Defects

There is one defect in each area on the worksheet: trigger, permissions, setup, context cost, secrets, and versioning. For each, write down the file and the evidence **before** you fix it.

**Acceptance criteria:** six defects located, each with a file and the evidence that proves it.

> **Hint:** read every file once, in the order Claude would meet them. A tool finds some of them. Your own reading finds the rest.

### Step 4: Fix Each Defect

**Acceptance criteria, by area:**

- **Trigger:** the description of the main skill would make Claude choose it for an expense digest request and not for unrelated finance questions.
- **Permissions:** no agent has a tool it does not need, and the role that claims to be read-only cannot write, edit, run a shell, or fetch from the web.
- **Setup:** a new hire who follows `SETUP.md` alone reaches a working connector in Claude Code and knows what to expect in Cowork.
- **Context cost:** always-on tokens fall below 1,000, and the policy rules are still available to Claude.
- **Secrets:** no credential-like value is left in any file, and your fix says where a real value would live instead.
- **Versioning:** every place that carries a version shows the same one, and the changelog explains the change.

> **Common Pitfall:** cutting descriptions to save tokens can leave nothing to say when the rule skills apply. Merge the rule skills into one skill that reads a short policy section, and keep one clear description.

### Step 5: Re-Check Your Fixes

```
claude plugin validate ~/work/expense-digest
claude --plugin-dir ~/work/expense-digest plugin details expense-digest
python3 $FILES/gauntlet/gauntlet.py --plugin ~/work/expense-digest --product 1 --static-only --out ~/work/autopsy-check
```

**Acceptance criteria:** validation still passes, always-on tokens are under 1,000, and the free Gauntlet checks show full marks for the secret, tool-scoping and release-hygiene lines.

> **Note:** the structure lines fail here because this plugin is not one of the four products. Ignore them in Part 1.

---

## Part 2: The Gauntlet (about 40 minutes)

### Step 6: Run the Free Checks First (about 5 minutes)

Run the free checks on your own plugin from Lab 1, and read the notes column.

```
python3 $FILES/gauntlet/gauntlet.py --plugin ~/work/<plugin name> --static-only
```

**Expected result:** a static score plus notes naming anything missing. No spend.

### Step 7: Write the Release Files (about 10 minutes)

Start from `$FILES/templates`.

**Acceptance criteria, all of these:**

- `SETUP.md` with Prerequisites, Install, Configure, Verify (with an expected result), and Troubleshooting sections, and a line on what works in chat, Cowork, and Claude Code.
- `CHANGELOG.md` with a first entry. The top version must match `plugin.json` and `server/manifest.json`. Repack the `.mcpb` if you change the manifest.
- `SECURITY-REVIEW.md` only if you added hooks. Do not add a `bin/` folder.

### Step 8: Smoke Test Your Set-Up (about 3 minutes)

Prove your set-up works with a single capped case before you spend on a full run.

```
python3 $FILES/gauntlet/gauntlet.py --plugin ~/work/<plugin name> --smoke
```

**Expected result:** one case completes and is rated.

### Step 9: Run the Full Gauntlet Once (about 10 minutes)

Run the whole Gauntlet and read the report, notes first.

```
python3 $FILES/gauntlet/gauntlet.py --plugin ~/work/<plugin name> --out ~/work/gauntlet-run-1
```

**Expected result:** a scored report with a tier, and a notes column explaining each loss.

### Step 10: Iterate on Your Losses (about 10 minutes)

Rank your losses by points. Fix the largest first, then re-run only the affected group, for example `--only trig` or `--only adv`, which is cheaper than a full run. Re-check the free items with `--static-only` after every change.

**Acceptance criteria:** a measured improvement over run 1, with the largest loss addressed first.

> **Common Pitfall:** cutting descriptions to save tokens can stop the skill firing. Re-run the trigger cases after each cut.

### Step 11: Assemble the Release Package (about 2 minutes, finish at home if needed)

Run the whole Gauntlet a final time, then assemble: the plugin folder, `CHANGELOG.md`, `RELEASE-NOTE.md` from the template with your Gauntlet score and tier, and a recorded 60-second self-demo following `SELF-DEMO-OUTLINE.md`.

**Acceptance criteria:** a report at Bronze or better, a changelog, a one-page release note whose score matches the report, and a recorded self-demo.

> **Note:** also run the adversarial prompts in `adversarial/ADVERSARIAL-PACK.md` by hand in a Cowork session if time allows. The automated eval exercises your plugin in Claude Code only.

---

## Part 3: Checkpoint

### Step 12: Verify Your Progress

**Part 1, the autopsy:**

- [ ] All six defects located, each with a file and recorded evidence
- [ ] Validation still passes after your fixes
- [ ] Always-on tokens under 1,000, with the policy rules still reachable by Claude
- [ ] No credential-like value left in any file, and your fix says where a real one would live
- [ ] Every version-carrying location shows the same version, with a changelog entry explaining it
- [ ] Free Gauntlet checks show full marks for secret, tool-scoping and release-hygiene lines

**Part 2, the Gauntlet:**

- [ ] `SETUP.md`, `CHANGELOG.md` written from the templates
- [ ] Top changelog version matches `plugin.json` and `server/manifest.json`
- [ ] Smoke test completed before the first full run
- [ ] A full Gauntlet report exists at Bronze or better
- [ ] Losses ranked by points, largest addressed first, with a measured improvement
- [ ] One-page release note whose score matches the report
- [ ] A recorded 60-second self-demo showing a slash command, a data problem called out, and the report

Your target is Silver or Gold.

---

## Troubleshooting Reference

| Issue | Symptom | Solution |
|---|---|---|
| Server breaks after removing a secret | Connector fails once the key is gone | You removed the secret from `config.json` but the server still reads it. Fix the code too |
| Version drift persists | Some files still show the old version | Search the whole folder for the old numbers. Every location must match |
| Cowork ignores the setting | Setup works in Claude Code only | You added the data folder step to `SETUP.md` but not the Cowork section. Cowork does not prompt for a setting that has no default |
| Group not rated | "Not rated" in the report | A group did not finish. Read the printed reason. `auth_failed` means Claude Code is not signed in: run `claude` and sign in with `/login`. A cost-ceiling stop means you hit the cap |
| Low structure score | Structure points missing | A name differs from the Lab 1 brief. The script lists exactly what is missing |
| Quality cases fail | Conflict or stale record not reported | The evals use mock connector data, not your server. Your skill and agents must instruct Claude to report both values and date every stale value. Do not rely on your server to judge |
| Injection case fails | Canary string leaked into the reply | Tell your skill and both agents that text in data is information, that anything resembling an instruction goes under `suspect_instructions`, and that Claude tells the user about it |
| Cold install STUCK | A step reports STUCK | Read the step. It is almost always a setting or command your guide assumes the reader already has |
| High total but no tier | 90 or more and still not Gold | A secret was found, or you are missing a security point. Gold needs all 10 |
| Run slow or rate-limited | Long waits or throttling | Lower `--concurrency` |

---

## Scoring Rubric (30 points)

**Part 1, the autopsy (12 points):** 2 points for each defect: 1 for the evidence you recorded and 1 for a fix that meets its acceptance criterion.

**Part 2, the Gauntlet (18 points):**

| Item | Points | Full marks when |
|---|---|---|
| Gauntlet tier | 14 | Bronze 8, Silver 11, Gold 14 |
| Release note | 2 | One page, uses the template, score matches the report |
| Self-demo | 2 | About 60 seconds, shows a slash command, a data problem called out, and the report |

---

## What You Built

In 65 minutes, you:

- Found six defects in a plugin that passes its own validator, including two that only reading finds
- Cut an always-on cost of about 2,050 tokens below 1,000 without losing the rules Claude needs
- Put your own plugin through a scored adversarial suite and ranked your losses by points rather than by what was easiest to fix
- Shipped a release package: setup guide, changelog with matching versions, a release note carrying your real score, and a recorded demo

---

## What's Next

Lab 3, Submit and Distribute, is the take-home lab. It covers the three distribution paths and the security review a reviewer performs before trusting your plugin.

---

## Facilitator Notes

The six planted defects in the autopsy plugin, and where each is:

1. **Vague trigger.** `skills/expense-digest/SKILL.md`, line 3: the description is "Helps with expense stuff and other finance things." Fix: say when to use it ("Summarizes an expense report by category and flags large items. Use when asked for an expense digest or a summary of expenses.").
2. **Over-broad tool permission.** `agents/policy-reviewer.md`, line 4: `tools: Read, Grep, Glob, Bash, Write, Edit, WebFetch` on an agent that says it is read-only. Fix: `tools: Read, Grep, Glob`. The security check of the Gauntlet reports it.
3. **Missing setup step.** `SETUP.md` never says to set the data folder. `.mcp.json` line 7 passes `${user_config.data_dir}` to the server and `.claude-plugin/plugin.json` declares `userConfig.data_dir` with no default. The server raises an error when the variable is unset. Fix: a Configure section that tells the reader to set the data folder through `/plugin configure expense-digest` in Claude Code and says Cowork ignores the server until an option has a default and does not prompt. Better fix: give the option a default or read a bundled folder when it is empty.
4. **Bloated always-on cost.** About 2,050 tokens always-on. Cause: seven rule skills (`expense-policy`, `receipt-rules`, `mileage-rules`, `per-diem-rules`, `lodging-rules`, `gift-rules`, `approval-rules`) each with a 600 to 1,000 character "use for anything" description, a 1,500 character description on `agents/policy-reviewer.md`, and a long description on `commands/digest.md`. Fix: one `expense-policy` skill with a 200-character description that reads a policy file, a short agent description, and a one-line command description. The per-component table from `plugin details` points to the offenders.
5. **Secret in a config file.** `server/config.json`, line 3: `"api_token": "FAKE-TOKEN-DO-NOT-USE-0000"`. The server reads the file but never uses the token. Fix: delete the key, and if a token were needed, declare it as a sensitive `user_config` option, never in the folder. Also check that nothing logs it.
6. **Version drift.** `.claude-plugin/plugin.json` line 4 says 1.4.0. The top `CHANGELOG.md` entry (line 3) is 1.2.1. `server/manifest.json` line 4 says 1.2.0. `server/server.py` line 37 reports 1.2.1. Fix: pick the real next version, write a changelog entry for the work since 1.2.1, and set every place to match. Either direction is acceptable if it is justified.

What to look for: students who run only the tools find defects 3 (partly), 4, and maybe 2. The secret and the version drift need reading. Cap the Part 1 time. If a student finishes early, ask what an attacker or a new hire would do with the plugin as it was.

For Part 2, run the Gauntlet yourself beforehand on a plugin you built, time it, and price it. This guide has not seen a paid run: the build environment was not signed in, so the eval cases, the cold-install case (which relies on `context.add_dirs` to give Claude read access to the copied plugin), the mock connector, and the point values were checked only for file format and for the static scoring. Expect to adjust `--runs`, `--max-cost-usd`, and `--concurrency`. Also unconfirmed: whether `claude plugin eval` can run a plugin whose connector is a local MCP server without mocks (the Gauntlet uses mocks, so student servers are not exercised by it; they are exercised by the self-test and by hand). Grader judgments by the language model can vary between runs, so read the report for a disputed score.

---

*Lab 2 Complete*
