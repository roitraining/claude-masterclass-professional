# Claude Code Professional: demo and lab files

Index of every file the demos and labs name. Everything is local text, YAML, JSON, Python or Markdown. Every person, company and figure is fictional. No file holds a real secret. The few credential-looking values are placeholders (`FAKE-TOKEN-DO-NOT-USE`, an all-zero organization id).

In the guides `$FILES` means this folder.

**Facilitator folders.** Each lab folder has a `facilitator/` subfolder with answer keys and reference solutions. Remove or withhold the `facilitator/` folders before you give `$FILES` to students. `lab2-review/score_review.py` reads `lab2-review/facilitator/answer_key.json`, so for Lab 2 give students the scorer and key together only after they have a findings file, or run the scorer yourself.

## Contents

| Folder | Used by | What is in it |
|---|---|---|
| `lab1-ci/tallybook/` | Lab 1, Demo 1 | The sample repository to copy into your own project: a tiny ledger with two failing tests, a CI workflow, and a CLAUDE.md |
| `lab1-ci/starters/github/` | Lab 1 | `claude.yml` and `claude-review.yml`, the starter workflows with planted traps |
| `lab1-ci/starters/gitlab/` | Lab 1 | `.gitlab-ci.yml`, the GitLab starter job with planted traps |
| `lab1-ci/fixtures/` | Lab 1 | `ISSUE-001.md`, `issue-body-injection.md`, `pr-description-injection.md` |
| `lab1-ci/security_gate.py` | Lab 1 | The local security gate (GitHub and GitLab), plus `gate-checklist-github.md`, `gate-checklist-gitlab.md`, `requirements.txt` |
| `lab1-ci/facilitator/` | Lab 1 | Hardened reference files that score 100 |
| `lab2-review/` | Lab 2, Demo 2 | `build_fixture.py`, `diffs/` (the eleven pull request diffs), starter `REVIEW.md`, `run_reviews.py`, `score_review.py`, `findings.schema.json`, `sample-findings.json` |
| `lab2-review/facilitator/` | Lab 2 | `ANSWER-KEY.md`, `answer_key.json`, a tuned `REVIEW.md` example |
| `lab3-plugin/relnotes-starter/` | Lab 3 | The plugin skeleton with a command, a hook, a subagent, a lint script, and an eval suite of six cases |
| `lab3-plugin/plugin_lint.py`, `marketplace-template/` | Lab 3 | Local plugin checks and a marketplace template |
| `lab3-plugin/facilitator/marketplace/` | Lab 3, Demo 6, Demo 7 | The reference marketplace with the finished plugin |
| `lab4-lsp/pylsp-plugin-starter/` | Lab 4 | The language server plugin task with one deliberate misconfiguration |
| `lab4-lsp/sample-project/` | Lab 4, Demo 8 | A small Python project with a known diagnostic and a symbol to navigate |
| `lab4-lsp/check_lsp.py`, `lsp_smoke.py` | Lab 4, Demo 8 | A static `.lsp.json` checker and a protocol-level smoke test |
| `lab4-lsp/facilitator/` | Lab 4 | The fixed file, a second misconfiguration variant, and a fixed plugin folder |
| `lab5-migration/` | Lab 5 | `scenario-sheet.md`, `runbook-template.md`, `rubric.md`, and `facilitator/model-answer-outline.md` |
| `demo2-review/` | Demo 2 | The documented review workflow example |
| `demo4-routine-vs-actions/` | Demo 4 | `comparison.md` |
| `demo5-checkpoint/` | Demo 5 | `nightly-fix-and-ship.yml` and `checkpoint-map.md` |
| `demo7-eval/` | Demo 7 | `expected-run-outline.md`, the fallback when a live run is not possible |
| `demo9-cutover/` | Demo 9 | `cutover-checklist.md`, `managed-settings-snippet.json`, `leftover_credentials_check.py` |

## Setup for the Python tools

Python 3.11 or later and Git 2.31 or later. `security_gate.py` needs PyYAML:

```
pip install pyyaml
```

The tools make no model calls and no network calls, except `run_reviews.py` and `claude plugin eval`, which call `claude` and use credits.
