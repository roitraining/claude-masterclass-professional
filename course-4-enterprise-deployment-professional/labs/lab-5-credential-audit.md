# Lab 5: Credential Audit (take-home)

> Part of **[Claude Enterprise Deployment and Security Operations Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

**Learning objective:** Independently audit a sample organization's Claude Code deployment for credential and secret hygiene issues, and write each finding with a fix. Time: about 60 minutes, take-home.

**Files:** `$FILES/lab5-audit/harbor-org`: `README.md`, `org/` (`managed-settings.json`, `credentials_inventory.csv`, `hr_departures.csv`, `ci_secrets_inventory.csv`) and `repos/` (`billing-service`, `inventory-service`, `payments-gateway`, each with `.claude/` and a CI workflow). Instructor only: `$FILES/lab5-audit/rubric.md`. Use `$FILES/lab5-audit/findings-template.md` for your findings. It has one block per finding: file and line, what is wrong, risk, severity, fix, rotation step, and owner, followed by a "Not a finding" list, a priority order with reasons, and a rotation and ownership plan.

**Context:** Harbor Example Co runs Claude Code in three repositories (`billing-service`, `inventory-service`, `payments-gateway`) and an organization-level managed settings file. Useful background: migrating from Console to Enterprise means removing leftover Console credentials (API key variables and `apiKeyHelper`) and moving CI to a `claude setup-token` credential or keeping Console keys for automation. Secure credential storage uses Keychain on macOS and a mode-0600 file on Linux.

**Steps:**

1. **Goal:** find every credential hygiene issue in the tree and write a finding for each with a fix.
2. **Acceptance criteria:** each finding gives the file and line, why it is a risk, the severity, a fix, and a rotation step where a credential is involved; the clean repository is not reported as defective; findings are ordered by priority.
3. **Hints:** read settings files, helper scripts, CI workflow files, a credentials inventory, and an HR departures list together. Ask who owns each credential, how long it lives, and how many places share it.

**Checkpoint:** A findings report with at least five findings, a fix for each, and a rotation plan.

**Common problems:**

- Flagging a placeholder as if it were real: every secret in the tree is a fake. Report the pattern, not the value.
- Fixing a hard-coded key by moving it to another file in the same repository.
- Recommending a long-lived token as the replacement for a long-lived token.
- Forgetting rotation: removing a leaked credential from a file does not make it safe.

**Scoring rubric (100):**

| Item | Points |
|------|--------|
| Five planted issues, 14 each: identified (7), location (3), fix (4) | 70 |
| The clean repository is not reported as defective | 10 |
| Findings are prioritized with a stated reason | 10 |
| Rotation and ownership plan | 10 |

**Facilitator note:** The tree and `lab5-audit/rubric.md` are built. Planted issues: (1) a key in a settings file (`billing-service/.claude/settings.json` sets an API key variable in `env`); (2) an `apiKeyHelper` script that only echoes a static key (`inventory-service/.claude/settings.json` points to `.claude/get_key.sh`); (3) a CI secret shared across repositories (the same secret name in the workflow files of `billing-service` and `inventory-service`, listed against both in a CI secrets inventory); (4) a long-lived OAuth token (from `claude setup-token`) owned by a person who has left, shown in a credentials inventory with no expiry and a last-used date after the departure date in the HR list; (5) missing deny rules for `.env` (`inventory-service` has a `.env` and no `permissions.deny`). Decoy: `payments-gateway` is clean (deny rules, a repository-scoped CI secret, no key in settings). All values are `FAKE-KEY-DO-NOT-USE-NNNN`. Instructor note: the lifetime of a `claude setup-token` credential is not in the verified facts (UNVERIFIED). The scenario's inventory states it as scenario data. Do not teach it as a product fact. The managed settings file in the tree may use `forceLoginOrgUUID` with an obviously fake UUID.
