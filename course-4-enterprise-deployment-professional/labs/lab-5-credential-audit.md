# Lab 5: Credential Audit (take-home)

**Course:** Claude Enterprise Deployment and Security Operations Professional
**Duration:** About 60 minutes
**Format:** Take-home lab, paper only — an audit report, no configuration changes

> Part of **[Claude Enterprise Deployment and Security Operations Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

## Prerequisites

- [ ] Labs 1 through 4 completed
- [ ] `$FILES/lab5-audit/harbor-org`: `README.md`, `org/` (`managed-settings.json`, `credentials_inventory.csv`, `hr_departures.csv`, `ci_secrets_inventory.csv`) and `repos/` (`billing-service`, `inventory-service`, `payments-gateway`, each with `.claude/` and a CI workflow)
- [ ] `$FILES/lab5-audit/findings-template.md` for your report
- [ ] No account or organization access needed. This lab produces a document

> **Note:** every secret in the tree is a fake, of the form `FAKE-KEY-DO-NOT-USE-NNNN`. Report the pattern, never the value.

---

## Overview

Harbor Example Co runs Claude Code in three repositories (`billing-service`, `inventory-service`, `payments-gateway`) and an organization-level managed settings file.

Useful background: migrating from Console to Enterprise means removing leftover Console credentials — API key variables and `apiKeyHelper` — and moving CI to a `claude setup-token` credential or keeping Console keys for automation. Secure credential storage uses Keychain on macOS and a mode-0600 file on Linux.

The findings template has one block per finding: file and line, what is wrong, risk, severity, fix, rotation step, and owner. It is followed by a "Not a finding" list, a priority order with reasons, and a rotation and ownership plan.

**One of the three repositories is clean.** Reporting it as defective costs points.

---

## Part 1: Read the Organization

### Step 1: Read the README and the Inventories Together

Read `harbor-org/README.md`, then the three inventories in `org/` side by side rather than one at a time.

**Expected result:** you know how many repositories there are, which credentials the organization thinks it has, and who has left the company.

> **Hint:** ask who owns each credential, how long it lives, and how many places share it. Those three questions find most of what is here.

---

## Part 2: Audit the Tree

### Step 2: Audit the Settings and Helper Scripts

Read every `.claude/settings.json` and any helper script it points at.

**Expected result:** you can say, for each repository, where a credential comes from at run time.

> **Common Pitfall:** a helper script is not automatically safer than a literal value. Read what the script actually does.

### Step 3: Audit the CI Workflows and the Secrets Inventory

Read the CI workflow file in each repository against `ci_secrets_inventory.csv`.

**Expected result:** you know which secret names appear in more than one place.

### Step 4: Cross-Check the Credentials Inventory Against HR Departures

Compare `credentials_inventory.csv` with `hr_departures.csv`, paying attention to expiry, last-used and last-rotated dates.

**Expected result:** you can name any credential whose owner is gone, and say whether it was used after they left.

---

> **Two findings can share one credential.** The shared CI secret and the
> departed owner's long-lived credential are **separate findings**, scored
> separately, even though they involve the same credential in the inventory.
> One is about **scope** — a secret used by more than one repository — and the
> other is about **ownership and lifecycle** — who holds it, whether it expires,
> whether it was rotated, and whether it was used after they left. Merging them
> into a single row loses the points for the one you did not state.

## Part 3: Write the Findings

### Step 5: Write One Finding Block per Issue

**Acceptance criteria:** each finding gives the file and line, why it is a risk, the severity, a fix, and a rotation step wherever a credential is involved.

> **Common Pitfall:** do not fix a hard-coded key by moving it to another file in the same repository. That changes the path, not the exposure.

> **Common Pitfall:** do not recommend a long-lived token as the replacement for a long-lived token.

### Step 6: List What Is Not a Finding, and Prioritize

**Acceptance criteria:** the clean repository is listed under "Not a finding", and every finding is ordered by priority with the reason stated.

---

## Part 4: Plan Rotation and Ownership

### Step 7: Write the Rotation and Ownership Plan

**Acceptance criteria:** a plan naming, for each credential involved, who owns it and how it gets rotated.

> **Key Insight:** removing a leaked credential from a file does not make it safe. Anything that was committed or shared must be rotated, not just deleted.

---

## Part 5: Checkpoint

### Step 8: Verify Your Progress

- [ ] At least five findings, each in the template block format
- [ ] Every finding gives a file and line
- [ ] Every finding states the risk and a severity
- [ ] Every finding gives a fix
- [ ] Every credential-related finding includes a rotation step
- [ ] No fix merely relocates a secret within the same repository
- [ ] No fix replaces a long-lived token with another long-lived token
- [ ] No placeholder value is reported as a real secret — the pattern is reported, not the value
- [ ] The clean repository appears under "Not a finding", not as a defect
- [ ] Findings are ordered by priority, each with a stated reason
- [ ] A rotation and ownership plan names an owner for every credential involved
- [ ] Anything you could not source is marked unverified rather than asserted

---

## Troubleshooting Reference

| Issue | Symptom | Solution |
|---|---|---|
| Placeholder reported as a breach | A finding quotes a `FAKE-KEY-DO-NOT-USE` value | Every secret here is fabricated. Report the pattern and the exposure, not the value |
| Fix does not reduce exposure | A key moved from settings into another tracked file | The repository is the exposure. Move it out of the repository and rotate it |
| Replacement is no better | A long-lived token recommended to replace a long-lived token | Choose a credential with a bounded lifetime, or a scoped CI credential |
| Clean repository flagged | Points lost on `payments-gateway` | It is the decoy and it is correct. List it under "Not a finding" |
| Rotation forgotten | Findings end at "remove the key" | A credential that has been committed or shared is compromised. Deleting it is not rotating it |

---

## Scoring Rubric (100 points)

| Item | Points |
|------|--------|
| Five planted issues, 14 each: identified (7), location (3), fix (4) | 70 |
| The clean repository is not reported as defective | 10 |
| Findings are prioritized with a stated reason | 10 |
| Rotation and ownership plan | 10 |

---

## What You Built

In about 60 minutes, you:

- Audited a multi-repository deployment by reading settings, helper scripts, CI workflows and two inventories against each other, rather than file by file
- Found the credential whose owner had already left, by crossing an inventory with an HR list
- Found the secret shared across repositories, which no single repository looks wrong on its own
- Left the clean repository alone, which an audit that pattern-matches for alarm would have flagged
- Paired every finding with a rotation step, because deleting a leaked credential does not make it safe

---

## What's Next

This is the final lab in Claude Enterprise Deployment and Security Operations Professional. The cross-reading habit is the one to keep: no single file in this tree looks wrong by itself.

---

## Facilitator Notes

The tree and `lab5-audit/facilitator/rubric.md` are built. Planted issues:

1. A key in a settings file — `billing-service/.claude/settings.json` sets an API key variable in `env`.
2. An `apiKeyHelper` script that only echoes a static key — `inventory-service/.claude/settings.json` points to `.claude/get_key.sh`.
3. A CI secret shared across repositories — the same secret name in the workflow files of `billing-service` and `inventory-service`, listed against both in a CI secrets inventory.
4. A long-lived OAuth token (from `claude setup-token`) owned by a person who has left, shown in a credentials inventory with no expiry and a last-used date after the departure date in the HR list.
5. Missing deny rules for `.env` — `inventory-service` has a `.env` and no `permissions.deny`.

Decoy: `payments-gateway` is clean (deny rules, a repository-scoped CI secret, no key in settings). All values are `FAKE-KEY-DO-NOT-USE-NNNN`.

Instructor note: the lifetime of a `claude setup-token` credential is not in the verified facts (UNVERIFIED). The inventory of the scenario states it as scenario data. Do not teach it as a product fact. The managed settings file in the tree may use `forceLoginOrgUUID` with an obviously fake UUID.

---

*Lab 5 Complete*
