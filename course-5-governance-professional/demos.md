# Claude Governance, Compliance and Conformance Professional: Demos

**Course:** Claude Governance, Compliance and Conformance Professional (Claude MasterClass Professional, Course 5)
**Contents:** 6 facilitator-led worked examples. Each takes 15 minutes or less and has a learning objective. The numbers match the Today's Demos slide.

---

## About this guide

Run the demos in order. Each has the same layout: a learning objective, a time, a Files line, a short context paragraph, steps, an Expected result, an Instructor note, and a Why this matters note.

This is a 300-level class for a mixed, non-technical room of executives, managers and employees. These demos assume Essentials Course 4 helps but is not required. They do not re-teach why adoption fails, the three phases, a Center of Excellence, Champions, change-management basics, or the five policy lines. The two Essentials demos on sponsors and pilots are not repeated.

Nobody needs software. Every demo runs on paper or on a shared screen showing a document. One fictional company, Brightwater Health Supply, carries the whole day. Every person, company and figure is invented.

**Regulation is awareness only.** Nothing here is legal advice. Tell the room that counsel confirms current dates and duties. Do not state EU AI Act dates in class. The dates in the verified-facts file are UNVERIFIED against the Official Journal.

**Files.** In this guide `$FILES` means the `demo-files` folder your instructor gives you. Print the files marked for each demo, or put them on screen.

- `$FILES/brightwater_org_brief.md` is the case. Hand it out before Demo 1.
- `$FILES/risk_tier_scale.md`, `technical_capabilities_card.md` and `evidence_menu.md` are reference sheets used in several demos.

> **Run it as a conversation.** Ask the room to attempt each step before you reveal the worked answer. A wrong first attempt teaches more than a right answer you read aloud.

---

## Demo 1: Crosswalk One Control Across Frameworks

**Learning objective:** Show where a single control lands in the NIST AI Risk Management Framework and in ISO/IEC 42001, and read the crosswalk the way an assessor does. Time: about 12 minutes.

**Files:** `$FILES/demo1_crosswalk_worked.md`, `$FILES/evidence_menu.md`.

**Context:** NIST AI RMF 1.0 organizes AI risk work into four functions: Govern, Map, Measure and Manage. ISO/IEC 42001 is a certifiable management system standard with clauses 4 to 10. Organizations run both because NIST gives a working method and a common language, and ISO gives an outside party something to audit. A crosswalk shows one control against both.

**Steps:**

1. Put Part A on screen. Read the control aloud: every AI use is in an inventory with a named owner, a risk tier and a review date.
2. Walk the four NIST rows. For each, read the "What an assessor asks" column and ask the room to say what they would hand over.
3. Walk the ISO/IEC 42001 rows. Stop at clause 9.2 (internal audit) and clause 9.3 (management review). Ask: who checks that the inventory is true, and who in leadership looks at the result?
4. Show the evidence line: E08, E07, E14, E15. Ask which of these Brightwater could produce today. (None of E14 and E15 exist yet.)
5. Switch to Part B. Fill the second control (a person reviews AI output before it goes outside the company) as a class, for NIST Govern, Map, Measure and Manage and for clauses 5, 8, 9.2, 9.3 and 10.
6. Ask the room: if this control were weak, in how many rows would the weakness show up?

**Expected result:** The class fills every row for the second control without help by the last NIST row. They name evidence for clause 9.2 as an audit record and for clause 9.3 as management review minutes. They see that a gap in a single control appears in many rows.

> **Instructor note:**
> - The crosswalk is a teaching device, not an official NIST or ISO mapping. Say so aloud. It works at function level and clause level only. Do not cite NIST subcategory numbers or Annex A control numbers.
> - Verified: NIST AI RMF 1.0 has four functions (Govern, Map, Measure, Manage). ISO/IEC 42001:2023 is certifiable and follows the Annex SL structure with clauses 4 to 10. Clause 9.2 is internal audit and 9.3 is management review.
> - UNVERIFIED: category and subcategory counts for NIST (19 and 72 from a secondary source), and Annex A details (38 controls across nine domains from a secondary source). Do not state them as fact. If a student asks, say they are unconfirmed.
> - Clause titles in the sample (context, leadership, planning, support, operation, performance evaluation, improvement) follow the common Annex SL structure and are not in the verified-facts file. Confirm against the standard text before delivery.
> - The EU AI Act line is awareness only. Do not teach tiers or dates beyond naming it as a regulation that sits over both frameworks. Counsel confirms current dates.

