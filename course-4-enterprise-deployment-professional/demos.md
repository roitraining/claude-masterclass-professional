# Claude Enterprise Deployment and Security Operations Professional: Demos

**Course:** Claude Enterprise Deployment and Security Operations Professional (Claude MasterClass Professional, Course 4)
**Contents:** 8 instructor-led demos. Each takes 15 minutes or less and has a learning objective. The numbers match the Today's Demos slide.

---

## About this guide

Run the demos in order: Demos 1 to 5 on Day 1, Demos 6 to 8 on Day 2. Each has the same layout: a learning objective, a time, a Files line when it uses files, a short context paragraph, numbered steps, an Expected result, an Instructor note, and a Why this matters note. Demos that need a live tenant also carry a Fallback.

These demos assume the Associate courses. They do not re-teach settings precedence basics or admin consent basics.

All demos run on an ROI sandbox Claude organization (Enterprise) and an identity provider test environment, driven by the instructor. No demo uses a real tenant, real identity data, or a real key. Every person, company, domain, and figure is fictional (`example.com` and similar).

**Rule for product claims.** Anything marked UNVERIFIED in an Instructor note is not confirmed by the course's verified facts. Say so out loud in class, and rehearse it on the sandbox before the day. Exact menu paths, field labels, API request shapes, and settings key names that are not in the verified facts are deliberately not written here. Collect them during rehearsal from the documentation pages named in each note.

**Files.** `$FILES` means the `demo-files` folder. Demos that reuse lab files say so. The lab files hold planted defects, so do not show a lab's answer key before the lab.

---

## Demo 1: Connect an Identity Provider

**Learning objective:** Connect an identity provider to a Claude organization in the right order, provision a test user through JIT, and say what SCIM would add. Time: about 15 minutes.

**Files:** none. Use the sandbox and the IdP test environment.

**Context:** SSO setup comes first and has two parts: domain verification and identity provider configuration. JIT creates a user at first login with the User role. SCIM creates and removes users from IdP assignments without a login and is limited to Enterprise and certain Console organizations, not Team.

**Steps:**

1. Show the sandbox organization before any change: no SSO, one Owner. State the sequence you will follow: verify the domain, configure the identity provider, test, then enforce.
2. Verify the sandbox email domain (a DNS record you prepared before class).
3. In the IdP test environment, create the application for Claude and assign a test group with a single test user.
4. Complete the SSO configuration on both sides. Do not enforce SSO yet.
5. Sign in as the test user in a private browser window. Show that the user was created at first login.
6. Show the user's role. State that JIT assigns the User role and that SCIM, if enabled, would have created the user without a login.
7. Name the one decision that looks done but is not: the domain. Ask the class what would happen to users of a second, unverified domain when you enforce SSO.

**Expected result:** The test user exists with the User role after the first SSO login, and SSO is configured but not yet enforced.

**Fallback (no live tenant):** Show a five-screenshot outline captured during rehearsal: (1) domain verification pending, (2) domain verified, (3) the IdP application with the test group assigned, (4) the first SSO login completing, (5) the new user in the member list with the User role.

> **Instructor note:** Whether the Team plan shows the same screens, the exact menu paths, and the label for invite-only versus JIT are not in the verified facts; the newer guide defaults to invite only and older labels differ. Rehearse the screens and capture them for the fallback. Support article 13133195 is the source. State that SCIM is not available on Team.

**Why this matters:** Most identity incidents start with an order-of-operations mistake. The domain check and the IdP assignment are separate controls, and one does not imply the other.

---

## Demo 2: Scope a Custom Role

**Learning objective:** Create a Custom role, attach it to a group, and show that a JIT user receives permissions only when the group exists in the organization. Time: about 15 minutes.

**Files:** `$FILES/lab1-identity/custom_roles.json` for the design vocabulary only (placeholders, not real permission names). Do not open the other Lab 1 files.

**Context:** Enterprise adds a Custom role next to Owner, Admin, and User. Custom-role permissions come from groups. Those groups sync from the IdP only with SCIM directory sync. Under JIT you create the groups and add the users yourself, in organization settings under Groups. Group mappings control role and seat tier.

**Steps:**

1. Write the role on a whiteboard first: name, purpose in one sentence, the smallest set of permissions that serves it, and what it must not do.
2. Create the Custom role in the sandbox with those permissions.
3. In the IdP, assign a second test user to a new test group and map that group to the Custom role. Do not create the group in the Claude organization yet.
4. Sign in as that user. Show that the user has no permissions.
5. Create the group in organization settings under Groups, add the user, attach the Custom role, and sign in again.
6. Show the permissions now present and attempt one action outside the role to show it is refused.

**Expected result:** Step 4 shows a signed-in user with no permissions. Step 6 shows only the scoped permissions, and the out-of-scope action is refused.

**Fallback (no live tenant):** Use an outline of three screenshots (the user with no permissions, the group with the role attached, the refused action) plus the whiteboard design. Say plainly that these are rehearsal captures.

