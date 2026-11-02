# Demo 7: Read the Sandbox Audit Trail

**Course:** Claude Enterprise Deployment and Security Operations Professional (Claude MasterClass Professional, Course 4)
**Demo:** 7 of 8
**Time:** about 12 minutes

> Part of **[Claude Enterprise Deployment and Security Operations Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

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

**Previous:** [Demo 6: Block a Write and a Network Call](demo-6-block-a-write-and-a-network-call.md) · **Next:** [Demo 8: Replace a Static Key With Federation](demo-8-replace-a-static-key-with-federation.md)


*Demo 7 of 8*