**Why this matters:** Leaders who hear "NIST" and "ISO" as two separate projects fund two programs. A crosswalk shows they are one control set, viewed from two angles.

---

## Demo 2: Settle a Conflict of Authority

**Learning objective:** Decide who may decide and who may accept a risk when three senior leaders disagree, and apply a five-part resolution pattern. Time: about 15 minutes.

**Files:** `$FILES/demo2_conflict_scenario.md`, `$FILES/risk_tier_scale.md`.

**Context:** Marcus Oyelaran (CRO) wants Claude connected to live account records for the whole Sales team on Monday. Priya Raman (General Counsel) cites a contract clause. Tomas Lindqvist (CISO) says controls are not ready. All three are acting inside their own authority. The policy draft says "management approval" and does not name a role.

**Steps:**

1. Read the situation and the three quotes aloud. Give the room 2 minutes in pairs or alone to answer the four questions.
2. Take answers to question 2: which positions are preferences, and which is an obligation? Write "preference" or "obligation" next to each quote.
3. Fill the decision rights chart on screen with the room's suggestions. Push on the last row: who settles a conflict between executives, and what if that person is a party?
4. Ask: may Marcus accept the Tier 3 risk himself? Take a show of hands, then ask for the reason.
5. Reveal the five-part resolution pattern. Compare it with the room's chart.
6. Ask the room to write the decision as a conditional approval in two sentences: what starts Monday, and what waits.

**Expected result:** The class identifies the Halvern clause as an obligation nobody inside the company may waive, and the speed and the tool block as preferences. They conclude that a person who benefits from a use does not accept its Tier 3 risk alone, that the accountable executive signs, and that a named tie-breaker decides on a deadline. A strong conditional decision starts Sales on Tier 1 and Tier 2 data, excludes Halvern records, and holds Tier 3 data until the notice is given and the controls exist.

> **Instructor note:**
> - Do not give a legal reading of the clause. It is a fictional contract term used to show the difference between an obligation and a preference.
> - Accept more than a single chart. Typical answers: the Board chair decides Tier 3 and conflicts, the CEO decides when the chair is a party, and risk acceptance sits with a named accountable executive. Hold firm on three points: no role approves what it also audits, risk acceptance is written, and a deadline exists.
> - If a student proposes a role from a real company (for example a specific Anthropic officer role), redirect to the generic version: a named accountable role at the top of the organization. A real company's governance role is UNVERIFIED here and is not used as a fact.
> - Watch for "escalate to the CEO" for everything. That fails: it creates a bottleneck and stops Tier 1 and Tier 2 decisions from being delegated.

**Why this matters:** Most governance failures come from unclear authority, not from missing technology. When authorities conflict and no tie-break exists, the loudest or fastest executive wins by default.

---

## Demo 3: Tier Five AI Uses

**Learning objective:** Tier five AI uses by their highest-risk fact, flag shadow and changed uses, and show how an intake form routes a new use. Time: about 15 minutes.

**Files:** `$FILES/demo3_five_ai_uses.md`, `$FILES/risk_tier_scale.md`.

**Context:** Shadow AI is the use nobody approved or knows about. The tier scale is Brightwater's own. It ranks by the highest-risk fact, not an average, and a person who reviews the output lowers the burden only when the review is real.

**Steps:**

1. Hand out the tier scale and the five uses. Give 4 minutes, alone, to complete the worksheet.
2. Take the uses in order. For each, ask for a tier and the deciding fact before any discussion.
3. At use C, ask: if recruiters read only the top 20, who is really deciding? Is the review real?
4. At use E, ask what status flag applies, and what the rep should do tomorrow.
5. Put the seven-question intake form on screen. Walk use B through it and show which questions send it to Tier 3.
6. Ask: of these five, which would your organization have found without asking people?

