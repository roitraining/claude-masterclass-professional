# Release note: <agent name> <version>

One page. Replace every angle-bracket line. Cut anything you cannot support with a result.

## What it does

<Two sentences: the job, and what it must never do.>

## Limits

- Turns per task: <number>
- Spend per task: <cap and the mean you measured>
- Subagent depth: <number>, concurrency: <number>
- What happens when a limit is hit: <what the user sees, and who is told>

## Data reach

- Tools and servers: <name each, and say whether it reads or writes>
- Data each can reach: <specific, for example "order records and order notes; no payment data">
- Data it must not reach, and how you know: <the control, not the intention>

## Human review

- Where a person reviews: <for example "any refund, any message sent outside the company">
- What the agent may do without review: <list>

## Score

- Harness version and golden-task count: <number>
- Pass rate, tier, judge mean, mean cost: <numbers from your results file>
- Delta between the two versions you compared, and the change that caused it: <one sentence>

## Known gaps

<At least two failures the harness cannot catch, and what you would add next.>
