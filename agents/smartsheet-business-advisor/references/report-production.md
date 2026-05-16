# Document Report Production from Smartsheet

Use this reference when the user wants to produce a **branded monthly report** (board pack, PCG monthly, lender update, client review) that consumes Smartsheet data but lives as a polished Word or PowerPoint document.

Core principle: **Smartsheet is the data engine; Word or PowerPoint is the presentation surface.** Do not bend Smartsheet to render brand-controlled documents — it cannot. Do not duplicate Smartsheet data into the document by hand — that breaks the link to the source. Instead, treat each section of the document as either (a) a screenshot of a dashboard widget, (b) a pasted Smartsheet report table, or (c) a short narrative block with a strict word budget.

---

## When to use this pattern

Use when **all** of these apply:

- The audience is external or executive (board, PCG, trustees, lender, client) and expects a polished branded document
- The data behind the report lives in Smartsheet dashboards and reports
- The report has a regular cadence (monthly, fortnightly)
- The current report is either a Word doc that has drifted into inconsistency, or a long PDF assembled by hand each month

Do not use when:

- The audience can read Smartsheet directly (give them a dashboard or a Smartsheet report instead)
- The report is one-off (just export to PDF from Smartsheet)
- The data is ad-hoc and changes every period (use a static document or a slide each time)

---

## Choosing Word vs PowerPoint

| Choose Word | Choose PowerPoint |
|---|---|
| Long-form narrative is part of the report | Mostly visual; narrative is captions only |
| Author is more fluent in Word | Author lives in PowerPoint |
| Distribution is read-only PDF or printed | Will be live-presented in a meeting |
| Existing template (or predecessor doc) is Word | Greenfield; team is happy to pick |
| Audience is board / PCG / lender style | Audience is conference / pitch / investor |

PowerPoint forces brevity (one slide = one topic) which is a feature when narrative tends to sprawl. Word handles overflow better and is universally editable.

---

## Template construction

Build a `.dotx` (Word) or `.potx` (PowerPoint) **once**, then never edit it directly when producing a monthly report — only edit the saved-as copy.

### Locked styles

| Style | Use | Settings (Word/PowerPoint) |
|---|---|---|
| `H1 — Section banner` | Major section title | Heading font, large, bold, white-on-navy table cell |
| `H2 — Section heading` | Sub-section | Heading font, medium, bold, brand colour |
| `Body` | Standard paragraph | Body font, 11 pt, ink colour |
| `Body — Placeholder` | `[KYLE TO ...]` block | Body font, bold, brand-primary colour |
| `KPI Tile Label` | Tile small label | Body font, 8 pt, bold, grey, uppercase, centred |
| `KPI Tile Value` | Tile large value | Heading font, 18 pt, bold, brand-primary, centred |
| `RAG Tile Label` | RAG strip label | Body font, 9 pt, bold, white, uppercase, centred |
| `RAG Tile Value` | RAG letter (G/A/R) | Heading font, 14 pt, bold, white, centred |
| `Footer` | Page footer | Body font, 8 pt, grey, with running fields |

### Palette alignment

The document palette **must** echo the Smartsheet dashboard palette so that pasted screenshots integrate seamlessly. If they clash, the report looks amateur.

- **Brand primary** (typically navy or similar): section banners, headings, footer rule
- **Dashboard background** (the dark colour the Smartsheet dashboard uses): cover hero band — makes the cover read as a continuation of the dashboard
- **Brand accent** (small accents only — leaves, dots, divider rules): single accent uses, never large blocks
- **RAG set**: Green / Amber / Red tuned to the brand (avoid screamingly bright reds — use a muted oxide red if the brand is soft); Grey for inactive/unknown
- **Neutrals**: ink for body, paper for card fills, rule for thin separators
- **Subtitle grey**: muted axis labels and small caps

Document the palette as hex codes inside the template's metadata or a hidden style guide page so future editors know what to use.

#### KPV palettes (two valid options — confirm per task)

KPV has **two palette/typography options** depending on the document type. Confirm with Kyle which applies before starting. See `kpv-conventions.md` §8 for full guidance.