**Expected result:** The class tiers A as Tier 1, D as Tier 2, and B, C and E as Tier 3. They flag B and E as shadow and not permitted as practiced, and C as changed. They name a different deciding fact for each.

> **Instructor note:**
> - Key. A: Tier 1, Public data and an editor reads every post. B: Tier 3, Regulated data and an unknown vendor, shadow, not permitted as practiced, route to Board review after vendor due diligence (E16). C: Tier 3 under tiering rule 3, because it ranks people, and the vendor changed the feature, so flag it changed. The Dublin staff add a reason to ask counsel and consult employee representatives. D: Tier 2, Confidential code with a real pull request review by a second engineer. E: Tier 3, a customer contract imposes conditions and a personal account is outside any control. Shadow, not permitted as practiced.
> - On C, say that whether an AI ranking tool falls in a regulated category under the EU AI Act is a question for counsel. This class does not answer it.
> - On D, if a student cites the Veracode figure, quote it only as follows: 56 percent of tests passed, about 44 percent found a vulnerability from the OWASP Top 10, using raw models with no agents, guardrails or human review. The figure shows how often models generate flaws, not how often flawed code reaches production. Re-read the report before quoting.
> - A student may tier D as Tier 1 because it is "just code". The tiering rule says Confidential data is Tier 2 at minimum.

**Why this matters:** A tier is a routing decision. Without it, either everything waits for legal and the business works around you, or everything moves and the risky use slips through.

---

## Demo 4: Trace a Policy Line to Evidence

**Learning objective:** Trace a policy statement to an owner, a control and dated evidence, and spot a line that cannot be traced. Time: about 12 minutes.

**Files:** `$FILES/demo4_policy_line_trace.md`, `$FILES/technical_capabilities_card.md`, `$FILES/evidence_menu.md`.

**Context:** An assessor starts from a policy line and asks five things: who owns it, what control makes it happen, what record shows it worked, how recent that record is, and what happens when it fails. The technical controls from Professional 4 are capabilities that exist. Nobody configures them today.

**Steps:**

1. Show the trace sheet columns. Read the first worked example: Regulated data only in the approved workspace, by users in the Regulated Data group.
2. For each column, ask the room where the answer would come from, then reveal the entry.
3. Show the second example, "employees should be careful," and ask which columns are empty. Ask the room to rewrite the line so it can be traced.
4. Hand out the capabilities card. Ask the class to trace the spend line: no individual spends beyond their group's AI budget without a reviewed request.
5. Compare with the checklist. Confirm the control used is a capability that exists, and that nothing leans on unconfirmed features.
6. Ask: which line in your own organization's policy would fail this test first?

**Expected result:** The class traces the spend line to the Finance Business Partner as owner, to spend limits that cascade from organization to group to individual as the control, to E06 (the limit settings and the request log) as evidence, and names a failure signal such as an increase with no recorded request. They identify "careful" as untraceable.

> **Instructor note:**
> - Verified: identity, roles and groups; Compliance API activity data; Tenant Restrictions (a proxy header listing allowed organizations); managed settings and sandbox; spend limits cascading organization, group, individual, with a Spend Limits API on Enterprise only.
> - UNVERIFIED: pooled group budgets and alert thresholds (secondary sources only). If a student invents an alert, say it is not confirmed and re-trace without it.
> - The first worked example's failure signal assumes an activity extract can be tied to a Regulated workflow. Activity data shows who did what and when, not which data class was in a prompt. Say this aloud. The data class check is a sampling review by a person, not a software readout.
> - Tenant Restrictions apply to traffic through the company proxy. What they mean for a personal phone off the company network is not confirmed here. Do not claim they block it.
> - Do not drift into how to set any of these up. That is Professional 4.

**Why this matters:** A policy line with no control is a wish, and a control with no evidence is a claim. Assessors and customers such as Halvern ask for the record, not the rule.

---

## Demo 5: Read an Adoption Dashboard

**Learning objective:** Read a dashboard whose headline metric hides problems, sort metrics into activity, value and risk, and set a response. Time: about 15 minutes.

**Files:** `$FILES/demo5_reading_sheet.md`, `$FILES/demo5_adoption_dashboard_monthly.csv`, `$FILES/demo5_adoption_dashboard_by_department.csv`.

