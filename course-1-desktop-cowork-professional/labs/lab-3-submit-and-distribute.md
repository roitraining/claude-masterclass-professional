# Lab 3 (take-home): Submit and Distribute

**Course:** Claude Desktop Professional
**Duration:** Untimed — work at your own pace
**Format:** Take-home lab. Nothing is uploaded or published from this lab

> Part of **[Claude Desktop Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

## Prerequisites

- [ ] Labs 1 and 2 completed — you need your finished plugin and its latest Gauntlet score
- [ ] `claude` signed in to a paid Anthropic account
- [ ] Claude Desktop installed **and signed in to the same account as Claude Code**, for the extension reinstall in Part 5. This is the one place in the course where the accounts must match: a plugin is saved to an account, so a mismatch means the one you packed will not appear. Parts 1 to 4 and 6 to 9 do not need Desktop
- [ ] `$FILES/templates` and `$FILES/gauntlet/SECURITY-CHECKLIST.md` from your instructor
- [ ] No directory submission required. You prepare and test everything locally

---

## Overview

There are three distribution paths:

- **Send people a folder or a zip.**
- **Run your own marketplace**, which is a repository with a `.claude-plugin/marketplace.json`.
- **Submit to the Anthropic directory** from the developer portal, which needs a paid claude.ai plan.

An Owner sets each plugin to Not available, Available to install, Installed by default, or Required.

You prepare and test all of it locally. The upload and the submission themselves are done by the instructor on the ROI sandbox account, or by you later on your own account.

---

## Part 1: Validate and Describe the Plugin

### Step 1: Pass Strict Validation

Fix every warning.

```
claude plugin validate --strict ~/work/<plugin name>
```

**Acceptance criteria:** a clean pass.

> **Hint:** warnings cover an unknown manifest field and a missing `version`.

### Step 2: Add the Distribution Metadata

Add `description`, `author`, `homepage`, and `repository` to `plugin.json` — use your own placeholders, not real ones — and add a `README.md` at the plugin root.

**Expected result:** a plugin that describes itself to someone who did not build it.

---

## Part 2: Path A, Distribute a Zip

### Step 3: Zip the Plugin and Load It

```
claude --plugin-dir ~/work/<plugin name>.zip
```

**Acceptance criteria:** the zip loads and the skill and the connector work. Check the folder against the upload limits of 5,000 files and 200 MB.

> **Common Pitfall:** the folder holding `.claude-plugin/plugin.json` must be at the top of the zip. A nested layout will not load.

---

## Part 3: Path B, Run a Local Marketplace

### Step 4: Add the Marketplace File

Make the plugin folder a marketplace by adding `.claude-plugin/marketplace.json` next to `plugin.json`, with an entry whose `name` is the same as the plugin and whose `source` is `"./"`:

```
{
  "name": "my-class-marketplace",
  "description": "A local marketplace for a class plugin.",
  "owner": { "name": "Your Name" },
  "plugins": [ { "name": "<plugin name>", "source": "./" } ]
}
```

**Expected result:** a marketplace file whose entry name matches the plugin name exactly.

### Step 5: Validate and Install from It

With a `marketplace.json` in the folder, `validate <folder>` checks the marketplace file, so point it at `plugin.json` to check the plugin itself:

```
claude plugin validate --strict ~/work/<plugin name>
claude plugin validate --strict ~/work/<plugin name>/.claude-plugin/plugin.json
claude plugin marketplace add ~/work/<plugin name>
claude plugin install <plugin name>@my-class-marketplace
```

**Acceptance criteria:** the plugin installs by name and loads in a new session.

> **Note:** install on your own machine only. Afterwards, remove the marketplace and the plugin so your machine is left clean.

---

## Part 4: Release a New Version

### Step 6: Ship an Update and Explain the Failure Mode

Change one thing, bump the version in every place, add a changelog entry, then:

```
claude plugin update <plugin name>@my-class-marketplace
```

**Acceptance criteria:** the new version loads, and you can explain in writing what would have happened if you had pushed the change without bumping `version`.

> **Common Pitfall:** never change the `name` of a published plugin. Users who installed it lose it.

---

## Part 5: Package the Desktop Extension

### Step 7: Polish the Manifest and Reinstall

Add the optional manifest fields for a polished extension — for example a display name, a long description, an icon, a repository, and a privacy policy link — using the MCPB manifest specification. Repack the `.mcpb` and reinstall it from the Advanced settings of Claude Desktop.

**Acceptance criteria:** it installs and a tool call works.

---

## Part 6: Review the Security Surface

### Step 8: Walk the Checklist and Describe the Reach

Walk `SECURITY-CHECKLIST.md` on your own plugin. Write `SECURITY-REVIEW.md` if you have any hooks.

**Acceptance criteria:** the checklist is complete, and you have described what the connector can reach.

---

## Part 7: Choose a Distribution Path

### Step 9: Write the Distribution Memo

In half a page, choose a path for your plugin and justify it: who needs it, how they get updates, what an Owner can require or block, and what changes if the plugin goes to the directory, including which surfaces load which components. Include a rollback plan.

**Acceptance criteria:** a path chosen and justified, Owner controls covered, and a rollback plan stated.

> **Hint:** check your memo against the support table. A `bin/` folder blocks installation in Cowork and chat, and a connector that needs `${user_config.*}` without a default is ignored in Cowork.

---

## Part 8: Assemble the Release Package

### Step 10: Collect Everything into One Folder

Assemble a single folder containing: the plugin folder and zip, the `.mcpb`, `CHANGELOG.md`, `SETUP.md`, `RELEASE-NOTE.md` with your latest Gauntlet score, `SECURITY-REVIEW.md` if applicable, your memo, and the self-demo.

**Acceptance criteria:** every item above is present.

---

## Part 9: Checkpoint

### Step 11: Verify Your Progress

- [ ] `claude plugin validate --strict` passes clean
- [ ] `plugin.json` carries `description`, `author`, `homepage` and `repository`, and a `README.md` sits at the plugin root
- [ ] The zip loads with `--plugin-dir`, and the skill and connector both work
- [ ] The folder is within the 5,000 file and 200 MB upload limits
- [ ] `.claude-plugin/marketplace.json` exists with an entry name matching the plugin name
- [ ] The plugin installs by name from your local marketplace and loads in a new session
- [ ] A bumped version reached your installed copy through `claude plugin update`
- [ ] You can explain what happens when a change ships without a version bump
- [ ] The `.mcpb` is repacked with the polished manifest fields and reinstalls, with a working tool call
- [ ] `SECURITY-CHECKLIST.md` walked, and the connector reach described
- [ ] A half-page distribution memo with a justified path, Owner controls and a rollback plan
- [ ] The release package folder contains every item from Step 10
- [ ] Your machine is left clean: the test marketplace and plugin removed

---

## Troubleshooting Reference

| Issue | Symptom | Solution |
|---|---|---|
| Unknown manifest field | Strict validation fails | Remove the field or check its spelling in the manifest reference |
| Update does nothing | `claude plugin update` reports you are already at the latest version | You did not change `version`. Bump it in every place that carries it |
| Marketplace entry not found | Install fails by name | The entry `name` and the manifest `name` differ. They must match |
| Zip will not load | Plugin not detected in the zip | The folder with `.claude-plugin/plugin.json` must be at the top of the zip |
| Users lose the plugin | An installed plugin disappears after an update | The `name` was changed. Never rename a published plugin |

---

## Scoring Rubric (20 points)

| Item | Points | Full marks when |
|---|---|---|
| Strict validation | 3 | Clean pass |
| Zip and local marketplace | 5 | Both install and load |
| Version release | 3 | Update reaches the installed copy; the missing-bump failure is explained |
| Extension package | 3 | Repacked and reinstalled, tool call works |
| Security review | 2 | Checklist complete, reach described |
| Distribution memo | 2 | Path justified, Owner controls and rollback covered |
| Release package | 2 | Everything listed in Step 10 is present |

---

## What You Built

Working at your own pace, you:

- Took a plugin from passing validation to passing strict validation, with the metadata someone else needs to understand it
- Proved two distribution paths end to end on your own machine: a zip and a local marketplace
- Shipped a version bump that reached an installed copy, and can explain why skipping the bump silently does nothing
- Reviewed your own security surface and described what the connector can actually reach
- Chose a distribution path with reasons, Owner controls and a rollback plan, rather than by default

---

## What's Next

This is the final lab in Claude Desktop Professional. Keep the distribution memo: the question it asks, who needs this and how do they get updates, is the one that decides whether a plugin survives contact with a team.

---

## Facilitator Notes

The commands for strict validation, a local marketplace (`claude plugin marketplace add`, `claude plugin install name@marketplace`, `claude plugin update`), the marketplace file shape, the zip route, and the directory requirements (a paid claude.ai plan and the developer portal) come from the Claude Code plugin publishing docs. The marketplace file validated in a scratch test here, and it warns in strict mode if the `description` is missing. `marketplace add`, `install`, and `update` were not run end to end, so rehearse them.

The portal applies directory rules that the command line does not check, so a clean local run does not guarantee acceptance, and the steps of the portal were not walked for this guide. Students do not submit. If you want to demonstrate a submission or a team upload of the extension, do it on the ROI sandbox account after rehearsal, because the Owner upload and allowlist steps were not verified.

The Lab 3 memo is a good place to check that students understand the support table: a `bin/` folder blocks installation in Cowork and chat, and a connector that needs `${user_config.*}` without a default is ignored in Cowork. A plugin installed through the directory reaches Claude Code through account sync, so a plugin with a Gold score on the directory still needs a Cowork check by hand.

---

*Lab 3 Complete*
