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
  - The MCP keys, CORRECTED TWICE. Read this before changing anything here.
    2026-11-06 I removed allowedMcpServers, writing that it does not exist. It does.
    2026-11-11 I restored it but wrote that it "does not restrict servers declared in a
    project .mcp.json", quoting a sentence that is NOT in the settings reference, and
    gave its type as an array of strings, which is also wrong. Both came from a summary
    of the page rather than the page. Checked in the page itself on 2026-11-11:
      allowedMcpServers  "Allowlist the MCP servers people can add. Claude Code blocks
                         any server that doesn't match an entry WHEREVER IT'S DEFINED,
                         including plugin servers, servers a user passes with
                         --mcp-config, and servers from claude.ai." Built-in, CLI-
                         configured and Claude Tag servers are exempt; in-process
                         type: "sdk" servers are exempt from both lists.
                         Type: array of objects, each with EXACTLY ONE KEY, such as
                         {"serverName": "github"}. The string "array of strings" does
                         not appear in that section.
      deniedMcpServers   same single-key object shape; a denied server is blocked even
                         if the allowlist permits it.
      enabledMcpjsonServers / disabledMcpjsonServers  approve / reject named servers
                         from a project .mcp.json. Plain names.
      enableAllProjectMcpServers  approve every server .mcp.json declares (the blanket).
    So a well-formed allowlist naming only approved servers DOES stop an unapproved
    server declared in .mcp.json, and the tester who reported that in run 1 was right.
    What does not work is a list of BARE STRINGS: it matches nothing, so it blocks every
    server including the approved ones. Confirmed on the VM, where that shape started a
    session with mcp_servers: []. This script therefore refuses the string shape rather
    than scoring it 8/8, which is what it did for most of 2026-11-11.
    The scoring splits the DECISION (blanket off, no unapproved server left running)
    from the key, so no student who got the security right scores zero.

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

    try:
        with open(os.path.join(root, ".mcp.json"), encoding="utf-8") as f:
            declared = set(json.load(f).get("mcpServers", {}).keys())
    except (OSError, ValueError):
        declared = set()
    unapproved = declared - APPROVED_SERVERS

    def entry_names(value, objects_only):
        """Server names from an allow/deny list. objects_only reflects the documented
        shape of allowedMcpServers / deniedMcpServers: an array of objects, each with
        exactly one key, e.g. {"serverName": "github"}. A bare string there is NOT a
        valid entry, and a list of them matches nothing - which blocks every server,
        approved ones included. Confirmed on the RVC VM 2026-11-11: with strings, the
        session started with mcp_servers: [].
        """
        names, malformed = set(), []
        for item in value or []:
            if isinstance(item, dict):
                n = low(item.get("serverName", ""))
                if n:
                    names.add(n)
                    continue
                malformed.append(item)
            elif objects_only:
                malformed.append(item)
            else:
                if low(item):
                    names.add(low(item))
        return names, malformed

    # enabledMcpjsonServers / disabledMcpjsonServers take plain server names.
    approve_json, _ = entry_names(cfg.get("enabledMcpjsonServers"), False)
    reject_json, _ = entry_names(cfg.get("disabledMcpjsonServers"), False)
    # allowedMcpServers / deniedMcpServers take single-key objects.
    allowlist, allow_bad = entry_names(cfg.get("allowedMcpServers"), True)
    denylist, deny_bad = entry_names(cfg.get("deniedMcpServers"), True)

    # allowedMcpServers blocks any server that does not match an entry "wherever it's
    # defined", so a well-formed allowlist naming only approved servers DOES stop an
    # unapproved server declared in .mcp.json. That is enforcement, not pre-approval.
    blocked = set(reject_json) | set(denylist)
    allowlist_set = bool(cfg.get("allowedMcpServers"))
    allowlist_ok = allowlist_set and not allow_bad and allowlist <= APPROVED_SERVERS
    if allowlist_ok:
        blocked |= unapproved
    left_running = unapproved - blocked

    enforcement_detail = "enableAllProjectMcpServers=%r; declared in .mcp.json=%r; still running=%r" % (
        cfg.get("enableAllProjectMcpServers"), sorted(declared), sorted(left_running))
    if allow_bad or deny_bad:
        enforcement_detail += ("; MALFORMED entries %r - allowedMcpServers and deniedMcpServers take "
                               "objects with one key, e.g. {\"serverName\": \"docs-search\"}. A list of "
                               "bare strings matches nothing and blocks EVERY server, approved included"
                               % (allow_bad + deny_bad))
    check("MCP: enable-all is off, and no unapproved server is left running", 5,
          cfg.get("enableAllProjectMcpServers") is not True and not left_running
          and not allow_bad and not deny_bad,
          enforcement_detail)

    approve = approve_json | allowlist
    reject = reject_json | denylist
    named_ok = ((bool(approve) and approve <= APPROVED_SERVERS) or bool(reject - APPROVED_SERVERS))         and not allow_bad and not deny_bad
    check("MCP: a setting names the approved servers, or rejects the unapproved one", 3, named_ok,
          "approves=%r; rejects=%r (approved servers are %r)" % (
              sorted(approve), sorted(reject), sorted(APPROVED_SERVERS)))

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
