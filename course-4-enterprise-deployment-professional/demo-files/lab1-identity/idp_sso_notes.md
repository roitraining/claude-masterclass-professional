# Northwind Example Corp: IdP and SSO Notes (exported design notes)

All names, domains, and counts are fictional. Attribute names below belong to the fictional IdP in these notes. They are not Claude-documented names.

## Organization

- Claude plan: Enterprise
- Identity provider: ExampleIdP (fictional)
- Provisioning mode: JIT only. SCIM directory sync is NOT enabled.
- Email domains in use: `example.com` and `northwind-labs.example.net` (acquired company)
- SSO enforcement: enabled for all users of both domains on the cutover weekend

## Attribute mapping (IdP side)

| Claude need | IdP attribute | Notes |
|-------------|---------------|-------|
| Unique identifier and email | `NameID` (email format) | Lower-case |
| First name | `givenName` | |
| Last name | `familyName` | |
| Group membership | `groups` | Sent as a multi-value attribute |

## Role policy (from the security team)

- Owner: named individuals only, at most 5 members, break-glass use.
- Admin: the platform team.
- User: everyone else who is assigned to the Anthropic app in the IdP.
- Custom role `SecOps Read-Only Auditor`: security analysts who review audit activity. It must be read-only. It must not change members, billing, or organization settings.
- Seat tier is decided by group mapping (see `group_mappings.csv`).

## Group design

The IdP sends group names at login. The mappings are in `group_mappings.csv`. Groups that exist inside the Claude organization are in `claude_groups.csv`.

## Offboarding (current practice)

See `offboarding_steps.csv`. The platform team removes departing people from the Claude Members list.

## Rollout

See `rollout_plan.csv` and `domains.csv`.
