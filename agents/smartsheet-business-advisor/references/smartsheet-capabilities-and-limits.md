# Smartsheet — Capabilities, Limits, and Architecture Rules

Use this reference when designing or auditing a Smartsheet system to ensure decisions are made once and won't be undermined later by a platform limit. This is the "what can and can't be done" matrix that drives durable architecture.

It is intentionally honest about uncertainty. Where exact thresholds or recently-changed features are involved, this file says so and points to where to verify. **Always verify limits against Smartsheet's current documentation** before betting an architecture on them, especially around row counts, cell history retention, and any feature that has shifted between plan tiers.

---

## 1. What can and can't be done via API

The Smartsheet REST API (and any MCP/SDK wrapper) supports **full CRUD on data structures** but is **read-only for presentation assets**.

| Asset | Read via API | Create / Modify via API | Notes |
|---|---|---|---|
| Workspaces | ✅ | ✅ | Create, share, list contents |
| Folders | ✅ | ✅ | Create, move, list |
| Sheets | ✅ | ✅ | Full lifecycle: create, copy, move, delete |
| Sheet columns | ✅ | ✅ | Add, update, delete, reorder; mind validation rules |
| Sheet rows | ✅ | ✅ | Add, update, delete, move; supports hierarchy via parent_id |
| Cells (within rows) | ✅ | ✅ | Including formulas, hyperlinks, contact references |
| Sheet Summary fields | ✅ | ✅ | Add, update, delete |
| Attachments | ✅ | ✅ | Files, URL links, including OneDrive/SharePoint links |
| Comments / Discussions | ✅ | ✅ | Full lifecycle |
| Cell history | ✅ | n/a | Read-only — Smartsheet tracks automatically |
| Shares | ✅ | ✅ | Manage sheet/workspace/report sharing |
| **Reports** | ✅ read | ❌ **cannot create or modify via API** | Author in Smartsheet UI only |
| **Dashboards (Sights)** | ✅ read | ❌ **cannot create or modify, including widgets, via API** | Author in Smartsheet UI only |
| **Forms** | n/a | ❌ **cannot create or modify via API** | Author in Smartsheet UI only |
| **Automations / Workflows** | partial read | ❌ **cannot create or modify via API** | Author in Smartsheet UI only |
| **Conditional formatting rules** | n/a | ❌ **cannot create or modify via API** | Author in Smartsheet UI only |

**Architecture implication:** anything that is "Smartsheet UI only" is a one-time human setup. Plan to invest the time once, document the setup in writing (the sheet registry, a build spec, screenshots), and avoid letting it drift. Reports, dashboards, forms, and automations are best treated as **slow-changing** — design them carefully and don't reshape them often.

For anything you might want to script repeatedly (bulk row loads, column changes, formula migrations, cross-sheet rebuilds), the API path is open and reliable.

---

## 2. Sheet structure rules

### Primary column

- **Required**: every sheet has exactly one primary column
- **Type is locked to TEXT_NUMBER** — cannot be changed
- **Cannot be set to AUTO_NUMBER** — this is the limitation that bit us in KPV's Unit Register
- **Can hold a formula** — but the result is treated as TEXT_NUMBER, so date-formula results render as strings unless you format carefully
- **Cannot be deleted** — must rename instead

**Workaround for unique IDs**: add a separate AUTO_NUMBER column (e.g. "Job ID", "Risk ID") on every sheet that participates in cross-sheet references. Use that column, not the primary, as the join key. AUTO_NUMBER supports prefixes, padding, and starting number — useful for human-readable IDs like `107-RSK-0001`.

### Column types

| Type | Stores | Best for |
|---|---|---|
| `TEXT_NUMBER` | Any string-like value, numbers, dates as strings | Names, IDs, free text, currency |
| `DATE` | Date only (no time) | Due dates, settlement dates |
| `DATETIME` / `ABSTRACT_DATETIME` | Date and time | Gantt start/end on dependency-enabled sheets |
| `CHECKBOX` | Boolean | Flags, "Up Next", "Approved" |
| `CONTACT_LIST` | One contact (user or email) | Owner, Assigned To |
| `MULTI_CONTACT_LIST` | Multiple contacts | Reviewers, watchers |
| `PICKLIST` | One value from a fixed list, optionally with symbol set | Status, Stage, RAG |
| `MULTI_PICKLIST` | Multiple values from a fixed list | Tags, categories |
| `DURATION` | Time spans (days, weeks) | Gantt durations |
| `PREDECESSOR` | Dependency reference | Gantt predecessors |
| `AUTO_NUMBER` | System-generated incrementing ID | Unique row IDs (cannot be primary) |
| `CREATED_BY`, `CREATED_DATE`, `MODIFIED_BY`, `MODIFIED_DATE` | System fields | Audit / metadata |

