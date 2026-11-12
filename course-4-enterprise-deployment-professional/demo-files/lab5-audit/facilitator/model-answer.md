# Lab 5 model answer (instructor only)

A full worked answer in the student's own template, written 2026-11-12 by doing the lab
from the student pack. Use it to calibrate marking, not as the only acceptable wording —
the rubric scores *identified / location / fix*, not phrasing.

Audit date is **2026-10-12** (`harbor-org/README.md`). Harbor's policy, from the same
file: named owner, re-issue to a team when the owner leaves, rotate at least every 180
days, CI secrets scoped to one repository.

---

## Finding 1 — C4

- **File and line:** `org/credentials_inventory.csv` line 2 (`cred-101`), read against
  `org/hr_departures.csv` line 2
- **What is wrong:** `cred-101` is owned by `p.nakamura@example.org`, whose last day was
  2026-06-30. It has never been rotated (created 2026-02-02, so 252 days old at the
  audit against a 180-day policy) and was last used 2026-10-09 — 101 days after its
  owner left.
- **Risk:** a live credential tied to a person with no current relationship to the
  company. Use after departure cannot be attributed to anyone accountable, and
  offboarding plainly did not revoke it, so the same gap applies to the next leaver.
- **Severity:** high
- **Fix:** revoke `cred-101`. Re-issue under a team identity, and add "revoke or re-issue
  every credential the leaver owns" to the offboarding checklist.
- **Rotation step:** revoke immediately; issue the replacement into the CI secret store
  and set a 180-day rotation.
- **Owner:** a team address, e.g. `platform-team@example.org`. Not an individual.

## Finding 2 — C3

- **File and line:** `org/ci_secrets_inventory.csv` line 2 (`SHARED_CLAUDE_CI_KEY`,
  scope `organization`, repositories `billing-service;inventory-service`), used at
  `repos/billing-service/.github/workflows/claude-review.yml` line 10 and
  `repos/inventory-service/.github/workflows/claude-review.yml` line 10
- **What is wrong:** one secret, organization-scoped, serving two repositories, backed by
  a single credential (`cred-101`) that has never been rotated.
- **Risk:** blast radius. A compromise in either repository exposes the other, use cannot
  be attributed to a repository, and rotating it breaks two pipelines at once — which is
  how a secret ends up never rotated.
- **Severity:** high
- **Fix:** one repository-scoped secret per repository, each backed by its own
  credential with its own owner and rotation date. `payments-gateway` already shows the
  pattern (`CLAUDE_CI_TOKEN_PAYMENTS`, scope `repository`).
- **Rotation step:** mint two new credentials, set one repository secret in each repo,
  then revoke `cred-101`.
- **Owner:** the owning team of each repository.

> **C3 and C4 are separate findings** even though both involve `cred-101`. C3 is scope;
> C4 is ownership and lifecycle. A merged row scores one of the two.

## Finding 3 — C1

- **File and line:** `repos/billing-service/.claude/settings.json` line 3
  (`env.ANTHROPIC_API_KEY`)
- **What is wrong:** a literal credential of the form `FAKE-KEY-DO-NOT-USE-NNNN` is
  committed in a tracked settings file and injected as `ANTHROPIC_API_KEY`.
- **Risk:** anyone with read access to the repository has the credential, and it is in
  git history, so deleting the line does not remove it. `ANTHROPIC_API_KEY` also outranks
  a developer's own sign-in, so every session opened in this repository silently bills
  against this key rather than the person using it.
- **Severity:** high
- **Fix:** delete the `env` block. Supply the credential at run time from the secret
  store in CI, or let developers use their own sign-in locally. Moving it to another
  tracked file in the same repository changes the path, not the exposure.
- **Rotation step:** treat as compromised. Revoke and re-issue into the secret store.
- **Owner:** the `billing-service` team. **Note: this credential is not in
  `credentials_inventory.csv` — see "Findings about the inventory itself" below.**

## Finding 4 — C2

- **File and line:** `repos/inventory-service/.claude/settings.json` line 2
  (`apiKeyHelper`) → `repos/inventory-service/.claude/get_key.sh` line 3
- **What is wrong:** the helper does nothing but `echo` a literal key. An `apiKeyHelper`
  implies a credential fetched at run time from somewhere trusted; this is a hard-coded
  key with an extra file in front of it.
- **Risk:** identical exposure to a key in a settings file, plus false assurance — a
  reviewer scanning for literal keys in `settings.json` sees a helper and moves on.
