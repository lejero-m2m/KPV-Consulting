# Village 105 (Rototuna) — Phase 4 Rollout Complete

**Generated:** 2026-05-23
**Workspace:** 105 - Rototuna (`2189930039404420`)
**Status:** ✅ API phases (A–E) complete. Awaiting Phase F UI work (Kyle).

---

## Workspace structure

- Total top-level folders: **7** ✓
- Total sheets created: **17** ✓

| Folder | Folder ID |
|---|---|
| 00 - Dashboards | `413889583179652` |
| 00 - Dashboards / Chart Sources | `8631639489177476` |
| 01 - Project Control | `5071420838438788` |
| 02 - Sales | `3593677210707844` |
| 03 - Procurement | `954849304045444` |
| 04 - Civil and Construction | `8836148651943812` |
| 05 - Health and Safety | `5651962977904516` |
| 06 - Reports | `3892744373462916` |
| 06 - Reports / Internal | `8473309814777732` |
| 06 - Reports / External | `8895522279843716` |

---

## Sheets created

| Sheet | Sheet ID | Rows | AUTO_NUMBER |
|---|---|---|---|
| 105 - Unit Register | `12767045046148` | 142 | — |
| 105 - Construction Register | `264203020488580` | 0 (deferred) | — |
| 105 - Civil Programme | `5604571798785924` | 41 | — |
| 105 - Construction Programme | `128413334458244` | 301 | — |
| 105 - RFQ and Quote Register | `7554171271073668` | 0 | `105-RFQ-0001` |
| 105 - Variation Log | `8643581135769476` | 0 | `105-VAR-0001` |
| 105 - Contract Register | `3568901181886340` | 38 | `105-CON-0001` |
| 105 - Sales Register | `2821136101363588` | 0 | — |
| 105 - Risk Register | `2264566858731396` | 0 | `105-RSK-0001` |
| 105 - Decision Log | `8599007965171588` | 0 | `105-DEC-0001` |
| 105 - Monthly RAG Log | `335808715247492` | 0 | — |
| 105 - H and S Incidents and Observations | `4767802647859076` | 0 | `105-HSE-0001` |
| 105 - H and S Monthly Indicators | `174669595365252` | 0 | — |
| 105 - Chart Source - Application Strength | `2380247507881860` | 4 | — |
| 105 - Chart Source - Construction Progress | `8770617141579652` | 4 | — |
| 105 - Chart Source - Sales Pipeline | `6983082354626436` | 5 | — |
| 105 - Chart Source - Typology Sales | `4839408342617988` | 4 | — |

**Row total: 539 rows imported across 17 sheets.**

---

## Formulas applied

- 38 column formulas verified inherited from 107 verbatim. 0 drift.
- Village column on Decision Log + Risk Register correctly set to `="105"`.
- Cross-sheet formulas show `#REF` until Phase F.1 UI work.

---

## Picklists customised

- **Main Stage picklist** (4 options): Stage 1, Stage 2, Stage 3, Stage 4 — applied to UR, CP, VL, RFQ, RR, Contract Register.
- **Civil Programme Stage picklist** (5 options): Stage 1, Stage 2, Stage 2-3, Stage 3, Stage 4 — note `Stage 2-3` combined stage per `105 - Civil Programme.xlsx`.
- **Building Reference picklist:** DEFERRED — source XLSX has no Building Reference column. Kyle to populate via UI.

---

## Data populated

| Sheet | Rows | Source XLSX | Headers matched |
|---|---:|---|---|
| 105 - Unit Register | 142 | 105 - Unit Register (1).xlsx | 13/39 |
| 105 - Civil Programme | 41 | 105 - Civil Programme.xlsx | 17/19 |
| 105 - Construction Programme | 301 | 105 - Construction Programme.xlsx | 11/17 (overrideValidation needed) |
| 105 - Contract Register | 38 | 105-Rototuna-Build-Contracts.xlsx | 14/19 |
| 105 - Chart Source × 4 | 17 | (seed from 107) | — |

---

## Anomalies

1. **Source data Stage values diverge from UR-derived picklist** — Construction Programme XLSX had values like "Stage 1 - Construction", "60", "61"... Picklist set to clean 4-state, source values land as orphans (overrideValidation bypassed strict checking). Kyle to reconcile.
2. Construction Register, Sales Register, Risk Register, Decision Log, Monthly RAG Log, H&S sheets all empty (no source data files for 105).
3. Contract Register Supplier ID blank on all 38 rows.
4. Building Reference picklist inherited from 107 (wrong for 105).
5. Cross-sheet references show `#REF` until Phase F.1.

---

## Kyle's next steps (Phase F UI work)

Same per-village checklist as 104 — see `phase4-village-104-complete.md` §"Kyle's next steps".
