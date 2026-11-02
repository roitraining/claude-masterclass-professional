# Claude Governance, Compliance and Conformance Professional: Labs

**Course:** Claude Governance, Compliance and Conformance Professional (Claude MasterClass Professional, Course 5)
**Contents:** Two timed hands-on labs and a take-home lab. The numbers match the Today's Labs slide.

---

## About this guide

You work on paper or in a document. No software, account or credential is needed. Work alone. If you prefer to work in a pair, you may, but nothing depends on it.

These are 300-level labs. Each states a goal, acceptance criteria and hints. Each contains planted gaps that you are expected to find. Each is scored with a rubric a facilitator can apply by hand. The labs assume Essentials Course 4 helps but do not re-teach it.

One fictional company carries the day: Brightwater Health Supply. Every person, customer and figure is invented. Use only the brief and your pack. Where a fact is missing, write an assumption and label it.

**Regulation is awareness only.** Nothing here is legal advice. Where a step touches the law, your answer is to name who must be asked, not to decide.

In this guide `$FILES` means the `demo-files` folder your instructor gives you.

**Before Lab 1:** Read `$FILES/brightwater_org_brief.md`, `$FILES/risk_tier_scale.md`, and `$FILES/technical_capabilities_card.md`.

---

## Lab 1: Draft an Enforceable AI Usage Policy

**Learning objective:** Turn an inherited draft policy into one that is enforceable, owned and followable, and test it against planted gaps. Time: 75 minutes.

**Files:** `$FILES/brightwater_org_brief.md`, `$FILES/risk_tier_scale.md`, `$FILES/technical_capabilities_card.md`, `$FILES/lab1_policy_template.md`, `$FILES/lab1_gap_check_sheet.md`, `$FILES/lab1_scoring_rubric.md`.

**Context:** Brightwater's committee wrote a short policy, version 0.3. It goes to the Governance Board next week. Marcus Oyelaran (CRO) wants speed, Priya Raman (General Counsel) wants approvals before use of customer or employee data, and Tomas Lindqvist (CISO) wants unapproved tools blocked. The policy must satisfy all three as far as it honestly can. The template holds the inherited text for each of the eight sections.

**Steps:**

1. **Goal:** Read the brief and the tier scale. In 5 minutes, list the three conflicts your policy must settle.
2. **Goal:** Complete all eight sections of `lab1_policy_template.md`. Allow 40 minutes. For each section, keep, repair or replace the inherited text and note which.
3. **Acceptance criteria while you draft:**
   - Every approval names a role, and a deputy for when that role is away.
   - Every rule can be checked by a control or a record, or is a duty a person can meet.
   - Every exception has an approver, a reason, an expiry date and a place in a register.
   - Every tool has an owner by role and a review date.
   - There are consequences, by severity, and a way to report a mistake.
   - The policy uses Brightwater's four data classes.
4. **Goal:** Run `lab1_gap_check_sheet.md` against your draft. Allow 15 minutes. Repair every gap you find.
5. **Goal:** Swap drafts with a colleague, or, working alone, set your policy aside for 3 minutes and then answer the five employee-test questions in `lab1_scoring_rubric.md` using only your text. Allow 10 minutes.
6. Write a one-sentence note: a conflict from the brief that you resolved and how. Allow 5 minutes.

**Hints:**

- Use the tier scale's decision times. They are how you meet speed and legal review at once.
- Write "the Governance Program Lead" and not "management".
- If a rule says "make sure", ask how a person would prove it. If they cannot, rewrite it.
- Name what the policy covers that the old text left out: contractors, personal phones, and AI features inside approved vendor tools.
- A tool you cannot reach with a technical control still needs a rule, an attestation and a sampling check.

**Checkpoint:** Your policy passes at least 10 of the 12 gap tests, answers at least 4 of the 5 employee questions from the text alone, and names an approver, an exception expiry and a consequence.

**Common problems:**

