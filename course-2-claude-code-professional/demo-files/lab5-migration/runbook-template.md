# Runbook: Larkspur Freight Software, Console to Enterprise (engineering)

Author: ______  Date: ______  Cutover window: Saturday 06:00 to 12:00

## 1. Before the window
- What you export from Console, in what form, who receives it, and by when. Say why it must happen before anything else.
- What you check in the identity provider and in the Enterprise organization before the window opens.

## 2. Identity and seats
- Group to seat mapping, including what happens to the contractors who are not in the provider.
- How you confirm the sync worked.

## 3. Roles
- The roles you define, each as "can" and "cannot". Mark anything you could not source as "to confirm".

## 4. Managed settings
- For each of the four needs: the mechanism, and for the unmanaged laptops what you can and cannot enforce.
- The order: when `forceLoginOrgUUID` is set relative to seat provisioning, and why. Use the placeholder `00000000-0000-0000-0000-000000000000` for the organization id.

## 5. Credentials
- For each of C1 to C5: keep, replace or remove, with the reason and the step.
- What you remove from laptops and repositories (names of variables and settings keys only).

## 6. Cutover steps, in order

_State where the pilot group cuts over relative to everyone else, and what you
check before widening._

A numbered list with a time for each step and an owner. Include the verification after the sign-in step, and the command or screen that proves it.

## 7. CI
- For each pipeline group (the 11 organization-secret repositories, the three with person-owned tokens, the GitLab project): which credential it uses after cutover, who owns it, and how you test it before the nightly run.
- Why you did or did not use a subscription token for an organization-wide secret.

## 8. After the window
- When migrated people are removed from the Console organization, and what must be true first.
- What stays in the Console organization, if anything, and why.

## 9. Rollback and communication
- The point after which you cannot roll back cheaply, and what you do before it.
- The message to engineers: what they must do and when.

## 10. What does not carry over
- State it plainly and say what you did about each item.
