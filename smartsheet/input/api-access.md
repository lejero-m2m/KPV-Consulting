# Smartsheet API Access

## Token

The KPV Smartsheet API token is stored in `config/.env` as `SMARTSHEET_API_TOKEN`. **Do not paste the token into this file or any committed file.**

To confirm the token is set:

```bash
grep SMARTSHEET_API_TOKEN /home/kyle/KPV-Consulting/config/.env
```

## Account Details

| Field | Value |
|-------|-------|
| Account owner | [Kyle to confirm — who manages KPV's Smartsheet account] |
| Plan / tier | [UPDATE] |
| Account ID (if known) | [UPDATE] |
| Primary user email | [UPDATE] |

## API Endpoint

- Base URL: `https://api.smartsheet.com/2.0`
- Auth header: `Authorization: Bearer $SMARTSHEET_API_TOKEN`
- Docs: https://smartsheet.redoc.ly/

## Quick Test

```bash
curl -H "Authorization: Bearer $SMARTSHEET_API_TOKEN" \
  https://api.smartsheet.com/2.0/users/me
```

Expected response: JSON with the token owner's user record.

## Notes

[Any rate limit, scope, or permission notes Kyle wants to record]
