# Lab 5 rubric (100 points)

Score the runbook against the scenario sheet. A point is earned only when the runbook says the specific thing. "Review credentials" earns nothing. "Remove `ANTHROPIC_API_KEY` from shell profiles after sign-in is verified" earns the point.

| Area | Points | What earns them |
|---|---|---|
| Order of operations | 20 | Export of Console reporting comes first. Seats and group mappings are provisioned and synced before sign-in is locked to the organization. CI is moved and tested before migrated users are removed from Console. Each ordering has its reason stated (5 points each, four orderings: export first, sync before lock, CI before removal, pilot before everyone) |
| Identity and seats | 10 | Group to seat mapping stated. A plan for the six contractors who are not in the provider. A way to confirm the sync worked |
| Roles | 10 | A platform lead role and an everyone role, written as can and cannot. The analyst-usage separation is addressed or marked "to confirm". No invented product role names |
| Managed settings | 15 | Each of the four needs is mapped to a mechanism. `forceLoginOrgUUID` is placed correctly. The unmanaged laptops are handled honestly: what cannot be enforced is said, not hidden. A two-sentence justification for server-managed or endpoint-managed per laptop group |
| Credentials | 15 | Each of C1 to C5 has a decision, a reason and a step. Leftover Console credentials (key variables, `apiKeyHelper`) are removed from laptops and repositories. The person-owned tokens in C5 are replaced because their owners are leaving or are contractors |
| CI | 15 | The organization-wide credential is an API key, not a subscription token, and the reason is the token's tie to one person's subscription. A named owner for each pipeline credential. A test before the nightly run. The GitLab project is covered |
| Verification | 5 | `/login` choosing the Enterprise organization and `/status` (or another stated check) proves each person is on the right organization |
| What does not carry over | 5 | Analytics and API keys named as not carrying over, with the action taken. Session history named as local and needing no migration |
| Rollback and communication | 5 | A point of no cheap return and what happens before it. A message to engineers with a deadline |
| Scope discipline | Deduction | Minus 5 for designing spend caps. Minus 5 for each product behavior asserted as fact that is not in the course material and not marked "to confirm" (maximum minus 15) |

Bands: 90 and above, ready to run. 75 to 89, ready after fixing the ordering or CI gaps. Below 75, rework before use.
