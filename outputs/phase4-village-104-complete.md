# Village 104 (Drury) — Phase 4 Rollout Complete

**Generated:** 2026-05-23
**Workspace:** 104 - Drury - KLE (`5737366867470212`)
**Status:** ✅ API phases (A–E) complete. Awaiting Phase F UI work (Kyle).

---

## Workspace structure

- Total top-level folders: **7** ✓
- Sub-folders: Chart Sources (in 00), Internal + External (in 06)
- Total sheets created: **17** ✓ (Resource Consent Register excluded per Decision 1)

| Folder | Folder ID | Contents |
|---|---|---|
| 00 - Dashboards | `3853161954862980` | (Chart Sources sub-folder + 4 chart source sheets) |
| 00 - Dashboards / Chart Sources | `5333104605849476` | 4 sheets (App Strength, Construction Progress, Sales Pipeline, Typology Sales) |
| 01 - Project Control | `6483193768503172` | Unit Register, Risk Register, Decision Log, Monthly RAG Log |
| 02 - Sales | `7116512466102148` | Sales Register |
| 03 - Procurement | `6377640652236676` | RFQ Register, Contract Register, Variation Log |
| 04 - Civil and Construction | `3070309675886468` | Civil Programme, Construction Programme, Construction Register |
| 05 - Health and Safety | `6360048466192260` | H&S Incidents, H&S Monthly Indicators |
| 06 - Reports | `7661870233479044` | (Internal + External sub-folders, empty awaiting reports) |
| 06 - Reports / Internal | `4515067954784132` | empty (Phase F) |
| 06 - Reports / External | `6274286559225732` | empty (Phase F) |

---

## Sheets created

| Sheet | Sheet ID | Rows | AUTO_NUMBER | Notes |
|---|---|---|---|---|
| 104 - Unit Register | `4980205960515460` | 286 | — | populated from `104 - Unit Register (2).xlsx` |
| 104 - Construction Register | `3927028439928708` | 0 | — | DEFERRED to Kyle (manual entry; brief 5.3 derivation requires Building Reference not present in source XLSX) |
| 104 - Civil Programme | `2451131648135044` | 26 | — | populated from `104 - Civil Programme.xlsx` |
| 104 - Construction Programme | `7574896635760516` | 285 | — | populated from `104 - Construction Programme.xlsx` (required `overrideValidation=true` for PICKLIST values not in destination list — Kyle to reconcile picklists) |
| 104 - RFQ and Quote Register | `7087338390769540` | 0 | `104-RFQ-0001` | source XLSX has incompatible schema; deferred (per Phase D plan) |
| 104 - Variation Log | `8478181408329604` | 0 | `104-VAR-0001` | source XLSX header-only |
| 104 - Contract Register | `4829967467630468` | 78 | `104-CON-0001` | populated from `104-Drury-Build-Contracts.xlsx`; Supplier ID left blank for Kyle's manual assignment |
| 104 - Sales Register | `5189179741785988` | 0 | — | no source data |
| 104 - Risk Register | `3994983412486020` | 0 | `104-RSK-0001` | re-cloned 2026-05-23 from updated 107 (post-§6.7 spec); empty |
| 104 - Decision Log | `473930568519556` | 0 | `104-DEC-0001` | re-cloned 2026-05-23 from updated 107 (post-§6.5 spec); empty |
| 104 - Monthly RAG Log | `5543155913936772` | 0 | — | empty |
| 104 - H and S Incidents and Observations | `3291356100251524` | 0 | `104-HSE-0001` | empty |
| 104 - H and S Monthly Indicators | `2578167653945220` | 0 | — | empty |
| 104 - Chart Source - Application Strength | `6954731275505540` | 4 | — | seed rows copied from 107 |
| 104 - Chart Source - Construction Progress | `2937379928100740` | 4 | — | seed rows copied from 107 |
| 104 - Chart Source - Sales Pipeline | `6748591635779460` | 5 | — | seed rows copied from 107 |
| 104 - Chart Source - Typology Sales | `1606191321927556` | 4 | — | seed rows copied from 107 |

**Row total: 692 rows imported across 17 sheets.**

---

## Formulas applied

- 38 column formulas verified across 8 sheets (Unit Register 7, Construction Register 9, Civil Programme 2, Construction Programme 1, RFQ Register 1, Variation Log 2, Contract Register 4, Sales Register 7, Risk Register 3, Decision Log 1, Monthly RAG Log 1).
- All match 107 source verbatim (audit: `outputs/phase4-formula-audit.json` — 0 missing, 0 differing).
- Village column on Decision Log + Risk Register correctly set to `="104"`.
- **Cross-sheet formulas show `#REF` until Kyle creates village-scoped references in UI** (Phase F.1, ~45 min).

