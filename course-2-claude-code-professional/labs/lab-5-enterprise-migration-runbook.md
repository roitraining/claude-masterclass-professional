# Lab 5 (take-home): Enterprise Migration Runbook

**Course:** Claude Code Professional
**Duration:** About 60 minutes
**Format:** Take-home lab, paper only — no tenant or organization changes

> Part of **[Claude Code Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

## Prerequisites

- [ ] Labs 1 through 4 completed
- [ ] Module 9 covered, including the Console-to-Enterprise cutover steps
- [ ] `$FILES/lab5-migration` from your instructor: `scenario-sheet.md`, `runbook-template.md`, `rubric.md`
- [ ] No account, tenant or organization access needed — this lab produces a document

> **Note:** this lab is paper only. Do not make changes in any real tenant or organization. Any live demonstration is instructor-only.

---

## Overview

The scenario sheet describes Larkspur Freight Software: team size, an identity provider, CI on GitHub Actions and GitLab, managed settings needs, and five credentials in use. You write the runbook a teammate could run on cutover day.

The steps come from the course: provision seats and SCIM group mappings and sync; confirm Claude Code is enabled and set `forceLoginOrgUUID` in managed settings; remove leftover Console credentials such as API key variables and `apiKeyHelper`; `/login`, choose the Enterprise organization, and verify with `/status`; move CI to a `claude setup-token` credential or keep Console keys for automation; remove migrated users from the Console organization.

Analytics and API keys do not carry over, so export Console reporting first. CLI session history is local and needs no migration. Spend limits are out of scope.

**This lab is about the order of the steps and what breaks if you do them early.**

---

## Part 1: Read the Scenario (about 10 minutes)

Goal: know the constraints before you write a word of the plan.

### Step 1: List Every Constraint and Trap

Read `scenario-sheet.md` and list every constraint and every trap you can find, before you write any of the runbook.

**Expected result:** a written list you can check your finished plan against.

> **Hint:** ask which credentials are tied to a person, and what happens when that person leaves.

> **Hint:** ask what you can enforce on a laptop the company does not manage.

---

## Part 2: Draft the Runbook (about 35 minutes)

Goal: a runbook that is exact about order, owner, time and the check that proves each step.

### Step 2: Fill In the Runbook Template

Work through `runbook-template.md`. Every step needs an owner, a time estimate, and the check that proves it worked.

**Expected result:** a complete runbook a teammate could follow on the day without asking you questions.

### Step 3: Decide Every Credential C1 to C5

**Acceptance criteria:** every credential C1 to C5 has a decision, a reason and a step in the plan.

> **Hint:** ask what a subscription token is tied to, and whether it fits a secret shared by 14 repositories.

### Step 4: State the Reason for Every Ordering

For each step, ask what fails if it runs first, and write the answer down.

**Acceptance criteria:** every ordering in the plan has its reason stated.

> **Common Pitfall:** where you need a product detail you cannot source, write "to confirm". Do not invent product behavior or role names. The rubric deducts for unsourced claims presented as fact.

---

## Part 3: Self-Score and Revise (about 15 minutes)

Goal: find your own weakest area before anyone else does.

### Step 5: Score Against the Rubric

Score your runbook yourself against `rubric.md`.

**Expected result:** a score out of 100 with your weakest area identified.

### Step 6: Fix the Lowest-Scoring Area

**Acceptance criteria:** the lowest-scoring area is revised, and you can say what changed.

---

## Part 4: Submit (optional)

### Step 7: Bring It to the Next Session

Bring the runbook to the next session, or send it to your instructor.

---

## Part 5: Checkpoint

### Step 8: Verify Your Progress

- [ ] Constraints and traps from the scenario sheet listed before drafting
- [ ] `runbook-template.md` completed end to end
- [ ] Every step has an owner, a time estimate and a proving check
- [ ] Credentials C1 through C5 each have a decision, a reason and a step
- [ ] Every ordering decision states what would fail if that step ran first
- [ ] Console reporting export is sequenced before users are removed
- [ ] Sign-in lock is sequenced after seats are provisioned and synced
- [ ] Leftover `ANTHROPIC_API_KEY` and `apiKeyHelper` removal appears in the plan
- [ ] Contractors on unmanaged laptops are addressed explicitly
- [ ] Anything unsourced is marked "to confirm" rather than asserted
- [ ] No spend-cap design included — out of scope
- [ ] Self-scored at 75 or above on `rubric.md`

---

## Troubleshooting Reference

| Issue | Symptom | Solution |
|---|---|---|
| Task list, not a runbook | Low score despite covering everything | The rubric gives its largest share to order and reasons. Sequence the steps and justify each position |
| Console users removed too early | Reporting lost, CI breaks | Export Console reporting first. The Console organization may need to stay for CI until each pipeline has moved |
| Sign-in locked too early | People cannot sign in | The `forceLoginOrgUUID` lock must follow seat provisioning and sync |
| Old credential keeps working | New sign-in appears not to take effect | A leftover `ANTHROPIC_API_KEY` or `apiKeyHelper` can keep working instead. Remove them |
| Scope creep | Deductions on the rubric | Spend caps are out of scope for this lab. Do not design them |

---

## Scoring Rubric

See `rubric.md`. It is out of 100, with deductions for scope creep and for unsourced claims presented as fact.

---

## What You Built

In about 60 minutes, you:

- Turned a scenario sheet into a runbook a teammate could execute on cutover day, with owners, times and proving checks
- Made a reasoned decision on all five credentials, including the ones tied to people who are leaving
- Justified every ordering decision by naming what breaks if that step runs first
- Marked what you could not source as "to confirm" instead of inventing product behavior

---

## What's Next

This is the final lab in Claude Code Professional. Bring the runbook to the next session if your cohort continues, and keep the ordering habit: for any migration, ask what fails if each step runs first.

---

## Facilitator Notes

`facilitator/model-answer-outline.md` lists the traps and what a strong answer does. The traps are: the export must come first, the sign-in lock must follow provisioning, the contractors are not in the identity provider and use unmanaged laptops, three tokens are tied to people who are leaving or are contractors, an organization-wide secret should be an API key, the Console organization may need to stay for CI until each pipeline has moved, and leftover credentials must go. Instructor-only: any demonstration in a tenant or an organization. This lab is paper only.

Some ordering reasons in the rubric are operational reasoning about what fails if a step runs early. The verified facts list the steps and what does not carry over. They do not list failure behavior, so do not present that reasoning as product documentation. Unconfirmed items students may meet: contribution-metric definitions and how they attach to GitHub, spend-alert thresholds, pooled group budgets, and GitLab mention-driven trigger setup beyond the documented webhook pattern. Mark answers that state these as fact.

For students who want to check a laptop in their own life, `$FILES/demo9-cutover/leftover_credentials_check.py` lists the names of leftover credentials without printing values.

---

*Lab 5 Complete*
