#!/usr/bin/env bash
# Find a working AppArmor change that lets Claude Code's sandbox start on
# Ubuntu 26.04, and prove it with a real before/after probe.
#
#   ./sandbox-apparmor.sh --diagnose            read-only, changes nothing
#   ./sandbox-apparmor.sh --try local-override  TRIED 2026-11-04, cannot work
#   ./sandbox-apparmor.sh --try claude-profile  TRIED 2026-11-11, not adopted
#   ./sandbox-apparmor.sh --try disable-profile TRIED 2026-11-11, WORKS (image-wide)
#
# All three have been tested on the RVC image. Only disable-profile makes the probe
# pass, because the denial is raised in unpriv_bwrap, which /usr/bin/bwrap transitions
# into - confining the caller does not change the child's transition. Re-run them only
# to re-confirm on a new image; the answer on this one is known.
#   ./sandbox-apparmor.sh --revert              undo everything this script did
#
# WHY THIS EXISTS
# The sysctl kernel.apparmor_restrict_unprivileged_userns=0 was tried on
# 2026-11-04 and did NOT work: bwrap-userns-restrict stays loaded and enforcing,
# transitioning bwrap into the unpriv_bwrap profile, which carries
# "audit deny capability". The observed denial:
#
#   apparmor="DENIED" operation="capable" class="cap" profile="unpriv_bwrap" \
#     comm="3" capability=21 capname="sys_admin"
#
# HONESTY NOTE
# None of the three options below has been tested. They are the documented ways
# to grant unprivileged user-namespace creation under AppArmor, ordered least
# invasive first. This script's job is to apply ONE, re-probe, and tell you
# whether it actually worked -- the thing that went wrong last time was treating
# an applied change as a working one.
#
# Every option backs up what it touches and is undone by --revert.

set -uo pipefail

MODE=""; OPTION=""
while [ $# -gt 0 ]; do
  case "$1" in
    --diagnose) MODE="diagnose" ;;
    --try)      MODE="try"; OPTION="${2:-}"; shift ;;
    --revert)   MODE="revert" ;;
    -h|--help)  sed -n '2,30p' "$0"; exit 0 ;;
    *) echo "unknown argument: $1 (try --help)"; exit 2 ;;
  esac
  shift
done
[ -z "$MODE" ] && { echo "Specify --diagnose, --try <option>, or --revert."; exit 2; }

BACKUP_DIR="$HOME/.claude-sandbox-apparmor-backup"
PROFILE="/etc/apparmor.d/bwrap-userns-restrict"
LOCAL_OVERRIDE="/etc/apparmor.d/local/bwrap-userns-restrict"
CLAUDE_PROFILE="/etc/apparmor.d/claude-code-sandbox"
SUDO=""; [ "$(id -u)" -ne 0 ] && SUDO="sudo"

ok()   { printf '  \033[32m[ OK ]\033[0m %s\n' "$1"; }
bad()  { printf '  \033[31m[FAIL]\033[0m %s\n' "$1"; }
info() { printf '  \033[36m[INFO]\033[0m %s\n' "$1"; }
hdr()  { printf '\n\033[1m== %s\033[0m\n' "$1"; }

# ---------------------------------------------------------------- the probe
# Shared with provision-rvc.sh. The two scripts disagreed on 2026-11-04 because
# they judged differently; now there is one implementation. See sandbox-probe.sh.
# shellcheck source=sandbox-probe.sh
. "$(dirname "${BASH_SOURCE[0]}")/sandbox-probe.sh"

probe() { sandbox_probe; }

recent_denials() {
  if command -v journalctl >/dev/null 2>&1; then
    $SUDO journalctl -k --since "-5 min" 2>/dev/null \
      | grep -i 'apparmor="DENIED"' | tail -5
  else
    $SUDO dmesg 2>/dev/null | grep -i 'apparmor="DENIED"' | tail -5
  fi
}

