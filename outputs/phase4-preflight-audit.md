# Phase 4 — Pre-flight audit

**Generated:** 2026-05-23
**Brief:** Phase 4 multi-village rollout (104, 105, 106 from 107 template)
**Status:** Ready for Kyle's authorisation to start Phase A — but **3 decisions needed first** (see end).

---

## 1.1 — Baseline audit (3 target workspaces)

All three workspaces are confirmed completely empty — Kyle has cleared sheets AND folders, so Phase A simplifies to "create 7 folders fresh, no rename/delete needed".

| Workspace | ID | Sheets | Folders | Reports | Dashboards |
|---|---|---|---|---|---|
| 104 - Drury - KLE | `5737366867470212` | 0 ✓ | 0 ✓ | 0 ✓ | 0 ✓ |
| 105 - Rototuna | `2189930039404420` | 0 ✓ | 0 ✓ | 0 ✓ | 0 ✓ |
| 106 - Waihi Beach | `1169583248828292` | 0 ✓ | 0 ✓ | 0 ✓ | 0 ✓ |

Source: `GET /workspaces/{id}` via REST API (the MCP `browse_workspace` errors on empty workspaces with a pydantic validation error — use REST directly instead, pattern same as the Phase 2.5 v2 work).

---

## 1.2 — 107 source sheet verification

17 of 18 expected sources accessible. **One source — 107 - Resource Consent Register — confirmed 404** (deleted in Phase 1 per registry, conventions §7).

| Sheet | Sheet ID | Version | Status |
|---|---|---|---|
| 107 - Unit Register | `5289542339743620` | 230 | ✓ |
| 107 - Construction Register | `2635310868418436` | 168 | ✓ |
| 107 - Civil Programme | `6233992763232132` | 83 | ✓ |
| 107 - Construction Programme | `4820480841174916` | 146 | ✓ |
| 107 - Resource Consent Register | `1643703515959172` | — | **❌ 404 — deleted Phase 1** |
| 107 - RFQ and Quote Register | `5413487898480516` | 12 | ✓ |
| 107 - Variation Log | `2963546479480708` | 23 | ✓ |
| 107 - Contract Register | `3948571190579076` | 35 | ✓ |
| 107 - Sales Register | `8224519314427780` | 92 | ✓ |
| 107 - Risk Register | `1049548813193092` | 32 | ✓ |
| 107 - Decision Log | `1863332356116356` | 6 | ✓ |
| 107 - Monthly RAG Log (was PCG Status Snapshot) | `8488689867902852` | 58 | ✓ |
| 107 - H and S Incidents and Observations | `8305827340308356` | 12 | ✓ |
| 107 - H and S Monthly Indicators | `3104570405244804` | 9 | ✓ |
| 107 - Chart Source - Application Strength | `2191119310868356` | 10 | ✓ |
| 107 - Chart Source - Construction Progress | `4094966644035460` | 20 | ✓ |
| 107 - Chart Source - Sales Pipeline | `7953427823808388` | 12 | ✓ |
| 107 - Chart Source - Typology Sales | `1171511254667140` | 13 | ✓ |

Per the brief's listing the expected count is 19, but the unique count is 18 (PCG Status Snapshot and Monthly RAG Log are the same sheet under different names — Phase 2.5 rename). With Resource Consent Register deleted, **viable source count is 17**.

---

## 1.3 — Data file inventory

Python (`openpyxl 3.1.5`) available — XLSX headers read locally.

### 104 - Drury (9 files in `input/104 - Drury/`)

