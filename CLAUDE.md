# KPV-Consulting — Claude Code Workspace

**Client:** Karaka Pines Village (KPV)  
**Role:** Kyle Dickinson — Director of Development  
**Workspace owner:** Lejero Consulting  
**Last updated:** 2026-05-14

---

## Scope

This workspace covers all work Kyle does in his Director of Development capacity at Karaka Pines Village. It is separate from the Lejero `Claude-Consulting` monorepo.

**In scope:**
- KPV development management and feasibility work
- KPV Smartsheet integration (KPV's own Smartsheet account)
- KPV documents, context, and deliverables
- KPV-specific agents and automation

**Out of scope:**
- `retire-app` (KPV iQ platform) — lives in `Claude-Consulting/apps/retire-app/`
- Lejero's Smartsheet account or credentials
- Other Lejero clients (Quinovic, Urban Homes, etc.)
- Shared PostgreSQL database schema changes

---

## KPV Systems Project — full context

For any work involving Smartsheet design, dashboards, reports, the documentation suite (Flow PNG + Word manual), the village lifecycle, naming conventions, brand palettes, or platform integration (Teams / SharePoint / Zoho), read the **`smartsheet-business-advisor` skill** at `agents/smartsheet-business-advisor/` — it carries the authoritative project context. Start with:

- **`agents/smartsheet-business-advisor/references/kpv-conventions.md`** — village register (100–107), lifecycle phases, folder structure, naming conventions, sheet name intent, brand palette options (systems vs marketing), documentation suite pattern, KPV principles, Teams channel mapping, KPV-specific advisory checklist
- **`agents/smartsheet-business-advisor/SKILL.md`** — the agent's operating instructions and pointers to the other reference files (Microsoft 365 integration, report production, Smartsheet capabilities and limits, generic Business-plan guide and templates)

The skill is the **single source of truth** for KPV systems-project conventions. This CLAUDE.md stays short and points at the skill; do not duplicate project rules here. When the live setup diverges from what the skill describes, Kyle's latest instruction wins — and the skill should be updated to reflect the new direction.

---

## Folder Structure

```
KPV-Consulting/
├── CLAUDE.md                    # This file
├── .claude/commands/            # Slash commands
├── context/                     # KPV business context
│   ├── kpv-overview.md          # Organisation, villages, team
│   ├── role-brief.md            # Kyle's role, scope, reporting
│   ├── current-priorities.md    # Active focus areas and decisions
│   └── development-pipeline.md # Active and upcoming development projects
├── clients/                     # KPV sub-projects (if needed)
├── development/                 # Development projects managed by Kyle
│   ├── active/                  # Current projects
│   └── inactive/                # Completed or paused
├── smartsheet/                  # Sheet IDs, column maps, integration notes
│   └── sheet-registry.md        # Master list of KPV Smartsheet sheets
├── agents/                      # KPV-specific agents (future)
│   ├── _context/
│   └── _templates/
├── config/
│   ├── .env                     # KPV credentials (gitignored)
│   └── .env.example             # Placeholder for onboarding
├── plans/                       # Implementation plans
├── outputs/
│   ├── meeting-notes/
│   ├── reports/
│   └── research/
└── reference/
    └── assets/                  # KPV brand assets
```

---

## Key Rules

1. **NZ English** throughout (colour, analyse, organise, prioritise)
2. **KPV Smartsheet token only** — never use Lejero token in this workspace
3. **Credentials in `config/.env`** — never in source code, never committed
4. **Client confidentiality** — KPV data does not leave this workspace
5. **Never fabricate statistics** — use known data or ask Kyle
6. **GitHub is single source of truth** — commit before deploying
7. **CLAUDE.md stays current** — update when structure changes
8. **Flag `[UPDATE]` markers** — do not invent content

---

## Smartsheet

KPV has its own Smartsheet account. All sheet IDs and column maps are documented in `smartsheet/sheet-registry.md`.

API token: stored in `config/.env` as `SMARTSHEET_API_TOKEN`

When integrating with KPV Smartsheets:
- Always read `smartsheet/sheet-registry.md` first
- Column IDs must be confirmed from the live sheet — do not guess
- Use the n8n Smartsheet node or direct API calls via n8n workflows

---

## Context Files

Read these at the start of any session:

| File | Purpose |
|------|---------|
| `agents/smartsheet-business-advisor/references/kpv-conventions.md` | **Authoritative KPV systems-project context** — village register, lifecycle, naming, sheets, brand palettes, documentation suite, principles |
| `agents/smartsheet-business-advisor/SKILL.md` | Smartsheet advisor operating instructions + pointers to MS 365 integration, report production, capabilities-and-limits references |
| `context/kpv-overview.md` | Organisation background, villages, team |
| `context/role-brief.md` | Kyle's role, scope, authority, reporting |
| `context/current-priorities.md` | What Kyle is focused on right now |
| `context/development-pipeline.md` | Active and upcoming development projects |
| `smartsheet/sheet-registry.md` | All KPV Smartsheet sheet IDs |

---

## Commands

Slash commands in `.claude/commands/`:

| Command | Purpose |
|---------|---------|
| `/prime` | Read all context files, flag staleness |
| `/meeting-notes` | Process raw notes → structured output |
| `/draft-email` | Draft professional emails |
| `/create-plan` | Plan changes without implementing |
| `/implement` | Execute a saved plan |
| `/create-report` | Structured report generation |

---

## Staleness Markers

Flag these, do not fill them:
- `[UPDATE]`, `[TBC]`, `[TO BE CONFIRMED]`
- `[Kyle to confirm]`, `[Kyle to update]`
- `TODO`, `FIXME`, `PLACEHOLDER`
