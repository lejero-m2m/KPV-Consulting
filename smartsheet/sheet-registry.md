# KPV Smartsheet Registry

**Last updated:** 2026-05-23 (Phase 4 multi-village rollout — 104/105/106 cloned from 107 template with 1502 rows imported; central `000 - Project Reference Picklists` register seeded with 62 rows; **103 Rolleston** workspace + 17-sheet structural shell added later same day — empty, awaiting masterplan; **100/101/102 operational villages** rolled out from `XXX - Village Template` with 6 sheets each + 7-folder flat layout; Approx Build Year + Year of Refurbishment cols added to 100/101/102/103 Unit Registers; 200 unit rows inserted from JLL XLSX + 77 103 rows updated). IDs change — re-audit each session per brief Section 3.

---

## Account

| Field | Detail |
|-------|--------|
| Account | KPV's own Smartsheet account |
| Region | **North America** — web app `app.smartsheet.com`, API `api.smartsheet.com` (the `.au` host is not used; confirmed 2026-05-22) |
| Working API token | `smartsheet/input/Smartsheet API.txt` (37-char token, valid as of 2026-05-10) |
| `config/.env` | Token stored there is **stale/invalid** — needs rotation; do not use without re-fetching |
| Token owner | kyle@karakapines.co.nz |

---

## Workspaces (11)

| Workspace | ID | Notes |
|---|---|---|
| `000 - Overview` | `1167040628189060` | Portfolio-level registers, governance, supplier compliance |
| `100 - Regency Park` | `3978690771085188` | **Added 2026-05-23.** Operational village (Rotorua, BOP). 6 sheets cloned from XXX template, 7-folder flat layout (different from Phase 4). 88 unit rows incl 22 refurb-tagged. AUTO_NUMBER: `100-RFQ-`, `100-VAR-`, `100-RC-` (RC uses formula+helper col workaround for HTTP 1057). |
| `101 - Kempton Park` | `1304678492333956` | **Added 2026-05-23.** Operational village (Bethlehem, Tauranga). Same pattern as 100. 56 unit rows incl 1A/1B/55 (Shed) non-numeric IDs. |
| `102 - Roseland Park` | `8060077933389700` | **Added 2026-05-23.** Operational village (Hamilton East). Same pattern as 100. 56 unit rows incl Community Centre + Garage non-numeric IDs. |
| `103 - Rolleston` | `2542728585209732` | **Added 2026-05-23.** Woodcroft Estate (CAN region). Structural shell — 17 sheets cloned from 107, plus 77 unit rows (1-77 from site plan), 9 contract rows, and Approx Build Year populated on all 77 units from JLL XLSX. Masterplan staging not yet locked; Stage/Building Reference picklists inherit 107 placeholders. Has an extra `Archive` sub-folder under `04 - Civil and Construction`. |
| `104 - Drury - KLE` | `5737366867470212` | |
| `105 - Rototuna` | `2189930039404420` | |
| `106 - Waihi Beach` | `1169583248828292` | |
| `107 - Papamoa` | `4481862027503492` | **Trial village** — template patterns validated here first |
| `2CP` | `267451138107268` | Non-KPV portfolio (BBP, Next Chapter, PKCT, Peri). Documented for completeness; out of scope for KPV systems work. |
| `KPV - Project Finance` | `4935633912260484` | Cross-village finance — Papamoa Budget and Typology Sale Budget plus Budget-vs-Actual reports. |
| `XXX - Village Template` | `5525504720693124` | Template cloned per new village. **Schema diverges from 107/103/104/105/106 Unit Register** (35 cols vs 22 cols). |

**Schema fork:** 100/101/102 Unit Registers follow the XXX template structure (35 cols, plain PICKLISTs for Status, no Typology Register lookups). 103/104/105/106/107 follow the 107-derived structure (22 cols, formula-based Status, INDEX/MATCH against `{TR Floor Area}` etc.). Cross-village reports must handle both. Folder structures also differ — 100/101/102 use brief's flat 7-folder layout; 103/104/105/106/107 use Phase 4's 7+3-subfolder layout.

---

## Folders

| Workspace | Folder | ID |
|---|---|---|
| 000 - Overview | 01 - Portfolio Overview | `690439037708164` |
| 000 - Overview | 02 - Supplier Compliance | `8204501501929348` |
| 000 - Overview | 03 - Project Reference Registers | `2834486711871364` |
| 000 - Overview | 04 - Governance | `5644631200294788` |
| 104 | 02 - Civil and Construction | `3758934398920580` |
| 104 | 104 - Reports | `4407440100878212` |
| 105 | 02 - Civil and Construction | `7227511332464516` |
| 105 | 105 - Reports | `4041126635169668` |
| 106 | 02 - Civil and Construction | `4423756681635716` |
| 106 | 106 - Reports | `5523268309411716` |
| 107 | 00 - Dashboards | `8767670498682756` |
| 107 | 00 - Dashboards / Chart Sources | `8978776731215748` |
| 107 | 01 - Project Control | `4066520629307268` |
| 107 | 02 - Sales (new 2026-05-23) | `4203940523861892` |
| 107 | 03 - Procurement (new 2026-05-23) | `6737215314257796` |
| 107 | 04 - Civil and Construction (renumbered 2026-05-23 from 02) | `2549523147974532` |
| 107 | 05 - Health and Safety (renumbered 2026-05-23 from 03; previously 04→03 in Phase 1) | `1401823060879236` |
| 107 | 06 - Reports (renamed 2026-05-23 from `05 - Reports Internal`) | `1382941310904196` |
| 107 | 06 - Reports / Internal (sub-folder, new 2026-05-23) | `6510166163122052` |
| 107 | 06 - Reports / Internal / PCG Report Set (moved 2026-05-23) | `2128613131741060` |
| 107 | 06 - Reports / External (sub-folder, new 2026-05-23) | `6932378628188036` |
| KPV - Project Finance | 107 - Papamoa | `2676925836617604` |

**Folders removed from 107 in the 2026-05-22 Phase 1 cleanup:**

| Removed folder | Former ID | Reason |
|---|---|---|
| `03 - Sales and Marketing` | `1801164825094020` | Sales Register moved to `01 - Project Control`; folder no longer needed. |
| `02 - Civil and Construction / Archive` | `6798331356702596` | Empty; per-building migration archive intent absorbed elsewhere. |

---

## Sheets and reports — 000 Overview

> **Restructure note (2026-05-22 inventory):** the single "Master Registers" folder has been replaced by four purpose-specific folders. All registers previously listed here are accounted for below; two new sheets (Insurance Register, Statutory Compliance Register) and two top-level reports (Supplier insurance, Village Insurance) appeared in this inventory.

### Workspace-root reports

| Report | ID | Notes |
|---|---|---|
| 000-Supplier insurance | `4801365418135428` | New in 2026-05-22 inventory |
| 000-Village Insurance | `7041395947687812` | New in 2026-05-22 inventory |

### 01 - Portfolio Overview (folder `690439037708164`)

| Sheet | ID | Notes |
|---|---|---|
| Portfolio Register | `4900490847408004` | **Identified 2026-05-13** via 107 Dashboard widget probe; folder location confirmed in 2026-05-22 inventory. Also referred to as "Village Register" in dashboard/widget context. Portfolio-level master, 16 cols. Primary = Village Code. Captures Region (BOP/WKT/AKL/CAN), Land Area (ha), Address, Operating Status (Pre-development/Under Construction/Operating/Mixed), Active Insurance Policies, Insurance Status, Earliest Policy Renewal, Total Insured Value, Open/Overdue Compliance Items, Next Compliance Due, Compliance RAG (RYGG), Notes. Dashboard reads Land Area = 7.265 ha from the Papamoa row. |

### 02 - Supplier Compliance (folder `8204501501929348`)

| Sheet | ID | Notes |
|---|---|---|
| Supplier Register | `3313684242714500` | |

### 03 - Project Reference Registers (folder `2834486711871364`)

| Sheet | ID | Notes |
|---|---|---|
| Exterior Scheme Register | `638139734380420` | |
| F&F Register | `7182086124294020` | |
| Interior Scheme Register | `3138605269602180` | |
| Status Register | `6181671203196804` | |
| Typology Register | `4159669319716740` | |

### 04 - Governance (folder `5644631200294788`)

| Sheet | ID | Notes |
|---|---|---|
| Insurance Register | `472632968302468` | New in 2026-05-22 inventory — not previously registered. Sits alongside the portfolio-level Insurance Status columns on the Portfolio Register; relationship between the two yet to be confirmed. |
| KPV Risk Register | `499689920089988` | **Created 2026-05-12** from `smartsheet/input/2.0 KPV_Manager_Risk_RAG_Dashboard.xlsx`. 17 cols × 13 risk rows (FM-001 to FM-013). Formula columns: Inherent Score (L×C), Inherent RAG (Red/Yellow/Green based on score with RYGG symbol), Residual Score, Residual RAG. Picklists: Category (10 opts incl. Strategic, Regulatory, Financial, Governance/Conflicts etc.), Owner (Board/CEO/CFO/Fund Manager/GM Compliance/Fund Admin/AML Officer/External Counsel/Ext Provider), Likelihood/Consequence (1-5), Control Effectiveness (Weak/Adequate/Strong), Trend (Improving/Stable/Worsening), Status (Open/Closed/On Hold). Current portfolio position: 3 Red residual (FM-002 AML/CFT, FM-004 Conflicts, FM-010 Key person), 5 Amber, 5 Green. |
| KPV Risk Actions | `8345066161524612` | **Created 2026-05-12** — companion to KPV Risk Register. 7 cols × 14 mitigation actions (A-001 to A-015, gap at A-012). Risk ID picklist links to Register. Days to Due formula `=IFERROR([Due Date]@row - TODAY(), "")`. Status picklist: Not Started/In Progress/Complete/Closed/On Hold. |
| Statutory Compliance Register | `7227126171258756` | New in 2026-05-22 inventory — not previously registered. |

