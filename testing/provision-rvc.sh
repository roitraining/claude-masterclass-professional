#!/usr/bin/env bash
# Provision / verify the ROI Virtual Classroom image for the Claude MasterClass
# Professional courses.
#
#   ./provision-rvc.sh --check      report only, change nothing (safe, no sudo)
#   ./provision-rvc.sh --install    apply everything installable
#   ./provision-rvc.sh --install --allow-sandbox-fix
#                                   also apply the AppArmor/sysctl sandbox change
#
# Intended workflow:
#   1. --check on the current image  -> see what is missing
#   2. --install                     -> apply it
#   3. --check again                 -> everything should be OK
#   Hand the step-1 and step-3 output to the team as the before/after evidence.
#
# Every requirement below is traceable to course material, not guesswork.
# Sources are named per item. Target image: Ubuntu 26.04.1 LTS.

set -uo pipefail

MODE=""
ALLOW_SANDBOX_FIX=0
for arg in "$@"; do
  case "$arg" in
    --check)              MODE="check" ;;
    --install)            MODE="install" ;;
    --allow-sandbox-fix)  ALLOW_SANDBOX_FIX=1
                          echo "note: --allow-sandbox-fix no longer does anything."
                          echo "      The sysctl it used to set was proven ineffective on 2026-11-04;"
                          echo "      AppArmor's unpriv_bwrap profile is the real block. See item 1." ;;
    -h|--help)            sed -n '2,30p' "$0"; exit 0 ;;
    *) echo "unknown argument: $arg (try --help)"; exit 2 ;;
  esac
done
[ -z "$MODE" ] && { echo "Specify --check or --install (see --help)."; exit 2; }

# Course 1 pins a minimum Claude Code version.
MIN_CLAUDE_VERSION="2.1.269"

PASS=0; FAIL=0; WARN=0; MANUAL=0
declare -a NOTES=()

c_ok()   { printf '  \033[32m[ OK ]\033[0m %s\n' "$1"; PASS=$((PASS+1)); }
c_bad()  { printf '  \033[31m[FAIL]\033[0m %s\n' "$1"; FAIL=$((FAIL+1)); }
c_warn() { printf '  \033[33m[WARN]\033[0m %s\n' "$1"; WARN=$((WARN+1)); }
c_man()  { printf '  \033[36m[HUMAN]\033[0m %s\n' "$1"; MANUAL=$((MANUAL+1)); }
hdr()    { printf '\n\033[1m== %s\033[0m\n' "$1"; }
note()   { NOTES+=("$1"); }

have() { command -v "$1" >/dev/null 2>&1; }

SUDO=""
if [ "$(id -u)" -ne 0 ]; then
  if sudo -n true 2>/dev/null; then SUDO="sudo"
  else SUDO="sudo"; note "sudo may prompt for a password; the tester reported passwordless sudo on this image."
  fi
fi

# apt packages: name -> why it is needed (course source)
APT_PKGS=(
  "python-is-python3|provides \`python\`; labs across all 5 courses call \`python\`, image has only python3"
  "python3-venv|PEP 668 refuses pip outside a venv; every pip step needs one"
  "python3-pip|pip itself"
  "curl|used by 15 labs, and by the Claude Code installer"
  "gnupg|needed by the apt install path for Claude Code"
  "git|16 labs commit locally"
  "nodejs|Course 1 packaging via mcpb; Course 3 TypeScript track"
  "npm|installs @anthropic-ai/mcpb"
)

hdr "1. System packages"
MISSING_APT=()
for entry in "${APT_PKGS[@]}"; do
  pkg="${entry%%|*}"; why="${entry#*|}"
  if dpkg -s "$pkg" >/dev/null 2>&1; then
    c_ok "$pkg"
  else
    c_bad "$pkg missing — $why"
    MISSING_APT+=("$pkg")
  fi
done

