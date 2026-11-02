# Demo 4: Trace a Policy Line to Evidence

**Course:** Claude Governance, Compliance and Conformance Professional (Claude MasterClass Professional, Course 5)
**Demo:** 4 of 6
**Time:** about 12 minutes

> Part of **[Claude Governance, Compliance and Conformance Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Trace a policy statement to an owner, a control and dated evidence, and spot a line that cannot be traced. Time: about 12 minutes.

**Files:** [`$FILES/demo4_policy_line_trace.md`](../demo-files/demo4_policy_line_trace.md), [`$FILES/technical_capabilities_card.md`](../demo-files/technical_capabilities_card.md), [`$FILES/evidence_menu.md`](../demo-files/evidence_menu.md).

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

**Previous:** [Demo 3: Tier Five AI Uses](demo-3-tier-five-ai-uses.md) · **Next:** [Demo 5: Read an Adoption Dashboard](demo-5-read-an-adoption-dashboard.md)


*Demo 4 of 6*
