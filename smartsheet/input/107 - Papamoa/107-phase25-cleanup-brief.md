# Phase 2.5 — 107 Papamoa Structural Cleanup Brief

**Owner:** Kyle Dickinson
**Purpose:** Execute the structural cleanup of 107 Papamoa following an in-depth column-by-column architecture review (May 2026). All 17 sheets reviewed. This is the cleanup brief that locks in the new architecture before snapshotting to XXX Village Template (Phase 3) and deploying to 105/106 (Phase 4).
**Smartsheet account:** app.smartsheet.com (NA host)
**Smartsheet MCP toolkit:** active
**Prior phases:** Phase 1 (107 cleanup) complete; Phase 2 (new registers built) complete.
**Brief version:** 2 (May 23 2026) — adds Variation Log granular workflow upgrade and 4-tier approval matrix per KPV org structure (Section K significantly expanded). Naming conventions locked per `kpv-naming-conventions.md`.

---

## Naming conventions reference

This brief references conventions locked in `kpv-naming-conventions.md`. Key items Claude Code must follow during execution:

- **Cross-sheet reference names** — use the 2-3 letter abbreviation pattern (e.g. `UR Sales Status`, `TR Beds`, `VL Cost Impact (NZD)`). Sheet abbreviations: UR, SR, RR, DL, MRL, ConP (Construction Programme), CivP (Civil Programme), ConR (Construction Register), ContR (Contract Register), VL, RFQ, HSI, HSM, TR, SuppR, PF
- **AUTO_NUMBER IDs** — `[VillageCode]-[Type]-NNNN` with 4-digit zero-padded sequence (e.g. `107-VAR-0001`, `107-RFQ-0001`)
- **Picklist values** — Title Case, no abbreviations except universal (LTI, MTI, PSIF), `Yellow` not `Amber` for RAG
- **Column names** — Title Case, parentheses for units `(NZD)`, `(m²)`, `(days)`

Any divergence between these conventions and the existing sheets is flagged for cleanup during Phase 2.5 execution. See Section T for retrofit tasks.

---

## How to work this brief

1. Sections are ordered to minimise rework. Folder structure first (formula-safe), then sheet renames (formula-safe), then column changes per sheet.
2. **Destructive operations** (delete column, delete sheet, rename column) require explicit Kyle confirmation before action. Never act on assumptions.
3. **UI-ONLY operations** (forms, automations, conditional formatting, dashboard widgets, cross-sheet reference creation/editing, picklist symbol settings, formula columns referencing cross-sheet ranges) cannot be done via API. Document them in the UI checklist for Kyle to action manually.
4. After each section, update `/mnt/project/kpv-smartsheet-inventory.md` and `smartsheet/sheet-registry.md` with changes.
5. **Snapshot before destructive changes.** Before deleting any column or sheet, dump the affected data to `/snapshots/107-phase25-{YYYY-MM-DD}/` as JSON.
6. At the end, produce a structured final report.

---

## Architectural principles locked in (do not relitigate)

These principles govern every decision in this brief. They go into `kpv-conventions.md` as a new "Sheet design rules" section after this brief executes.

1. **One sheet, one job.** Each sheet has a single primary purpose. No sheet does timeline AND finance AND status.
2. **Programmes track time. Registers track state. Contracts hold contract values. Variations hold variations. Project Finance holds budgets.**
3. **Canonical source per concept.** Each fact lives in one place. Other sheets pull via cross-sheet formula, not manual entry.
4. **Picklists for stable known values; cross-sheet formula lookups for values that drift** (suppliers, contractors).
5. **Folder structure serves human navigation.** Different teams see different folders.
6. **Folder moves and sheet renames are formula-safe.** Cross-sheet references use sheet IDs, not names or paths.
7. **Column renames may break formulas.** Audit cross-sheet references before any rename.

---

## Section A — Folder restructure

**Formula-safe.** Sheet IDs unchanged. Cross-sheet references unaffected. Do this first.

### Task A.1 — Confirm current folder state

Call `browse_workspace` on workspace `4481862027503492` and list all current folders with their IDs and contents. Flag any divergence from the inventory file `kpv-smartsheet-inventory.md`.