if [ "$MODE" = "install" ] && [ ${#MISSING_APT[@]} -gt 0 ]; then
  echo "  installing: ${MISSING_APT[*]}"
  $SUDO apt-get update -qq && $SUDO apt-get install -y "${MISSING_APT[@]}"
fi

hdr "2. python command and PEP 668"
if have python; then
  c_ok "\`python\` resolves ($(python --version 2>&1))"
else
  c_bad "\`python\` not found — install python-is-python3 (blocker 3)"
fi
have python3 && c_ok "\`python3\` resolves ($(python3 --version 2>&1))" \
             || c_bad "python3 missing"
if python3 -c 'import venv' 2>/dev/null; then
  c_ok "venv module available"
else
  c_bad "venv module missing — python3-venv"
fi

hdr "3. Claude Code"
if have claude; then
  CV="$(claude --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)"
  if [ -n "$CV" ]; then
    LOWEST="$(printf '%s\n%s\n' "$CV" "$MIN_CLAUDE_VERSION" | sort -V | head -1)"
    if [ "$LOWEST" = "$MIN_CLAUDE_VERSION" ]; then
      c_ok "claude $CV (>= $MIN_CLAUDE_VERSION required by Course 1)"
    else
      c_bad "claude $CV is below the $MIN_CLAUDE_VERSION Course 1 needs — run: claude update"
    fi
  else
    c_warn "claude present but version unreadable"
  fi
  # Auto-update means the image version drifts; worth recording per run.
  note "Claude Code auto-updates, so the image version drifts. Record the version at each test run."
else
  c_bad "claude not installed"
  if [ "$MODE" = "install" ]; then
    echo "  installing Claude Code (native installer)"
    curl -fsSL https://claude.ai/install.sh | bash
    note "Claude Code installed; open a new shell or add \$HOME/.local/bin to PATH."
  fi
fi

# PATH check: the native installer puts the launcher in ~/.local/bin
case ":$PATH:" in
  *":$HOME/.local/bin:"*) c_ok "\$HOME/.local/bin on PATH" ;;
  *) c_bad "\$HOME/.local/bin not on PATH — add: echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.bashrc" ;;
esac

hdr "4. Class API key for the Agent SDK (Course 3)"
# Course 3 REQUIRES an API key. This is taught content, not an accident:
# deck slide 11 is "Install, Authenticate, Run" and Module 2 spends 45 minutes
# on it. Anthropic's Agent SDK overview states that claude.ai login is not
# allowed for Agent SDK agents, so a subscription token is NOT a substitute.
# Deck slide 6: "Each student gets a class API key with a spend limit."
if [ -n "${ANTHROPIC_API_KEY:-}" ]; then
  c_ok "ANTHROPIC_API_KEY set in this shell (Course 3 can run)"
  note "Keep ANTHROPIC_API_KEY per-shell. Exported in ~/.bashrc it overrides subscription login for Courses 1, 2 and 4."
else
  c_bad "ANTHROPIC_API_KEY not set — all five Course 3 labs stop at the guard in agent_core.py"
  note "Course 3 needs a class API key with a spend limit, handed out per student. A subscription token is not a valid substitute (see IMAGE-REQUIREMENTS.md item 6)."
fi
if [ -f "$HOME/.claude/.credentials.json" ]; then
  c_ok "stored CLI login found (Courses 1, 2, 4)"
else
  c_bad "no stored CLI login — run: claude auth login"
fi

hdr "5. Node tooling (Course 1 packaging)"
if have npm; then
  c_ok "npm present ($(npm --version 2>/dev/null))"
  if npm ls -g --depth=0 2>/dev/null | grep -q '@anthropic-ai/mcpb'; then
    c_ok "@anthropic-ai/mcpb installed globally"
  else
    c_bad "@anthropic-ai/mcpb missing — Course 1 Lab 1 packaging"
    if [ "$MODE" = "install" ]; then
      echo "  installing @anthropic-ai/mcpb"
      $SUDO npm install -g @anthropic-ai/mcpb
    fi
  fi
else
  c_bad "npm missing — needed for @anthropic-ai/mcpb"
  note "Fallback exists: course-1 starter-server/pack_mcpb.py works without Node (tester confirmed)."
fi

hdr "6. Per-course Python environments"
# Separate venvs so PEP 668 never bites and courses cannot break each other.
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_BASE="$HOME/.venvs"

