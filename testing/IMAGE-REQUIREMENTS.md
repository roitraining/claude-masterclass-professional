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

**Capture the output.** Section 10 of the `--check` run after installing prints
the exact versions of everything it installed, including OS, kernel, Claude Code
and the contents of each venv. That block is what goes into the change request:
it gives the team package names *and* versions rather than names alone.

```bash
./provision-rvc.sh --check   2>&1 | tee before.txt
./provision-rvc.sh --install 2>&1 | tee install.txt
./provision-rvc.sh --check   2>&1 | tee after.txt
```

The point of running it on a live VM first is to prove the installs work before
anyone changes the image. Three things will still show FAIL afterwards and that
is expected, not a script failure: the sandbox (item 1, which has no scripted
fix), a class API key (item 6) and the Claude Desktop account match (item 5).

---

## 1. Sandbox — AppArmor, and only AppArmor

**Unblocks:** Course 4 Lab 3 (its core exercise), Course 2 Lab 3 evals,
Course 4 Lab 4 defences, probably the Course 1 Gauntlet.

Every sandboxed Bash call from Claude Code fails with:

```
apply-seccomp: write /proc/self/setgroups
(nested userns is capability-restricted; caller must provide CAP_SYS_ADMIN):
Permission denied
```

### The sysctl is NOT the fix — tested and disproven 2026-11-04

An earlier version of this document offered relaxing
`kernel.apparmor_restrict_unprivileged_userns` as a simple option. **It does not
work.** The tester set it to 0 and the error did not change.

The `bwrap-userns-restrict` AppArmor profile stays loaded and enforcing, and the
sysctl does not turn it off. It moves everything `bwrap` launches into the
`unpriv_bwrap` profile, which carries `audit deny capability`. The kernel kept
denying *after* the sysctl was relaxed:

```
apparmor="DENIED" operation="capable" class="cap" profile="unpriv_bwrap"
  comm="3" capability=21 capname="sys_admin"
```

Two consequences:

- **`provision-rvc.sh --allow-sandbox-fix` has been retired.** It still parses,
  but prints a notice and does nothing. Leaving it in would relax a security
  setting for no benefit.
- **If an earlier run already applied it, revert it:**
  ```bash
  sudo rm /etc/sysctl.d/99-claude-sandbox.conf
  sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=1   # or reboot
  ```
  The script now detects that file and flags it.

### What is actually needed

An **AppArmor change** so the Claude Code sandbox can create a nested user
namespace — either a profile that grants `userns create` to the Claude Code
binary, or an adjustment to how `unpriv_bwrap` applies to it.

**We have not written or tested such a profile**, and this needs someone who
knows AppArmor on Ubuntu 26.04. What we can supply is the exact denial above,
which names the profile (`unpriv_bwrap`), the operation (`capable`) and the
capability (`21`, `sys_admin`).

`provision-rvc.sh` no longer offers a fix here — it only diagnoses and probes.

### `sandbox-apparmor.sh` — find which change actually works

There is now a harness for this, because the thing that went wrong last time was
treating an *applied* change as a *working* one:

```bash
./sandbox-apparmor.sh --diagnose              # read-only: what is loaded, where the binary is, baseline probe
./sandbox-apparmor.sh --try local-override    # least invasive, try first
./sandbox-apparmor.sh --try claude-profile
./sandbox-apparmor.sh --try disable-profile   # last resort, image-wide
./sandbox-apparmor.sh --revert                # undo anything that did not work
```

Each `--try` probes **before** and **after** with the sandbox forced on, and
says plainly whether the sandbox now starts. On success it prints the exact
change for the team to bake into the image.

| Option | What it does | Trade-off |
|---|---|---|
| ~~`local-override`~~ | ~~Appends `capability sys_admin,`~~ | **TRIED 2026-11-04 AND FAILED.** `unpriv_bwrap` carries `audit deny capability`, and an AppArmor deny beats any allow, so this can never work. Reverted |
| `claude-profile` | Installs a profile naming the real Claude Code binary with `userns,` | Scoped to Claude Code. **Caveat: Claude Code auto-updates, so the binary path moves and the profile needs re-pointing** |
| `disable-profile` | Disables `bwrap-userns-restrict` entirely | Works for everything on the image, Claude Code included. Removes the restriction broadly, so only use it if the narrower options fail |

