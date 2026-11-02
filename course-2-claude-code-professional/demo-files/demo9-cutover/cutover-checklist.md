# Demo 9: Console to Enterprise cutover, fill-in checklist

The instructor fills this in live for a fictional team of 12 engineers. Placeholders only. No real organization identifiers.

Team: Harbor Lane Studios, 12 engineers, one SAML identity provider, one GitHub organization, two repositories running `claude-code-action` with a Console API key in a repository secret.

| Step | Do | Check that proves it | Breaks if done early |
|---|---|---|---|
| 1 | Export Console reporting (usage and cost by key and workspace) | The export file exists and opens | Analytics and API keys do not carry over, so this cannot be done afterwards |
| 2 | Provision seats and SCIM group mappings, then sync | A pilot user appears with a seat | Setting the sign-in lock first locks out people with no seat |
| 3 | Confirm Claude Code is enabled for the organization. Set `forceLoginOrgUUID` in managed settings (placeholder in `managed-settings-snippet.json`) | A pilot user can still sign in | Without seats in step 2 nobody can sign in |
| 4 | Remove leftover Console credentials: key variables in shell profiles, `apiKeyHelper` in settings (run `leftover_credentials_check.py`) | The check prints no FOUND lines | A leftover key can keep authenticating the old way |
| 5 | Each person runs `/login`, chooses the Enterprise organization, then `/status` | `/status` names the Enterprise organization | |
| 6 | Move CI: a `claude setup-token` credential, or keep Console keys for automation | A test run of each pipeline passes | Removing people from Console before this can break nightly runs |
| 7 | Remove migrated users from the Console organization | Members list shows the remaining accounts only | Doing it before steps 1 and 6 loses data or breaks CI |
| 8 | Tell people what did not carry over | Message sent | |

Does not carry over: Console analytics and API keys. CLI session history is stored locally and needs no migration.

Out of scope here: spend cap design (Professional 4).