### Picklist validation

- `validation = true` — only listed values accepted (enforced on UI and API)
- `validation = false` — list is suggestion only; free text accepted

**Rule of thumb**: always set validation = true on Status, Stage, RAG, and other controlled fields. Mistaken `validation = false` is a common source of dirty data ("In Progres" vs "In Progress").

### Hierarchy

- Rows can be indented to create parent/child structure
- Max indent depth is **6 levels**
- Parent rows can roll up date and duration via `=MIN(CHILDREN())` etc.
- **Quirk on dependency-enabled sheets**: parent End Date has no rollup formula by default — it's static; adding new descendants at deeper levels does not auto-extend it. Workaround: write a value to parent Start Date (overrides rollup formula) and let Duration recalculate End Date

### Soft sheet limits

| Limit | Approximate value | Verify |
|---|---|---|
| Rows per sheet | 20,000 (Business) — has been increasing, verify | [Smartsheet docs] |
| Columns per sheet | ~400 (effective) | [Smartsheet docs] |
| Cell character limit | 4,000 characters | [Smartsheet docs] |
| Indent depth | 6 levels | Confirmed |
| Attachments per row | 50 | [Smartsheet docs] |
| Cell history retention | Verify on current plan | Plan-dependent |

If you're approaching any of these, treat it as a design smell — split the sheet by portfolio, period, or status.

---

## 3. Formulas — what works, what to avoid

### In-sheet formulas (recommended default)

- Work on any column except those locked by validation rules
- Support most Excel-equivalent functions: IF, COUNTIFS, SUMIFS, AVG, COLLECT, INDEX, MATCH, VLOOKUP, JOIN, CONCAT, CHILDREN(), PARENT(), ANCESTORS(), DESCENDANTS(), TODAY()
- **Column-level formulas** (newer feature) apply a formula to every row in a column, so adding a new row inherits the formula — strongly recommended for derived fields

### Sheet Summary formulas

- Live at the sheet level, not in any row
- Useful for headline metrics (count of open items, total contract value, last updated date)
- Surface directly on dashboard metric widgets
- Refresh when underlying data changes (sometimes a refresh delay; force by re-opening)

### Cross-sheet formulas — the architecture choice

**Cross-sheet references live in the destination sheet, not the source.** You build them by:

1. Open the sheet where you want the formula
2. In the formula bar: **References Other Sheets**
3. Pick the source sheet and the range
4. Give the reference a name (e.g. `UR Unit Numbers`)
5. Use the named range in your formula: `=INDEX({UR Unit Numbers}, MATCH([Unit Number]@row, {UR Unit Number Range}, 0))`

**KPV pattern**: Unit Register (UR) is the canonical source per village. All cross-sheet formulas pulling unit data live in the **other** sheets (Construction Programme, Sales Tracking, Reports), each with their own named ranges back to UR. UR itself stays mostly manual entry + simple in-sheet formulas. This is the right model.

### Performance — known to bite

- **Cross-sheet references slow recalculation** — there's a per-cell limit (Smartsheet recommends keeping each formula's cross-sheet reference count low; verify current guidance)
- **Many helper columns are cheaper than one mega-formula** — Smartsheet's recalc is more efficient on simple formulas
- **Avoid recalculating on every row** when you can compute once in Sheet Summary

### Formula quirks

- **Silent override**: writing a value via API to a column that has a column-level formula returns SUCCESS but the formula overrides the value. Always verify with a re-fetch
- **End Date column on dependency-enabled sheets**: API rejects direct writes with error 1080. Write Start Date or Duration instead
- **Primary column formula constraint**: result is treated as TEXT_NUMBER — date formulas render as strings unless explicitly formatted
- **Empty cell vs zero**: COUNTIFS treats blank differently from "0" — be explicit with `<> ""` or `> 0` conditions
- **Bulk hierarchical load recalc lag**: after a large `add_rows` build of a multi-level `=SUM(CHILDREN())` hierarchy, section/grand totals can lag **minutes** behind the (already-correct) category-parent values. Never trust a section/grand total read immediately after a bulk load — verify at category-parent level, force recalc, then poll until stable. **See §10 "Known quirks" for the full quirk and mitigation steps.**

