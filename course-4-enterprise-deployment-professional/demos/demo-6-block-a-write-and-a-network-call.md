# Demo 6: Block a Write and a Network Call

**Course:** Claude Enterprise Deployment and Security Operations Professional (Claude MasterClass Professional, Course 4)
**Demo:** 6 of 8
**Time:** about 12 minutes

> Part of **[Claude Enterprise Deployment and Security Operations Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Show the sandbox denying a write outside the working directory and a call to a disallowed domain. Time: about 12 minutes.

**Files:** [`$FILES/lab3-harden/vuln-app/.claude/settings.json`](../demo-files/lab3-harden/vuln-app/.claude/settings.json) is the weak starter, shown for contrast only.

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

**Previous:** [Demo 5: Design a Spend-Limit Tree](demo-5-design-a-spend-limit-tree.md) · **Next:** [Demo 7: Read the Sandbox Audit Trail](demo-7-read-the-sandbox-audit-trail.md)


*Demo 6 of 8*
