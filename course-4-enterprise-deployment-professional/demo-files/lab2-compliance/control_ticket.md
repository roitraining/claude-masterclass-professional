# Change Ticket CHG-4471: Deployment Control for Northwind Example Corp

All identifiers are fictional. Choose ONE track and submit the matching JSON template.

## Track A: Tenant Restrictions proxy rule

Requirement from Security: employees on the corporate network may reach Claude only for approved Claude organizations. Use the proxy's request-header rewrite to enforce it.

Approved organizations as written by the requester (this list was pasted from a chat message):

```
Northwind production     00000000-0000-4000-8000-0000000000a1
Northwind research       00000000-0000-4000-8000-0000000000a2,
Partner Sandbox  (RETIRED 2026-08-30, do not allow)   00000000-0000-4000-8000-0000000000f9
Northwind subsidiary     00000000-0000-4000-8000-0000000000a3
```

Proxy facts from the network team:

- The proxy can add a request header to matching hosts.
- TLS inspection is currently OFF on the proxy for anthropic.com traffic.
- Traffic to be covered: the Claude web app, the API, and Claude Desktop sessions, whether the user signs in with an account, an API key, or an OAuth token.

Fill in `control_proxy_spec.json`.

## Track B: Claude Desktop managed policy

Requirement from IT: every managed laptop must receive a Desktop policy that controls auto-update, desktop extensions, and local development MCP servers. The fleet is 60 percent macOS (managed with Jamf Pro) and 40 percent Windows (managed with Intune). Users are local administrators on the Windows machines and can write to their own per-user registry hive.

Fill in `control_desktop_policy.json`. Real key names are NOT supplied in this exercise and are not in the course facts. Use placeholders that start with `UNVERIFIED:` followed by a short description. Do not invent key names.
