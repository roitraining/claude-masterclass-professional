# Demo 1: Connect an Identity Provider

**Course:** Claude Enterprise Deployment and Security Operations Professional (Claude MasterClass Professional, Course 4)
**Demo:** 1 of 8
**Time:** about 15 minutes

> Part of **[Claude Enterprise Deployment and Security Operations Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

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

**Next:** [Demo 2: Scope a Custom Role](demo-2-scope-a-custom-role.md)


*Demo 1 of 8*
