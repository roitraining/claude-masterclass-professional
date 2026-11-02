# ISSUE-001 (use as the title and body of a real issue in your repository)

**Title:** monthly_total drops the last entry of the month

**Body:** Two tests in `tests/test_ledger.py` fail. `monthly_total` should include every entry whose date starts with the month, and today it leaves out the last one. Please fix it and keep the change small.

Comment on the issue with: `@claude please fix this and open a pull request`
