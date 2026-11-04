# RVC Image Requirements — Claude MasterClass Professional

**For:** whoever maintains the ROI Virtual Classroom image
**Target:** Ubuntu 26.04.1 LTS
**Verify with:** `testing/provision-rvc.sh --check`

The 2026-11-03 test run could not complete any lab cleanly. 10 of 21 labs were
blocked outright, and most of that traces to the image rather than the course
content. Everything below is needed before a retest is meaningful.

Each item says which courses it unblocks, so the list can be triaged rather
than taken whole.

---

## How to use this

```bash
git clone -b lab-testing/rvc-2026-11 \
  https://github.com/roitraining/claude-masterclass-professional.git
cd claude-masterclass-professional/testing

./provision-rvc.sh --check      # before: what is missing (changes nothing)
./provision-rvc.sh --install    # apply everything installable
./provision-rvc.sh --check      # after: should be all OK
```

`--check` makes no changes and needs no sudo, so it is safe to run on a live
image. Keep the before and after output as the evidence that provisioning works.

The sandbox change is held back behind a separate flag because it alters the
image's security posture — see item 1.

---

## 1. Sandbox — needs a decision, not just an install

**Unblocks:** Course 4 Lab 3 (its core exercise), Course 2 Lab 3 evals,
Course 4 Lab 4 defences, probably the Course 1 Gauntlet.

Ubuntu 26.04 sets `kernel.apparmor_restrict_unprivileged_userns = 1` and ships
the `bwrap-userns-restrict` AppArmor profile. Every sandboxed Bash call from
Claude Code fails with:

```
apply-seccomp: write /proc/self/setgroups
(nested userns is capability-restricted; caller must provide CAP_SYS_ADMIN):
Permission denied
```

Two ways to fix it, and the choice is the team's:

| Option | Command | Trade-off |
|---|---|---|
| **A. Targeted AppArmor profile** | A profile granting `userns create` to the Claude Code binary | Narrower, preferred. **We have not written or tested this profile** — it needs someone who knows AppArmor |
| **B. Relax the sysctl image-wide** | `provision-rvc.sh --install --allow-sandbox-fix` writes `kernel.apparmor_restrict_unprivileged_userns=0` to `/etc/sysctl.d/99-claude-sandbox.conf` | Simple and reversible, but weakens unprivileged user-namespace restrictions for everything on the image |

Option B is what the script can do unattended. **If option A is viable, prefer
it** — we are asking for a security relaxation on a training VM, and a targeted
profile is the better answer if your team can produce one.

Why this matters beyond "a lab fails": with the sandbox down, **Course 4 Lab 3
tells students an attack is blocked when it is not.** The tester confirmed the
secrets file was read (`read 83 bytes from config/secrets.env`) despite the deny
rules. That is worse than a broken lab.

Revert option B with: `sudo rm /etc/sysctl.d/99-claude-sandbox.conf` and reboot.

## 2. `python` command and virtual environments

**Unblocks:** nearly every lab's first command, across all five courses.

The image has `python3` but no `python`, and PEP 668 refuses `pip install`
outside a virtual environment — including `--user`.

Install:

```
python-is-python3   python3-venv   python3-pip
```

The script also pre-builds three virtual environments under `~/.venvs`, so no
student hits the PEP 668 wall:

| venv | Packages | For |
|---|---|---|
| `mc-agent-sdk` | `claude-agent-sdk`, `mcp[cli]` | Course 3, all five labs |
| `mc-ci` | `pyyaml>=6.0` | Course 2 Lab 1 |
| `mc-lsp` | `python-lsp-server[pyflakes,pycodestyle]` | Course 2 Lab 4 |

Package choices come from the courses' own `requirements.txt` files and the
Course 2 Lab 4 Step 1 command, not from our judgement. Versions are deliberately
unpinned upstream; pin them after a successful rehearsal.

## 3. Node.js and npm

