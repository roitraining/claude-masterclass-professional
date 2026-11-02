# Brightwater Risk Tier Scale

This is Brightwater's own scale for internal review routing. It is not the EU AI Act's tiers and it is not a NIST or ISO term. Do not mix them up.

| Tier | A use lands here when | Review route | Decision time | Who may accept the risk |
|---|---|---|---|---|
| Tier 1, Low | Only Public or Internal data. A person reviews anything before it leaves the company. No decision about a person. | Self-registration in the inventory | Same day | The use owner's manager |
| Tier 2, Moderate | Confidential data, or code, or output used in a business decision. A person reviews the output. | Owner and security check | 2 business days | The department head |
| Tier 3, High | Regulated data, or any decision or ranking about a person, or output sent to a customer without full review, or a customer contract imposes conditions. | AI Governance Board review | 10 business days | The accountable executive, in writing |

## Status flags (separate from the tier)

- **Not permitted as practiced:** the use as it runs today breaks a rule. It stays off until it is redesigned and routed again.
- **Shadow:** the use exists and is not in the inventory.
- **Changed:** the use was approved earlier and its data, vendor, or features have since changed. It is routed again.

## Tiering rules

1. Tier by the highest-risk fact, not the average. Confidential data plus a single Regulated field is Tier 3.
2. A person who reviews the output lowers the review burden only when the review is real: a named role, time to do it, and a record.
3. A use affecting hiring, pay, discipline, or access to a service is Tier 3 whatever the data.
4. The tier is set at intake and rechecked at each review date and whenever the use changes.