- Fixing wording and not the mechanism. "Approval will be given within 2 business days" with no named approver still fails G1.
- Adding a rule that cannot be enforced, for example banning all personal chatbots on personal phones with no way to check. Pair every such rule with what you will actually do.
- Making the CISO the owner of everything. Separate approval from audit.
- Leaving "Owner" as "IT". A team is not an owner.
- Writing a policy so long that the employee test fails. Keep each rule to a sentence.
- Treating the EU AI Act as a rule you must interpret. Name counsel as the consulted role.

**Scoring rubric:** `lab1_scoring_rubric.md`. 100 points: gap closure 60, fit to the organization 20, employee test 20. Bands: Gold 85 to 100, Silver 70 to 84, Bronze 50 to 69. A zero on G1, G2 or G5 caps the band at Bronze.

**Facilitator note:**

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

## Lab 2: Governance Program Design

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

---

## Lab 3 (Take-Home): Risk Register

**Learning objective:** Build a risk-tiered register for a portfolio of 12 AI uses, with an owner, a tier, a control and evidence for each, and spot what the portfolio hides. Time: 90 to 120 minutes, on your own, after class.

**Files:** `$FILES/lab3_ai_use_portfolio.md`, `$FILES/lab3_risk_register_template.md`, `$FILES/lab3_risk_register_template.csv`, `$FILES/lab3_scoring_rubric.md`, `$FILES/risk_tier_scale.md`, `$FILES/technical_capabilities_card.md`, `$FILES/evidence_menu.md`.

**Context:** Brightwater's 12 AI uses are listed with the owner on file and a note. Some owners are wrong, some uses have changed, and some data classes are hidden. The register is the working inventory the governance program runs on. Professional 4's controls are capabilities that exist. You cite them. You do not configure them.

**Steps:**

1. **Goal:** Read the portfolio. Mark anything that looks stale, hidden or missing. Allow 15 minutes.
2. **Goal:** Complete a register row for each use, in the Markdown template or the CSV. Allow 60 minutes.
3. **Acceptance criteria:**
   - Every owner is a named current role that exists in the brief.
   - Every tier follows the highest-risk fact and the deciding fact is stated.
   - Every control is specific, fits the tier, and states its own limit.
   - Every row cites an evidence ID from the menu, or a clearly described dated record.
   - Every row has a next review date and a trigger for an earlier review.
4. **Goal:** Count by tier. Rank your top three risks and give a reason for each. Allow 15 minutes.
5. **Goal:** Write what looks wrong, stale or hidden in the portfolio. Score yourself with `lab3_scoring_rubric.md`. Allow 15 minutes.

**Hints:**

- If the owner on file left the company, assign a current role and say why.
- Check the data column against the notes. A note can contradict a data class.
- A tool that added a feature has changed. Route it again.
- A control that needs a setting you invented does not count.
- Evidence you cannot produce today needs a first-available date.

**Checkpoint:** Twelve rows, no blank owner, a count by tier, three ranked risks, and a register review date with a trigger.

**Common problems:**

- Putting a team as the owner.
- Tiering by the data column alone and missing a note that changes it.
- Naming a capability without saying what it does not reach.
- Listing "policy" as evidence.
- Ranking risks by how loud they sound rather than by who could be harmed.

**Scoring rubric:** `lab3_scoring_rubric.md`. 100 points: 7 points a row (12 rows) plus 16 for the whole portfolio. Bands: Gold 85 to 100, Silver 70 to 84, Bronze 50 to 69.

**Facilitator note:** Share this key after the take-home is due.

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

*Traps:* stale owner (BW-04), hidden data class (BW-06), changed use (BW-09), consultation not done (BW-11). Count by tier: Tier 1: 2, Tier 2: 4, Tier 3: 6. Accept a defensible variation if the reason is stated. The strongest top three are usually BW-05, BW-04 and BW-11, because people are harmed, a customer obligation is at stake, and owners are missing. Do not ask students to configure any capability. Cite the capability as an existing source of evidence only.
