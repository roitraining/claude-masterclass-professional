# Lab 5 Rubric (100 points) and Answer Key

Instructor use. Hold back until the audit is submitted.

## Planted issues (14 points each: identified 7, location 3, fix 4)

| Id | Issue | Where | Acceptable fix |
|----|-------|-------|----------------|
| C1 | A key in a settings file | `repos/billing-service/.claude/settings.json`, `env.ANTHROPIC_API_KEY` | Remove it and rotate it. Supply credentials at run time from a secret store or the user's own login. Do not move it to another file in the repository. |
| C2 | An `apiKeyHelper` that only echoes a static key | `repos/inventory-service/.claude/get_key.sh` (referenced by `.claude/settings.json`) | The helper must fetch a short-lived credential from a broker or secret store. A static echo is just a key in a script. Rotate the key. |
| C3 | A CI secret shared across repositories | `org/ci_secrets_inventory.csv` (`SHARED_CLAUDE_CI_KEY` for two repositories) and the two `claude-review.yml` files | One repository-scoped secret per repository, each with its own owner and rotation date. |
| C4 | A credential owned by a person who left, still live and never rotated | `org/credentials_inventory.csv` `cred-101` (owner `p.nakamura@example.org`, never rotated, used 2026-10-09 — about 3.5 months after the 2026-06-30 departure in `org/hr_departures.csv`) | Revoke `cred-101`, re-issue under a team-owned identity, rotate the CI secrets it backs, and add a credential-revocation step to offboarding. **The defect is ownership and rotation, not lifetime:** `cred-101` and the clean `cred-102` have the same one-year lifetime, so an expiry still ~3.7 months away is not what makes this one bad — nobody owns it and nobody has ever rotated it. A student who replaces it with another one-year team-owned token has answered correctly; the Checkpoint's "no long-lived token replacing a long-lived token" is about an *unscoped, unrotated* credential, and the fix must name an owner and a rotation date. |
| C5 | Missing deny rules for `.env` | `repos/inventory-service/.claude/settings.json` has no `permissions.deny`, and the repository has a `.env` | Add `Read` deny rules for `.env` and `.env.*`. Note a deny rule matches the command as written, so add sandbox isolation for reads through other commands. |

## Other points

| Item | Points |
|------|--------|
| `payments-gateway` is not reported as defective (it is the clean repository) | 10 |

> **Defending the clean repository.** `cred-102` is team-owned (`payments-team@example.org`), its expiry (2027-08-20) is one year from creation as a `setup-token` credential should be, its CI secret is repository-scoped, and its workflow supplies the token through `CLAUDE_CODE_OAUTH_TOKEN`, which is the correct variable for a `setup-token` credential. Its `last_rotated` equals its `created` date, which is normal for a credential inside its first rotation period, not a defect. A student who argues that a setup token is person-tied in principle is reasoning correctly; the distinction here is **ownership and lifecycle**: team-owned, scoped and rotatable, against `cred-101` which is person-owned, never rotated, and used after its owner left. Do not deduct for a student who asks the question and then concludes the repository is clean.

> **C3 and C4 score separately** even though both involve `cred-101`'s CI use.
> C3 is the shared scope across two repositories; C4 is the departed owner, the
> never-rotated credential and the use after departure. A student who merges them into one
> finding has stated only one of the two problems. Award the row they stated and
> note the merge; the lab now warns against it explicitly.

| Findings are prioritized with a stated reason (suggested order: C4, C3, C1, C2, C5, because C4 is a live credential tied to a former employee and C3 has the widest reach) | 10 |
| Rotation and ownership plan covers every credential involved | 10 |

## Notes

- A `claude setup-token` credential is a **one-year OAuth token**, and the authentication documentation says to supply it through `CLAUDE_CODE_OAUTH_TOKEN`. `ANTHROPIC_API_KEY` is for Console API keys. Both setup-token credentials in the inventory now carry a one-year expiry and all three workflows use the correct variable, so a student who notices the variable is right and finds nothing wrong — do not expect it as a finding and do not deduct either way. (Before 2026-11-11 this note said the lifetime was UNVERIFIED and `cred-101` had no expiry, which contradicted the product and made the clean repository look misconfigured.)
- `billing-service` has correct `.env` deny rules: reporting it for C5 is a false positive.
