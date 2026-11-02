# Demo 8: Read a Plugin's Cost and Usage

**Course:** Claude Desktop Professional, Plugin and Extension Engineering (Claude MasterClass Professional, Course 1)
**Demo:** 8 of 8
**Time:** about 10 minutes

> Part of **[Claude Desktop Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Compare the always-on cost of two plugins, find the signals that show how a plugin is used, and say which signals are available to an individual and which to an administrator. Time: about 10 minutes.

**Files:** [`$FILES/autopsy-plugin`](../demo-files/autopsy-plugin), `~/work/records-desk` (from Demos 1 to 3).

**Context:** Cost and use are the two numbers behind keep, split, or retire. The component inventory and the always-on figure tell you the cost before anyone uses the plugin. Telemetry tells you who used it afterward. This demo previews the monitoring covered in the enterprise courses.

**Steps:**

1. Print the inventory and cost of the small plugin and the flawed one, side by side:

```
claude --plugin-dir ~/work/records-desk plugin details records-desk
claude --plugin-dir $FILES/autopsy-plugin plugin details expense-digest
```

2. Compare the per-component tables. Find the three or four components that make up most of the larger plugin's cost. Say what you would shorten or split.
3. In a Claude Code session, run `/plugin` and open a plugin from the official marketplace. Show the Context cost section and the highlight at 2,000 tokens or more.
4. In the same session run `/usage` after a few turns and show what it reports.
5. On a slide, show the administrator view: OpenTelemetry events for plugin installs and use, and, on Enterprise, an Analytics API endpoint with per-plugin install and invocation counts across Claude Code and Cowork. Do not open an admin console.
6. Ask the class for a keep, split, or retire decision for the flawed plugin, given its cost and an invented 2 hours saved a week.

**Expected result:** The flawed plugin's always-on cost is a multiple of the small plugin's (about 2,050 against about 125 tokens when this guide was built), and most of it sits in skill and agent descriptions. The class proposes shortening descriptions or merging the seven rule skills into a single skill that reads a policy file.

> **Instructor note:** Verified: `claude plugin details` reports a component inventory, an Always-on token estimate, and a per-component split, and does not count hooks or MCP tool schemas. The `/plugin` Context cost section and its 2,000-token highlight apply to plugins in the official marketplace. The OpenTelemetry events and the Enterprise Analytics API are stated in the plugin measurement docs. Not verified: what `/usage` shows about plugins, and the endpoint names and field names for the Analytics API. Rehearse `/usage`, and describe the administrator view only in general terms. Position the whole demo as a preview, not as the monitoring curriculum.

> **Why this matters:** A plugin that costs more than it saves should be split or retired. You can only decide that with the numbers.

---

**Previous:** [Demo 7: Review a Plugin Before You Trust It](demo-7-review-a-plugin-before-you-trust-it.md)


*Demo 8 of 8*