**Context:** The leadership dashboard says 78 percent of licensed seats are active weekly, up from 52 percent in March. All figures are synthetic. The class has the data behind the headline.

**Steps:**

1. Show the headline. Ask the room whether this is good news and what they would want to know.
2. Open the monthly file and read the last column. Ask what prompts per active user is doing while the active percent rises.
3. Open the department file. Ask the room to find the three departments that most worry them, and why.
4. Fill the metric-kind table together: activity, value or risk.
5. Ask the class to name at least three problems, each with the number that shows it.
6. Write one response per problem with an owner and a date. Close by asking for a value metric the dashboard lacks.

**Expected result:** The class finds that growth is broad and shallow: active percent keeps rising while prompts per active user peaked in June at 175 and fell to 164. They find that Sales and Engineering produce about 73 percent of all prompts (37,300 of 51,300). They find Sales at 98 percent active with only 2 intake requests and 9 of its 14 exceptions past expiry. They find Tier 3 evidence at 2 of 7 uses. They find Support, which handles Regulated data, only 49 percent active. They note 88 seats are idle on a flat budget.

> **Instructor note:**
> - Key to metric kinds. Weekly active percent, total prompts and prompts per active user are activity. Intake requests are a process count. Exceptions past expiry and Tier 3 uses with evidence are risk. No value metric exists on the dashboard. Suggested value metrics: a cycle time or handling time with a baseline, as in Demo 6's input pack.
> - All numbers are synthetic and invented. Do not present them as benchmarks for any real company.
> - A student may argue that low Sales intake means Sales is compliant. Point to the 9 past-expiry exceptions: heavy use with little intake suggests uses nobody registered.
> - Support's low activity is a different problem from Sales' high activity. One is a stall, the other is a control gap. A single adoption target would push the wrong way for both.

**Why this matters:** An adoption target set without a value or risk measure rewards logins. A stall can look like success and a risk can look like momentum.

---

## Demo 6: Assemble a Board Report

**Learning objective:** Build a one-page board report that states a status, requests a decision, and uses only evidence-backed numbers. Time: about 15 minutes.

**Files:** `$FILES/demo6_board_report_template.md`, `$FILES/demo6_board_inputs.md`, `$FILES/evidence_menu.md`.

**Context:** The Audit Committee wants a quarterly written report. The pack contains 15 facts. Some matter, some are noise, and a good report leaves things out.

**Steps:**

1. Show the template. Read the rule at the top: a reader finds the status and the decision in ten seconds.
2. Ask the room to pick the status color and give the one-line reason. Take two answers and compare.
3. Ask for the decision to request of the board. Insist on options and a recommendation.
4. Pick the four risk posture measures from the pile. Cross out facts that will not appear.
5. Ask for two value measures. If none qualify, state what you would measure instead.
6. Name the one thing that could surprise the board and its owner. Confirm the report fits on a page.

**Expected result:** The class picks amber or red, with a reason built on Tier 3 evidence at 2 of 7, 11 of 23 exceptions past expiry, and the unsent Halvern notice. They request a decision, for example to fund more Tier 3 review capacity or to pause Tier 3 Sales work until the notice is given. They cut fact 2 (raw prompts) and fact 13 (a dashboard widget). They use fact 7 as a value measure and treat fact 8 as an honest signal that Support has not yet improved.

> **Instructor note:**
> - Accept any defensible status color if the reason names evidence. A report that is green because adoption is up fails.
> - The Halvern notice needs 30 days and the renewal closes in five weeks, which leaves only 5 days of slack. Point this out if the class misses it. It is a fictional contract term.
> - Fact 15 (seven vendor AI features on by default, four in the inventory) is a strong candidate for the surprise.
> - Fact 12 (Dublin consultation not yet done) is also strong. Do not give an opinion on what any employee consultation law requires. Say counsel and HR confirm that.
> - The template mentions internal audit and management review in the style of ISO/IEC 42001 clauses 9.2 and 9.3. Whether Brightwater pursues certification is not decided. Say the report works the same either way.

**Why this matters:** A board cannot act on a report that does not say what it needs. The report is where governance either becomes a decision or stays a document.
