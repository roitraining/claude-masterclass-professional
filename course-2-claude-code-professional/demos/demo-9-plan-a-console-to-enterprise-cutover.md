# Demo 9: Plan a Console to Enterprise Cutover

**Course:** Claude Code Professional: Pipelines, Plugins and Enterprise Operations (Claude MasterClass Professional, Course 2)
**Demo:** 9 of 9
**Time:** about 15 minutes

> Part of **[Claude Code Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Walk the cutover steps for a fictional team in the right order, and say what breaks if a step happens early. Time: about 15 minutes.

**Files:** [`$FILES/demo9-cutover/cutover-checklist.md`](../demo-files/demo9-cutover/cutover-checklist.md), `managed-settings-snippet.json`, `leftover_credentials_check.py`.

**Context:** In a move from Console to Enterprise, identity moves to the identity provider, and seats are assigned through SCIM group mappings. The steps are: provision seats and SCIM mappings and sync; confirm Claude Code is enabled and set `forceLoginOrgUUID` in managed settings; remove leftover Console credentials; `/login`, choose the Enterprise organization, and verify with `/status`; move CI to a `claude setup-token` credential or keep Console keys for automation; remove migrated users from the Console organization. Analytics and API keys do not carry over, so export Console reporting first. CLI session history is local and needs no migration. Spend limits are covered in Professional 4, not here.

**Steps:**

1. Open `cutover-checklist.md`. Introduce Harbor Lane Studios: 12 engineers, a SAML provider, two repositories running Claude in Actions.
2. Fill the table with the class, one row at a time. For each row ask what breaks if it runs earlier.
3. Show `managed-settings-snippet.json` and say the id is a placeholder.
4. Show leftover credentials. In a throwaway shell:

```
export ANTHROPIC_API_KEY="FAKE-TOKEN-DO-NOT-USE"
python $FILES/demo9-cutover/leftover_credentials_check.py
unset ANTHROPIC_API_KEY
```

   The check lists names only, never values.
5. Show how a person verifies: `/login`, choose the Enterprise organization, then `/status`. `claude auth status --text` also shows how the session is authenticated.
6. In the ROI sandbox tenant, if available, show where seats and group mappings are configured. The instructor only.
7. State what is out of scope: caps and the wider policy decision.

**Expected result:** The class produces an order with reasons: export first, provision and sync, pilot, lock sign-in, remove leftover credentials, verify, move CI, and remove users from Console last. They name what does not carry over.

**Instructor note:** Instructor and sandbox tenant only. Which screens hold the seat and mapping settings is not in the verified facts, so step 6 needs rehearsal, and a screenshot set is the fallback. The "what breaks if it runs early" reasons are operational reasoning, not documented product behavior, so label them as reasoning. Contribution-metric definitions, spend-alert thresholds and pooled group budgets are unconfirmed. Do not teach them.

**Why this matters:** The risk in a migration is order. A correct list in the wrong order locks people out, loses reporting or breaks a nightly pipeline.

---

**Previous:** [Demo 8: Wire In a Language Server](demo-8-wire-in-a-language-server.md)


*Demo 9 of 9*
