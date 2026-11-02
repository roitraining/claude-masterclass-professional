# Lab 1 Live Path Scorecard (instructor use)

The live path runs on an instructor-provisioned sandbox Claude organization (Enterprise) and an identity provider test environment. Students work from the goal and acceptance criteria in `labs/lab-1-configure-identity-and-access.md`. Menu paths and exact labels are not listed here because they are not in the verified course facts: rehearse them on the sandbox before class and give students a printed map.

## Pre-planted traps (set these up before class)

| Trap | How to plant it |
|------|-----------------|
| T1 No permissions after JIT | In the IdP, assign a test group (for example `claude-secops-analysts`) to the Anthropic app and map it to the Custom role, but do not create the matching group in the Claude organization. The first test user signs in with no permissions. |
| T2 Broad Owner mapping | Pre-map a large IdP group to Owner in the starting configuration. Students must notice it. |
| T3 Removal only in Claude | Provide a test user who is removed in Claude only. At the next SSO login the user is added again. |
| T4 Domain not verified | Give each student pair a second test domain that has no verification record. |

## Scorecard (100)

| Check | Points |
|-------|--------|
| Domain verification completed (or the missing step identified) before SSO is enforced | 20 |
| JIT test user signs in and receives the User role | 10 |
| T1 found, cause named (no Claude group), and fixed (group created and user added, or SCIM directory sync used where the plan allows) | 20 |
| Custom role contains only the read-only permissions the brief allows, and a test user cannot perform an out-of-scope action | 20 |
| T2 found and Owner membership reduced to named individuals | 10 |
| T3 shown: user removed in Claude only is re-added at next login, then unassigned in the IdP and stays out | 20 |

If the sandbox is unavailable on the day, move the student to the offline path. Do not mix scores.
