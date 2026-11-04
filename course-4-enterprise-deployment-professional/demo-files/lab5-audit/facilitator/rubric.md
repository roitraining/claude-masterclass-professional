# Lab 5 Rubric (100 points) and Answer Key

Instructor use. Hold back until the audit is submitted.

## Planted issues (14 points each: identified 7, location 3, fix 4)

| Id | Issue | Where | Acceptable fix |
|----|-------|-------|----------------|
| C1 | A key in a settings file | `repos/billing-service/.claude/settings.json`, `env.ANTHROPIC_API_KEY` | Remove it and rotate it. Supply credentials at run time from a secret store or the user's own login. Do not move it to another file in the repository. |
| C2 | An `apiKeyHelper` that only echoes a static key | `repos/inventory-service/.claude/get_key.sh` (referenced by `.claude/settings.json`) | The helper must fetch a short-lived credential from a broker or secret store. A static echo is just a key in a script. Rotate the key. |
| C3 | A CI secret shared across repositories | `org/ci_secrets_inventory.csv` (`SHARED_CLAUDE_CI_KEY` for two repositories) and the two `claude-review.yml` files | One repository-scoped secret per repository, each with its own owner and rotation date. |
| C4 | A long-lived credential owned by a person who left | `org/credentials_inventory.csv` `cred-101` (owner `p.nakamura@example.org`, no expiry, never rotated, used after the 2026-06-30 departure in `org/hr_departures.csv`) | Replace under a team-owned identity, revoke `cred-101`, set an expiry, add a departure step to offboarding. |
| C5 | Missing deny rules for `.env` | `repos/inventory-service/.claude/settings.json` has no `permissions.deny`, and the repository has a `.env` | Add `Read` deny rules for `.env` and `.env.*`. Note a deny rule matches the command as written, so add sandbox isolation for reads through other commands. |

## Other points

| Item | Points |
|------|--------|
| `payments-gateway` is not reported as defective (it is the clean repository) | 10 |

> **Defending the clean repository.** `cred-102` is team-owned (`payments-team@example.org`) and has an expiry (2027-02-20). Its `last_rotated` equals its `created` date, which is normal for a credential inside its first rotation period, not a defect. Contrast it with `cred-101`, which is person-owned, never expires and has never been rotated. A student who argues that a setup token is person-tied in principle is reasoning correctly; the distinction here is **ownership and expiry**: team-owned with an expiry, against `cred-101` which is person-owned, never expires, has never been rotated, and was used after its owner left. Do not deduct for a student who asks the question and then concludes the repository is clean.

> **C3 and C4 score separately** even though both involve `cred-101`'s CI use.
> C3 is the shared scope across two repositories; C4 is the departed owner, the
> missing expiry and the use after departure. A student who merges them into one
> finding has stated only one of the two problems. Award the row they stated and
> note the merge; the lab now warns against it explicitly.

| Findings are prioritized with a stated reason (suggested order: C4, C3, C1, C2, C5, because C4 is a live credential tied to a former employee and C3 has the widest reach) | 10 |
| Rotation and ownership plan covers every credential involved | 10 |

## Notes

- The lifetime of a `claude setup-token` credential is not in the course's verified facts (UNVERIFIED). The `none` expiry in the inventory is scenario data. Do not teach it as a product fact.
- `billing-service` has correct `.env` deny rules: reporting it for C5 is a false positive.
