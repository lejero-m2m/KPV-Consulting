# KPV Operating Conventions

Authoritative conventions for the Karaka Pines Villages (KPV) systems project. When working in the KPV context, this file overrides anything in the generic skill — workspace prefixes, sheet names, naming conventions, brand assets, and documentation patterns are all locked to what's recorded here.

When working outside the KPV context, ignore this file and use the generic guidance in `business-plan-guide.md` and `templates.md` instead.

**Last updated:** 2026-05-14 (from Kyle's project instructions)

---

## 1. Purpose and context

Kyle Dickinson, Director of Development at KPV, is building a comprehensive digital operating system for Karaka Pines Villages — a multi-village retirement development portfolio in New Zealand. The goal is a scalable, integrated technology stack supporting the full village lifecycle from feasibility through to ongoing maintenance.

**Success** looks like a clean, consistent system across all platforms that can be templated and deployed across multiple village developments.

---

## 2. Platform stack and interface philosophy

| Platform | Role |
|---|---|
| **Microsoft Teams** | Primary interface for the whole team — communication, document access, dashboards, Smartsheet report viewing |
| **SharePoint** | Backend document storage and file hierarchy, operates in the background via Teams |
| **Smartsheet** | Development team's primary project management tool. **Web app: `app.smartsheet.au`. API: `api.smartsheet.com`** (the global API endpoint — this is what all scripts, the MCP toolkit, and direct API calls must use; the AU API host returns 401 for this token). Do not assume the web-app region implies the API region — they differ. |
| **Zoho CRM** | Sales pipeline, prospect management, resident onboarding |
| **Microsoft 365 / Outlook** | Email, calendar, productivity |
| **Claude (chat)** | Mapping conversations, flow chart drafting, manual writing |
| **Claude Code** | API-based Smartsheet build execution via structured markdown briefs |

### Interface philosophy

**Most of the KPV team will never open Smartsheet directly.** Development uses Smartsheet as the source of truth. Reports, dashboards, and project visibility are surfaced into Microsoft Teams channels so the broader team (sales, management, operations) can view progress without needing Smartsheet access or training. SharePoint sits behind Teams and handles document storage — users interact with it through Teams without knowing or caring about the underlying structure.

When advising on Smartsheet at KPV, always ask: **how does this surface into Teams?** If it doesn't, it's the wrong design.

---

## 3. Village register (authoritative)

Format: `[Code] [Location] ([Region]) - [Village Name]`

- **100** Rotorua (BOP) — Regency Park
- **101** Bethlehem (BOP) — Kempton Park
- **102** Ham East (WKT) — Roseland Park Village
- **103** Rolleston (CAN) — Woodcroft Estate
- **104** Drury (AKL) — Karaka Lifestyle Estate
- **105** Rototuna (WKT) — Karaka Pines Rototuna
- **106** Waihi Beach (WKT) — Karaka Pines Waihi Beach
- **107** Papamoa (BOP) — Karaka Pines Papamoa

**Trial village: 107 Papamoa.** Template patterns are validated on Papamoa before being rolled out to other villages. **Template-first discipline** — validate and clean on 107 before deploying elsewhere.

Regions: BOP (Bay of Plenty), WKT (Waikato), AKL (Auckland), CAN (Canterbury).

---

## 4. KPV village lifecycle

Seven phases, gated by Board approval at the end of Feasibility:

1. **Feasibility** — sub-stages: Gateway feasibility, Comprehensive feasibility, Go/No-go decision
2. **Design and Consenting**
3. **Procurement and Tendering**
4. **Infrastructure (Civil Delivery)**
5. **Vertical Construction (Civil Construction)**
6. **Sales and Handover**
7. **Maintenance**

After Board approval (end of Feasibility), the village workspace is set up and the sequential phases run.

### Cross-cutting registers

These sit alongside the phases — multiple phases write into them:

- Variations Register
- Risk Register
- Health and Safety Register

---

## 5. SharePoint and Smartsheet folder structure

Each village has a workspace cloned from `XXX - Village Template`, with these subfolders:

- **01 Feasibility**
- **02 Design Civil and Construction** (houses Design and Consenting, plus Civil Delivery and Civil Construction)
- **03 Procurement**
- **04 Sales and Handover**

**Maintenance** sits in the portfolio-level Maintenance Tracker, not the per-village workspace.

The same folder structure is mirrored across SharePoint and Smartsheet so the team sees the same hierarchy wherever they look.

---

## 6. Naming conventions (locked)

| Asset | Convention | Example |
|---|---|---|
| Project numbers | `KPV-YY-NNN` | `KPV-25-001` |
| Ticket IDs | `KPV-[CODE]-NNNN` | `KPV-RSK-0123` |
| Village codes | Numeric 100–107, used as prefix on workspace names | `107 - Papamoa` |
| Stage references | `[VillageCode]-S[N]` or `S[N][Letter]` | `107-S1`, `107-S2A` |
| Trade codes | Alphanumeric short codes set per trade | `V01` (vertical construction package 1) |
| Tender Pack codes | `VillageCode-StageCode-TradeCode-Sequence` | `107-S1-V01` |
| Civil Item IDs | `[VillageCode]-CW-S[N]-NNN` | `107-CW-S1-003` |

**Critical:** all platform names, folder structures, and workspace names follow the same conventions across Teams, SharePoint, Smartsheet, and Zoho. **Inconsistency between platforms is a failure mode**, not a stylistic preference.

### Style rules

- **Hyphens, not em dashes** in names
- **"and", not ampersands** in names (`Civil and Construction Programme`, not `Civil & Construction Programme`)
- Consistent across all platforms

---

## 7. Sheets and registers (current intent — open to discussion)

The list below represents Kyle's **current simplified intent**. The previous structure had large sheets (separate Civil Programme + Construction Programme; Typology Register vs Unit Register; Sales Tracking as its own register) that grew unwieldy and ran against the "one canonical sheet per concept" rule. The list here consolidates them.

**This is not frozen.** Kyle and the agent will discuss best structure on an ongoing basis. The list is the working target — improvements that further simplify or better align with platform limits (see `smartsheet-capabilities-and-limits.md`) are welcome. When you encounter a divergence between the live Smartsheet and this list, **discuss with Kyle before acting** — don't silently rename, merge, or archive.

### Per village (working target)

- **Unit Register** (was Typology Register; renamed and broadened)
- **Civil and Construction Programme** (combines previous separate Civil Programme + Construction Programme)
- **RFQ and Quote Register**
- **Contract Register**
- **Variation Log**
- **Resource Consent Register**
- **Risk Register**
- **Health and Safety Register**

### Central / portfolio

- **Village Register** (Portfolio Overview workspace)
- **Build Status** (Portfolio Overview workspace)
- **Supplier Register** (Central Registry — master register with Consultant / Subcontractor / Supplier type checkboxes)
- **Maintenance Register** (Central Registry / Maintenance Tracker)

### Sheets in the live Smartsheet that don't match this list

Currently the live Smartsheet still carries some earlier names (e.g. `107 - Civil Programme` and `107 - Construction Programme` as separate sheets; `107 - Sales Tracking` as a standalone register). These represent **in-flight migrations** — the consolidation conversation is ongoing. When working with them:

- Use the live name in API calls and registry entries
- Flag the divergence to Kyle in writing
- Don't auto-rename or auto-consolidate without an explicit instruction

---

## 8. Brand assets

**Formatting is confirmed per task, not locked.** Two valid palette/typography sets are documented below. At the start of any piece of work, ask Kyle which one applies. Default to the systems-project palette for internal/PCG documents and the marketing palette for public-facing or brand-led work.

### Option A — Systems project / PCG palette

| Role | Name | HEX |
|---|---|---|
| Primary brand | Dark Navy | `#1A2332` |
| Accent | Bright Green | `#2ECC71` |
| Background | Light Grey | `#F4F6F8` |
| Surface | White | `#FFFFFF` |
| Body text dark | Dark Charcoal | `#2C3E50` |

Typography: **Arial throughout** (headings and body). Headings **black**, not navy or blue.

Tables: header row dark navy `#1A2332` with white bold text; body rows white, no alternating shading; **first column bold**; hyphen bullets within cells.

Bullets: **hyphen markers (`-`)**, not dots.

Flow PNGs: white background, single tall column, coloured rounded boxes per band — style matches the procurement, civil delivery, and civil construction flows already built.

### Option B — Marketing palette (from `reference/brand-guidelines.md` working draft)

| Role | Name | HEX |
|---|---|---|
| Primary brand | KPV Navy | `#1B3A5B` |
| Accent | Leaf Green | `#7FC242` |
| Action Green | Action Green | `#71BF44` |
| Subtitle Grey | Subtitle Grey | `#A8A49B` |
| Ink (body text) | Ink | `#3A3A3A` |
| Paper (section bg) | Paper | `#F5F5F5` |
| Rule (dividers) | Rule | `#E5E5E5` |

Typography: classical serif heading (Garamond / Source Serif Pro) + humanist sans-serif body (Calibri / Source Sans Pro).

This palette appears in the existing `PCG Monthly Report - Papamoa - TEMPLATE.docx` and matches website / brand-led collateral inferred from the public KPV site.

### Picking between them

| Use Option A (systems / PCG) when… | Use Option B (marketing) when… |
|---|---|
| Internal section manuals, flow charts | Public-facing brochures, prospectus |
| Process documentation | Resident-facing material |
| KPV team-only board / PCG reports | Lender / external trustee summaries where the brand-led look matters |
| Anything that pairs with a Smartsheet dashboard | Print collateral |

If unclear at the start of a task, **ask Kyle which palette to use** rather than picking silently.

---

## 9. Documentation suite

Every section flow gets **two artefacts**:

1. **Flow PNG** — white background, single tall column, coloured rounded boxes
2. **Word manual** — Arial 11 pt, black headings, hyphen bullets, navy-header tables with bold first column. Embeds the flow PNG in the Process flow section.

### Manual section structure (standard)

Every section manual follows this template:

- Title block: subject (large bold), "Section manual" (subtitle), "Karaka Pines Villages - 107 Papamoa", "Version 1.0 - April 2026"
- Purpose
- Process flow (with embedded flow PNG)
- Roles
- [Section-specific body content]
- Status reference
- Automations
- Data model
- Permissions or Form configuration (where relevant)
- Common scenarios (where relevant)
- Integration with other sections
- Open items
- Change history

### Mapping conversation pattern

For each new section the workflow is:

1. **Mapping conversation** — Claude asks clarifying questions, Kyle answers, the flow is worked out
2. **Flow chart** — rendered as inline SVG first for review, then exported as a white-background PNG
3. **Manual** — Word doc following the standard structure, with the flow PNG embedded

---

## 10. Documentation status (as of 2026-05-14)

| Section | Flow | Manual | Status |
|---|---|---|---|
| Master flow | Done | Not required | Kyle requested PNG only |
| Feasibility | Not mapped | — | Future |
| Design and Consenting | Not mapped | — | Future |
| Procurement | Done | Done | Complete |
| Civil Delivery | Done | Done | Complete |
| Civil Construction | Done | Done | Complete |
| Sales and Handover | Not mapped | — | Future |
| Maintenance | Not mapped | — | Future |
| Variations | Not mapped | — | Next session |
| Risk | Not mapped | — | Future |
| Health and Safety | Not mapped | — | Future |

**Update this table** as sections progress.

---

## 11. Key principles

- **Template-first discipline** — validate and clean on 107 Papamoa before deploying to other villages
- **Less is more** — simple, scalable design over complexity
- **Naming conventions matter** — hyphens not em dashes, "and" not ampersands, consistent throughout all platforms
- **Iterative refinement before building** — structure and naming locked in before execution
- **Platform alignment** — all systems reflect the same village hierarchy, naming conventions, and lifecycle phases
- **Teams as the window** — Smartsheet is the engine, Teams is what most people see — design outputs with that in mind
- **Builders own delivery, PM owns oversight** — automated notifications to PM rather than gate-keeping verification steps
- **Flow + manual pattern** — every section gets the same two artefacts in the same style

---

## 12. Approach and patterns

- Works **iteratively** — mapping conversation first, flow chart second, manual third
- **Single-word confirmations** like "Continue" mean proceed with the established plan
- Prefers conversational problem-solving over multiple-choice option lists where possible, but multiple-choice is acceptable when concrete options need to be chosen
- Reviews flow charts visually before committing to the manual
- **Pushes back on over-engineered solutions** that won't scale
- Applies changes **template-first** before rolling out to live village instances
- Expects Claude to **flag cross-platform implications** when making changes to any single platform
- When advising on any platform, considers **how it surfaces into Teams** for the broader team
- Proceeds pragmatically with what exists rather than realigning to documentation when drift occurs

### Cross-session continuity

- **Artefacts do not persist between sessions** — Claude flags this when delivering files
- **Sheet IDs, workspace IDs, and folder IDs are documented in the userMemories** — Claude refers to those when working with specific Smartsheet objects
- **Where the userMemories drift from current state**, Kyle's latest instruction wins

---

## 13. KPV-specific Teams channel mapping

| Teams channel | Smartsheet asset / Power Automate flow |
|---|---|
| Leadership / Board | Portfolio dashboard (Build Status, Village Register summary), monthly PCG reports as PDFs in Files tab |
| 107 Papamoa | 107 Dashboard, monthly PCG report, Risk Report, H&S Open Items |
| Per-village channels (104/105/106/107) | Village dashboard, Civil and Construction Programme report, Sales pipeline summary |
| Procurement | RFQ and Quote Register report, Contract Register report, Supplier Register lookup |
| H&S | Health and Safety Register form, H&S monthly report |
| Maintenance | Maintenance Register report, request form |
| Sales (cross-village) | Build Status, Unit Register sales status views, Zoho CRM pipeline |

This mapping is the **default**. Adjust per how Kyle's team channels are actually structured.

---

## 14. When advising on a new section or feature at KPV

Use this checklist:

1. Does the change honour the **locked sheet naming** in section 7?
2. Does the design **surface into Teams** for the broader team?
3. Are documents using **Arial + hyphen bullets + navy `#1A2332` table headers**?
4. Are flow PNGs in the **white-background, single-column, coloured-rounded-box** style?
5. Does the work follow the **mapping → flow → manual** workflow?
6. Is it being built **on 107 Papamoa first** before rolling out to other villages?
7. Are **naming conventions** (KPV-YY-NNN, 107-S1, 107-S1-V01, etc.) used consistently?
8. Are **cross-platform implications** flagged (Teams / SharePoint / Smartsheet / Zoho)?
9. Does the recommendation respect the **API capability matrix** in `smartsheet-capabilities-and-limits.md`? (Reports/dashboards/forms/automations are UI-only — design once, don't churn)
10. If a polished document is being produced, does it follow the **report-production.md** pattern using KPV's authoritative palette and Arial typography?

---

## 15. Where this file fits

This file is the **first reference to consult** when working in the KPV context. It supersedes generic guidance in `business-plan-guide.md`, `templates.md`, and `microsoft-integration.md` wherever there's a conflict — but those generic files are still useful for:

- General architectural patterns
- API capability reference
- Microsoft 365 integration recipes
- Plan-tier matrix

Read this file first, then the generic files for the underlying patterns.
