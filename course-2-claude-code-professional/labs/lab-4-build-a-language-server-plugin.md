# Lab 4: Build a Language Server Plugin

**Course:** Claude Code Professional
**Duration:** 75 minutes
**Format:** Instructor-led, in-class hands-on lab (300 level)

> Part of **[Claude Code Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

## Prerequisites

- [ ] Python 3.11 or later
- [ ] `claude` signed in to a paid Anthropic account
- [ ] `$FILES/lab4-lsp` from your instructor: `pylsp-plugin-starter/`, `sample-project/`, `check_lsp.py`, `lsp_smoke.py`
- [ ] The official Python code intelligence plugin **disabled** for the duration of this lab
- [ ] A terminal session, not a cloud session — Claude Code does not start plugin language servers in cloud sessions

---

## Overview

A language server plugin tells Claude Code which command starts a language server and which file extensions it handles, in a `.lsp.json` file at the plugin root. It does not install the server. With a server running, Claude sees the errors and warnings the server reports after each edit, and gets an `LSP` tool for finding definitions and references by symbol.

Claude Code skips the whole `.lsp.json` file when any entry is invalid, and `claude plugin validate` does not read this file, **so a bad file looks like a working plugin that does nothing.** That failure mode is the point of this lab.

The server here is `pylsp` (the Python LSP Server). Python already has an official code intelligence plugin built on a different server. If an official plugin covers your language, install that instead of writing your own. This lab writes the file by hand for practice, so do not have the official Python plugin enabled while you work. If two servers claim the same extension, the first registered wins.

---

## Part 1: Install the Language Server (about 10 minutes)

Goal: `pylsp` on the PATH of the shell you start `claude` from.

### Step 1: Install pylsp with Its Check Extras

```bash
pip install "python-lsp-server[pyflakes,pycodestyle]"
```

The two extras add the checks that produce diagnostics. Without them the server starts and reports nothing.

**Expected result:** the install completes in a virtual environment or your user environment.

### Step 2: Confirm It Is on the PATH

```bash
pylsp --help
```

On Windows, check with `Get-Command pylsp` in PowerShell or `where pylsp`.

**Acceptance criteria:** `pylsp --help` runs from the shell you will use for `claude`.

> **Hint:** if you used a virtual environment, activate it in the same shell before you start `claude`.

---

## Part 2: Reproduce the Symptom (about 10 minutes)

Goal: see that the plugin loads and does nothing.

### Step 3: Validate, Then Watch Nothing Happen

```bash
claude plugin validate pylsp-plugin-starter
```

Then start a session with `claude --plugin-dir pylsp-plugin-starter` in `sample-project`, ask Claude to add a line that uses an undefined name to `app/report.py`, and look for a diagnostics line.

**Acceptance criteria:** you can state what `validate` said, what the session did, and where the real error is shown — the `/plugin` Errors tab, and `claude --debug`.

> **Key Insight:** a passing `validate` tells you nothing about `.lsp.json`. It does not read that file.

---

## Part 3: Find and Fix the Configuration (about 15 minutes)

Goal: a `.lsp.json` that loads.

### Step 4: Locate the Fault

```bash
python3 check_lsp.py pylsp-plugin-starter
```

Use the output, the Errors tab and the documentation together.

**Expected result:** `check_lsp.py` names the invalid entry.

### Step 5: Fix the File and Write the Root Cause

**Acceptance criteria:** `check_lsp.py` reports no FAIL lines, plus a root-cause note of two sentences: what was wrong, and why the whole file was skipped.

> **Hint:** read the plugin components documentation for the exact shape of `extensionToLanguage`.

> **Common Pitfall:** edits to `.lsp.json` do nothing until you restart the session, or run `/reload-plugins` where it applies.

---

## Part 4: Test the Server Without Claude (about 10 minutes)

Goal: show that the server and your config work before you blame Claude Code.

### Step 6: Run the Smoke Test

```bash
python3 lsp_smoke.py pylsp-plugin-starter sample-project/app/report.py
```

Then ask for a definition with `--definition LINE:COL` at a use of `rate_for` in `app/billing.py`.

**Acceptance criteria:** diagnostics for `app/report.py` include an unused import and an undefined name. A definition lookup for `rate_for` points at `app/tax.py`.

---

## Part 5: Prove It Inside a Session (about 20 minutes)

Goal: diagnostics and navigation in Claude Code.

### Step 7: Trigger Diagnostics from an Edit

Restart the session with `claude --plugin-dir`. Ask Claude to make an edit that introduces an error, then fix it.

**Acceptance criteria:** after an edit, the conversation shows a `Found N new diagnostic issues` line. Open it with Ctrl+O and read the issue.

> **Hint:** the server starts the first time Claude edits a file with one of your extensions. If the binary was missing when the session started, start a new session from a shell where it is on the PATH.

### Step 8: Ask a Navigation Question

Ask where `rate_for` is defined and what calls it.

**Acceptance criteria:** the transcript shows Claude using the `LSP` tool instead of searching text. Capture it.

---

## Part 6: Stretch — Meet the Conflict Case (about 10 minutes, optional)

Goal: see what happens when two servers claim one extension.

### Step 9: Add a Conflicting Entry

Add a second entry that claims `.py` and read the warning the Errors tab shows. Restore the file afterwards.

**Acceptance criteria:** you can say which server handles `.py` files, and why.

---

## Part 7: Checkpoint

### Step 10: Verify Your Progress

- [ ] `pylsp --help` runs from the shell you start `claude` from
- [ ] `pylsp` was installed with the pyflakes and pycodestyle extras
- [ ] You reproduced the silent failure: plugin loads, nothing happens
- [ ] You can name where the real error is reported, and why `validate` missed it
- [ ] `check_lsp.py` reports no FAIL lines
- [ ] A two-sentence root-cause note explains why one bad entry skipped the whole file
- [ ] The smoke test shows an unused import and an undefined name in `app/report.py`
- [ ] The smoke test resolves `rate_for` to `app/tax.py`
- [ ] An in-session edit produced a `Found N new diagnostic issues` line, and you read the issue
- [ ] A navigation question shows Claude using the `LSP` tool, captured in the transcript
- [ ] Optional: the extension-conflict warning read and explained

---

## Troubleshooting Reference

| Issue | Symptom | Solution |
|---|---|---|
| Server not found | No diagnostics and no error line | The server is not on the PATH of the shell that started `claude`, or `pylsp` was installed without its checks. `claude --debug` logs `LSP server <name> failed to start` when the binary is missing |
| PATH mismatch | `Executable not found in $PATH` in the Errors tab | Install the server, then start a new session from a shell where it is found |
| Whole file skipped | `Invalid LSP server config for ".lsp.json"` in the Errors tab | An entry is invalid and the entire file was skipped. Fix the entry |
| Validator is no help | `claude plugin validate` passes and nothing works | It does not read `.lsp.json`. Use `check_lsp.py` and the Errors tab |
| Edits have no effect | Config changes do nothing | Restart the session, or run `/reload-plugins` where it applies |
| Works outside, not inside | Diagnostics in the smoke test but not the session | The shell that started `claude` has a different PATH from the one you tested in |
| Cloud session silent | No diagnostics in a cloud session | Claude Code does not start plugin language servers in cloud sessions. Use a terminal session |
| Server disconnects | Claude Code drops the server | A language server must log to standard error. One that prints logs to standard output gets disconnected |

---

## Scoring Rubric (100 points)

| Item | Points |
|---|---|
| Root cause stated correctly, with the reason the whole file was skipped | 15 |
| `check_lsp.py` has no FAIL lines | 20 |
| Smoke test shows the diagnostics and the definition | 15 |
| In-session diagnostics line shown, and the issue read | 20 |
| In-session navigation shown through the `LSP` tool | 15 |
| Explains why `validate` passed, and where an invalid file is reported | 10 |
| Stretch: conflict warning read and explained | 5 |

---

## What You Built

In 75 minutes, you:

- Met a failure mode that looks like success: a plugin that validates, loads, and silently does nothing
- Found the one invalid entry that caused Claude Code to skip an entire configuration file
- Proved the server and your config worked outside Claude Code first, before blaming the tool
- Got diagnostics firing on edits inside a live session, and watched Claude use the `LSP` tool for navigation instead of grepping text

---

## What's Next

Lab 5, Enterprise Migration Runbook, is the take-home lab. It moves from configuring one machine to planning a migration across an organization.

---

## Facilitator Notes

The default misconfiguration (variant A) is in `pylsp-plugin-starter/.lsp.json`: the keys of `extensionToLanguage` are `py` and `pyi`, with no leading dot. That makes the whole file invalid, so the plugin loads with no language server. `facilitator/lsp.fixed.json` is the fix. For a second round or a class that finishes early, swap in `facilitator/lsp.variant-b-wrong-binary.json`, whose `command` is `python-lsp-server`, a name that is not on the PATH, so the symptom is `LSP server python-pylsp failed to start` in the debug log. `check_lsp.py` reports both.

Confirmed locally while building this lab: `pylsp` started with no arguments serves the protocol on standard input and output, and with `python-lsp-server` 1.15.0 and its pyflakes and pycodestyle extras the smoke test reports `'json' imported but unused`, `'os' imported but unused` and `undefined name 'grand_total'` for `app/report.py`, and a definition for `rate_for` in `app/tax.py`. Rehearse the in-session part on your class machines: the `Found N new diagnostic issues` line is documented, and the `LSP` tool is documented, and neither has been run for this lab.

Why Python and `pylsp`: students already have Python, and the server is a free install. An official Python plugin exists, so say plainly that in real work you would install it, and that this lab is about authoring the file. For a student who works in another language, let them pick it if a free server exists, and then make the one deliberate misconfiguration yourself.

Unconfirmed: the nine LSP operation names in the old outline. Do not teach them. The documentation names diagnostics and code navigation, and the course sticks to those words. Rehearse what the `LSP` tool reports on your version and say that it is read-only.

---

*Lab 4 Complete*