- **Severity:** high
- **Fix:** the helper must fetch a short-lived credential from a secret store or broker
  and return it on stdout. Remove the literal from the script.
- **Rotation step:** treat as compromised; revoke and re-issue. The script is committed,
  so history retains the value.
- **Owner:** the `inventory-service` team. **Also not in the inventory.**

## Finding 5 — C5

- **File and line:** `repos/inventory-service/.claude/settings.json` lines 3–5
  (`permissions` has only `allow`), with `repos/inventory-service/.env` lines 1–2 present
  in the repository
- **What is wrong:** the repository contains a `.env` holding two secrets and has no
  `permissions.deny`. Both other repositories deny `Read(./.env)` and `Read(./.env.*)`.
- **Risk:** Claude Code can read the secrets file straight into context.
- **Severity:** medium — exposure needs a read to happen, and there is no evidence one
  did, which is what separates it from the four above.
- **Fix:** add `Read(./.env)` and `Read(./.env.*)` to `permissions.deny`. A deny rule
  matches the command as written, so a shell command that reads the file another way is
  not covered — pair it with sandbox `filesystem.denyRead` as `payments-gateway` does.
- **Rotation step:** the two values in `.env` are committed to the repository, so rotate
  both regardless of whether anything read them.
- **Owner:** the `inventory-service` team.

---

## Not a finding

- **`payments-gateway` — the clean repository.** Deny rules cover `.env`, `.env.*`,
  `secrets/**` and the network commands; the sandbox is on and set to fail closed; no
  credential appears in settings; its CI secret `CLAUDE_CI_TOKEN_PAYMENTS` is scoped to
  one repository; its credential `cred-102` is team-owned, inside its lifetime and
  rotated 53 days before the audit; and the workflow supplies a `setup-token` credential
  through `CLAUDE_CODE_OAUTH_TOKEN`, which is the correct variable for that credential
  kind.
- **`j.alvarez@example.org`**, departed 2026-03-15, owns no credential in the inventory.
  Offboarding worked in that case — which is what makes `cred-101` a lapse rather than a
  policy that never existed.
- **`org/managed-settings.json`** pins `forceLoginOrgUUID`. That is a control, and the
  UUID is an obvious placeholder, not a secret.
- **`cred-103`** expires 2026-11-02, 21 days after the audit, and was rotated 163 days
  ago — inside the 180-day policy. Not a defect; it belongs in the rotation plan as work
  to schedule, not in the findings.

## Priority order

1. **C4** — a live credential belonging to someone who left four months ago, still in use.
   Nothing else here is being actively used by an unaccountable holder.
2. **C3** — widest blast radius and the reason C4 was never rotated.
3. **C1** — a committed literal that also silently redirects every developer session's
   billing.
4. **C2** — the same exposure as C1, ranked below it only because it bills nobody by
   surprise; its false assurance makes it likelier to survive the next review.
5. **C5** — real, but exposure requires a read and none is evidenced.

## Rotation and ownership plan

| Credential | Owner | Lifetime | Where used | Rotation | If the owner leaves |
|---|---|---|---|---|---|
| `cred-101` | currently p.nakamura (departed) → re-issue to `platform-team` | one year, to 2027-02-02 | CI for billing-service and inventory-service | **never rotated — revoke now**, then 180 days | revoke on last day; this is the step that failed |
| `cred-102` | `payments-team@example.org` | one year, to 2027-08-20 | CI for payments-gateway | 2026-08-20, next by 2027-02-16 | team-owned, so no single leaver breaks it |
| `cred-103` | `platform-team@example.org` | to 2026-11-02 | nightly report job | 2026-05-02; **expires in 21 days — schedule now** | team-owned |
| billing-service settings key | unassigned — **not in the inventory** | unknown | every session opened in that repo | revoke on discovery | no owner to ask |
| inventory-service helper key | unassigned — **not in the inventory** | unknown | every session opened in that repo | revoke on discovery | no owner to ask |

---

## Findings about the inventory itself

Worth drawing out in the debrief, and **not currently scored**:

The organization believes it has three credentials. The tree contains **five**. The two
that are provably exposed — the literal in `billing-service/.claude/settings.json` and
the one `get_key.sh` echoes — appear in no inventory, have no owner, no expiry and no
rotation date. That is the realistic shape of this problem: the credentials an
organization tracks are rarely the ones that leak, and an audit that only reconciles the
inventory against HR would have found C4 and missed C1 and C2 entirely.

A student who notices this is reasoning better than the rubric asks for. Credit it in the
rotation plan.
