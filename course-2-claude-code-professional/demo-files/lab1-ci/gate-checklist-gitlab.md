# Lab 1 security gate checklist: GitLab CI/CD

`security_gate.py` scores a `.gitlab-ci.yml` that runs the `claude` command in a job. A file passes at 90 or more with every CRITICAL check ok. Pass `--platform gitlab` if your file has another name.

| Check | Points | Critical | The question it asks |
|---|---|---|---|
| L1 Rules and who can start a job | 20 | Yes | Does the job have rules? Can a merge request from a fork start it? Can the trigger API start it without a protected-ref condition? |
| L2 Secrets handling | 20 | Yes | Is the API key defined in the file, printed by a script line, or exposed by an environment dump? |
| L3 Untrusted text | 20 | Yes | Is text an outsider wrote (a merge request title or description, a commit message, a branch name, the trigger payload variables) pasted into the claude command line or prompt? |
| L4 Tool grants | 15 | No | Does the command name its tools, with nothing broader than the job needs? Are permission checks left on? |
| L5 Cost and runtime limits | 10 | No | Is there a turn limit and a job timeout? |
| L6 Loop and overlap control | 15 | No | Can two runs overlap on the same merge request? Can Claude's own push start another run? |

Run it:

```
pip install pyyaml
python security_gate.py .gitlab-ci.yml
python security_gate.py .gitlab-ci.yml --json
```

Limits of the gate. It reads the file only. It cannot see whether `ANTHROPIC_API_KEY` is masked or protected in Settings, CI/CD, Variables, which token the job uses, branch protection, or who can run pipelines. Check those by hand and write down what you saw.

Notes on where this checklist is stricter than the documentation. The GitLab page's example job grants `Bash Read Edit Write mcp__gitlab` and passes `$AI_FLOW_INPUT` into the prompt for mention-driven runs. The gate treats a bare `Bash` grant and a prompt built from a trigger payload as findings, because anyone who can post a comment can influence both. That is a lab design rule, not a product requirement.
