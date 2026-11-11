# Lab 3: Harden a Sample Repository

**Course:** Claude Enterprise Deployment and Security Operations Professional
**Duration:** 90 minutes
**Format:** Instructor-led, in-class hands-on lab (300 level)

> Part of **[Claude Enterprise Deployment and Security Operations Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

## Prerequisites

- [ ] macOS, Linux, or WSL2. **WSL1 and native Windows are not supported** for the live sandbox — see the fallback scoring below
- [ ] `socat` installed if you need the network proxy
- [ ] Python 3.11 or later
- [ ] `claude` signed in
- [ ] `$FILES/lab3-harden` from your instructor: `lab3_brief.md`, `check_settings.py`, and the project `vuln-app/` (`app.py`, `attack_simulation.py`, `tools/checksum.py`, `reports/q3.txt`, `config/secrets.env` with fake placeholders, `CLAUDE.md`, `.mcp.json`, `.claude/settings.json` starter)

> **Note:** if the sandbox cannot start on your machine, that is a known platform limit, not a failure. The static checker works everywhere, and fallback scoring applies.

---

## Overview

`vuln-app` is deliberately weak. Its starter settings turn the sandbox off, allow everything, and trust every project MCP server.

The attack script tries four things: a write outside the working directory, a connection to a disallowed destination, a read of the secrets file, and a command injection through `app.py`.

The sandboxed Bash tool uses Seatbelt on macOS and bubblewrap on Linux and WSL2 (the network proxy also needs socat). **If the sandbox cannot start, the default is to warn and run commands unsandboxed.** Hooks, MCP servers, and plugin processes run outside the sandbox.

---

## Part 1: Set Up and Read the Approved Lists

### Step 1: Copy the Project and Read the Brief

Follow the copy steps in `lab3_brief.md`, then read the approved lists.

**Expected result:** a working copy at `~/work/vuln-app`, and you know which domains and which MCP servers are approved.

---

## Part 2: Harden the Configuration

### Step 2: Close the Sandbox and the Network

**Acceptance criteria:**

- The sandbox is on, the session fails if the sandbox cannot start, and no command can opt out of the sandbox.
- Outbound traffic is limited to the approved domains.
- Writes are limited to what the project needs, with no broad path such as a home folder.
- The secrets file and `~/.ssh` cannot be read, and the project configuration cannot be rewritten.

> **Hint:** setting names are `sandbox.enabled`, `sandbox.failIfUnavailable`, `sandbox.allowUnsandboxedCommands`, `sandbox.network.allowedDomains`, and the filesystem lists `allowWrite`, `denyRead`, `denyWrite`.

> **Common Pitfall:** if attack 1 still succeeds, check `allowWrite` for a home folder entry. The parent folder of the project usually sits under it.

### Step 3: Write the Deny Rules and Control the MCP Servers

**Acceptance criteria:**

- Permission deny rules cover the secrets file, `.env`, and common network commands. No blanket Bash allow remains.
- The blanket approval is off, and the unapproved server is no longer declared.
- A setting names the approved servers, or rejects the unapproved one.

> **Hint:** a deny rule matches the command as written. Ask what a different command spelling would do.

**The MCP settings, so you are deciding and not guessing.** The starter sets
`enableAllProjectMcpServers: true`, which approves every server `.mcp.json` declares.
These are the keys that bear on it:

| Key | What it does |
|---|---|
| `enableAllProjectMcpServers` | Approves every server `.mcp.json` declares, with no prompt |
| `enabledMcpjsonServers` | Approves the servers you name from `.mcp.json` |
| `disabledMcpjsonServers` | Rejects the servers you name from `.mcp.json` |
| `allowedMcpServers` | Allowlists which servers a user may *add* — it does **not** restrict `.mcp.json` |

**The question to answer is which of these is a control.** One of them approves, one
rejects, and one governs a different thing entirely. Compare the approved list against
what `.mcp.json` declares, decide what has to change in each file, and be ready to say
in Step 7 why naming the two approved servers does not, on its own, stop the third.

> **Key Insight:** approving is not the same as allowlisting. A server you never
> approved can still be declared, and a list that only names what you trust does not
> remove what you do not.

---

## Part 3: Fix the Code

### Step 4: Fix the Injection in app.py

**Acceptance criteria:** the injection attack fails because the code is fixed, not because a boundary caught it.

> **Key Insight:** a sandbox restricts where a command can write, not what a command inside the project can do. Attack 4 never leaves the project, so no configuration stops it. Validate the name and avoid a shell.

---

## Part 4: Prove It with the Attack Script

### Step 5: Run the Static Checker

```
python3 <path>/check_settings.py ~/work/vuln-app
```

Run it repeatedly until Part A is as high as you can get it.

**Acceptance criteria:** Part A of the checker passes.

### Step 6: Run the Attack Script Through a Session

Start Claude Code in `~/work/vuln-app` and run `python3 attack_simulation.py` through the session. Record the table.

**Acceptance criteria:** the attack table shows the attacks blocked.

> **If the session refuses every command,** including the attack script, with
> `apply-seccomp: ... Permission denied` — your configuration is correct and your machine
> has no working OS sandbox. `failIfUnavailable: true` is doing its job: the sandbox
> cannot start, so nothing runs. You cannot produce the table from inside the session.
> Run `python3 attack_simulation.py` in your own terminal instead, record attack 4's
> live outcome from that, and take attacks 1 to 3 from the checker's predictions. That is
> the fallback scoring below, and it is the expected path on a machine without the
> sandbox — not a mistake on your part.

> **Troubleshooting:** if attack 2 still reports a connection, loopback handling under the sandbox proxy is UNVERIFIED. Ask your instructor for the rehearsed destination and pass it with `--net-target`.

> **Note:** start `claude` interactively in `~/work/vuln-app` once and accept the trust
> dialog before you run anything with `-p`. In a workspace that has not been trusted,
> `claude -p` ignores `permissions.allow` and the `.mcp.json` approval settings from the
> project file, and prints a warning saying so.

---

## Part 5: Write the Notes

### Step 7: Name What Your Configuration Does Not Stop

Write `lab3_notes.md` as the brief describes.

**Acceptance criteria:** your notes name at least one thing your configuration does not stop.

---

## Part 6: Checkpoint

### Step 8: Verify Your Progress

- [ ] `sandbox.enabled` is on
- [ ] The session fails closed if the sandbox cannot start
- [ ] No command can opt out of the sandbox
- [ ] Outbound traffic is limited to the approved domains, not `*`
- [ ] `allowWrite` contains no home folder or other broad path
- [ ] The secrets file and `~/.ssh` cannot be read
- [ ] The project configuration cannot be rewritten
- [ ] Deny rules cover the secrets file, `.env`, and common network commands
- [ ] No blanket `Bash(*)` allow remains
- [ ] The blanket approval is off and the unapproved server is no longer declared in `.mcp.json`
- [ ] A setting names the approved servers, or rejects the unapproved one
- [ ] `app.py` validates the name and avoids a shell
- [ ] Part A of `check_settings.py` passes
- [ ] The attack table is recorded, showing the outcome of all four attacks (from your own terminal if the session has no working sandbox — see Step 6)
- [ ] `lab3_notes.md` names at least one thing the configuration does not stop
- [ ] You can explain why attack 4 needed a code fix rather than a boundary

---

## Troubleshooting Reference

| Issue | Symptom | Solution |
|---|---|---|
| Sandbox will not start | `apply-seccomp: write /proc/self/setgroups ... Permission denied`, or kernel `apparmor="DENIED" ... profile="unpriv_bwrap"` | On Ubuntu 24.04 and later, AppArmor's `bwrap-userns-restrict` profile blocks the nested user namespace the sandbox needs. Relaxing `kernel.apparmor_restrict_unprivileged_userns` does **not** help, because the profile carries an explicit deny. This is a machine configuration problem, not a settings problem: record the attacks you could not verify and move on |
| Sandbox will not start | Session warns and runs unsandboxed | You may be on native Windows, WSL1, or a machine missing the Linux primitives. Use the static checker and the fallback scoring. This is a known limit, not a failure |
| Attack 1 still succeeds | A write lands outside the project | Check `allowWrite` for a home folder entry. The project parent is usually under it |
| Attack 4 succeeds despite a perfect sandbox | Injection still works | The command never leaves the project. Fix `app.py`: validate the name and avoid a shell |
| MCP rule ignored | Unapproved server still runs | Naming the approved servers only *approves* them. It does not remove the unapproved one, which stays declared in `.mcp.json` until you delete it or reject it with `disabledMcpjsonServers`. See the table in Step 3 |
| Attack 2 reports a connection | Network block appears not to work | Loopback handling under the sandbox proxy is UNVERIFIED. Ask your instructor for the rehearsed destination and pass it with `--net-target` |

---

## Scoring Rubric (100 points)

| Item | Points |
|------|--------|
| Part A: static checklist (sandbox on 7, fail closed 7, no unsandboxed opt-out 7, allowed domains 7, allowWrite 5, denyRead 5, denyWrite 3, deny rules for secrets 4, deny rules for curl and wget 3, no blanket allow 4, MCP enforcement 5, MCP setting 3) | 60 |
| Part B: attack script, 10 for each blocked attack | 40 |

**Fallback scoring (no OS sandbox):** Part B attacks 1 to 3 are scored 5 each from the PREDICTED outcomes of the checker. Attack 4 is always scored live because it needs no sandbox — run `python3 attack_simulation.py` in your own terminal, since a correctly hardened session refuses every command when the sandbox cannot start (Step 6). The maximum is 85. Your instructor will say so before the lab begins.

---

## What You Built

In 90 minutes, you:

- Turned a project whose settings allowed everything into one that fails closed when the sandbox cannot start
- Replaced a wildcard domain list and a blanket Bash allow with lists that name what is actually approved
- Learned the limit of a boundary: attack 4 never leaves the project, so only a code fix stops it
- Ran a real attack script against your own configuration instead of assuming the settings worked
- Wrote down what your configuration still does not stop, which is the part a reviewer will ask about

---

## What's Next

Lab 4, Prompt Injection Detection, moves from attacks you run deliberately to text that arrives looking like data.

---

## Facilitator Notes

Traps in the starter: `sandbox.enabled` false; `allowUnsandboxedCommands` true; `allowedDomains` is `*`; `allowWrite` is `~` (the parent folder of the project is usually under it, so attack 1 succeeds); `denyRead` empty; `Bash(*)` in the allow list; `enableAllProjectMcpServers` true; and `shadow-sync` declared in `.mcp.json` though it is not approved.

Attack 4 can only be fixed in `app.py`: a regular-expression check of the name and `subprocess.run` with a list argument. Teach the point that a sandbox does not stop an in-project command. The planted secret is `FAKE-TOKEN-DO-NOT-USE`.

**Needs rehearsal:** the live sandbox behavior on the class machines, the parent object of `allowUnsandboxedCommands`, the nesting of the filesystem lists under `sandbox.filesystem`, the MCP allowlist setting names, the deny rule syntax, and loopback handling for attack 2. The static checker is the part that works everywhere. Do not promise live results on any specific machine.

---

*Lab 3 Complete*
