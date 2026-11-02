# Tallybook (Lab 1 sample repository)

A tiny fictional ledger library. Four tests exist and two fail: `monthly_total` drops the last entry of the month. The failing test is the work item for the `@claude` trigger test in Lab 1.

Copy this folder into your own personal or sample repository. Do not use a repository that holds real work.

```
python -m venv .venv
. .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install pytest
python -m pytest -q
```

The starter workflow files are not in this folder. They are in `../starters/`, so you add them to your repository on purpose.
