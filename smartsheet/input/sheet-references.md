# Sheet References — Raw Input

Paste sheet IDs, names, links, and short descriptions here. Once confirmed, promote into `smartsheet/sheet-registry.md`.

## Sheets

| Sheet Name | Sheet ID | Link | Purpose | Notes |
|------------|----------|------|---------|-------|
| [paste] | [paste] | [paste] | [paste] | |

## Workspaces / Folders (optional)

| Workspace / Folder | ID | Purpose |
|--------------------|----|---------|
| [paste] | [paste] | [paste] |

## How to Find a Sheet ID

- In the Smartsheet UI: open the sheet → **File → Properties** → "Sheet ID"
- Or via API: `GET https://api.smartsheet.com/2.0/sheets` (lists all accessible sheets)

## Column IDs

Once a sheet is confirmed, run:

```bash
curl -H "Authorization: Bearer $SMARTSHEET_API_TOKEN" \
  https://api.smartsheet.com/2.0/sheets/{SHEET_ID}/columns
```

Record the column ID map under the sheet's section in `smartsheet/sheet-registry.md`. Never guess column IDs.
