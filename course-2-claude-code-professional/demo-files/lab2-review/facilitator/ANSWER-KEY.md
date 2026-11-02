# Lab 2 answer key (facilitator only)

Do not hand this folder to students before they score. `answer_key.json` is what `score_review.py` reads. Line numbers come from the files on each pull request branch and are produced by `build_fixture.py`, so a rebuilt fixture gives the same numbers.

## Planted bugs (5)

| Id | Pull request branch | File and line | Kind | What is wrong |
|---|---|---|---|---|
| B1 | pr-01-senior-waiver | lending/fines.py:15 | Logic error | `if is_senior or fee < WAIVER_THRESHOLD_CENTS` waives every senior's fine in full and every member's small fine. The docstring says seniors with small fines, so it must be `and`. The added test passes anyway. |
| B2 | pr-02-catalog-paging | lending/catalog.py:9 | Off-by-one | `items[start:start + size + 1]` returns one item too many on every page. The test asserts "at least" the page size, so it passes. |
| B3 | pr-03-delete-member | lending/api.py:32 | Missing authorization check | `delete_member` is on the public router and never calls `require_role`. Every sibling handler does. |
| B4 | pr-04-overdue-email | lending/notify.py:13 | Hard-coded secret | `SMTP_PASSWORD = "FAKE-TOKEN-DO-NOT-USE"` in source. The value is a deliberate fake placeholder. It shadows `lending/config.py`, which reads the environment. |
| B5 | pr-05-genre-filter | lending/catalog.py:7 | SQL injection | `genre` is formatted into the SQL text with an f-string. The title value is bound, which makes the unsafe part easy to miss. |

## False-positive bait (5)

Each of these looks like a bug and is not. A finding rated important on any of them is a false positive.

| Id | Pull request branch | File and line | Looks like | Why it is fine |
|---|---|---|---|---|
| F1 | pr-06-bulk-lookup | lending/catalog.py:8 | SQL injection | The f-string inserts only generated `?` placeholders. Every value is bound. CLAUDE.md allows generated placeholders. |
| F2 | pr-07-notify-tests | tests/test_notify.py:6 | Hard-coded secret | A placeholder used against a mocked SMTP object in a unit test. |
| F3 | pr-08-loan-gaps | lending/reports.py:9 | Off-by-one | `range(len(dates) - 1)` is correct for consecutive pairs, and fewer than two dates returns 0. |
| F4 | pr-09-waive-all | lending/admin_api.py:15 | Missing authorization check | The route is on `admin`, a `Router(guard_role="librarian")`. `Router.dispatch` checks the role for every route. |
| F5 | pr-10-prorated-fine | lending/fines.py:14 | Logic error (truncation) | `int()` truncates on purpose. Policy LIB-7 in CLAUDE.md and the docstring says truncate, never round up. |

## Clean pull request (1)

pr-11-docstrings adds two docstrings and changes nothing else. Any important finding is a false positive. Nits are allowed and capped for Gold.

## Scoring and tiers

`python score_review.py findings.json` prints bugs caught, false positives, nits, precision and a tier.

- Gold: all 5 bugs, at most 1 false positive, at most 6 nits.
- Silver: at least 4 bugs, at most 3 false positives.
- Bronze: at least 3 bugs, at most 5 false positives.

These thresholds are untested with real model runs. Rehearse once with the sample reviewer prompt and adjust the numbers at the top of `score_review.py` (`TIERS`) if the class would otherwise all land in one tier. `sample-findings.json` is hand-written, not a recorded run. It scores Silver and exists to test the scorer and to show the JSON shape.

## What a good tuning looks like

- Defines Important narrowly: wrong behavior, a missing authorization check, a credential in code, injectable SQL.
- Caps nits and says what CI or the team does not care about (style, docstrings, naming).
- Cites the repository's own rules so the reviewer can clear the bait: generated placeholders are allowed, router-level guards count, truncation is policy LIB-7, test placeholders are not secrets.
- Requires evidence before a finding is raised: a file and line, and a statement of what the code does instead of what its name suggests.
- Does NOT list the planted bugs or the bait pull request names. If a student's REVIEW.md mentions a branch name or a line number, it is overfit. Mark it down and ask how it would behave on the next repository.

## Where the traps are

- B2 and B1 are covered by a passing test, so "tests pass" is not evidence. Watch for students who excuse them.
- B5 looks safe because half the query is bound.
- F4 needs the reader to open `lending/web.py` or the top of `admin_api.py`. A reviewer working from the diff alone will usually flag it, which is why the driver lets Claude read the repository.
- A REVIEW.md that says "report fewer things" gets fewer false positives and misses bugs. The scorer shows both numbers on purpose.
