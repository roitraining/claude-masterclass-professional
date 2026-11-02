# Plugin Autopsy worksheet

Plugin under review: `autopsy-plugin` (named `expense-digest`). It passes `claude plugin validate` and it still has six defects. Find each one, write down the evidence, and fix it in your copy.

Work in a copy: `cp -r autopsy-plugin ~/work/expense-digest` (use Copy-Item on Windows PowerShell).

Tools you can use: `claude plugin validate`, `claude --plugin-dir <path> plugin details expense-digest`, and your eyes. Not every defect shows up in a tool.

| # | Area | What you found (file and line) | Evidence | Fix you made |
|---|---|---|---|---|
| 1 | Trigger | | | |
| 2 | Permissions | | | |
| 3 | Setup | | | |
| 4 | Context cost | | | |
| 5 | Secrets | | | |
| 6 | Versioning | | | |

After the fixes:

- [ ] `claude plugin validate` still passes.
- [ ] Always-on tokens went down. Before: ______  After: ______
- [ ] You can state which surface each fix matters most on (chat, Cowork, Claude Code).
- [ ] You wrote a CHANGELOG entry and bumped the version in all places that carry it.
