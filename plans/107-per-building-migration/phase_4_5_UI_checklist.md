# Phases 4 & 5 — UI Execution Checklist (Kyle)

These steps **cannot be done via API** (cross-sheet named ranges, sheet rename/move). API phases 1, 2a, 2b, 2c, 3 are complete and verified. Do these in the Smartsheet UI.

Sheet IDs:
- New Programme (per building): `4820480841174916` — <https://app.smartsheet.com/sheets/9wjXRCF8JcFxjmJ7hwJf7RPqVWRQGpcG3xfJq6Q1>
- Old Programme (to archive): `5063906232848260`
- Construction Register: `2635310868418436`
- Budget: `5631895457976196`
- Archive folder: `6798331356702596`

---

## Phase 4 — Cross-sheet references (on the NEW Programme `4820480841174916`)

For each column below: right-click the column header → **Edit Column Formula** → **References Other Sheets** → pick the source sheet, select the column range, name it exactly as shown → paste the formula → Save.

### 4.1 Construction Status  ← Construction Register
Named ranges to create:
- `Register Construction Status` → Construction Register column **Construction Status**
- `Register Contract Block` → Construction Register column **Contract Block** (now holds Building References)

Formula:
```
=IFERROR(INDEX({Register Construction Status}, MATCH([Building Reference]@row, {Register Contract Block}, 0)), "")
```
Caveat: returns the status of the **first** matching unit in the building. If duplex units differ, only one shows. Acceptable for now (Phase 5 enhancement option: a worst-case helper).

### 4.2 Budget Approved ← Budget
Named ranges:
- `Budget Building Reference` → Budget column **Building Reference**
- `Budget Budget Approved` → Budget column **Budget Approved**

Formula:
```
=IFERROR(INDEX({Budget Budget Approved}, MATCH([Building Reference]@row, {Budget Building Reference}, 0)), "")
```

### 4.3 Expected Total Cost ← Budget
- `Budget Expected Total Cost` → Budget column **Expected Total Cost**
```
=IFERROR(INDEX({Budget Expected Total Cost}, MATCH([Building Reference]@row, {Budget Building Reference}, 0)), "")
```

### 4.4 Expected Variance ← Budget
- `Budget Expected Total Variance` → Budget column **Expected Total Variance**
```
=IFERROR(INDEX({Budget Expected Total Variance}, MATCH([Building Reference]@row, {Budget Building Reference}, 0)), "")
```

### 4.5 (Optional, on the OLD Programme `5063906232848260` during cutover window)
To stop its Construction Status drifting before archive, convert that column to a pull from Register on Task Name = Unit Number. Skip if you're archiving immediately.

**Checkpoint 4:** spot-check 3–4 building rows on the new Programme — Construction Status / Budget Approved / Expected values should populate. `#NO MATCH` on a row means its Building Reference isn't on the Register/Budget — re-check.

---

## Phase 5 — Cutover and archive

1. **Verify** the new Programme one more time (53 buildings + 260 phase rows; cross-sheet pulls return values).
2. **Rename old Programme** `5063906232848260`: `107 - Construction Programme` → `107 - Construction Programme (ARCHIVE - per unit)`.
3. **Move** the renamed old Programme into the **Archive** folder (`6798331356702596`).
4. **Rename new Programme** `4820480841174916`: `107 - Construction Programme (per building)` → `107 - Construction Programme`.
5. **Repoint the 2 reports** that source from the old Programme:
   - `107 - PCG - Construction Status` (`2902958600572804`) — change source to the new Programme.
   - `107 - External - Signature Homes Build Status` (`6144240361885572`) — **external, shared with Signature Homes.** Repoint to the new Programme; sanity-check the shared view before/after so the external party sees no broken report. Coordinate timing.
6. **RAG symbol**: on the new Programme, set the `RAG` column symbol to **RYGG** (right-click → Edit Column → symbol). API couldn't do this (cosmetic only; options Red/Yellow/Green/Gray already correct).
7. **Budget report**: add `Building Reference` as a column to `RPT - 107 Budget vs Actual` (or equivalent).
8. **178,176 Budget Section flag** (from Phase 1): row `178,176` carries `S3-B05` (Stage 3 per Register) but its Budget **Section** still says "Stage 4 and 5". Decide: correct the Section to "Stage 3", or leave (Register is the source of truth either way).
9. **Memory / registry**: update `smartsheet/sheet-registry.md` — Construction Programme split into per-building Programme + Construction Register; new Programme ID after rename; Building Reference is the canonical building join key; Sales Status now a validated picklist. (Building Reference architecture is the KPV standard — also worth a line in `agents/smartsheet-business-advisor/references/kpv-conventions.md` for the next village.)

---

## Rollback (if needed, any time before/after cutover)

The old Programme is untouched and recoverable. Full reverse:
1. Delete the new Programme sheet `4820480841174916`.
2. Register: restore `Contract Block` from the `Contract Block (Legacy)` column (id `1026239933747076`) or `mapping.json → register_contract_block_old_to_new`; delete the legacy column.
3. Budget: delete the `Building Reference` column (id `7028778852454276`).
4. Unit Register: convert `Sales Status` (id `8282836699484036`) back to TEXT_NUMBER if desired (data already conformed; values are intact regardless).
5. Rename old Programme back to `107 - Construction Programme` and move out of Archive.

State files: `migration_log.md`, `mapping.json`, `phase_2a_audit.md`, this checklist — all in `plans/107-per-building-migration/`.
