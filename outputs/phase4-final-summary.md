# Phase 4 — Final Summary

**Date:** 2026-05-23
**Brief:** v2 (with §6.5/6.6/6.7/6.8 mid-execution updates)
**Status:** ✅ API phases A–E complete for 104, 105, 106. Awaiting Kyle's Phase F UI work.

---

## Headline numbers

- **30 folders** created across 3 village workspaces (7 top-level + 3 sub-folders each)
- **51 sheets cloned** from 107 (17 per village × 3) — Resource Consent Register excluded per Decision 1
- **6 columns added to 107 Decision Log** (§6.5 spec) — Village formula, Due Date, Source, Source Reference + 2 picklists rewritten
- **4 columns added to 107 Risk Register** (§6.7 spec) + Category picklist rewritten + 5 "HS" rows migrated
- **1 new portfolio register** created (`000 - Project Reference Picklists`, 62 rows)
- **2 sheets re-cloned on 104** (Decision Log + Risk Register) after 107 spec landed mid-execution
- **1502 rows imported** via XLSX (286/142/105 Unit Reg + 26/41/24 Civil + 285/301/101 Construction + 78/38/24 Contract + 51 Chart Sources)
- **114 column formulas verified** (38 per village × 3) — 0 drift
- **0 hard errors** across the full run

---

## What was done — by phase

### Pre-flight (§1)
- 3 village workspaces confirmed completely empty (sheets + folders)
- 17 of 18 107 sources accessible (Resource Consent Register confirmed 404 — deleted Phase 1 per Decision 1)
- 15 XLSX files inspected for column structure
- Output: `outputs/phase4-preflight-audit.md`

### Phase A — folder restructure
- 30 folder creates total (7 top + 3 sub per village)
- All 3 workspaces verified at 7 top-level folders in correct order
- Output: `outputs/phase4-folder-ids.json`

### 107 pre-Phase-B updates (§6.5, §6.7, §6.8)
- Created `000 - Project Reference Picklists` register, 62 rows
- 107 Decision Log: Forum (7-opt) + Decision Type (8-opt, "Health and Safety") picklists; added Village/Due Date/Source/Source Reference cols
- 107 Risk Register: Category (8-opt) picklist; 5 "HS" rows migrated → "Health and Safety"; added Village/Linked Stage/Linked Building/Accountable Person cols
- 104's already-cloned Decision Log + Risk Register deleted and re-cloned from updated 107

### Phase B — sheet clones
- 17 sheets per village cloned via `POST /sheets/{id}/copy?include=filters,forms` (excludes row data, keeps columns/formulas/forms/filters)
- 18 AUTO_NUMBER prefix resets per village pattern
- Village column formulas set to `="104"` / `="105"` / `="106"` on Decision Log + Risk Register
- Output: `outputs/phase4-sheet-ids.json`

### Phase C — Stage picklist customisation
- 7 sheets per village updated with village-specific Stage options
- Building Reference picklist DEFERRED (source XLSX has no Building Reference column)
- 0 errors across 21 picklist updates

### Phase D — data population
- 4 sheets populated per village from XLSX + 4 Chart Sources seeded from 107
- Construction Programme + Contract Register required `?overrideValidation=true` for PICKLIST values not matching destination's locked options
- Construction Register intentionally LEFT EMPTY (brief 5.3 derivation requires Building Reference not in source data)
- Outputs: `outputs/phase4-population-report.json`, `outputs/phase4-population-run.log`

### Phase E — formula audit
- 114 column formulas verified across 39 sheets (13 sheets × 3 villages with formulas)
- 0 missing, 0 differing, 0 extras
- Cross-sheet refs show `#REF` — EXPECTED until Phase F.1
- Output: `outputs/phase4-formula-audit.json`

---

## What Kyle needs to do (Phase F — UI work, ~3-4 hours per village)

Per-village checklist:

1. **Cross-sheet references** (~45 min). Open Sheet Reference Manager on each formula-using sheet; create village-scoped references per the matrix in Phase 4 brief §7.1. Without these, all cross-sheet formulas show `#REF`.

2. **Picklist reconciliation** (~30 min):
   - **Construction Status** orphan values from `overrideValidation` import — sweep Construction Programme + Contract Register, update orphaned values or re-add picklist options.
   - **Building Reference** — replace 107-inherited `S1-B01..S5-B08` with village masterplan values across all sheets that use Building Reference as a picklist.

