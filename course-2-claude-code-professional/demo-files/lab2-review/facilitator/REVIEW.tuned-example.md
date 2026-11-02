# Review instructions

## What Important means here

Reserve Important for findings that break behavior, expose data, or weaken access control: incorrect logic, off-by-one errors in loops or slices, handlers on the public router that do not check a role, credentials written into source, and SQL built from unbound values.

Style, naming, missing docstrings and refactoring ideas are Nit at most.

## Cap the nits

Report at most three Nits per pull request.

## Do not report

- Anything a unit test does not need to prove, and test-only placeholder values used against mocks
- Missing docstrings and formatting
- A handler registered on a Router created with `guard_role=...`. The router checks the role for every route on it.
- SQL where the only f-string content is generated `?` placeholders and every value is bound
- Integer truncation that the code or CLAUDE.md names as the fine policy

## Always check

- Read the surrounding file, and the Router the handler is registered on, before saying a check is missing.
- For every loop bound and slice, work one small example by hand before calling it an error.
- Money stays in integer cents.

## Evidence

Every Important finding needs a file and line, and a sentence saying what the code does, not what its name suggests. If you cannot point at the line, do not report it.
