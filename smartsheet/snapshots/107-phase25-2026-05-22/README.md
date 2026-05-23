# 107 Phase 2.5 — pre-destructive snapshots

Captured 2026-05-22 via Smartsheet API before any destructive operations.

Snapshots cover every column slated for deletion plus values used to verify formula conversions.

## Files

- `unit-register-typology-before.json` — Typology values per unit; confirms no use of options being removed
- `hs-incidents-type-before.json` — Type values per row on H&S Incidents; confirms no use of "Lost Time Injury"
- `risk-register-formulas-before.json` — Likelihood/Consequence/Score/RAG per risk; shows one manual RAG override (RSK-0012)
- `construction-programme-cut-columns-before.json` — Data on the 7 Construction Programme columns slated for deletion
- `civil-programme-cut-columns-before.json` — Data on the 6 Civil Programme columns slated for deletion
- `pcg-snapshot-cut-columns-before.json` — Data on the 17 PCG Status Snapshot columns slated for deletion (1 row only)
- `unit-register-cut-columns-before.json` — Data on the 4 Unit Register columns slated for deletion (Beds/Garage/Attachment Type/Floor Area)
