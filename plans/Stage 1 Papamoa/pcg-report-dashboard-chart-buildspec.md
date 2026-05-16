# 107 Dashboard — Chart Widget Build Spec

**Dashboard:** `107 - Dashboard` (id `3236074114836356`)
**URL:** <https://app.smartsheet.com/dashboards/MgV3W8XJrMJHRrv4gmpmJ3cj3QvHQVggGFM75g71>
**Purpose:** Add the 7 missing chart widgets that the redesigned PCG monthly report (see `pcg-report-redesign-powerpoint-template.md`) depends on.
**Method:** **Smartsheet UI** — the API does not expose dashboard widget CRUD, so each chart must be built manually in Smartsheet. Estimated time: 15–20 minutes once data sources are in place.
**Last updated:** 2026-05-13

---

## Current dashboard state

10 widgets: 2 section banners + 2 report grids + 5 metric tile blocks + 1 H&S monthly indicator block. **Zero chart widgets**.

| Layout y | Widget | Type |
|---|---|---|
| 0 | Land Area / Total Units metrics | METRIC |
| 4 | "Sales Overview" banner | TITLE |
| 7 | Sales report (Sales Team Report) | REPORT GRID |
| 7 | Sales status counts (7 tiles) | METRIC |
| 24 | Avg List Price | METRIC |
| 58 | "Construction Overview" banner | TITLE |
| 61 | Construction report (Signature Report) | REPORT GRID |
| 61 | Unit completion counts (4 tiles) | METRIC |
| 74 | H&S Monthly Indicators (10 tiles) | METRIC |

This spec adds 7 chart widgets covering the visualisations the PCG report needs.

---

## Charts to build

### Chart 1 — Sales Pipeline donut

**Purpose:** Pipeline status at a glance for the Sales section of the report.

**Smartsheet config:**
- Widget type: **Chart → Donut** (or Pie if Donut not available in the UI)
- Data source: sheet `8224519314427780` (`107 - Sales Tracking`)
- Source range: `Sales Status` column, all rows
- Aggregation: count by category
- Categories (order): Settled, Unconditional, Application, Available, Not Available
- Colour mapping:
  - Settled → dark green `#1F7A1F`
  - Unconditional → light green `#7AC97A`
  - Application → amber `#F4B400`
  - Available → light grey `#C9C9C9`
  - Not Available → dark grey `#6B6B6B`
- Title: "Sales Pipeline"
- Show data labels: counts + percentages

**Placement:** Above current widget [1] sales status tiles (or replace tiles). Suggest y≈10, span left half.

**Alternative if Smartsheet UI lacks donut counts directly:** create 5 sheet-summary COUNTIF fields on the Sales Tracking sheet (one per status) and source the chart from those — same approach the current dashboard uses for metric tiles.

---

### Chart 2 — Cumulative settlements vs target (combo)

**Purpose:** Are sales pace and value tracking the budget?

**Smartsheet config:**
- Widget type: **Chart → Column + Line combo** (use stacked column if combo not native)
- Data source: a new sheet `107 - Monthly Sales Snapshot` (to be created — see "Prerequisites" below)
- X-axis: Period (months, e.g. Jan 2026 → Dec 2027)
- Series:
  - Bar series: `Settlements this month` (count) — dark green
  - Line series 1: `Cumulative settlements (actual)` — solid blue
  - Line series 2: `Cumulative settlements (target)` — dashed grey
- Optional: secondary y-axis with `$ value cumulative` as line if dual-axis is supported
- Title: "Settlements — actual vs target"
- Show data labels: on bars only

**Prerequisites:**
- Create `107 - Monthly Sales Snapshot` sheet with cols: Period (date), Settlements (count), Cumulative Settled (formula), Cumulative Value (formula), Target Settled (manual), Target Value (manual)
- Populate one row per month going forward; backfill from Settlement Date column on Sales Tracking

**Placement:** Right half of Sales Overview section, y≈10.

---

### Chart 3 — Construction % Complete by block

**Purpose:** Replace the "Programme Milestones" hard-coded table with a live progress chart.

