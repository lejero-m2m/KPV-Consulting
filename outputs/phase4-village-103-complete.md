# Village 103 (Rolleston, Woodcroft Estate) — Rollout Complete

**Generated:** 2026-05-23
**Workspace:** `103 - Rolleston` (ID `2542728585209732`)
**Status:** ✅ Structural shell complete. No data populated (out of scope per brief §0). Awaiting Phase F UI work.

---

## Workspace structure

- **Total top-level folders:** 7 ✓
- **Total sub-folders:** 4 (Chart Sources, Internal, External, **Archive**)
- **Total sheets created:** 17 ✓ (matches 104/105/106 — Resource Consent Register skipped per Phase 4 Decision 1, see deviations below)

| Folder | Folder ID |
|---|---|
| 00 - Dashboards | `6775045386200964` |
| 00 - Dashboards / Chart Sources | `1814048921675652` |
| 01 - Project Control | `3960295619094404` |
| 02 - Sales | `5226933014292356` |
| 03 - Procurement | `6282464176957316` |
| 04 - Civil and Construction | `1075177107810180` |
| 04 - Civil and Construction / Archive | `3951499526072196` ← **per brief, not in 104/105/106** |
| 05 - Health and Safety | `3995479991183236` |
| 06 - Reports | `3291792549406596` |
| 06 - Reports / Internal | `1673311433320324` |
| 06 - Reports / External | `1136749758965636` |

---

## Sheets created

| Sheet | Sheet ID | AUTO_NUMBER |
|---|---|---|
| 103 - Unit Register | `471418012651396` | — |
| 103 - Construction Register | `877296717090692` | — |
| 103 - Civil Programme | `1541949348597636` | — |
| 103 - Construction Programme | `5380896344461188` | — |
| 103 - RFQ and Quote Register | `3137795450163076` | `103-RFQ-0001` |
| 103 - Variation Log | `2877782961901444` | `103-VAR-0001` |
| 103 - Contract Register | `8056162753662852` | `103-CON-0001` |
| 103 - Sales Register | `8654103268773764` | — |
| 103 - Risk Register | `3425651137662852` | `103-RSK-0001` (Village formula `="103"`) |
| 103 - Decision Log | `7965766576983940` | `103-DEC-0001` (Village formula `="103"`) |
| 103 - Monthly RAG Log | `6173841796583300` | — |
| 103 - H and S Incidents and Observations | `491328944164740` | `103-HSE-0001` |
| 103 - H and S Monthly Indicators | `3922041982898052` | — |
| 103 - Chart Source - Application Strength | `647417182506884` | — |
| 103 - Chart Source - Construction Progress | `7929250765033348` | — |
| 103 - Chart Source - Sales Pipeline | `7226817453707140` | — |
| 103 - Chart Source - Typology Sales | `642701308415876` | — |

All sheets are **empty** (cloned with `?include=filters,forms` — no row data).

---

## Portfolio Register row

Added row to `000 - Portfolio Register` (sheet `4900490847408004`), new row ID `1240572914237316`:

| Field | Value |
|---|---|
| Village Code | 103 |
| Region | CAN |
| Operating Status | Pre-development |
| Notes | Structural shell created 2026-05-23; masterplan staging pending; full operating-model configuration (forms, automations, dashboards) deferred to Kyle's Phase F UI work. |

**Note:** Portfolio Register doesn't have a "Village Name" column (or it's locked/formula). "Woodcroft Estate" not recorded — Kyle may want to add a Village Name column or put it in Notes / a different field. Spot-check the Portfolio Register schema in UI.

---

## Brief deviations (intentional)

1. **Resource Consent Register skipped.** Brief §3 lists it with source ID `1643703515959172` which has been 404 since Phase 1 deletion (Decision 1, Phase 4). Skipping matches 104/105/106 pattern → 17 sheets, not 19. Same deferral applies: if Kyle later wants Resource Consent Register on 103, clone from XXX Village Template (`3572291202928516`).
2. **Folder named `02 - Sales`** not `02 - Sales and Marketing`. Aligns with 107 + 104/105/106. The brief's name is inconsistent with current portfolio convention.
3. **Sheet named `103 - Monthly RAG Log`** not `103 - PCG Status Snapshot`. 107 sheet was renamed in Phase 2.5 v2; brief's old name is stale.

## Brief honoured verbatim

- **Archive sub-folder** created under `04 - Civil and Construction` (104/105/106 don't have this; was explicitly requested for 103).
- Linked Stage / Building Reference picklists left untouched (inherit 107 values) — masterplan not yet locked per brief §4.
- No data populated.

---

## Formulas

Inherited from 107 verbatim — verified in Phase 4 (114 formulas across the 3 sister villages all matched 107 with 0 drift). 103 inherits the same pattern.

- Village column: set to `="103"` on Decision Log + Risk Register
- All cross-sheet formulas show `#REF` until Kyle creates village-scoped references in UI

---

## Outstanding for Kyle (Phase F)

Same per-village checklist as 104/105/106 — see `outputs/phase4-village-104-complete.md` for the full list. 103-specific additions:

1. **Populate Linked Stage / Stage / Building Reference picklists** once Rolleston masterplan is locked.
2. **Add 103 - Decision Log + 103 - Risk Register as 5th source sheets** to the Master Decision Register + Master Risk Register reports (when created).
3. **Add 4th Power Automate flow** for 103 Variation → Decision Log auto-create.
4. **Spot-check Portfolio Register row** for 103 — confirm Village Name field state and any other columns I couldn't populate.
5. **Configure forms, reports, dashboards, automations** per Phase 4 brief §7.

Estimated UI workload: ~3-4 hours (same as 104/105/106) plus the masterplan-dependent picklist work (~30 min when masterplan ready).
