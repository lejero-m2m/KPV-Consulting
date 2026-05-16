# Microsoft 365 Integration Playbook

Use this reference when the user wants Smartsheet to play well with the Microsoft suite — Teams, Word, PowerPoint, Excel, Power Automate, SharePoint, OneDrive, Outlook, Power BI, and Microsoft Forms.

Core principle: **Smartsheet is the workflow engine and structured data store; Microsoft 365 is where the data is consumed, presented, and acted on.** Most users live in Teams, Outlook, and the Office apps — push Smartsheet data to those surfaces rather than expecting people to come to Smartsheet.

---

## Plan-tier matrix (what works without premium add-ons)

| Capability | Smartsheet Business | Notes |
|---|---|---|
| Microsoft Teams integration (Smartsheet for Teams app) | ✅ included | Embed dashboards/sheets/reports as channel tabs |
| Microsoft 365 SSO | ✅ included | Configurable on any paid plan |
| Outlook Add-in (convert email → row, attach email) | ✅ included | Free from the M365 app store |
| OneDrive / SharePoint file attachments on rows | ✅ included | Linked attachments, not native files |
| Export to Excel / PDF | ✅ included | Manual download from sheets and reports |
| Send via email (Smartsheet → Outlook) | ✅ included | Single row or whole sheet as PDF/Excel |
| Power Automate connector (Smartsheet) | ✅ works on any Smartsheet plan | Requires a Microsoft Power Automate licence — included in most M365 business plans |
| Microsoft Forms (M365 native) | ✅ separate | Microsoft licence, not Smartsheet |
| Power Query in Excel/Power BI via Smartsheet API | ⚠ possible | Requires API token and a custom connector — workable but fiddly |
| **Smartsheet Live Data Connector** (ODBC for Excel/Power BI/Tableau) | ❌ premium add-on | Mark as optional, not assumed |
| **Bridge** (workflow orchestration) | ❌ premium add-on | Optional |
| **DataMesh / Data Shuttle** | ❌ premium add-on | Optional |
| **Pivot App / Calendar App / Dynamic View** | ❌ premium add-ons | Optional |
| **Control Center** | ❌ Enterprise + premium | Optional |
| Power BI native dashboard tile pinning | ❌ premium / OData | Premium plan add-on |

**Decision rule:** If a Microsoft integration can be achieved with **native Smartsheet + Power Automate**, prefer that path on Business plan. Only recommend Live Data Connector, Bridge, or DataMesh when Power Automate genuinely cannot meet the requirement and the cost is justified.

---

## 1. Microsoft Teams — dashboards and reports where people already work

Teams is the primary collaboration surface. Aim to make people see Smartsheet data without leaving Teams.

### Patterns

- **Channel tabs**: pin the relevant dashboard, report, or form as a tab in the relevant Teams channel
- **Smartsheet for Teams app**: install once at the org level; users add tabs from the Smartsheet picker
- **Alerts**: route Smartsheet alerts to Teams channels via the native connector, or via Power Automate for richer formatting (adaptive cards with action buttons)
- **Meetings**: drop Smartsheet report links into meeting invites and chat; review live in screen-share

### Mapping cheat sheet

| Teams channel | Smartsheet asset to tab |
|---|---|
| Leadership / Exec | Executive dashboard, monthly board report (Word/PDF in Files tab) |
| Operations | Operations dashboard, "Active Jobs by Stage" report |
| Project / village channel | Project dashboard, "Programme % Complete" report, project's photo log |
| Maintenance | Maintenance request form, "Open Requests" report |
| Health & Safety | Incident submission form, "Open H&S Items" report, H&S monthly dashboard section |
| Finance | Approval queue report, budget vs actual dashboard |

### Common mistakes