| File | Sheet name | Cols | Rows | Brief uses this? |
|---|---|---|---|---|
| `104 - Civil Programme.xlsx` | 104 - Civil Programme | 19 | 27 | ✅ Yes (Civil Programme) |
| `104 - Civil and Construction Program (1).xlsx` | 104 - Civil and Construction Pr | 18 | 515 | ❌ No — old merged file (historical) |
| `104 - Construction Programme.xlsx` | 104 - Construction Programme | 17 | 374 | ✅ Yes (Construction Programme) |
| `104 - RFQ and Quote Register (1).xlsx` | 104 - RFQ and Quote Register | 23 | 2 | ✅ Yes (RFQ Register) — **header + 1 data row** |
| `104 - Resource Consent Register.xlsx` | 104 - Resource Consent Register | 21 | 1 | ⚠️ Yes per brief, but **header-only — no data** |
| `104 - Unit Register (1).xlsx` | 104 - Unit Register | 38 | 286 | ❌ No — brief says use (2) |
| `104 - Unit Register (2).xlsx` | 104 - Unit Register | 39 | 287 | ✅ Yes (Unit Register) |
| `104 - Variation Log.xlsx` | 104 - Variation Log | 24 | 1 | ⚠️ Yes per brief, but **header-only — no data** |
| `104-Drury-Build-Contracts.xlsx` | Build Contracts | 19 | 79 | ✅ Yes (Contract Register) |

### 105 - Rototuna (6 files)

| File | Sheet name | Cols | Rows | Brief uses this? |
|---|---|---|---|---|
| `105 - Civil Programme.xlsx` | 105 - Civil Programme | 19 | 42 | ✅ Yes |
| `105 - Civil and Construction Program.xlsx` | 105 - Civil and Construction Pr | 18 | 197 | ❌ No — old merged file |
| `105 - Construction Programme.xlsx` | 105 - Construction Programme | 17 | 801 | ✅ Yes |
| `105 - Unit Register (1).xlsx` | 105 - Unit Register | 39 | 143 | ✅ Yes (brief says use (1)) |
| `105 - Unit Register.xlsx` | 105 - Unit Register | 38 | 139 | ❌ No — older structure |
| `105-Rototuna-Build-Contracts.xlsx` | Build Contracts | 19 | 39 | ✅ Yes |

### 106 - Waihi Beach (7 files)

| File | Sheet name | Cols | Rows | Brief uses this? |
|---|---|---|---|---|
| `106 - Civil Programme.xlsx` | 106 - Civil Programme | 19 | 25 | ✅ Yes |
| `106 - Civil and Construction Program.xlsx` | 106 - Civil and Construction Pr | 18 | 64 | ❌ No — old merged file |
| `106 - Construction Programme.xlsx` | 106 - Construction Programme | 17 | 591 | ✅ Yes |
| `106 - Unit Register (1).xlsx` | 106 - Unit Register | 39 | 106 | ✅ Yes |
| `106 - Unit Register.xlsx` | 106 - Unit Register | 38 | 107 | ❌ No — older structure |
| `106-KPW-Civil-Programme.xlsx` | Civil Programme | 17 | 25 | ❌ No — header newlines (`\n` in `Civil\nContractor`) — older file, ignore |
| `106-Waihi-Beach-Build-Contracts.xlsx` | Build Contracts | 19 | 25 | ✅ Yes |

### Column structure observations

**Unit Register source files have ~39 columns vs 107 target ~18.** Many extra fields in source data: `Build Partner`, `Contract Package`, `Contract Price (incl GST)`, `Construction Budget Price`, `Construction Budget Variance`, `Construction Variance Flag`, `Budget Sale Price`, `List Price`, `Sale Price Variance`, `Sale Variance Flag`, `CCC Received`, `Master Build Certificate`, `Expected Settlement Date`, plus `Beds`/`Garage`/`Attachment Type`/`Floor Area (m²)` (these were Phase 2.5 CUTS from 107 — now formula-pulled from Typology Register).

Brief 5.2 column-mapping rule covers this: "If a file column has no match on destination, log warning and skip it. If a destination column has no match in file, leave it blank (formula columns will populate)." Expected outcome: ~18 of 39 source cols land on each Unit Register; the rest are skipped with warnings.

**Civil Programme source files (19 cols)** include the 6 financial cols (Civil Contractor, Civils Budget, Contracted Price, Budget Variance, Variations to Date, Total Cost) — which were Phase 2.5 Section I cuts **deferred** on 107. So 107 still has them. Population fits 1:1.

**Construction Programme source files (17 cols)** include `Build Partner`, `Contract Price`, `Variations`, `Building Consent Number` — these were Phase 2.5 cuts from 107 (Section H executed). Destination won't have these columns. Will skip 4 of 17 source cols.

**Build Contracts XLSX files** (19 cols) map clean 1:1 to 107 Contract Register columns.

