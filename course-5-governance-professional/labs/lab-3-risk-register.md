# Lab 3 (Take-Home): Risk Register

> Part of **[Claude Governance, Compliance and Conformance Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

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
