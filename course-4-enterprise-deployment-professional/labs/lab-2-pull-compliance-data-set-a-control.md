# Lab 2: Pull Compliance Data, Set a Control

> Part of **[Claude Enterprise Deployment and Security Operations Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

**Learning objective:** Turn activity data into findings backed by event evidence, and write a deployment control specification that is correct on the points a reviewer would check. Time: 90 minutes (about 55 for the data task, 35 for the control).

**Files:** `$FILES/lab2-compliance`: `activity_export.json`, `activity_export.csv`, `findings_lab2.json`, `control_ticket.md`, `control_proxy_spec.json`, `control_desktop_policy.json`, `check_lab2.py`. Instructor only: `instructor/make_activity_export.py`.

**Context:** The export is SYNTHETIC: 439 fictional events over seven days for Northwind Example Corp, in UTC. Event type names are invented for this lab and are not the Compliance API schema (UNVERIFIED). The organization's business hours are 09:00 to 18:00 UTC, Monday to Friday, and its known locations are the US ranges listed in the export's metadata. The Compliance API has the full set for Enterprise: the Activity Feed (a key with `read:compliance_activities`), the directory, and content for claude.ai organizations. Console organizations get the Activity Feed only.

**Steps (offline path, data task):**

1. **Goal:** write a short script or query (any language) that surfaces activity worth a security review, then write findings backed by event ids.
2. **Acceptance criteria:** each finding names the account, cites event ids from the export, gives a severity, and explains why the pattern matters; benign activity that merely looks unusual is not reported as a threat; the analysis script is saved and referenced in `findings_lab2.json`.
3. **Hints:** group by actor and by hour. Compare source addresses and countries against the known locations. Compare event time with business hours. Look at what happens in the minutes before and after each unusual event. Check what a share was shared with.
4. Record findings in `findings_lab2.json`.

**Steps (live path, data task):**

1. **Goal:** prove you can pull data from the Compliance API, then analyze the provided export.
2. **Acceptance criteria:** a script makes an authenticated request to the Activity Feed on the sandbox, reads at least a page of events, and writes them to a CSV with the actor, time, event type, and source address. Then complete the offline data task on the provided export.
3. **Hints:** the request shape and pagination are not in this guide: your instructor supplies them from the Compliance API documentation (UNVERIFIED here). Read the key from an environment variable and never paste it into a file. A sandbox organization will not contain the planted anomalies, which is why the analysis runs on the provided export.

**Steps (control task, both paths):**

1. Read `control_ticket.md` and choose one track.
2. **Track A goal:** write a Tenant Restrictions proxy rule specification in `control_proxy_spec.json`. **Acceptance criteria:** it names the request header, gives the value in the required format, lists the hosts and the authentication methods covered, states what the proxy must be able to do, and allows only the approved organizations. **Hints:** the ticket's organization list was pasted from a chat message. Read it as a reviewer would.
3. **Track B goal:** write a Claude Desktop managed policy specification in `control_desktop_policy.json`. **Acceptance criteria:** it names the macOS preference domain, the Windows precedence between machine and user level, the delivery method and installer for each platform, the three policy areas, and what happens to the in-app extension allowlist. Key names are not supplied: use placeholders that start with `UNVERIFIED:` and do not invent any.
4. Score yourself: `python check_lab2.py --findings findings_lab2.json --control <your control file>`

**Checkpoint:** A finding report with four anomalies backed by event ids and no benign activity flagged as a threat, plus a control spec that passes the checklist.

**Common problems:**

- Reading the CSV timestamps as local time: they are UTC, as is the business-hours definition.
- Reporting every large download: ask whether the pattern repeats at the same time on other days and who the user is.
- Citing only the first event of a sequence: cite several so a reviewer can reproduce the finding.
- Pasting the ticket's organization list straight into the header value: check spaces, a trailing comma, and the retired entry.
- Writing key names you remember from somewhere: do not invent them. Use `UNVERIFIED:` placeholders.

**Scoring rubric (100):**

| Item | Points |
|------|--------|
| Each of four anomalies: account named (6), event ids cited (5), explanation (4) | 60 |
| Benign activity not over-reported (minus 5 for each benign account rated medium or high) | 10 |
| Control task, scored by checklist (Track A: header 5, value format 5, approved ids exact 6, hosts 5, TLS 4, authentication coverage 5. Track B: domain 5, HKLM priority 5, three policy areas on both platforms 9, no invented key names 5, delivery and installers 3, allowlist override 3) | 30 |

**Facilitator note:** Planted anomalies, found by rule in `check_lab2.py`:

- **A1: after-hours bulk download.** `dana.whitfield@example.com`, 64 `file_downloaded` events between 02:14 and 02:31 UTC on Saturday 2026-09-12, from her usual address, so location alone will not find it.
- **A2: API key created and used from a new location.** `marcus.bell@example.com` creates `key-FAKE-0042` on Wednesday at 15:41 UTC from `203.0.113.55` (country RO) and uses it nine times from the same address. His usual address is `198.51.100.17`.
- **A3: project shared outside the organization.** `hana.kobayashi@example.com` shares "Project: Q4 Pricing Strategy" with `consultant@outside-example.net` (external true, edit permission).
- **A4: failed then successful SSO sequence.** `lee.ortega@example.com`: eight `login_sso_failed` events in about five minutes from `203.0.113.88` (country BR), then a success from the same address, then three downloads of HR extracts.
- **Decoys:** `priya.nair` downloads 25 files at 14:05 UTC on two days (recurring, business hours); `sam.okafor` creates and uses a key from one known address; `jun.park` shares a project with an internal group; `omar.haddad` has a single failure then success from the same address.
- **Control traps:** the retired organization `...00f9` in the ticket list; a trailing comma and spaces; TLS inspection currently off; Windows users can write HKCU, so HKLM priority must be stated.

Proxy facts used: the header `anthropic-allowed-org-ids` carries comma-separated organization UUIDs with no spaces; it is added to traffic for claude.ai, api.anthropic.com, claude.com, and anthropic.com; TLS inspection is required; web, desktop, API key, and OAuth token authentication are covered. Instructor note: the Compliance API request shape for the live path and all Desktop key names are not in the verified facts. Rehearse the live path and bring the key names from support article 12622667 for debriefing only.
