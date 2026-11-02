# Lab 3: Harden a Sample Repository

> Part of **[Claude Enterprise Deployment and Security Operations Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

**Learning objective:** Configure a sandbox boundary that fails closed, filesystem and network isolation, permission deny rules, and an MCP server allowlist, and prove with an attack script which attacks the configuration stops and which it does not. Time: 90 minutes.

**Files:** `$FILES/lab3-harden`: `lab3_brief.md`, `check_settings.py`, and the project `vuln-app/` (`app.py`, `attack_simulation.py`, `tools/checksum.py`, `reports/q3.txt`, `config/secrets.env` with fake placeholders, `CLAUDE.md`, `.mcp.json`, `.claude/settings.json` starter).

**Context:** `vuln-app` is deliberately weak. Its starter settings turn the sandbox off, allow everything, and trust every project MCP server. The attack script tries four things: a write outside the working directory, a connection to a disallowed destination, a read of the secrets file, and a command injection through `app.py`. The sandboxed Bash tool uses Seatbelt on macOS and bubblewrap on Linux and WSL2 (the network proxy also needs socat); WSL1 is not supported. If the sandbox cannot start, the default is to warn and run commands unsandboxed. Hooks, MCP servers, and plugin processes run outside the sandbox.

**Steps:**

1. Follow the copy steps in `lab3_brief.md`. Read the approved lists.
2. **Goal:** a project where the attack script no longer succeeds and the static checker passes.
3. **Acceptance criteria:**
   - The sandbox is on, the session fails if the sandbox cannot start, and no command can opt out of the sandbox.
   - Outbound traffic is limited to the approved domains.
   - Writes are limited to what the project needs, with no broad path such as a home folder.
   - The secrets file and `~/.ssh` cannot be read, and the project's own configuration cannot be rewritten.
   - Permission deny rules cover the secrets file, `.env`, and common network commands. No blanket Bash allow remains.
   - Only the approved MCP servers can run, and no unapproved server remains declared.
   - The injection attack fails because the code is fixed.
4. **Hints:** the starter settings contain several traps. A deny rule matches the command as written, so ask what a different command would do. A sandbox restricts where a command can write, not what a command inside the project can do. Setting names: `sandbox.enabled`, `sandbox.failIfUnavailable`, `allowUnsandboxedCommands`, `sandbox.network.allowedDomains`, and the filesystem lists `allowWrite`, `denyRead`, `denyWrite`.
5. Run `python <path>/check_settings.py ~/work/vuln-app` until Part A is as high as you can get it.
6. Start Claude Code in `~/work/vuln-app` and run `python attack_simulation.py` through the session. Record the table.
7. Write `lab3_notes.md` as the brief describes.

**Checkpoint:** Part A of the checker passes, the attack table shows the attacks blocked, and your notes name at least one thing your configuration does not stop.

**Common problems:**

- The sandbox does not start: you may be on native Windows, WSL1, or a machine missing the Linux primitives. Use the static checker and the fallback scoring below. This is a known limit, not a failure.
- Attack 1 still succeeds: check `allowWrite` for a home folder entry.
- Attack 4 still succeeds with a perfect sandbox: the command never leaves the project. Fix `app.py` (validate the name and avoid a shell).
- The MCP rule is ignored: the setting names for an MCP allowlist are UNVERIFIED in this course. Confirm them in the current Claude Code settings documentation.
- Attack 2 still reports a connection: loopback handling under the sandbox proxy is UNVERIFIED. Ask your instructor for the rehearsed destination and pass it with `--net-target`.

**Scoring rubric (100):**

| Item | Points |
|------|--------|
| Part A: static checklist (sandbox on 7, fail closed 7, no unsandboxed opt-out 7, allowed domains 7, allowWrite 5, denyRead 5, denyWrite 3, deny rules for secrets 4, deny rules for curl and wget 3, no blanket allow 4, MCP allowlist 8) | 60 |
| Part B: attack script, 10 for each blocked attack | 40 |

**Fallback scoring (no OS sandbox):** Part B attacks 1 to 3 are scored 5 each from the checker's PREDICTED outcomes. Attack 4 is always scored live because it needs no sandbox. The maximum is 85. Say so before the lab begins.

**Facilitator note:** Traps in the starter: `sandbox.enabled` false; `allowUnsandboxedCommands` true; `allowedDomains` is `*`; `allowWrite` is `~` (the parent folder of the project is usually under it, so attack 1 succeeds); `denyRead` empty; `Bash(*)` in the allow list; `enableAllProjectMcpServers` true; and `shadow-sync` declared in `.mcp.json` though it is not approved. Attack 4 can only be fixed in `app.py`: a regular-expression check of the name and `subprocess.run` with a list argument. Teach the point that a sandbox does not stop an in-project command. The planted secret is `FAKE-TOKEN-DO-NOT-USE`. **Needs rehearsal:** the live sandbox behavior on the class machines, the parent object of `allowUnsandboxedCommands`, the nesting of the filesystem lists under `sandbox.filesystem`, the MCP allowlist setting names, the deny rule syntax, and loopback handling for attack 2. The static checker is the part that works everywhere. Do not promise live results on any specific machine.
