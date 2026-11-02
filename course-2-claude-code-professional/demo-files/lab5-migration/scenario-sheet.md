# Lab 5 scenario sheet: Larkspur Freight Software

Fictional company. Every name, count and date is invented for this exercise.

You are the engineering operations lead. Larkspur has used Claude Code through a Claude Console organization for a year. The company has bought Claude Enterprise. You own the cutover plan for the engineering group. Write the runbook in `runbook-template.md`.

## The team

| Item | Detail |
|---|---|
| People moving | 62 engineers and 8 data analysts, in three groups: platform (24), shipping apps (38), data (8) |
| Contractors | 6 contractors on shipping apps. They are not in the company identity provider. Their contracts end in 11 weeks |
| Leaving soon | Priya Raman (platform) leaves in 4 weeks. She owns one of the credentials below |
| Laptops | 55 company laptops under device management. The contractors and 9 employees use unmanaged personal laptops |

## Identity

- The company identity provider is a SAML provider, "LarkID". Groups: `eng-platform`, `eng-apps`, `eng-data`. Group membership is correct for employees and is reviewed monthly.
- Enterprise seats will be assigned from identity provider groups (SCIM group mappings). Everyone in `eng-data` needs standard seats. Platform and apps need standard seats, and platform leads need a different role (see Roles).
- Today the Console organization has 41 members invited by email address, a mix of company and personal addresses.

## Roles

- Platform leads (4 people) administer Claude Code for the company. They must be able to manage settings and members, and must not be able to see data analysts' usage detail.
- Everyone else uses Claude Code and needs no admin function.
- Design the roles by what each can and cannot do. Do not invent product role names. Where you need a product detail you cannot source, write "to confirm" beside it.

## Managed settings needs

1. Engineers must sign in to the company Enterprise organization only. Personal accounts must not work for Claude Code on company laptops.
2. Only the company plugin marketplace may be added. Other marketplaces are blocked.
3. Hooks may run only if the company's managed settings define them.
4. Contractors on personal laptops must be covered by the same rules as far as the product allows. Say what you can and cannot enforce for them.

Delivery choice: decide between server-managed and endpoint-managed policy for each group of laptops and justify it in two sentences. Detailed policy design and precedence belong to a later course, so stay at the level of "which mechanism, and which of the four needs it covers".

## Credentials in use today

| Id | Credential | Where it lives | Used by |
|---|---|---|---|
| C1 | 29 personal Console API keys | `ANTHROPIC_API_KEY` in shell profiles on laptops | Engineers' daily Claude Code use |
| C2 | One shared Console API key | A secrets vault. Six repositories' `.claude/settings.json` use an `apiKeyHelper` script that reads it | Engineers on those six repositories |
| C3 | One Console API key | A GitHub organization secret named `ANTHROPIC_API_KEY` | `claude-code-action` workflows in 14 repositories |
| C4 | One masked CI/CD variable `ANTHROPIC_API_KEY` | One GitLab project (the legacy billing service) | A review job on merge requests |
| C5 | Three long-lived tokens created with `claude setup-token` | Three GitHub repository secrets named `CLAUDE_CODE_OAUTH_TOKEN` | Workflows in three platform repositories. Two were made by Priya Raman and one by a contractor |

## CI

- 14 GitHub repositories run Claude in GitHub Actions. 11 use C3. Three use C5.
- One GitLab project runs a review job using C4.
- Nightly pipelines must not miss a run. Cutover is Saturday 06:00 to 12:00, when no deployments are scheduled.

## Reporting

- Finance needs the last 12 months of Console usage and cost by key and by workspace to close the year. Console analytics and API keys do not carry over to Enterprise.

## Out of scope

- Spend limits and caps. Another course covers them. Write "out of scope" and move on.
- Organization-wide policy decisions behind the migration, and analytics interpretation.
- CLI session history. It is stored locally on each laptop, and nothing needs migrating.

## Your deliverable

A runbook that a teammate who was not in the planning meetings could run on Saturday. Use `runbook-template.md`. A page and a half to three pages is enough. Be exact about order, because several steps break something if done early.
