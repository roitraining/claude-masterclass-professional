# Demo 7 fallback: what a run looks like (outline, not a recording)

Use this when credits or time do not allow a live run. It describes the shape of the output so you can narrate over `facilitator/marketplace/plugins/relnotes/evals/` and a previously saved `report.html` if you have one. It contains no recorded results. Do not present numbers from it as real.

1. Command, run from the plugin folder:

```
claude plugin eval . --scaffold --ablation none --no-publish --runs 1 --threshold 0.8 --max-cost-usd 3 --allow-tools Write Edit "Bash(git *)"
```

2. What to point at while it runs:
   - Each case starts in an empty workspace. For cases with a `scaffold.sh`, the script builds the fictional repository first. That only happens because of `--scaffold`.
   - Read-only tools come from the case's `allowed_tools`. `Write`, `Edit` and `Bash` come from the `--allow-tools` grant, and a case that wanted one without a grant shows `not granted`.
   - `--no-publish` keeps the HTML report on this machine. Without it, the report is published to claude.ai when the account supports that.

3. What the end of a run contains: a per-case score, the grader verdicts, a total, and an exit code. Exit 0 means every case met the threshold. Exit 1 means a case scored below it or something failed. Exit 2 means a partial run, for example the cost ceiling was hit.

4. Questions for the room:
   - Which grader costs nothing to run (regex, tool_used, tool_order, file_exists) and which calls a judge model (llm, baseline)?
   - Why does `ignores-unrelated` matter as much as the cases that exercise the plugin?
   - What would you change in the command's `description` if `ignores-unrelated` failed?
