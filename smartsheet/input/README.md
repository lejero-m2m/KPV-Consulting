# Smartsheet Input

Drop information here as a starting point for Smartsheet API work. Once content is confirmed, it should be promoted into `smartsheet/sheet-registry.md` (the canonical registry).

## Files

| File | Purpose |
|------|---------|
| `api-access.md` | API token reference, account ID, endpoint notes. **Secret token lives in `config/.env`, not here.** |
| `sheet-references.md` | Sheet IDs, names, links, and brief purpose. Raw paste area before formalising in the registry. |
| `overview.md` | What you are trying to update, why, and the workflow context. |

## Workflow

1. Paste raw inputs into the relevant file in this folder.
2. Confirm column IDs from the live sheet (`GET /sheets/{id}/columns`) — never guess.
3. Promote confirmed sheet metadata into `smartsheet/sheet-registry.md`.
4. Implementation plans for API updates live in `plans/`.