**Unblocks:** Course 1 Lab 1 packaging; Course 3's optional TypeScript track.

Install `nodejs` and `npm`, then globally:

```
npm install -g @anthropic-ai/mcpb
```

A fallback already exists and the tester confirmed it works —
`course-1-.../starter-server/pack_mcpb.py` packages an extension without Node
(`Wrote starter.mcpb: 6 files, 6427 bytes`). So this is a convenience, not a
hard blocker. If Node is awkward on the image, tell us and we will make the
Python fallback the documented path instead.

## 4. Global git identity

**Unblocks:** every lab that commits — 16 labs reference git.

Commits currently fail with `Author identity unknown`. Either pre-set an
identity in the image, or we add the two `git config` lines to each course's
first lab. Pre-setting is less friction for students.

```bash
git config --global user.name  "RVC Student"
git config --global user.email "student@rvc.local"
```

The script sets those placeholders, overridable with `RVC_GIT_NAME` and
`RVC_GIT_EMAIL`.

## 5. Claude Desktop, signed in to the same account as the CLI

**Unblocks:** all three Course 1 labs.

Claude Desktop and the `claude` CLI are currently signed in to **different
accounts**, which blocks Course 1 entirely. Course 1 also requires Claude Code
**2.1.269 or later**; the image had 2.1.317, which is fine.

This one needs a person — it cannot be scripted. Note that Claude Code
auto-updates, so the installed version drifts between runs; the script records
it each time.

## 6. A Claude credential — no API key or student payment needed

**Unblocks:** all five Course 3 labs.

The original finding was "no `ANTHROPIC_API_KEY` on the VM". On investigation,
**Course 3 does not need one.** Its `require_api_key()` guard is course-authored,
not an SDK requirement, and the course makes no direct API calls — everything
goes through the Agent SDK, which wraps the Claude Code CLI and inherits its
credential precedence.

The classroom path is a subscription-backed token:

```bash
claude setup-token                      # browser flow once, prints a 1-year token
export CLAUDE_CODE_OAUTH_TOKEN=<token>
```

Per Anthropic's docs this "authenticates with your Claude subscription and
requires a Pro, Max, Ultra, Team, or Enterprise plan" and "can only make model
requests" — which is all the labs do. **No Console account, no API key, no
student spend.** It also works headless, which fixes browser login on the VM.

One caution: do **not** set `ANTHROPIC_API_KEY` image-wide. It overrides
subscription login for *every* course, so Courses 1, 2 and 4 would silently bill
against it.

A course-side change is still needed to relax the guard; that is ours, not yours.

---

## Not installable — needs a decision or a person

| Item | Needed for |
|---|---|
| Account tier for testing: Max, or a free account to observe free-tier limits | Deciding what students actually hit |
| A remote GitHub or GitLab project with admin access | Course 2 Lab 1 Tracks A and B |
| An instructor-provisioned sandbox Claude organization | Course 4 Labs 1–2 live paths (offline path works without) |
| Claude Console access | Course 3 Lab 4 Part 6 |
| Approval to run a full Gauntlet (~40 agent runs, 5 USD cap, never priced) | Course 1 Lab 2 |

---

## Summary for triage

| # | Item | Scriptable | Unblocks |
|---|---|---|---|
| 1 | Sandbox (AppArmor or sysctl) | With `--allow-sandbox-fix` | ~4 labs, and fixes a lab that teaches something false |
| 2 | `python-is-python3`, venvs | Yes | Nearly every lab |
| 3 | Node + `@anthropic-ai/mcpb` | Yes | Course 1 packaging (has a fallback) |
| 4 | Git identity | Yes | 16 labs |
| 5 | Desktop same-account | **No** | All of Course 1 |
| 6 | `claude setup-token` | Partly | All of Course 3 |

Items 2, 3 and 4 are routine and safe. Item 1 needs a security judgement.
Items 5 and 6 need a person with the right accounts.
