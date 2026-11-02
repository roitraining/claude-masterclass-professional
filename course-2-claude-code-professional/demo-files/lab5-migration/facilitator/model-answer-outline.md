# Lab 5 model answer outline (facilitator only)

Traps in the scenario and what a strong runbook does about each:

1. Reporting export before anything else. Console analytics and API keys do not carry over, and removing people from Console loses their view. Finance needs 12 months by key and workspace, so export first and name the recipient.
2. `forceLoginOrgUUID` too early. If it is set before seats are provisioned and synced, people cannot sign in. Provision and sync, confirm a pilot user, then set it.
3. The contractors. Six people are not in the identity provider. A good answer picks one of: add them to the provider, give them seats another way if the course material supports it (write "to confirm"), or exclude them and keep a separate path with an end date. It also says unmanaged personal laptops cannot be forced by endpoint management, and says what server-managed delivery could cover. Do not accept a claim that managed settings reach a laptop the company does not manage unless the student marks the mechanism "to confirm".
4. C5. A subscription token made with `claude setup-token` is tied to one person's subscription. Two belong to a person leaving in four weeks and one to a contractor. Replace them before those people go. For the 14-repository organization secret, the guidance is an API key, not an OAuth token.
5. Console organization. The verified steps remove migrated users from the Console organization, and keep Console keys as an option for automation. A strong answer keeps the Console organization (and the C3 and C4 keys) for CI until each pipeline has moved and passed a test, and says which pipelines stay on Console keys by choice.
6. Leftover credentials. C1 and C2 mean `ANTHROPIC_API_KEY` in shell profiles and `apiKeyHelper` in six repositories' settings. Remove them, then `/login`, choose the Enterprise organization, and verify with `/status`. `demo-files/demo9-cutover/leftover_credentials_check.py` can list the names on a laptop without printing values.
7. Order inside the window: export, provision and sync, pilot two users, set `forceLoginOrgUUID`, roll to everyone with the sign-in and verify steps, move CI and test it, then remove users from Console last.
8. Out of scope. Spend caps. Deduct if the student designs them.

Unconfirmed items you may meet in answers (mark as "to confirm" and do not give credit for stating them as fact): contribution-metric definitions and how they attach to GitHub, spend-alert thresholds, pooled group budgets, and GitLab mention-driven trigger setup beyond the documented webhook pattern.