---

## 4. Reports — what they can and can't do

Reports are **filtered, sorted, grouped views over sheets**. They are not a calculation layer.

### What reports can do

- Filter rows from one or more source sheets
- Group by column (max 3 levels of grouping)
- Sort by column (multiple sort keys)
- Show / hide columns
- Aggregate within groups (count, sum, average, min, max) — for grouped views
- Update cells (edits write back to the source sheet)
- Be embedded in dashboards (grid widgets) and Teams tabs

### What reports cannot do

- **Add columns** that don't exist on a source sheet — column mapping in multi-source reports requires matching column types
- **Calculate derived columns** that aren't formula columns on the source sheet
- **Pull from other reports** — only from sheets
- **Be created or modified via API** — UI only
- **Filter on a formula expression** — only column-value criteria
- **Display formulas** — only their evaluated results

### Single-source vs multi-source

- **Single-source**: one sheet, fast to set up, columns map automatically
- **Multi-source**: rows from multiple sheets unified by mapped columns. Setting up the mapping is the work. Useful for portfolio rollups (e.g. all civil programmes across 4 villages into one report)

### Architecture implication

- Build reports as **views** that the audience needs — not as data transformation pipelines
- If you find yourself wanting calculations a report can't do, add the calculation to the source sheet as a formula column, then surface it in the report

---

## 5. Dashboards (Sights) — what they can and can't do

### Widget types

| Widget | Reads from | Use |
|---|---|---|
| Title | Static | Section banner |
| Rich text | Static | Instructions, interpretation |
| Metric | Sheet Summary field OR cell reference | Single number with optional label |
| Chart | Sheet (rows × columns) — and reports in some configurations | Visualisations |
| Report (grid) | Report | Embedded grid view |
| Shortcut | URL or Smartsheet asset | Quick links |
| Web content | External URL (HTTPS) | Embedded web page |
| Image | Upload | Logos, photos |

### What dashboards can do

- Layout is a 90-column grid; widgets snap to it
- Background colour, widget borders, font controls
- Mix metric tiles, charts, embedded reports, shortcuts, rich text
- Conditional formatting on metric tiles (limited — typically you bake colour into the source data via a helper column with format rules)
- Be embedded in Teams as tabs, or shared via Smartsheet link

### What dashboards cannot do

- **Be created or modified via API** — UI only
- **Drill-through to underlying data** in a deep way — clicking through opens the source sheet but won't preserve filters
- **Cross-sheet aggregation in a chart** without a chart source sheet that pre-aggregates the data
- **Custom JavaScript / interactive elements** — fixed widget vocabulary
- **Print-perfect layout** — dashboards are screen-first; export to PDF requires manual setup and rarely looks polished

### Architecture implication

- Treat dashboards as **slow-changing**: design once with care, refresh data automatically via the source sheets
- For polished, printable output → use the Word/PowerPoint template pattern (see `report-production.md`), not dashboard PDF export

---

## 6. Forms — what they can and can't do

### What forms can do

- Custom title, description, logo
- Field-level conditional logic ("show field B only if field A is X")
- Required fields
- Hidden / pre-filled fields (via URL parameters or fixed defaults)
- File attachments
- Email confirmation to submitter
- Multiple themes / branding
- Public (no login) or restricted to licensed users

### What forms cannot do

- **Be modified via API** — UI only
- **Multi-step / multi-page logic** beyond conditional show/hide on a single page
- **Direct integration with non-Smartsheet sources** (use Power Automate to bridge Microsoft Forms → Smartsheet if you need M365-style forms)
- **Validate against other rows** (e.g. "this unit number is already taken")
- **Update existing rows** — only create new ones (use `Update Request` automation for updates instead)

### When to use Microsoft Forms instead

- Survey/quiz style with scoring
- Result goes to SharePoint/Excel for analysis, not into a Smartsheet workflow
- External audience where you'd prefer a Microsoft-branded form

---

## 7. Automations — what they can and can't do