Expected current state (per Phase 1 reorganisation, Kyle's sidebar 22 May 2026):

```
107 - Papamoa
├── 00 - Dashboards
│   └── Chart Sources
├── 01 - Project Control
│   ├── 107 - PCG Status Snapshot
│   ├── 107 - Risk Register
│   ├── 107 - Sales Register
│   ├── 107 - Unit Register
│   └── 107 - Decision Log
├── 02 - Civil and Construction
│   ├── 107 - Civil Programme
│   ├── 107 - Construction Programme
│   ├── 107 - Construction Register
│   ├── 107 - Variation Log
│   ├── 107 - RFQ and Quote Register
│   └── 107 - Contract Register
├── 03 - Health and Safety (or 04 — verify)
│   ├── 107 - H and S Incidents and Observations
│   └── 107 - H and S Monthly Indicators
├── 05 - Reports Internal
│   ├── (various reports)
│   └── PCG Report Set/ (sub-folder)
└── 06 - Reports External
    └── (various reports)
```

### Task A.2 — Execute folder restructure

After Kyle confirms current state, execute these moves and renames in order. **Get explicit confirmation before each destructive step.**

**Step 1 — Create new folders:**
- Create `02 - Sales` in workspace `4481862027503492`
- Create `03 - Procurement` in workspace `4481862027503492`

**Step 2 — Move sheets to new folders:**
- Move `107 - Sales Register` (sheet ID `8224519314427780`) → `02 - Sales`
- Move `107 - RFQ and Quote Register` (sheet ID `5413487898480516`) → `03 - Procurement`
- Move `107 - Contract Register` (sheet ID `3948571190579076`) → `03 - Procurement`
- Move `107 - Variation Log` (sheet ID `2963546479480708`) → `03 - Procurement`

**Step 3 — Renumber existing folders:**
- Rename `02 - Civil and Construction` → `04 - Civil and Construction`
- Rename existing H&S folder (currently `03` per sidebar, or whatever it is now) → `05 - Health and Safety`

**Step 4 — Reports folder consolidation:**
- Rename `05 - Reports Internal` → `06 - Reports`
- Inside `06 - Reports`, create sub-folder `Internal`
- Inside `06 - Reports`, create sub-folder `External`
- Move all reports currently in `06 - Reports` (root) → `06 - Reports / Internal /`
- Move existing `PCG Report Set` sub-folder (and all its contents) → `06 - Reports / Internal /`
- Move all reports from `06 - Reports External` (the old folder) → `06 - Reports / External /`
- Delete the now-empty old `06 - Reports External` folder

**Step 5 — Verify final state matches target:**

```
107 - Papamoa
├── 00 - Dashboards
│   └── Chart Sources
├── 01 - Project Control
│   ├── 107 - Unit Register
│   ├── 107 - Risk Register
│   ├── 107 - Decision Log
│   └── 107 - PCG Status Snapshot (will be renamed in Section B)
├── 02 - Sales
│   └── 107 - Sales Register
├── 03 - Procurement
│   ├── 107 - RFQ and Quote Register
│   ├── 107 - Contract Register
│   └── 107 - Variation Log
├── 04 - Civil and Construction
│   ├── 107 - Civil Programme
│   ├── 107 - Construction Programme
│   └── 107 - Construction Register
├── 05 - Health and Safety
│   ├── 107 - H and S Incidents and Observations
│   └── 107 - H and S Monthly Indicators
└── 06 - Reports
    ├── Internal/
    └── External/
```

### Task A.3 — Update inventory and conventions

- Update `/mnt/project/kpv-smartsheet-inventory.md` with new folder IDs and new sheet placements
- Add to `/mnt/project/kpv-conventions.md` §5 (SharePoint and Smartsheet folder structure): the new 7-folder pattern for villages, with note that Procurement comes before Civil and Construction (lifecycle order)

---

## Section B — Sheet renames

**Formula-safe.** Sheet IDs unchanged.

### Task B.1 — Rename PCG Status Snapshot

Sheet ID `8488689867902852`:
- Old name: `107 - PCG Status Snapshot`
- New name: `107 - Monthly RAG Log`

Reason: after Section H column changes, this sheet only holds monthly RAG ratings and overall commentary, not the broader status snapshot it was originally designed for.

**Action:** Smartsheet API `update_sheet` with new name. Verify.

### Task B.2 — Update inventory

Update inventory file with rename. Keep "Previously known as PCG Status Snapshot" note for searchability.

---

## Section C — Unit Register (sheet ID 5289542339743620)

**Current:** 22 columns. **Target:** 18 columns.

### Task C.1 — Pre-flight typology reconciliation

Unit Register's `Typology` picklist has 27 options. Typology Register (sheet ID `4159669319716740` in `000 - Overview / 03 - Project Reference Registers`) has 29 typology rows.

**Known mismatches** (Unit Register values not in Typology Register):
- Harris SG (not on Typology Register; Typology Register only has Harris and Harris DG)
- Robertson DG, Robertson SG (Typology Register has only "Robertson")
- Stanaway DG, Stanaway SG (Typology Register has only "Stanaway")

**Kyle's decision:** consolidate Unit Register picklist to remove variants not in Typology Register.

**Action:**
1. Snapshot Unit Register Typology values per unit to `/snapshots/107-phase25-{date}/unit-register-typology-before.json`
2. Check live Unit Register Typology column for any units currently set to: Harris SG, Robertson DG, Robertson SG, Stanaway DG, Stanaway SG
3. **If any unit has one of these values, STOP and report to Kyle.** Kyle must reassign those units to a valid Typology Register value before proceeding. Do not auto-reassign.
4. Once no units use the unmapped values, remove these options from Unit Register's Typology picklist:
   - Remove: Harris SG, Robertson DG, Robertson SG, Stanaway DG, Stanaway SG
5. Verify remaining Typology picklist values all exist in Typology Register Typology Name column

### Task C.2 — Cut redundant columns

After typology reconciliation succeeds, cut these 4 columns (data is derivable from Typology Register via formula):

| Column | Column ID |
|---|---|
| Beds | `5890299397443460` |
| Garage | `3638499583758212` |
| Attachment Type | `8142099211128708` |
| Floor Area (m²) | `823749816651652` |

**Action:**
1. Snapshot current values to `/snapshots/107-phase25-{date}/unit-register-cut-columns.json`
2. Get Kyle's explicit confirmation to delete
3. Delete each column via API

### Task C.3 — Expand Sales Status picklist (in preparation for Phase 1 formula conversion)

Current Sales Status picklist (col ID `8282836699484036`) has 6 options: Not Available, Available, Application, Unconditional, Settled, Clubhouse.

Add to align with Sales Register's expanded picklist (Section D): **Conditional, Transfer, Occupied**.

Final picklist: Not Available, Available, Application, Conditional, Unconditional, Transfer, Settled, Occupied, Clubhouse (9 options).

**Action:** `update_column` on column ID `8282836699484036` with `type: 'PICKLIST'` and the updated options array. Validation stays `true`.

### Task C.4 — UI-only: Sales Status formula conversion (Phase 1 carryover)

Per Phase 1 decision: Sales Status on Unit Register becomes a cross-sheet formula reading from Sales Register.

**Cannot be done via API** — cross-sheet references must be created in the UI.

**UI checklist for Kyle:**
- [ ] In Unit Register Sales Status column, create cross-sheet references: `SR Sales Status` (pointing to Sales Register Sales Status column) and `SR Unit Number` (pointing to Sales Register Unit Number column)
- [ ] Convert Sales Status to column formula: `=INDEX({SR Sales Status}, MATCH([Unit Number]@row, {SR Unit Number}, 0))`
- [ ] Lock the column from manual edit
- [ ] Verify all units show correct Sales Status from Sales Register

### Task C.5 — UI-only: Add cross-sheet formulas pulling from Typology Register

After Task C.2 cuts the manual columns, add formula columns pulling the same data from Typology Register.

**UI checklist for Kyle:**
- [ ] In Unit Register, create cross-sheet references to Typology Register (sheet ID `4159669319716740`):
  - `TR Typology Name` → Typology Name column
  - `TR Beds` → Beds column
  - `TR Garage` → Garage column
  - `TR Attachment Type` → Attachment Type column
  - `TR Floor Area` → Floor Area (m²) column
- [ ] Add 4 new formula columns to Unit Register:
  - `Beds` = `=INDEX({TR Beds}, MATCH(Typology@row, {TR Typology Name}, 0))`
  - `Garage` = `=INDEX({TR Garage}, MATCH(Typology@row, {TR Typology Name}, 0))`
  - `Attachment Type` = `=INDEX({TR Attachment Type}, MATCH(Typology@row, {TR Typology Name}, 0))`
  - `Floor Area (m²)` = `=INDEX({TR Floor Area}, MATCH(Typology@row, {TR Typology Name}, 0))`
- [ ] Verify all units show correct derived values from Typology Register

### Task C.6 — Verify

- Re-fetch Unit Register column list. Confirm 18 columns total.
- Confirm all values populate correctly after UI follow-ups.

---

## Section D — Sales Register (sheet ID 8224519314427780)

**Current:** 16 columns. **Target:** 16 columns. Picklist update only.

### Task D.1 — Expand Sales Status picklist

Current Sales Status picklist (col ID `4247873805127556`) has 6 options: Not Available, Available, Application, Unconditional, Settled, Clubhouse.

Add: **Conditional, Transfer, Occupied**.

Final picklist (9 options): Not Available, Available, Application, Conditional, Unconditional, Transfer, Settled, Occupied, Clubhouse.

**Action:** `update_column` on column ID `4247873805127556` with `type: 'PICKLIST'` and updated options array. Validation stays `true`.

### Task D.2 — Verify

Re-fetch Sales Register column list. Confirm Sales Status has 9 options.

---

## Section E — Risk Register (sheet ID 1049548813193092)

**Current:** 13 columns. **Target:** 14 columns. Two formula conversions and one new column.

### Task E.1 — Convert Score to column formula

Current Score column (col ID `5598299569819524`) is TEXT_NUMBER manual entry. Convert to column formula: `=[Likelihood]@row * [Consequence]@row`.

**Pre-flight:**
1. Snapshot current Score values per row to `/snapshots/107-phase25-{date}/risk-register-scores-before.json`
2. Verify formula result will equal existing values (all current scores appear to be Likelihood × Consequence already: 4×4=16, 3×4=12, 4×3=12, 3×3=9, 4×2=8)

**Action:**
1. Get Kyle's explicit confirmation
2. Set column formula via `update_column` on col `5598299569819524`
3. Verify all rows show correct calculated Score
4. Compare against snapshot — flag any discrepancies

### Task E.2 — Convert RAG to column formula

Current RAG column (col ID `8888052318769028`) is PICKLIST manual with RYGG symbol set (Red, Yellow, Green, Gray).

Convert to column formula derived from Score:
```
=IF([Score]@row = "", "Gray", IF([Score]@row >= 15, "Red", IF([Score]@row >= 8, "Yellow", "Green")))
```

**Pre-flight:**
1. Snapshot current RAG values per row
2. Calculate what each row's RAG would be under the new formula based on Score
3. Compare — flag any rows where Kyle has manually overridden the matrix RAG (e.g. amber score that's been manually set red for PM judgement)
4. **If any overrides exist, STOP and report.** Kyle must decide: keep formula and lose overrides, or keep manual RAG.

**Action (after no-override confirmation):**
1. Get Kyle's explicit confirmation
2. Set column formula via `update_column` on col `8888052318769028`, keep `type: 'PICKLIST'`, keep `symbol: 'RYGG'`, keep options array
3. Verify all rows show correct calculated RAG

### Task E.3 — Add Date Identified column

Add new system column of type DATETIME with `system_column_type: CREATED_DATE`. Name: `Date Identified`.

**Action:** `add_columns` to col index just after Risk Title. Verify column added and populated with creation timestamps.

### Task E.4 — Verify

Re-fetch Risk Register column list. Confirm 14 columns total. Confirm Score and RAG are formula-driven. Confirm Date Identified shows creation timestamps for existing rows.

---

## Section F — PCG Status Snapshot → Monthly RAG Log (sheet ID 8488689867902852)

**Current:** 29 columns. **Target:** 12 columns. Significant strip.

Sheet rename already executed in Section B.

### Task F.1 — Standardise Quality RAG to match other RAG columns

Current Quality RAG column (col ID `1794470374051716`) is PICKLIST with options "Green, Amber, Red" and no symbol.

Other RAG columns use options "Red, Yellow, Green, Gray" with RYGG symbol.

**Action:**
1. Snapshot current Quality RAG values (only 1 row currently, value is "Green")
2. `update_column` on col `1794470374051716`: change options to ["Red", "Yellow", "Green", "Gray"], symbol to "RYGG", keep `type: 'PICKLIST'` and validation `true`
3. The existing "Green" value should map directly. Verify.

### Task F.2 — Cut 17 columns

These columns are either: (a) already canonical elsewhere, (b) narrative blocks that should live in the Word PCG document instead, or (c) summaries derivable from canonical sources.

| Column | Column ID | Reason |
|---|---|---|
| Civil - This Period | `3610338523385732` | Narrative block — lives in PCG Word doc |
| Civil - Next Period | `8113938150756228` | Narrative block — lives in PCG Word doc |
| Building - This Period | `795588756279172` | Narrative block — lives in PCG Word doc |
| Building - Next Period | `5299188383649668` | Narrative block — lives in PCG Word doc |
| Landscape and Other - This Period | `3047388569964420` | Narrative block — lives in PCG Word doc |
| Landscape and Other - Next Period | `7550988197334916` | Narrative block — lives in PCG Word doc |
| Sales - This Period | `1921488663121796` | Narrative block — lives in PCG Word doc |
| Sales - Next Period | `6425088290492292` | Narrative block — lives in PCG Word doc |
| Settled This Period | `7898167583739780` | Count derivable from Sales Register |
| Settled Cumulative | `579818189262724` | Count derivable from Sales Register |
| Application Count | `5083417816633220` | Count derivable from Sales Register |
| Unconditional Count | `2831618002947972` | Count derivable from Sales Register |
| Available Count | `7335217630318468` | Count derivable from Sales Register |
| Total Sales to Date | `1705718096105348` | Sum derivable from Sales Register |
| New Enquiries This Period | `6209317723475844` | Count derivable from Sales Register or Zoho CRM |
| Top Risks Summary | `3957517909790596` | Live in Risk Register, filter to top 5 |
| Board Resolutions This Period | `8461117537161092` | Live in Decision Log, filter to current period |

**Action:**
1. Snapshot all 17 columns' values to `/snapshots/107-phase25-{date}/pcg-snapshot-cut-columns.json`
2. Get Kyle's explicit confirmation to delete all 17
3. Delete columns one by one via API

### Task F.3 — Verify

Re-fetch sheet. Confirm 12 columns remain: Period Label, Period Date, Is Current Period, Overall RAG, Submitted By, Quality RAG, Programme RAG, Cost RAG, Health and Safety RAG, Sales RAG, Maori Procurement RAG, Overall Commentary.

---

## Section G — Decision Log (sheet ID 1863332356116356)

**Current:** 13 columns. **Target:** 13 columns. No changes.

Per Kyle's decision: Decision Type picklist keeps "H&S" with ampersand (already in use, not aligning to convention).

Document parked decision in `kpv-conventions.md`: H&S vs HS vs "H and S" naming divergence across sheets — accepted as-is; if cross-sheet filter on H&S category becomes needed, normaliser will be added.

---

## Section H — Construction Programme (sheet ID 4820480841174916)

**Current:** 24 columns. **Target:** 17 columns. Major financial cleanup.

### Task H.1 — Cut 7 columns

| Column | Column ID | Reason |
|---|---|---|
| Build Partner | `2328413351481220` | Hardcoded 17-value picklist — Build Partner lives on Construction Register pulling from Supplier Register |
| Contract Package | `1202513444638596` | Should be in Contract Register |
| Contract Price (incl GST) | `5706113072009092` | Should be in Contract Register |
| Variations (incl GST) | `3454313258323844` | Should be in Variation Log (canonical) summed in Contract Register |
| Budget Approved | `1765463398059908` | Should be in Project Finance |
| Expected Total Cost | `6269063025430404` | Should be in Project Finance |
| Expected Variance | `4017263211745156` | Should be in Project Finance |

**Action:**
1. Snapshot all 7 columns' values to `/snapshots/107-phase25-{date}/construction-programme-cut-columns.json`
2. Verify no current data exists that hasn't been migrated to canonical sources. If data exists that Kyle hasn't moved elsewhere, **STOP and report.**
3. Get Kyle's explicit confirmation
4. Delete columns one by one via API

### Task H.2 — Leave existing Construction Status pull as-is

Per Kyle's decision (revised mid-conversation): Construction Programme remains the canonical source for Construction Status. Construction Register pulls from Programme via formula (existing setup, do not change).

**No action.** Leave Construction Programme Construction Status column (col ID `4580213165166468`) as the manual canonical entry.

### Task H.3 — Verify

Re-fetch Construction Programme. Confirm 17 columns total. Confirm timeline columns intact (Start Date, End Date, Predecessors, Duration, % Complete).

---

## Section I — Civil Programme (sheet ID 6233992763232132)

**Current:** 19 columns. **Target:** 13 columns. Same pattern as Construction Programme.

### Task I.1 — Cut 6 columns

| Column | Column ID | Reason |
|---|---|---|
| Civil Contractor | `5504746625732484` | Hardcoded picklist — contractor lives on Contract Register via Supplier Register |
| Civils Budget (incl GST) | `6586215498551172` | Project Finance |
| Contracted Price (incl GST) | `4589952951422852` | Contract Register |
| Budget Variance (incl GST) | `7434318397083524` | Derived from financials being cut |
| Variations to Date (incl GST) | `2338153137737604` | Variation Log canonical |
| Total Cost (incl GST) | `4610895614611332` | Derived |

**Action:** same pattern as Section H. Snapshot → confirm → delete.

### Task I.2 — Document Stage picklist divergence

Civil Programme uses Stage 1/2/3/4/5/Clubhouse (no sub-stages). Construction Programme, Variation Log, Contract Register use Stage 1/2A/2B/2C/2D/2E/3/4/5. This is **deliberate** — civils don't sub-divide stage 2.

**UI checklist for Kyle:**
- [ ] Add a sheet description to Civil Programme noting the Stage picklist intentionally differs from Construction Programme

**Conventions update:**
- Add a "Stage picklist conventions" sub-section to `kpv-conventions.md` §7 documenting this difference. Future templating to 105/106 must preserve this difference.

### Task I.3 — Verify

Re-fetch Civil Programme. Confirm 13 columns total.

---

## Section J — Construction Register (sheet ID 2635310868418436)

**Current:** 19 columns. **Target:** 19 columns. Composition change — manual columns become formulas.

### Task J.1 — Convert Build Partner from hardcoded picklist to cross-sheet formula

Current Build Partner column (col ID `1304968656359300`) is PICKLIST with 17 hardcoded contractor names. Convert to TEXT_NUMBER column formula pulling from Supplier Register.

**Cannot be done via API.** Cross-sheet references must be created in the UI.

**UI checklist for Kyle:**
- [ ] In Construction Register, create cross-sheet references to Supplier Register (sheet ID `3313684242714500`):
  - `SuppR Build Partner Name` → Trading Name column (or equivalent canonical supplier-name column on Supplier Register)
  - `SuppR Build Partner ID` → Supplier ID column
- [ ] Change Build Partner column type from PICKLIST to TEXT_NUMBER
- [ ] Add formula. **Note:** the join key needs deciding. If Construction Register has a Supplier ID column for the build partner, use that. If not, lookup by name from Construction Register's existing entries. Kyle to confirm match key with Claude Code at execution time.

### Task J.2 — Pre-flight financial column changes

Per Kyle's decision (Option C): financial columns on Construction Register become cross-sheet formulas instead of manual entry.

**Current state of financial columns:**
- Contract Price (incl GST) — col `5245618330308484` — manual TEXT_NUMBER
- Post Contract Variations (incl GST) — col `1033268421234564` — manual TEXT_NUMBER
- Construction Budget (incl GST) — col `2993818516623236` — already formula pulling from Project Finance (keep as-is)
- Budget Remaining (incl GST) — col `7497418143993732` — already formula derived from the manuals
- Budget Flag — col `1867918609780612` — already formula derived

### Task J.3 — UI-only: Convert Contract Price to cross-sheet formula

**UI checklist for Kyle:**
- [ ] In Construction Register, create cross-sheet references to Contract Register (sheet ID `3948571190579076`):
  - `CR Contract Value` → Contract Value (NZD) column
  - `CR Building Reference` → a Building Reference column on Contract Register (NOTE: Contract Register may not currently have a Building Reference column — see Section K Task K.4 for the addition)
- [ ] Convert Contract Price (incl GST) column to formula. Approach depends on whether contracts on Contract Register are per-building or per-stage:
  - Per-building: `=INDEX({CR Contract Value}, MATCH([Building Reference]@row, {CR Building Reference}, 0))`
  - Per-stage (one contract covers multiple buildings): different approach needed; decide during UI work

### Task J.4 — UI-only: Convert Post Contract Variations to SUMIFS formula

**UI checklist for Kyle:**
- [ ] In Construction Register, create cross-sheet references to Variation Log (sheet ID `2963546479480708`):
  - `VL Cost Impact` → Cost Impact (NZD) column
  - `VL Linked Building` → Linked Building column
  - `VL Final Approval Status` → Final Approval Status column
- [ ] Convert Post Contract Variations (incl GST) column to formula:
  - `=SUMIFS({VL Cost Impact}, {VL Linked Building}, [Building Reference]@row, {VL Final Approval Status}, "Approved")`

### Task J.5 — UI-only: Update Budget Remaining and Budget Flag formulas

The existing formulas on Budget Remaining and Budget Flag should continue to work after Contract Price and Post Contract Variations become formulas (they reference the column values, not the entry method).

**UI checklist for Kyle:**
- [ ] After Tasks J.3 and J.4, verify Budget Remaining and Budget Flag still calculate correctly. Adjust formulas if needed.

### Task J.6 — Verify

Re-fetch Construction Register. Confirm column count still 19. Confirm composition: Build Partner is formula, financial columns are formulas (after UI work).

---

---

## Section K — Variation Log (sheet ID 2963546479480708)

**Current:** 29 columns. **Target:** 35 columns. Granular workflow upgrade and 4-tier approval matrix.

This section implements the variation workflow upgrade decided in the May 23 conversation: granular 9-state workflow, 4-tier approval matrix (Matt → Kyle → Julie → Liam), Cost Category and Variation Source root-cause analytics, and documented automation plan for Phase 2.6 execution.

### Task K.1 — Expand Approval Status picklist to granular workflow

Current Approval Status picklist has fewer states than the target granular workflow.

**Target picklist options** (9 states, ordered):
1. Draft
2. Submitted
3. Pricing
4. Pending Approval
5. Approved
6. Rejected
7. Issued
8. Built
9. Closed

**Pre-flight:**
1. Snapshot current Approval Status values per row to `/snapshots/107-phase25-{date}/variation-log-approval-status-before.json`
2. Check if any rows currently use Approval Status values not in the new picklist
3. If yes, STOP and report. Kyle must reassign before picklist update.

**Action (after no-mismatch confirmation):**
1. Get Kyle's explicit confirmation
2. `update_column` on Approval Status column with new options array
3. Set `type: 'PICKLIST'`, validation `true`

### Task K.2 — Add 4 new approval tier columns

The current Variation Log has L1 Approver (PM/Matt) and L2 Approver (Director/Kyle). The new approval matrix requires 4 tiers: Matt → Kyle → Julie → Liam.

**Add new columns** (use `add_columns`, place after existing L2 Approval Date column):

| Column name | Type | Purpose |
|---|---|---|
| L3 Approver | CONTACT_LIST | Julie (CFO) on material variations $25k-$50k |
| L3 Approval Date | DATE | When L3 signed off |
| L4 Approver | CONTACT_LIST | Liam (CEO) on strategic variations >$50k |
| L4 Approval Date | DATE | When L4 signed off |

### Task K.3 — Rename existing approval columns for clarity

The current L1 and L2 columns reference role abstractions (PM, Director). Rename to match KPV's actual role nomenclature.

| Current name | New name |
|---|---|
| L1 Approver (PM) | L1 Approver (Delivery Lead) |
| L2 Approver (Director) | L2 Approver (GM Developments) |

**Action:** `update_column` on each, change `title` only. Cross-sheet references unaffected (ID-based).

### Task K.4 — Update Cost Band formula to 4-tier matrix

Current Cost Band formula:
```
=IF(ABS([Cost Impact (NZD)]@row) > 25000, "Director Approval Required", "PM Approval Only")
```

New Cost Band formula (4-tier matching KPV approval matrix):
```
=IF(ABS([Cost Impact (NZD)]@row) <= 5000, "Delivery Lead Approval",
  IF(ABS([Cost Impact (NZD)]@row) <= 25000, "GM Developments Approval",
    IF(ABS([Cost Impact (NZD)]@row) <= 50000, "CFO Co-Sign Required",
      "CEO Approval Required")))
```

**Update Required Approval Level formula** to match:
```
=IF([Cost Band]@row = "Delivery Lead Approval", "L1",
  IF([Cost Band]@row = "GM Developments Approval", "L2",
    IF([Cost Band]@row = "CFO Co-Sign Required", "L3",
      "L4")))
```

**Action:**
1. Snapshot current Cost Band and Required Approval Level values per row
2. Update Cost Band column formula via `update_column`
3. Update Required Approval Level column formula
4. Verify all existing rows recalculate correctly against the new tiers

### Task K.5 — Add Cost Category column

New column for variation cost categorisation (root cause analytics).

**Column spec:**
- Name: `Cost Category`
- Type: PICKLIST
- Options: Materials, Labour, Plant, Subcontractor, Design, Other
- Validation: true

**Action:** `add_columns` after Trade Package column.

### Task K.6 — Add Variation Source column

New column for variation root cause tracking.

**Column spec:**
- Name: `Variation Source`
- Type: PICKLIST
- Options: Client Request, Design Change, Site Conditions, Statutory / Consent, Error / Omission, Programme Acceleration, Other
- Validation: true

**Action:** `add_columns` after Cost Category column.

### Task K.7 — UI-only: Form configuration

After API changes complete, Kyle (or designated form editor) updates the Variation Submission form.

**UI checklist for Kyle:**
- [ ] Form opens with Approval Status defaulted to "Draft"
- [ ] Programme Impact (days) marked as optional
- [ ] Cost Category required field
- [ ] Variation Source required field
- [ ] L3 and L4 Approver fields hidden from form (set by automation, not by submitter)
- [ ] L3/L4 Approval Date fields hidden from form
- [ ] Cost Band, Required Approval Level fields hidden (formula-driven)

### Task K.8 — UI-only: Document automation plan (Phase 2.6)

Automations are UI-only and out of scope for Phase 2.5 API execution. Document the automation plan in the brief output so Phase 2.6 can build them.

**Planned automations (Phase 2.6 — UI only):**

| # | Trigger | Condition | Action |
|---|---|---|---|
| 1 | Row added via form | Approval Status = Submitted | Notify Matt (L1 Approver) via email + Teams adaptive card |
| 2 | Approval Status changes to Pricing | — | Notify designated quoter (currently Matt) |
| 3 | Approval Status changes to Pending Approval AND Required Approval Level = L1 | — | Request approval from L1 Approver |
| 4 | Approval Status changes to Pending Approval AND Required Approval Level = L2 | — | After L1 approves: request approval from L2 (Kyle) |
| 5 | Approval Status changes to Pending Approval AND Required Approval Level = L3 | — | Sequential: L1 → L2 → L3 (Julie) |
| 6 | Approval Status changes to Pending Approval AND Required Approval Level = L4 | — | Sequential: L1 → L2 → L3 → L4 (Liam) |
| 7 | Approval Status changes to Approved | — | Notify Matt to set Issued; set Final Approved By + Final Approval Date |
| 8 | Approval Status changes to Rejected | — | Notify Matt + Submitted By with rejection reason; close workflow |
| 9 | Approval Status changes to Issued | — | Notify site team via Teams; mark workflow active |
| 10 | Approval Status changes to Built | — | Notify Matt for closeout |
| 11 | Approval Status changes to Closed | — | Notify Julie (CFO) that variation is settled commercially |
| 12 | Pending Approval > 7 days | — | Escalate: remind approver via Teams; copy Kyle for visibility |
| 13 | Pending Approval > 14 days | — | Auto-escalate to next tier; notify Kyle |

**Architectural notes:**
- Sequential approvals require Smartsheet's native "request an approval" automation OR Power Automate adaptive cards
- Power Automate adaptive cards in Teams are preferred — approvers can approve/reject from Teams chat without opening Smartsheet
- All escalation logic uses Required Approval Level column to drive the routing

### Task K.9 — Verify

Re-fetch Variation Log columns. Confirm:
- 35 columns total (29 original + 4 approval tier columns + Cost Category + Variation Source)
- Approval Status picklist has 9 options matching granular workflow
- Cost Band formula recalculates with new 4-tier logic
- L1 and L2 columns renamed (titles only; column IDs unchanged)
- No existing rows broken; all current variations show correct new Cost Band and Required Approval Level
- Automation plan documented in brief output for Phase 2.6 execution

## Section L — RFQ and Quote Register (sheet ID 5413487898480516)

**Current:** 22 columns. **Target:** 23 columns. Add Quote ID, convert Supplier Name to formula.

### Task L.1 — Add Quote ID column

Add new column `Quote ID`, type TEXT_NUMBER, manual entry initially.

Format convention: `{Parent RFQ ID}-Q{nn}` where nn is the child sequence. E.g. parent `107-RFQ-001` has children `107-RFQ-001-Q01`, `107-RFQ-001-Q02`, etc.

Initially manual entry; formula derivation can be added later if needed.

**Action:** `add_columns` to add Quote ID column after the existing ID column (index 2).

### Task L.2 — UI-only: Convert Supplier Name to cross-sheet formula

Current Supplier Name (col ID `1981890910523268`) is manual TEXT_NUMBER. Convert to formula pulling from Supplier Register via Supplier ID match.

**UI checklist for Kyle:**
- [ ] In RFQ Register, create cross-sheet references to Supplier Register:
  - `SuppR Trading Name` → Trading Name column
  - `SuppR Supplier ID` → Supplier ID column
- [ ] Convert Supplier Name column to formula:
  - `=IF([Type]@row = "Quote", IFERROR(INDEX({SuppR Trading Name}, MATCH([Supplier ID]@row, {SuppR Supplier ID}, 0)), ""), "")`
- [ ] Note: the supplier-facing Quote Submission form will need Supplier ID captured (via URL parameter or supplier knows their ID). Decide approach when building form.

### Task L.3 — Verify

Re-fetch RFQ Register. Confirm 23 columns.

---

## Section M — Contract Register (sheet ID 3948571190579076)

**Current:** 24 columns. **Target:** 22 columns. Cuts, renames, formula conversions.

### Task M.1 — Rename Counterparty columns to Supplier

| Current name | Column ID | New name |
|---|---|---|
| Counterparty Name | `2558877957918596` | Supplier Name |
| Counterparty ID | `7062477585289092` | Supplier ID |

**Pre-flight:** check if any other sheet references these columns by name (cross-sheet references are typically by sheet ID and column ID, so rename is usually safe — but verify).

**Action:** `update_column` on each, change `title` only. All else unchanged.

### Task M.2 — Cut Insurance Verified, Insurance Expiry, H and S Inducted

Insurance-related fields belong on Supplier Register (per-supplier, not per-contract).

| Column | Column ID | Reason |
|---|---|---|
| Insurance Verified | `2418140469563268` | Supplier-level, lives on Supplier Register |
| Insurance Expiry | `6921740096933764` | Supplier-level |
| H and S Inducted | `1292240562720644` | Supplier-level induction tracking, not contract-level |

**Action:** Snapshot values to `/snapshots/107-phase25-{date}/contract-register-cut-insurance.json`. Confirm with Kyle. Delete columns.

### Task M.3 — Add Supplier Insurance Status column

Add new column `Supplier Insurance Status`, type TEXT_NUMBER. Will be formula-driven from Supplier Register (UI-only setup).

**Action:** `add_columns` with placeholder TEXT_NUMBER. Formula added in UI follow-up.

### Task M.4 — UI-only: Convert Supplier Name to cross-sheet formula

Same pattern as RFQ Register Section L.2.

**UI checklist for Kyle:**
- [ ] In Contract Register, create cross-sheet references to Supplier Register (already exist if Section J done — reuse):
  - `SuppR Trading Name`
  - `SuppR Supplier ID`
- [ ] Convert Supplier Name (renamed from Counterparty Name) to formula:
  - `=IFERROR(INDEX({SuppR Trading Name}, MATCH([Supplier ID]@row, {SuppR Supplier ID}, 0)), "")`

### Task M.5 — UI-only: Convert Variations to Date to SUMIFS formula

Phase 2 follow-up: convert manual Variations to Date column to SUMIFS rollup from Variation Log.

**UI checklist for Kyle:**
- [ ] In Contract Register, create cross-sheet references to Variation Log:
  - `VL Cost Impact` → Cost Impact (NZD) column
  - `VL Linked Contract` → Linked Contract column
  - `VL Final Approval Status` → Final Approval Status column
- [ ] Convert Variations to Date (NZD) (col `5373627725025156`) to formula:
  - `=SUMIFS({VL Cost Impact}, {VL Linked Contract}, [Contract ID]@row, {VL Final Approval Status}, "Approved")`

### Task M.6 — UI-only: Add Supplier Insurance Status formula

**UI checklist for Kyle:**
- [ ] Create cross-sheet reference to Supplier Register Insurance Status column: `SuppR Insurance Status`
- [ ] Add formula on Supplier Insurance Status column:
  - `=IFERROR(INDEX({SuppR Insurance Status}, MATCH([Supplier ID]@row, {SuppR Supplier ID}, 0)), "")`

### Task M.7 — Optional: Add Building Reference column for Construction Register pull-back

Per Section J Task J.3 — Construction Register needs to pull Contract Price from Contract Register matched on Building Reference.

If Kyle's contracts are per-building (one contract per building), add a `Building Reference` column to Contract Register so the cross-sheet match works.

If contracts span multiple buildings (one contract for Stages 1-3), the Stages Covered multi-picklist handles it but Construction Register's pull becomes harder (would need a sum across contracts touching the building).

**Action:** Discuss with Kyle at execution time. Defer if unclear.

### Task M.8 — Verify

Re-fetch Contract Register. Confirm 22 columns. Confirm renames executed.

---

## Section N — H and S Incidents and Observations (sheet ID 8305827340308356)

**Current:** 14 columns. **Target:** 14 columns. Picklist deduplication only.

### Task N.1 — Deduplicate Type picklist

Current Type picklist (col ID `5732978469932932`) options: Near Miss - Minor, Near Miss - Serious (PSIF), MTI, LTI, **Lost Time Injury**, Observation, Other.

"Lost Time Injury" duplicates "LTI". Remove "Lost Time Injury", keep "LTI".

**Pre-flight:**
1. Check if any rows currently use "Lost Time Injury" as the Type value
2. If yes, **STOP and report.** Kyle must reassign those rows to "LTI" before the picklist option can be removed

**Action (after no-use confirmation):**
1. Get Kyle's explicit confirmation
2. `update_column` on col `5732978469932932`: options array without "Lost Time Injury"
3. Final options: Near Miss - Minor, Near Miss - Serious (PSIF), MTI, LTI, Observation, Other (6 options)

### Task N.2 — Parked decision (no action)

Entry ID currently manual. Defer AUTO_NUMBER conversion until 6-month review.

**Document in conventions:**
- Add to `kpv-conventions.md` parked decisions: H&S Entry ID AUTO_NUMBER conversion — review November 2026

### Task N.3 — Verify

Re-fetch H&S Incidents. Confirm 14 columns and 6-option Type picklist.

---

## Section O — H and S Monthly Indicators (sheet ID 3104570405244804)

**Current:** 19 columns. **Target:** 19 columns. Composition change — incident counts become COUNTIFS formulas.

### Task O.1 — UI-only: Convert Near Miss / MTI / LTI to COUNTIFS formulas

These columns currently hold manual count values. Convert to cross-sheet formulas reading from Incidents sheet.

**UI checklist for Kyle:**
- [ ] In Monthly Indicators, create cross-sheet references to H&S Incidents and Observations (sheet ID `8305827340308356`):
  - `INC Type` → Type column
  - `INC Date Identified` → Date Identified column
- [ ] Convert these columns to formulas. The period boundaries (Period Start and Period End on Monthly Indicators) define the date range:
  - **Near Miss Minor** (col `2936391582650244`): `=COUNTIFS({INC Type}, "Near Miss - Minor", {INC Date Identified}, @cell >= [Period Start]@row, {INC Date Identified}, @cell <= [Period End]@row)`
  - **Near Miss Serious PSIF** (col `7439991210020740`): `=COUNTIFS({INC Type}, "Near Miss - Serious (PSIF)", {INC Date Identified}, @cell >= [Period Start]@row, {INC Date Identified}, @cell <= [Period End]@row)`
  - **MTI** (col `1810491675807620`): `=COUNTIFS({INC Type}, "MTI", {INC Date Identified}, @cell >= [Period Start]@row, {INC Date Identified}, @cell <= [Period End]@row)`
  - **LTI** (col `6314091303178116`): `=COUNTIFS({INC Type}, "LTI", {INC Date Identified}, @cell >= [Period Start]@row, {INC Date Identified}, @cell <= [Period End]@row)`
- [ ] Verify counts match what's currently manually entered

### Task O.2 — Discipline note: Contractor picklist must match Supplier Register

Current Contractor picklist hardcoded with 9 contractor values. Kept hardcoded (small known set).

**Discipline rule:** picklist values must match Supplier Register canonical Trading Names exactly. Spelling drift causes silent reporting mismatches.

**Conventions update:**
- Add to `kpv-conventions.md` §7 (Sheets and registers): when adding contractors to the Monthly Indicators Contractor picklist, the spelling must exactly match the Trading Name on Supplier Register

### Task O.3 — Verify

After UI follow-ups, verify all 4 incident count columns are formula-driven and produce correct counts.

---

## Section P — Chart Sources (4 sheets, sheet IDs 2191119310868356, 4094966644035460, 7953427823808388, 1171511254667140)

**Current:** 18 total columns across 4 sheets. **Target:** unchanged.

### Task P.1 — Verify Construction Progress Chart Source formula

Construction Progress Chart Source (sheet ID `4094966644035460`) has a formula referencing a cross-sheet range named `{Construction Programme Is Unit}`. Construction Programme does not have a column named "Is Unit" — only Units, Unit Count, Building Group.

**Action:**
1. In the UI, click into the Construction Progress Chart Source formula
2. Click Edit Reference on `{Construction Programme Is Unit}`
3. Confirm which column on Construction Programme this actually points to
4. If the named range is broken (no column attached), the formula is currently returning 0 or error — flag to Kyle for repair
5. If the named range points to a valid but misleadingly named column, document that — leave as-is unless Kyle wants to rename

**Document outcome** in the final report.

### Task P.2 — No other changes

Other three Chart Sources are well-formed and left alone.

---

## Section Q — Update conventions and inventory

### Task Q.1 — Update kpv-conventions.md

Add the following to `/mnt/project/kpv-conventions.md`:

**Section 5 (SharePoint and Smartsheet folder structure) — update:**

Add new 7-folder pattern for villages, replacing previous 4-folder pattern. Include rationale: separate audiences served (Project Control / Sales / Procurement / Civil and Construction / Health and Safety / Reports), procurement before construction in lifecycle order.

**Section 7 (Sheets and registers) — additions:**

- Document the renamed sheet: PCG Status Snapshot → Monthly RAG Log
- Note Civil Programme uses different Stage picklist (no sub-stages) — deliberate
- Note Monthly Indicators Contractor picklist must match Supplier Register Trading Names exactly
- Add "shared reference layer" framing to Project Control folder: it contains the Unit Register (master reference for everyone) plus governance artefacts (Risk Register, Decision Log, Monthly RAG Log)

**New §10 (Sheet design rules):**

Add the seven architectural principles from this brief's preamble. These now govern all future sheet changes.

**Section 10 (parked decisions):**

- H&S Entry ID AUTO_NUMBER conversion — review November 2026
- Trade Package picklist conversion — review November 2026 (was already parked from Phase 2)
- Cost Band threshold parameterisation — review when volume justifies
- H&S vs HS vs "H and S" naming divergence — accepted; revisit if cross-category filter needed
- AUTO_NUMBER shared sequence on RFQ Register parent/child — added separate Quote ID column in Section L

### Task Q.2 — Update kpv-smartsheet-inventory.md

Full refresh:
- New folder structure (7 folders)
- New folder IDs
- Sheet rename (PCG Status Snapshot → Monthly RAG Log)
- New columns added (Risk Register Date Identified, RFQ Register Quote ID, Contract Register Supplier Insurance Status)
- Columns removed (Unit Register 4 cuts, PCG Status Snapshot 17 cuts, Construction Programme 7 cuts, Civil Programme 6 cuts, Contract Register 3 cuts)
- Column renames (Contract Register Counterparty → Supplier)

### Task Q.3 — Update smartsheet/sheet-registry.md

Refresh column ID maps for every modified sheet.

---

## Section T — Naming convention retrofits

Apply locked naming conventions from `kpv-naming-conventions.md` to any existing data that diverges.

### Task T.1 — Audit AUTO_NUMBER sequences for 4-digit format

Per locked convention: all AUTO_NUMBER sequences use 4-digit padding (`107-VAR-0001`).

Check existing AUTO_NUMBER configurations on:
- Variation Log (already 4-digit per Phase 2 build)
- Risk Register (already 4-digit)
- Decision Log (verify — likely 3-digit, needs update)
- RFQ Register (verify — likely 3-digit, needs update)
- Contract Register (verify — likely 3-digit, needs update)

**For each sheet found with 3-digit sequences:**
1. Snapshot existing IDs
2. Get Kyle's explicit confirmation
3. Use `update_column` on the AUTO_NUMBER column to change the format to 4 digits
4. **IMPORTANT:** Smartsheet's AUTO_NUMBER format change does NOT retroactively renumber existing rows. Existing rows keep their 3-digit IDs; new rows use 4-digit. Document this in the final report.
5. If Kyle wants existing IDs renumbered to 4 digits, this requires manual UI work per row (out of scope for Phase 2.5 API execution — flag as UI follow-up if needed)

### Task T.2 — Audit picklist values for "Amber" vs "Yellow"

Per locked convention: RAG picklists use `Yellow` not `Amber`.

Scan all RAG picklists across the 13 sheets. Where `Amber` is found:
1. Snapshot picklist values
2. Get Kyle's confirmation
3. Check if any rows currently use `Amber` (would need rewriting to `Yellow` before picklist option removal)
4. Update picklist to use `Yellow` consistently

### Task T.3 — Audit picklist values for case consistency

Per locked convention: Title Case throughout. Scan all picklists for mixed casing within a single picklist (`In Progress` vs `In progress`). Flag any found; do not silently rewrite — get Kyle's confirmation per inconsistency.

### Task T.4 — Verify

Output a structured list of any divergences found and corrections made. Include in the Final Report.

---



Produce a structured summary covering:

1. **What was done** — sheet-by-sheet list of API changes with column IDs.
2. **Column count summary** — confirm against target totals:
   - Unit Register: 22 → 18
   - Sales Register: 16 → 16 (composition change)
   - Risk Register: 13 → 14
   - Monthly RAG Log (renamed): 29 → 12
   - Decision Log: 13 → 13 (no change)
   - Construction Programme: 24 → 17
   - Civil Programme: 19 → 13
   - Construction Register: 19 → 19 (composition change)
   - Variation Log: 29 → 35
   - RFQ and Quote Register: 22 → 23
   - Contract Register: 24 → 22
   - H&S Incidents and Observations: 14 → 14 (picklist only)
   - H&S Monthly Indicators: 19 → 19 (composition change)
   - Chart Sources (4 sheets): 18 → 18 (verify only)
   - **Total: 281 → 251 columns** (net 30 removed, 6 added on Variation Log, 13% reduction)
3. **What's pending UI action** — consolidated checklist of all UI items from Sections A-Q. Group by sheet so Kyle can work one sheet at a time. Include all cross-sheet reference setups, formula conversions, form configurations.
4. **Variation Log automation plan** — confirm the 13 automations documented in Task K.8 are captured in the output for Phase 2.6 execution.
5. **Snapshots taken** — list all snapshot files with paths.
6. **Decisions Kyle must still make** — any items that surfaced during execution (e.g. Construction Register Build Partner match key, Contract Register per-building or per-stage decision).
7. **Inventory and conventions updated** — confirm both files current.
8. **Phase 3 readiness check** — is 107 ready to snapshot to XXX Village Template? Specifically:
   - All API changes done ✓
   - All UI follow-ups done? (yes/no)
   - All decisions resolved? (yes/no)
   - Test data cleaned out (no stray test rows)
   - Folder structure matches target
9. **Estimated UI workload remaining** — sum of UI checklist items, organised by complexity.

---

## Phase 2.5 NOT in scope

Deliberately out of scope. Do not start:

- Snapshotting 107 to XXX Village Template (Phase 3)
- Touching 105 or 106 workspaces (Phase 4)
- Modifying any reports or dashboards (UI-only and out of scope for this brief — covered separately when needed)
- Building Power Automate flows
- Building any monthly Claude Code workflow (Phase 5)
- Adding any new sheets beyond those discussed
- Migrating any historic data between sheets (variation history from email, etc.)
- Touching the Typology Register at portfolio level (read-only reference from 107)
- Touching the Supplier Register at portfolio level (read-only reference from 107)
- Repairing the misfiled "104 - Sale Variance Watch" report in the 105 workspace (Phase 4 cleanup)

---

## Decision log for this brief

All decisions Kyle made during the May 2026 sheet-by-sheet conversation are encoded in this brief. Key calls:

- **Folder structure**: 7 folders, procurement before construction
- **Unit Register**: cut Beds/Garage/Floor Area/Attachment to Typology Register pull; expand Sales Status picklist; Sales Status formula (Phase 1 carryover)
- **Sales Register**: expand picklist (add Conditional, Transfer, Occupied)
- **Risk Register**: Score and RAG become formulas; add Date Identified
- **Monthly RAG Log** (renamed from PCG Status Snapshot): strip to 12 columns
- **Decision Log**: no change
- **Construction Programme**: cut 7 financial/supplier columns; Construction Status stays canonical here
- **Civil Programme**: cut 6 financial/supplier columns; Stage picklist deliberate divergence documented
- **Construction Register**: Option C financials (Contract Price + Variations become formulas); Build Partner becomes Supplier Register formula
- **Variation Log**: granular 9-state workflow; 4-tier approval matrix (Matt $5k → Kyle $25k → Julie $50k → Liam); add Cost Category and Variation Source columns; rename L1/L2 columns to match KPV roles; document 13 automations for Phase 2.6 build
- **RFQ Register**: add Quote ID; Supplier Name becomes formula
- **Contract Register**: rename Counterparty → Supplier; drop Insurance/H&S Inducted; add Supplier Insurance Status; Variations to Date SUMIFS formula
- **H&S Incidents**: dedupe Type picklist (remove "Lost Time Injury")
- **H&S Monthly Indicators**: incident counts become COUNTIFS formulas
- **Chart Sources**: verify Construction Progress formula only

---

End of Phase 2.5 brief.
