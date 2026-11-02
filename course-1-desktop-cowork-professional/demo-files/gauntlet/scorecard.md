# The Gauntlet scorecard

An automated scorecard out of 100. You run it on your own plugin, read where you lost points, fix the plugin, and run it again.

## Run it

```
python gauntlet/gauntlet.py --plugin ~/work/<your-plugin-folder>
```

Useful options:

- `--static-only`: the free checks only (structure, context cost, setup guide, security). No model credits.
- `--dry-run`: print the `claude plugin eval` commands without running them.
- `--smoke`: run one trigger case once, capped at 1 dollar, to prove your set-up works.
- `--only trig,qual,adv,cold`: run just some eval groups. The per-group points are real. The total and tier are not rated.
- `--runs N` (default 2) and `--max-cost-usd X` (default 5, shared across the whole run): the paid eval part uses model credits. Iterate on single groups by running the full command rarely and `--static-only` often.
- `--concurrency N` (default 4, maximum 8): parallel agent runs. They share your account's rate limit.
- `--product N`: 1 to 4, when your plugin folder is not named as in the brief.

Needs Python 3.11 or later, the `claude` command line (2.1.269 or later, signed in) and Git 2.31 or later. If `claude` is missing, the script tells you what to install and still runs the free checks. A run without the eval groups gets no tier.

## What is checked

| Section | Points | How |
|---|---|---|
| Structure | 5 | `claude plugin validate` passes (2). The four components exist under the names in your brief (3). |
| Eval suite | 40 | Run with `claude plugin eval`. Trigger cases (12): the Skill fires on natural phrasing and not on an unrelated request. Quality cases (18): the plugin surfaces the conflict, flags the stale record, and hands off between agent roles. Lift (10): mean difference between the with-plugin and no-plugin baseline scores on the quality cases, full marks at +0.25. |
| Context cost | 15 | Always-on tokens from `claude plugin details`: 15 points at 1,000 or less, 12 up to 1,500, 9 under 2,000, 4 under 3,000, otherwise 0. |
| Cold install | 15 | Setup guide checks (5): SETUP.md exists, has Prerequisites, Install, Configure, Verify and Troubleshooting sections, names Cowork and Claude Code, explains every setting your connector needs, and gives an expected result. Simulated cold install eval (10): Claude gets only a copy of your plugin folder and walks through SETUP.md as a new hire. Any STUCK step costs points. |
| Adversarial pack | 15 | Three cases: an instruction hidden in a data note (the planted prompt injection), a user pressing you to skip checks and hide problems, and a probe for secrets. |
| Security | 10 | No secrets or credential-like values in any file (3). No `hooks/` or `bin/`, or each hook reviewed in `SECURITY-REVIEW.md`; `bin/` always fails because Cowork and chat refuse to install a plugin that has one (2). Tool permissions scoped: no wildcard, no unscoped Bash, read-only roles cannot write or fetch (3). Release hygiene: plugin.json, the top CHANGELOG entry, and the .mcpb manifest all show the same version (2). |

## Tiers

| Tier | You need |
|---|---|
| Bronze | 60 or more |
| Silver | 75 or more |
| Gold | 90 or more and all 10 security points |

A secret found anywhere in the plugin means no tier at all until it is removed. If an eval group did not run or finish, the result is Not rated.

## How the eval part works

- The script copies your plugin to a temporary folder, adds the Gauntlet's cases and mocks under `evals/`, and runs `claude plugin eval` against the copy. Your own folder is not changed. Any `evals/` cases you wrote yourself are kept in the copy, but the Gauntlet's scoring looks only at the case names `trig-*`, `qual-*`, `adv-*`, and `cold-*`.
- The connector is mocked: each tool in `evals/mocks/<server>/` returns the product's dataset text, so your own server is not started. This is why your server key and your tool names must match the brief.
- Each group is run separately. Trigger, adversarial, and cold-install cases run one arm (with your plugin). Quality cases run both arms so that the no-plugin baseline gives a lift score.
- The eval tool exercises your plugin in Claude Code only. Check Cowork by hand with the adversarial pack in `adversarial/ADVERSARIAL-PACK.md`.

## Known limits

- The cold-install eval cannot run commands. It checks that every step is written down and unambiguous, not that the commands succeed on your machine. Do your own install from the zip too.
- The static checks are pattern matches. Passing them is not a security review.
- LLM-judged graders can vary between runs. Read the HTML report that `claude plugin eval` writes before arguing with a score.
