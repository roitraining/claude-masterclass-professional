# Lab 3 (take-home): Submit and Distribute

> Part of **[Claude Desktop Professional: Labs](README.md)**. `$FILES` is the `demo-files` folder your instructor gives you. Read the [guide preamble](README.md) for prerequisites, scenario notes and token-cost caps before you start.

---

**Learning objective:** Prepare your finished plugin and its Desktop extension for a distribution path and assemble a submission-ready release package. No timed session, and nothing is uploaded or published from this lab.

**Files:** your plugin from Labs 1 and 2, `$FILES/templates`, `$FILES/gauntlet/SECURITY-CHECKLIST.md`.

**Context:** There are three paths. Send people a folder or a zip. Run your own marketplace, which is a repository with a `.claude-plugin/marketplace.json`. Or submit to Anthropic's directory from the developer portal, which needs a paid claude.ai plan. An Owner sets each plugin to Not available, Available to install, Installed by default, or Required. You prepare and test all of it locally. The upload and the submission themselves are done by the instructor on the ROI sandbox account, or by you later on your own account.

**Steps:**

1. **Strict validation.** Fix every warning:

```
claude plugin validate --strict ~/work/<plugin name>
```

   Goal: a clean pass. Hint: warnings cover an unknown manifest field and a missing `version`.

2. **Metadata.** Add `description`, `author`, `homepage`, and `repository` to `plugin.json` (use your own placeholders, not real ones), and a `README.md` at the plugin root.
3. **Path A, a zip.** Make a zip of the plugin folder and load it for a session:

```
claude --plugin-dir ~/work/<plugin name>.zip
```

   Acceptance: the zip loads and the skill and the connector work. Check the folder against the upload limits (5,000 files and 200 MB).
4. **Path B, a local marketplace.** Make the plugin folder a marketplace by adding `.claude-plugin/marketplace.json` next to `plugin.json`, with an entry whose `name` is the same as the plugin and whose `source` is `"./"`:

```
{
  "name": "my-class-marketplace",
  "description": "A local marketplace for a class plugin.",
  "owner": { "name": "Your Name" },
  "plugins": [ { "name": "<plugin name>", "source": "./" } ]
}
```

   Then validate it and install from it on your own machine only. With a `marketplace.json` in the folder, `validate <folder>` checks the marketplace file, so point it at `plugin.json` to check the plugin itself:

```
claude plugin validate --strict ~/work/<plugin name>
claude plugin validate --strict ~/work/<plugin name>/.claude-plugin/plugin.json
claude plugin marketplace add ~/work/<plugin name>
claude plugin install <plugin name>@my-class-marketplace
```

   Acceptance: the plugin installs by name and loads in a new session. Afterward, remove the marketplace and the plugin so that your machine is clean.
5. **Release a new version.** Change one thing, bump the version in every place, add a changelog entry, run `claude plugin update <plugin name>@my-class-marketplace`, and confirm the new version loads. Then explain what would have happened if you had pushed the change without bumping `version`.
6. **Extension package.** Add the optional manifest fields for a polished extension (for example a display name, a long description, an icon, a repository, and a privacy policy link) using the MCPB manifest specification, repack the `.mcpb`, and reinstall it from Claude Desktop's Advanced settings. Acceptance: it installs and a tool call works.
7. **Security review.** Walk `SECURITY-CHECKLIST.md` on your own plugin and write `SECURITY-REVIEW.md` if you have any hooks. Describe what the connector can reach.
8. **Distribution memo.** In half a page, choose a path for your plugin and justify it: who needs it, how they get updates, what an Owner can require or block, and what changes if the plugin goes to the directory (which surfaces will load which components). Include a rollback plan.
9. **Release package.** Assemble a single folder: the plugin folder and zip, the `.mcpb`, `CHANGELOG.md`, `SETUP.md`, `RELEASE-NOTE.md` with your latest Gauntlet score, `SECURITY-REVIEW.md` if applicable, your memo, and the self-demo.

**Checkpoint:** `claude plugin validate --strict` passes, the zip and the local marketplace install both work, a new version reached your installed copy through `claude plugin update`, and the release package is complete.

**Common problems:**

- Strict validation fails on an unknown manifest field: remove the field or check the spelling in the manifest reference.
- `claude plugin update` says you are already at the latest version: you did not change `version`.
- The marketplace entry is not found: the entry `name` and the manifest `name` differ.
- The zip has the wrong layout: the folder with `.claude-plugin/plugin.json` must be at the top of the zip.
- Never change a published plugin's `name`. Users who installed it lose it.

**Scoring rubric (20 points):**

| Item | Points | Full marks when |
|---|---|---|
| Strict validation | 3 | Clean pass |
| Zip and local marketplace | 5 | Both install and load |
| Version release | 3 | Update reaches the installed copy; the missing-bump failure is explained |
| Extension package | 3 | Repacked and reinstalled, tool call works |
| Security review | 2 | Checklist complete, reach described |
| Distribution memo | 2 | Path justified, Owner controls and rollback covered |
| Release package | 2 | Everything listed in step 9 is present |

**Facilitator note:** The commands for strict validation, a local marketplace (`claude plugin marketplace add`, `claude plugin install name@marketplace`, `claude plugin update`), the marketplace file shape, the zip route, and the directory's requirements (a paid claude.ai plan and the developer portal) come from the Claude Code plugin publishing docs. The marketplace file validated in a scratch test here (it warns in strict mode if the `description` is missing). `marketplace add`, `install`, and `update` were not run end to end, so rehearse them. The portal applies directory rules that the command line does not check, so a clean local run does not guarantee acceptance, and the portal's steps were not walked for this guide. Students do not submit. If you want to demonstrate a submission or a team upload of the extension, do it on the ROI sandbox account after rehearsal, because the Owner upload and allowlist steps were not verified. The Lab 3 memo is a good place to check that students understand the support table: a `bin/` folder blocks installation in Cowork and chat, and a connector that needs `${user_config.*}` without a default is ignored in Cowork. A plugin installed through the directory reaches Claude Code through account sync, so a Gold-score plugin on the directory still needs a Cowork check by hand.
