# Release note: <plugin-name> <version>

Date: <YYYY-MM-DD>  Author: <name>

## What it does

<Two sentences. The job the plugin does and for whom.>

## What is in it

- Skill: `<skill>`: <when it fires>
- Connector: `<server>` with tools `<tool>`, `<tool>`, `<tool>`. Also packaged as `<file>.mcpb`.
- Agents: `<agent>` (<read-only or not>) hands off to `<agent>` using the handoff JSON.
- Commands: `/<plugin>:<command>`, `/<plugin>:<command>`

## Gauntlet score

Total: <score> / 100. Tier: <Bronze, Silver, or Gold>.

| Section | Points | Max |
|---|---|---|
| Structure | | 5 |
| Eval suite | | 40 |
| Context cost | | 15 |
| Cold install | | 15 |
| Adversarial pack | | 15 |
| Security | | 10 |

Always-on cost: <tokens> tokens. Baseline lift on quality cases: <delta>.

## Known limits

- <What the plugin does not do or does not verify, for example Cowork behavior checked by hand only>
- <Any Gauntlet check you lost points on and why you accepted it>

## What it can reach

<The folders and systems the connector reads, and whether it writes anything.>

## Install

See `SETUP.md`. Supported: <chat / Cowork / Claude Code and what loads on each>.

## Changes since the last version

<Copy the newest CHANGELOG entry.>

## Self-demo

<Link or file name of the 60-second recording.>