**`local-override` was tried on 2026-11-04 and failed** for the reason above. `claude-profile` is expected to fail the same way, since the deny is on the profile bwrap transitions into rather than on the calling binary. That leaves `disable-profile`, which is image-wide and needs a decision. Neither remaining option has been tested. They are the documented ways to grant
unprivileged user-namespace creation under AppArmor, ordered least invasive
first. The script exists to find out which one works on this image, with
evidence. Everything it changes is backed up and undone by `--revert`, which
also removes the leftover ineffective sysctl from the earlier run.

### Why this is the top priority

With the sandbox down, **Course 4 Lab 3 tells students an attack was blocked
when it was not.** The tester confirmed the secrets file was read
(`read 83 bytes from config/secrets.env`) despite the deny rules. The lab's
checker has since been corrected to say "blocked if the OS sandbox starts", so
it no longer lies — but the exercise still cannot be run as designed.

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

**Unblocks:** the optional extension install in Course 1 Lab 1 Part 8, and
Lab 3 Part 5. **It does not block the rest of Course 1** — that was an
over-block in the first report, since Lab 1 Parts 1 to 7 and all of Lab 2 are
command line only.

Claude Desktop and the `claude` CLI are currently signed in to **different
accounts**, which blocks Course 1 entirely. Course 1 also requires Claude Code
**2.1.269 or later**; the image had 2.1.317, which is fine.

This one needs a person — it cannot be scripted. Note that Claude Code
auto-updates, so the installed version drifts between runs; the script records
it each time.

## 6. Class API keys with spend limits (Course 3)

**Unblocks:** all five Course 3 labs.

Course 3 needs an **Anthropic API key**, and this is deliberate taught content,
not an oversight. Deck slide 11 is titled *"Install, Authenticate, Run"* and says
*"Set `ANTHROPIC_API_KEY` as an environment variable"*; Module 2 spends 45
minutes on it. The outline lists *"an Anthropic API key or Console access"* as a
student requirement.

**A subscription login is not a substitute.** Anthropic's Agent SDK overview
states:

> Unless previously approved, Anthropic does not allow third party developers to
> offer claude.ai login or rate limits for their products, including agents built
> on the Claude Agent SDK. Use the API key authentication methods described in
> the Quickstart instead.

The deck already carries this as a verified source check, dated 19 October 2026.
So the key is a policy requirement, not just a technical one.

**Students should not be paying for this.** Deck slide 6 states the intended
model: *"Each student gets a class API key with a spend limit."* The ask is
therefore:

- **Class API keys**, one per student, each with a spend limit set in the Console
- **An agreed handout channel.** Slide 6's instructor note says to *"hand out the
  class keys through the agreed channel"* — as far as we can tell no channel has
  been agreed yet, and that is the actual gap
- **Console access** for Module 13 and Course 3 Lab 4 Part 6, which teach the
  Console Evaluate tool. This is separate from the key and is also taught content

The labs already cap spend themselves — 12 turns and 0.50 USD per run by
default, overridable by the instructor through `LAB_MAX_TURNS` and
`LAB_BUDGET_USD` — so a per-key Console spend limit is a second belt rather than
the only control.

**One thing to get right:** set the key **per shell**, not in `~/.bashrc` or a
system-wide profile. `ANTHROPIC_API_KEY` outranks subscription login in Claude
Code's credential precedence, so a globally exported key makes Courses 1, 2 and
4 bill against it silently. `SETUP-CLAUDE-CODE.md` section 7 covers this.

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
| 1 | Sandbox — **AppArmor only**, sysctl disproven | **No** | ~4 labs. Needs an AppArmor specialist |
| 2 | `python-is-python3`, venvs | Yes | Nearly every lab |
| 3 | Node + `@anthropic-ai/mcpb` | Yes | Course 1 packaging (has a fallback) |
| 4 | Git identity | Yes | 16 labs |
| 5 | Desktop same-account | **No** | All of Course 1 |
| 6 | Class API keys + Console access | **No** | All of Course 3 |

Items 2, 3 and 4 are routine and safe. Item 1 cannot be scripted at all and
needs an AppArmor specialist.
Items 5 and 6 need a person with the right accounts — item 6 needs Console
administration to mint keys and set spend limits.