### What automations can do

- **Triggers**: row added; row changed; column value matches condition; date reached (relative to a date field); recurring schedule (daily/weekly/monthly)
- **Conditions**: any column comparison
- **Actions**: send alert (email, Teams, mobile); send approval request; send update request; record date; change cell value; lock/unlock row; copy row to another sheet; move row to another sheet; assign people
- Chain conditions ("if X AND Y")

### What automations cannot do

- **Be created or modified via API** — UI only
- **Trigger across sheets** — each automation is scoped to one sheet (cross-sheet logic requires duplication or Power Automate)
- **Loop or iterate** — single-pass logic only
- **Pull external data** — no HTTP requests or external API calls (use Power Automate for this)
- **Conditional branching beyond simple AND/OR** — for complex logic, use Power Automate

### When to escalate to Power Automate (free with most M365 licences)

- The flow crosses systems (Smartsheet ↔ Outlook ↔ Teams ↔ SharePoint)
- You need adaptive cards in Teams with action buttons
- You need approval emails that managers can action from Outlook mobile
- You need to create calendar events from Smartsheet dates
- You need to mirror Smartsheet attachments into a structured SharePoint folder

---

## 8. Plan tiers — what's where

| Capability | Pro | Business | Enterprise | Premium add-on |
|---|---|---|---|---|
| Multiple sheets | ✅ limited | ✅ | ✅ | — |
| Unlimited free viewers/editors | ❌ | ✅ | ✅ | — |
| Dashboards | ✅ limited | ✅ | ✅ | — |
| Reports | ✅ | ✅ | ✅ | — |
| Forms | ✅ | ✅ | ✅ | — |
| Automations | ✅ basic | ✅ richer | ✅ richest | — |
| Single sign-on (SSO) | ❌ | ✅ | ✅ | — |
| User and group management | ❌ | limited | ✅ | — |
| Resource Management | ❌ | ❌ | optional | ✅ |
| Bridge (workflow orchestration) | ❌ | ❌ | optional | ✅ |
| DataMesh / Data Shuttle | ❌ | ❌ | optional | ✅ |
| Control Center | ❌ | ❌ | optional | ✅ |
| Live Data Connector (ODBC) | ❌ | ❌ | optional | ✅ |
| Calendar App / Pivot App / Dynamic View | ❌ | ❌ | optional | ✅ |
| Power Automate Smartsheet connector | ✅ | ✅ | ✅ | works on any plan; requires M365 Power Automate licence |

**KPV is on Business plan.** Avoid recommending Premium add-ons as default. Power Automate is the lever to reach beyond Smartsheet without paying for Premium.

---

## 9. Architecture rules that follow from these limits

These are durable rules that, once decided, should not be relitigated each time:

1. **Source of truth per concept.** One sheet per concept (UR for unit data, CCP for construction tasks, ST for sales tracking, Risk Register for risks). Other sheets cross-reference. Never two sheets with overlapping primary data.

2. **Unique ID is a separate AUTO_NUMBER column, not the primary.** Primary can be human-readable (Unit Number, Stage Name) but the cross-sheet join key is the AUTO_NUMBER (Job ID, Risk ID).

3. **Cross-sheet formulas live in the destination sheet.** Source sheets (canonical) stay mostly manual + in-sheet formulas. Consumer sheets pull via INDEX/MATCH on named ranges back to the source.

4. **Picklist + validation = true** on every status/stage/RAG/category column.

5. **Column-level formulas** for derived fields wherever possible — new rows inherit the formula automatically.

6. **Helper columns over mega-formulas.** Easier to debug, faster to recalculate, easier to chart.

7. **Reports for views; never for calculation.** If a report needs a derived value, add a formula column to the source sheet.

8. **Dashboards as slow-changing artefacts.** Design once carefully. Build chart source sheets so the chart widget is reading clean, pre-aggregated data — not raw operational data.

9. **Documents (Word/PowerPoint) for branded output**, not Smartsheet itself. Dashboards drive the document via screenshot/paste patterns. See `report-production.md`.

10. **Power Automate for cross-system orchestration**, not Smartsheet automations. Smartsheet automations are scoped per sheet and cannot reach into M365 cleanly.

11. **SharePoint/OneDrive as document store.** Smartsheet row attachments should preferentially be links to the SharePoint canonical file, not native uploaded copies.

