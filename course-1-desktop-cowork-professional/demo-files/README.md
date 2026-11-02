# demo-files

Everything the Professional 1 demos and labs use. In `demos.md` and the lab guides in `labs/`, `$FILES` means this folder.

- `starter-server/`: a working local MCP server template (Python standard library only), its self-test, an extension manifest, and a fallback packer.
- `products/`: four plugin products. Each has `BRIEF.md`, a `data/` folder with a messy fictional dataset, and an `ANSWER-KEY.md` that lists the planted traps. Hand students the brief and the data. Keep the answer keys for the checkpoints.
  - `1-board-pack-builder/`, `2-close-the-books-copilot/`, `3-client-meeting-prep-desk/`, `4-incident-commander/`
- `demo-snippets/`: ready-made skill, command, agent, and `.mcp.json` files for the instructor's `records-desk` demo plugin (Demos 1 to 3).
- `untrusted-plugin/`: a fictional third-party plugin with a hook, a `bin/` script, an unpinned server, and a hidden skill instruction, for the Demo 7 review. Never install it.
- `autopsy-plugin/`: a deliberately flawed plugin with six planted defects. It passes `claude plugin validate`. `AUTOPSY-WORKSHEET.md` is the student worksheet.
- `gauntlet/`: the scorecard runner, scoring rules, eval suites and mocks, adversarial pack, security checklist, and sample reports.
- `templates/`: SETUP.md, CHANGELOG.md, release note, self-demo outline, and a security review template.

Every person, company, system, and figure is fictional. The one planted secret is the placeholder `FAKE-TOKEN-DO-NOT-USE-0000` in `autopsy-plugin/server/config.json`. No file contains a real credential.

Tested before delivery: `claude plugin validate` and `claude plugin details` on the autopsy plugin, the starter server self-test, and the runner's static checks and dry run. Not tested: a paid eval run (the build environment was not signed in), the `.mcpb` install into Claude Desktop, and Cowork behavior. Rehearse those on the class machine.