---

## Picklists customised

**Stage values applied** (per village masterplan — extracted from `104 - Unit Register (2).xlsx`):

- **Main Stage picklist** (8 options): Stage 1, Stage 2A, Stage 2B, Stage 2C, Stage 3A, Stage 3B, Stage 3C, Clubhouse — applied to Unit Register, Construction Programme, Variation Log Linked Stage, RFQ Register Linked Stage, Risk Register Linked Stage, Contract Register Stages Covered (MULTI_PICKLIST).
- **Civil Programme Stage picklist** (5 options): Stage 1, Stage 2A, Stage 3A, Stage 3B/3C, Clubhouse — village-specific civils decomposition per `104 - Civil Programme.xlsx`.

**Building Reference picklist:** Phase 4 DEFERRED. Source XLSX files don't include a Building Reference column. Picklist values remain inherited from 107 (`S1-B01` etc.) which are wrong for 104. Kyle to populate via UI with village masterplan building references.

---

## Data populated

| Sheet | Rows | Source XLSX | Headers matched | Source cols dropped |
|---|---:|---|---|---|
| 104 - Unit Register | 286 | 104 - Unit Register (2).xlsx | 13/39 | 26 source cols not in destination (Build Partner, Contract Price, Construction Budget Price, Sale Price variants, CCC Received, Master Build Certificate, etc.) — these were Phase 2.5 cuts on 107; data won't land |
| 104 - Civil Programme | 26 | 104 - Civil Programme.xlsx | 16/19 | Sub-Phase, Budget Variance, Total Cost dropped (formula-derived on dest) |
| 104 - Construction Programme | 285 | 104 - Construction Programme.xlsx | 11/17 | Task Name, Is Unit, Build Partner, Building Consent Number, Contract Price, Variations dropped — all Phase 2.5 cuts on 107 |
| 104 - Contract Register | 78 | 104-Drury-Build-Contracts.xlsx | 14/19 | Contract ID (AUTO_NUMBER), Supplier Name (formula), Variations to Date (formula), Current Contract Value (formula), Documents dropped |
| 104 - Chart Source × 4 | 17 | (seed from 107) | — | — |

---

## Anomalies

1. **Construction Status PICKLIST validation failures** on Construction Programme + Contract Register imports — source data had values not in the locked 5-state Construction Status (e.g. "Practical Completion", "Civil Works" — Phase 2.5 cut these). Resolved with `overrideValidation=true` on retry. **Kyle should sweep these columns in UI** and either: (a) update orphaned cell values to the 5-state set, or (b) re-add the historical values to the picklist if operationally needed.
2. **Construction Register row deferral.** Brief 5.3 says "derive from Unit Register" by grouping by Building Reference, but the source XLSX has no Building Reference column. Manual entry by Kyle recommended after Building Reference picklist is populated.
3. **Contract Register Supplier ID is BLANK** on all 78 rows. Brief 5.4 suggested hardcoding `SUP-0001` (Signature Homes BOP) — I chose to leave blank rather than introduce wrong data. Kyle to assign Supplier IDs against `000 - Supplier Register`.
4. **Building Reference picklist inherited from 107** (S1-B01..S5-B08) — wrong for 104. Kyle to replace with 104 masterplan building references via UI.
5. **Cross-sheet references show `#REF`** on all formula columns — EXPECTED until Phase F.1 UI work.

---

## Kyle's next steps (Phase F UI work, ~3–4 hours)

1. **Cross-sheet references** (~45 min) — create village-scoped references on each formula-using sheet per the matrix in brief §7.1.
2. **Picklist reconciliation** (~30 min) — Construction Status orphans + Building Reference values.
3. **Construction Register population** (~30 min) — one row per building with comma-separated unit numbers and Building Reference.
4. **Contract Register Supplier ID assignment** (~15 min) — match 78 contracts to canonical Supplier IDs.
5. **Forms** — Variation Log, H&S Incidents, Decision Log forms.
6. **Reports** — PCG Report Set, Internal, External.
7. **Dashboards** — 104 - Dashboard + 104 - PCG Dashboard.
8. **Conditional formatting** per sheet.
9. **Power Automate flow** — Variation Approved → Decision Log auto-create (per brief §6.5).
