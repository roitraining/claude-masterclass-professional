# Demo 8: Wire In a Language Server

**Course:** Claude Code Professional: Pipelines, Plugins and Enterprise Operations (Claude MasterClass Professional, Course 2)
**Demo:** 8 of 9
**Time:** about 13 minutes

> Part of **[Claude Code Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Configure a language server plugin, show diagnostics and navigation working, and show that `claude plugin validate` does not read `.lsp.json`. Time: about 13 minutes.

**Files:** [`$FILES/lab4-lsp/facilitator/pylsp-plugin-fixed`](../demo-files/lab4-lsp/facilitator/pylsp-plugin-fixed), [`$FILES/lab4-lsp/sample-project`](../demo-files/lab4-lsp/sample-project), [`$FILES/lab4-lsp/check_lsp.py`](../demo-files/lab4-lsp/check_lsp.py), [`$FILES/lab4-lsp/lsp_smoke.py`](../demo-files/lab4-lsp/lsp_smoke.py).

**Context:** A language server plugin is an `.lsp.json` file at the plugin root. It maps a server name to a `command` (a binary found on your PATH), optional `args`, and `extensionToLanguage`. It does not install the server. With a server running, Claude gets diagnostics after edits and an `LSP` tool for code navigation. If an official code intelligence plugin covers your language, install that instead. This demo writes the file by hand to show what is inside it.

**Steps:**

1. Install the server:

```
pip install "python-lsp-server[pyflakes,pycodestyle]"
pylsp --help
```

2. Show `.lsp.json` in `pylsp-plugin-fixed`. Point at the command, and the dots on the extensions. Run `claude plugin validate` on the plugin and note that it passes. Say it did not read this file.
3. `python check_lsp.py $FILES/lab4-lsp/facilitator/pylsp-plugin-fixed`
4. Test the server with no Claude involved:

```
python lsp_smoke.py $FILES/lab4-lsp/facilitator/pylsp-plugin-fixed $FILES/lab4-lsp/sample-project/app/report.py
```

5. In `sample-project`, start `claude --plugin-dir $FILES/lab4-lsp/facilitator/pylsp-plugin-fixed`. Ask Claude to add a line using an undefined name to `app/report.py`. Look for the `Found N new diagnostic issues` line and press Ctrl+O.
6. Ask where `rate_for` is defined and what calls it. Show that Claude uses the `LSP` tool and not a text search.
7. Break it on purpose: remove a dot from an extension in a copy, run `check_lsp.py`, and show the `/plugin` Errors tab.

**Expected result:** The smoke test prints `'json' imported but unused`, `'os' imported but unused` and `undefined name 'grand_total'` for `app/report.py`. In the session an edit produces the diagnostics line, and the navigation question is answered from the language server.

**Instructor note:** Steps 1 to 4 and 7 use no credits. Steps 5 and 6 use credits. The smoke test was run while building the files, with `python-lsp-server` 1.15.0. The in-session steps have not been run. Rehearse them, and note what the `LSP` tool reports on your version. The documentation names diagnostics and code navigation. Do not name specific protocol operations, because the old outline's list of nine is unconfirmed. Plugin language servers do not start in cloud sessions. Fallback with no model: steps 1 to 4 and 7 alone. Without an installed server, show the smoke test output from a rehearsal run.

**Why this matters:** Claude with a language server sees the type error before the build does, and navigates by symbol. The file is short and easy to get subtly wrong, and nothing but the Errors tab tells you.

---

**Previous:** [Demo 7: Evaluate a Plugin With a Test Suite](demo-7-evaluate-a-plugin-with-a-test-suite.md) · **Next:** [Demo 9: Plan a Console to Enterprise Cutover](demo-9-plan-a-console-to-enterprise-cutover.md)


*Demo 8 of 9*
