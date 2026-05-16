# KPV Smartsheet Registry

**Last updated:** 2026-05-11 (snapshot from session-start audit; IDs change — re-audit each session per brief Section 3)

---

## Account

| Field | Detail |
|-------|--------|
| Account | KPV's own Smartsheet account |
| Working API token | `smartsheet/input/Smartsheet API.txt` (37-char token, valid as of 2026-05-10) |
| `config/.env` | Token stored there is **stale/invalid** — needs rotation; do not use without re-fetching |
| Token owner | kyle@karakapines.co.nz |

---

## Workspaces (6)

| Workspace | ID |
|---|---|
| `000 - Overview` | `1167040628189060` |
| `104 - Drury - KLE` | `5737366867470212` |
| `105 - Rototuna` | `2189930039404420` |
| `106 - Waihi Beach` | `1169583248828292` |
| `107 - Papamoa` | `4481862027503492` |
| `XXX - Village Template` | `5525504720693124` |

---

## Folders

| Workspace | Folder | ID |
|---|---|---|
| 000 - Overview | Master Registers | `5644631200294788` |
| 104 | 02 - Civil and Construction | `3758934398920580` |
| 104 | 104 - Reports | `4407440100878212` |
| 105 | 02 - Civil and Construction | `7227511332464516` |
| 105 | 105 - Reports | `4041126635169668` |
| 106 | 02 - Civil and Construction | `4423756681635716` |
| 106 | 106 - Reports | `5523268309411716` |
| 107 | 02 - Civil and Construction | `2549523147974532` |
| 107 | 107 - Reports | `1382941310904196` |

---

## Sheets — Master Registers (000 - Overview)

| Sheet | ID | Notes |
|---|---|---|
| Exterior Scheme Register | `638139734380420` | |
| F&F Register | `7182086124294020` | |
| Interior Scheme Register | `3138605269602180` | |
| KPV Risk Register | `499689920089988` | **Created 2026-05-12** from `smartsheet/input/2.0 KPV_Manager_Risk_RAG_Dashboard.xlsx`. 17 cols × 13 risk rows (FM-001 to FM-013). Formula columns: Inherent Score (L×C), Inherent RAG (Red/Yellow/Green based on score with RYGG symbol), Residual Score, Residual RAG. Picklists: Category (10 opts incl. Strategic, Regulatory, Financial, Governance/Conflicts etc.), Owner (Board/CEO/CFO/Fund Manager/GM Compliance/Fund Admin/AML Officer/External Counsel/Ext Provider), Likelihood/Consequence (1-5), Control Effectiveness (Weak/Adequate/Strong), Trend (Improving/Stable/Worsening), Status (Open/Closed/On Hold). Current portfolio position: 3 Red residual (FM-002 AML/CFT, FM-004 Conflicts, FM-010 Key person), 5 Amber, 5 Green. |
| KPV Risk Actions | `8345066161524612` | **Created 2026-05-12** — companion to KPV Risk Register. 7 cols × 14 mitigation actions (A-001 to A-015, gap at A-012). Risk ID picklist links to Register. Days to Due formula `=IFERROR([Due Date]@row - TODAY(), "")`. Status picklist: Not Started/In Progress/Complete/Closed/On Hold. |
| Status Register | `6181671203196804` | |
| Supplier Register | `3313684242714500` | |
| Typology Register | `4159669319716740` | |
| Village Register (portfolio) | `4900490847408004` | **Identified 2026-05-13** via 107 Dashboard widget probe. Portfolio-level master, 16 cols. Primary = Village Code. Captures Region (BOP/WKT/AKL/CAN), Land Area (ha), Address, Operating Status (Pre-development/Under Construction/Operating/Mixed), Active Insurance Policies, Insurance Status, Earliest Policy Renewal, Total Insured Value, Open/Overdue Compliance Items, Next Compliance Due, Compliance RAG (RYGG), Notes. Dashboard reads Land Area = 7.265 ha from the Papamoa row. Folder location not yet confirmed — likely sits in 000 - Overview / Master Registers. |

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

---

## Sheets — 105 Rototuna

