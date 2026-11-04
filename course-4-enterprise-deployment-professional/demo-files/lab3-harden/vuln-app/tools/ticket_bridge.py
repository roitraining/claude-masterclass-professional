#!/usr/bin/env python3
"""Deliberately minimal MCP server stub for the Lab 3 ticket-bridge entry.

`.mcp.json` in this project registers a `ticket-bridge` server pointing here.
The lab does not exercise it: it exists so the project's MCP configuration
resolves instead of failing on a missing file, which was masking the real
exercise. Hardening the configuration, not this file, is the lab.

It speaks no protocol on purpose. Started by hand it exits immediately.
"""
import sys

if __name__ == "__main__":
    sys.stderr.write(
        "ticket-bridge: stub only, not part of the Lab 3 exercise. Exiting.\n")
    sys.exit(0)
