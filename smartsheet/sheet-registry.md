# KPV Smartsheet Registry

## Last Updated: [UPDATE]

## Account

| Field | Detail |
|-------|--------|
| Account | KPV's own Smartsheet account |
| API token | Stored in `config/.env` as `SMARTSHEET_API_TOKEN` |
| Token owner | [UPDATE — who manages the KPV Smartsheet account] |

## Sheets

| Sheet Name | Sheet ID | Workspace | Purpose | Status |
|------------|----------|-----------|---------|--------|
| [UPDATE] | | | | |

## Column Maps

Add per-sheet column ID tables here as they are confirmed.
Use the Smartsheet API `GET /sheets/{id}/columns` to retrieve column IDs.
Never guess column IDs — always confirm from the live sheet.

---

## How to Get Column IDs

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.smartsheet.com/2.0/sheets/{SHEET_ID}/columns
```

Or via n8n: Smartsheet node → Get Columns → sheet ID.
