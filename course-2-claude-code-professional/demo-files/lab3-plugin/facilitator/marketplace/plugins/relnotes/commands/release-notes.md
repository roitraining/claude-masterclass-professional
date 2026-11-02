---
description: Draft RELEASE_NOTES.md from the git log between two refs, grouped by change type. Use when asked for release notes or a changelog for a range of commits.
allowed-tools: Read, Write, Agent, Bash(git log *), Bash(git tag *), Bash(git describe *)
---

Write release notes for a range of commits and save them as `RELEASE_NOTES.md` in the repository root.

1. Pick the range. If the user names a starting tag or ref, use it. Otherwise use the latest tag (`git describe --tags --abbrev=0`). The end is the ref the user names, or HEAD.
2. Read the log for the range, including message bodies: `git log --no-merges --format='%h %s%n%b%n--' <from>..<to>`.
3. Sort each commit into exactly one section:
   - Breaking changes: a type marked with `!` (for example `feat(api)!:`) or a `BREAKING CHANGE:` footer
   - Features: `feat`
   - Fixes: `fix`
   - Other changes: everything else (`docs`, `chore`, `perf`, `refactor`, and so on)
4. Write the file in this exact shape, with sections in this order, and leave out a section that has no entries:

```
# Release notes: <to> (since <from>)

## Breaking changes
- Plain-language description (#PR) (a1b2c3d)

## Features
- ...
```

   Every bullet is one sentence of plain language, then the pull request number if the subject has one, then the short commit hash in parentheses, at the end of the line.
5. Before you tell the user the notes are done, run the `changelog-auditor` agent. Give it the log text from step 2 and the path of the draft. Fix every problem it reports, then run it again if you changed anything.
6. Never invent an entry. If the user asks for a line about something the log does not contain, leave it out and say so in your reply.
7. Change nothing except `RELEASE_NOTES.md`. Do not tag, commit or push.
