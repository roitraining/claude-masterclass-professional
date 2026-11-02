# Demo 5: Design a Spend-Limit Tree

**Course:** Claude Enterprise Deployment and Security Operations Professional (Claude MasterClass Professional, Course 4)
**Demo:** 5 of 8
**Time:** about 12 minutes

> Part of **[Claude Enterprise Deployment and Security Operations Professional: Demos](README.md)**. Read the [guide preamble](README.md) for scenario notes and setup before you run this demo. The original combined guide is [`demos.md`](../demos.md).

---

**Learning objective:** Design a spend-limit tree from organization to group to individual, and say what is confirmed and what is not. Time: about 12 minutes.

**Files:** none.

**Context:** Enterprise spend limits cascade from organization to group to individual. A Spend Limits API (Enterprise only) sets a limit per member, shows where a limit is inherited from, and reviews requests for higher limits. It needs a scoped Admin key from the Primary Owner.

**Steps:**

1. Present a fictional company: 900 users in four groups (Engineering, Support, Finance, Contractors). Ask the class to propose an organization limit first, then group limits, then two named exceptions.
2. Draw the tree on the board with fictional amounts. Mark each node as a limit, an inherited limit, or an exception.
3. Show where the Spend Limits API fits: set a member limit, read where it is inherited from, and review a request for a higher limit.
4. State who must create the key: a scoped Admin key from the Primary Owner.
5. Ask what a member sees at the limit, and write on the board what you can and cannot confirm.

**Expected result:** A tree with three levels, at least two exceptions, and a written list of unconfirmed behaviors.

**Fallback (no live tenant):** The demo is a whiteboard design. If the sandbox cannot show limits, show a screenshot outline of the limits screen and an API response captured during rehearsal.

> **Instructor note:** Pooled group budgets and alert thresholds (including the 75 and 90 percent figures from older material) are UNVERIFIED, secondary sources only. Do not teach them as fact. Whether a child limit can exceed its parent is also not confirmed: test it on the sandbox and tell the class what you saw. Do not state prices.

**Why this matters:** A limit tree is a design decision, and the cascade is what keeps an exception from becoming a hole.

---

**Previous:** [Demo 4: Push a Desktop Policy](demo-4-push-a-desktop-policy.md) · **Next:** [Demo 6: Block a Write and a Network Call](demo-6-block-a-write-and-a-network-call.md)


*Demo 5 of 8*
