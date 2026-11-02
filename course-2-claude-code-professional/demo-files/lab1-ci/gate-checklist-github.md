# Lab 1 security gate checklist: GitHub Actions

`security_gate.py` scores each workflow that calls `anthropics/claude-code-action`. A file passes at 90 or more with every CRITICAL check ok. The checklist says what each check asks for. It does not say how to fix the file.

| Check | Points | Critical | The question it asks |
|---|---|---|---|
| T1 Who can trigger a run | 15 | Yes | Can someone without write access, or someone outside the repository, start a run? Does a comment or issue trigger filter events before a runner starts? |
| T2 Permissions granted | 10 | No | Is there an explicit permissions block, and does it grant only what this workflow's job needs? |
| T3 Secrets handling | 15 | Yes | Can a secret reach a log, or sit in the file as a literal value? |
| T4 Bot loop control | 10 | No | Can Claude's own activity, or another bot, start the workflow again? Are overlapping runs capped? |
| T5 Untrusted text | 15 | Yes | Is text an outsider wrote (an issue, a pull request description, a title, a branch name) expanded into a shell command or pasted into the prompt? |
| T6 Tool grants | 10 | No | Does the run name its tools, with nothing broader than the job needs? Are permission checks left on? |
| T7 Cost and runtime limits | 10 | No | Is there a turn limit and a job timeout? |
| T8 Action reference | 5 | No | Is the action pinned to its v1 release or a full commit SHA? |
| T9 Pushes that start CI | 10 | No | Will your CI workflow run on a commit Claude pushes? |

Run it:

```
pip install pyyaml
python security_gate.py .github/workflows
python security_gate.py .github/workflows/claude.yml --json
```

Limits of the gate. It reads the file only. It cannot see repository settings (branch protection, secret scope, who has write access, whether Actions can approve pull requests), so a passing file still needs those checked in the repository. Check them by hand and write down what you saw.
