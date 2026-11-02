# Lab 1: Configure Identity and Access

> Part of **[Claude Enterprise Deployment and Security Operations Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

**Learning objective:** Design SSO, JIT or SCIM provisioning, group mappings, and a custom role that enforces real scope limits, and find the provisioning and group defects that leave users without permissions or with too much. Time: 90 minutes.

**Files:** `$FILES/lab1-identity`: `idp_sso_notes.md`, `group_mappings.csv`, `claude_groups.csv`, `custom_roles.json`, `offboarding_steps.csv`, `rollout_plan.csv`, `domains.csv`, `findings_lab1.json`, `check_lab1.py`, `live_path_scorecard.md` (instructor).

**Context:** Northwind Example Corp is moving to an Enterprise organization using JIT. SCIM is not enabled. The security team's role policy is in `idp_sso_notes.md`. The design is about to go live. Your job is to review it before it does.

**Steps (offline path):**

1. Copy `lab1-identity` to a working folder. Read `idp_sso_notes.md` first: it holds the role policy you are checking against.
2. **Goal:** find every defect in the provided configuration and correct it in your copies of the files.
3. **Acceptance criteria:**
   - Every mapping that sends a person to a role has what that role needs to take effect under the provisioning mode in use.
   - No role is mapped to a population broader than its policy allows.
   - The offboarding procedure leaves a departed person unable to return at the next login.
   - The rollout order is one that a security reviewer would accept for every email domain in use.
   - A custom role's permissions match its written description.
   - Rows that are already correct are left unchanged.
4. **Hints:** Compare each mapping row with `claude_groups.csv`. Compare member counts with the role policy. Ask what happens at the next SSO login after a removal. Compare `rollout_plan.csv` with `domains.csv`. Read the access level of every permission in `custom_roles.json`.
5. Record each finding in `findings_lab1.json`: the file, the issue, and the fix.
6. Score yourself: `python check_lab1.py <your-folder>`

**Steps (live path):**

1. **Goal:** in the sandbox organization, connect the identity provider, provision a test user through JIT, create a custom role, and assign it so a test user holds exactly the scoped permissions.
2. **Acceptance criteria:** the domain is verified before SSO is enforced; a JIT test user signs in with the User role; a second test user mapped to a custom role has the scoped permissions and is refused an out-of-scope action; Owner membership is limited to named individuals; a user removed only in Claude is shown to return at next login and is then unassigned in the IdP.
3. **Hints:** the instructor has pre-planted traps (see `live_path_scorecard.md`). Menu paths and permission names are not in this guide: use the printed map the instructor gives you.

**Checkpoint:** Offline: `check_lab1.py` shows each defect found and fixed. Live: the instructor's scorecard is complete. Either way you can state, in one sentence each, why a mapped user can have no permissions under JIT and why a user removed only in Claude comes back.

**Common problems:**

- Fixing the mapping row but not the group: under JIT, the group has to exist in the organization with members before the role takes effect. Alternatively use SCIM directory sync, which this plan allows.
- Changing a correct row (Owner or Admin) to look tidy: the checker penalizes that.
- Adding a verification step after the enforce step: the order matters.
- Treating `PLACEHOLDER-` permission ids as real names: they are placeholders and UNVERIFIED.
- Live path: the test user stays signed in with an old session. Use a fresh private window after every change.

**Scoring rubric (100):**

| Item | Points |
|------|--------|
| D1 found (10) and fixed (10) | 20 |
| D2 found (10) and fixed (10) | 20 |
| D3 found (10) and fixed (10) | 20 |
| D4 found (10) and fixed (10) | 20 |
| D5 found (5) and fixed (5) | 10 |
| Correct rows left untouched | 10 |

**Facilitator note:** Answer key and where each trap is planted:

- **D1: JIT with a Custom role and no Claude group.** `group_mappings.csv`, row `claude-secops-analysts` (`claude_group` is `secops-analysts`, `provisioning` is JIT). `claude_groups.csv` has no `secops-analysts`. Fix: create the group with the custom role and add members, or move the mapping to SCIM directory sync (Enterprise only).
- **D2: Owner mapped too broadly.** `group_mappings.csv`, row `it-operations` (212 members, Owner). The policy in `idp_sso_notes.md` allows at most 5 named Owners. Decoy: `claude-owners` (3 members) is correct.
- **D3: Removal only in Claude.** `offboarding_steps.csv` has no IdP step. Under JIT a user removed only in Claude is added again at the next SSO login, so the person must also be unassigned in the IdP.
- **D4: Missing domain verification.** `rollout_plan.csv` has no verification step before SSO enforcement. `domains.csv` shows `northwind-labs.example.net` not verified. Decoy: `example.com` is verified.
- **D5 (bonus): the role exceeds its description.** `custom_roles.json`, `SecOps Read-Only Auditor` holds `PLACEHOLDER-MANAGE-MEMBERS` with `write` access.

`check_lab1.py` contains the answer logic: give it to students after they submit. It matches findings by keyword, so read borderline findings yourself. Instructor note: the real custom-role permission names, the group picker, and seat-tier labels (`standard` and `premium` here are the exercise's own labels) are not in the verified facts. For the live path, rehearse the full sequence on the sandbox and plant the four traps in `live_path_scorecard.md`.
