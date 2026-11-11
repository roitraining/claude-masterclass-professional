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
- [ ] `$FILES/lab3-harden` from your instructor: `lab3_brief.md`, `check_settings.py`, and the project `vuln-app/` (`app.py`, `attack_simulation.py`, `tools/checksum.py`, `reports/q3.txt`, `config/secrets.env` with fake placeholders, `CLAUDE.md`, `.mcp.json`, `tools/mcp_stub.py`, `classroom-sandbox.sh`, `.claude/settings.json` starter)

> **Note:** if the sandbox cannot start on your machine, that is a known platform limit, not a failure. The static checker works everywhere, and fallback scoring applies.
>
> **On a Linux classroom VM you can switch it on yourself** — see Step 0 below. Do that and the lab scores out of 100 instead of 85.

---

## Overview

`vuln-app` is deliberately weak. Its starter settings turn the sandbox off, allow everything, and trust every project MCP server.

The attack script tries four things: a write outside the working directory, a connection to a disallowed destination, a read of the secrets file, and a command injection through `app.py`.

The sandboxed Bash tool uses Seatbelt on macOS and bubblewrap on Linux and WSL2 (the network proxy also needs socat). **If the sandbox cannot start, the default is to warn and run commands unsandboxed.** Hooks, MCP servers, and plugin processes run outside the sandbox.

---

## Part 1: Set Up and Read the Approved Lists

### Step 0: Check Whether the Sandbox Can Start (Linux, optional)

```
bash $FILES/lab3-harden/classroom-sandbox.sh --check
```

If it says the sandbox **can** start, skip to Step 1 — you will score out of 100.

If it says `bwrap-userns-restrict is ACTIVE`, the OS is blocking the sandbox and Part B's
attacks 1 to 3 cannot be blocked on this machine. You have two choices:

1. **Do nothing.** Fallback scoring applies, the maximum is 85, and nothing in the lab
   breaks. Attack 4 still runs live.
2. **Switch it on for this VM** (needs `sudo`), then put it back when you finish:

   ```
   bash $FILES/lab3-harden/classroom-sandbox.sh --on
   # ... do the lab ...
   bash $FILES/lab3-harden/classroom-sandbox.sh --off
   ```

> **Read this before you run `--on`, because it is the lab's first real security
> decision.** That command disables an AppArmor profile, and it does **not** grant the
> permission to Claude Code alone — the profile is machine-wide, so every process on the
> VM gains the ability it lifts. You are weakening a host control in order to switch on an
> application sandbox. That is a genuine trade, and on a production fleet or a developer's
> laptop the answer is usually no. It is defensible here only because this is a
> disposable classroom VM holding nothing but fake credentials.
>
> Narrower options exist in principle and were tried on this image: a profile naming the
> `claude` binary does not work, because the denial is raised inside `unpriv_bwrap`, the
> profile that `/usr/bin/bwrap` transitions *into*. Confining the caller does not change
> what its child transitions to. Be ready to say in Step 7 which choice you made and why.

**Expected result:** you know whether your attack table will be live or predicted, and
you can say what `--on` costs.

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

| Key | What it does | Value shape |
|---|---|---|
| `enableAllProjectMcpServers` | Approves every server `.mcp.json` declares, with no prompt | `true` / `false` |
| `enabledMcpjsonServers` | Approves the servers you name from `.mcp.json` | names: `["docs-search"]` |
| `disabledMcpjsonServers` | Rejects the servers you name from `.mcp.json` | names: `["shadow-sync"]` |
| `allowedMcpServers` | Blocks any server that does not match an entry, **wherever it is defined** | one-key objects: `[{"serverName": "docs-search"}]` |

**The question to answer is which of these is a control.** Two of them only approve
servers that are already declared; one of them blocks. Compare the approved list against
what `.mcp.json` declares, decide what has to change in each file, and be ready to say
in Step 7 why naming the two approved servers does not, on its own, stop the third.

> **Key Insight:** approving is not the same as allowlisting. A server you never
> approved can still be declared and still run, so approving only what you trust does
> not remove what you do not.

> **Common Pitfall:** `allowedMcpServers` takes **objects with one key**, not bare
> strings. A list of strings matches nothing, which blocks every server including the
> ones you approved — your session starts with no MCP servers at all. If that happens,
> check the shape before you change the rule.

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

> **Also note, if you ran Step 0's `--on`:** you turned off a host control to turn on an application sandbox. Say in one line what you would have needed before doing that on a machine that mattered.

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
| Sandbox will not start | Session warns and runs unsandboxed, or every command fails with `apply-seccomp` | On Linux, run `classroom-sandbox.sh --check` — an active `bwrap-userns-restrict` profile is the usual cause and Step 0 can switch it off. On native Windows or WSL1 the primitives are missing and fallback scoring applies. Either way this is a known limit, not a failure |
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

**Fallback scoring (no OS sandbox):** Part B attacks 1 to 3 are scored 5 each from the PREDICTED outcomes of the checker. Attack 4 is always scored live because it needs no sandbox — run `python3 attack_simulation.py` in your own terminal, since a correctly hardened session refuses every command when the sandbox cannot start (Step 6). The maximum is 85. Your instructor will say so before the lab begins. **On a Linux classroom VM, Step 0 can switch the sandbox on and put the lab back to the full 100.**

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
