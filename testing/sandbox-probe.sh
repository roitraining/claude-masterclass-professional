#!/usr/bin/env bash
# The single source of truth for "does Claude Code's sandbox actually work here".
# Sourced by provision-rvc.sh and sandbox-apparmor.sh so they can never disagree.
#
#   sandbox_probe            -> prints PROBE_PASS | PROBE_FAIL | PROBE_SKIP
#                               diagnostic lines go to stderr
#
# HISTORY, because this has been wrong twice and the reasons matter:
#
#  v1 ran `claude -p` with no sandbox settings at all. Bash was never sandboxed,
#     so it passed on every run including with the restriction fully active.
#
#  v2 forced the sandbox on with failIfUnavailable: true, but still decided from
#     stdout text. With --permission-mode bypassPermissions the model stepped
#     OUTSIDE the sandbox and retried after the sandboxed call had correctly
#     failed, so the expected string appeared anyway and the probe passed while
#     sandbox-apparmor.sh, reading kernel denials, said it had failed.
#
#  v3, this one, decides from the TOOL RESULT rather than from stdout, and
#     removes the model's ability to retry unsandboxed:
#       - --output-format stream-json, and require a Bash tool_result with
#         is_error false
#       - allowUnsandboxedCommands: false so no unsandboxed retry can happen
#       - no bypassPermissions; --allowedTools Bash is enough to permit the call
#
# The lesson: a probe must assert on the mechanism it is testing, not on a
# string that something else can also produce.

SANDBOX_SETTINGS='{"sandbox":{"enabled":true,"failIfUnavailable":true,"allowUnsandboxedCommands":false}}'
PROBE_MARKER="SANDBOX_OK_$$"

sandbox_probe() {
  command -v claude >/dev/null 2>&1 || { echo "PROBE_SKIP"; return; }
  command -v python3 >/dev/null 2>&1 || { echo "PROBE_SKIP"; echo "  python3 needed to parse the probe output" >&2; return; }

  local raw
  raw="$(timeout 150 claude -p "Run the bash command: echo $PROBE_MARKER" \
           --allowedTools Bash \
           --output-format stream-json --verbose \
           --settings "$SANDBOX_SETTINGS" 2>&1)"

  printf '%s' "$raw" | PROBE_MARKER="$PROBE_MARKER" python3 -c '
import json, os, sys

marker = os.environ["PROBE_MARKER"]
saw_tool_use = False
ok_result = False
err_texts = []

for line in sys.stdin.read().splitlines():
    line = line.strip()
    if not line.startswith("{"):
        continue
    try:
        ev = json.loads(line)
    except Exception:
        continue

    msg = ev.get("message") or {}
    content = msg.get("content")
    if not isinstance(content, list):
        continue

    for block in content:
        if not isinstance(block, dict):
            continue
        if block.get("type") == "tool_use" and block.get("name") == "Bash":
            saw_tool_use = True
        if block.get("type") == "tool_result":
            body = block.get("content")
            if isinstance(body, list):
                text = " ".join(b.get("text", "") for b in body if isinstance(b, dict))
            else:
                text = body if isinstance(body, str) else ""
            # A pass requires BOTH: the tool did not error, and it produced our
            # marker. Either alone is not evidence the sandbox ran the command.
            if block.get("is_error"):
                err_texts.append(text)
            elif marker in text:
                ok_result = True

if ok_result:
    print("PROBE_PASS")
else:
    print("PROBE_FAIL")
    if not saw_tool_use:
        print("      no Bash tool_use in the transcript: the call never ran", file=sys.stderr)
    for t in err_texts[:2]:
        for ln in t.splitlines():
            if any(k in ln.lower() for k in
                   ("seccomp", "setgroups", "userns", "cap_sys_admin", "denied",
                    "sandbox", "permission")):
                print("      " + ln.strip()[:150], file=sys.stderr)
'
}
