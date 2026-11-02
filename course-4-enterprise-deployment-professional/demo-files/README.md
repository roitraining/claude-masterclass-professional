# Professional 4 demo-files

Sample files for the Enterprise Deployment and Security Operations Professional labs. In `labs.md`, `$FILES` means this folder. Everything is fictional: people, companies, domains (`example.com` and similar), and data. Every secret is a placeholder such as `FAKE-TOKEN-DO-NOT-USE`. Nothing here touches a real tenant. Scripts need Python 3.11 or later and the standard library only.

| Folder | Used by | Contents |
|--------|---------|----------|
| `lab1-identity` | Lab 1 | IdP notes, group mapping and offboarding CSVs, custom roles, `check_lab1.py`, live path scorecard (instructor) |
| `lab2-compliance` | Lab 2 | Synthetic activity export (JSON and CSV, 439 events), control ticket and templates, `check_lab2.py`, `instructor/` generator (instructor only) |
| `lab3-harden` | Lab 3 | `lab3_brief.md`, `check_settings.py`, the `vuln-app` project with `attack_simulation.py` |
| `lab4-injection` | Lab 4 | `shipping-notes` repository with the payload, `defense_configs`, `record_sheet.csv`, `check_record.py` |
| `lab5-audit` | Lab 5 (take-home) | `harbor-org` tree with planted credential issues, `rubric.md` (instructor) |

Instructor-only items: `lab1-identity/live_path_scorecard.md`, `lab2-compliance/instructor/`, `lab5-audit/rubric.md`. The checker scripts hold answer logic: hand them out after students submit.

The demos have no files; their sample snippets are inline in `demos.md`.

Items that need rehearsal before class are listed in the Facilitator notes of `labs.md` and the Instructor notes of `demos.md`.
