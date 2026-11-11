#!/usr/bin/env python3
"""Static settings checker for Lab 3. Works on any machine: it reads files and runs nothing.

Usage:  python3 check_settings.py PATH_TO_PROJECT      (for example ~/work/vuln-app)
Reads PATH_TO_PROJECT/.claude/settings.json, .mcp.json and app.py.

Scores 60 points (part A). Part B is the live attack script (40 points). It also prints
the attack outcomes the configuration PREDICTS, for machines with no OS sandbox support.
A prediction is not an observation: live sandbox behavior needs rehearsal.

Key names CONFIRMED 2026-11-06 against the Claude Code settings reference
(code.claude.com/docs/en/settings-reference):
  - sandbox.enabled, sandbox.failIfUnavailable and sandbox.allowUnsandboxedCommands
    are all children of the sandbox object. There is no top-level spelling, so this
    script no longer accepts one: it would have given 7 points for a key Claude Code
    ignores. Corroborated on the RVC VM, where forcing sandbox.failIfUnavailable true
    made the run fail closed (apply-seccomp denial) where no settings ran unsandboxed.
  - The .mcp.json approval keys are enabledMcpjsonServers, disabledMcpjsonServers and
    enableAllProjectMcpServers. There is NO allowedMcpServers key, so this script no
    longer accepts one: it would have given 8 points for a list that does nothing.

STILL UNVERIFIED (confirm before delivery):
  - Permission rule syntax such as Read(./config/secrets.env) follows the Associate
    courses.
"""
import json
import os
import sys

APPROVED_DOMAINS = {"pypi.org", "files.pythonhosted.org", "api.example.com"}
APPROVED_SERVERS = {"docs-search", "ticket-bridge"}
BROAD_WRITE = {"~", "/", "*", "..", "../", "$home", "%userprofile%", "~/", "**"}


def low(s):
    return str(s).strip().lower()


def find(obj, key):
    """Return the first value for key anywhere inside obj, else None."""
    if isinstance(obj, dict):
        if key in obj:
            return obj[key]
        for v in obj.values():
            r = find(v, key)
            if r is not None:
                return r
    return None


