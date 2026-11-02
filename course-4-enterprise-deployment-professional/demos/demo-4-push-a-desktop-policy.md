# Demo 4: Push a Desktop Policy

**Course:** Claude Enterprise Deployment and Security Operations Professional (Claude MasterClass Professional, Course 4)
**Demo:** 4 of 8
**Time:** about 15 minutes

> Part of **[Claude Enterprise Deployment and Security Operations Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

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

**Previous:** [Demo 3: Pull Activity With the Compliance API](demo-3-pull-activity-with-the-compliance-api.md) · **Next:** [Demo 5: Design a Spend-Limit Tree](demo-5-design-a-spend-limit-tree.md)


*Demo 4 of 8*
