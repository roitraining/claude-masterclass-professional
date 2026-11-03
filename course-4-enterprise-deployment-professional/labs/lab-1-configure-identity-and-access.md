# Lab 1: Configure Identity and Access

**Course:** Claude Enterprise Deployment and Security Operations Professional
**Duration:** 90 minutes
**Format:** Instructor-led, in-class hands-on lab (300 level). Two paths — offline review, or live in the sandbox

> Part of **[Claude Enterprise Deployment and Security Operations Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

## Prerequisites

<!-- setup-ref:start -->
> **New to this course, or on a fresh machine?** Install and sign in to Claude Code first: **[Setup: Install and Sign In to Claude Code](../../SETUP-CLAUDE-CODE.md)**. About 10 minutes, Linux and Windows. Courses can be taken in any order, so this lab does not assume another course set it up.
>
> Already set up? Confirm with `claude --version` and `claude auth status`.
<!-- setup-ref:end -->
- [ ] Python 3.11 or later, for the offline scorer
- [ ] `$FILES/lab1-identity` from your instructor: `idp_sso_notes.md`, `group_mappings.csv`, `claude_groups.csv`, `custom_roles.json`, `offboarding_steps.csv`, `rollout_plan.csv`, `domains.csv`, `findings_lab1.json`, `check_lab1.py`
- [ ] Live path only: sandbox organization access and the printed menu map from your instructor
- [ ] Live path only: a browser that can open fresh private windows

> **Note:** anything in a tenant or a shared organization is instructor-only. The live path runs on an instructor-provisioned sandbox, never on a real organization.

---

## Overview

Northwind Example Corp is moving to an Enterprise organization using JIT. SCIM is not enabled. The role policy of the security team is in `idp_sso_notes.md`. The design is about to go live. **Your job is to review it before it does.**

**Choose one path.** Part 2 is the offline review, which everyone can do. Part 3 is the live sandbox configuration, which needs instructor-provisioned access. Do Part 1 either way, then one of Part 2 or Part 3, then Part 4.

---

## Part 1: Set Up and Read the Policy

### Step 1: Copy the Folder and Read the Role Policy

Copy `lab1-identity` to a working folder. Read `idp_sso_notes.md` **first** — it holds the role policy you are checking everything else against.

**Expected result:** you can state the maximum number of Owners the policy allows, and which provisioning mode is in use.

---

## Part 2: Offline Path — Review the Design

Everyone can do this path. If you are taking the live path instead, continue at Part 3.

### Step 2: Find Every Defect in the Configuration

**Hints:**

- Compare each mapping row with `claude_groups.csv`.
- Compare member counts with the role policy.
- Ask what happens at the next SSO login after a removal.
- Compare `rollout_plan.csv` with `domains.csv`.
- Read the access level of every permission in `custom_roles.json`.

**Expected result:** a list of suspected defects, each tied to a file and a row.

### Step 3: Correct the Files in Your Copy

**Acceptance criteria:**

- Every mapping that sends a person to a role has what that role needs to take effect under the provisioning mode in use.
- No role is mapped to a population broader than its policy allows.
- The offboarding procedure leaves a departed person unable to return at the next login.
- The rollout order is one that a security reviewer would accept for every email domain in use.
- The permissions of a custom role match its written description.
- Rows that are already correct are left unchanged.

> **Common Pitfall:** do not tidy a correct row. The checker penalizes changes to the Owner and Admin rows that were already right.

> **Common Pitfall:** `PLACEHOLDER-` permission ids are placeholders and UNVERIFIED. Do not treat them as real permission names.

### Step 4: Record Each Finding

Record each finding in `findings_lab1.json`: the file, the issue, and the fix.

**Acceptance criteria:** every defect you corrected has a matching recorded finding.

### Step 5: Score Yourself

```
python check_lab1.py <your-folder>
```

**Acceptance criteria:** each defect shown as found and fixed.

---

## Part 3: Live Path — Configure the Sandbox

Only if your instructor has provisioned sandbox access. Otherwise take Part 2.

### Step 6: Connect the Identity Provider and Provision a JIT User

**Acceptance criteria:** the domain is verified **before** SSO is enforced, and a JIT test user signs in with the User role.

> **Hint:** menu paths and permission names are not in this guide. Use the printed map your instructor gives you.

### Step 7: Create and Assign a Custom Role

**Acceptance criteria:** a second test user mapped to a custom role holds the scoped permissions and is refused an out-of-scope action. Owner membership is limited to named individuals.

> **Common Pitfall:** a test user who stays signed in keeps an old session. Use a fresh private window after every change.

### Step 8: Prove the Removal Gap

**Acceptance criteria:** a user removed only in Claude is shown to return at next login, and is then unassigned in the identity provider so the removal holds.

> **Note:** your instructor has pre-planted traps. They are listed in `live_path_scorecard.md`, which is instructor-only.

---

## Part 4: Checkpoint

### Step 9: Verify Your Progress

**Offline path:**

- [ ] `idp_sso_notes.md` read before any file was changed
- [ ] `check_lab1.py` shows each defect found **and** fixed
- [ ] Every finding recorded in `findings_lab1.json` with file, issue and fix
- [ ] Correct rows left untouched
- [ ] No `PLACEHOLDER-` id treated as a real permission name

**Live path:**

- [ ] The scorecard of the instructor is complete
- [ ] Domain verified before SSO enforcement
- [ ] A JIT test user signs in with the User role
- [ ] A custom-role user holds the scoped permissions and is refused an out-of-scope action
- [ ] Owner membership limited to named individuals
- [ ] A Claude-only removal demonstrated returning at next login, then closed in the identity provider

**Either path:**

- [ ] You can state in one sentence why a mapped user can have no permissions under JIT
- [ ] You can state in one sentence why a user removed only in Claude comes back

---

## Troubleshooting Reference

| Issue | Symptom | Solution |
|---|---|---|
| Role still has no effect | Mapping row looks correct but the user has no permissions | Under JIT the group has to exist in the organization with members before the role takes effect. Alternatively use SCIM directory sync, which this plan allows |
| Points lost on correct rows | Score drops after a tidy-up | Changing a correct Owner or Admin row is penalized. Leave correct rows alone |
| Rollout order rejected | A reviewer refuses the plan | A verification step placed after the enforce step is the wrong order. Verification comes first |
| Placeholder treated as real | Findings reference `PLACEHOLDER-` names as products | They are placeholders and UNVERIFIED. Flag the access level, not the name |
| Live path shows stale state | Changes appear not to apply | The test user is on an old session. Use a fresh private window after every change |

---

## Scoring Rubric (100 points)

| Item | Points |
|------|--------|
| D1 found (10) and fixed (10) | 20 |
| D2 found (10) and fixed (10) | 20 |
| D3 found (10) and fixed (10) | 20 |
| D4 found (10) and fixed (10) | 20 |
| D5 found (5) and fixed (5) | 10 |
| Correct rows left untouched | 10 |

---

## What You Built

In 90 minutes, you:

- Reviewed an identity design before it went live, against a written role policy rather than against your instincts
- Found the gap where a mapping looks correct and still leaves a user with no permissions, because the provisioning mode changes what a mapping needs
- Found the offboarding procedure that lets a departed person back in at the next SSO login
- Caught a custom role holding write access its own description did not claim
- Left the correct rows alone, which is a skill the checker deliberately tests

---

## What's Next

Lab 2, Pull Compliance Data and Set a Control, moves from who can sign in to what you can prove about their activity afterwards.

---

## Facilitator Notes

Answer key and where each trap is planted:

- **D1: JIT with a Custom role and no Claude group.** `group_mappings.csv`, row `claude-secops-analysts` (`claude_group` is `secops-analysts`, `provisioning` is JIT). `claude_groups.csv` has no `secops-analysts`. Fix: create the group with the custom role and add members, or move the mapping to SCIM directory sync (Enterprise only).
- **D2: Owner mapped too broadly.** `group_mappings.csv`, row `it-operations` (212 members, Owner). The policy in `idp_sso_notes.md` allows at most 5 named Owners. Decoy: `claude-owners` (3 members) is correct.
- **D3: Removal only in Claude.** `offboarding_steps.csv` has no IdP step. Under JIT a user removed only in Claude is added again at the next SSO login, so the person must also be unassigned in the IdP.
- **D4: Missing domain verification.** `rollout_plan.csv` has no verification step before SSO enforcement. `domains.csv` shows `northwind-labs.example.net` not verified. Decoy: `example.com` is verified.
- **D5 (bonus): the role exceeds its description.** `custom_roles.json`, `SecOps Read-Only Auditor` holds `PLACEHOLDER-MANAGE-MEMBERS` with `write` access.

`check_lab1.py` contains the answer logic: give it to students after they submit. It matches findings by keyword, so read borderline findings yourself.

Instructor note: the real custom-role permission names, the group picker, and seat-tier labels (`standard` and `premium` here are labels belonging to this exercise) are not in the verified facts. For the live path, rehearse the full sequence on the sandbox and plant the four traps in `live_path_scorecard.md`.

---

*Lab 1 Complete*
