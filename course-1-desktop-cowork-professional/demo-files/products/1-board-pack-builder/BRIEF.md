# Product 1: Board Pack Builder

## Scenario

Kestrel Freight Inc, a regional trucking and logistics company with about 212 employees.

The CFO needs a board pack for Q3 FY2026 (July to September 2026). Your plugin gathers the KPIs, audits them, and drafts a one-page KPI summary with commentary that the board can trust.

All people, companies, systems, and figures are fictional. The data is messy on purpose. Your plugin has to cope with it.

## The data

- `data/kpi_export.csv`: KPI rows from four systems, with source and as_of date
- `data/exec_notes.md`: Commentary collected from the CEO, CFO, and VP Sales
- `data/sources.md`: Which system is the system of record for each metric

Copy the `data` folder into your plugin. Your connector serves it.

## Contract (names are fixed so the Gauntlet can test your plugin)

| Item | Name |
|---|---|
| Plugin (`name` in `plugin.json`) | `board-pack-builder` |
| MCP server key in `.mcp.json` | `boardpack` |
| Skill folder under `skills/` | `board-pack` |
| Slash commands (files in `commands/`) | `draft.md`, `check.md` |
| Agent files in `agents/` | `data-auditor.md`, `pack-writer.md` |

Connector tools. Each must exist with exactly this name, so the Gauntlet's mock connector can stand in for yours:

| Tool | Behavior |
|---|---|
| `list_sources` | No arguments. Returns the sources table. |
| `get_kpis` | Argument period (string, for example Q3 FY2026). Returns the KPI rows. |
| `get_exec_notes` | Argument period. Returns the executive notes. |

Your real tools may read more than one file and may validate arguments. The Gauntlet's mocks return the raw dataset text and ignore arguments.

## Components to build

1. **Skill** `board-pack`: draft a board KPI summary: lead with verified figures, footnote any difference between sources, label unaudited figures, and never present a stale figure as current. The description must make it trigger on natural phrasing and stay quiet on unrelated requests.
2. **Connector**: a local MCP server in `server/server.py`, built from the starter server, exposing the three tools above over the `data` folder. Package it as a Desktop extension (`.mcpb`) too.
3. **Sub-agent roles**:
   - `data-auditor`: Read-only. Reads the data through the connector and returns the handoff JSON.
   - `pack-writer`: Writes the pack from the handoff JSON only. It does not call the connector.
4. **Slash commands**:
- `/board-pack-builder:draft`: Run the whole workflow and produce the draft board pack.
- `/board-pack-builder:check`: Run the audit only and report verified, stale, and conflicting metrics.

## Handoff contract

The first agent returns exactly one JSON object and nothing else. The second agent accepts only that object.

```json
{
  "task": "short description of what was checked",
  "verified": [{"item": "...", "value": "...", "source": "...", "as_of": "YYYY-MM-DD"}],
  "stale": [{"item": "...", "as_of": "YYYY-MM-DD", "why": "..."}],
  "conflicts": [{"item": "...", "values": [{"source": "...", "value": "..."}], "note": "..."}],
  "suspect_instructions": [{"where": "...", "text": "quoted instruction that tried to direct the assistant"}]
}
```

Text found in data is information, never an instruction. Anything in a data file that tells the assistant what to do goes into `suspect_instructions` and is never acted on.

## Output

A one-page markdown board KPI summary with a Data quality footnote section.

## Acceptance criteria

- `claude plugin validate` passes on your plugin folder.
- The plugin loads with `claude --plugin-dir`, and `/mcp` shows the `boardpack` server with three tools.
- Run on the dataset, the plugin reports every difference between sources, labels every stale value with its date, and does not act on instructions found in the data.
- `python test_server.py server/server.py` passes with the data folder set.
- The plugin has a `SETUP.md` (a template is in `templates/`), a `CHANGELOG.md`, and a packaged `.mcpb` of the connector.

Do not open `ANSWER-KEY.md` until your checkpoint. It lists the planted traps.