**Variation Log + Resource Consent Register source files are header-only** (no data). Empty sheets will be created either way; population is moot.

---

## Phase A simplification

Because workspaces are completely empty (not just sheet-empty), Phase A is just `create_folder_in_workspace` ×7 per village + `create_folder_in_folder` ×3 per village (Chart Sources + Internal + External). Total **30 folder creates** across 3 villages. No deletes, no renames.

---

## Phase B simplification (sheet-clone count)

If Resource Consent Register is dropped, sheet clones per village = **17** (not 19). Total = **51 sheet clones** (not 57).

If Resource Consent Register is included (cloned from XXX Village Template or built fresh), sheet clones per village = **18**. Total = 54.

---

## Anomalies / risks raised by pre-flight

1. **107 - Resource Consent Register doesn't exist** (deleted Phase 1). Brief Phase B expects to clone it. See Decision #1 below.
2. **Brief sheet count** says 19 sheets per village. Actual is 17 or 18 depending on Resource Consent Register decision.
3. **Brief AUTO_NUMBER prefix for Resource Consent uses `RC`** (`104-RC-0001`) but locked naming conventions §3 says `RCN` (`104-RCN-0001`). Minor — only matters if we create the sheet.
4. **Build Partner column** on 107 - Construction Register: brief Phase E formula in section 6.1 references `Build Partner` as a SOURCE column, but per Phase 2.5 Construction Register tasks J.1, Build Partner was to become formula-driven from Supplier Register (UI-only conversion not yet done). On 107 right now Build Partner is still a PICKLIST. The cloned Construction Register will inherit the PICKLIST; UI-only formula conversion still applies post-rollout.
5. **Construction Register inherits a `Stage` formula on clone** that derives Stage from Building Reference using LEFT()/FIND() string-parsing. Per kpv-conventions §7, stage picklists deliberately differ per village. If 105/106 use stage codes that don't parse cleanly (e.g. `S5-216-1` on 106 per the synthetic identifier exception in `kpv-naming-conventions.md` §4) the formula may produce garbage. Pre-flight should verify; flag for review post-clone.
6. **MCP `browse_workspace` chokes on empty workspaces** (pydantic validation error). Workaround: use REST directly via curl. Already proven on Phase 2.5 v2 work.
7. **MCP doesn't expose `copy_file` or `update_sheet`.** Brief Phase B uses both. Both work via REST: `POST /sheets/{id}/copy` and `PUT /sheets/{id}` — same pattern as Phase 2.5 v2.

---

## Decisions Kyle needs to make before Phase A starts

### Decision 1 — Resource Consent Register handling

107 doesn't have one (deleted Phase 1, by design — consent status lives on Construction Register and flows to Unit Register). Brief expects to clone it. Options:

- **A. Don't create it on any village.** Consistent with 107's current model. 104 has a data file (header-only — no data anyway). 105/106 have no data files. Drop from sheet count → 17 sheets/village.
- **B. Create on 104 only**, cloned from XXX Village Template (`3572291202928516`), since 104 has the source file structure. 105/106 don't get one. Sheet count: 18/17/17.
- **C. Create on all 3**, cloned from XXX Village Template. Empty for 105/106; 104 populated (header-only, so really also empty). 18 sheets/village.

### Decision 2 — AUTO_NUMBER prefix for Resource Consent

If we proceed with B or C, use `RC` (per brief 11.4) or `RCN` (per locked naming conventions §3)?

### Decision 3 — Construction Register `Stage` formula on 106

Construction Register inherits a `=IFERROR("Stage " + MID([Building Reference]@row, ...))` formula that parses the stage code out of `S{N}-B{NN}` Building Reference values. 106 Waihi Beach uses synthetic identifiers `S5-216-1` for Stanaway/Clarence blocks per kpv-naming-conventions §4. The formula will likely return `Stage 5` for `S5-216-1` (parses up to the first `-`), which is correct. But if 106 has other non-standard references, the formula may misbehave.

- **A. Proceed and accept** — formula likely fine; review post-clone.
- **B. Pre-emptively swap to a per-village Stage PICKLIST** on Construction Register for 106 only (matches `Linked Stage` on most other sheets).
