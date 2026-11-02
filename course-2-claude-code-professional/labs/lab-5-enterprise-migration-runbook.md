# Lab 5 (take-home): Enterprise Migration Runbook

> Part of **[Claude Code Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

**Learning objective:** Draft the cutover plan for a fictional team moving from Console to Enterprise, covering identity, roles, managed settings, credentials, CI, and export of Console reporting. Time: about 60 minutes at home.

**Files:** `$FILES/lab5-migration`: `scenario-sheet.md`, `runbook-template.md`, `rubric.md`.

**Context:** The scenario sheet describes Larkspur Freight Software: team size, an identity provider, CI on GitHub Actions and GitLab, managed settings needs, and five credentials in use. You write the runbook a teammate could run on cutover day. The steps come from the course: provision seats and SCIM group mappings and sync; confirm Claude Code is enabled and set `forceLoginOrgUUID` in managed settings; remove leftover Console credentials such as API key variables and `apiKeyHelper`; `/login`, choose the Enterprise organization, and verify with `/status`; move CI to a `claude setup-token` credential or keep Console keys for automation; remove migrated users from the Console organization. Analytics and API keys do not carry over, so export Console reporting first. CLI session history is local and needs no migration. Spend limits are out of scope. This lab is about the order of the steps and what breaks if you do them early.

**Steps:**

1. Read `scenario-sheet.md` and list every constraint and every trap you can find, before you write.
2. Fill in `runbook-template.md`. Goal: a runbook that is exact about order, owner, time and the check that proves each step.
3. Score it yourself against `rubric.md`. Fix the lowest area.
4. Optional: bring it to the next session, or send it to your instructor.

Acceptance criteria and hints:

- Every credential C1 to C5 has a decision, a reason and a step.
- Every ordering in the plan has its reason stated. Ask, for each step, what fails if it runs first.
- Where you need a product detail you cannot source, write "to confirm". Do not invent product behavior or role names.
- Ask which credentials are tied to a person, and what happens when that person leaves.
- Ask what a subscription token is tied to, and whether it fits a secret shared by 14 repositories.
- Ask what you can enforce on a laptop the company does not manage.

**Checkpoint:** A completed runbook that scores at least 75 on the rubric.

**Common problems:**

- A runbook that lists tasks and no order: the rubric gives its largest share to order and reasons.
- A plan that removes users from Console first: reporting is lost and CI can break.
- A plan that locks sign-in to the Enterprise organization before seats are provisioned and synced: people cannot sign in.
- A plan that leaves `ANTHROPIC_API_KEY` or `apiKeyHelper` in place: an old credential can keep working instead of the new sign-in.
- A plan that designs spend caps: out of scope here.

**Scoring rubric:** See `rubric.md`. It is out of 100, with deductions for scope creep and for unsourced claims presented as fact.

**Facilitator note:** `facilitator/model-answer-outline.md` lists the traps and what a strong answer does. The traps are: the export must come first, the sign-in lock must follow provisioning, the contractors are not in the identity provider and use unmanaged laptops, three tokens are tied to people who are leaving or are contractors, an organization-wide secret should be an API key, the Console organization may need to stay for CI until each pipeline has moved, and leftover credentials must go. Instructor-only: any demonstration in a tenant or an organization. This lab is paper only.

Some ordering reasons in the rubric are operational reasoning about what fails if a step runs early. The verified facts list the steps and what does not carry over. They do not list failure behavior, so do not present that reasoning as product documentation. Unconfirmed items students may meet: contribution-metric definitions and how they attach to GitHub, spend-alert thresholds, pooled group budgets, and GitLab mention-driven trigger setup beyond the documented webhook pattern. Mark answers that state these as fact.

For students who want to check a laptop in their own life, `$FILES/demo9-cutover/leftover_credentials_check.py` lists the names of leftover credentials without printing values.
