# Professional 4 demo-files

Sample files for the Enterprise Deployment and Security Operations Professional labs. In the lab guides in `labs/`, `$FILES` means this folder. Everything is fictional: people, companies, domains (`example.com` and similar), and data. Every secret is a placeholder such as `FAKE-TOKEN-DO-NOT-USE`. Nothing here touches a real tenant. Scripts need Python 3.11 or later and the standard library only.

| Folder | Used by | Contents |
|--------|---------|----------|
| `lab1-identity` | Lab 1 | IdP notes, group mapping and offboarding CSVs, custom roles, `check_lab1.py`, and `facilitator/live_path_scorecard.md` (instructor only) |
| `lab2-compliance` | Lab 2 | Synthetic activity export (JSON and CSV, 439 events), control ticket and templates, `check_lab2.py`, and `facilitator/make_activity_export.py` (instructor only) |
| `lab3-harden` | Lab 3 | `lab3_brief.md`, `check_settings.py`, the `vuln-app` project with `attack_simulation.py` |
| `lab4-injection` | Lab 4 | `shipping-notes` repository with the payload, `defense_configs`, `record_sheet.csv`, `check_record.py` |
| `lab5-audit` | Lab 5 (take-home) | `harbor-org` tree with planted credential issues, and `facilitator/rubric.md` (instructor only) |

## Building the student pack

Run `./make-student-pack.sh <destination>`. It copies this folder and removes the
instructor-only items listed below. Do not hand out this folder as it stands.

**Withheld — these hold answer logic:**

| Path | Why |
|---|---|
| `lab1-identity/check_lab1.py` | Names all five planted defects |
| `lab2-compliance/check_lab2.py` | Names the four planted anomalies and their event ids |
| `lab1-identity/facilitator/` | Live-path scorecard |
| `lab2-compliance/facilitator/` | Export generator, which encodes the anomalies |
| `lab5-audit/facilitator/` | The C1–C5 rubric |

**Shipped — these are student tools and hold no answers:**

| Path | Why |
|---|---|
| `lab3-harden/check_settings.py` | Scores a configuration against stated acceptance criteria. Lab 3 Step 5 tells students to run it repeatedly |
| `lab3-harden/classroom-sandbox.sh` | Lab 3 Step 0 |
| `lab4-injection/check_record.py` | Scores the record sheet for **completeness and internal consistency**, not correctness. Lab 4 Part 4 tells students to run it. There is no right answer for it to leak: the result is whatever the model did |

`check_record.py` was previously listed as withheld while Lab 4 told students to run it.
It scores 65 mechanical points — filled columns, legal values, a defense named where
`stopped_by` requires one — and contains no planted item. It is a student file.


The demos have no files; their sample snippets are inline in `demos.md`.

Items that need rehearsal before class are listed in the Facilitator notes in `labs/` and the Instructor notes of `demos.md`.