3. **Construction Register population** (~30-45 min per village). One row per building with: Building Reference, comma-separated Unit Numbers, Typology, Stage. Currently empty across all 3 villages. Deferred by Phase 4 because source XLSX lacks Building Reference column.

4. **Contract Register Supplier ID assignment** (~15-20 min per village). All 78 + 38 + 24 contract rows have blank Supplier ID. Match each to canonical IDs in `000 - Supplier Register`.

5. **Forms**: Variation Log, H&S Incidents, Decision Log forms per `kpv-conventions.md` and brief §6.5/6.6/6.7 form specs.

6. **Reports**: PCG Report Set (mirror 107 — 12 reports), Internal/External report folders.

7. **Dashboards**: `{VC} - Dashboard` + `{VC} - PCG Dashboard` mirroring 107.

8. **Conditional formatting** rules per sheet (RAG colours, overdue highlights).

9. **Power Automate flows** — 4 flows total (1 per village + 107) for Variation Log `Final Approval Status = Approved` → Decision Log auto-create per §6.5.

10. **Master Decision Register + Master Risk Register** (portfolio-level cross-sheet reports). Cannot be created via API. Build once after all 4 villages' Decision Logs/Risk Registers exist. Default filter `Forum ≠ Site` and `Status ≠ Closed` respectively.

---

## Decisions I made autonomously while Kyle was out of signal

Per Kyle's authorisation ("continue in the background"):

1. **Resource Consent Register**: maintained Decision 1 — not cloned to any village.
2. **Construction Register row population**: deferred to Kyle's manual entry rather than synthesize Building References from grouping logic.
3. **Contract Register Supplier ID**: left blank rather than hardcode `SUP-0001` (brief 5.4 suggested) — chose silence over potentially wrong data.
4. **Construction Programme + Contract Register validation failures**: used `overrideValidation=true` per admin Smartsheet API to preserve source data; flagged for Kyle's picklist reconciliation pass.
5. **Building Reference picklist customisation**: deferred to Kyle's UI work — source XLSX doesn't contain village masterplan building references.
6. **Stage picklist values per village**: extracted from each village's Unit Register XLSX as canonical. Civil Programme uses civil-specific Stage decomposition per its source file. 105 Civil's "Stage 2-3" combined value preserved. 104 Civil's "Stage 3B/3C" combined preserved.
7. **Halt rule** still active: all hard errors would have halted. None encountered (validation overrides were the only retry needed; pattern explicitly allowed by Smartsheet API for admin users).

---

## Outputs index

| File | Purpose |
|---|---|
| `outputs/phase4-preflight-audit.md` | Pre-Phase-A baseline + 107 source audit + XLSX inventory |
| `outputs/phase4-folder-ids.json` | All folder IDs per village |
| `outputs/phase4-sheet-ids.json` | All sheet IDs per village (includes re-clone IDs for 104 Decision Log + Risk Register) |
| `outputs/phase4-107-formulas.json` | 107 column formulas snapshot (Phase E reference) |
| `outputs/phase4-column-cache.json` | Column metadata for Phase D data mapping |
| `outputs/phase4-population-report.json` | Phase D row import counts + per-sheet warnings |
| `outputs/phase4-population-run.log` | Full execution log for Phase D |
| `outputs/phase4-formula-audit.json` | Phase E formula audit (114 formulas across 39 sheets) |
| `outputs/phase4-village-104-complete.md` | 104 Drury detailed completion report |
| `outputs/phase4-village-105-complete.md` | 105 Rototuna completion report |
| `outputs/phase4-village-106-complete.md` | 106 Waihi Beach completion report |
| `outputs/phase4-final-summary.md` | This file |

---

## Carryover items not in Phase 4 scope but still pending

These were on the books before Phase 4 and remain:

- **Quality RAG symbol RYGG** on `107 - Monthly RAG Log` — UI-only cell-clear + symbol-change.
- **Civil Programme Section I cuts on 107** — deferred until Contract Register has the Matco Stage 1 row populated.
- **Chart Source `{Construction Programme Is Unit}`** broken named-range on 107 — UI-only repair.
- **Sales Status formula migration on 107 Unit Register** (Phase 1 carryover) — UI-only cross-sheet ref creation.

All Phase 4 sheets inherit these gaps from 107 since they're cloned from current state. Kyle's Phase F includes these by extension.