provision_venv() {
  local name="$1"; shift
  local path="$VENV_BASE/$name"
  if [ -x "$path/bin/python" ]; then
    c_ok "venv $name exists"
  else
    c_bad "venv $name missing ($*)"
    if [ "$MODE" = "install" ]; then
      echo "  creating $path"
      python3 -m venv "$path" || { c_bad "venv creation failed for $name"; return; }
    else
      return
    fi
  fi
  if [ "$MODE" = "install" ]; then
    "$path/bin/pip" install -q --upgrade pip
    "$path/bin/pip" install -q "$@" && c_ok "packages installed into $name" \
      || c_bad "pip install failed in $name: $*"
  fi
}

mkdir -p "$VENV_BASE" 2>/dev/null
# Course 3, Agent SDK — demo-files/python/requirements.txt (unpinned on purpose)
provision_venv "mc-agent-sdk"  "claude-agent-sdk" "mcp[cli]"
# Course 2 Lab 1, CI gate — demo-files/lab1-ci/requirements.txt
provision_venv "mc-ci"         "pyyaml>=6.0" "pytest"
# Course 2 Lab 4, language server — the lab's own Step 1 command
provision_venv "mc-lsp"        "python-lsp-server[pyflakes,pycodestyle]"

if [ -x "$VENV_BASE/mc-lsp/bin/pylsp" ]; then
  c_ok "pylsp available at $VENV_BASE/mc-lsp/bin/pylsp"
  note "Course 2 Lab 4 needs pylsp on PATH of the shell that starts claude: activate mc-lsp first."
else
  [ "$MODE" = "check" ] && c_bad "pylsp not installed (Course 2 Lab 4)"
fi

hdr "7. Git identity (blocker 6)"
GN="$(git config --global user.name 2>/dev/null)"
GE="$(git config --global user.email 2>/dev/null)"
if [ -n "$GN" ] && [ -n "$GE" ]; then
  c_ok "git identity set ($GN <$GE>)"
else
  c_bad "no global git identity — every lab that commits fails with 'Author identity unknown'"
  if [ "$MODE" = "install" ]; then
    git config --global user.name  "${RVC_GIT_NAME:-RVC Student}"
    git config --global user.email "${RVC_GIT_EMAIL:-student@rvc.local}"
    c_ok "set a placeholder identity; override with RVC_GIT_NAME / RVC_GIT_EMAIL"
  fi
fi

hdr "8. Sandbox (blocker 1) — diagnostic only, no fix available here"
# PROVEN ON 2026-11-04: setting kernel.apparmor_restrict_unprivileged_userns=0
# does NOT fix this. The bwrap-userns-restrict AppArmor profile stays loaded and
# enforcing, moving everything bwrap launches into unpriv_bwrap, which carries
# "audit deny capability". The kernel kept denying after the sysctl was relaxed:
#   apparmor="DENIED" operation="capable" class="cap" profile="unpriv_bwrap" #     comm="3" capability=21 capname="sys_admin"
# So this section no longer offers a fix. It diagnoses and reports.
SYSCTL_KEY="kernel.apparmor_restrict_unprivileged_userns"
CURRENT="$(sysctl -n "$SYSCTL_KEY" 2>/dev/null || echo "unset")"
echo "  $SYSCTL_KEY = $CURRENT (informational: changing this does NOT fix the sandbox)"
if [ -e /etc/apparmor.d/bwrap-userns-restrict ]; then
  c_bad "AppArmor profile bwrap-userns-restrict present — this is the actual block"
else
  c_warn "bwrap-userns-restrict not found; the block may be elsewhere on this image"
fi
if command -v aa-status >/dev/null 2>&1; then
  if $SUDO aa-status 2>/dev/null | grep -q unpriv_bwrap; then
    c_bad "profile unpriv_bwrap is loaded and enforcing"
  fi
fi
if [ -f /etc/sysctl.d/99-claude-sandbox.conf ]; then
  c_bad "/etc/sysctl.d/99-claude-sandbox.conf exists from an earlier run of this script"
  note "That file relaxes a security setting and fixes nothing. Remove it: sudo rm /etc/sysctl.d/99-claude-sandbox.conf && sudo sysctl -w $SYSCTL_KEY=1"
