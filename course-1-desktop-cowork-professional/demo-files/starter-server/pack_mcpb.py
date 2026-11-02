#!/usr/bin/env python3
"""FALLBACK packer: zips a server folder into a .mcpb using only the standard library.

Prefer the official tool:  npm install -g @anthropic-ai/mcpb   then   mcpb pack <folder> <output.mcpb>
Use this script only if Node.js is not available. A .mcpb file is a zip archive with
manifest.json at its root (per the MCPB repository). Whether Claude Desktop accepts a
bundle made this way is NOT confirmed: rehearse an install before relying on it, and
prefer `mcpb pack` for anything you distribute.

Usage:  python pack_mcpb.py <folder-with-manifest.json> <output.mcpb>
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
m = json.loads(manifest.read_text(encoding="utf-8"))
for key in ("manifest_version", "name", "version", "description", "author", "server"):
    if key not in m:
        sys.exit(f"manifest.json is missing required field: {key}")
entry = src / m["server"]["entry_point"]
if not entry.is_file():
    sys.exit(f"entry_point not found: {entry}")

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
