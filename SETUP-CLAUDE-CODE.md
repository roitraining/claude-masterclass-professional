# Setup: Install and Sign In to Claude Code

**Applies to:** every MasterClass course that uses the `claude` command line
**Platforms:** Linux (the class default) and Windows
**Time:** about 10 minutes, once per machine

> **Read this before Lab 1 of any course listed below.** Courses can be taken in
> any order, days or weeks apart, so no course assumes you set this up in
> another one. If `claude --version` already prints a version and
> `claude auth status` shows you signed in, you are done — skip to
> [Check it works](#4-check-it-works).

---

## Which courses need this

| Course | Needs Claude Code | How you sign in |
|---|---|---|
| Associate 3 — Claude Code | Yes | Subscription login |
| Professional 1 — Desktop | Yes, **2.1.269 or later** | Subscription login, **same account as Claude Desktop** |
| Professional 2 — Claude Code | Yes | Subscription login, **paid account required** |
| Professional 3 — Agent SDK | Yes (via the SDK) | **`ANTHROPIC_API_KEY` only** — see [section 6](#6-api-key-path-professional-3-only) |
| Professional 4 — Enterprise Deployment | Yes, from Day 2 | Subscription login |
| Associate 1, 2, 4 · Essentials 1, 2 · Professional 5 | No | Not needed — those use claude.ai, Claude Desktop, or paper |

**Professional 3 is the exception.** It authenticates with an API key and not a
subscription login. If you take it in the same week as another course, read
[section 7](#7-switching-between-the-two) — the two methods interfere.

---

## 1. Before you start

**Account.** Claude Code requires a **Pro, Max, Ultra, Team, Enterprise, or
Console** account. **The free claude.ai plan does not include Claude Code
access.** Your instructor tells you which class account to use.

**Operating system.** Ubuntu 20.04+, Debian 10+, or Windows 10 1809+.
4 GB RAM or more.

**Git.** Optional for Claude Code itself, but several labs need it, and
`claude plugin eval` — used by the Professional 1 Gauntlet — requires
**Git 2.31 or later**. Check with:

```
git --version
```

Set your identity if you have not already, because labs commit locally:

```
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

**Python 3.11 or later** is required by Associate 3 and Professional 1, 2, 3
and 4. Check with `python3 --version` on Linux or `python --version` on
Windows.

---

## 2. Install on Linux (class default)

Open a terminal and run:

```
curl -fsSL https://claude.ai/install.sh | bash
```

The command prints nothing while it downloads.

When it finishes, **follow the PATH instruction the installer prints** — it
tells you exactly what to add for your shell. If you missed it, or `claude` is
not found afterwards, add the install directory to your `PATH` yourself:

```
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
```

The native installer puts the launcher at `~/.local/bin/claude`, which is why
that is the directory you add.

> Use `~/.zshrc` instead of `~/.bashrc` if your shell is zsh — check with
> `echo $SHELL`. Opening a brand-new terminal has the same effect as
> `source`, so either works.
>
> **Re-running setup?** The append adds the line every time. To avoid
> duplicate entries in `~/.bashrc`, guard it:
>
> ```
> grep -q '.local/bin' ~/.bashrc || echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
> source ~/.bashrc
> ```

> **Professional 1 needs 2.1.269 or later.** The plain command above installs
> the latest version, which satisfies this. To pin an exact version instead:
>
> ```
> curl -fsSL https://claude.ai/install.sh | bash -s 2.1.269
> ```

<details>
<summary>Alternative: Debian/Ubuntu package manager</summary>

Use this if your VM image is built with a package manager rather than a
per-user install. It needs `sudo`.

```
sudo apt install curl gnupg
sudo install -d -m 0755 /etc/apt/keyrings
sudo curl -fsSL https://downloads.claude.ai/keys/claude-code.asc \
  -o /etc/apt/keyrings/claude-code.asc
echo "deb [signed-by=/etc/apt/keyrings/claude-code.asc] https://downloads.claude.ai/claude-code/apt/stable stable main" \
  | sudo tee /etc/apt/sources.list.d/claude-code.list
sudo apt update
sudo apt install claude-code
```

Verify the key fingerprint before trusting it:

```
gpg --show-keys /etc/apt/keyrings/claude-code.asc
```

It must print `31DDDE24DDFAB679F42D7BD2BAA929FF1A7ECACE`.

Package-manager installs **do not auto-update**. Upgrade with
`sudo apt update && sudo apt upgrade claude-code`.

</details>

---

## 3. Install on Windows

Check which shell you are in. PowerShell shows `PS C:\>`; CMD shows `C:\>`
without the `PS`.

**PowerShell:**

```
irm https://claude.ai/install.ps1 | iex
```

**CMD:**

```
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

You do **not** need to run as Administrator. Open a new terminal window when it
finishes.

To pin a version in PowerShell:

```
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 2.1.269
```

> **Install Git for Windows.** Without it, Claude Code uses PowerShell for shell
> commands instead of Bash. Professional 2 says to run its shell commands in Git
> Bash, so install it: https://git-scm.com/downloads/win

**Common shell mix-up.** `The token '&&' is not a valid statement separator`
means you are in PowerShell but ran the CMD command.
`'irm' is not recognized` means you are in CMD but ran the PowerShell command.

---

## 4. Check it works

```
claude --version
```

A working install prints a version, such as `2.1.269 (Claude Code)`.

For a fuller check that validates your settings files without starting a
session:

```
claude doctor
```

If `claude` is not found, the install directory is not on your `PATH` yet.
Open a new terminal first; if it still fails, see
https://code.claude.com/docs/en/troubleshoot-install

---

## 5. Sign in (all courses except Professional 3)

Run:

```
claude auth login
```

This opens your browser. Sign in with the class account your instructor gave
you, then return to the terminal.

Confirm it took:

```
claude auth status
```

> **Professional 1 only.** Claude Code and Claude Desktop must be signed in to
> **the same account**. If Desktop is already signed in, use that same account
> here.

To sign out — for example before handing the VM back:

```
claude auth logout
```

---

## 6. API key path (Professional 3 only)

The Agent SDK course authenticates with an API key, **not** a subscription
login. Its guide states: *"Use API-key authentication only."*

Set the key in the shell you run the agent from. Your instructor provides the
class key.

**Linux:**

```
export ANTHROPIC_API_KEY=sk-ant-...
```

**Windows PowerShell:**

```
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

**Never** put the key in a file, a prompt, or a commit. Verify the shell has it
without printing it:

```
python preflight.py
```

It prints `Ready.` and never echoes the key.

---

## 7. Switching between the two

**This is the part that bites when you take two courses in one week.**

If `ANTHROPIC_API_KEY` is set in your environment and you approve it when
Claude Code asks, **Claude Code skips the login prompt and uses the key
instead of your subscription.** That is documented behaviour, not a bug.

What it means in practice:

- If you set the key for **Professional 3** and leave it exported in your shell
  profile (`~/.bashrc`, `~/.zshrc`, or a Windows user environment variable),
  then **Professional 1, 2 and 4 may silently run on API-key billing** rather
  than the class subscription. Your labs still work, but the spend lands in the
  wrong place and can exhaust the class key.
- Conversely, if you are signed in with a subscription and need the API-key
  path for Professional 3, the key must be set in that shell.

**Recommended practice:** set the key **per shell session only** — type the
`export` line in the terminal where you run the Agent SDK labs, and do not add
it to your shell profile. Then close that terminal when the course ends.

To check which method is in use:

```
claude auth status
echo $ANTHROPIC_API_KEY        # Linux; prints empty if unset
```

On Windows PowerShell, use `$env:ANTHROPIC_API_KEY` for the second check.

---

## 8. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `claude: command not found` | `~/.local/bin` not on `PATH` | Open a new terminal. If it persists: `echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc` |
| Login opens no browser | Headless or remote session | Run `claude setup-token` instead to create a long-lived token (needs a subscription) |
| Signed in but billed to the wrong place | `ANTHROPIC_API_KEY` is set | See [section 7](#7-switching-between-the-two) |
| `claude plugin eval` fails | Git older than 2.31 | Upgrade Git |
| Free account rejected | Free plan excludes Claude Code | Use the paid class account |
| Version below a course minimum | Old install | Run `claude update`, or reinstall pinning the version |

Full installation and login troubleshooting:
https://code.claude.com/docs/en/troubleshoot-install

---

## Verified against

Commands taken from the official setup documentation
(https://code.claude.com/docs/en/setup) and confirmed against the installed CLI
(`claude auth --help`, `claude install --help`, `claude setup-token --help`).

**Not yet confirmed on the ROI Virtual Classroom image** — rehearse before
delivery:

- Whether the class VM has Claude Code pre-installed, and at what version
- Whether students have `sudo`, which the package-manager path needs
- Whether the browser login flow completes inside the VM, or whether
  `claude setup-token` is required
- Which account tier the class accounts actually carry