> **Instructor note:** The permission names and the exact permission picker are not in the verified facts. Describe permissions by purpose and read the real names from the sandbox. Do not claim a count of permissions. Lab 1 plants this same trap, so tell students you are showing the symptom and not the full list of defects.

**Why this matters:** A role that is correct on paper and empty at login looks like an outage. Knowing the JIT group requirement shortens the diagnosis from hours to minutes.

---

## Demo 3: Pull Activity With the Compliance API

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

## Demo 4: Push a Desktop Policy

**Learning objective:** Describe and deliver a Claude Desktop policy for macOS and Windows, and say which level wins on Windows. Time: about 15 minutes.

**Files:** none. Use the support article for key names.

**Context:** On macOS, configuration profiles use the domain `com.anthropic.claudefordesktop` (Jamf Pro, Kandji, and Intune are named), and a `.pkg` installer exists for enterprises. On Windows, Group Policy or Intune sets machine-wide (HKLM) or per-user (HKCU) values, with the machine level taking priority, and an `.msix` installer exists. Keys cover auto-update, desktop extensions, and local development MCP. User-machine policy overrides the in-app extension allowlist.

**Steps:**

1. Show the three policy areas on the board: auto-update, desktop extensions, local development MCP.
2. Open the Desktop enterprise configuration support article and show where the key names are listed. Copy two key names into the policy tool you rehearsed with.
3. On macOS (or a profile in the MDM sandbox), show the profile payload with the domain `com.anthropic.claudefordesktop`.
4. On a Windows test machine, set one value in HKCU and a conflicting value in HKLM. Show which value Desktop honors.
5. Show where the extension allowlist lives in the app and state that a user-machine policy overrides it.
6. Name the installers and the MDM tools from the context above.

**Expected result:** The conflicting HKLM and HKCU values resolve to the HKLM value, and the profile payload uses the correct domain.

**Fallback (no live tenant or no test machine):** Use a screenshot outline: the profile payload, the registry editor showing both hives with the HKLM value highlighted, and the in-app extension list.

> **Instructor note:** Key names are intentionally absent from this guide and from the Lab 2 files. Read them from support article 12622667 before class and confirm them on the test machine. The separate third-party-inference workflow that exports `.mobileconfig` or `.reg` files, with ADMX and plist templates, is a different path: do not mix the two. Whether a setting reaches a running Desktop session without a restart was not verified.

**Why this matters:** On Windows, users can often write their own hive. The machine-level priority is what makes a policy enforceable and not advisory.

---

## Demo 5: Design a Spend-Limit Tree

**Learning objective:** Design a spend-limit tree from organization to group to individual, and say what is confirmed and what is not. Time: about 12 minutes.

**Files:** none.

**Context:** Enterprise spend limits cascade from organization to group to individual. A Spend Limits API (Enterprise only) sets a limit per member, shows where a limit is inherited from, and reviews requests for higher limits. It needs a scoped Admin key from the Primary Owner.

**Steps:**

1. Present a fictional company: 900 users in four groups (Engineering, Support, Finance, Contractors). Ask the class to propose an organization limit first, then group limits, then two named exceptions.
2. Draw the tree on the board with fictional amounts. Mark each node as a limit, an inherited limit, or an exception.
3. Show where the Spend Limits API fits: set a member limit, read where it is inherited from, and review a request for a higher limit.
4. State who must create the key: a scoped Admin key from the Primary Owner.
5. Ask what a member sees at the limit, and write on the board what you can and cannot confirm.

**Expected result:** A tree with three levels, at least two exceptions, and a written list of unconfirmed behaviors.

**Fallback (no live tenant):** The demo is a whiteboard design. If the sandbox cannot show limits, show a screenshot outline of the limits screen and an API response captured during rehearsal.

> **Instructor note:** Pooled group budgets and alert thresholds (including the 75 and 90 percent figures from older material) are UNVERIFIED, secondary sources only. Do not teach them as fact. Whether a child limit can exceed its parent is also not confirmed: test it on the sandbox and tell the class what you saw. Do not state prices.

**Why this matters:** A limit tree is a design decision, and the cascade is what keeps an exception from becoming a hole.

---

## Demo 6: Block a Write and a Network Call

**Learning objective:** Show the sandbox denying a write outside the working directory and a call to a disallowed domain. Time: about 12 minutes.

**Files:** `$FILES/lab3-harden/vuln-app/.claude/settings.json` is the weak starter, shown for contrast only.

**Context:** The sandboxed Bash tool uses operating-system primitives: Seatbelt on macOS, bubblewrap on Linux and WSL2 (the network proxy also needs socat). WSL1 is not supported. Writes are limited to the working directory by default. Outbound traffic goes through a proxy that enforces `sandbox.network.allowedDomains`. If the sandbox cannot start, the default is to warn and run unsandboxed.

**Steps:**