| Sheet | ID | Worked on |
|---|---|---|
| 105 - Civil Programme | `7961358078267268` | **Loaded 41-row section-level hierarchy** (2026-05-11): 4 stage parents (Stg1, Stg2-3, Stg3 Wright SP1+SP3, Stg4) + 8 sub-parents (Earthworks/Civils per stage, with Stg3 split into SP1+SP3) + 29 section leaves. Builders: Online Contractors (2016) Ltd (Stg1), [TBC] (Stg2-3 future), Wright Civil Limited (Stg3 actual), Matco Civil Contractors Limited (Stg4). Stg1 total: **$1,177,431.65 incl GST** (contracted) / $1,413,350 budget = -$235,918.35 variance. Stg3 (Wright): **$735,923.62** contracted + **$232,344.09** variations = **$968,267.71** total (note: template flagged Claim 10 certified $1,150,551.45 / total claimed $1,501,860.80 with $351,309.35 deduction dispute). Stg4: **$465,497.59 incl GST** (Matco — Cut to Waste at Borman Road, Hamilton — contract 183983/4 dated 25/2/26). Schema was already 107-aligned (Civils Budget, Contracted Price, Budget Variance formula, Variations to Date, Total Cost formula). Picklists expanded: Stage adds "Stage 2-3"; Civil Contractor adds Online Contractors / Wright Civil / Matco / Dempsey Wood / [TBC]. |
| 105 - Construction Programme | `75158441119620` | **Reloaded** with 800-row hierarchy (4 top + 4 sub + 132 units + 660 phase children); 100 Foundation Starts from budget (Stage 1A/1B added to picklist) |
| 105 - Unit Register | `1096218196266884` | **Loaded** 137 rows; Unit Numbers later text-fixed (numeric→string); 104 of 104 List Prices applied |

---

## Sheets — 106 Waihi Beach

| Sheet | ID | Worked on |
|---|---|---|
| 106 - Civil Programme | `4813421928206212` | **Reloaded with 24-row hierarchy** (2026-05-12): deleted 41 incorrect rows that were copy-pasted from 105. Loaded 1 stage parent (Stage 1 EW & Civil Contract – SP1, SP2 & SP3) + 3 sub-parents (SP1 Stage 1 Earthworks; SP2 Stage 1A Civil Works; SP3 Stage 1B Civil Works Provisional) + 20 section leaves (SP1: 100/200/300/400; SP2 & SP3: 100/200/300/400/500/600/700/800 each). Contractor: **RZG**. Contract 183864, Lysaght (Peter Moodie) QS / Crowther & Co bank QS, tender awarded 30/11/2021, site possession 06/12/2021. SP1 LDs $800/day from 01/06/2022. Lender: ASB. **Parent total $3,406,359.64 incl GST contracted vs $2,896,947.75 budget = +$509,411.89 OVER-BUDGET variance**. SP1 $1,548,445.05 / SP2 $958,275.71 / SP3 $899,638.87. Picklists expanded: Stage adds 1A/1B; Civil Contractor adds RZG. |
| 106 - Construction Programme | `7130063131594628` | **Reloaded** with 32-row hierarchy (1 top + 1 sub + 5 units + 25 phase children); 2 Foundation + 2 Practical Start budget updates (only 5 unit rows in source) |
| 106 - Unit Register | `4460551978569604` | **Loaded** 105 rows; Unit Numbers later text-fixed (numeric→string); 75 of 96 List Prices applied; Stage picklist added 1A/1B |

---

## Sheets — 107 Papamoa

| Sheet | ID | Worked on |
|---|---|---|
| 107 - Civil Programme | `6233992763232132` | **Restructured to 14-row section-level hierarchy** (2026-05-11): Contract Award milestone + Stage 1 Civils top parent + SP1 Earthworks sub-parent (3 section leaves: 100/200/300) + SP2 Civils sub-parent (7 section leaves: 100/200/400/500/600/700/800). All Contracted Price (incl GST) populated, reconciles to **$1,494,083.45 incl GST** ($1,299,203 excl × 1.15) per NZS3910 contract with Matco Civil Contractors awarded 19 July 2024 (Lysaght Ref 225269). Includes +$19,110 post-tender adjustment (Item 504 WW connection rate). 900/1000 sections (unscheduled/dayworks) omitted from rows. |
| 107 - Construction Programme | `5063906232848260` | Tidied to 658 rows (manual + script). 114 List Prices on UR; 106 Foundation Start + 106 Practical Start from budget. |
| 107 - Resource Consent Register | `1643703515959172` | |
| 107 - Unit Register | `5289542339743620` | 114 of 114 List Prices applied (Papamoa budget). Has both `Sales Status` (PICKLIST: Not Available/Available/Application/Unconditional/Settled) AND `Construction Status` — note the dashboard "Sales Overview" tile block reuses Construction Status counts for "Units" and "On Hold" tiles, so the section grouping is mixed (see chart-buildspec appendix). |
| 107 - Sales Tracking | `8224519314427780` | **Identified 2026-05-13** via dashboard probe. 14 cols, primary = Unit Number. Cross-sheet formulas: Stage / Typology via INDEX/MATCH from Unit Register Range; Build Status via INDEX/MATCH on Construction Status. Native columns: Sales Status (PICKLIST), Application Strength (RYGB symbol picklist), Settlement Date (Expected Date), Budget Sale Price (incl GST), List or Sold Price (incl GST), Sale Price Variance (formula), Sale Variance Flag (DIRECTIONS_3_WAY formula picklist Up/Unchanged/Down), Notes, Latest Comment, Include in Report. Source for `107 - Sales Report - Expanded` and dashboard Avg List Price tile ($914,514.87). **Duplication risk**: Sales Status also exists on Unit Register — confirm which is canonical. |
| 107 - H&S Monthly Indicators | `3104570405244804` | **Identified 2026-05-13** via dashboard probe. 19 cols × 5 rows (Jan–May 2026; only April populated). Primary = Entry Label (e.g. "April 2026"); paired with Period Start / Period End / Record ID / Contractor (PICKLIST: KPV/Signature Homes/Matco Civil/BaseUp/AmpT/Out the Gate/Downey Construction/Home Construction/Other) / Submitted By (CONTACT) / Date Submitted. KPI columns: Inductions, Contractor Audits, Internal Audits PM, Internal Audits DM, External Inspections, Near Miss Minor, Near Miss Serious PSIF, MTI, LTI, LTI Days, Observations Narrative, Notes. Drives dashboard widget [9] via SUMIF on Entry Label = [Current Period]#. Apr 2026 row: Inductions 17, Contractor Audits 7, Near Miss Minor 2, all others 0. |

