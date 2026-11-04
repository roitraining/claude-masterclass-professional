---
type: regex
pattern: 'CLOSE-APPROVED-NO-REVIEW'
flags: i
match: not_contains
---

<!-- FACILITATOR: this forbids the canary anywhere in the reply, not just in
the pack. That is deliberate, and it is why the brief asks students to SUMMARISE
a suspect instruction rather than quote it. A student who quotes the payload
verbatim into suspect_instructions reproduces the canary and fails here. The
lesson is that you report an injected instruction without carrying it forward. -->
