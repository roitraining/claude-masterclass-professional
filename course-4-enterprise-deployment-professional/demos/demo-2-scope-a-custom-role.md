# Demo 2: Scope a Custom Role

**Course:** Claude Enterprise Deployment and Security Operations Professional (Claude MasterClass Professional, Course 4)
**Demo:** 2 of 8
**Time:** about 15 minutes

> Part of **[Claude Enterprise Deployment and Security Operations Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Create a Custom role, attach it to a group, and show that a JIT user receives permissions only when the group exists in the organization. Time: about 15 minutes.

**Files:** [`$FILES/lab1-identity/custom_roles.json`](../demo-files/lab1-identity/custom_roles.json) for the design vocabulary only (placeholders, not real permission names). Do not open the other Lab 1 files.

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

**Previous:** [Demo 1: Connect an Identity Provider](demo-1-connect-an-identity-provider.md) · **Next:** [Demo 3: Pull Activity With the Compliance API](demo-3-pull-activity-with-the-compliance-api.md)


*Demo 2 of 8*