### 107 Reports and Dashboard

| Asset | ID | Type | Folder | Notes |
|---|---|---|---|---|
| 107 - Dashboard | `3236074114836356` | dashboard | workspace root | 10 widgets, dark navy `#131F39` background, 90-col grid. Two sections: Sales Overview + Construction Overview. **No chart widgets** — all metric tiles and report grids. Pulls from: Village Register (Land Area), Unit Register (sales status + total units), Construction Programme (% complete buckets), Sales Tracking (Avg List Price), H&S Monthly Indicators (10 KPI tiles), 107 - Papamoa - Signature Report, 107 - Sales Team Report. See `plans/Stage 1 Papamoa/pcg-report-dashboard-chart-buildspec.md`. |
| 107 - Papamoa - Signature Report | `6144240361885572` | report | 04 - Reports External | Per-unit construction grid: Primary, Construction Status, Stage, Typology, RAG, % Complete, Start/End Dates, Duration. 29 rows (Stage 1 hierarchy + units + phases). External-facing, shared with Signature Homes. Drives Construction Overview widget on dashboard. |
| 107 - Sales Team Report | `8674117833150340` | report | 03 - Reports Internal | Per-unit sales grid embedded in dashboard Sales Overview widget. Sourced from 107 - Sales Tracking. |
| 107 - Sales Report - Expanded | `1830541908201348` | report | 03 - Reports Internal | 11 cols × 23 rows from 107 - Sales Tracking. Adds Budget Sale Price + Sale Price Variance + Sale Variance Flag (DIRECTIONS_3_WAY) vs the Sales Team Report. Use this for variance-focused board reporting. |
| 107 - Design Report | `7555536550580100` | report | 03 - Reports Internal | |
| 107 - Risk Report | `2047711023943556` | report | 03 - Reports Internal | 13 cols × 14 rows (107-RSK-0001 → 0014). All risks currently Yellow RAG. Note: RSK-0003 records the gap between PCG report (showed 0 near misses in April) and Signature Homes' own data (recorded 2). Source sheet: `1049548813193092` — **not yet in registry**, add. |
| 107 H&S Monthly Report | `794965968899972` | report | 03 - Reports Internal | 14 cols × 5 rows (Jan–May 2026) from 107 - H&S Monthly Indicators (`3104570405244804`). |
| 107 - H&S Open Items Report | `8821624189964164` | report | 03 - Reports Internal | |
| 107 Consent Status Report | `6547943396953988` | report | 03 - Reports Internal | |

### 107 Folders

| Folder | ID |
|---|---|
| 01 - Project Control | `4066520629307268` |
| 02 - Civil and Construction Programmes | `2549523147974532` |
| 03 - Reports Internal | `1382941310904196` |
| 04 - Reports External | `6714388368385924` |
| 05 - Health and Safety | `1401823060879236` |

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

### 107 - Unit Register (sheet `5289542339743620`)
- Unit Number: `5749561909088132` (primary)
- Construction Status: `3779237072113540`
- List Price (incl GST): `260799863230340`

### 107 - Construction Programme (sheet `5063906232848260`)
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

---

## Anomalies flagged at audit (2026-05-10)

- **Naming drift**: report `104 - Sale Variance Watch` (id `3871985162473348`) lives inside `105 - Rototuna / 105 - Reports` — wrong village prefix.
- **Orphan summary sheet**: `104 - Design Status Summary` (sheet `7302384400158596`) inside `104 - Reports`. Per brief, these were earlier mistakes; matching report `104 Design Status` already exists.
- **"Untitled report"** entries in 104, 105, and 106 Reports folders.

---

## Reports (38 total)

Reports were enumerated in the session-start audit but not used directly. They live in each village's `XXX - Reports` folder. Re-audit if you need specific report IDs.

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