# ---------------------------------------------------------------- diagnose
if [ "$MODE" = "diagnose" ]; then
  hdr "1. What is loaded"
  [ -e "$PROFILE" ] && bad "$PROFILE present (this is the restriction)" \
                    || info "$PROFILE not present on this image"
  if command -v aa-status >/dev/null 2>&1; then
    $SUDO aa-status 2>/dev/null | grep -qi unpriv_bwrap \
      && bad "profile unpriv_bwrap is loaded" \
      || info "unpriv_bwrap not listed by aa-status"
    info "enforcing profiles: $($SUDO aa-status 2>/dev/null | grep -c 'enforce' || echo '?')"
  else
    info "aa-status not installed (apparmor-utils provides it)"
  fi

  hdr "2. Can the shipped profile be extended without editing it"
  if [ -e "$PROFILE" ] && grep -q 'include if exists <local/' "$PROFILE" 2>/dev/null; then
    info "the profile has a local include, but 'local-override' was TRIED 2026-11-04 AND FAILED:"
    info "unpriv_bwrap carries 'audit deny capability', and an AppArmor deny beats any allow."
    info "Do not retry it. Try 'claude-profile', then 'disable-profile'."
    grep -o 'include if exists <local/[^>]*>' "$PROFILE" | sed 's/^/        /'
  else
    info "no local include found; option 'local-override' may not apply. Try 'claude-profile' instead."
  fi

  hdr "3. Where the claude binary actually lives"
  CB="$(command -v claude 2>/dev/null)"
  if [ -n "$CB" ]; then
    REAL="$(readlink -f "$CB")"
    info "launcher: $CB"
    info "real binary: $REAL"
    info "an AppArmor profile must name the REAL path, not the launcher symlink"
  else
    bad "claude not on PATH; cannot write a binary profile"
  fi

  hdr "4. Baseline probe (sandbox forced on)"
  R="$(probe)"
  case "$R" in
    PROBE_PASS) ok "the sandbox already works — no AppArmor change needed" ;;
    PROBE_FAIL) bad "the sandbox does not start (expected before a fix)" ;;
    *)          info "probe skipped: claude not installed" ;;
  esac

  hdr "5. Recent kernel denials"
  D="$(recent_denials)"
  if [ -n "$D" ]; then printf '%s\n' "$D" | sed 's/^/        /'
  else info "none in the last 5 minutes (run the probe, then re-check)"; fi

  hdr "Next"
  echo "  Try the options in order, re-probing after each:"
  echo "    ./sandbox-apparmor.sh --try local-override"
  echo "    ./sandbox-apparmor.sh --try claude-profile"
  echo "    ./sandbox-apparmor.sh --try disable-profile"
  echo "  Then ./sandbox-apparmor.sh --revert to undo whatever did not work."
  exit 0
fi

# ---------------------------------------------------------------- revert
if [ "$MODE" = "revert" ]; then
  hdr "Reverting every change this script makes"
  [ -f "$BACKUP_DIR/local-override.created" ] && { $SUDO rm -f "$LOCAL_OVERRIDE"; ok "removed $LOCAL_OVERRIDE"; }
  [ -f "$BACKUP_DIR/local-override.bak" ] && { $SUDO cp "$BACKUP_DIR/local-override.bak" "$LOCAL_OVERRIDE"; ok "restored $LOCAL_OVERRIDE"; }
  if [ -f "$BACKUP_DIR/claude-profile.created" ]; then
    # Unload FIRST, then delete. Deleting the file and reloading AppArmor does not
    # unload a profile whose file is gone: it stays in the kernel and attaches to every
    # new claude process until reboot. Run 3 found this VM still carrying
    # claude-code-sandbox (unconfined) hours after a --revert that said it had reverted.
    $SUDO apparmor_parser -R "$CLAUDE_PROFILE" 2>/dev/null       || echo -n "$(basename "$CLAUDE_PROFILE")" | $SUDO tee /sys/kernel/security/apparmor/.remove >/dev/null 2>&1
    $SUDO rm -f "$CLAUDE_PROFILE"
    if $SUDO aa-status 2>/dev/null | grep -q "$(basename "$CLAUDE_PROFILE")"; then
      bad "$(basename "$CLAUDE_PROFILE") is STILL LOADED in the kernel"
      echo "        remove it with:"
      echo "          echo -n $(basename "$CLAUDE_PROFILE") | sudo tee /sys/kernel/security/apparmor/.remove"
      echo "        or reboot. Until then it attaches to every new $(command -v claude 2>/dev/null || echo claude)."
    else
      ok "removed and unloaded $CLAUDE_PROFILE"
    fi
  fi
  if [ -f "$BACKUP_DIR/profile-disabled" ]; then
    $SUDO rm -f "/etc/apparmor.d/disable/$(basename "$PROFILE")"
    $SUDO apparmor_parser -r "$PROFILE" 2>/dev/null && ok "re-enabled $(basename "$PROFILE")"
  fi
  # The retired sysctl from the earlier provisioning run, if still present.
  [ -f /etc/sysctl.d/99-claude-sandbox.conf ] && {
    $SUDO rm -f /etc/sysctl.d/99-claude-sandbox.conf
    $SUDO sysctl -w kernel.apparmor_restrict_unprivileged_userns=1 >/dev/null 2>&1
    ok "removed the ineffective sysctl override and restored the default"
  }
  $SUDO systemctl reload apparmor 2>/dev/null || $SUDO service apparmor reload 2>/dev/null
  $SUDO rm -rf "$BACKUP_DIR"
  if $SUDO aa-status 2>/dev/null | grep -qE "$(basename "$CLAUDE_PROFILE")"; then
    bad "revert INCOMPLETE - see the removal command above. A reboot also clears it."
  else
    ok "reverted. A reboot guarantees a clean state."
  fi
  exit 0
