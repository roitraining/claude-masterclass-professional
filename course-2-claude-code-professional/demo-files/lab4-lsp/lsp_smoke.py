#!/usr/bin/env python3
"""Talk to the language server your .lsp.json configures, without Claude Code.

Usage:
    python lsp_smoke.py PLUGIN_DIR_OR_LSP_JSON FILE [--definition LINE:COL] [--wait 8]

It picks the .lsp.json entry whose extensionToLanguage claims FILE's extension, starts
that command, opens FILE over the Language Server Protocol, prints the diagnostics the
server publishes, and optionally asks where the symbol at LINE:COL (1-based) is defined.
No model calls, no network.

If no entry claims the extension, it says so. That is the same reason Claude Code would
show no diagnostics for the file.

Limits: this checks the server and your config, not Claude Code itself. A passing smoke
test then needs a session test (edit a file, look for the diagnostics line, ask for a
definition).
"""
import json
import queue
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path


def frame(obj):
    body = json.dumps(obj).encode("utf-8")
    return b"Content-Length: " + str(len(body)).encode() + b"\r\n\r\n" + body


def reader(stream, q):
    try:
        while True:
            length = None
            while True:
                line = stream.readline()
                if not line:
                    return
                line = line.strip()
                if not line:
                    break
                if line.lower().startswith(b"content-length:"):
                    length = int(line.split(b":")[1])
            if length is None:
                continue
            q.put(json.loads(stream.read(length).decode("utf-8")))
    except Exception as exc:  # pragma: no cover
        q.put({"reader_error": str(exc)})


def wait_for(q, pred, timeout):
    end = time.time() + timeout
    while time.time() < end:
        try:
            msg = q.get(timeout=0.2)
        except queue.Empty:
            continue
        if pred(msg):
            return msg
    return None


def main(argv):
    rest = list(argv)
    definition, wait = None, 8.0
    if "--definition" in rest:
        i = rest.index("--definition")
        definition = rest[i + 1]
        del rest[i:i + 2]
    if "--wait" in rest:
        i = rest.index("--wait")
        wait = float(rest[i + 1])
        del rest[i:i + 2]
    if len(rest) != 2:
        print(__doc__)
        return 2
    cfg_path = Path(rest[0])
    cfg_path = cfg_path / ".lsp.json" if cfg_path.is_dir() else cfg_path
    target = Path(rest[1]).resolve()
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    entry = None
    for name, c in cfg.items():
        if target.suffix in (c.get("extensionToLanguage") or {}):
            entry, entry_name = c, name
            break
    if entry is None:
        print(f"No server in {cfg_path.name} claims '{target.suffix}'. Check extensionToLanguage (each key must start with a dot).")
        return 1
    exe = shutil.which(entry["command"])
    if exe is None:
        print(f"'{entry['command']}' is not on the PATH of this shell. Install the server or fix the command.")
        return 1
    language = entry["extensionToLanguage"][target.suffix]
    root = target.parent
    while root.parent != root and not any((root / m).exists() for m in (".git", "README.md", "pyproject.toml")):
        root = root.parent
    if (root.parent / "README.md").exists() and root.name == "app":
        root = root.parent
    print(f"Server '{entry_name}': {exe} {' '.join(entry.get('args', []))}")
    proc = subprocess.Popen([exe, *entry.get("args", [])], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL, cwd=str(root))
    q = queue.Queue()
    threading.Thread(target=reader, args=(proc.stdout, q), daemon=True).start()

    def send(obj):
        proc.stdin.write(frame(obj))
        proc.stdin.flush()

    send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
          "params": {"processId": None, "rootUri": root.as_uri(),
                     "capabilities": {"textDocument": {"publishDiagnostics": {}, "definition": {}}}}})
    init = wait_for(q, lambda m: m.get("id") == 1, wait)
    if init is None:
        print("The server did not answer initialize. Its stdout may carry non-protocol output, or it is not a stdio server.")
        proc.kill()
        return 1
    caps = (init.get("result") or {}).get("capabilities", {})
    print(f"initialize ok. definitionProvider: {bool(caps.get('definitionProvider'))}, referencesProvider: {bool(caps.get('referencesProvider'))}")
    send({"jsonrpc": "2.0", "method": "initialized", "params": {}})
    uri = target.as_uri()
    send({"jsonrpc": "2.0", "method": "textDocument/didOpen",
          "params": {"textDocument": {"uri": uri, "languageId": language, "version": 1,
                                      "text": target.read_text(encoding="utf-8")}}})
    diag = wait_for(q, lambda m: m.get("method") == "textDocument/publishDiagnostics"
                    and m["params"]["uri"].lower() == uri.lower() and m["params"]["diagnostics"], wait)
    if diag is None:
        print("No diagnostics published within the wait. The file may be clean, the server may need more time (--wait 15), or the server may lack the plugin that produces diagnostics (for pylsp: pip install \"python-lsp-server[pyflakes,pycodestyle]\").")
    else:
        for d in diag["params"]["diagnostics"]:
            print(f"  diagnostic {d['range']['start']['line'] + 1}:{d['range']['start']['character'] + 1}  {d['message']}")
    if definition:
        line, col = (int(x) for x in definition.split(":"))
        send({"jsonrpc": "2.0", "id": 2, "method": "textDocument/definition",
              "params": {"textDocument": {"uri": uri}, "position": {"line": line - 1, "character": col - 1}}})
        res = wait_for(q, lambda m: m.get("id") == 2, wait)
        locs = (res or {}).get("result") or []
        locs = locs if isinstance(locs, list) else [locs]
        if not locs:
            print(f"  definition at {definition}: none found")
        for loc in locs:
            u = loc.get("uri") or loc.get("targetUri")
            r = loc.get("range") or loc.get("targetRange")
            print(f"  definition at {definition}: {u} line {r['start']['line'] + 1}")
    send({"jsonrpc": "2.0", "id": 3, "method": "shutdown", "params": None})
    wait_for(q, lambda m: m.get("id") == 3, 3)
    try:
        send({"jsonrpc": "2.0", "method": "exit"})
    except Exception:
        pass
    time.sleep(0.2)
    proc.kill()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