**Smartsheet config:**
- Widget type: **Chart → Horizontal Bar** (stacked: Complete vs Remaining)
- Data source: report `6144240361885572` (`107 - Papamoa - Signature Report`) — already filtered to unit-level rows
- Categories (Y-axis): Unit number / block
- Values (X-axis):
  - Series 1: `% Complete` (0–100)
  - Series 2: `100 - % Complete` (stacked, light grey, the "remaining")
- Colour: bar coloured by RAG (Green/Amber/Red/Grey) — use the existing `RAG` column from the report
- Sort: by Stage, then Unit Number
- Title: "Construction — % Complete by block"
- Show data labels: % only on the completed segment

**Alternative if Smartsheet bar chart can't read directly from a report:** point the chart at sheet `5063906232848260` (Construction Programme), filtered to `Is Unit = 1`.

**Placement:** Top of Construction Overview section, y≈61, spans wider (left 2/3 of grid).

---

### Chart 4 — H&S Monthly trend (stacked column)

**Purpose:** Replace the static H&S table with a 6-month rolling trend.

**Smartsheet config:**
- Widget type: **Chart → Stacked Column**
- Data source: sheet `3104570405244804` (`107 - H&S Monthly Indicators`)
- X-axis: Entry Label (Jan 2026 → current month)
- Stacked series (one column per month):
  - Inductions — blue
  - Contractor Audits — light blue
  - Internal Audits (PM + DM) — teal
  - Near Miss Minor — amber
  - Near Miss Serious (PSIF) — red
  - MTI — dark red
  - LTI — black
- Title: "H&S monthly indicators"
- Show data labels: only on Near Miss / MTI / LTI (highlight risk events)

**Placement:** Below current H&S metric tile block (widget [9]), y≈85.

**Note:** Currently only April has data populated. As more months are entered, the chart auto-extends.

---

### Chart 5 — Risk Heat Map

**Purpose:** All active risks plotted on a 5×5 likelihood × consequence grid.

**Smartsheet config:**
- Widget type: **Chart → Scatter** (or Bubble if available)
- Data source: report `2047711023943556` (`107 - Risk Report`) — or its source sheet (`1049548813193092` — currently not in sheet registry, add)
- X-axis: Likelihood (1–5)
- Y-axis: Consequence (1–5)
- Bubble size (if Bubble chart): 1 (uniform) — purpose is position not magnitude
- Colour: by `RAG` column (Red / Amber / Green / Yellow)
- Data labels: Risk ID (e.g. "RSK-0004")
- Title: "Risk Heat Map"

**Prerequisites:**
- Confirm Likelihood and Consequence are stored as numbers (1–5), not text — they are stored as TEXT_NUMBER picklists "3", "4" etc. which should chart correctly. Verify in Smartsheet UI.

**Alternative if Smartsheet doesn't support scatter on a dashboard:** build a 5×5 grid table widget where each cell shows count of risks at that L×C position via formula.

**Placement:** New section banner "Risk Overview" at y≈100, plus chart at y≈103.

---

### Chart 6 — Budget vs Certified (horizontal bar)

**Purpose:** Replace the two big numbers on the current report with a visual comparison.

**Smartsheet config:**
- Widget type: **Chart → Horizontal Bar**
- Data source: a new sheet `107 - BBD Drawdown Snapshot` (recommended) — or paste-update each month manually
- Categories (Y-axis): Stage 1 Civil, Stage 2 Civil, [future stages]
- Series:
  - `Budget` — dark blue
  - `Certified to date` — green
  - `Contingency` — amber (small bar appended)
- Title: "Budget vs Certified — Civil"
- Show data labels: $ values

**Prerequisites:**
- Decide where BBD data lives (per Open Question 2 in the report spec). Recommend a 2-col + period sheet (`Stage`, `Period`, `Budget`, `Contingency`, `Certified to Date`, `To Complete`) so it's chartable.

**Placement:** Add a new "Cost" section to the dashboard at y≈40 (between Sales and Construction sections).

---

### Chart 7 — RAG status tile row (header)

**Purpose:** Replace the image-based RAG cover page on the current Word report with live, data-driven tiles.