---

## Sheets — 104 Drury (KLE)

| Sheet | ID | Worked on |
|---|---|---|
| 104 - Civil Programme | `3427842057523076` | **Restructured to 24-row section-level hierarchy** (2026-05-11): 4 stage parents (Stage 1, 2A, 3A, 3B/3C) + 6 sub-parents (Earthworks + Civils for Stg1 & Stg2A; combined for 3A & 3B/3C) + 16 section leaves. Contracted Price populated from `smartsheet/104-KLE-Civil-Programme.xlsx` (sourced from McKenzie & Co QS contracts 1696-stg1 + 1696-3A). Reconciles to **$3,910,920.54 incl GST** (Stage 1, complete) + **$3,831,053.34 incl GST** (Stage 2A, complete incl $1.85M variations) + **$1,468,789.02 incl GST** (Stage 3A, [TBC]) + Stage 3B/3C [TBC, all financials]. Civil contractor: Dempsey Wood Civil Ltd. 4 original empty placeholder rows remain at top of sheet (to delete via UI). Added columns: Civils Budget, Budget Variance (formula), Total Cost (formula). Renamed: Contract Value → Contracted Price; Variations → Variations to Date. Stage picklist expanded for 2A / 3A / 3B-3C. |
| 104 - Construction Programme | `2443332474064772` | Source template — used as model for hierarchy. Has 274 unit rows (template). |
| 104 - Resource Consent Register | `6946932101435268` | |
| 104 - Unit Register | `8249131825844100` | List Price applied for 37 units (KLE budget, 2026-05-10) |
| 104 - RFQ and Quote Register | `1493560586096516` | At workspace root, not in folder |
| 104 - Variation Log | `5317417214365572` | At workspace root, not in folder |

### 104 - Reports (folder `4407440100878212`)

| Asset | ID | Type | Notes |
|---|---|---|---|
| 104 - Drury | `1718153349752708` | dashboard | Village dashboard. |
| 104 - Active Build | `8021914634112900` | report | |
| 104 - Construction Status | `4640890608897924` | report | |
| 104 - Construction Variance Watch | `4701559974743940` | report | |
| 104 - Design Status Summary | `7302384400158596` | sheet | Orphan summary sheet — earlier mistake; matching `104 Design Status` report exists. |
| 104 - Master Unit Status | `6046841710792580` | report | |
| 104 - Sale Variance Watch | `7737065960591236` | report | |
| 104 - Sales Pipeline | `7804795447365508` | report | |
| 104 - Schedule Risk | `6329980987330436` | report | |
| 104 - Upcoming Starts | `1405304913743748` | report | |
| 104 Design Status | `674110353919876` | report | |
| Untitled report | `6472306070081412` | report | Housekeeping. |

---

## Sheets — 105 Rototuna

| Sheet | ID | Worked on |
|---|---|---|
| 105 - Civil Programme | `7961358078267268` | **Loaded 41-row section-level hierarchy** (2026-05-11): 4 stage parents (Stg1, Stg2-3, Stg3 Wright SP1+SP3, Stg4) + 8 sub-parents (Earthworks/Civils per stage, with Stg3 split into SP1+SP3) + 29 section leaves. Builders: Online Contractors (2016) Ltd (Stg1), [TBC] (Stg2-3 future), Wright Civil Limited (Stg3 actual), Matco Civil Contractors Limited (Stg4). Stg1 total: **$1,177,431.65 incl GST** (contracted) / $1,413,350 budget = -$235,918.35 variance. Stg3 (Wright): **$735,923.62** contracted + **$232,344.09** variations = **$968,267.71** total (note: template flagged Claim 10 certified $1,150,551.45 / total claimed $1,501,860.80 with $351,309.35 deduction dispute). Stg4: **$465,497.59 incl GST** (Matco — Cut to Waste at Borman Road, Hamilton — contract 183983/4 dated 25/2/26). Schema was already 107-aligned (Civils Budget, Contracted Price, Budget Variance formula, Variations to Date, Total Cost formula). Picklists expanded: Stage adds "Stage 2-3"; Civil Contractor adds Online Contractors / Wright Civil / Matco / Dempsey Wood / [TBC]. |
| 105 - Construction Programme | `75158441119620` | **Reloaded** with 800-row hierarchy (4 top + 4 sub + 132 units + 660 phase children); 100 Foundation Starts from budget (Stage 1A/1B added to picklist) |
| 105 - Unit Register | `1096218196266884` | **Loaded** 137 rows; Unit Numbers later text-fixed (numeric→string); 104 of 104 List Prices applied |

### 105 - Reports (folder `4041126635169668`)

| Asset | ID | Type | Notes |
|---|---|---|---|
| 104 - Sale Variance Watch | `3871985162473348` | report | **Misfiled** — 104-prefixed report lives in 105 Reports folder. Move to 104 or rename. |
| 105 - Active Build | `2254064069857156` | report | |
| 105 - Construction Status | `1445204086181764` | report | |
| 105 - Construction Variance Watch | `4650020165865348` | report | |
| 105 - Master Unit Status | `8522938205556612` | report | |
| 105 - Sales Pipeline | `4220407472148356` | report | |
| 105 - Schedule Risk | `5065863194431364` | report | |
| 105 - Upcoming Starts | `8693900922277764` | report | |
| 105 Design Status | `6472207285833604` | report | |
| Untitled report | `6159053100109700` | report | Housekeeping. |

---

## Sheets — 106 Waihi Beach

| Sheet | ID | Worked on |
|---|---|---|
| 106 - Civil Programme | `4813421928206212` | **Reloaded with 24-row hierarchy** (2026-05-12): deleted 41 incorrect rows that were copy-pasted from 105. Loaded 1 stage parent (Stage 1 EW & Civil Contract – SP1, SP2 & SP3) + 3 sub-parents (SP1 Stage 1 Earthworks; SP2 Stage 1A Civil Works; SP3 Stage 1B Civil Works Provisional) + 20 section leaves (SP1: 100/200/300/400; SP2 & SP3: 100/200/300/400/500/600/700/800 each). Contractor: **RZG**. Contract 183864, Lysaght (Peter Moodie) QS / Crowther & Co bank QS, tender awarded 30/11/2021, site possession 06/12/2021. SP1 LDs $800/day from 01/06/2022. Lender: ASB. **Parent total $3,406,359.64 incl GST contracted vs $2,896,947.75 budget = +$509,411.89 OVER-BUDGET variance**. SP1 $1,548,445.05 / SP2 $958,275.71 / SP3 $899,638.87. Picklists expanded: Stage adds 1A/1B; Civil Contractor adds RZG. |
| 106 - Construction Programme | `7130063131594628` | **Reloaded** with 32-row hierarchy (1 top + 1 sub + 5 units + 25 phase children); 2 Foundation + 2 Practical Start budget updates (only 5 unit rows in source) |
| 106 - Unit Register | `4460551978569604` | **Loaded** 105 rows; Unit Numbers later text-fixed (numeric→string); 75 of 96 List Prices applied; Stage picklist added 1A/1B |

### 106 - Reports (folder `5523268309411716`)

| Asset | ID | Type | Notes |
|---|---|---|---|
| 106 - Active Build | `2891102209134468` | report | |
| 106 - Construction Status | `1589749063044996` | report | |
| 106 - Construction Variance Watch | `4218071009939332` | report | |
| 106 - Master Unit Status | `2243721788608388` | report | |
| 106 - Sale Variance Watch | `6757663697227652` | report | |
| 106 - Sales Pipeline | `3663723876011908` | report | |
| 106 - Schedule Risk | `557109606305668` | report | |
| 106 - Upcoming Starts | `5196816143306628` | report | |
| 106 Design Status | `3139147777658756` | report | |
| Untitled report | `6747321415978884` | report | Housekeeping. |

---

## Sheets and reports — 107 Papamoa (TRIAL VILLAGE)

