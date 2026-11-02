# Lab 4: Build a Language Server Plugin

> Part of **[Claude Code Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

**Learning objective:** Configure a language server plugin that gives Claude diagnostics and code navigation, and find and fix a deliberate misconfiguration. Time: 75 minutes.

**Files:** `$FILES/lab4-lsp`: `pylsp-plugin-starter/`, `sample-project/`, `check_lsp.py`, `lsp_smoke.py`.

**Context:** A language server plugin tells Claude Code which command starts a language server and which file extensions it handles, in a `.lsp.json` file at the plugin root. It does not install the server. With a server running, Claude sees the errors and warnings the server reports after each edit, and gets an `LSP` tool for finding definitions and references by symbol. Claude Code skips the whole `.lsp.json` file when any entry is invalid, and `claude plugin validate` does not read this file, so a bad file looks like a working plugin that does nothing.

The server in this lab is `pylsp` (the Python LSP Server). Python already has an official code intelligence plugin built on a different server. If an official plugin covers your language, install that instead of writing your own. This lab writes the file by hand for practice, so do not have the official Python plugin enabled while you work. If two servers claim the same extension, the first registered wins.

**Steps:**

1. **Install the server (about 10 minutes).** Goal: `pylsp` on the PATH of the shell you start `claude` from.
   - `pip install "python-lsp-server[pyflakes,pycodestyle]"` in a virtual environment or your user environment. The two extras add the checks that produce diagnostics.
   - Acceptance criteria: `pylsp --help` runs from the shell you will use for `claude`. On Windows, check with `Get-Command pylsp` in PowerShell or `where pylsp`.
   - Hint: if you used a virtual environment, activate it in the same shell before you start `claude`.

2. **Reproduce the symptom (about 10 minutes).** Goal: see that the plugin loads and does nothing.
   - Run `claude plugin validate pylsp-plugin-starter`. Then start a session with `claude --plugin-dir pylsp-plugin-starter` in `sample-project`, ask Claude to add a line that uses an undefined name to `app/report.py`, and look for a diagnostics line.
   - Acceptance criteria: you can state what `validate` said, what the session did, and where the real error is shown (the `/plugin` Errors tab, and `claude --debug`).

3. **Find and fix (about 15 minutes).** Goal: a `.lsp.json` that loads.
   - Use `python check_lsp.py pylsp-plugin-starter`, the Errors tab and the documentation. Fix the file.
   - Acceptance criteria: `check_lsp.py` reports no FAIL lines. A root-cause note of two sentences: what was wrong, and why the whole file was skipped.
   - Hint: read the plugin components documentation for the exact shape of `extensionToLanguage`.

4. **Test the server without Claude (about 10 minutes).** Goal: show that the server and your config work before you blame Claude Code.
   - `python lsp_smoke.py pylsp-plugin-starter sample-project/app/report.py`, then ask for a definition with `--definition LINE:COL` at a use of `rate_for` in `app/billing.py`.
   - Acceptance criteria: diagnostics for `app/report.py` include an unused import and an undefined name. A definition lookup for `rate_for` points at `app/tax.py`.

5. **Prove it inside a session (about 20 minutes).** Goal: diagnostics and navigation in Claude Code.
   - Restart the session with `claude --plugin-dir`. Ask Claude to make an edit that introduces an error, then fix it. Ask where `rate_for` is defined and what calls it.
   - Acceptance criteria:
     - After an edit, the conversation shows a `Found N new diagnostic issues` line. Open it with Ctrl+O and read the issue.
     - For the navigation question, the transcript shows Claude using the `LSP` tool instead of searching text. Capture it.
   - Hints: the server starts the first time Claude edits a file with one of your extensions. If the binary was missing when the session started, start a new session from a shell where it is on the PATH.

6. **Stretch (about 10 minutes, optional).** Goal: meet the conflict case.
   - Add a second entry that claims `.py` and read the warning the Errors tab shows. Restore the file.
   - Acceptance criteria: you can say which server handles `.py` files and why.

**Checkpoint:** Working diagnostics and navigation inside a session, with the evidence from steps 4 and 5.

**Common problems:**

- No diagnostics and no error line: the server is not on the PATH of the shell that started `claude`, or `pylsp` was installed without its checks. `claude --debug` logs `LSP server <name> failed to start` when the binary is missing.
- `Executable not found in $PATH` in the Errors tab: the same cause. Install the server, then start a new session from a shell where it is found.
- `Invalid LSP server config for ".lsp.json"` in the Errors tab: an entry is invalid and the whole file was skipped.
- `claude plugin validate` passes and nothing works: it does not read `.lsp.json`.
- Edits to `.lsp.json` do nothing: restart the session, or run `/reload-plugins` where it applies.
- Diagnostics appear in the smoke test and not in the session: the shell that started `claude` has a different PATH from the one you tested in.
- A cloud session shows no diagnostics: Claude Code does not start plugin language servers in cloud sessions. Use a terminal session.
- The server prints logs to standard output and Claude Code disconnects it: a language server must log to standard error.

**Scoring rubric (100 points):**

| Item | Points |
|---|---|
| Root cause stated correctly, with the reason the whole file was skipped | 15 |
| `check_lsp.py` has no FAIL lines | 20 |
| Smoke test shows the diagnostics and the definition | 15 |
| In-session diagnostics line shown, and the issue read | 20 |
| In-session navigation shown through the `LSP` tool | 15 |
| Explains why `validate` passed, and where an invalid file is reported | 10 |
| Stretch: conflict warning read and explained | 5 |

**Facilitator note:** The default misconfiguration (variant A) is in `pylsp-plugin-starter/.lsp.json`: the keys of `extensionToLanguage` are `py` and `pyi`, with no leading dot. That makes the whole file invalid, so the plugin loads with no language server. `facilitator/lsp.fixed.json` is the fix. For a second round or a class that finishes early, swap in `facilitator/lsp.variant-b-wrong-binary.json`, whose `command` is `python-lsp-server`, a name that is not on the PATH, so the symptom is `LSP server python-pylsp failed to start` in the debug log. `check_lsp.py` reports both.

Confirmed locally while building this lab: `pylsp` started with no arguments serves the protocol on standard input and output, and with `python-lsp-server` 1.15.0 and its pyflakes and pycodestyle extras the smoke test reports `'json' imported but unused`, `'os' imported but unused` and `undefined name 'grand_total'` for `app/report.py`, and a definition for `rate_for` in `app/tax.py`. Rehearse the in-session part on your class machines: the `Found N new diagnostic issues` line is documented, and the `LSP` tool is documented, and neither has been run for this lab.

Why Python and `pylsp`: students already have Python, and the server is a free install. An official Python plugin exists, so say plainly that in real work you would install it, and that this lab is about authoring the file. For a student who works in another language, let them pick it if a free server exists, and then make the one deliberate misconfiguration yourself.

Unconfirmed: the nine LSP operation names in the old outline. Do not teach them. The documentation names diagnostics and code navigation, and the course sticks to those words. Rehearse what the `LSP` tool reports on your version and say that it is read-only.
