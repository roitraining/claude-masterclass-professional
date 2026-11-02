# Demo 4: a routine and an Actions workflow on the same GitHub trigger

Use the trigger "a pull request is opened". Fill the right-hand column live from what you see on screen. The left columns come from the course facts.

| Question | Actions workflow (`claude-code-action@v1`) | Routine (research preview) |
|---|---|---|
| Where does it run | A GitHub-hosted runner in your repository | Anthropic infrastructure, in a cloud session |
| What defines it | A workflow file you commit and review | A routine you configure, with no workflow file |
| Triggers | Any GitHub event, including a cron schedule | Cloud schedule (one hour minimum), API, or GitHub event |
| Who is allowed to start it | The actor needs write access. Bots are rejected unless listed in `allowed_bots` | Belongs to one account. Check what GitHub events it accepts on screen |
| Permissions and tool grants | Your `permissions:` block and `--allowedTools` | No permission-mode picker. Check on screen what it can do |
| Secrets | A repository or organization secret, or workload identity federation | None in your repository. It runs as the account that owns it |
| Cost | Runner minutes plus API tokens, or subscription usage for a subscription token | Check on screen and in the account |
| Review trail | The workflow file, the run log, the permissions block in version control | Check on screen |
| Fails if | A secret is missing, a fork pull request has no secrets, a bot loop is blocked | The owner leaves, or the account loses access |
| Choose it when | Several people must own and review the automation, or CI must run on its output | One person wants a quick personal automation with no file to maintain |

Rules of thumb to end on:

- Anything a team depends on goes where the team can review it: a file in the repository.
- A routine is one person's automation. Say who owns it, and what happens when they leave.
- Neither removes the need for a human checkpoint before something ships (Demo 5).
