# Lab 2: Governance Program Design

> Part of **[Claude Governance, Compliance and Conformance Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

**Learning objective:** Design a governance program with owners, decision rights, tiers, controls, cadence, metrics and reporting under conflicting constraints, with every commitment tied to named evidence. Time: 75 minutes.

**Files:** `$FILES/brightwater_org_brief.md`, `$FILES/risk_tier_scale.md`, `$FILES/technical_capabilities_card.md`, `$FILES/evidence_menu.md`, `$FILES/lab2_constraints_and_draft.md`, `$FILES/lab2_program_design_template.md`, `$FILES/lab2_scoring_rubric.md`.

**Context:** Six weeks after the policy was approved, Dana Whitfield (CEO) wants a program leadership can approve on Friday. A steering committee drafted ten commitments, and five constraints conflict. A customer obligation to Halvern is not negotiable. You design the program.

**Steps:**

1. **Goal:** Read `lab2_constraints_and_draft.md`. Allow 10 minutes. List the five constraints and the ten draft commitments.
2. **Goal:** Audit the draft. Allow 15 minutes. For each of C1 to C10, write what is wrong in section 10 of the template.
3. **Goal:** Design the program in sections 1 to 8 of `lab2_program_design_template.md`. Allow 30 minutes.
4. **Acceptance criteria:**
   - Decision rights name a role for every decision, and approval, operation and audit are separate roles.
   - Tier routing meets the 2-business-day constraint without sending every use to Legal.
   - Every tier has preventive, detective and corrective controls. Technical capabilities are cited as existing, with their limits.
   - Every forum has a chair, a membership, an interval, inputs and outputs. Internal audit and management review both appear, with dates.
   - Metrics include at least one of activity, value and risk, each with source, threshold and action.
   - All five conflicts are resolved, the trade-off is stated, and a named role accepted it.
5. **Goal:** Complete the commitment and evidence ledger (section 9) and the capacity check (section 11). Allow 15 minutes. Every commitment cites evidence by ID.
6. Review the ledger once more and drop or rewrite any commitment that has no evidence. Allow 5 minutes.

**Hints:**

- Resolve a conflict by changing the scope of a commitment, not by splitting the difference.
- A contract obligation is not a trade-off. Build it into intake and into an owner's duties.
- Add up hours. The program has about 87 hours a month.
- Capabilities have limits. A control that cannot reach the use cannot be claimed as evidence.
- Do not promise a review of everything. A sampling plan with a stated size and interval can be done and checked.

**Checkpoint:** A leadership team could approve your program on Friday. Every commitment has a named owner, evidence by ID, and a date it first exists. Your capacity total is at or under 87 hours, or you say what you cut.

**Common problems:**

- Writing a program that satisfies each executive by promising what they asked for. That recreates the draft's contradictions.
- Citing "the Compliance API" as evidence with no extract, date or owner.
- Metrics with only activity. Add a value and a risk measure.
- Giving the CISO every role. The audit and the operation need separate owners.
- Forgetting the Dublin consultation before anything that monitors staff.
- Forgetting Halvern's 30-day notice, which sits outside the tier scale.

**Scoring rubric:** `lab2_scoring_rubric.md`. 100 points across nine sections. The evidence tie is worth 20. Bands: Gold 85 to 100 with an evidence tie of 16 or more, Silver 70 to 84 with 12 or more, Bronze 50 to 69.

**Facilitator note:**

*Where the planted gaps are, and what repairs them:*

- C1, overloaded role with no separation: the CISO chairs, approves every tier and audits. Repair: the COO chairs the Board, tier approvers differ by tier, and internal audit sits outside the CISO's line.
- C2, contradiction of K1, K2 and the Legal headcount: reviewing every use in 2 days cannot be done by 22 people. Repair: Tier 1 needs none, Tier 2 uses pre-cleared standard terms, and Tier 3 gets Legal review inside the 10-day route.
- C3, review of all prompts: impossible at scale and it triggers K5 consultation. The Compliance API provides activity data for all, and content endpoints only for claude.ai organizations. Repair: consult Dublin employee representatives first, then sample Tier 3 activity at a stated size and interval, recorded as E02 and E12.
- C4, activity-only success measure: repair with a value metric (cycle time with a baseline) and a risk metric (Tier 3 uses with current evidence).
- C5, exceptions "reviewed regularly": repair with a monthly exception review, a chair, a register (E09) and a maximum term.
- C6, a block that cannot reach everything: Tenant Restrictions apply to traffic through the company proxy. Whether they reach a personal phone off the network is UNVERIFIED, so do not accept the claim. Repair: block on the company network where the capability reaches, plus attestation, training and a sampling check for the rest.
- C7, over capacity: the activity table already sums to 88 hours against about 87 available, before a monthly audit of all tiers is added. Repair: cut the audit to a quarterly sample, and ask the CFO for hours or accept slower Tier 3 review. Name who accepted.
- C8, a promise with no mechanism: repair with Contracts Manager as owner, the Halvern notice as an intake step (question 5), the clause tracker (E17), and a first-available date before the renewal.
- C9, no owner or threshold: repair with the Finance Business Partner, spend limits by organization, group and individual, a review of increase requests, and E06. Do not rely on pooled budgets or alerts, which are unconfirmed.
- C10, no cadence: repair with a quarterly Audit Committee report using a fixed content list, and a management review (E15) at a stated interval.

*What a strong answer contains:* A conflict table with five resolutions that each state who accepted the trade-off, such as the COO and CEO. A tier route table at same day, 2 days and 10 days. A short list of metrics with sources and thresholds. A ledger where at least 90 percent of commitments qualify. An honest capacity note.

*Watch for:* "Legal reviews all Tier 3 in 2 days." That breaks the 10-day route and K2. Also watch for any claim that goes beyond a capability's limit.
