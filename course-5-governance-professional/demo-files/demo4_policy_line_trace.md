# Demo 4 Sample: Trace a Policy Line to Evidence

Use `technical_capabilities_card.md` and `evidence_menu.md`.

## The trace sheet

Every policy line should fill every column. An empty cell is a gap.

| Column | Question |
|---|---|
| Policy line | The exact sentence in the policy |
| Owner | Which named role makes this line true? |
| Control | What technical or process control makes it happen? |
| Evidence | Which record shows the control worked? (ID from the menu) |
| Freshness | How recent must the record be, and who produces it? |
| Failure signal | What would show this line is not being followed? |
| Consequence | What happens when it fails? |

## Worked example: a line that traces

| Column | Entry |
|---|---|
| Policy line | "Regulated data may be entered into AI tools only in the approved Claude Enterprise workspace, and only by users in the Regulated Data group." |
| Owner | Governance Program Lead (line); IT Identity Lead (group membership) |
| Control | Role and group assignment through the identity provider; the Regulated Data group is limited to named people; Tenant Restrictions list the company organization as the only one allowed from the company network. |
| Evidence | E01 (dated users, roles and groups export), E02 (activity extract for the Regulated Data group), E03 (proxy rule and change history), E10 (training roster for group members) |
| Freshness | E01 and E10 each quarter, E02 on request within 2 business days |
| Failure signal | A user outside the group appears in an activity extract tied to a Regulated workflow, or a group member has no training record |
| Consequence | Access removed the same day; the incident is logged (E18); repeat or deliberate breaches go to HR |

## Worked example: a line that does not trace

| Column | Entry |
|---|---|
| Policy line | "Employees should be careful with sensitive data when using AI." |
| Owner | None named |
| Control | None. "Careful" cannot be built, measured or audited. |
| Evidence | None |
| Freshness | None |
| Failure signal | None |
| Consequence | None |

## Your turn: trace this line

**Policy line:** "No individual may spend beyond their group's AI budget without a reviewed request."

| Column | Your entry |
|---|---|
| Owner | |
| Control | |
| Evidence (IDs) | |
| Freshness | |
| Failure signal | |
| Consequence | |

## Check your answer

- Did you name an owner by role, not by team?
- Does the control use a capability that exists? Spend limits cascade from organization to group to individual, and a Spend Limits API on Enterprise reviews requests for higher limits.
- Did you avoid relying on pooled group budgets or alert thresholds? Those are not confirmed.
- Does your evidence show the control working, with a date?
