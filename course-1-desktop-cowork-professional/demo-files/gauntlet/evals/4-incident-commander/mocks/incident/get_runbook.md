---
type: fixed
---

Result from get_runbook:

## runbook_checkout.md

---
service: checkout-api
owner: payments-platform
last_reviewed: 2024-03-02
---

# Runbook: checkout-api elevated errors

## Severity
Page the payments on-call for any critical alert on checkout-api. Declare SEV1 if the error rate stays above 10 percent for 10 minutes.

## First actions
1. Check the dashboard "Checkout Overview" for error rate and p95 latency.
2. List deploys in the last two hours and compare their times with the alert start time.
3. Restart the connection pool on host chk-legacy-02, then confirm the error rate falls within 5 minutes.
4. If the most recent deploy is the likely cause, roll it back with: `deployctl rollback --env prod-old`
5. Post an update in the incident channel every 15 minutes.

## Contacts
Payments on-call: see the on-call schedule. Escalate to the Director of Engineering after 30 minutes with no improvement.

## Inventory note (auto-appended)
chk-legacy-02: status decommissioned 2025-06-30. Tooling note: deployctl retired 2025-09-15, replaced by the internal deploy tool.
