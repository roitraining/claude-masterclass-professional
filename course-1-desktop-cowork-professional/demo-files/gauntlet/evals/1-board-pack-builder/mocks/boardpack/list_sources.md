---
type: fixed
---

Result from list_sources:

## sources.md

# Data sources: Kestrel Freight board reporting

| Source | System of record for | Refresh |
|---|---|---|
| finance_ledger | Revenue, gross margin, EBITDA | Monthly, after close |
| sales_crm | Customers, churn, retention, pipeline | Daily; pipeline coverage is refreshed at each forecast review |
| hr_system | Headcount | Monthly |
| bank_feed | Cash | Daily |

When two sources report the same metric, the system of record wins for the board pack, and the difference is disclosed in a footnote.