def flat(items):
    return [low(x) for x in (items or []) if isinstance(x, str)]


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    root = sys.argv[1]
    try:
        with open(os.path.join(root, ".claude", "settings.json"), encoding="utf-8") as f:
            cfg = json.load(f)
    except (OSError, ValueError) as exc:
        print("Cannot read .claude/settings.json: %s" % exc)
        sys.exit(1)
    sb = cfg.get("sandbox", {}) if isinstance(cfg.get("sandbox"), dict) else {}
    perms = cfg.get("permissions", {}) if isinstance(cfg.get("permissions"), dict) else {}
    deny = flat(perms.get("deny"))
    allow = flat(perms.get("allow"))
    rows = []

    def check(label, pts, ok, detail):
        rows.append((label, pts, pts if ok else 0, detail))

    enabled = sb.get("enabled") is True
    check("sandbox.enabled is true", 7, enabled, "sandbox.enabled = %r" % sb.get("enabled"))
    check("sandbox.failIfUnavailable is true", 7, sb.get("failIfUnavailable") is True,
          "failIfUnavailable = %r (default is to warn and run unsandboxed)" % sb.get("failIfUnavailable"))
    unsb = find(sb, "allowUnsandboxedCommands")
    check("allowUnsandboxedCommands is false", 7, unsb is False, "allowUnsandboxedCommands = %r" % unsb)

    domains = find(sb, "allowedDomains")
    dl = flat(domains)
    bad = [d for d in dl if d not in APPROVED_DOMAINS]
    check("network.allowedDomains is a non-empty list of approved domains only", 7,
          bool(dl) and not bad, "allowedDomains = %r; not approved: %r" % (domains, bad))

    aw = find(sb, "allowWrite")
    awl = flat(aw)
    broad = [x for x in awl if x in BROAD_WRITE or x.startswith("~") or x.startswith("/") and len(x) <= 5]
    check("filesystem.allowWrite grants no broad path (home, root, parent)", 5, not broad,
          "allowWrite = %r; too broad: %r" % (aw, broad))
    dr = flat(find(sb, "denyRead"))
    sec = any("secrets" in x for x in dr)
    ssh = any(".ssh" in x for x in dr)
    check("filesystem.denyRead covers the secrets file and ~/.ssh", 5, sec and ssh,
          "denyRead = %r (secrets file: %s, ssh: %s)" % (dr, sec, ssh))
    dw = flat(find(sb, "denyWrite"))
    check("filesystem.denyWrite protects .claude and .mcp.json", 3,
          any(".claude" in x for x in dw) and any(".mcp.json" in x for x in dw), "denyWrite = %r" % dw)

    check("permissions.deny blocks reading the secrets file and .env", 4,
          any("read" in x and "secrets" in x for x in deny) and any("read" in x and ".env" in x for x in deny),
          "deny = %r" % deny)
    check("permissions.deny blocks curl and wget", 3,
          any("curl" in x for x in deny) and any("wget" in x for x in deny), "deny = %r" % deny)
    blanket = [x for x in allow if x in ("bash", "bash(*)", "bash(*:*)", "*")]
    check("permissions.allow has no blanket Bash allow", 4, not blanket, "blanket allow rules: %r" % blanket)

    mcp_allow = cfg.get("enabledMcpjsonServers")
    names = set()
    for item in mcp_allow or []:
        names.add(low(item.get("serverName", "")) if isinstance(item, dict) else low(item))
    try:
        with open(os.path.join(root, ".mcp.json"), encoding="utf-8") as f:
            declared = set(json.load(f).get("mcpServers", {}).keys())
    except (OSError, ValueError):
        declared = set()
    mcp_ok = (cfg.get("enableAllProjectMcpServers") is not True and bool(names) and names <= APPROVED_SERVERS
              and not (declared - APPROVED_SERVERS))
    check("MCP: no enable-all, an allowlist of approved servers, no unapproved server declared", 8, mcp_ok,
          "enableAllProjectMcpServers=%r; allowlist=%r; declared in .mcp.json=%r" % (
              cfg.get("enableAllProjectMcpServers"), sorted(names), sorted(declared)))

    total = 0
    print("PART A: static checklist")
    for label, pts, got, detail in rows:
        total += got
        print("  [%s] %2d/%-2d %s" % ("PASS" if got else "FAIL", got, pts, label))
        if not got:
            print("            %s" % detail)
    print("  PART A SCORE: %d / 60\n" % total)

    net_ok = enabled and bool(dl) and "*" not in dl
    # A Read deny rule alone does NOT stop a shell command reading the file:
    # deny rules gate Claude's Read tool, and the OS sandbox is what stops Bash.
    # This used to be `(enabled and sec) or any(read deny rule)`, so with the
    # sandbox disabled attack 3 still printed "blocked if the OS sandbox starts"
    # while attacks 1 and 2 correctly printed "will succeed" -- and the fallback
    # scoring, which reads these lines, awarded 5 points for it.
    read_ok = enabled and sec
    write_ok = enabled and not broad
    app_path = os.path.join(root, "app.py")
    try:
        with open(app_path, encoding="utf-8") as f:
            vulnerable = "os.system(" in f.read()
    except OSError:
        vulnerable = True
    print("PREDICTED attack outcomes (a prediction, not an observation; rehearse the live sandbox)")
    print("  1 write outside the working directory : %s" % ("blocked if the OS sandbox starts" if write_ok else "will succeed"))
    print("  2 disallowed destination              : %s" % ("blocked if the OS sandbox starts (loopback handling UNVERIFIED)" if net_ok else "will succeed"))
    print("  3 read the secrets file               : %s" % ("blocked if the OS sandbox starts"
          if read_ok else "will succeed"))
    print("      deny rules gate Claude's Read tool. A shell command run through Bash is")
    print("      stopped by the OS sandbox, so with the sandbox down this file can still be read.")
    print("  4 command injection in app.py         : %s" % ("will succeed: app.py still builds a shell command (a sandbox does not stop a command inside the working directory)" if vulnerable else "no os.system found in app.py"))


if __name__ == "__main__":
    main()
