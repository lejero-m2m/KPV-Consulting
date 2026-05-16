# PCG Monthly Report — PowerPoint Template Spec

**Project:** 107 Papamoa Stage 1
**Replaces:** `smartsheet/input/PCG Monthly Report 2026 05 (April) (Stu).docx` (Word-doc format)
**Status:** Draft for Kyle review
**Last updated:** 2026-05-13

> **Placeholders for Kyle's input** are marked in bold throughout this file as **`[KYLE TO PROVIDE: ...]`**, **`[KYLE TO DECIDE: ...]`**, or **`[KYLE TO CONFIRM: ...]`**. Jump to the **Decisions required from Kyle** section at the bottom for the full list, or scan in-place within each slide.

---

## Purpose

Convert the existing Word-based PCG monthly report into a structured PowerPoint deck driven by the live 107 Smartsheet Dashboard. Reduce manual data re-entry, lift the visual quality of board-facing reporting, and shorten monthly assembly to under one hour.

## Design principles

1. **One topic per slide.** No more two-column "headlines + financials" mash-ups.
2. **Charts over numbers, numbers over prose.** Reverse the current ratio — currently ~80% narrative, target ~30%.
3. **Live data, frozen narrative.** Numbers/charts come from Smartsheet (current period). Commentary and risk narrative are paste-in with strict word budgets.
4. **Consistent colour grammar.** Red/Amber/Green has one meaning across the deck. Avoid blue/yellow/grey as RAG variants.
5. **Single source of truth.** If a number appears in two places (it shouldn't), they both link to the same Smartsheet field.

## Branding

Derived from `reference/brand-guidelines.md` and the current 107 Smartsheet Dashboard background. Confirmed with Kyle 2026-05-13.

### Logo

- Source file: `reference/KPV Logo.pdf` (vector) — fallback raster: `reference/KPV Logo-1.jpg`
- Placement: top-left of every slide, ~28 mm wide, with clear space equal to the height of the "VILLAGES" wordmark on all sides (per brand guide §2)
- Variation: full-colour roundel on light slides; reversed (white) roundel on the cover and any dark-navy section banners

### Palette

| Role | Name | HEX | Used for |
|---|---|---|---|
| **Primary brand** | KPV Navy | **`#1B3A5B`** | Section banners, headings, footer bar, RAG-tile borders |
| **Header dark** | Smartsheet Dashboard Navy | **`#131F39`** | Cover-slide hero band, KPI strip background (matches 107 Dashboard) |
| **Brand accent** | Leaf Green | **`#7FC242`** | Logo leaf, small accents only — never large blocks |
| **Body text** | Ink | **`#3A3A3A`** | All body copy and slide-level headings on light backgrounds |
| **Section background** | Paper | **`#F5F5F5`** | Cards, table backgrounds |
| **Dividers** | Rule | **`#E5E5E5`** | Thin separator lines |
| **Subtitle / muted** | Subtitle Grey | **`#A8A49B`** | Sub-labels, axis text, "VILLAGES"-style spaced caps |
| **Page** | White | **`#FFFFFF`** | Slide background, type on dark sections |

### RAG palette (for status tiles and chart series)

Smartsheet's stock RYGG symbol uses brighter values; these are tuned to sit beside KPV Navy without screaming.

| Status | HEX | Notes |
|---|---|---|
| Green / on-track | **`#5BA844`** | Mid-saturation green — safe next to Leaf Green without clashing |
| Amber / watch | **`#E8A33C`** | Warm amber, not neon yellow |
| Red / critical | **`#C0392B`** | Muted oxide red — dignified, not alarmist |
| Grey / inactive | **`#A8A49B`** | Same as Subtitle Grey |

**Rules:** Use these four exclusively for status meaning. Do not use Link Blue (`#0170B9`) as a chart series — it reads as "interactive" in this context.

### Typography

Per brand guide §4 — pair classical serif headings with humanist sans-serif body.

| Element | Font | Size | Weight |
|---|---|---|---|
| Slide title | **Source Serif Pro** (or **Garamond** as built-in PowerPoint fallback) | 28 pt | Semibold |
| Section banner (in-slide) | Source Serif Pro / Garamond | 18 pt | Regular |
| Body | **Source Sans Pro** (or **Calibri** as built-in fallback) | 11 pt | Regular |
| Sub-labels & axis | Source Sans Pro / Calibri | 9 pt | Regular, letter-spaced 1pt for caps |
| Footer | Source Sans Pro / Calibri | 8 pt | Regular |

Do not set "Karaka Pines" anywhere in body type as a faux wordmark — always use the logo file for the brand name.

### Footer

- Left: `Karaka Pines Villages — Papamoa`
- Centre: `PCG Monthly Report — {Month YYYY}`
- Right: `Page {n} of {total}`
- Footer rule: 0.5 pt line in `#E5E5E5` above the footer text

---

## Slide-by-slide structure

### Slide 1 — Cover + Executive RAG

**Purpose:** One-page snapshot for the board chair. If they read nothing else, they read this.

**Layout sketch:**
```
+------------------------------------------------+
| KPV LOGO          PCG MONTHLY REPORT           |
|                   PAPAMOA — APRIL 2026         |
+------------------------------------------------+
| OVERALL: [AMBER]                               |
|                                                |
| QUALITY  PROGRAMME  COST   H&S    SALES  MĀORI |
|  [G]      [G]       [A]    [G]    [A]    [G]   |
+------------------------------------------------+
| HEADLINE NUMBERS                               |
| Units Settled: 6/128   Construction: 11 Cmpl   |
| Avg List Price: $914k  Near Miss MTD: 2        |
+------------------------------------------------+
| KEY EVENTS THIS PERIOD                         |
| • 3-bullet summary, max 15 words each          |
+------------------------------------------------+
```

**Data source:**
- 6 RAG tiles: manually set each month by Kyle (recommend a `Period RAG` sheet summary on a dedicated `107 - Monthly RAG` sheet so they're auditable)
- Headline numbers: live from 107 Dashboard widgets [5], [7], [8], [9] — screenshot each month
- Key events: paste-in, max 3 bullets × 15 words

**Word budget:** 45 words total
**Production time:** 5 min

---

### Slide 2 — Programme

**Purpose:** Where is each unit/stage in the build cycle, and is the schedule holding?

**Layout sketch:**
```
+------------------------------------------------+
| PROGRAMME                              [G]     |
+------------------------------------------------+
| [Construction % Complete by Block, h-bar]      |
|  Berkeley 105/107  ████████████████████ 100%   |
|  Monterey 109/111  ███████████████      85%    |
|  Melrose 113/115   ████████              40%   |
|  ... (auto from Smartsheet)                    |
+------------------------------------------------+
| Achieved this period     | Next period         |
| • Unit 112 handed over   | • 109/111 kitchen   |
| • 109/111 paint underway | • 113/115 slab pour |
+------------------------------------------------+
```

**Data source:**
- Bar chart: 107 Dashboard chart widget (to be built — see chart-buildspec, Chart 3) screenshot
- Two-column narrative: paste-in from Stu's "Progress achieved/next period" sections

**Word budget:** 80 words (40 per column)
**Production time:** 10 min

---

### Slide 3 — Cost / Financial

**Purpose:** Budget vs actual, certified to date, contingency status.

**Layout sketch:**
```
+------------------------------------------------+
| COST                                   [A]     |
+------------------------------------------------+
| Stage 1 Civil                                  |
| Budget        ██████████  $2,225k              |
| Certified     █████████   $1,932k              |
| To complete   ▏           $0                   |
|                                                |
| Stage 2 Civil                                  |
| Budget        █████      $1,304k               |
| Contingency   █          $237k                 |
| Certified     ██         $391k                 |
+------------------------------------------------+
| BBDNZ DRAWDOWN — [paste table here]            |
|   Period: April 2026                           |
|   Source: BBD attachment (Schedule 2)          |
+------------------------------------------------+
| Headline commentary (max 50 words)             |
+------------------------------------------------+
```

**Data source:**
- Bar chart: Smartsheet dashboard chart widget (chart-buildspec Chart 6) — or build as a static chart in PowerPoint pasting in BBD figures monthly
- BBDNZ table: paste-in from BBD attachment (placeholder block)
- Commentary: paste-in, max 50 words

**Word budget:** 50 words
**Production time:** 15 min (BBD wrangle is the slow bit)

**Decision (2026-05-13):** BBD figures remain a **monthly paste-in** from BBD's PDF for now. Revisit when there's appetite to build a `107 - BBD Drawdown` Smartsheet for live charting.

---

### Slide 4 — Sales & Marketing (overview)

**Purpose:** Pipeline at a glance, plus this period's sales activity.

**Layout sketch:**
```
+------------------------------------------------+
| SALES & MARKETING                      [A]     |
+------------------------------------------------+
| PIPELINE                | CUMULATIVE SETTLEMTS |
| [donut chart]           | [combo chart]        |
| Settled         6       |                      |
| Unconditional   1       |    Target line       |
| Application     5       |    Actual cumulative |
| Available       6       |                      |
| Not Available   4       |  Months: J F M A M.. |
+------------------------------------------------+
| Headline commentary (max 80 words)             |
| • Enquiry level for period                     |
| • Appointments / conversions this period       |
| • Market conditions one-liner                  |
+------------------------------------------------+
```

**Data source:**
- Donut: chart-buildspec Chart 1
- Combo line+bar: chart-buildspec Chart 2 — needs a monthly settlements snapshot sheet to track over time
- Commentary: rewrite of current Schedule 3 narrative, max 80 words (currently ~500 words — cut to 80)

**Word budget:** 80 words
**Production time:** 10 min

---

### Slide 5 — Sales detail (per-unit)

**Purpose:** Trustee-level transparency on every unit's sales status and any price variance.

**Layout sketch:**
```
+------------------------------------------------+
| SALES — PER-UNIT DETAIL                        |
+------------------------------------------------+
| [Screenshot of 107 - Sales Report - Expanded]  |
| Unit  Stage  Typology  Build  Sales  ...       |
| 101   Stg1   Juniper   Cmpl   Uncond           |
| 102   Stg1   Berkeley  Cmpl   Settled          |
| ...                                            |
+------------------------------------------------+
```

**Data source:**
- Full screenshot of `107 - Sales Report - Expanded` (id `1830541908201348`)
- No commentary on this slide — the table speaks for itself

**Word budget:** 0
**Production time:** 2 min

---

### Slide 6 — Health & Safety

**Purpose:** Lead and lag indicators for the period + 6-month trend.

**Layout sketch:**
```
+------------------------------------------------+
| HEALTH AND SAFETY                       [G]    |
+------------------------------------------------+
| April 2026 — Signature Homes                   |
|                                                |
| LEAD              | LAG                        |
| Inductions  17    | Near Miss Minor    2       |
| Contractor  7     | Near Miss PSIF     0       |
| Audits PM   0     | MTI                0       |
| External    0     | LTI                0       |
+------------------------------------------------+
| [6-month stacked column trend chart]           |
| Inductions / Audits / Near Misses by month     |
+------------------------------------------------+
| Open items: see 107 - H&S Open Items Report    |
+------------------------------------------------+
```

**Data source:**
- Top tiles: screenshot dashboard widget [9]
- Trend chart: chart-buildspec Chart 4

**Word budget:** 30 words (open items summary line)
**Production time:** 5 min

**Note:** Risk Report row 107-RSK-0003 flags that PCG reports have been under-reporting near misses vs Signature Homes' own QR-code system. Recommend the H&S Monthly Indicators sheet becomes the **single source** and Stu's manual H&S table is retired.

---

### Slide 7 — Risk Register

**Purpose:** Top 5 risks and where they sit on the heat map.

**Layout sketch:**
```
+------------------------------------------------+
| RISK REGISTER                                  |
+------------------------------------------------+
| TOP 5 ACTIVE RISKS                             |
| ID         Risk                  RAG  Owner    |
| RSK-0002   H&S audit frequency   [Y]  PM/Sig   |
| RSK-0004   Open drain trip       [Y]  Sig      |
| RSK-0005   Wind-blown materials  [Y]  Sig      |
| RSK-0003   Near-miss reporting   [Y]  PM       |
| RSK-0001   HSMS safe behaviour   [Y]  PM       |
+------------------------------------------------+
| [Risk heat map — 5×5 likelihood × consequence] |
|                                                |
| All 14 active risks plotted as dots            |
+------------------------------------------------+
```

**Data source:**
- Top 5 table: filtered screenshot of 107 - Risk Report (id `2047711023943556`)
- Heat map: chart-buildspec Chart 5

**Word budget:** 0 (table + chart only)
**Production time:** 5 min

---

### Slide 8 — Māori Procurement

**Purpose:** Schedule 4 obligation — contracts awarded to Māori-owned businesses.

**Layout sketch:**
```
+------------------------------------------------+
| MĀORI PROCUREMENT                              |
+------------------------------------------------+
| Contractor          Service        Value  Date |
| Out the Gate Cont.  Boundary Fence [tbc] 12/2/26|
| ...                                            |
+------------------------------------------------+
| Cultural / iwi update (max 40 words)           |
| • Road naming with Waitaha                     |
| • Wetland planting coordination                |
+------------------------------------------------+
```

**Data source:**
- Table: manual or sourced from a dedicated `107 - Māori Procurement Register` (recommend creating — does not yet exist)
- Cultural update: paste-in from current Schedule 3 narrative

**Word budget:** 40 words
**Production time:** 5 min

**`[KYLE TO DECIDE: build a 107 - Māori Procurement Register Smartsheet (recommended — enables Schedule 4 auto-population) OR keep table as manual paste-in each month]`**

---

### Slide 9 — Photo record

**Purpose:** Visual progress per block.

**Layout sketch:**
```
+------------------------------------------------+
| PHOTOGRAPHIC RECORD — APRIL 2026               |
+------------------------------------------------+
| Berkeley 105-107  |  Monterey 109-111          |
| [photo]           |  [photo]                   |
| [photo]           |  [photo]                   |
+-------------------+----------------------------+
| Melrose 113-115   |  Street view               |
| [photo]           |  [photo]                   |
| [photo]           |  [photo]                   |
+------------------------------------------------+
```

**Data source:**
- Photos sourced from attachments on the matching rows in `107 - Construction Programme` (id `5063906232848260`) — or a dedicated `107 - Photo Log` sheet (recommend creating)
- Caption each with block + date

**Word budget:** 0
**Production time:** 15 min (most of the slow time is photo curation)

**`[KYLE TO DECIDE: photos attached to Construction Programme rows (per-unit, simple) OR a dedicated 107 - Photo Log sheet with Photo Date + Block + Caption (recommended — chronological + filterable)]`**

---

### Slide 10 — Appendix

**Purpose:** Auditable links to live Smartsheet sources so recipients can dig deeper.

**Layout sketch:**
```
+------------------------------------------------+
| APPENDIX — LIVE DATA                           |
+------------------------------------------------+
| 107 Dashboard:                                 |
|   smartsheet.com/dashboards/MgV3W8XJ...        |
|                                                |
| Civil Programme:           ID 6233992763232132 |
| Construction Programme:    ID 5063906232848260 |
| Unit Register:             ID 5289542339743620 |
| Sales Tracking:            ID 8224519314427780 |
| H&S Monthly Indicators:    ID 3104570405244804 |
| Risk Register:             see Risk Report     |
+------------------------------------------------+
| Schedule of approvals/resolutions              |
| (small text, as current page 3)                |
+------------------------------------------------+
```

---

## Production workflow (monthly)

| Step | Owner | Time | Activity |
|---|---|---|---|
| 1 | Project team | T-3 days | Update Smartsheet rows for the period (Construction %, Sales Status, H&S row, Risks) |
| 2 | Kyle | T-2 days | Set 6 Period RAG values on the monthly RAG sheet |
| 3 | Stu (or Kyle) | T-1 day | Screenshot dashboard sections into PowerPoint placeholders |
| 4 | Stu | T-1 day | Paste BBD drawdown table into Slide 3 |
| 5 | Stu | T-1 day | Write/trim narrative blocks (≤300 words across whole deck) |
| 6 | Kyle | T-0 | Final review, export to PDF, distribute |

**Total target time:** 60 minutes of active assembly per month.

---

## What does NOT change

- Schedule 2 (BBDNZ drawdown) — still a paste-in / attachment from BBD
- The CEO/board approvals log (currently a small box on page 3) — stays as a static slide footer or appendix entry
- The schedule of monthly sign-off / distribution

## What gets retired

- The "Project Dashboard" front cover with image-based RAG indicators (replaced by data-driven RAG tiles)
- The two-column "Headlines + Financial Summary" page (split into Programme and Cost slides)
- The vertically-stacked H&S table (replaced by tiles + trend chart)
- Hard-typed Programme Milestones table (driven by Construction Programme % Complete)
- Long-form Sales & Marketing narrative (cut from ~500 words to 80)

---

## Dependencies

This template depends on:

1. **Chart widgets being built on the 107 Dashboard** — see `pcg-report-dashboard-chart-buildspec.md`
2. **Monthly RAG sheet being created** — single sheet, 6 picklist columns (Quality/Programme/Cost/H&S/Sales/Māori) keyed by Period
3. **BBD figures process** — decide paste-in vs Smartsheet entry
4. **Photo log** — attachments-on-rows vs dedicated sheet
5. **KPV brand assets** — colours, fonts, logo

---

## Decisions required from Kyle

Each block below is a placeholder — replace the bracketed text with your answer once decided.

### 1. Template tool

**`[KYLE TO DECIDE: PowerPoint (recommended — universally editable, exports cleanly to PDF) / InDesign (best visual quality, requires Adobe licence) / Google Slides (collaborative, but charts are less polished)]`**

### 2. BBD financials

**`[KYLE TO DECIDE: see Slide 3 — paste-in vs Smartsheet]`**

### 3. Māori Procurement register

**`[KYLE TO DECIDE: see Slide 8 — Smartsheet register vs manual table]`**

### 4. Photo log

**`[KYLE TO DECIDE: see Slide 9 — row attachments vs Photo Log sheet]`**

### 5. Report owner

**`[KYLE TO CONFIRM: who owns monthly assembly going forward — Stu / Kyle / shared]`**

### 6. Distribution list and cadence

**`[KYLE TO PROVIDE: list of recipients + frequency — e.g. "PCG monthly; trustees quarterly; lenders on request"]`**
