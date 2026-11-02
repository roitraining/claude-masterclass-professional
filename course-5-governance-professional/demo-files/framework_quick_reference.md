# Framework Quick Reference (Leave-Behind)

Claude MasterClass, Professional Course 5. Regulation here is awareness only, not legal advice. Check the source text before you quote wording, and check current dates with counsel.

## NIST AI Risk Management Framework 1.0

Voluntary guidance. Organizes AI risk work into four functions:

| Function | In plain words |
|---|---|
| Govern | Policies, roles, accountability, culture |
| Map | Know the uses, their context, and who is affected |
| Measure | Test and track the risks you found |
| Manage | Respond, prioritize and treat the risks |

## ISO/IEC 42001:2023

A certifiable AI management system standard. It follows the Annex SL high-level structure, so management-system clauses run 4 to 10:

- Clauses 4 to 10 cover context, leadership, planning, support, operation, performance evaluation, and improvement.
- Clause 9.2 is internal audit. Clause 9.3 is management review.
- Annex A holds controls. Do not quote a count until you have checked the standard.

## Why organizations run both

NIST gives a common language and a working method for risk. ISO/IEC 42001 gives a management system an outside party can certify. Certification is the difference: NIST is guidance, ISO/IEC 42001 can be certified.

## EU AI Act (awareness only)

A regulation with tiers: prohibited practices, high-risk, limited-risk with transparency duties, minimal risk, plus obligations for general-purpose AI models. Dates and scope change. Ask counsel which tier any of your uses could fall into and what applies today.

## Technical controls that can supply evidence

| Capability | Evidence it can supply |
|---|---|
| Identity and roles | Dated export of users, roles and groups |
| Compliance API activity data | Activity extract; directory snapshot |
| Tenant Restrictions | Proxy rule listing allowed organizations |
| Managed settings and sandbox | Enforced settings and change history |
| Spend limits | Limits by level; request and decision log |

## Industry data point (quote with its limits)

Veracode's 2026 GenAI Code Security Report found that AI-generated code passes security tests 56 percent of the time, so about 44 percent of tests found a vulnerability from the OWASP Top 10. The tests used raw models with no agents, guardrails or human review. It shows how often models generate flaws, not how often flawed code reaches production. Re-read the report before you quote it.

## Five questions an assessor asks about any policy line

1. Who owns it, by name or role?
2. What control makes it happen?
3. What record proves the control worked?
4. How recent is that record?
5. What happens when it fails?

## Your next step

Pick a policy line. Trace it to a control and to evidence. If a link is missing, that is the gap to raise this week.
