#!/usr/bin/env python3
"""FALLBACK packer: zips a server folder into a .mcpb using only the standard library.

Prefer the official tool:  npm install -g @anthropic-ai/mcpb   then   mcpb pack <folder> <output.mcpb>
Use this script only if Node.js is not available. A .mcpb file is a zip archive with
manifest.json at its root (per the MCPB repository). Whether Claude Desktop accepts a
bundle made this way is NOT confirmed: rehearse an install before relying on it, and
prefer `mcpb pack` for anything you distribute.

Usage:  python3 pack_mcpb.py <folder-with-manifest.json> <output.mcpb>
"""
import json
import sys
import zipfile
from pathlib import Path

SKIP_DIRS = {"__pycache__", ".git", ".venv", "evals", "node_modules"}
SKIP_SUFFIXES = {".pyc", ".mcpb", ".log"}

if len(sys.argv) != 3:
    sys.exit(__doc__)
src, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
manifest = src / "manifest.json"
if not manifest.is_file():
    sys.exit(f"No manifest.json in {src}")
try:
    m = json.loads(manifest.read_text(encoding="utf-8"))
except json.JSONDecodeError as e:
    sys.exit(f"manifest.json is not valid JSON: {e}")

for key in ("manifest_version", "name", "version", "description", "author", "server"):
    if key not in m:
        sys.exit(f"manifest.json is missing required field: {key}")

server = m["server"]
if not isinstance(server, dict):
    sys.exit("manifest.json: server must be an object")

# server.type is an ENUM, not a command. This check exists because a sweep that
# rewrote `python` to `python3` set it to python3, and this script packed the
# broken manifest and exited 0 -- so the failure only surfaced later, in
# `mcpb pack`, as "Invalid enum value". Validate what mcpb validates.
SERVER_TYPES = ("python", "node", "binary")
stype = server.get("type")
if stype not in SERVER_TYPES:
    sys.exit(f"manifest.json: server.type is {stype!r}; expected one of {' | '.join(SERVER_TYPES)}. "
             "This is the extension runtime, not the command to run. The interpreter belongs in "
             "server.mcp_config.command.")

if "entry_point" not in server:
    sys.exit("manifest.json: server.entry_point is missing")
entry = src / server["entry_point"]
if not entry.is_file():
    sys.exit(f"entry_point not found: {entry}")

cfg = server.get("mcp_config")
if not isinstance(cfg, dict) or not cfg.get("command"):
    sys.exit("manifest.json: server.mcp_config.command is missing. This is what actually "
             "launches the server, for example python3.")

out.parent.mkdir(parents=True, exist_ok=True)   # dist/ may not exist yet

count = 0
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for p in sorted(src.rglob("*")):
        rel = p.relative_to(src)
        if p.is_dir() or p == out:
            continue
        if SKIP_DIRS & set(rel.parts) or p.suffix in SKIP_SUFFIXES:
            continue
        z.write(p, rel.as_posix())
        count += 1
print(f"Wrote {out.name}: {count} files, {out.stat().st_size} bytes")

# server.py falls back to the sample_data folder beside it when no data folder
# is configured, and the manifest tells users that. Warn if the bundle cannot
# honour that promise.
with zipfile.ZipFile(out) as z:
    names = z.namelist()
if (src / "sample_data").is_dir() and not any(n.startswith("sample_data/") for n in names):
    print("WARNING: sample_data/ is not in the bundle, but the manifest offers it as the "
          "fallback when no data folder is set. The extension will start with no records.",
          file=sys.stderr)
    sys.exit(1)
