# Lab 3 (Take-Home): Risk Register

**Course:** Claude Governance, Compliance and Conformance Professional
**Duration:** 90 to 120 minutes
**Format:** Take-home lab, on your own after class. Paper only — you cite capabilities, you do not configure them

> Part of **[Claude Governance, Compliance and Conformance Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

## Prerequisites

- [ ] Labs 1 and 2 completed — the register is what the program you designed runs on
- [ ] `$FILES/lab3_ai_use_portfolio.md` — the 12 AI uses, with the owner on file and a note
- [ ] `$FILES/lab3_risk_register_template.md` or `$FILES/lab3_risk_register_template.csv`
- [ ] `$FILES/lab3_scoring_rubric.md`, `$FILES/risk_tier_scale.md`, `$FILES/technical_capabilities_card.md`, `$FILES/evidence_menu.md`
- [ ] No account or tooling needed

> **Note:** the controls from Professional 4 are capabilities that exist. You cite them. **You do not configure them.**

---

## Overview

The 12 AI uses of Brightwater are listed with the owner on file and a note. **Some owners are wrong, some uses have changed, and some data classes are hidden.**

The register is the working inventory the governance program runs on. A row that looks complete but names a departed owner, or tiers from a data column that a note contradicts, is worse than a blank row — it reads as settled.

---

## Part 1: Read the Portfolio

### Step 1: Mark Anything Stale, Hidden or Missing (about 15 minutes)

Read the portfolio and mark every use that looks stale, hidden or missing something.

**Expected result:** a marked-up portfolio, before you fill in a single register row.

> **Hint:** check the data column against the notes. A note can contradict a data class.

> **Hint:** a tool that added a feature has changed. Route it again.

---

## Part 2: Build the Register

### Step 2: Complete a Row for Each of the Twelve Uses (about 60 minutes)

Work in the Markdown template or the CSV.

**Acceptance criteria:**

- Every owner is a named current role that exists in the brief.
- Every tier follows the highest-risk fact, and the deciding fact is stated.
- Every control is specific, fits the tier, and states its own limit.
- Every row cites an evidence ID from the menu, or a clearly described dated record.
- Every row has a next review date and a trigger for an earlier review.

> **Hint:** if the owner on file left the company, assign a current role and say why.

> **Common Pitfall:** a team is not an owner. Name a role.

> **Common Pitfall:** a control that needs a setting you invented does not count.

> **Common Pitfall:** evidence you cannot produce today needs a first-available date.

---

## Part 3: Count and Rank the Risks

### Step 3: Count by Tier and Rank Your Top Three (about 15 minutes)

**Acceptance criteria:** a count by tier, and three ranked risks each with a stated reason.

Then set a review date for the **register as a whole**, and a trigger that brings
that review forward. This is separate from the per-row dates in Step 2: a row
review checks one use, while the register review asks whether the inventory is
still complete.

**Acceptance criteria:** a register-level review date and a stated trigger for an
earlier review.

> **Key Insight:** rank by who could be harmed, not by how loud the risk sounds.

---

## Part 4: Write What the Portfolio Hides

### Step 4: Record What Looks Wrong, Stale or Hidden

**Acceptance criteria:** a written note naming what the portfolio obscured, not just what it listed.

---

## Part 5: Score Yourself

### Step 5: Apply the Rubric (about 15 minutes)

Score yourself with `lab3_scoring_rubric.md`.

**Expected result:** a score and a band, with your weakest rows identified.

---

## Part 6: Checkpoint

### Step 6: Verify Your Progress

- [ ] Twelve rows completed
- [ ] No blank owner, and no team listed as an owner
- [ ] Every owner is a current role that exists in the brief
- [ ] Every tier states the deciding fact, taken from the highest-risk fact
- [ ] No row is tiered from the data column alone where a note contradicts it
- [ ] Every control is specific, fits its tier, and states its own limit
- [ ] No control relies on a setting you invented
- [ ] Every row cites an evidence ID, or a clearly described dated record
- [ ] "Policy" is not listed as evidence anywhere
- [ ] Evidence you cannot produce today has a first-available date
- [ ] Every row has a next review date and a trigger for an earlier review
- [ ] A count by tier is recorded
- [ ] A register-level review date and an earlier-review trigger are set, separate from the per-row dates
- [ ] Three risks ranked, each with a reason based on who could be harmed
- [ ] A written note records what the portfolio obscured
- [ ] Scored against the rubric, with a band

---

## Troubleshooting Reference

| Issue | Symptom | Solution |
|---|---|---|
| Owner is a team | "Owner: Finance" | A team cannot be accountable. Name a role |
| Owner has left | The owner on file is gone | Assign a current role from the brief and say why you reassigned it |
| Tier too low | A note contradicts the data column | Tier follows the highest-risk fact. State the deciding fact in the row |
| Control overclaims | A capability named with no limit | Say what it does not reach. A control that cannot reach the use is not a control for it |
| Evidence not real | "Policy" cited as evidence | A policy is a commitment, not evidence. Cite a record with a date and an owner |
| Ranking by volume | Top three are the loudest risks | Rank by who could be harmed, and by whether an obligation is at stake |

---

## Scoring Rubric

See `lab3_scoring_rubric.md`. 100 points: 7 points a row (12 rows) plus 16 for the whole portfolio.

Bands: **Gold** 85 to 100, **Silver** 70 to 84, **Bronze** 50 to 69.

---

## What You Built

In 90 to 120 minutes, you:

- Turned a portfolio listing into a working register with a named current owner on every row
- Tiered by the highest-risk fact and stated which fact decided it, so a reviewer can disagree with your reasoning rather than guess at it
- Cited each control with its own limit, instead of naming a capability and implying full coverage
- Found what the portfolio hid: a departed owner, a data class buried in a note, a tool that changed under you, and a consultation never done
- Ranked your top three by who could be harmed, not by how alarming each sounded

---

## What's Next

This is the final lab in Claude Governance, Compliance and Conformance Professional, and in the Professional track. Across the three labs you wrote the policy, designed the program that enforces it, and built the register it runs on. The register is the one that goes stale fastest — the review trigger on each row is what keeps it honest.

---

## Facilitator Notes

Share this key after the take-home is due.

| ID | Tier | Flag | Deciding fact | Strong control and evidence |
|---|---|---|---|---|
| BW-01 | 1 | None | Public data, editor reads each post | Editor approval; inventory entry (E08) |
| BW-02 | 2 | None | Confidential source code | Managed settings and sandbox, pull request review; E04, E05, E02 |
| BW-03 | 3 | Shadow, not permitted as practiced | Regulated data, unknown vendor | Stop use, vendor review (E16), route through intake; incident record (E18) |
| BW-04 | 3 | Changed | Ranks people, EU candidates, stale owner | Assign a current owner, switch off by default until reviewed, human decision record (E21), counsel and consultation (E20) |
| BW-05 | 3 | Shadow, not permitted as practiced | Halvern contract terms and a personal account | Stop use, approved workspace with data rules, notice tracker (E17), attestation (E11) |
| BW-06 | 3 | None | Payment references present, so highest-risk fact is Regulated | Data rule, sampling check by Finance and Security, activity extract (E02) |
| BW-07 | 2 | None | Confidential, a lawyer reads every change | Group-limited access (E01); inventory entry (E08) |
| BW-08 | 3 | None | Health-related details feeding regulatory reports | Named reviewer sign-off, counsel consulted on reporting duties; risk acceptance (E13) |
| BW-09 | 2 | Changed | The vendor added a chat assistant by default | Vendor due diligence on the new feature (E16), re-intake, switch off pending review |
| BW-10 | 1 | Shadow | Public data, personal subscription | Register it, move to a company-paid tool or approve it; rights question to counsel |
| BW-11 | 3 | Hold until consultation | EU personal data, recorded voices of staff and customers | Consultation with Dublin employee representatives (E20), vendor review (E16), named owner |
| BW-12 | 2 | None | Confidential logs, a person reviews every report | Group-limited access, review sign-off; note the CISO also audits, so separate it |

*Traps:* stale owner (BW-04), hidden data class (BW-06), changed use (BW-09), consultation not done (BW-11).

Count by tier: Tier 1: 2, Tier 2: 4, Tier 3: 6. Accept a defensible variation if the reason is stated.

The strongest top three are usually BW-05, BW-04 and BW-11, because people are harmed, a customer obligation is at stake, and owners are missing.

Do not ask students to configure any capability. Cite the capability as an existing source of evidence only.

---

*Lab 3 Complete*
