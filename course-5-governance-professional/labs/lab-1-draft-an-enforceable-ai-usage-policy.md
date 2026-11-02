# Lab 1: Draft an Enforceable AI Usage Policy

> Part of **[Claude Governance, Compliance and Conformance Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

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