**Smartsheet config:**
- Widget type: **6 × METRIC tiles** (not technically a chart, but listed here as a coordinated build)
- Data source: a new sheet `107 - Monthly RAG`
  - Cols: `Period`, `Quality`, `Programme`, `Cost`, `H&S`, `Sales`, `Māori`
  - Each RAG col: PICKLIST with RYGG symbol (`Red / Yellow / Green / Gray`)
  - Sheet summary fields: `Current Quality RAG = INDEX(Quality:Quality, MATCH([Current Period]#, Period:Period, 0))` — one per category
- Each tile: metric widget pointing at one summary field, with conditional formatting on tile background by RAG colour
- Title each tile: "Quality" / "Programme" / "Cost" / "H&S" / "Sales" / "Māori"

**Placement:** Very top of dashboard, above current Land Area / Total Units row. Move existing top tiles down.

**Why a sheet not picklists in summary directly:** keeping history of RAG status month-over-month enables a future "RAG trend" line chart and a historical audit trail.

---

## Build sequence (suggested order)

| # | Build | Why first |
|---|---|---|
| 1 | Chart 1 (Sales donut) | Quick win, no new sheets needed |
| 2 | Chart 3 (Construction % bar) | Quick win, no new sheets needed |
| 3 | Chart 4 (H&S trend) | Quick win, no new sheets needed |
| 4 | Chart 7 (RAG tiles) | Needs new RAG sheet but it's small and unlocks the cover slide |
| 5 | Chart 5 (Risk heat map) | Risk Register source sheet already exists |
| 6 | Chart 6 (Budget vs Certified) | Needs BBD snapshot sheet — decision needed first |
| 7 | Chart 2 (Cumulative settlements) | Needs Monthly Sales Snapshot sheet — biggest setup cost |

Steps 1–3 can be done in ~30 minutes total with no new sheets.

---

## Appendix A — Widget [1] labelling concern

**Observation:** The "Sales Overview" section contains a metric tile block (widget [1]) where the first two tiles are not strictly sales-status metrics:

| Tile label | Field counted | Should it be in Sales Overview? |
|---|---|---|
| Units | Construction Status = Complete = 11 | **No** — this is a construction metric |
| On Hold | Construction Status = On Hold = 0 | **No** — this is a construction metric |
| Not Available | Sales Status = Not Available = 4 | Yes |
| Available | Sales Status = Available = 6 | Yes |
| Application | Sales Status = Application = 5 | Yes |
| Unconditional | Sales Status = Unconditional = 1 | Yes |
| Settled | Sales Status = Settled = 6 | Yes |

The data feeds are technically correct (COUNTIFs are valid); the issue is that two Construction Status counts have been bundled into a Sales Overview tile block.

**Recommendation:**
- Move the `Units (Construction Complete)` and `On Hold (Construction Status)` tiles to the Construction Overview section, next to the existing 4 completion buckets
- OR relabel them as "Construction Complete" and "Construction On Hold" if they need to stay in the sales section for context — but more honest to move them
- Once moved, the Sales Overview tile block cleanly contains the 5 Sales Status counts (which match the 5 PICKLIST options on the Sales Status column)

**Risk if left as-is:** A board reader sees "Units: 11" under Sales Overview and may interpret this as "11 units sold" — they're actually 11 units construction-complete (only 6 of which are settled).

---

## Appendix B — Data duplication risk (Sales Status)

The Smartsheet ecosystem currently has Sales Status defined in **two places**:

1. **107 - Unit Register** (`5289542339743620`), column `Sales Status` (id `4247873805127556`) — PICKLIST, populated manually per unit
2. **107 - Sales Tracking** (`8224519314427780`), column `Sales Status` (id `4770130688249732`) — also PICKLIST, also populated manually

The current 107 Dashboard widget [1] reads from #1 (Unit Register). The 107 - Sales Report - Expanded (id `1830541908201348`) reads from #2 (Sales Tracking).

**Action:** Designate one as canonical, drive the other via cross-sheet INDEX/MATCH formula (matching the pattern already in use on Sales Tracking's Stage / Typology / Build Status columns).

---

## Appendix C — What this spec does not do

- It does not build the charts via API (Smartsheet MCP does not expose widget CRUD). Each chart must be configured in the Smartsheet UI by an editor with OWNER access on the dashboard.
- It does not redesign Reports — only adds chart widgets that source from existing reports and sheets.
- It does not change the report-grid widgets on the current dashboard. Those continue to drive Slides 5 (sales detail) and the embedded construction report.
