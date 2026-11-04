# Lab 3 Brief: Harden report-archiver

## Approved lists (from the security team)

Network destinations the project may reach:

- `pypi.org`
- `files.pythonhosted.org`
- `api.example.com`

MCP servers approved for this project:

- `docs-search`
- `ticket-bridge`

Everything else is not approved. `shadow-sync` has not been vetted.

## Protected material

- `config/secrets.env` (fake placeholder secrets) and any `.env` file
- `~/.ssh`
- the project's own `.claude/` folder and `.mcp.json`

## Deliverables

1. A hardened `.claude/settings.json` and `.mcp.json` in your working copy.
2. A fixed `app.py`.
3. `lab3_notes.md` with: the controls you would move to managed settings and why; what your configuration does NOT stop; and one gap that hooks or MCP servers leave open.
4. Output of `check_settings.py` and of `attack_simulation.py` (or a note that no OS sandbox was available).

## Copy the project

```
mkdir -p ~/work && cp -r $FILES/lab3-harden/vuln-app ~/work/vuln-app
cd ~/work/vuln-app
git init -q && git add -A && git commit -qm "baseline"
```

Commit locally only. Nothing in this course pushes to a remote. Run `python3 attack_simulation.py` from inside a Claude Code session started in `~/work/vuln-app`, so the Bash tool, not your shell, is what is tested.