fi

# Probe via the shared helper, so this script and sandbox-apparmor.sh can never
# report different answers. See sandbox-probe.sh for why this has been wrong twice.
# shellcheck source=sandbox-probe.sh
. "$(dirname "${BASH_SOURCE[0]}")/sandbox-probe.sh"
if have claude; then
  echo "  probing (sandbox forced on, decided from the Bash tool result)..."
  case "$(sandbox_probe)" in
    PROBE_PASS) c_ok "a genuinely sandboxed Bash call succeeded" ;;
    PROBE_FAIL) c_bad "sandboxed Bash call failed — the sandbox is unavailable on this image" ;;
    *)          c_warn "probe skipped" ;;
  esac
else
  c_warn "claude not installed; cannot probe the sandbox"
fi

note "No scripted fix for the sandbox. It needs an AppArmor change on the image: see IMAGE-REQUIREMENTS.md item 1."

hdr "9. Needs a person (not scriptable)"
c_man "Claude Desktop signed in to the SAME account as the CLI — needed only for the optional extension install in Course 1 Lab 1 Part 8 and for Lab 3 Part 5. It does NOT block the rest of Course 1"
c_man "Decide the account tier for testing: Max, or a free account to observe free-tier limits"
c_man "Course 2 Lab 1 Tracks A and B need a remote GitHub/GitLab project with admin access"
c_man "Course 4 Labs 1-2 live paths need an instructor-provisioned sandbox organization (offline path works without)"
c_man "Course 3 Lab 4 Part 6 needs Claude Console access"

hdr "10. Installed versions (for the image spec)"
# The team needs exact versions to bake into the image, not just package names.
# Paste this block into the change request.
for pkg in python-is-python3 python3-venv python3-pip curl gnupg git nodejs npm; do
  v="$(dpkg-query -W -f='${Version}' "$pkg" 2>/dev/null)"
  if [ -n "$v" ]; then printf '  %-20s %s
' "$pkg" "$v"
  else printf '  %-20s NOT INSTALLED
' "$pkg"; fi
done
printf '  %-20s %s
' "ubuntu"  "$(. /etc/os-release 2>/dev/null; echo "${PRETTY_NAME:-unknown}")"
printf '  %-20s %s
' "kernel"  "$(uname -r 2>/dev/null)"
printf '  %-20s %s
' "claude"  "$(claude --version 2>/dev/null || echo 'not installed')"
printf '  %-20s %s
' "node"    "$(node --version 2>/dev/null || echo '-')"
printf '  %-20s %s
' "mcpb"    "$(npm ls -g --depth=0 2>/dev/null | grep -o 'mcpb@[0-9.]*' || echo '-')"
printf '  %-20s %s
' "pylsp"   "$($VENV_BASE/mc-lsp/bin/pylsp --version 2>/dev/null | head -1 || echo '-')"
for v in mc-agent-sdk mc-ci mc-lsp; do
  if [ -x "$VENV_BASE/$v/bin/pip" ]; then
    printf '  venv %-15s %s
' "$v" "$("$VENV_BASE/$v/bin/pip" list --format=freeze 2>/dev/null | tr '
' ' ' | cut -c1-110)"
  fi
done

hdr "Summary"
printf '  OK %d   FAIL %d   WARN %d   HUMAN %d\n' "$PASS" "$FAIL" "$WARN" "$MANUAL"
if [ ${#NOTES[@]} -gt 0 ]; then
  echo
  echo "  Notes:"
  for n in "${NOTES[@]}"; do echo "   - $n"; done
fi
echo
if [ "$MODE" = "check" ] && [ "$FAIL" -gt 0 ]; then
  echo "  Not ready. Run: $0 --install"
  exit 1
elif [ "$FAIL" -gt 0 ]; then
  echo "  Some items still failing after install — see FAIL lines above."
  exit 1
else
  echo "  All scripted checks pass. HUMAN items above still need a person."
  exit 0
fi