fi

# ---------------------------------------------------------------- try
mkdir -p "$BACKUP_DIR" 2>/dev/null

hdr "Before: probe with the sandbox forced on"
BEFORE="$(probe)"
echo "  result: $BEFORE"
if [ "$BEFORE" = "PROBE_PASS" ]; then
  ok "the sandbox already works. Nothing to change."
  exit 0
fi

apply_local_override() {
  # Least invasive and upgrade-safe: extend the shipped profile through its
  # local include rather than editing it.
  if [ ! -e "$PROFILE" ]; then bad "$PROFILE not present"; return 1; fi
  $SUDO mkdir -p "$(dirname "$LOCAL_OVERRIDE")"
  if [ -f "$LOCAL_OVERRIDE" ]; then
    $SUDO cp "$LOCAL_OVERRIDE" "$BACKUP_DIR/local-override.bak"
  else
    touch "$BACKUP_DIR/local-override.created"
  fi
  printf '# Added by sandbox-apparmor.sh to let the Claude Code sandbox start.\ncapability sys_admin,\n' \
    | $SUDO tee -a "$LOCAL_OVERRIDE" >/dev/null
  $SUDO apparmor_parser -r "$PROFILE" || { bad "apparmor_parser failed to reload the profile"; return 1; }
  ok "appended 'capability sys_admin,' to $LOCAL_OVERRIDE and reloaded"
}

apply_claude_profile() {
  # Give the Claude Code binary its own profile granting userns creation.
  local CB REAL
  CB="$(command -v claude 2>/dev/null)" || { bad "claude not on PATH"; return 1; }
  REAL="$(readlink -f "$CB")"
  [ -z "$REAL" ] && { bad "cannot resolve the claude binary"; return 1; }
  touch "$BACKUP_DIR/claude-profile.created"
  $SUDO tee "$CLAUDE_PROFILE" >/dev/null <<EOF
# Written by sandbox-apparmor.sh. Lets the Claude Code sandbox create a nested
# user namespace. Remove with: sandbox-apparmor.sh --revert
abi <abi/4.0>,
include <tunables/global>

profile claude-code-sandbox "$REAL" flags=(unconfined) {
  userns,
  include if exists <local/claude-code-sandbox>
}
EOF
  $SUDO apparmor_parser -r "$CLAUDE_PROFILE" || { bad "apparmor_parser rejected the profile"; return 1; }
  ok "installed $CLAUDE_PROFILE for $REAL"
  info "note: the binary path changes when Claude Code auto-updates; re-run this after an update"
}

apply_disable_profile() {
  # Most invasive: stop confining unprivileged bwrap image-wide.
  if [ ! -e "$PROFILE" ]; then bad "$PROFILE not present"; return 1; fi
  $SUDO mkdir -p /etc/apparmor.d/disable
  $SUDO ln -sf "$PROFILE" "/etc/apparmor.d/disable/$(basename "$PROFILE")"
  $SUDO apparmor_parser -R "$PROFILE" || { bad "apparmor_parser failed to unload the profile"; return 1; }
  touch "$BACKUP_DIR/profile-disabled"
  ok "disabled $(basename "$PROFILE")"
  info "this removes the restriction for everything on the image, not just Claude Code"
}

hdr "Applying option: $OPTION"
case "$OPTION" in
  local-override)  apply_local_override  || exit 1 ;;
  claude-profile)  apply_claude_profile  || exit 1 ;;
  disable-profile) apply_disable_profile || exit 1 ;;
  *) echo "  unknown option: '$OPTION'"; echo "  expected: local-override | claude-profile | disable-profile"; exit 2 ;;
esac

hdr "After: the same probe"
AFTER="$(probe)"
echo "  result: $AFTER"

hdr "Verdict"
if [ "$AFTER" = "PROBE_PASS" ]; then
  ok "option '$OPTION' WORKS. The sandbox starts."
  echo
  echo "  Give the team this change to bake into the image:"
  case "$OPTION" in
    local-override)  echo "    append 'capability sys_admin,' to $LOCAL_OVERRIDE, then apparmor_parser -r $PROFILE" ;;
    claude-profile)  echo "    install $CLAUDE_PROFILE (shown below), then apparmor_parser -r it"; echo; $SUDO cat "$CLAUDE_PROFILE" | sed 's/^/      /' ;;
    disable-profile) echo "    disable $(basename "$PROFILE") -- note this is image-wide; prefer a narrower option if one works" ;;
  esac
  echo
  echo "  Record the before/after output in testing/results/ as the evidence."
else
  bad "option '$OPTION' did NOT work. The sandbox still fails."
  echo
  echo "  Recent denials:"
  recent_denials | sed 's/^/        /'
  echo
  echo "  Revert this attempt before trying the next option:"
  echo "    ./sandbox-apparmor.sh --revert"
fi