- Over-alerting: every row change goes to a channel and people mute it
- Using Teams chat as the approval record (use Smartsheet's approval columns + Power Automate adaptive cards instead)
- Duplicating discussion across Teams chat and Smartsheet row comments — pick one channel per topic

---

## 2. Word and PowerPoint — branded reports

Smartsheet is **not the right tool** for board-facing monthly reports. Use Word or PowerPoint templates that consume Smartsheet outputs.

See the full pattern in `report-production.md`. Headlines here:

- Build a `.dotx` (Word) or `.potx` (PowerPoint) with locked styles, palette aligned to the Smartsheet dashboard, KPI tile and RAG strip patterns as table-based components
- Every "data block" is a paste-in: dashboard widget screenshot, Smartsheet report screenshot, or short narrative
- Pre-populate as much current data as you can in the template (e.g. live risk-register top 5), so each month is mostly screenshot refresh + narrative trim
- Export final report to PDF; distribute via Outlook, Teams Files tab, or SharePoint

### When to use Word vs PowerPoint

| Choose Word when | Choose PowerPoint when |
|---|---|
| Long-form narrative + tables + photos | Slide-style visual layout |
| Board / PCG / lender style monthly report | Conference, presentation, or pitch deck |
| Distribution is read-only PDF | Will be live-presented in a meeting |
| Author is more comfortable in Word | Author is comfortable in PowerPoint |

---

## 3. Excel — analysis and ad-hoc reporting

Default position: **do not duplicate Smartsheet data into Excel for ongoing reporting** — fix the Smartsheet metrics/report layer instead.

Legitimate Excel uses:

- One-off analysis or modelling that doesn't need to recur
- Pivot tables off a Smartsheet export when investigating a question
- Complex financial workbooks that already live in Excel (BBD-style drawdown sheets, cashflow models)
- Power Query refresh into Excel for analysts who need scripted transforms

### How to pull Smartsheet data into Excel

| Method | Plan | Best for |
|---|---|---|
| Export to Excel from a sheet or report | Any plan | One-off snapshots |
| Power Query → Smartsheet API (custom connector or web data source with token) | Any plan, free | Repeatable refresh, analysts |
| Smartsheet Live Data Connector (ODBC) | **Premium add-on** | Repeatable refresh in Excel/Power BI/Tableau without API plumbing |

### Common mistakes

- Sending Excel files around by email when the Smartsheet report would serve
- Letting Excel become the de-facto source of truth — drift from Smartsheet
- Using Excel for board reporting because "Smartsheet looks ugly" — fix the dashboard

---

## 4. Power Automate — the free Smartsheet ↔ Microsoft bridge

Power Automate is the single most useful Microsoft tool for Smartsheet users. **Included in most M365 business plans, works on any Smartsheet plan.**

### Recipe library

| Recipe | Trigger | Action |
|---|---|---|
| Adaptive card on row added | Smartsheet: new row | Teams: post adaptive card with row fields + Approve/Reject buttons |
| Outlook approval | Smartsheet: status = Submitted | Outlook: start-and-wait-for-approval mail; on response, update Smartsheet status |
| Calendar event from date | Smartsheet: row added/modified with Due Date | Outlook: create calendar event for assigned contact |
| File mirror to SharePoint | Smartsheet: attachment added | SharePoint: copy file to `/Projects/{Project}/{RowID}/` |
| Weekly digest | Schedule: Monday 8am | Smartsheet: read KPI summary; Outlook: email digest to leadership; Teams: post in #leadership |
| New Microsoft Form submission → Smartsheet row | Microsoft Forms: response | Smartsheet: add row with mapped fields |
| Daily overdue scan | Schedule: 7am | Smartsheet: filter overdue; Teams: post to operations channel with mention |
| PDF on completion | Smartsheet: status = Complete | Word/SharePoint: render PDF from template, save to SharePoint, link back to row |
| Cross-village rollup | Schedule: monthly | Read 4 project dashboards; write to `RPT - Portfolio Rollup`; email to board |

### Build rules

- Keep flows small and named clearly: `[Smartsheet→Teams] Row added → ops channel card`
- Use the same automation register as Smartsheet-native automations (one source of truth)
- Test in a staging sheet before pointing at production
- Document the Power Automate environment and ownership — flows die quietly when an owner leaves

---

## 5. SharePoint and OneDrive — document repository

Treat SharePoint or OneDrive as the **document store**. Smartsheet attachments should preferentially be **links to SharePoint files**, not native uploaded copies — keeps version control and permissions in one system.

### Patterns

- **Per-project folder structure** in SharePoint mirroring the Smartsheet workspace layout: e.g. `Documents/107 Papamoa/02 Civil/Contracts/`
- **Link Smartsheet rows to the relevant SharePoint document** via the row attachment URL field
- **Power Automate** to enforce structure: when a row is created in `OPS - Active Jobs`, create the matching SharePoint folder tree
- **Document libraries** with metadata columns (project, stage, document type) for searchability beyond folder structure

### What not to do

- Store the only copy of a contract or drawing as a Smartsheet attachment — versioning, permissions, and discoverability suffer
- Build a parallel folder structure that drifts from Smartsheet's workspace structure

---

## 6. Outlook — calendar and mail

### Patterns

- **Calendar events** from Smartsheet date columns via Power Automate (e.g. settlement dates from the Sales Tracking sheet automatically appear in the sales manager's Outlook calendar)
- **Approval mail** via Power Automate's "Start and wait for approval" — recipient approves from Outlook mobile without opening Smartsheet
- **Smartsheet's Send via email** for one-off PDF/Excel distribution
- **Outlook Add-in for Smartsheet**: convert an incoming email into a Smartsheet row (good for client requests, supplier responses)

### Mistakes

- Using Outlook flags or folders as a project workflow — should be in Smartsheet
- Long email threads as the audit trail for approvals — push to Smartsheet approval columns

---

## 7. Power BI — when Smartsheet dashboards aren't enough

Smartsheet's native dashboards handle most needs. Reach for Power BI only when:

- You need to **combine Smartsheet with other data sources** (SQL, finance system, Excel models, Salesforce)
- The visualisation Smartsheet can't do natively (sankey, scatter, geographic maps with custom layers, drill-through)
- Cross-portfolio analytics with row-level security (lender sees only their loans, etc.)

### How

| Path | Plan | Notes |
|---|---|---|
| Power BI custom connector via Smartsheet API + token | Any plan | Free but fiddly; refresh tokens need maintenance |
| Smartsheet OData connector | Premium add-on | Easier, but a paid feature |
| Smartsheet Live Data Connector (ODBC) | Premium add-on | Required for Tableau too |

### Mistakes

- Building a Power BI dashboard to compensate for a poorly structured Smartsheet — fix the source first
- Letting Power BI dashboards proliferate without ownership — same governance rules apply

---

## 8. Microsoft Forms vs Smartsheet Forms

Both are good. Pick based on where the response should land and what the workflow needs.

| Use Smartsheet Forms when | Use Microsoft Forms when |
|---|---|
| Response → Smartsheet row → workflow → approval | Response → SharePoint list or Excel for later analysis |
| Conditional logic that depends on Smartsheet column values | Quizzes, surveys, scored questions, training feedback |
| Form is part of an operational process (maintenance, H&S, variations) | One-off feedback, event registration, polling |
| Internal users, simple structured intake | External respondents, larger audiences |
| You want forms managed alongside the sheet | You want forms managed alongside other M365 content |

**Bridge pattern**: if a stakeholder strongly prefers Microsoft Forms but the data needs to drive a Smartsheet workflow, use Power Automate to push Microsoft Forms responses into a Smartsheet intake sheet.

---

## 9. Common patterns by department

### Construction / project ops

- Teams channels per project / village
- Smartsheet dashboard pinned in each channel
- Power Automate for: variation approval (Outlook adaptive card), site photos (SharePoint mirror), H&S incident alerting (Teams + Outlook), weekly progress digest (Teams)
- Word PCG monthly report consuming dashboard screenshots — see `report-production.md`

### Operations / maintenance

- Teams maintenance channel with intake form pinned + open requests report
- Smartsheet Forms for fast intake; Power Automate to acknowledge and triage
- SharePoint for asset documents, linked from Smartsheet asset register

### Sales / commercial

- Outlook calendar events from settlement dates (Power Automate)
- Smartsheet sales tracking sheet → weekly Teams digest in #sales
- Word/PowerPoint client report templates using Smartsheet report exports

### Finance / approvals

- Outlook approval flows via Power Automate for variations, POs, budget changes
- Excel for live financial modelling (BBD drawdown, cashflow) — Smartsheet stores summary only
- Monthly board pack as Word PDF, distributed via Teams and Outlook

---

## 10. What not to do

- Recommend premium add-ons (Live Data Connector, Bridge, DataMesh) as the default solution when Power Automate would suffice
- Pin too many Smartsheet tabs in Teams channels — pick the one or two each team actually uses
- Push every Smartsheet alert into Teams — alert fatigue undermines the value
- Re-key Smartsheet data into Excel/Word for ongoing reporting — duplication causes drift
- Use Smartsheet attachments as the canonical document store when SharePoint/OneDrive exists
- Treat Power BI as a replacement for fixing a poorly structured Smartsheet
- Forget about plan tier — always confirm whether the recommended feature is Business-included or requires premium
