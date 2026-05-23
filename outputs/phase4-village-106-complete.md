# Village 106 (Waihi Beach) — Phase 4 Rollout Complete

**Generated:** 2026-05-23
**Workspace:** 106 - Waihi Beach (`1169583248828292`)
**Status:** ✅ API phases (A–E) complete. Awaiting Phase F UI work (Kyle).

---

## Workspace structure

- Total top-level folders: **7** ✓
- Total sheets created: **17** ✓

| Folder | Folder ID |
|---|---|
| 00 - Dashboards | `2802028838709124` |
| 00 - Dashboards / Chart Sources | `3054916513097604` |
| 01 - Project Control | `5713535629059972` |
| 02 - Sales | `330326699468676` |
| 03 - Procurement | `8141257303189380` |
| 04 - Civil and Construction | `1790478141155204` |
| 05 - Health and Safety | `1333081304000388` |
| 06 - Reports | `8369955721766788` |
| 06 - Reports / Internal | `5271531954694020` |
| 06 - Reports / External | `1401251024922500` |

---

## Sheets created

| Sheet | Sheet ID | Rows | AUTO_NUMBER |
|---|---|---|---|
| 106 - Unit Register | `1813612472520580` | 105 | — |
| 106 - Construction Register | `409888311168900` | 0 (deferred) | — |
| 106 - Civil Programme | `8848354439024516` | 24 | — |
| 106 - Construction Programme | `6317212099891076` | 101 | — |
| 106 - RFQ and Quote Register | `968156750237572` | 0 | `106-RFQ-0001` |
| 106 - Variation Log | `3708779676782468` | 0 | `106-VAR-0001` |
| 106 - Contract Register | `2125083500826500` | 24 | `106-CON-0001` |
| 106 - Sales Register | `6146796387520388` | 0 | — |
| 106 - Risk Register | `6367119082999684` | 0 | `106-RSK-0001` |
| 106 - Decision Log | `3288680335626116` | 0 | `106-DEC-0001` |
| 106 - Monthly RAG Log | `3894996573835140` | 0 | — |
| 106 - H and S Incidents and Observations | `850811264388996` | 0 | `106-HSE-0001` |
| 106 - H and S Monthly Indicators | `472676438069124` | 0 | — |
| 106 - Chart Source - Application Strength | `7699214464143236` | 4 | — |
| 106 - Chart Source - Construction Progress | `2162780428783492` | 4 | — |
| 106 - Chart Source - Sales Pipeline | `2546041835442052` | 5 | — |
| 106 - Chart Source - Typology Sales | `8572696995516292` | 4 | — |

**Row total: 271 rows imported across 17 sheets.**

---

## Formulas applied

- 38 column formulas verified inherited from 107 verbatim. 0 drift.
- Village column on Decision Log + Risk Register correctly set to `="106"`.
- Cross-sheet formulas show `#REF` until Phase F.1 UI work.

---

## Picklists customised

- **Main Stage picklist** (5 options): Stage 1, Stage 1A, Stage 1B, Stage 2, Stage 3 — note 1A/1B sub-stage split per `106 - Unit Register (1).xlsx`.
- **Civil Programme Stage picklist** (3 options): Stage 1, Stage 1A, Stage 1B — civils only cover Stage 1 sub-stages.
- **Building Reference picklist:** DEFERRED. Note per `kpv-naming-conventions.md` §4 — 106 uses synthetic `S{Stage}-{Block}-{Unit}` identifiers (e.g. `S5-216-1` for Stanaway/Clarence blocks). Construction Register Stage formula `=IFERROR("Stage " + MID(...))` should parse this correctly, but to be verified once Kyle populates real values.

---

## Data populated

| Sheet | Rows | Source XLSX | Headers matched |
|---|---:|---|---|
| 106 - Unit Register | 105 | 106 - Unit Register (1).xlsx | 13/39 |
| 106 - Civil Programme | 24 | 106 - Civil Programme.xlsx | 17/19 |
| 106 - Construction Programme | 101 | 106 - Construction Programme.xlsx | 11/17 (overrideValidation needed) |
| 106 - Contract Register | 24 | 106-Waihi-Beach-Build-Contracts.xlsx | 14/19 |
| 106 - Chart Source × 4 | 17 | (seed from 107) | — |

---

## Anomalies

1. **Construction Programme imported via overrideValidation** — Kyle to reconcile orphaned PICKLIST values.
2. Sales / Risk / Decision / MRL / H&S all empty (no source data).
3. Contract Register Supplier ID blank on all 24 rows.
4. Building Reference picklist inherited from 107 (wrong for 106).
5. **Synthetic Building Reference IDs** (`S5-216-1`) flagged per kpv-naming-conventions §4 — needs verification post-population that Construction Register's `Stage` formula handles them correctly.
6. Cross-sheet references show `#REF` until Phase F.1.

---

## Kyle's next steps (Phase F UI work)

Same per-village checklist as 104 — see `phase4-village-104-complete.md` §"Kyle's next steps".

Extra item for 106: verify Construction Register `Stage` formula behaviour on synthetic `S5-216-1` IDs (likely returns "Stage 5" correctly, but worth checking on first populated row).
