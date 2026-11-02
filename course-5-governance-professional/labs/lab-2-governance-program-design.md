# Lab 2: Governance Program Design

**Course:** Claude Governance, Compliance and Conformance Professional
**Duration:** 75 minutes
**Format:** Instructor-led, in-class hands-on lab (300 level). Paper only — no tooling required

> Part of **[Claude Governance, Compliance and Conformance Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

## Prerequisites

- [ ] Lab 1 completed — this program implements the policy you drafted
- [ ] `$FILES/brightwater_org_brief.md`, `$FILES/risk_tier_scale.md`, `$FILES/technical_capabilities_card.md`
- [ ] `$FILES/evidence_menu.md` — commitments are cited against these IDs
- [ ] `$FILES/lab2_constraints_and_draft.md`, `$FILES/lab2_program_design_template.md`, `$FILES/lab2_scoring_rubric.md`

> **Note:** no account or tooling needed. This lab produces a program design document.

---

## Overview

Six weeks after the policy was approved, Dana Whitfield (CEO) wants a program leadership can approve on Friday.

A steering committee drafted ten commitments, and **five constraints conflict.** A customer obligation to Halvern is not negotiable. You design the program.

The program has about **87 hours a month**. That number decides what you can honestly promise.

---

## Part 1: Read the Constraints and the Draft

### Step 1: List the Five Constraints and the Ten Commitments (about 10 minutes)

Read `lab2_constraints_and_draft.md`.

**Expected result:** five constraints and ten draft commitments written out, so you can see which pairs conflict.

---

## Part 2: Audit the Ten Commitments

### Step 2: Write What Is Wrong with Each of C1 to C10 (about 15 minutes)

Record your audit in section 10 of the template.

**Acceptance criteria:** every one of C1 to C10 has a stated defect.

> **Hint:** resolve a conflict by changing the scope of a commitment, not by splitting the difference.

> **Key Insight:** a contract obligation is not a trade-off. Build it into intake and into the duties of an owner.

---

## Part 3: Design the Program

### Step 3: Complete Sections 1 to 8 (about 30 minutes)

**Acceptance criteria:**

- Decision rights name a role for every decision, and approval, operation and audit are separate roles.
- Tier routing meets the 2-business-day constraint without sending every use to Legal.
- Every tier has preventive, detective and corrective controls. Technical capabilities are cited as existing, with their limits.
- Every forum has a chair, a membership, an interval, inputs and outputs. Internal audit and management review both appear, with dates.
- Metrics include at least one of activity, value and risk, each with source, threshold and action.
- All five conflicts are resolved, the trade-off is stated, and a named role accepted it.

> **Common Pitfall:** do not satisfy each executive by promising what they asked for. That recreates the contradictions in the draft.

> **Common Pitfall:** a control that cannot reach the use cannot be claimed as evidence. Capabilities have limits — state them.

> **Common Pitfall:** do not promise a review of everything. A sampling plan with a stated size and interval can be done and can be checked.

---

## Part 4: Tie Commitments to Evidence

### Step 4: Complete the Ledger and the Capacity Check (about 15 minutes)

Complete the commitment and evidence ledger (section 9) and the capacity check (section 11).

**Acceptance criteria:** every commitment cites evidence by ID, and the capacity total is at or under 87 hours — or you state what you cut and who accepted it.

> **Hint:** add up hours. Do not estimate the total by feel.

### Step 5: Drop or Rewrite Anything with No Evidence (about 5 minutes)

**Acceptance criteria:** no commitment remains that has no evidence behind it.

> **Common Pitfall:** citing "the Compliance API" is not evidence. Name the extract, the date and the owner.

---

## Part 5: Checkpoint

### Step 6: Verify Your Progress

- [ ] Five constraints and ten commitments listed before designing
- [ ] All of C1 to C10 audited with a stated defect
- [ ] Every decision has a named role
- [ ] Approval, operation and audit sit with separate roles
- [ ] Tier routing meets the 2-business-day constraint without routing everything to Legal
- [ ] Every tier has preventive, detective and corrective controls
- [ ] Every claimed capability is cited with its limits, not beyond its reach
- [ ] Every forum has a chair, membership, interval, inputs and outputs
- [ ] Internal audit and management review both appear, with dates
- [ ] Metrics cover activity, value and risk, each with source, threshold and action
- [ ] All five conflicts resolved, each with the trade-off stated and a named role who accepted it
- [ ] The Dublin consultation precedes anything that monitors staff
- [ ] The Halvern 30-day notice is built into intake and into an owner's duties
- [ ] Every commitment cites evidence by ID, with a date it first exists
- [ ] The capacity total is at or under 87 hours, or the cut is stated with who accepted it
- [ ] No commitment remains without evidence

---

## Troubleshooting Reference

| Issue | Symptom | Solution |
|---|---|---|
| Contradictions survive | Every executive is satisfied on paper | You promised what each asked for. Change the scope of commitments instead |
| Evidence not verifiable | "The Compliance API" cited as evidence | Name the extract, the date and the owner. An API is a source, not evidence |
| Metrics tell you nothing | Only activity measures | Add a value metric (cycle time with a baseline) and a risk metric (Tier 3 uses with current evidence) |
| No separation of duties | The CISO holds every role | The audit and the operation need separate owners |
| Staff monitoring blocked late | A control cannot proceed | The Dublin consultation comes first, before anything that monitors staff |
| Contract obligation missed | The Halvern notice is nowhere | It sits outside the tier scale. Put it in intake and in an owner's duties |
| Capacity overrun | The program promises more than 87 hours | Add up the hours, cut something specific, and name who accepted the slower route |

---

## Scoring Rubric

See `lab2_scoring_rubric.md`. 100 points across nine sections. The evidence tie is worth 20.

Bands: **Gold** 85 to 100 with an evidence tie of 16 or more, **Silver** 70 to 84 with 12 or more, **Bronze** 50 to 69.

---

## What You Built

In 75 minutes, you:

- Designed a program leadership could approve on Friday, with a named role behind every decision
- Resolved five conflicting constraints by changing scope rather than splitting the difference, and named who accepted each trade-off
- Separated approval, operation and audit so no one reviews their own work
- Tied every commitment to evidence by ID, with a date it first exists, and dropped the ones that had none
- Added up the hours and said what you cut, instead of promising 88 hours of work in an 87-hour program

---

## What's Next

Lab 3, the Risk Register, is the take-home. It moves from program design to the register that tracks what could go wrong and who owns it.

---

## Facilitator Notes

*Where the planted gaps are, and what repairs them:*

- **C1, overloaded role with no separation:** the CISO chairs, approves every tier and audits. Repair: the COO chairs the Board, tier approvers differ by tier, and internal audit sits outside the line of the CISO.
- **C2, contradiction of K1, K2 and the Legal headcount:** reviewing every use in 2 days cannot be done by 22 people. Repair: Tier 1 needs none, Tier 2 uses pre-cleared standard terms, and Tier 3 gets Legal review inside the 10-day route.
- **C3, review of all prompts:** impossible at scale and it triggers K5 consultation. The Compliance API provides activity data for all, and content endpoints only for claude.ai organizations. Repair: consult Dublin employee representatives first, then sample Tier 3 activity at a stated size and interval, recorded as E02 and E12.
- **C4, activity-only success measure:** repair with a value metric (cycle time with a baseline) and a risk metric (Tier 3 uses with current evidence).
- **C5, exceptions "reviewed regularly":** repair with a monthly exception review, a chair, a register (E09) and a maximum term.
- **C6, a block that cannot reach everything:** Tenant Restrictions apply to traffic through the company proxy. Whether they reach a personal phone off the network is UNVERIFIED, so do not accept the claim. Repair: block on the company network where the capability reaches, plus attestation, training and a sampling check for the rest.
- **C7, over capacity:** the activity table already sums to 88 hours against about 87 available, before a monthly audit of all tiers is added. Repair: cut the audit to a quarterly sample, and ask the CFO for hours or accept slower Tier 3 review. Name who accepted.
- **C8, a promise with no mechanism:** repair with Contracts Manager as owner, the Halvern notice as an intake step (question 5), the clause tracker (E17), and a first-available date before the renewal.
- **C9, no owner or threshold:** repair with the Finance Business Partner, spend limits by organization, group and individual, a review of increase requests, and E06. Do not rely on pooled budgets or alerts, which are unconfirmed.
- **C10, no cadence:** repair with a quarterly Audit Committee report using a fixed content list, and a management review (E15) at a stated interval.

*What a strong answer contains:* A conflict table with five resolutions that each state who accepted the trade-off, such as the COO and CEO. A tier route table at same day, 2 days and 10 days. A short list of metrics with sources and thresholds. A ledger where at least 90 percent of commitments qualify. An honest capacity note.

*Watch for:* "Legal reviews all Tier 3 in 2 days." That breaks the 10-day route and K2. Also watch for any claim that goes beyond the limit of a capability.

---

*Lab 2 Complete*
