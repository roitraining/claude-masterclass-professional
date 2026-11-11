#!/usr/bin/env bash
# Build the Course 4 student pack: a copy of demo-files with the instructor-only
# material removed.
#
#   ./make-student-pack.sh /path/to/output      write the pack there
#   ./make-student-pack.sh --list               show what would be removed, change nothing
#
# The withheld list is the one in README.md. If you add a checker or a facilitator file,
# add it here too -- a file that is not on this list ships to students.
set -eu

WITHHOLD="
lab1-identity/check_lab1.py
lab1-identity/facilitator
lab2-compliance/check_lab2.py
lab2-compliance/facilitator
lab5-audit/facilitator
"

SRC="$(cd "$(dirname "$0")" && pwd)"

if [ "${1:-}" = "--list" ]; then
  echo "Withheld from the student pack:"
  for p in $WITHHOLD; do
    if [ -e "$SRC/$p" ]; then echo "  [present] $p"; else echo "  [MISSING] $p  <- check the list"; fi
  done
  echo
  echo "Shipped to students (no answer logic):"
  echo "  lab3-harden/check_settings.py     scores a configuration, not an answer key"
  echo "  lab3-harden/classroom-sandbox.sh  Lab 3 Step 0"
  echo "  lab4-injection/check_record.py    scores completeness and consistency only"
  exit 0
fi

DEST="${1:-}"
[ -z "$DEST" ] && { sed -n '2,8p' "$0" | sed 's/^# \{0,1\}//'; exit 2; }
[ -e "$DEST" ] && { echo "Refusing to overwrite an existing path: $DEST"; exit 1; }

mkdir -p "$DEST"
# -a would carry the script and the README's instructor section; copy, then prune.
cp -R "$SRC/." "$DEST/"
rm -f "$DEST/make-student-pack.sh"

for p in $WITHHOLD; do
  if [ -e "$DEST/$p" ]; then
    rm -rf "$DEST/$p"
    echo "  removed  $p"
  else
    echo "  WARNING  $p was not in the copy - the withheld list may be stale"
  fi
done

# Belt and braces: nothing named check_lab*.py or any facilitator folder should survive.
LEFT="$(find "$DEST" \( -name 'check_lab*.py' -o -name 'facilitator' \) -print 2>/dev/null || true)"
if [ -n "$LEFT" ]; then
  echo
  echo "REFUSING TO FINISH - instructor material is still present:"
  echo "$LEFT" | sed 's/^/    /'
  echo "  Fix the withheld list in this script, delete $DEST, and run it again."
  exit 1
fi

echo
echo "Student pack written to $DEST"
echo "Kept deliberately: lab3-harden/check_settings.py, lab3-harden/classroom-sandbox.sh,"
echo "lab4-injection/check_record.py - the labs tell students to run all three."
