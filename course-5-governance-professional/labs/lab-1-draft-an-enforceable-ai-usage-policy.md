# Lab 1: Draft an Enforceable AI Usage Policy

**Course:** Claude Governance, Compliance and Conformance Professional
**Duration:** 75 minutes
**Format:** Instructor-led, in-class hands-on lab (300 level). Paper only — no tooling required

> Part of **[Claude Governance, Compliance and Conformance Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

## Prerequisites

- [ ] Modules 1 through 4 covered, including the risk tier scale
- [ ] `$FILES/brightwater_org_brief.md`, `$FILES/risk_tier_scale.md`, `$FILES/technical_capabilities_card.md`
- [ ] `$FILES/lab1_policy_template.md` — holds the inherited text for each of the eight sections
- [ ] `$FILES/lab1_gap_check_sheet.md` and `$FILES/lab1_scoring_rubric.md`
- [ ] A colleague to swap drafts with, if the room allows it. Working alone is supported

> **Note:** no account or tooling needed. This lab produces a policy document.

---

## Overview

The committee of Brightwater wrote a short policy, version 0.3. It goes to the Governance Board next week.

Three executives want different things, and the policy must satisfy all three as far as it honestly can:

- **Marcus Oyelaran (CRO)** wants speed.
- **Priya Raman (General Counsel)** wants approvals before use of customer or employee data.
- **Tomas Lindqvist (CISO)** wants unapproved tools blocked.

The template holds the inherited text for each of the eight sections. Your job is to make it enforceable, owned and followable.

---

## Part 1: Read the Brief and Name the Conflicts

### Step 1: List the Three Conflicts Your Policy Must Settle (about 5 minutes)

Read the brief and the tier scale, then list the three conflicts.

**Expected result:** three conflicts written down, each naming the two positions it sits between.

> **Hint:** use the decision times of the tier scale. They are how you meet speed and legal review at once.

---

## Part 2: Draft the Policy

### Step 2: Complete All Eight Sections (about 40 minutes)

For each section, keep, repair or replace the inherited text, and note which you did.

**Acceptance criteria:**

- Every approval names a role, and a deputy for when that role is away.
- Every rule can be checked by a control or a record, or is a duty a person can meet.
- Every exception has an approver, a reason, an expiry date and a place in a register.
- Every tool has an owner by role and a review date.
- There are consequences, by severity, and a way to report a mistake.
- The policy uses the four data classes of Brightwater.

> **Hint:** write "the Governance Program Lead", not "management".

> **Hint:** if a rule says "make sure", ask how a person would prove it. If they cannot, rewrite it.

> **Hint:** name what the policy covers that the old text left out: contractors, personal phones, and AI features inside approved vendor tools.

> **Key Insight:** a tool you cannot reach with a technical control still needs a rule, an attestation and a sampling check. Honesty about reach beats a ban you cannot enforce.

---

## Part 3: Close the Gaps

### Step 3: Run the Gap Check Sheet (about 15 minutes)

Run `lab1_gap_check_sheet.md` against your draft.

**Expected result:** a list of which of the 12 gap tests your draft currently fails.

### Step 4: Repair Every Gap You Found

**Acceptance criteria:** your policy passes at least 10 of the 12 gap tests.

> **Common Pitfall:** fixing wording is not fixing the mechanism. "Approval will be given within 2 business days" with no named approver still fails G1.

> **Common Pitfall:** do not make the CISO the owner of everything. Separate approval from audit.

> **Common Pitfall:** "Owner: IT" is not an owner. A team cannot be accountable.

---

## Part 4: Run the Employee Test

### Step 5: Answer the Five Questions from Your Text Alone (about 10 minutes)

Swap drafts with a colleague. Working alone, set your policy aside for 3 minutes, then answer the five employee-test questions in `lab1_scoring_rubric.md` using **only** your text.

**Acceptance criteria:** at least 4 of the 5 questions answerable from the text alone.

> **Common Pitfall:** a policy long enough to be thorough often fails the employee test. Keep each rule to a sentence.

---

## Part 5: Record What You Resolved

### Step 6: Write the Resolved-Conflict Note (about 5 minutes)

**Acceptance criteria:** one sentence naming a conflict from the brief that you resolved, and how.

---

## Part 6: Checkpoint

### Step 7: Verify Your Progress

- [ ] Three conflicts from the brief listed before drafting
- [ ] All eight sections completed, each marked kept, repaired or replaced
- [ ] Every approval names a role and a deputy
- [ ] Every rule is checkable by a control, a record, or a duty a person can meet
- [ ] Every exception has an approver, a reason, an expiry and a register entry
- [ ] Every tool has an owner by role and a review date
- [ ] Consequences are stated by severity, with a way to report a mistake
- [ ] The four Brightwater data classes are used
- [ ] Contractors, personal phones and vendor-embedded AI features are all in scope
- [ ] At least 10 of the 12 gap tests pass
- [ ] At least 4 of the 5 employee questions answerable from the text alone
- [ ] An approver, an exception expiry and a consequence are all named somewhere
- [ ] A one-sentence note records a resolved conflict and how
- [ ] No legal duty or date is stated as fact without naming counsel as the consulted role

---

## Troubleshooting Reference

| Issue | Symptom | Solution |
|---|---|---|
| Wording changed, gap remains | G1 still fails after a rewrite | A time limit with no named approver is not an approval mechanism. Name the role and a deputy |
| Unenforceable rule added | A ban you cannot check | Pair every such rule with what you will actually do: an attestation, a sampling check, a stated limit of reach |
| One person owns everything | The CISO approves and audits | Separate approval from audit. An auditor cannot review their own approval |
| Owner is a team | "Owner: IT" | A team is not an owner. Name a role |
| Employee test fails | Nobody can find the answer in your text | The policy is too long or too abstract. One sentence per rule |
| Legal duty asserted | A regulation interpreted as a rule | Name counsel as the consulted role rather than interpreting it yourself |

---

## Scoring Rubric

See `lab1_scoring_rubric.md`. 100 points: gap closure 60, fit to the organization 20, employee test 20.

Bands: **Gold** 85 to 100, **Silver** 70 to 84, **Bronze** 50 to 69. A zero on G1, G2 or G5 caps the band at Bronze.

---

## What You Built

In 75 minutes, you:

- Turned an inherited draft into a policy where every approval has a named role and a deputy
- Replaced rules that sound firm but cannot be checked with ones an auditor could actually test
- Settled three executive conflicts using the tier scale rather than by picking a side
- Stated honestly where a technical control cannot reach, and paired those rules with an attestation and a sampling check
- Tested your own policy the way an employee would read it, from the text alone

---

## What's Next

Lab 2, Governance Program Design, moves from a single policy document to the program that keeps it alive: intake, review cadence, and who does what.

---

## Facilitator Notes

*Where each planted gap sits in the inherited text:*

- G1, no named approver: Section 5, "management approval".
- G2, exception with no expiry: Section 6, "stay in place until the need ends".
- G3, rule that cannot be enforced: Section 4, "make sure no AI tool ever keeps company data".
- G4, missing owner: Section 3, two tools have a blank owner and the third lists a team.
- G5, no consequence: Section 7, "dealt with appropriately".
- G6, scope too narrow: Section 1, employees on company laptops only.
- G7, undefined data term: Section 4, "sensitive data".
- G8, no review cadence: Section 8, "periodically".
- G9, no request path: Section 5, "promptly" and no form.
- G10, no separation of duties: Section 2, the CISO approves and audits.
- G11, no safeguards on a use that affects people: Section 5, "AI may be used to help screen job applicants".
- G12, no reporting path: Section 7, silence.

*What a strong answer contains:*

- A policy owner by role, an approver by tier with a deputy, a separate auditor, and Tier 3 risk acceptance by an accountable executive in writing.
- A tool table with an owner role, data classes allowed, groups allowed and a review date. A rule for unlisted tools: not permitted until routed through intake.
- Data rules by class: Regulated data only in the approved workspace, for named groups, with a sampling check by a person. Honest limits stated where a capability does not reach, for example personal phones off the company network.
- Intake with seven questions, decision times of the same day, 2 business days and 10 business days, and legal involvement set by tier so speed and legal review both hold.
- A rule that any use affecting a person is Tier 3, has a human decision with a record, and has counsel and Dublin employee representatives consulted where relevant.
- Exceptions: approver by tier, written reason, maximum 90 days (or similar fixed period), register entry, review before expiry.
- Enforcement by severity, who decides, and a good-faith reporting channel with a response time.
- A fixed review interval (for example every 6 months), an owner, and triggers such as an incident or a vendor change.

*Watch for:* students who copy the policy conflicts into the "kept" column. Ask each one: how would an auditor check this line? Also watch for dates or legal duties stated as fact. Confirm any current dates with counsel. The facilitator may remind the room that EU AI Act dates are not covered here and are UNVERIFIED in the source notes.

---

*Lab 1 Complete*