> **Phase 2.5 v2 restructure (2026-05-23)** — workspace is now in the 7-folder target shape via REST API (PUT /sheets/{id}, PUT /folders/{id}, POST /sheets/{id}/move, POST /folders/{id}/move, DELETE /folders/{id}; the MCP toolkit doesn't surface these, but the REST endpoints work with the KPV API token):
>
> ```
> 00 - Dashboards (+ Chart Sources)
> 01 - Project Control (Unit Register, Risk Register, Decision Log, Monthly RAG Log)
> 02 - Sales (Sales Register)
> 03 - Procurement (RFQ Register, Contract Register, Variation Log)
> 04 - Civil and Construction (Civil Programme, Construction Programme, Construction Register)
> 05 - Health and Safety (H&S Incidents, H&S Monthly Indicators)
> 06 - Reports / Internal / External (with PCG Report Set under Internal)
> ```
>
> Sheet rename: `107 - PCG Status Snapshot` → `107 - Monthly RAG Log` (sheet ID `8488689867902852` unchanged). Folder renumbers: 02→04 (Civil/Construction), 03→05 (H&S), 05→06 (Reports). New folders: 02 - Sales (`4203940523861892`), 03 - Procurement (`6737215314257796`), and sub-folders Internal (`6510166163122052`) + External (`6932378628188036`) under 06 - Reports. Old `06 - Reports External` (`6714388368385924`) deleted after its single report was moved.
>
> Earlier (Phase 1, 2026-05-22): `03 - Sales and Marketing` (Phase 1) and `02 / Archive` folders deleted. Two stray top-level reports (`107 - Construction Program` `5093377811894148`, `Untitled report` `1730274806157188`) deleted. `107 - Resource Consent Register` `1643703515959172` intentionally removed — consent status now lives on Construction Register and flows up to Unit Register. The per-unit Construction Programme `5063906232848260` was replaced by the per-building sheet `4820480841174916` in the earlier per-building migration (see `plans/107-per-building-migration/`).

### Workspace-root reports

None as of 2026-05-22 (both stray reports cleaned up — see Phase 1 note above).

### 00 - Dashboards (folder `8767670498682756`)

| Asset | ID | Type | Notes |
|---|---|---|---|
| 107 - Dashboard | `3236074114836356` | dashboard | 10 widgets, dark navy `#131F39` background, 90-col grid. Two sections: Sales Overview + Construction Overview. **No chart widgets** — all metric tiles and report grids. Pulls from: Portfolio Register (Land Area), Unit Register (sales status + total units), Construction Programme (% complete buckets), Sales Register (Avg List Price), H&S Monthly Indicators (10 KPI tiles), the External Signature Homes report, and the Sales Team View report. See `plans/Stage 1 Papamoa/pcg-report-dashboard-chart-buildspec.md`. |
| 107 - PCG Dashboard | `6078071154468740` | dashboard | New PCG dashboard alongside the original 107 - Dashboard. Companion to the PCG Report Set; purpose and widget set to be documented next time it's worked on. |

#### Chart Sources (folder `8978776731215748`)

| Sheet | ID | Notes |
|---|---|---|
| 107 - Chart Source - Application Strength | `2191119310868356` | Backing sheet for an Application Strength chart on the PCG dashboard. |
| 107 - Chart Source - Construction Progress | `4094966644035460` | Backing sheet for a Construction Progress chart. |
| 107 - Chart Source - Sales Pipeline | `7953427823808388` | Backing sheet for a Sales Pipeline chart. |
| 107 - Chart Source - Typology Sales | `1171511254667140` | Backing sheet for a Typology Sales chart. |

### 01 - Project Control (folder `4066520629307268`)

| Sheet | ID | Notes |
|---|---|---|
| 107 - Monthly RAG Log | `8488689867902852` | **Renamed 2026-05-23 via PUT /sheets/{id}** (was `107 - PCG Status Snapshot`). **12 cols** × 1 row (was 29; Phase 2.5 cut 8 narrative blocks + 6 derivable count columns + Top Risks Summary + Board Resolutions This Period). Quality RAG options standardised to Red/Yellow/Green/Gray (was Green/Amber/Red); **symbol RYGG application is still a UI follow-up** (API couldn't coerce existing "Green" cell value). Remaining cols: Period Label, Period Date, Is Current Period, Overall RAG, Submitted By, Quality RAG, Programme RAG, Cost RAG, Health and Safety RAG, Sales RAG, Maori Procurement RAG, Overall Commentary. |
| 107 - Risk Register | `1049548813193092` | Source for `107 - PCG - Risk Register` report. **14 cols** × 13 rows. Phase 2.5: Score column became formula `=[Likelihood]@row * [Consequence]@row` (col `5598299569819524`). RAG column became formula `=IF([Score]@row = "", "Gray", IF([Score]@row >= 15, "Red", IF([Score]@row >= 8, "Yellow", "Green")))` (col `8888052318769028`). RSK-0012 flipped from manual Green to formula-derived Yellow (Score=9 falls in Yellow band). New `Date Identified` DATETIME CREATED_DATE column added (col `5974658469105540`). Categories: HS / Commercial / Environmental / Programme / Quality / Compliance / Stakeholder / Other. |
| 107 - Sales Register | `8224519314427780` | **Moved to 01 - Project Control on 2026-05-22** (was 03 - Sales and Marketing). 16 cols × 128 rows. Sales Status PICKLIST is **independently maintained** on both this sheet AND Unit Register — duplication of truth, needs reconciliation in Phase 2. Cross-sheet pulls: Building Ref / Stage / Typology from Unit Register; Build Status from Construction Register via `{107 Construction Status}` + `{107 CR Building Reference}`; Budget Sale Price from Typology Sale Budget. Native cols include Application Strength (RYGB), Settlement Date, List or Sold Price, Incentive Agreed, Sale Price Variance formula, Sale Variance Flag (DIRECTIONS_3_WAY). |
| 107 - Unit Register | `5289542339743620` | **18 cols** × 128 rows (was 22; Phase 2.5 cut Beds/Garage/Attachment Type/Floor Area — UI follow-up will reinstate them as cross-sheet formulas pulling from Typology Register). Typology PICKLIST trimmed in Phase 2.5: removed Harris SG / Robertson DG / Robertson SG / Stanaway DG / Stanaway SG (none in use). Sales Status PICKLIST expanded to 9 options: Not Available / Available / Application / Conditional / Unconditional / Transfer / Settled / Occupied / Clubhouse. Sales Status remains hand-maintained pending Phase 1 carryover UI work (cross-sheet formula from Sales Register). Cross-sheet pulls (unchanged): Consent Status from Construction Register `{107 Consent Status}`; Construction Status from CR `{107 Construction Status}` keyed on `{107 CR Building Reference}`. |
| 107 - Decision Log | `1863332356116356` | **Created 2026-05-22 (Phase 2).** 13 cols, empty (E.3 backfill of 5 historic Board decisions was deferred at Kyle's instruction — to be done manually). Primary = Decision Title. AUTO_NUMBER `107-DEC-0001` (4-digit padding; retrofitted from 3-digit on 2026-05-22 per kpv-naming-conventions §3). Picklists with strict validation: Forum (Board/PCG/PM/Director/Other), Decision Type (Budget/Programme/Design/Procurement/Sales/H&S/Governance/Other), Status (Open/In Progress/Closed/Superseded). Scope: Board + PCG + PM decisions. Direct entry, no form. |

### 04 - Civil and Construction (folder `2549523147974532`) — renumbered from `02` on 2026-05-23

| Sheet | ID | Notes |
|---|---|---|
| 107 - Civil Programme | `6233992763232132` | **Restructured to 14-row section-level hierarchy** (2026-05-11): Contract Award milestone + Stage 1 Civils top parent + SP1 Earthworks sub-parent (3 section leaves: 100/200/300) + SP2 Civils sub-parent (7 section leaves: 100/200/400/500/600/700/800). All Contracted Price (incl GST) populated, reconciles to **$1,494,083.45 incl GST** ($1,299,203 excl × 1.15) per NZS3910 contract with Matco Civil Contractors awarded 19 July 2024 (Lysaght Ref 225269). Includes +$19,110 post-tender adjustment (Item 504 WW connection rate). 900/1000 sections (unscheduled/dayworks) omitted from rows. |
| 107 - Construction Programme | `4820480841174916` | **17 cols** × 329 rows (was 24; Phase 2.5 cut Build Partner, Contract Package, Contract Price (incl GST), Variations (incl GST), Budget Approved, Expected Total Cost, Expected Variance — all migrated to Contract Register / Construction Register / Variation Log canonical sources per Phase 2.5 architectural rules). Programme is now timeline-only. Stage PICKLIST: Stage 1, Stage 2A-2E, Stage 3, Stage 4, Stage 5, Pavilion. Construction Status remains canonical here (col `4580213165166468`) — Construction Register pulls from it via cross-sheet formula. Sheet replaced the old per-unit sheet `5063906232848260` per per-building migration. |
| 107 - Construction Programme (per-unit, ARCHIVE) | `5063906232848260` | **Archived** — superseded by the per-building sheet above. Tidied to 658 rows (manual + script). 114 List Prices on UR; 106 Foundation Start + 106 Practical Start from budget. Migration log: `plans/107-per-building-migration/migration_log.md`. |
| 107 - Construction Register | `2635310868418436` | 19 cols × 64 rows. Carries per-building consent + budget tracking. Cross-sheet formulas: Construction Status via INDEX/MATCH on Construction Programme `{107 CP Construction Status}` + `{107 CP Building Reference}`; Construction Budget via INDEX/MATCH on Papamoa Budget `{Papamoa Budget Approved}` + `{Papamoa Budget Building Reference}` (with `SUM(CHILDREN)` rollup for parent rows). Native Consent Status PICKLIST (Not Yet Lodged / Ready to Lodge / Design Approval / Lodged / Approved). Includes Budget Flag formula (DIRECTIONS_3_WAY). |
| 107 - Variation Log | `2963546479480708` | **Created 2026-05-22 (Phase 2); restructured 2026-05-23 per Phase 2.5 v2 Section K.** 34 cols (was 29; +6 added, −1 deleted: legacy Reason for Change), empty. Primary = Variation Title. AUTO_NUMBER `107-VAR-0001` (4-digit padding). **Cost Band formula 4-tier**: `<=$5k Delivery Lead Approval` / `<=$25k GM Developments Approval` / `<=$50k CFO Co-Sign Required` / `>$50k CEO Approval Required`. Required Approval Level returns L1/L2/L3/L4. Approver columns: L1 Approver (Delivery Lead) / L2 Approver (GM Developments) / L3 Approver (CFO) / L4 Approver (CEO) with matching Approval Date columns per tier. Approval Status PICKLIST is 9-state workflow (Draft/Submitted/Pricing/Pending Approval/Approved/Rejected/Issued/Built/Closed). **Analytics columns**: `Cost Category` (Materials/Labour/Plant/Subcontractor/Design/Other) and `Variation Source` (Client Request/Design Change/Site Conditions/Statutory \\| Consent/Error \\| Omission/Programme Acceleration/Other). Trade Package is free-text (review for picklist 2026-11-01). Intake via UI form `FORM - Variation Submission` (pending UI build). 13 automations documented for Phase 2.6 build. |
| 107 - RFQ and Quote Register | `5413487898480516` | **Created 2026-05-22 (Phase 2).** 22 cols, empty. Single sheet with parent (Type=RFQ) and child (Type=Quote) rows via indent. Primary = RFQ or Quote Name. AUTO_NUMBER `107-RFQ-0001` (4-digit padding; retrofitted from 3-digit on 2026-05-22) is SHARED between parents and children — parents get 0001, 0003, 0005... children get 0002, 0004... (Quote ID column `224072465420164` carries the derived `{Parent}-Q{nn}` form, e.g. `107-RFQ-0001-Q01`) Picklists with strict validation: Type (RFQ/Quote), Linked Stage, RFQ Status (Draft/Open/Quotes Received/Awarded/Cancelled — parent only), Quote Status (Submitted/Shortlisted/Awarded/Declined/Withdrawn — child only). Two intake forms pending UI build: `FORM - RFQ Creation` (KPV-side), `FORM - Quote Submission` (public URL for suppliers). |
| 107 - Contract Register | `3948571190579076` | **Created 2026-05-22 (Phase 2).** 24 cols, empty. Primary = Contract Title. AUTO_NUMBER `107-CON-0001` (4-digit padding; retrofitted from 3-digit on 2026-05-22). Direct entry (no form) — triggered by RFQ Award automation. Stages Covered is MULTI_PICKLIST (single contract can span multiple stages). Picklists with strict validation: Contract Type (Construction/Civil/Supply/Consulting/Service/Other), Stages Covered, Contract Status (Draft/Executed/In Progress/Practical Completion/Complete/Terminated/Disputed). Current Contract Value = Contract Value + Variations to Date (local formula). Variations to Date is **plain TEXT_NUMBER initially** — pending UI conversion to SUMIFS formula once cross-sheet refs to Variation Log are created: `=SUMIFS({VL Cost Impact}, {VL Linked Contract}, [Contract ID]@row, {VL Final Approval Status}, "Approved")`. |

> **Resource Consent Register** — sheet `1643703515959172` **deleted 2026-05-22** (intentional, confirmed by Kyle). 107 does not have a standalone consent register; consent status is captured on Construction Register and flows up to Unit Register via cross-sheet formula.

### 05 - Health and Safety (folder `1401823060879236`)

> **Renumbered 2026-05-23** from `03 - Health and Safety` per Phase 2.5 v2 Section A (was `04 - Health and Safety` until Phase 1 cleanup renumbered it to 03). Gap-free 7-folder structure now in place.

| Sheet | ID | Notes |
|---|---|---|
| 107 - H and S Incidents and Observations | `8305827340308356` | New in 2026-05-22 inventory. Companion sheet to Monthly Indicators; likely captures individual events. |
| 107 - H and S Monthly Indicators | `3104570405244804` | **Identified 2026-05-13** via dashboard probe. 19 cols × 5 rows (Jan–May 2026; only April populated). Primary = Entry Label (e.g. "April 2026"); paired with Period Start / Period End / Record ID / Contractor (PICKLIST: KPV/Signature Homes/Matco Civil/BaseUp/AmpT/Out the Gate/Downey Construction/Home Construction/Other) / Submitted By (CONTACT) / Date Submitted. KPI columns: Inductions, Contractor Audits, Internal Audits PM, Internal Audits DM, External Inspections, Near Miss Minor, Near Miss Serious PSIF, MTI, LTI, LTI Days, Observations Narrative, Notes. Drives dashboard widget [9] via SUMIF on Entry Label = [Current Period]#. Apr 2026 row: Inductions 17, Contractor Audits 7, Near Miss Minor 2, all others 0. |

### 06 - Reports / Internal (folder `6510166163122052`, parent `1382941310904196` renamed from `05 - Reports Internal`)

> **Renamed 2026-05-23** — `05 - Reports Internal` became `06 - Reports` and the reports inside it were moved into a new `Internal/` sub-folder. `06 - Reports External` (was `6714388368385924`) was emptied into a new `External/` sub-folder and the old folder deleted.

| Report | ID | Notes |
|---|---|---|
| 107 - Design Report | `7555536550580100` | |
| 107 - PCG - Construction Status - Granular | `5514606595231620` | New in 2026-05-22 inventory. |
| 107 - Sales Team View | `8674117833150340` | **Renamed from `107 - Sales Team Report`** (2026-05-22 inventory). Per-unit sales grid embedded in dashboard Sales Overview widget. Sourced from 107 - Sales Register. |

#### PCG Report Set (folder `2128613131741060`)

| Report | ID | Notes |
|---|---|---|
| 107 - PCG - Building Consent Status | `6547943396953988` | Was "107 Consent Status Report". |
| 107 - PCG - Civil Programme | `440619490037636` | New in 2026-05-22 inventory. |
| 107 - PCG - Construction Status | `2902958600572804` | New in 2026-05-22 inventory. |
| 107 - PCG - Design Status | `7970693592338308` | New in 2026-05-22 inventory. |
| 107 - PCG - H&S Monthly Indicators | `794965968899972` | Was "107 H&S Monthly Report". 14 cols × 5 rows (Jan–May 2026) from 107 - H and S Monthly Indicators (`3104570405244804`). |
| 107 - PCG - H&S Open Items | `8821624189964164` | Was "107 - H&S Open Items Report". |
| 107 - PCG - Risk Register | `2047711023943556` | Was "107 - Risk Report". 13 cols × 14 rows. Source sheet: `1049548813193092` (107 - Risk Register, now in 01 - Project Control). |
| 107 - PCG - Sales Pipeline | `1094205601435524` | New in 2026-05-22 inventory. |
| 107 - PCG - Sales Status | `1830541908201348` | **Renamed from `107 - Sales Report - Expanded`** (2026-05-22 inventory). 11 cols × 23 rows from 107 - Sales Register. Adds Budget Sale Price + Sale Price Variance + Sale Variance Flag (DIRECTIONS_3_WAY) vs the Sales Team View. Use this for variance-focused board reporting. |
| 107 - PCG - Settlements Upcoming | `3805380084715396` | New in 2026-05-22 inventory. |
| 107 - PCG - Top 5 Risks | `3731440612102020` | New in 2026-05-22 inventory. |
| Copy of 107 - PCG - H&S Monthly Indicators - Lead | `4807577668898692` | **Pending UI rename to `107 - PCG - H&S Lead Indicators`** (decision 2026-05-22). Genuinely separate purpose from the original (7-col Lead-indicator subset: Inductions, Audits, External Inspections + Contractor Audits) vs the original (11-col, includes Lag indicators Near Miss/MTI/LTI). |

### 06 - Reports / External (folder `6932378628188036`, new 2026-05-23)

> **Old `06 - Reports External` (`6714388368385924`) deleted 2026-05-23** after the single report it contained was moved to the new External sub-folder.

| Report | ID | Notes |
|---|---|---|
| 107 - External - Signature Homes Build Status | `6144240361885572` | **Renamed from `107 - Papamoa - Signature Report`** (2026-05-22 inventory). Per-unit construction grid: Primary, Construction Status, Stage, Typology, RAG, % Complete, Start/End Dates, Duration. 29 rows (Stage 1 hierarchy + units + phases). External-facing, shared with Signature Homes. Drives Construction Overview widget on dashboard. |

### 107 cross-sheet reference map (2026-05-22)

```
Construction Programme (4820480841174916)   ── source of truth, per-building/phase
   │
   ├─ {107 CP Construction Status}  ─┐
   └─ {107 CP Building Reference}   ─┴──→ Construction Register (2635310868418436)
                                              │
   Papamoa Budget (5631895457976196)          │
       └─ {Papamoa Budget Approved}     ─────→│   (and SUM(CHILDREN) rollup on parent rows)
       └─ {Papamoa Budget Building Reference}─┤
                                              │
                                              ├─ {107 CR Building Reference}  ──┐
                                              ├─ {107 Consent Status}            │
                                              └─ {107 Construction Status}       │   <-- ambiguous range name
                                                                 │              │
                                                                 ▼              ▼
                                          Unit Register (5289542339743620)  Sales Register (8224519314427780)
                                              ├─ Consent Status (← CR)         ├─ Build Status (← CR via {107 Construction Status})
                                              └─ Construction Status (← CR)    ├─ Building Ref / Stage / Typology (← Unit Register)
                                                                               └─ Budget Sale Price (← Typology Sale Budget {Typology Sale Budget Value} / {Typology Budget Names})
```

**Open issue — UI confirmation needed:** named range `{107 Construction Status}` is used by both Unit Register's `Construction Status` column and Sales Register's `Build Status` column. The range name lacks a `CR`/`CP` prefix, so the source isn't visible in the formula text. By context (sibling range `{107 CR Building Reference}`) it should point to Construction Register, but worth verifying in the UI (right-click column → Edit Column Formula → hover the range). Phase 2 should standardise these to carry `CR`/`CP` prefixes.

**Duplication of truth — Sales Status:** PICKLIST exists natively on both Unit Register (col `8282836699484036`) and Sales Register (col `4247873805127556`). Neither has a formula — both are hand-maintained. Picklist options identical (Not Available / Available / Application / Unconditional / Settled / Clubhouse). Phase 2 should pick a canonical home (recommendation: Sales Register) and convert the other to a cross-sheet formula.

---

## Sheets — XXX Village Template

| Sheet | ID |
|---|---|
| XXX - Civil Programme | `3923860045909892` |
| XXX - Construction Programme | `1507473327345540` |
| XXX - Resource Consent Register | `3572291202928516` |
| XXX - RFQ and Quote Register | `896569527193476` |
| XXX - Unit Register | `7737437206826884` |
| XXX - Variation Log | `6208456229867396` |

---

## Sheets and reports — KPV - Project Finance (workspace `4935633912260484`)

Cross-village finance workspace, new in 2026-05-22 inventory (was not previously registered).

### Workspace-root reports

| Report | ID | Notes |
|---|---|---|
| 107 - Budget vs Actual | `6175816542015364` | Budget-vs-Actual reporting for 107. |
| 107 - Budget vs Actual - ALL Stages | `2837326920109956` | All-stages roll-up variant. |
| 107 - Budget vs Actual - Headlines | `6163422608576388` | Headline summary variant. |

### 107 - Papamoa (folder `2676925836617604`)

| Sheet | ID | Notes |
|---|---|---|
| 107 - Papamoa Budget | `5631895457976196` | 107 budget sheet — likely the canonical source backing the Budget vs Actual reports. Connects to the build script under `smartsheet/` (see commit `8ab8ee1`). |
| 107 - Typology Sale Budget | `2636028799045508` | Typology-level sale budget for 107. |

---

## Workspace — 2CP (`267451138107268`)

Non-KPV portfolio. Captured here for completeness so we don't keep re-discovering it on each audit. Out of scope for KPV systems work; confirm provenance with Kyle if any task requires interacting with it.

| Asset | ID | Type | Path |
|---|---|---|---|
| Peri | `6977456635334532` | sheet | workspace root |
| Peri_Main_Program_Rows | `7041132327292804` | sheet | workspace root |
| Program | `2930626779893636` | sheet | BBP (folder `8278342727165828`) |
| 01 PGF Funding Tranches | `5336677391224708` | sheet | PKCT / 01 Project Control (folder `7517102723622788`) |
| 1.0 Overview | `330583770091396` | sheet | PKCT / 02 Program (folder `1702885235943300`) |
| 1.1 Superior Program | `334567352258436` | sheet | PKCT / 02 Program |
| 1.2 1st Gas Program | `2586367165943684` | sheet | PKCT / 02 Program |
| 1.3 KR Program | `186032350777220` | sheet | PKCT / 02 Program |

`Next Chapter` folder (`7011705331967876`) is empty.

---

## Verified column IDs (sheets actively used, snapshot 2026-05-10)

### 104 - Unit Register (sheet `8249131825844100`)
- Unit Number: `7613116342112132`
- List Price (incl GST): `7190903877046148`
- Contract Price (incl GST): `4939104063360900`
- Construction Budget Price (incl GST): `8068481810730884`
- Budget Sale Price (incl GST): `2687304249675652`

### 105 - Unit Register (sheet `1096218196266884`)
- Unit Number: `5945002516844420` (primary)
- Stage: `3693202703159172` (PICKLIST, validation=false; includes Stage 1A, Stage 1B)
- Typology: `8196802330529668` (PICKLIST, validation=true)
- List Price (incl GST): `456240470986628`
- Contract Price (incl GST): `7493114888753028`
- Construction Budget Price (incl GST): `1863615354539908`
- Budget Sale Price (incl GST): `8619014795595652`
- Construction Budget Variance (incl GST): `6367214981910404` (FORMULA)
- Construction Variance Flag: `4115415168225156` (FORMULA)
- Sale Price Variance (incl GST): `4959840098357124` (FORMULA)
- Sale Variance Flag: `2708040284671876` (FORMULA)

### 105 - Construction Programme (sheet `75158441119620`)
- Task Name: `6079967569153924` (primary)
- Is Unit: `3828167755468676`
- Stage: `1013417988362116` (PICKLIST; includes Stage 1A, Stage 1B)
- Typology: `5517017615732612` (FORMULA — VLOOKUP)
- Construction Status: `3265217802047364` (FORMULA — VLOOKUP)
- Build Partner: `7768817429417860` (FORMULA — VLOOKUP)
- Building Consent Number: `2139317895204740` (FORMULA — VLOOKUP)
- Contract Price (incl GST): `6642917522575236` (FORMULA — VLOOKUP)
- Start Date: `4602223941422980` (ABSTRACT_DATETIME, GANTT_START_DATE)
- End Date: `2350424127737732` (ABSTRACT_DATETIME, GANTT_END_DATE)
- Duration: `6854023755108228`

### 106 - Unit Register (sheet `4460551978569604`)
- Unit Number: `2276009524367236`
- Stage: `6779609151737732` (PICKLIST; includes Stage 1A, Stage 1B)
- List Price (incl GST): `6498134175027076`
- Construction Budget Price (incl GST): `5372234268184452`

### 106 - Construction Programme (sheet `7130063131594628`)
- Task Name: `1327852544102276`
- Is Unit: `5831452171472772`
- Stage: `8083251985158020`
- Start Date: `483427613970308`
- End Date: `4987027241340804`
- Duration: `2735227427655556`

### 107 - Unit Register (sheet `5289542339743620`) — updated 2026-05-22 Phase 2.5

- Unit Number: `5749561909088132` (primary)
- Stage: `3497762095402884` (PICKLIST)
- Typology: `8001361722773380` (PICKLIST, validation=true) — **22 options after Phase 2.5 trim** (removed Harris SG / Robertson DG / Robertson SG / Stanaway DG / Stanaway SG)
- Building Reference: `648556682973060`
- Up Next: `683012328296324` (CHECKBOX)
- Exterior Scheme: `5186611955666820` (PICKLIST)
- Interior Scheme: `2934812141981572` (PICKLIST)
- F&F Scheme: `7438411769352068` (PICKLIST)
- Landscape Approved: `1808912235138948` (CHECKBOX)
- Design Approved: `6312511862509444` (CHECKBOX)
- Design Status (Internal Process): `4060712048824196` (PICKLIST)
- Contract Signed: `7156936792641412` (CHECKBOX)
- CEO Approval: `1527437258428292` (CHECKBOX)
- Consent Status: `6031036885798788` (FORMULA — INDEX/MATCH from CR)
- Construction Status: `3779237072113540` (FORMULA — INDEX/MATCH from CR)
- Sales Status: `8282836699484036` (PICKLIST, validation=true) — **9 options after Phase 2.5 expansion**: Not Available, Available, Application, Conditional, Unconditional, Transfer, Settled, Occupied, Clubhouse
- Latest Comment: `7594600268337028`
- Notes: `3075549630336900`
- **DELETED in Phase 2.5**: Beds (was `5890299397443460`), Garage (was `3638499583758212`), Attachment Type (was `8142099211128708`), Floor Area (m²) (was `823749816651652`). UI follow-up restores these as cross-sheet formula columns pulling from Typology Register.

### 107 - Construction Programme — OLD per-unit, ARCHIVED (sheet `5063906232848260`)

> **Superseded** by the per-building sheet `4820480841174916` (confirmed 2026-05-22 inventory). The column IDs below belong to the old sheet — kept here for migration/archive reference. Re-audit columns on the new sheet via `get_columns` before next active use.

- Task Name: `6646557238923140` (primary)
- Is Unit: `4394757425237892`
- Stage: `102264030400388` (PICKLIST; includes Stage 2D, Stage 2E)
- Typology: `4605863657770884` (FORMULA — VLOOKUP)
- Construction Status: `2354063844085636` (FORMULA — VLOOKUP)
- Build Partner: `6857663471456132` (FORMULA — VLOOKUP)
- Building Consent Number: `1228163937243012` (FORMULA — VLOOKUP)
- Contract Price (incl GST): `5731763564613508` (FORMULA — VLOOKUP)
- Start Date: `5168813611192196`
- End Date: `2917013797506948`
- Duration: `7420613424877444`

### 104 - Civil Programme (sheet `3427842057523076`)
- Task Name: `8811206059265924` (primary)
- Required: `226219269590916` (CHECKBOX)
- Stage: `4729818896961412` (PICKLIST; Clubhouse, Stage 1/2/2A/3/3A/3B-3C/4/5)
- Sub-Phase: `2478019083276164` (PICKLIST: Preliminaries, Earthworks, Civils)
- Civil Contractor: `6981618710646660` (TEXT_NUMBER; populated with "Dempsey Wood Civil Ltd")
- Construction Status: `1352119176433540` (PICKLIST, validation=true)
- RAG: `5855718803804036` (PICKLIST RYGG)
- % Complete: `3603918990118788` (GANTT_PERCENT_COMPLETE)
- Start Date: `8107518617489284` (GANTT_START_DATE)
- End Date: `789169223012228` (GANTT_END_DATE)
- Duration: `5292768850382724` (GANTT_DURATION)
- Predecessors: `3040969036697476` (GANTT_PREDECESSOR)
- Civils Budget (incl GST): `3065437096284036`
- Contracted Price (incl GST): `7544568664067972` (renamed from "Contract Value")
- Budget Variance (incl GST): `2856351645863812` (FORMULA: `=IFERROR([Contracted Price (incl GST)]@row - [Civils Budget (incl GST)]@row, "")`)
- Variations to Date (incl GST): `1915069129854852` (renamed from "Variations")
- Total Cost (incl GST): `2436510002745220` (FORMULA: `=IFERROR([Contracted Price (incl GST)]@row + [Variations to Date (incl GST)]@row, "")`)
- Notes: `6418668757225348`
- Include in Report: `4166868943540100` (CHECKBOX)

### 107 - Civil Programme (sheet `6233992763232132`)
- Task Name: `6067696579153796` (primary)
- Required: `3815896765468548` (CHECKBOX)
- Stage: `8319496392839044` (PICKLIST: Clubhouse, Stage 1-5)
- Sub-Phase: `1001146998361988` (PICKLIST: Preliminaries, Earthworks, Civils) — left blank on section-level rows
- Civil Contractor: `5504746625732484`
- Construction Status: `3252946812047236` (PICKLIST, validation=true)
- RAG: `7756546439417732` (PICKLIST RYGG)
- % Complete: `2127046905204612` (GANTT_PERCENT_COMPLETE; expects 0.0–1.0)
- Duration: `8882446346260356` (formula on parent rows: `=CALCDURATION([Start Date]@row, [End Date]@row)`)
- Start Date: `6630646532575108` (formula on parent rows: `=MIN(CHILDREN())` — but can be overridden by direct write)
- End Date: `4378846718889860` (no rollup formula; static value — does not auto-recompute when new descendants added)
- Predecessors: `86353324052356`
- Civils Budget (incl GST): `6586215498551172`
- Contracted Price (incl GST): `4589952951422852`
- Budget Variance (incl GST): `7434318397083524` (FORMULA: `=IFERROR([Contracted Price (incl GST)]@row - [Civils Budget (incl GST)]@row, "")`)
- Variations to Date (incl GST): `2338153137737604`
- Total Cost (incl GST): `4610895614611332` (FORMULA: `=IFERROR([Contracted Price (incl GST)]@row + [Variations to Date (incl GST)]@row, "")`)
- Notes: `6841752765108100`
- Include in Report: `1212253230894980` (CHECKBOX)

### 107 - Variation Log (sheet `2963546479480708`) — built 2026-05-22

- Variation Title: `8234098962501508` (primary, TEXT_NUMBER)
- Variation ID: `629369738661764` (AUTO_NUMBER, prefix `107-VAR-`, fill `0000`)
- Date Raised: `5132969366032260` (DATE)
- Raised By: `2881169552347012` (CONTACT_LIST)
- Linked Stage: `7384769179717508` (PICKLIST, validation=true; Stage 1, 2A–2E, 3, 4, 5)
- Linked Building: `1755269645504388` (TEXT_NUMBER, optional, format S[N]-B[NN])
- Linked Unit: `6258869272874884` (TEXT_NUMBER, optional)
- Linked Contract: `4007069459189636` (TEXT_NUMBER, optional — refs 107 - Contract Register)
- Trade Package: `8510669086560132` (TEXT_NUMBER, free-text; review for picklist 2026-11-01)
- Variation Type: `347894761951108` (PICKLIST, validation=true; Scope/Cost/Programme/Quality/Other)
- Reason for Change: `4851494389321604` (PICKLIST, validation=true; Client request/Site condition/Design change/Council requirement/Consultant change/Other)
- Description: `2599694575636356`
- Cost Impact (NZD): `7103294203006852` (currency format set in UI)
- Programme Impact (days): `1473794668793732`
- Cost Band: `5977394296164228` (FORMULA — 4-tier as of 2026-05-23 Phase 2.5 v2 Section K.4): `=IF(ABS([Cost Impact (NZD)]@row) <= 5000, "Delivery Lead Approval", IF(ABS([Cost Impact (NZD)]@row) <= 25000, "GM Developments Approval", IF(ABS([Cost Impact (NZD)]@row) <= 50000, "CFO Co-Sign Required", "CEO Approval Required")))`
- Cost Category: `7411673995710340` (PICKLIST, validation=true, **added 2026-05-23**; options: Materials / Labour / Plant / Subcontractor / Design / Other)
- Variation Source: `1782174461497220` (PICKLIST, validation=true, **added 2026-05-23**; options: Client Request / Design Change / Site Conditions / Statutory | Consent / Error | Omission / Programme Acceleration / Other) — replaced legacy `Reason for Change` (was col `4851396389321604`, **deleted 2026-05-23**)
- Required Approval Level: `3725594482478980` (FORMULA: `=IF([Cost Band]@row = "Director Approval Required", "L2", "L1")`)
- Approval Status: `8229194109849476` (PICKLIST, validation=true; **9-state workflow as of 2026-05-22**: Draft / Submitted / Pricing / Pending Approval / Approved / Rejected / Issued / Built / Closed)
- L1 Approver (Delivery Lead): `910844715372420` (CONTACT_LIST) — **renamed from "L1 Approver (PM)" 2026-05-23**. Matt's role per §17 approval matrix (≤$5k tier).
- L1 Approval Date: `5414444342742916` (DATE)
- L2 Approver (GM Developments): `3162644529057668` (CONTACT_LIST) — **renamed from "L2 Approver (Director)" 2026-05-23**. Kyle's role per §17 approval matrix ($5k–$25k tier).
- L3 Approver (CFO): `7132107595091844` (CONTACT_LIST, **added 2026-05-23**). Julie's role per §17 approval matrix ($25k–$50k tier).
- L3 Approval Date: `1502608060878724` (DATE, **added 2026-05-23**)
- L4 Approver (CEO): `6006207688249220` (CONTACT_LIST, **added 2026-05-23**). Liam's role per §17 approval matrix (>$50k tier).
- L4 Approval Date: `3754407874563972` (DATE, **added 2026-05-23**)
- L2 Approval Date: `7666244156428164` (DATE)
- Final Approval Status: `2036744622215044` (PICKLIST, validation=true; Open/Approved/Rejected/Withdrawn)
- Final Approved By: `6540344249585540` (CONTACT_LIST)
- Final Approval Date: `4288544435900292` (DATE)
- Rejection Reason: `8792144063270788`
- Document Link: `207157273595780`
- Notes: `4710756900966276`
- Created: `2458957087281028` (DATETIME, CREATED_DATE system column)
- Modified: `6962556714651524` (DATETIME, MODIFIED_DATE system column)

### 107 - RFQ and Quote Register (sheet `5413487898480516`) — built 2026-05-22

> **Single sheet with parent/child rows.** Parents = RFQ (Type=RFQ); children indented under them = Quotes (Type=Quote). AUTO_NUMBER sequence is shared across both — parents and children take consecutive numbers.

- RFQ or Quote Name: `6869032728039300` (primary, TEXT_NUMBER) — parent: RFQ scope summary; child: Supplier name
- ID: `7048440491315076` (AUTO_NUMBER, prefix `107-RFQ-`, fill `0000` — retrofitted 2026-05-22)
- Type: `1418940957101956` (PICKLIST, validation=true; RFQ/Quote)
- Linked Stage: `5922540584472452` (PICKLIST, validation=true; Stage 1, 2A–2E, 3, 4, 5)
- Trade Package: `3670740770787204` (TEXT_NUMBER, free-text; review 2026-11-01)
- Scope Description: `8174340398157700`
- RFQ Issue Date: `855991003680644` (DATE — parent only)
- RFQ Due Date: `5359590631051140` (DATE — parent only)
- Suppliers Invited: `3107790817365892` (MULTI_CONTACT_LIST — parent only)
- RFQ Status: `7611390444736388` (PICKLIST, validation=true; Draft/Open/Quotes Received/Awarded/Cancelled — parent only)
- Supplier Name: `1981890910523268` (TEXT_NUMBER — child only; should match Supplier Register Trading Name)
- Supplier ID: `6485490537893764` (TEXT_NUMBER — child only; refs Supplier Register Supplier ID `5018996092211076`)
- Quote Submitted Date: `4233690724208516` (DATE — child only)
- Quote Amount (NZD): `8737290351579012` (child only)
- Quote Validity (days): `152303561904004` (child only)
- Quote Status: `4655903189274500` (PICKLIST, validation=true; Submitted/Shortlisted/Awarded/Declined/Withdrawn — child only)
- Award Date: `2404103375589252` (DATE — child only)
- Linked Contract: `6907703002959748` (TEXT_NUMBER — child only; refs 107 - Contract Register Contract ID)
- Document Link: `1278203468746628`
- Notes: `5781803096117124`
- Created: `3530003282431876` (DATETIME, CREATED_DATE)
- Modified: `8033602909802372` (DATETIME, MODIFIED_DATE)

### 107 - Contract Register (sheet `3948571190579076`) — built 2026-05-22

- Contract Title: `6447571882250116` (primary, TEXT_NUMBER)
- Contract ID: `4810677771603844` (AUTO_NUMBER, prefix `107-CON-`, fill `0000` — retrofitted 2026-05-22)
- Counterparty Name: `2558877957918596` (TEXT_NUMBER; should match Supplier Register Trading Name `515396464840580`)
- Counterparty ID: `7062477585289092` (TEXT_NUMBER; should match Supplier Register Supplier ID `5018996092211076`)
- Contract Type: `1432978051075972` (PICKLIST, validation=true; Construction/Civil/Supply/Consulting/Service/Other)
- Stages Covered: `5936577678446468` (MULTI_PICKLIST, validation=true; Stage 1, 2A–2E, 3, 4, 5)
- Trade Package: `3684777864761220`
- Linked RFQ: `8188377492131716` (TEXT_NUMBER; refs RFQ Register ID)
- Contract Value (NZD): `870028097654660` (currency format set in UI; signed value incl GST)
- Variations to Date (NZD): `5373627725025156` (plain TEXT_NUMBER initially; **pending UI conversion** to SUMIFS formula `=SUMIFS({VL Cost Impact}, {VL Linked Contract}, [Contract ID]@row, {VL Final Approval Status}, "Approved")` once cross-sheet refs created)
- Current Contract Value (NZD): `3121827911339908` (FORMULA: `=[Contract Value (NZD)]@row + [Variations to Date (NZD)]@row`)
- Contract Date: `7625427538710404`
- Practical Completion Date: `1995928004497284`
- Final Completion Date: `6499527631867780`
- Payment Terms: `4247727818182532`
- Retention %: `8751327445553028`
- Contract Status: `166340655878020` (PICKLIST, validation=true; Draft/Executed/In Progress/Practical Completion/Complete/Terminated/Disputed)
- Document Link: `4669940283248516`
- Insurance Verified: `2418140469563268` (CHECKBOX)
- Insurance Expiry: `6921740096933764` (DATE; manual entry — future: pull from Supplier Register `Insurance Status` formula col `322681181605764`)
- H and S Inducted: `1292240562720644` (CHECKBOX)
- Notes: `5795840190091140`
- Created: `3544040376405892` (DATETIME, CREATED_DATE)
- Modified: `8047640003776388` (DATETIME, MODIFIED_DATE)

### 107 - Decision Log (sheet `1863332356116356`) — built 2026-05-22

- Decision Title: `4227486107078532` (primary, TEXT_NUMBER)
- Decision ID: `3232522439004036` (AUTO_NUMBER, prefix `107-DEC-`, fill `0000` — retrofitted 2026-05-22)
- Date: `7736122066374532` (DATE)
- Forum: `2106622532161412` (PICKLIST, validation=true; Board/PCG/PM/Director/Other)
- Decision Type: `6610222159531908` (PICKLIST, validation=true; Budget/Programme/Design/Procurement/Sales/H&S/Governance/Other)
- Description: `4358422345846660`
- Decision Owner: `8862021973217156` (CONTACT_LIST)
- Status: `277035183542148` (PICKLIST, validation=true; Open/In Progress/Closed/Superseded)
- Closed Date: `4780634810912644` (DATE)
- Linked Document: `2528834997227396` (SharePoint URL)
- Notes: `7032434624597892`
- Created: `1402935090384772` (DATETIME, CREATED_DATE)
- Modified: `5906534717755268` (DATETIME, MODIFIED_DATE)

### 107 - Sales Register (sheet `8224519314427780`) — Phase 2.5 picklist expansion

- Sales Status: `4247873805127556` (PICKLIST, validation=true) — **9 options after Phase 2.5 expansion**: Not Available, Available, Application, Conditional, Unconditional, Transfer, Settled, Occupied, Clubhouse
- All other columns unchanged from Phase 2 build (see top-of-section sheet description for full inventory).

### 107 - Risk Register (sheet `1049548813193092`) — captured 2026-05-22 Phase 2.5

- Risk ID: `1657649895870340` (AUTO_NUMBER, prefix `107-RSK-`, fill `0000`)
- Risk Title: `4384452691398532` (primary)
- RAG: `8888052318769028` (PICKLIST RYGG, **FORMULA**: `=IF([Score]@row = "", "Gray", IF([Score]@row >= 15, "Red", IF([Score]@row >= 8, "Yellow", "Green")))`)
- Date Identified: `5974658469105540` (DATETIME, CREATED_DATE) — **added in Phase 2.5**
- Category: `6161249523240836` (PICKLIST: HS / Commercial / Environmental / Programme / Quality / Compliance / Stakeholder / Other)
- Risk Description: `3909449709555588`
- Likelihood: `8413049336926084` (PICKLIST: 1–5)
- Consequence: `1094699942449028` (PICKLIST: 1–5)
- Score: `5598299569819524` (**FORMULA**: `=[Likelihood]@row * [Consequence]@row`) — converted in Phase 2.5
- Current Controls / Mitigation: `3346499756134276`
- Owner: `7850099383504772`
- Status: `2220599849291652` (PICKLIST: Active / In Review / Closed)
- Last Reviewed: `6724199476662148` (DATE)
- Notes: `4472399662976900`

### 107 - Monthly RAG Log (sheet `8488689867902852`) — Phase 2.5 strip + 2026-05-23 rename

> **Sheet renamed 2026-05-23** from `107 - PCG Status Snapshot` to `107 - Monthly RAG Log` via REST API.

Remaining columns (12):
- Period Label: `8860005578346372` (primary)
- Period Date: `2962042024923012` (DATE)
- Is Current Period: `7465641652293508` (CHECKBOX, FORMULA: `=IF([Period Date]@row = MAX([Period Date]:[Period Date]), 1, 0)`)
- Overall RAG: `275018788671364` (PICKLIST RYGG)
- Submitted By: `7423969908264836` (CONTACT_LIST)
- Quality RAG: `1794470374051716` (PICKLIST — options Red/Yellow/Green/Gray; symbol RYGG application is UI follow-up)
- Programme RAG: `6298070001422212` (PICKLIST RYGG)
- Cost RAG: `4046270187736964` (PICKLIST RYGG)
- Health and Safety RAG: `8549869815107460` (PICKLIST RYGG)
- Sales RAG: `387095490498436` (PICKLIST RYGG)
- Maori Procurement RAG: `4890695117868932` (PICKLIST RYGG)
- Overall Commentary: `5862138337070980`
- **17 columns deleted in Phase 2.5** — see snapshot `smartsheet/snapshots/107-phase25-2026-05-22/pcg-snapshot-cut-columns-before.json` for the prior state and rationale.

### 107 - Construction Programme (sheet `4820480841174916`) — Phase 2.5 cuts

Remaining columns (17):
- Building Reference: `7746806653161348` (primary)
- Include in Report: `4413928406028164` (CHECKBOX)
- Building Name: `2117307118948228`
- Building Group: `3066359130132356` (FORMULA: derives stage prefix from Building Reference)
- Stage: `6620906746318724` (PICKLIST: Stage 1, 2A–2E, 3, 4, 5, Pavilion)
- Units: `4369106932633476`
- Unit Count: `8872706560003972`
- Typology: `76613537795972`
- Construction Status: `4580213165166468` (PICKLIST validation=true; **5-state as of 2026-05-22**: Not Started / Under Construction / Complete / On Hold / Cancelled — reduced from 8 options) — **canonical source for build status**
- Building Consent Numbers: `6832012978851716`
- % Complete: `7957912885694340` (GANTT_PERCENT_COMPLETE)
- RAG: `639563491217284` (PICKLIST RYGG)
- Start Date: `5143163118587780` (GANTT_START_DATE)
- End Date: `2891363304902532` (GANTT_END_DATE)
- Predecessors: `7585736319864708` (GANTT_PREDECESSOR)
- Duration: `1956236785651588` (GANTT_DURATION)
- Notes/Latest: `7394962932273028`
- **7 columns deleted in Phase 2.5**: Build Partner `2328413351481220`, Contract Package `1202513444638596`, Contract Price (incl GST) `5706113072009092`, Variations (incl GST) `3454313258323844`, Budget Approved `1765463398059908`, Expected Total Cost `6269063025430404`, Expected Variance `4017263211745156`. See `smartsheet/snapshots/107-phase25-2026-05-22/construction-programme-cut-columns-before.json`.

### 107 - Contract Register (sheet `3948571190579076`) — Phase 2.5 renames + cuts + add

Cols total: **22** (was 24; -3 cut, +1 added). Renames + adds:
- Counterparty Name → **Supplier Name** (col `2558877957918596`, title only changed)
- Counterparty ID → **Supplier ID** (col `7062477585289092`, title only changed)
- **New: Supplier Insurance Status** (col `806575861436292`, TEXT_NUMBER) — pending UI conversion to cross-sheet formula `=IFERROR(INDEX({SuppR Insurance Status}, MATCH([Supplier ID]@row, {SuppR Supplier ID}, 0)), "")`
- **Deleted in Phase 2.5**: Insurance Verified `2418140469563268`, Insurance Expiry `6921740096933764`, H and S Inducted `1292240562720644` (all empty; insurance lives on Supplier Register).

### 107 - RFQ and Quote Register (sheet `5413487898480516`) — Phase 2.5 add

Cols total: **23** (was 22; +1 added).
- **New: Quote ID** (col `224072465420164`, TEXT_NUMBER, index 2 — between ID and Type) — manual entry initially, convention `{Parent RFQ ID}-Q{nn}` e.g. `107-RFQ-001-Q01`.

### 107 - H and S Incidents and Observations (sheet `8305827340308356`) — Phase 2.5 picklist dedupe + 2026-05-22 AUTO_NUMBER conversion

- Entry ID: `6858878376775556` (TEXT_NUMBER, **systemColumnType=AUTO_NUMBER as of 2026-05-22**, prefix `107-HSE-`, fill `0000`, startingNumber=1). Existing 8 rows (OBS-001 through OBS-006, INC-001, INC-002) preserved; new rows auto-number as `107-HSE-0001` onwards.
- Type: `5732978469932932` (PICKLIST) — **"Lost Time Injury" option removed** (canonical is "LTI"). Final 6 options: Near Miss - Minor, Near Miss - Serious (PSIF), MTI, LTI, Observation, Other.

### 000 - Supplier Register (sheet `3313684242714500`) — key columns for cross-reference

> Inventoried 2026-05-22 (Phase 2 A.2) for use by RFQ and Contract Registers. Full column list has 43 entries; only the cross-reference columns captured here.

- Trading Name: `515396464840580` (primary, TEXT_NUMBER, locked)
- Supplier ID: `5018996092211076` (AUTO_NUMBER, no prefix — bare numeric)
- Legal Name: `2767196278525828`
- NZBN: `7270795905896324`
- Type: `1641296371683204` (PICKLIST: Consultant/Subcontractor/Supplier/Build Partner)
- Trade or Service Category: `6144895999053700` (PICKLIST, 26 options incl. Building/Civil/Earthworks/Electrical/etc)
- Status: `3893096185368452` (PICKLIST: Active/Inactive/Preferred/Blacklisted)
- Contact Name: `1078346418261892`
- Phone: `5581946045632388`
- Email: `3330146231947140`
- Insurance Status: `322681181605764` (PICKLIST RYG, FORMULA — auto-derived from all expiry columns; Red if any insurance type expired or all blank, Yellow if any expires within 30 days, Green otherwise)
- KPV H and S Compliance: `7939298975584132` (PICKLIST: Pending/Approved/Expired/Not Required)
- KPV Trading Terms Agreed: `620949581107076` (PICKLIST: Pending/Agreed/Declined)

---

## Anomalies flagged at audit

**Closed in 2026-05-22 Phase 1 cleanup:**

- ✅ Stray top-level reports in 107 (`107 - Construction Program` `5093377811894148`, `Untitled report` `1730274806157188`) — deleted.
- ✅ `02 - Civil and Construction / Archive` folder `6798331356702596` — deleted (was empty).
- ✅ `03 - Sales and Marketing` folder `1801164825094020` — deleted; Sales Register moved to 01 - Project Control.
- ✅ `04 - Health and Safety` renumbered to `03 - Health and Safety`.
- ✅ Host correction: `app.smartsheet.com` (NA). Convention docs, SKILL.md, capabilities doc updated.
- ✅ `107 - Resource Consent Register` `1643703515959172` deleted (intentional — consent status lives on Construction Register now).
- ✅ Civil Programme + Construction Programme: decision locked to keep separate; conventions doc §7 updated.

**Closed in 2026-05-22 Phase 2.5 structural cleanup:**

- ✅ Unit Register Typology picklist trimmed — removed Harris SG / Robertson DG / Robertson SG / Stanaway DG / Stanaway SG (none in use).
- ✅ Unit Register manual data cols cut — Beds / Garage / Attachment Type / Floor Area. UI follow-up to reinstate as cross-sheet formulas from Typology Register.
- ✅ Unit Register + Sales Register Sales Status picklists expanded to 9 options (added Conditional, Transfer, Occupied).
- ✅ Risk Register Score column → formula `=L*C`; RAG column → derived-from-Score formula. RSK-0012 flipped Green→Yellow as a result. New `Date Identified` CREATED_DATE column added.
- ✅ PCG Status Snapshot stripped 29→12 cols (8 narrative blocks + 6 derivable count cols + Top Risks Summary + Board Resolutions This Period removed). Quality RAG options standardised to Red/Yellow/Green/Gray.
- ✅ Construction Programme stripped 24→17 cols (Build Partner + 5 financial cols + Contract Package removed). Programme is now timeline-only per architectural rule.
- ✅ Contract Register: Counterparty Name/ID → Supplier Name/ID renamed; 3 insurance/H&S cols cut; `Supplier Insurance Status` placeholder added (UI follow-up converts to cross-sheet formula).
- ✅ RFQ Register: `Quote ID` column added at index 2 (manual entry initially).
- ✅ H&S Incidents Type picklist deduped — "Lost Time Injury" removed (canonical is LTI).

**Closed in 2026-05-23 Phase 2.5 v2 finalisation (via REST API):**

- ✅ Section A folder restructure — 7-folder target achieved (Dashboards / Project Control / Sales / Procurement / Civil and Construction / H&S / Reports). 2 new folders created, 4 sheets moved, 3 folders renamed, 4 reports + 1 sub-folder moved into Reports/Internal, 1 report moved into Reports/External, old `06 - Reports External` folder deleted.
- ✅ Section B sheet rename — `107 - PCG Status Snapshot` → `107 - Monthly RAG Log` via PUT /sheets/{id}.

**Still open from Phase 2.5:**
- **Quality RAG symbol (Section F.1)** — `Quality RAG` column on PCG Status Snapshot has correct options (Red/Yellow/Green/Gray) but no symbol. API refused to set `symbol: RYGG` due to existing "Green" cell value coercion. Kyle to clear the cell in UI, set symbol, then re-enter "Green".
- **Civil Programme financials (Section I)** — DEFERRED. Civil Programme still carries the Matco Stage 1 civils contract values (Civil Contractor, Civils Budget, Contracted Price, Budget Variance, Variations to Date, Total Cost). Kyle to populate Contract Register with the Matco row first, then we cut these in a follow-up.
- **Chart Source — Construction Progress (Section P)** — named range `{Construction Programme Is Unit}` is **broken** (Construction Programme has no `Is Unit` column). Named range `{Construction Programme Status}` likely points to the actual `Construction Status` column (misleadingly named). Both need UI repair via right-click column → Edit Column Formula → Edit Reference. Likely the COUNTIFS in `Stage 1 Count` is returning 0 because the broken range can't match `=1`.
- **Sales Status formula migration (Phase 1 carryover)** — Unit Register Sales Status PICKLIST still hand-maintained. UI needs cross-sheet refs `SR Sales Status` + `SR Unit Number` created, then column converted to formula.
- **Cross-sheet formula conversions on Construction Register (Section J)** — Build Partner from PICKLIST → cross-sheet formula from Supplier Register. Contract Price → cross-sheet formula from Contract Register. Post Contract Variations → SUMIFS from Variation Log. All UI-only.
- **Construction Register may need a Building Reference column** if Contract Register goes per-building (Section M.7 — deferred decision).
- **Sales Status duplication** still open until UI work is done. PICKLIST natively maintained on both UR and SR.
- **`{107 Construction Status}` named range** still lacks `CR`/`CP` prefix — Phase 1 open item carried forward.

**Still open:**

- **Misfiled report**: report `104 - Sale Variance Watch` (id `3871985162473348`) lives inside `105 - Rototuna / 105 - Reports` — wrong village prefix. Same finding in 2026-05-10 and 2026-05-22 audits.
- **Orphan summary sheet**: `104 - Design Status Summary` (sheet `7302384400158596`) inside `104 - Reports`. Per brief, these were earlier mistakes; matching report `104 Design Status` already exists.
- **"Untitled report"** entries in 104, 105, 106 Reports folders: 104/Reports `6472306070081412`, 105/Reports `6159053100109700`, 106/Reports `6747321415978884`. (107 cleaned up.)
- **`Copy of 107 - PCG - H&S Monthly Indicators - Lead`** (id `4807577668898692`) — pending UI rename to `107 - PCG - H&S Lead Indicators` (decision made 2026-05-22, kept because it's a deliberate Lead-indicator variant, not a stale duplicate).
- **107 Construction Programme rebuild**: old per-unit sheet `5063906232848260` was already archived/removed earlier; new per-building sheet `4820480841174916` is live. Column IDs for the new sheet not yet captured (re-audit before next active use).
- **Sales Status duplication-of-truth**: PICKLIST exists natively on both `107 - Sales Register` and `107 - Unit Register`, both hand-maintained. Phase 2 to make Sales Register canonical and convert Unit Register's column to a formula.
- **Ambiguous named range `{107 Construction Status}`** used by Unit Register + Sales Register Build Status. No `CR`/`CP` prefix — UI confirmation needed.

---

## Inventory totals (2026-05-22)

- Workspaces: 8 (KPV-related: `000`, `104`, `105`, `106`, `107`, `KPV - Project Finance`, `XXX`; non-KPV: `2CP`)
- Folders: ~25
- Sheets (data): ~50
- Reports: ~55
- Dashboards: 3 (`107 - Dashboard`, `107 - PCG Dashboard`, plus one in 104 — `1718153349752708`)

---

## How to get column IDs

Smartsheet column IDs are stable across row deletions/additions. Pull current state with:

```bash
curl -H "Authorization: Bearer $SMARTSHEET_API_TOKEN" \
  https://api.smartsheet.com/2.0/sheets/{SHEET_ID}/columns
```

Or via the MCP `get_columns` tool.

Never guess column IDs — always confirm from the live sheet.

---

## Re-audit checklist

Per brief Section 3, every session begins with a fresh audit:

1. `search_smartsheet` for terms: `Overview`, `Drury`, `Rototuna`, `Waihi`, `Papamoa`, `Template`, `Karaka`
2. `browse_workspace` for each workspace ID
3. `browse_folder` for each folder
4. Capture each asset's `asset_id`, name, and URL prefix (`/sheets/`, `/reports/`, `/dashboards/`)
5. Flag naming drift, orphan sheets, untitled assets, missing standard sheets, duplicate names

If the brief on a task contains pre-supplied sheet IDs, validate them against the fresh audit — three of four IDs in the 2026-05-10 budget brief did not exist (had been recreated).

---

## Known Smartsheet quirks (observed during builds)

### Parent date rollup on hierarchical Gantt sheets

On the 107 Civil Programme, **End Date** has no column-level rollup formula — it's a static value computed at the moment children are first added. When new descendants are added later at deeper levels, the End Date does not auto-recompute up the chain.

- **Start Date** has formula `=MIN(CHILDREN())` and rolls up correctly.
- **End Date** is static — must be force-updated.
- **Duration** has formula `=CALCDURATION([Start Date]@row, [End Date]@row)`.

**Workaround**: writing a value to the parent's `Start Date` overrides the rollup formula and forces Smartsheet to recompute Duration from the new Start + existing End. This is the only reliable way to fix a stuck End Date when API can't write End directly (dependency-enabled sheets reject direct End writes).

When building a multi-level hierarchy from scratch, **add children in the order their date ranges should span**. The first child sets the initial parent dates; subsequent children may not extend them automatically.

### End Date writes rejected on dependency-enabled sheets

API returns error 1080: "End Dates on dependency-enabled sheets cannot be created/updated. Please update either the Duration or Start Date column."

For leaf rows: write Start Date and Duration; End Date auto-computes.
For parent rows: write Start Date directly (overrides rollup) or write Duration (will adjust End via CALCDURATION).

### Successful update with silent override

Smartsheet API returns `message: SUCCESS` even when a cell write was silently overridden by a formula on the column. The response will show the formula in the cell, not the value you wrote. Always verify with a re-fetch after writes to dependency-controlled columns.

---

## Reference documents

| Document | Path | Purpose |
|---|---|---|
| `Budget sales figures.xlsx` | `smartsheet/input/Budget sales figures.xlsx` | List Price + Start dates source for UR/CCP loads across 4 villages (KLE/Papamoa/Rototuna/Waihi Beach tabs) |
| `225269 KPV Simpson Rd Stage 1 - NZS3910 Contract Document (1).pdf` | `smartsheet/input/` | Source for 107 Civil Programme Contracted Price (incl GST). Matco contract awarded 19 July 2024. Lysaght Ref 225269. Schedule of Prices broken into SP1 Earthworks + SP2 Civils. Total $1,299,203.00 excl GST. |
