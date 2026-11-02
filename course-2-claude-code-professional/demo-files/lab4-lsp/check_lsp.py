#!/usr/bin/env python3
"""Static check of a plugin's .lsp.json. `claude plugin validate` does not read this file,
and Claude Code skips the WHOLE file when any entry is invalid, so check it yourself.

Usage:
    python check_lsp.py PLUGIN_DIR_OR_LSP_JSON

Checks (from the plugin components documentation):
  * the file is valid JSON and maps server names directly to configs, with no wrapper object
  * each entry has a "command" and it is found on your PATH
  * each entry has "extensionToLanguage" with at least one extension, each starting with "."
  * two entries do not claim the same extension (the first registered wins)

Exit code 0 when there are no FAIL lines, 1 otherwise. A passing check means the file is
well formed and the binary is on the PATH of THIS shell. It does not start the server
(use lsp_smoke.py) and it does not prove Claude Code can see the same PATH.
"""
import json
import shutil
import sys
from pathlib import Path


def main(argv):
    if len(argv) != 1:
        print(__doc__)
        return 2
    p = Path(argv[0])
    f = p / ".lsp.json" if p.is_dir() else p
    if not f.exists():
        print(f"[FAIL] {f} does not exist")
        return 1
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"[FAIL] not valid JSON: {exc}")
        return 1
    fails = 0

    def fail(msg):
        nonlocal fails
        fails += 1
        print(f"[FAIL] {msg}")

    if not isinstance(data, dict) or not data:
        fail("expected an object that maps server names to configs")
        return 1
    if "mcpServers" in data or "servers" in data or "lspServers" in data:
        fail("found a wrapper key. The file maps each server name directly to its config, with no wrapper object.")
    claimed = {}
    for name, cfg in data.items():
        if not isinstance(cfg, dict):
            fail(f"'{name}' is not an object")
            continue
        cmd = cfg.get("command")
        if not cmd:
            fail(f"'{name}': no \"command\"")
        elif shutil.which(cmd) is None:
            fail(f"'{name}': \"{cmd}\" is not on the PATH of this shell. Claude Code starts the command by name from the PATH.")
        else:
            print(f"[ok  ] '{name}': \"{cmd}\" found at {shutil.which(cmd)}")
        ext = cfg.get("extensionToLanguage")
        if not isinstance(ext, dict) or not ext:
            fail(f"'{name}': \"extensionToLanguage\" needs at least one entry")
            continue
        for e in ext:
            if not str(e).startswith("."):
                fail(f"'{name}': extension \"{e}\" must start with a dot (for example \".py\")")
            elif e in claimed:
                fail(f"'{name}': extension {e} is also claimed by '{claimed[e]}'. The first registered wins.")
            else:
                claimed[e] = name
        if all(str(e).startswith(".") for e in ext):
            print(f"[ok  ] '{name}': handles {', '.join(ext)}")
    print(f"\n{fails} FAIL. " + ("If you ran this on a fixed file, now test the server with lsp_smoke.py." if not fails else "Fix these, then run it again."))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
