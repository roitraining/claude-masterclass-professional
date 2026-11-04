#!/usr/bin/env python3
"""List leftover Console credentials on this machine, by NAME only. Values are never printed.

Usage:
    python3 leftover_credentials_check.py [PROJECT_DIR ...]

Looks for:
  * environment variables named ANTHROPIC_API_KEY or CLAUDE_CODE_OAUTH_TOKEN in this shell
  * an "apiKeyHelper" key in ~/.claude/settings.json and in each PROJECT_DIR's
    .claude/settings.json and .claude/settings.local.json
  * lines in common shell profile files that mention ANTHROPIC_API_KEY
  * a "forceLoginOrgUUID" key in the same settings files (informational)

Read-only. Makes no network calls. A clean result here does not prove the migration worked:
finish with /login, choose the Enterprise organization, and check /status.
"""
import json
import os
import sys
from pathlib import Path

ENV_NAMES = ("ANTHROPIC_API_KEY", "CLAUDE_CODE_OAUTH_TOKEN")
PROFILES = (".bashrc", ".zshrc", ".profile", ".bash_profile", ".zprofile")


def settings_keys(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else {}


def main(argv):
    home = Path.home()
    found = 0
    for name in ENV_NAMES:
        if os.environ.get(name):
            print(f"[FOUND] environment variable {name} is set in this shell (value not shown)")
            found += 1
    files = [home / ".claude" / "settings.json"]
    for d in argv:
        files += [Path(d) / ".claude" / "settings.json", Path(d) / ".claude" / "settings.local.json"]
    for f in files:
        data = settings_keys(f)
        if data is None:
            continue
        if "apiKeyHelper" in data:
            print(f"[FOUND] {f}: apiKeyHelper is set (value not shown)")
            found += 1
        if "forceLoginOrgUUID" in data:
            print(f"[info ] {f}: forceLoginOrgUUID is set")
    for name in PROFILES:
        p = home / name
        if p.exists():
            for n, line in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                if "ANTHROPIC_API_KEY" in line and not line.lstrip().startswith("#"):
                    print(f"[FOUND] {p}:{n} mentions ANTHROPIC_API_KEY (line not shown)")
                    found += 1
    if os.name == "nt":
        print("[info ] Windows: user and system environment variables are not scanned here. Check System Properties, Environment Variables.")
    print(f"\n{found} leftover credential reference(s) found.")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
