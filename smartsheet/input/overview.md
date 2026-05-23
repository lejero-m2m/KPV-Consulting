# Smartsheet Update — Overview

## Goal

[What are you trying to achieve by updating Smartsheets via the API? e.g. "Sync development pipeline status from local notes into the master tracker."]

## Sheets in Scope

[Which sheets will be read or written. Reference `sheet-references.md` for IDs.]

## What Will Be Updated

| Sheet | Operation | Fields / Columns | Trigger |
|-------|-----------|------------------|---------|
| [name] | read / add row / update row / update cell | [columns] | [manual / scheduled / event] |

## Source of Truth

[Where does the data come from? A local file, another sheet, an n8n workflow, manual input?]

## Frequency

[One-off migration / on demand / scheduled (cron) / event-driven]

## Constraints & Risks

- Never overwrite data without confirmation if a row was edited by a user since last sync
- Respect Smartsheet API rate limits (300 requests / minute / token)
- [Any KPV-specific constraints — e.g. "do not touch Board Reporting workspace"]

## Open Questions

- [ ] [Kyle to confirm — anything outstanding before implementation]
