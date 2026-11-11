# Lab 2: Pull Compliance Data, Set a Control

**Course:** Claude Enterprise Deployment and Security Operations Professional
**Duration:** 90 minutes — about 55 for the data task, 35 for the control
**Format:** Instructor-led, in-class hands-on lab (300 level)

> Part of **[Claude Enterprise Deployment and Security Operations Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

## Prerequisites

- [ ] Any language you can group and filter data in — a script or a query is fine
- [ ] `$FILES/lab2-compliance` from your instructor: `activity_export.json`, `activity_export.csv`, `findings_lab2.json`, `control_ticket.md`, `control_proxy_spec.json`, `control_desktop_policy.json`
- [ ] `check_lab2.py` **only if your facilitator hands it out** — it contains the answer logic, so it is normally withheld until you submit. The lab says where it is used
- [ ] Live path only: sandbox Compliance API access, and the request shape and pagination details from your instructor
- [ ] Live path only: an API key read from an environment variable, never pasted into a file

> **Note:** the export is SYNTHETIC — 439 fictional events over seven days, in UTC. Event type names are invented for this lab and are **not** the Compliance API schema (UNVERIFIED).

---

## Overview

Northwind Example Corp business hours are 09:00 to 18:00 UTC, Monday to Friday, and its known locations are the US ranges listed in the metadata of the export.

The Compliance API has the full set for Enterprise: the Activity Feed (a key with `read:compliance_activities`), the directory, and content for claude.ai organizations. Console organizations get the Activity Feed only.

Everyone does the data task in Part 1 and the control task in Part 3. Part 2 is an extra step for students with sandbox access.

---

## Part 1: The Data Task (about 55 minutes)

### Step 1: Write the Analysis Script

Write a short script or query in any language that surfaces activity worth a security review.

**Hints:**

- Group by actor and by hour.
- Compare source addresses and countries against the known locations.
- Compare event time with business hours.
- Look at what happens in the minutes before and after each unusual event.
- Check what a share was shared with.

**Expected result:** a saved script that surfaces candidate patterns, not just a list of unusual-looking rows.

> **Common Pitfall:** the CSV timestamps are UTC, as is the business-hours definition. Reading them as local time invents anomalies and hides real ones.

### Step 2: Write Findings Backed by Event Ids

**Acceptance criteria:** each finding names the account, cites event ids from the export, gives a severity, and explains why the pattern matters. Benign activity that merely looks unusual is **not** reported as a threat.

> **Common Pitfall:** do not report every large download. Ask whether the pattern repeats at the same time on other days, and who the user is.

> **Common Pitfall:** citing only the first event of a sequence is not enough. Cite **at least three events from the sequence** — enough that a reviewer can reproduce the finding without taking your word for the pattern. One anomaly is a single event; for that one, citing it is citing all of it. For a long sequence you do not need all of it, but the ids you pick must show the pattern, not just its first moment.

### Step 3: Record the Findings

Record findings in `findings_lab2.json`, and reference your analysis script there.

**Acceptance criteria:** the script is saved and referenced in `findings_lab2.json`.

---

## Part 2: Live Path Addition — Pull from the Compliance API

Only if your instructor has provisioned sandbox access. Everyone else continues at Part 3.

### Step 4: Pull a Page from the Activity Feed

**Acceptance criteria:** a script makes an authenticated request to the Activity Feed on the sandbox, reads at least a page of events, and writes them to a CSV with the actor, time, event type, and source address.

> **Hint:** the request shape and pagination are not in this guide. Your instructor supplies them from the Compliance API documentation (UNVERIFIED here).

> **Note:** a sandbox organization will not contain the planted anomalies, which is why the analysis in Part 1 runs on the provided export.

---

## Part 3: The Control Task (about 35 minutes)

### Step 5: Read the Ticket and Choose a Track

Read `control_ticket.md` and choose Track A or Track B.

**Expected result:** one track chosen, and you know which file you are writing.

> **Common Pitfall:** the organization list in the ticket was pasted from a chat message. Read it as a reviewer would, not as a trusted input.

### Step 6: Write Your Specification

**Track A — Tenant Restrictions proxy rule**, in `control_proxy_spec.json`.

Facts you need, from the course's verified set:

- The header is `anthropic-allowed-org-ids`
- Its value is comma-separated organization UUIDs, **no spaces**
- It is added to traffic for `claude.ai`, `api.anthropic.com`, `claude.com` and
  `anthropic.com`
- TLS inspection is required
- Web, desktop, API key and OAuth token authentication are all covered

**Acceptance criteria:** it names the request header, gives the value in the required format, lists the hosts and the authentication methods covered, states what the proxy must be able to do, and allows only the approved organizations.

> **Hint:** the facts above are given. The work is deciding *which* organizations
> belong in the value, from the ticket, and reading that list as a reviewer.

**Track B — Claude Desktop managed policy**, in `control_desktop_policy.json`.

**Acceptance criteria:** it names the macOS preference domain, the Windows precedence between machine and user level, the delivery method and installer for each platform, the three policy areas, and what happens to the in-app extension allowlist.

**Facts you need for Track B, from the course's verified set:**

- The macOS configuration-profile preference domain is `com.anthropic.claudefordesktop` (see Demo 4).
- On Windows, Group Policy or Intune sets machine-wide (HKLM) or per-user (HKCU) values, and **the machine level takes priority**.
- Installers: `.pkg` on macOS, `.msix` on Windows.
- The three policy areas are auto-update, desktop extensions, and local development MCP.
- User-machine policy overrides the in-app extension allowlist.

> **Common Pitfall:** the *individual key names* under that domain are not supplied. The domain above is given; the keys are not. Use placeholders that start with `UNVERIFIED:` for any key name and do not invent one. Writing key names you half-remember loses the points for that row.

### Step 7: Score Yourself

```
python3 check_lab2.py --findings findings_lab2.json --control <your control file>
```

The checker contains the answer key: it names the planted actors and the
approved resource IDs. Your facilitator runs it for you, or hands it over once
your findings file is written and submitted. If it is not in your pack, that is
deliberate — ask rather than looking for it.

**Acceptance criteria:** the findings report scores, and the control spec passes its checklist.

---

## Part 4: Checkpoint

### Step 8: Verify Your Progress

- [ ] Timestamps were treated as UTC throughout
- [ ] Four anomalies found, each naming the account
- [ ] Each finding cites at least three event ids from its sequence, not just the first (one anomaly is a single event, and citing it is enough)
- [ ] Each finding gives a severity and explains why the pattern matters
- [ ] No benign account rated medium or high
- [ ] The analysis script is saved and referenced in `findings_lab2.json`
- [ ] Live path only: an authenticated Activity Feed request read at least one page and wrote a CSV
- [ ] Live path only: the key came from an environment variable, never a file
- [ ] One control track chosen and its specification written
- [ ] Track A: the approved organization list is exact, with the retired entry removed and no stray spaces or trailing comma
- [ ] Track B: no invented key names — every unknown is an `UNVERIFIED:` placeholder
- [ ] `check_lab2.py` passes the control checklist

---

## Troubleshooting Reference

| Issue | Symptom | Solution |
|---|---|---|
| Phantom anomalies | Everything looks out of hours | The CSV timestamps are UTC, as is the business-hours definition. Do not convert to local time |
| Over-reporting downloads | Many large-download findings | Ask whether the pattern repeats at the same time on other days, and who the user is. Recurring business-hours activity is a decoy |
| Finding not reproducible | A reviewer cannot confirm it | You cited only the first event. Cite at least three ids from the sequence |
| Control value rejected | Track A header value fails the check | The organization list was pasted from a chat message. Check for spaces, a trailing comma, and the retired entry |
| Invented key names | Track B loses the no-invention points | Do not write key names from memory. Use `UNVERIFIED:` placeholders |

---

## Scoring Rubric (100 points)

| Item | Points |
|------|--------|
| Each of four anomalies: account named (6), event ids cited (5), explanation (4) | 60 |
| Benign activity not over-reported (minus 5 for each benign account rated medium or high) | 10 |
| Control task, scored by checklist (Track A: header 5, value format 5, approved ids exact 6, hosts 5, TLS 4, authentication coverage 5. Track B: domain 5, HKLM priority 5, three policy areas on both platforms 9, no invented key names 5, delivery and installers 3, allowlist override 3) | 30 |

---

## What You Built

In 90 minutes, you:

- Turned a week of raw activity into four findings a reviewer can reproduce from event ids, rather than a list of things that looked odd
- Left the decoys alone: recurring business-hours bulk downloads, a key used from a known address, an internal share, a single failed login
- Found the anomaly that location filtering cannot catch, because it came from the usual address of the user
- Wrote a deployment control specification exact on the points a reviewer checks, including an organization list that arrived untrusted in a chat message
- Marked what you did not know as `UNVERIFIED:` instead of inventing a key name

---

## What's Next

Lab 3, Harden a Sample Repository, moves from monitoring and policy to changing a codebase so the controls hold.

---

## Facilitator Notes

Planted anomalies, found by rule in `check_lab2.py`:

- **A1: after-hours bulk download.** `dana.whitfield@example.com`, 64 `file_downloaded` events between 02:14 and 02:31 UTC on Saturday 2026-09-12, from the usual address of this user, so location alone will not find it.
- **A2: API key created and used from a new location.** `marcus.bell@example.com` creates `key-FAKE-0042` on Wednesday at 15:41 UTC from `203.0.113.55` (country RO) and uses it nine times from the same address. The usual address is `198.51.100.17`.
- **A3: project shared outside the organization.** `hana.kobayashi@example.com` shares "Project: Q4 Pricing Strategy" with `consultant@outside-example.net` (external true, edit permission).
- **A4: failed then successful SSO sequence.** `lee.ortega@example.com`: eight `login_sso_failed` events in about five minutes from `203.0.113.88` (country BR), then a success from the same address, then three downloads of HR extracts.
- **Decoys:** `priya.nair` downloads 25 files at 14:05 UTC on two days (recurring, business hours); `sam.okafor` creates and uses a key from one known address; `jun.park` shares a project with an internal group; `omar.haddad` has a single failure then success from the same address.
- **Control traps:** the retired organization `...00f9` in the ticket list; a trailing comma and spaces; TLS inspection currently off; Windows users can write HKCU, so HKLM priority must be stated.

Proxy facts used: the header `anthropic-allowed-org-ids` carries comma-separated organization UUIDs with no spaces; it is added to traffic for claude.ai, api.anthropic.com, claude.com, and anthropic.com; TLS inspection is required; web, desktop, API key, and OAuth token authentication are covered.

Instructor note: the Compliance API request shape for the live path and all Desktop key names are not in the verified facts. Rehearse the live path and bring the key names from support article 12622667 for debriefing only.

---

*Lab 2 Complete*
