# Success criteria (write this before you build the harness)

Fill in every line. Keep it to one page. The harness exists to measure these, so a criterion you cannot measure needs a different wording.

## The job

One sentence: what the agent is for, and what it must never do.

## Correctness

- Which questions must it answer correctly, and from which source (a tool result, a policy, arithmetic)?
- What counts as a correct "not found" answer?

## Tool behavior

- Which tool must it call for each kind of task?
- Which tools must it never call? Why?
- The most tool calls a task may use before you call it a runaway:

## Safety

- What must it ignore if it appears inside a tool result?
- What data may it reach? What must it never reveal?

## Limits

- Maximum turns per task:
- Maximum spend per task (set by your instructor or your own cap):
- Cost target for the Gold tier (mean cost per task):

## Open-ended output

- Which output needs a judge, and what are the criteria (3 to 4 short lines)?
- What judge score counts as a pass?

## What this does not cover

Name at least two failures your golden tasks cannot catch.
