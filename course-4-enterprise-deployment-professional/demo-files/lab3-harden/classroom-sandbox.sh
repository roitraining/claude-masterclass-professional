#!/usr/bin/env bash
# Turn the Claude Code sandbox on for this classroom VM, and turn it back off.
#
#   ./classroom-sandbox.sh --check     is the sandbox blocked? (changes nothing, no sudo)
#   ./classroom-sandbox.sh --on        let the sandbox start (needs sudo)
#   ./classroom-sandbox.sh --off       put the machine back as you found it
#
# WHY THIS EXISTS, AND WHY YOU WOULD NOT DO THIS AT WORK
#
# On Ubuntu 24.04 and later, the AppArmor profile `bwrap-userns-restrict` stops
# unprivileged processes from creating nested user namespaces. Claude Code's sandbox is
# built on bubblewrap, which needs exactly that, so on a stock image every sandboxed Bash
# call fails with:
#
#   apply-seccomp: write /proc/self/setgroups
#   (nested userns is capability-restricted; caller must provide CAP_SYS_ADMIN): Permission denied
#
# `--on` disables that profile. Note what it does NOT do: it does not grant the
# permission to Claude Code specifically. The profile is image-wide, so disabling it lifts
# the restriction for every process on the machine. We tried the two narrower options
# first and neither can work -- the denial is raised inside `unpriv_bwrap`, the profile
# that `/usr/bin/bwrap` transitions into, so confining the calling binary changes nothing
# about what its child transitions to.
#
# That trade -- weaken a machine-wide control to switch on one application's sandbox -- is
# the kind of decision this course is about, and on a production fleet the answer is
# usually no. It is defensible HERE because this is a disposable single-purpose classroom
# VM holding nothing but fake credentials, and because the alternative is being unable to
# run the exercise that teaches you what the sandbox does. Make the same call on a
# developer's laptop or a build server and you have traded a real control for convenience.
#
# Run `--off` when you are finished. A reboot also restores the default.

set -u
PROFILE="/etc/apparmor.d/bwrap-userns-restrict"
DISABLE_LINK="/etc/apparmor.d/disable/$(basename "$PROFILE")"
SUDO=""; [ "$(id -u)" -ne 0 ] && SUDO="sudo"

case "${1:-}" in --check|--on|--off) MODE="$1" ;; *)
  sed -n '2,6p' "$0" | sed 's/^# \{0,1\}//'
  exit 2 ;;
esac

if [ "$(uname -s)" != "Linux" ]; then
  echo "This script is for Linux. On macOS the sandbox uses Seatbelt and needs no change."
  exit 1
fi
if [ ! -e "$PROFILE" ] && [ ! -L "$DISABLE_LINK" ]; then
  echo "[ OK ] $PROFILE is not present on this machine."
  echo "       Nothing here is blocking the sandbox. If sandboxed commands still fail,"
  echo "       the cause is something else - tell your instructor what the error says."
  exit 0
fi

loaded() { $SUDO aa-status 2>/dev/null | grep -q 'unpriv_bwrap'; }

report() {
  if [ -L "$DISABLE_LINK" ]; then
    echo "[ OK ] bwrap-userns-restrict is DISABLED - the sandbox can start."
    echo "       Put it back with: $0 --off"
  elif loaded; then
    echo "[INFO] bwrap-userns-restrict is ACTIVE - the sandbox cannot start on this machine."
    echo "       Sandboxed Bash calls will fail with 'apply-seccomp ... Permission denied'."
    echo "       That is a platform limit, not a mistake in your configuration."
    echo "       Switch it off for this lab with: $0 --on"
  else
    echo "[ OK ] unpriv_bwrap is not loaded - nothing is blocking the sandbox."
  fi
}

case "$MODE" in
  --check) report ;;

  --on)
    if [ -L "$DISABLE_LINK" ]; then echo "[ OK ] already disabled. Nothing to do."; exit 0; fi
    $SUDO mkdir -p "$(dirname "$DISABLE_LINK")" || exit 1
    $SUDO ln -sf "$PROFILE" "$DISABLE_LINK" || exit 1
    if $SUDO apparmor_parser -R "$PROFILE" 2>/dev/null; then
      echo "[ OK ] disabled bwrap-userns-restrict. The sandbox can now start."
      echo "       Machine-wide, for every process - see the notes at the top of this file."
      echo "       Undo with: $0 --off"
    else
      $SUDO rm -f "$DISABLE_LINK"
      echo "[FAIL] apparmor_parser could not unload the profile. Nothing was changed."
      echo "       Check you have sudo, then tell your instructor."
      exit 1
    fi ;;

  --off)
    if [ ! -L "$DISABLE_LINK" ]; then echo "[ OK ] not disabled by this script. Nothing to do."; exit 0; fi
    $SUDO rm -f "$DISABLE_LINK"
    if $SUDO apparmor_parser -r "$PROFILE" 2>/dev/null; then
      echo "[ OK ] re-enabled bwrap-userns-restrict. The machine is as you found it."
    else
      echo "[WARN] could not reload the profile. Reboot to restore the default."
      exit 1
    fi ;;
esac
