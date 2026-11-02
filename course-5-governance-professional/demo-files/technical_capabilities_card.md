# Technical Capabilities Card

These controls were covered in Professional 4. For this course they are capabilities that exist at Brightwater, which is on Claude Enterprise. You cite them as controls and as sources of evidence. You are not asked to configure or operate any of them.

| Capability | What it does | Evidence it can supply | Limits to remember |
|---|---|---|---|
| Identity and roles | Single sign-on and the company identity provider create and remove users. Roles are Owner, Admin, User, and on Enterprise a Custom role. Groups decide who gets which permissions. | A dated export of users, roles and groups (the directory data) | Removing a person only in Claude can be undone at the next sign-in if they remain assigned in the identity provider. Group-based custom roles depend on directory sync being set up. |
| Compliance API activity data | The Enterprise API gives an Activity Feed of events, a directory of users, roles and groups, and, for claude.ai organizations, chats, files and projects. Listed coverage includes Cowork, Claude Code, Claude for Microsoft 365 and Claude in Chrome sessions. | An activity extract for a date range; a directory snapshot | Content endpoints serve claude.ai data only. The admin-settings audit-log export is narrower: a capped lookback, CSV, no content. |
| Tenant Restrictions | A network proxy adds a header that lists the organizations allowed from the company network. Covers web, desktop, API key and OAuth token sign-in. Needs TLS inspection. | The proxy rule and its change history | Applies to traffic that goes through the company proxy. Confirm with Professional 4 material what it means for a personal phone off the company network. |
| Managed settings and sandbox (Claude Code) | Settings an organization enforces for Claude Code and Desktop, including sandbox rules for what code can read, write and reach on the network. | The managed settings file and its change history | Applies to the surfaces and machines the settings reach. |
| Spend limits | Enterprise limits cascade organization, group, individual. A Spend Limits API (Enterprise only) sets limits per member, shows where a limit comes from, and reviews requests for higher limits. | Limit settings by level; the log of increase requests and decisions | Pooled group budgets and alert thresholds are not confirmed. Do not rely on them. |

## Not technical, still controls

Training, signed attestations, intake forms, an exception register, Governance Board minutes, internal audit, and management review. These need people and records, not software.

## Instructor note

Everything in the table traces to the Professional 4 verified facts. The Tenant Restrictions limit for personal phones, the custom data retention minimum, CMEK behavior, sensitivity-label policies for Microsoft 365 add-ins, and pooled group budgets are UNVERIFIED or not covered. Do not state them as fact.