1. In a scratch project, show settings with `sandbox.enabled` true and `sandbox.network.allowedDomains` holding a single domain.
2. Start Claude Code in the project and ask it to run: `echo test > ../outside.txt`. Show the denial.
3. Ask it to fetch a domain that is not in the allowed list with `curl`. Show the denial.
4. Ask for a write inside the working directory and show that it succeeds.
5. Stop the session, show the starter file from Lab 3, and ask the class which of the three results would change with the starter settings.

**Expected result:** The outside write and the call to the disallowed domain are refused, and the inside write succeeds.

**Fallback (sandbox not available on the demo machine):** Use a recorded-transcript outline: the three prompts, the denial messages, and the success, captured on a rehearsed machine. State that the live behavior needs OS support.

> **Instructor note:** The exact denial wording, and whether a denied command is reported to the user in a particular way, are not in the verified facts. Rehearse and capture it. Do not run this on a Windows machine that is native, not WSL2.

**Why this matters:** The sandbox holds without relying on what the command looks like, so it covers a command written in a way no rule anticipated.

---

## Demo 7: Read the Sandbox Audit Trail

**Learning objective:** Read what the sandbox and the logs record after a denial, and add a hook that records configuration changes. Time: about 12 minutes.

**Files:** none; the sample hook is inline below.

**Context:** `ConfigChange` hooks can audit or block settings changes. `/status` shows which settings sources apply. Hooks, MCP servers, and plugin processes run outside the sandbox. A deny rule matches the command as written, while sandbox network isolation does not depend on the command text.

**Steps:**

1. Repeat one denial from Demo 6 and show what Claude Code displays.
2. Run `/status` and show which sources apply.
3. Show this logging script. It writes the raw hook input and a timestamp without assuming any field names:

```python
import datetime, sys
with open(".claude/audit.log", "a", encoding="utf-8") as f:
    f.write("%s %s\n" % (datetime.datetime.now(datetime.timezone.utc).isoformat(), sys.stdin.read().strip()))
```

4. Register it as a `ConfigChange` hook in `.claude/settings.json`, restart, and change a setting.
5. Open `.claude/audit.log` and read the entry.
6. Ask the class: this hook runs outside the sandbox. What does that mean for who can edit the script, and how would you protect it?

**Expected result:** A timestamped line appears in the log for the settings change, and the class names the protection (managed settings and a write-deny on the hook path).

**Fallback:** If the hook does not fire on the demo version, show a recorded-transcript outline of the log entry.

> **Instructor note:** The exact JSON fields the hook receives, the hook registration shape for `ConfigChange`, and whether the sandbox itself writes an audit file or only surfaces a denial are not in the verified facts: UNVERIFIED. Rehearse. Do not claim a sandbox log location.

**Why this matters:** A control you cannot read back after an incident is a guess, and a hook that is writable by the user can be silenced by the user.

---

## Demo 8: Replace a Static Key With Federation

**Learning objective:** Replace a static key with a short-lived credential obtained at run time, and compare it with a CI credential from `claude setup-token`. Time: about 15 minutes.

**Files:** none; the sample scripts are inline below.

**Context:** Moving from Console keys to an Enterprise deployment means removing leftover Console credentials (API key variables and `apiKeyHelper`), signing in with `/login`, verifying with `/status`, and moving CI to a `claude setup-token` credential or keeping Console keys for automation. Secure credential storage uses Keychain on macOS and a mode-0600 file on Linux.

**Steps:**

1. Show a settings file with a key placed directly in it. Ask the class what is wrong: it is long-lived, copyable, and unaudited.
2. Show the pattern that replaces it. A helper script obtains a short-lived credential from a broker when it is needed. The local stand-in below issues a fake token with an expiry:

```python
import datetime, secrets
exp = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5)
print("FAKE-TOKEN-DO-NOT-USE-%s" % secrets.token_hex(4))
print("expires", exp.isoformat(), file=__import__("sys").stderr)
```

3. Run it twice and show two different values and the expiry on stderr. Point out that the token is fictional and does not authenticate.
4. Show where a helper is referenced in settings (the `apiKeyHelper` setting) and what removes the static key.
5. On the board, compare three CI options: a `claude setup-token` credential, a Console key for automation, and a broker-issued credential. Fill in what each costs to rotate, who owns it, and what the audit trail shows.
6. Ask who owns the credential when its holder leaves the company.

**Expected result:** Two runs produce two different short-lived values, and the class completes a three-row comparison with an owner and rotation plan for each option.

**Fallback (no live tenant):** The demo runs fully offline. If the class asks to see a real federated login, show a screenshot outline of `/login` and `/status` captured on the sandbox.

> **Instructor note:** Federation features on the Anthropic side (for example, exchanging a cloud identity for a Claude credential), the lifetime of a `claude setup-token` credential, and how often `apiKeyHelper` is called are not in the verified facts: UNVERIFIED. This demo teaches the pattern with a local stand-in and does not claim a product feature. Rehearse any real federated path before presenting it as one.

**Why this matters:** The credential that leaks is the one that lives longest. Short life, a named owner, and an audit trail are what make a leak survivable.