12. **One canonical "Status" per dimension.** If you have Sales Status and Construction Status they live on **one** sheet each. Don't duplicate Sales Status on UR and on Sales Tracking (KPV currently has this duplication — should be reconciled).

13. **Naming conventions** — Workspaces: portfolio code (`107 - Papamoa`) or function prefix (`OPS -`). Folders: numbered functional sections (`02 - Civil & Construction`, `03 - Reports Internal`, `04 - Reports External`). Sheets: portfolio prefix + concept (`107 - Unit Register`). Reports: prefix `107 -` for portfolio context.

14. **Sheet registry**: maintain a markdown registry of every sheet, report, dashboard, with column IDs, formulas, and dependencies. Smartsheet's UI does not surface this — a written registry is the only way to keep architecture coherent over time.

15. **Re-audit each session.** Sheet IDs are stable; report IDs and dashboard IDs can change if assets are recreated. Verify against a fresh audit before assuming an ID is current.

---

## 10. Known quirks (the ones that have already bitten KPV)

| Quirk | Where seen | Workaround |
|---|---|---|
| End Date rollup on dependency-enabled sheets is static | 107 Civil Programme (Smartsheet quirk) | Write Start Date directly to force Duration recalculation |
| API write to End Date column rejected on dependency-enabled sheets | 107 Civil Programme | Write Start Date + Duration instead; End computes |
| API returns SUCCESS but formula silently overrides cell value | Build Status formula columns | Verify with re-fetch after writes |
| Primary column cannot be AUTO_NUMBER | Multiple KPV sheets | Add a separate AUTO_NUMBER column for unique IDs |
| Dashboard widget [1] mixes Construction and Sales Status counts under "Sales Overview" | 107 Dashboard | Relabel widgets or split into two tile blocks |
| Same data point in two sheets (Sales Status on UR and Sales Tracking) | KPV pattern | Designate canonical source; drive the other by INDEX/MATCH |
| Smartsheet stock RAG symbol palette can clash with brand | Brand-sensitive dashboards | Don't rely on RYGG symbols where brand matters — build a colour-coded formula column instead |
| Cross-sheet reference setup is slow in the UI when many sheets are involved | Multi-village rollups | Plan the reference structure on paper first; create named ranges in batches |
| Reports can't show columns that don't exist on the source — multi-source reports require matched column types across all source sheets | Portfolio rollup reports | Standardise column names and types across sheets at design time |
| Severe `SUM(CHILDREN())` rollup recalc lag after bulk hierarchical load: ~250 rows, 3-level hierarchy (section → category → line items), section/grand totals lagged correct values by **minutes**, showing only the first child branch (e.g. a section reading its Design-category-only subtotal) | 107 Papamoa Budget build, 16 May 2026 | (1) Verify correctness at the **category-parent** level — parent value should equal the sum of its own children; this settles fast and is the true correctness signal. (2) Force the top rollups by **re-asserting `=SUM(CHILDREN())`** on the lagging section/parent rows via a PUT (same formula, triggers recalc). (3) Poll the grand total until **stable across ≥2 consecutive reads AND in the expected range** — a single "stable" read is insufficient (a partially-recalced value can read stable between two close polls). For financial loads, reconcile against the **grand total + per-category sums**, never section parents read early. |
| KPV account is hosted in the North American region | KPV environment | Web app and API are both `app.smartsheet.com` / `api.smartsheet.com` (confirmed 2026-05-22 inventory). The `.au` host is not used. |

---

## 11. How to use this reference

When the user proposes a new feature, sheet, or integration:

1. Check **section 1 (API capabilities)** — is the asset programmable, or is it a one-time UI build?
2. Check **section 9 (architecture rules)** — does the proposal honour the canonical-source pattern?
3. Check **section 10 (known quirks)** — has KPV hit a related issue before?
4. If recommending an integration with Microsoft 365, cross-check against `microsoft-integration.md` for plan-tier and tooling
5. If producing a polished document, cross-check against `report-production.md`
6. Recommend only Business-plan-included or Power-Automate-bridged features unless a premium add-on is explicitly authorised

When a constraint is hit:

1. Confirm the limit against Smartsheet's current documentation (link or quote)
2. Update this file with the date and example so the next architect doesn't relearn it
3. Add to the "Known quirks" table if it has bitten production
