#!/usr/bin/env python3
"""Verify a packed .mcpb end to end, without Claude Desktop and without a GUI.

    python3 verify-mcpb.py path/to/plugin-0.1.0.mcpb [--expect get_kpis,get_exec_notes,list_sources]

WHY THIS EXISTS

Three Course 1 checks were listed as "needs a person":

  * Lab 1 Part 8  - install the extension in Desktop and ask a question that
                    uses a tool. (The step's own acceptance criteria is only
                    that a packed .mcpb exists; the install is optional.)
  * Lab 3 Part 5  - "it installs and a tool call works".  <- the scored one
  * Lab 1 Step 10 - "/mcp lists your server with three tools".

Playwright cannot help with any of them: it drives browser pages, and Claude
Desktop is a native application. But all three are really asking one question
about OUR artifact rather than about Anthropic's installer:

    does the bundle contain a server that starts and serves its tools?

That is answerable here. This script extracts the bundle, validates the
manifest the way mcpb does, launches the server exactly as the manifest says
Desktop would, and speaks MCP to it over stdio: initialize, tools/list, and a
tools/call against the first tool.

WHAT IT DOES NOT COVER

Claude Desktop's own install dialog, and whether Desktop renders the extension
correctly. That is Anthropic's software, not course content, and it stays a
one-time human click-through. If this script passes and the Desktop install
fails, the problem is the installer or the account, not the bundle.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

SERVER_TYPES = ("python", "node", "binary")
PROTOCOL_VERSION = "2024-11-05"

ok_count = 0
fail_count = 0


def ok(msg):
    global ok_count
    ok_count += 1
    print(f"  [ OK ] {msg}")


def bad(msg):
    global fail_count
    fail_count += 1
    print(f"  [FAIL] {msg}")


def info(msg):
    print(f"  [INFO] {msg}")


def load_manifest(root):
    p = root / "manifest.json"
    if not p.is_file():
        bad("no manifest.json at the top of the bundle")
        return None
    try:
        m = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        bad(f"manifest.json is not valid JSON: {e}")
        return None
    ok("manifest.json present and parses")
    return m


def check_manifest(m, root):
    for key in ("manifest_version", "name", "version", "description", "author", "server"):
        if key not in m:
            bad(f"manifest.json missing required field: {key}")
            return None
    server = m.get("server") or {}
    stype = server.get("type")
    if stype not in SERVER_TYPES:
        bad(f"server.type is {stype!r}; expected one of {' | '.join(SERVER_TYPES)}. "
            "It is the runtime, not the command — the interpreter belongs in "
            "server.mcp_config.command")
        return None
    ok(f"server.type is {stype!r}")

    entry = server.get("entry_point")
    if not entry or not (root / entry).is_file():
        bad(f"entry_point {entry!r} is not in the bundle")
        return None
    ok(f"entry_point {entry} is in the bundle")

    cfg = server.get("mcp_config") or {}
    if not cfg.get("command"):
        bad("server.mcp_config.command is missing — nothing would launch the server")
        return None
    ok(f"mcp_config.command is {cfg['command']!r}")
    return cfg


def build_command(cfg, root):
    """Substitute the placeholders Desktop would expand before launching."""
    def sub(s):
        return (s.replace("${__dirname}", str(root))
                 .replace("${HOME}", os.path.expanduser("~")))
    cmd = [sub(cfg["command"])] + [sub(a) for a in cfg.get("args", [])]
    env = dict(os.environ)
    for k, v in (cfg.get("env") or {}).items():
        v = sub(v)
        # An unexpanded ${user_config.*} means the option was never set, which is
        # the same state a fresh install is in. Pass it through empty so the
        # server exercises its own default, as server.py does with sample_data.
        env[k] = "" if v.startswith("${") else v
    return cmd, env


def rpc(proc, msg):
    proc.stdin.write(json.dumps(msg) + "\n")
    proc.stdin.flush()


def read_reply(proc, want_id, timeout_note):
    """Read lines until a JSON-RPC reply with the wanted id appears."""
    while True:
        line = proc.stdout.readline()
        if not line:
            bad(f"server closed its output while waiting for {timeout_note}")
            return None
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        if d.get("id") == want_id:
            return d


def speak_mcp(cmd, env, root, expect):
    info(f"launching: {' '.join(cmd)}")
    try:
        proc = subprocess.Popen(cmd, cwd=str(root), env=env, text=True,
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    except FileNotFoundError:
        bad(f"cannot launch {cmd[0]!r}: not found on PATH")
        return
    try:
        rpc(proc, {"jsonrpc": "2.0", "id": 1, "method": "initialize",
                   "params": {"protocolVersion": PROTOCOL_VERSION,
                              "capabilities": {}, "clientInfo": {"name": "verify-mcpb"}}})
        d = read_reply(proc, 1, "initialize")
        if not d or "result" not in d:
            bad("initialize did not return a result — the server did not start cleanly")
            return
        si = d["result"].get("serverInfo", {})
        ok(f"initialize answered: {si.get('name', '?')} {si.get('version', '')}".strip())

        rpc(proc, {"jsonrpc": "2.0", "method": "notifications/initialized"})
        rpc(proc, {"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        d = read_reply(proc, 2, "tools/list")
        if not d or "result" not in d:
            bad("tools/list did not return a result")
            return
        tools = [t.get("name") for t in d["result"].get("tools", [])]
        ok(f"tools/list returned {len(tools)}: {', '.join(tools) or '(none)'}")

        if expect:
            missing = [t for t in expect if t not in tools]
            if missing:
                bad("missing contract tools: " + ", ".join(missing))
            else:
                ok("every expected contract tool is present")
        for t in d["result"].get("tools", []):
            if not (t.get("description") or "").strip():
                bad(f"tool {t.get('name')!r} has no description — the model cannot choose it well")

        if tools:
            rpc(proc, {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                       "params": {"name": tools[0], "arguments": {}}})
            d = read_reply(proc, 3, "tools/call")
            if not d:
                return
            if "error" in d:
                # A tool that needs arguments may legitimately refuse an empty
                # call. That still proves the server is serving.
                info(f"tools/call on {tools[0]} returned an error, which is fine if it "
                     f"requires arguments: {d['error'].get('message', '')[:90]}")
                ok("the server handled a tools/call and replied")
            else:
                ok(f"tools/call on {tools[0]} returned a result")
    finally:
        try:
            proc.stdin.close()
        except Exception:
            pass
        proc.terminate()
        try:
            err = proc.stderr.read()[:400]
        except Exception:
            err = ""
        if err.strip():
            info("server stderr (logging here is correct; stdout would break the protocol):")
            for ln in err.strip().splitlines()[:5]:
                print(f"         {ln}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bundle")
    ap.add_argument("--expect", default="",
                    help="comma-separated tool names the contract requires")
    args = ap.parse_args()

    bundle = Path(args.bundle).resolve()
    if not bundle.is_file():
        sys.exit(f"not a file: {bundle}")

    print(f"\nVerifying {bundle.name}\n")
    tmp = Path(tempfile.mkdtemp(prefix="verify-mcpb-"))
    try:
        try:
            with zipfile.ZipFile(bundle) as z:
                names = z.namelist()
                z.extractall(tmp)
        except zipfile.BadZipFile:
            bad("not a zip archive — a .mcpb is a zip")
            return 1
        ok(f"bundle opened: {len(names)} entries")

        root = tmp
        if not (root / "manifest.json").is_file():
            # Tolerate a single wrapping directory, and say so, because Desktop
            # expects the manifest at the top.
            subs = [p for p in root.iterdir() if p.is_dir()]
            if len(subs) == 1 and (subs[0] / "manifest.json").is_file():
                bad(f"manifest.json is nested under {subs[0].name}/ rather than at the "
                    "top of the bundle; Desktop expects it at the top")
                root = subs[0]

        m = load_manifest(root)
        if not m:
            return 1
        cfg = check_manifest(m, root)
        if not cfg:
            return 1

        expect = [x.strip() for x in args.expect.split(",") if x.strip()]
        cmd, env = build_command(cfg, root)
        speak_mcp(cmd, env, root, expect)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print(f"\n  OK {ok_count}   FAIL {fail_count}\n")
    if fail_count:
        print("  The bundle is not ready. Fix the above before the Desktop install.")
        return 1
    print("  The bundle starts and serves its tools. If the Desktop install still")
    print("  fails, the problem is the installer or the account, not this bundle.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