**Option A — Systems project / PCG**: navy `#1A2332`, bright green `#2ECC71`, light grey `#F4F6F8`, white surfaces, dark charcoal `#2C3E50` body. Arial throughout, black headings, hyphen bullets, navy table headers with white bold text, first column bold.

**Option B — Marketing**: KPV Navy `#1B3A5B`, Leaf Green `#7FC242`, Action Green `#71BF44`, Subtitle Grey `#A8A49B`, Ink `#3A3A3A` body, Paper `#F5F5F5` section backgrounds. Garamond/Source Serif Pro headings + Calibri/Source Sans Pro body. Used by the existing `PCG Monthly Report - Papamoa - TEMPLATE.docx`.

Pick A for internal section manuals, flow charts, process documentation. Pick B for public-facing brochures, prospectus, brand-led collateral. If unclear, **ask Kyle** — don't pick silently.

### Bullets

For KPV Option A: **hyphen markers (`-`)** in all bulleted lists, not dots. For Option B and non-KPV work follow the relevant brand guide.

---

## Reusable visual components (tables-as-layout in Word; native shapes in PowerPoint)

### KPI tile row

A 1-row, N-column table where each cell has:
- Paper fill background, thin rule border
- Small uppercase label (top)
- Large bold value (centre)

In Word: implement as a borderless N-column table with cell shading. In PowerPoint: a row of identical rounded rectangles.

### RAG strip

A 1-row, 6-column table (one per category — Quality, Programme, Cost, H&S, Sales, [extra]):
- Each cell shaded with the category's RAG colour
- White category label on top, large RAG letter (G/A/R) below
- All centred

### Chart placeholder

A bordered card with italic grey text inside saying exactly what to paste:

> *[PASTE: Construction % Complete by Block — screenshot Chart 3 from the 107 Dashboard]*

The placeholder text references the chart-buildspec doc so the assembler knows exactly which widget to screenshot.

### Two-column achievement/outlook block

A 1-row, 2-column table:
- Left: "Achieved this period" bullets
- Right: "Planned next period" bullets

Each bullet a placeholder: **`[KYLE TO ADD: max 15 words]`**

### Per-unit detail (full-page Smartsheet report)

A single full-width chart-placeholder card sized to A4-portrait body area, with placeholder text:

> *[PASTE: full screenshot of {Report Name} (Smartsheet report id ...)]*

---

## Placeholder conventions

Bolded placeholders make the editing surface obvious. Use a consistent prefix:

- **`[KYLE TO PASTE: ...]`** — paste a screenshot or pasted table
- **`[KYLE TO WRITE: max N words]`** — narrative block with a budget
- **`[KYLE TO ADD: ...]`** — list item or table row
- **`[KYLE TO UPDATE: ...]`** — small fact (period, date) refreshed each month
- **`[KYLE TO SET: ...]`** — pick from options (e.g. RAG letters)
- **`[KYLE TO MAINTAIN: ...]`** — recurring log
- **`[NEXT: ...]`** — flag a future improvement (e.g. "build the Smartsheet that auto-populates this")

Render placeholders in the brand-primary colour, bolded, so they're impossible to miss when scanning.

---

## Monthly assembly workflow

Target: under 60 minutes per period.

| Step | When | Who | Action |
|---|---|---|---|
| 1 | T-3 days | Project team | Update Smartsheet operational rows for the period — Construction %, Sales Status, H&S row, Risk updates |
| 2 | T-2 days | Report owner | Set monthly RAG values (Quality/Programme/Cost/H&S/Sales/Māori) — either in the document directly or in a dedicated `Monthly RAG` sheet that feeds the dashboard tiles |
| 3 | T-1 day | Report owner | Open saved-as copy of the template; refresh the dashboard; screenshot each widget into the matching placeholder |
| 4 | T-1 day | Report owner | Paste tabular reports (sales detail, risk top-5, etc.) — keep the Smartsheet column order |
| 5 | T-1 day | Report owner | Write/trim narrative blocks. Stay within word budgets. Prefer specifics over aspiration |
| 6 | T-1 day | Report owner | Paste BBD/finance attachments into their placeholder block |
| 7 | T-0 | Report owner | Final read-through; export to PDF; distribute via Outlook, Teams Files, or SharePoint |

