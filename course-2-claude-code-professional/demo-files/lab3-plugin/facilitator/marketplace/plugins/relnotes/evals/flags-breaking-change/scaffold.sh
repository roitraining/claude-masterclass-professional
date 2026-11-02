#!/usr/bin/env bash
# Builds a small fictional repository in the empty eval workspace.
set -e
g() { git -c user.name="Fixture" -c user.email="fixture@example.invalid" -c commit.gpgsign=false "$@"; }
git init -q -b main
echo "v1" > app.txt; git add -A; g commit -q -m "chore: initial import"
g tag v1.0.0
echo a >> app.txt; g commit -qam "feat(search): add fuzzy matching to the search box (#41)"
echo b >> app.txt; g commit -qam "fix(login): stop the session timer resetting on refresh (#43)"
echo c >> app.txt; g commit -qam "feat(api)!: drop the legacy /v1/token endpoint (#44)" -m "BREAKING CHANGE: clients must move to /v2/token."
echo d >> app.txt; g commit -qam "docs: update the install guide (#45)"
echo e >> app.txt; g commit -qam "perf(report): cache the monthly rollup (#46)"
