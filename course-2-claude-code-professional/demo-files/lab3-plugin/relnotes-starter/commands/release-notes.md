---
description: Write release notes.
---

TODO: write the command body so that the evals in `evals/` pass.

The command should:

- work out the range of commits to cover, from a tag or ref the user names, or from the latest tag to HEAD
- read the git log for that range
- write `RELEASE_NOTES.md` in the format the checker script in `scripts/` enforces
- have the `changelog-auditor` agent check the draft before finishing
- never invent an entry and never change anything except `RELEASE_NOTES.md`
