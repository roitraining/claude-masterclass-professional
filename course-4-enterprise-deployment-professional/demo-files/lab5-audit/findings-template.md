# Credential Audit: Findings

Audit target: `harbor-org` (fictional). Auditor: ____________  Date: ____________

Write one block per finding. A finding is a real credential or secret hygiene problem. Do not list a clean item as a finding.

- **File and line** may list more than one location when a finding genuinely spans files.
- **Severity** — high: already exposed, or live and unaccountable. Medium: exposure is possible but needs something further, and nothing shows it happened. Low: hygiene that does not expose a credential on its own.
- **Owner** — if the credential is not in the inventory and has no owner, write `unassigned - not in the inventory` and say who should own it.

## Finding 1

- **File and line:**
- **What is wrong:**
- **Risk:**
- **Severity:** high, medium, or low
- **Fix:**
- **Rotation step:**
- **Owner:**

## Finding 2

- **File and line:**
- **What is wrong:**
- **Risk:**
- **Severity:**
- **Fix:**
- **Rotation step:**
- **Owner:**

(Copy the block for each further finding.)

## Not a finding

List items you checked and found sound, with one line on why.

-

## Priority order

Rank the findings and give a reason for each position.

1.

## Rotation and ownership plan

For every credential in the inventory, **and every credential you found in the tree that is not in it**: the owner, how long it lives, where it is used, how it is rotated, and what happens when its owner leaves. Write `unknown` where the tree does not say, and `unassigned` where nobody owns it.

| Credential | Owner | Lifetime | Where used | Rotation | If the owner leaves |
|---|---|---|---|---|---|
|  |  |  |  |  |  |