### Sources for the assembly steps

- **Dashboard screenshots** come from the Smartsheet dashboard widgets — design widgets at an aspect ratio that fits the placeholder card
- **Tabular paste-ins** come from Smartsheet reports — pick reports that have exactly the columns and filtering you want for the document (don't expect to filter at paste-time)
- **Narrative** is the only fully manual content — keep it tight

---

## Pre-populate what you can

The template ships with sensible defaults so each month is mostly screenshot refresh + narrative trim:

- Current top-5 risks already in the table (refresh on assembly)
- Current month's example numbers in the KPI tiles (showing what "good" looks like)
- The Cost table showing the latest known stage budgets (Stage 1, Stage 2, etc.)
- The Māori Procurement table with the latest known row
- The Appendix A links to the Smartsheet dashboard, sheets, and reports — these are stable

Pre-population also serves as documentation: a reader who opens the template knows exactly what each cell will contain.

---

## Distribution

After PDF export:

- **Primary**: attach to Teams meeting invite or paste link from Files tab into the relevant Teams channel
- **Lender / external**: Outlook email with PDF attached (or SharePoint link with view-only permissions)
- **Archive**: save a dated copy (`PCG Monthly Report — Papamoa — 2026-04.pdf`) to a SharePoint folder so historic reports are findable

Power Automate flow option: when the PDF is dropped into a specific SharePoint folder, automatically email it to the distribution list and post a notification card in the relevant Teams channel.

---

## Common mistakes

- **Manually re-typing Smartsheet data into the doc** — breaks the link to source, drifts every month, takes hours
- **Editing the template directly each month** — the template becomes the report; no clean version to start the next month from
- **Letting narrative sprawl** — the old long-narrative format is what drove the redesign in the first place; respect the word budgets
- **Palette drift** — pasting a Smartsheet screenshot whose colours don't match the document palette; fix by aligning the dashboard background colour with the template's cover hero band
- **Hard-typed milestone tables** — replace with a dashboard chart of % complete by unit/block
- **Static charts hidden inside the doc** — if it's a chart you want, put it on the dashboard and screenshot
- **Photos taking over the report** — photos are an appendix, not the main body; the main body is data + narrative
- **No ownership** — without a named owner, monthly reports lapse or drift; assign one person

---

## Quick checklist

Before declaring the template ready:

- [ ] Palette explicitly hex-coded and aligned to the Smartsheet dashboard background
- [ ] Typography pair set with safe fallbacks
- [ ] All placeholders bolded in brand-primary colour with clear `[ROLE TO ACTION: detail]` prefix
- [ ] Cover slide / page 1 includes period field + overall RAG strip + headline KPI tiles + key events
- [ ] One section per topic (Programme, Cost, Sales, H&S, Risk, Māori, Appendix)
- [ ] Each section opens with a navy banner carrying section name + RAG chip
- [ ] Each chart placeholder names the source widget and references the dashboard chart-buildspec
- [ ] Sales/risk per-unit detail is a single full-page screenshot of the relevant Smartsheet report
- [ ] Photos in the appendix, not the main body
- [ ] Appendix lists all Smartsheet IDs and the dashboard URL
- [ ] Footer carries project name, period field, and auto page number
- [ ] Logo in header on every page

---

## Reference implementation

For KPV's PCG monthly report on Papamoa Stage 1, the following artefacts implement this pattern and can serve as a working example:

- `plans/Stage 1 Papamoa/pcg-report-redesign-powerpoint-template.md` — the slide-by-slide / page-by-page spec
- `plans/Stage 1 Papamoa/pcg-report-dashboard-chart-buildspec.md` — the chart widgets that feed the document, with widget configuration
- `plans/Stage 1 Papamoa/build-pcg-template.py` — Python builder using `python-docx` that emits a fresh `.docx` template from code; re-run any time the palette or structure changes
- `plans/Stage 1 Papamoa/PCG Monthly Report - Papamoa - TEMPLATE.docx` — the produced template

These can be referenced or adapted for other portfolios.
