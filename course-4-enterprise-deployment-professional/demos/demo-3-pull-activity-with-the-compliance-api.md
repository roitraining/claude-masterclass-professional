# Demo 3: Pull Activity With the Compliance API

**Course:** Claude Enterprise Deployment and Security Operations Professional (Claude MasterClass Professional, Course 4)
**Demo:** 3 of 8
**Time:** about 15 minutes

> Part of **[Claude Enterprise Deployment and Security Operations Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Pull audit activity programmatically, state what each access level returns, and place the call in a monitoring pipeline. Time: about 15 minutes.

**Files:** none. The Lab 2 export is synthetic and is shown only in the lab.

**Context:** Enterprise has the full API: the Activity Feed (needs a key with `read:compliance_activities`), the directory of users, roles and groups, and chats, files and projects for claude.ai organizations (needs a Compliance Access Key with the relevant scope). Console organizations get the Activity Feed only. Content endpoints serve claude.ai data only. The admin-settings CSV audit-log export is narrower: a capped lookback, CSV only, no content.

**Steps:**

1. Put two columns on the board: what the Compliance API returns, what the admin CSV export returns. Fill in the coverage and lookback differences from the context above.
2. Open the Compliance API documentation page and show the Activity Feed request you rehearsed. Name the scope the key needs.
3. Run the rehearsed request with a sandbox key read from an environment variable. Never paste a key on screen.
4. Show the response: count events by type and by surface, and point out any Claude Code, Cowork, Claude for Microsoft 365, or Claude in Chrome sessions listed.
5. Download the admin CSV export for the same window and compare the fields and the lookback.
6. Draw the pipeline: scheduled pull, store, detection rules, alert. Name where a SIEM sits and say that SIEM integrations are vendor descriptions, not Anthropic documentation.

**Expected result:** A response with activity events that the instructor can count and group, and a visible difference in depth and lookback against the CSV export.

**Fallback (no live tenant):** Walk through a recorded-transcript outline: the request (with the key redacted), the first page of the response, the grouping command, and the CSV comparison, all captured during rehearsal.

> **Instructor note:** The request shape, pagination, and field names are not in the verified facts. Copy them from platform.claude.com/docs/en/manage-claude/compliance-api during rehearsal. Do not state event type names from memory. Compliance Access Key issuance and who may create one were not verified: confirm on the sandbox.

**Why this matters:** An audit trail that no one pulls is not a control. The access level decides what a security team can actually see.

---

**Previous:** [Demo 2: Scope a Custom Role](demo-2-scope-a-custom-role.md) · **Next:** [Demo 4: Push a Desktop Policy](demo-4-push-a-desktop-policy.md)


*Demo 3 of 8*
