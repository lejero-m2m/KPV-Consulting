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
| **Smartsheet** | Development team's primary project management tool. **Web app and API are both on the North American region: `app.smartsheet.com` / `api.smartsheet.com`** (confirmed 2026-05-22 inventory). The `.au` host is not used. |
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

**Per-village 7-folder structure (locked 2026-05-22 in Phase 2.5 architectural review):**

- **00 - Dashboards** (incl. Chart Sources sub-folder)
- **01 - Project Control** — Unit Register, Risk Register, Decision Log, Monthly RAG Log (shared reference layer + governance artefacts; serves all teams)
- **02 - Sales** — Sales Register
- **03 - Procurement** — RFQ and Quote Register, Contract Register, Variation Log (procurement lifecycle comes BEFORE construction in folder order to reflect lifecycle order)
- **04 - Civil and Construction** — Civil Programme, Construction Programme, Construction Register (delivery timelines + per-building register)
- **05 - Health and Safety** — H and S Incidents and Observations, H and S Monthly Indicators
- **06 - Reports** with sub-folders `Internal/` and `External/`

**Maintenance** sits in the portfolio-level Maintenance Tracker, not the per-village workspace.

The same folder structure is mirrored across SharePoint and Smartsheet so the team sees the same hierarchy wherever they look.

> **107 live state (2026-05-23):** the 7-folder structure is **live**. Executed via REST API on 2026-05-23 (PUT /sheets/{id}, PUT /folders/{id}, POST /sheets/{id}/move, POST /folders/{id}/move, POST /reports/{id}/move, DELETE /folders/{id}). The MCP toolkit does not expose sheet/folder rename or move, but direct REST calls with the KPV API token work — that pattern is now established and the same approach will apply when templating to 105/106 in Phase 4.

---

## 6. Naming conventions (locked)

This section is the high-level summary. **The detailed, authoritative naming standard lives in [`kpv-naming-conventions.md`](kpv-naming-conventions.md)** — covers column names, cross-sheet reference names (with locked abbreviations: UR, SR, RR, DL, MRL, ConP, CivP, ConR, ContR, VL, RFQ, HSI, HSM, TR, SuppR, PF), AUTO_NUMBER ID formats, picklist value sets, automation/Power Automate flow names, SharePoint folder naming, and common mistakes to avoid. Update that file when establishing new naming conventions.

### High-level pattern summary

| Asset | Convention | Example |
|---|---|---|
| Project numbers | `KPV-YY-NNN` | `KPV-25-001` |
| Ticket IDs | `KPV-[CODE]-NNNN` (4-digit padding per `kpv-naming-conventions.md` §3) | `KPV-RSK-0123` |
| Village codes | Numeric 100–107, used as prefix on workspace names | `107 - Papamoa` |
| Stage references | `[VillageCode]-S[N]` or `S[N][Letter]` | `107-S1`, `107-S2A` |
| Building Reference | `S[Stage]-B[NN]` — cross-sheet join key | `S1-B05` |
| Trade codes | Alphanumeric short codes set per trade (V/C/E/R/L/S) | `V01` (vertical construction package 1) |
| Tender Pack / Trade Package codes | `VillageCode-StageCode-TradeCode-Sequence` | `107-S1-V01` |
| Civil Item IDs | `[VillageCode]-CW-S[N]-NNN` | `107-CW-S1-003` |
| AUTO_NUMBER per-sheet IDs | `[VillageCode]-[3-letter Type]-[4-digit Seq]` | `107-VAR-0001`, `107-RFQ-0001`, `107-CON-0001`, `107-DEC-0001`, `107-RSK-0001`, `107-HSE-0001` |
| Quote ID (RFQ child rows) | `[Parent RFQ ID]-Q[2-digit]` | `107-RFQ-0001-Q01` |

**Critical:** all platform names, folder structures, and workspace names follow the same conventions across Teams, SharePoint, Smartsheet, and Zoho. **Inconsistency between platforms is a failure mode**, not a stylistic preference.

### Style rules (high-level — see `kpv-naming-conventions.md` for the full set)

- **NZ English throughout** — colour, organisation, prioritise
- **Hyphens, not em dashes** in names
- **"and", not ampersands** in names (`Civil and Construction Programme`, not `Civil & Construction Programme`). One historical exception: `H&S` in Decision Log Decision Type picklist, accepted as-is.
- **Title Case** for labels and picklist values
- **Yellow not Amber** for RAG picklists everywhere
- Consistent across all platforms

---

## 7. Sheets and registers (current intent — open to discussion)

The list below represents Kyle's **current simplified intent**. It is not frozen — Kyle and the agent will discuss best structure on an ongoing basis. When you encounter a divergence between the live Smartsheet and this list, **discuss with Kyle before acting** — don't silently rename, merge, or archive.

**107 IS the template.** Per the 2026-05-22 Phase 1 review, the XXX Village Template will be re-cut as a periodic snapshot of 107, not separately maintained.

### Per village (working target)

- **Unit Register** (was Typology Register; renamed and broadened)
- **Civil Programme** — civils works only (e.g. 107 contract with Matco)
- **Construction Programme** — per-building build phases (e.g. 107 contracts with Signature Homes)
- **Construction Register** — consolidates Programme rows up to per-building entries; carries cross-sheet pulls for Construction Status, Budget; feeds Unit Register and Sales Register
- **Sales Register** (was "Sales Tracking"; now lives under 01 - Project Control on 107)
- **Variation Log** — built on 107 in Phase 2 (2026-05-22). 2-level approval (PM/Director); auto-escalates to Director when \|Cost Impact\| > $25,000 via column formula. Intake via `FORM - Variation Submission` (UI build pending).
- **RFQ and Quote Register** — built on 107 in Phase 2 (2026-05-22). Single sheet, parent (Type=RFQ) + child (Type=Quote) via indent. AUTO_NUMBER sequence is shared (`107-RFQ-001`). Two intake forms pending UI build: `FORM - RFQ Creation` (internal), `FORM - Quote Submission` (public URL for suppliers).
- **Contract Register** — built on 107 in Phase 2 (2026-05-22). Direct entry (no form), triggered by RFQ award. One row per contract; `Stages Covered` is MULTI_PICKLIST. Variations to Date column pending UI conversion to SUMIFS cross-sheet formula against Variation Log.
- **Decision Log** — built on 107 in Phase 2 (2026-05-22), lives in `01 - Project Control`. Captures Board + PCG + PM decisions. Backfill of 5 historic Board decisions deferred — manual entry.
- **Risk Register** — Score and RAG converted to column formulas in Phase 2.5 (Score = Likelihood × Consequence; RAG derived from Score with thresholds: ≥15 Red, 8–14 Yellow, <8 Green, blank Gray). `Date Identified` CREATED_DATE column added. Categories include `HS` (no ampersand — divergence from Decision Log's `H&S`; documented in parked decisions).
- **Monthly RAG Log** — formerly `107 - PCG Status Snapshot`; renamed in Phase 2.5. Sheet now holds 12 cols: Period Label, Period Date, Is Current Period, Overall RAG, Submitted By, Quality RAG (standardised options to Red/Yellow/Green/Gray; symbol RYGG application is UI follow-up), Programme RAG, Cost RAG, Health and Safety RAG, Sales RAG, Maori Procurement RAG, Overall Commentary. Narrative blocks, sales counts, and Top Risks Summary cut — they live in the PCG Word doc, Sales Register, or Risk Register respectively.
- **Health and Safety: Incidents and Observations** + **Monthly Indicators** (two sheets in the live template). Incidents `Type` picklist deduped in Phase 2.5 (removed redundant "Lost Time Injury"; canonical is "LTI"). Monthly Indicators `Contractor` picklist must exactly match Supplier Register Trading Names — spelling drift causes silent reporting mismatches. Adding a contractor here means adding the same Trading Name to Supplier Register first.

**Civil + Construction Programme are intentionally separate sheets.** Earlier intent (one combined "Civil and Construction Programme" sheet) was reviewed 2026-05-22 and rejected: civils and building have different primary keys (Task Name vs Building Reference), different hierarchies, different counterparties (Matco vs Signature Homes), and different cost-column shapes. Merging would force either a flat master Gantt that loses both hierarchies, or two primary trees in one sheet (Smartsheet only supports one primary column). Keep separate.

**Stage picklist divergence is deliberate.** Civil Programme uses `Stage 1, Stage 2, Stage 3, Stage 4, Stage 5, Clubhouse` (no sub-stages — civils don't sub-divide stage 2). Construction Programme, Construction Register, Variation Log, RFQ Register, Contract Register, Decision Log, and the Sales/Project Control sheets use `Stage 1, Stage 2A, Stage 2B, Stage 2C, Stage 2D, Stage 2E, Stage 3, Stage 4, Stage 5`. Future templating to 105/106 must preserve this difference.

**Programme sheets are timeline-only as of Phase 2.5.** Construction Programme and Civil Programme no longer carry financial columns. Construction Programme cut: Build Partner, Contract Package, Contract Price, Variations, Budget Approved, Expected Total Cost, Expected Variance. Civil Programme: cuts deferred (Section I) — Matco contract values stay on Civil Programme until Contract Register is populated with the Matco Stage 1 row (then Civil Programme financials will be cut in a follow-up).

**Resource Consent Register is intentionally NOT in the 107 template** (decision 2026-05-22). Consent status lives on `107 - Construction Register` (Consent Lodged, Consent Approved, Building Consent Number, Days to Approval, Consent Status PICKLIST) and flows up to `107 - Unit Register` (Consent Status formula). 104 still has a standalone Resource Consent Register; do not delete that without instruction.

### Central / portfolio

- **Portfolio Register** (000 - Overview / 01 - Portfolio Overview — also referred to as "Village Register" by dashboards)
- **Supplier Register** (000 - Overview / 02 - Supplier Compliance)
- **Insurance Register**, **Statutory Compliance Register**, **KPV Risk Register**, **KPV Risk Actions** (000 - Overview / 04 - Governance)
- Project reference registers — **Exterior / Interior / F&F Scheme**, **Typology**, **Status** (000 - Overview / 03 - Project Reference Registers)
- **Maintenance Register** (Central Registry / Maintenance Tracker — not yet built)

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

### Sheet design rules (added 2026-05-22 in Phase 2.5)

These govern every sheet change going forward. They are not negotiable in a single conversation.

1. **One sheet, one job.** Each sheet has a single primary purpose. No sheet does timeline AND finance AND status.
2. **Programmes track time. Registers track state. Contracts hold contract values. Variations hold variations. Project Finance holds budgets.**
3. **Canonical source per concept.** Each fact lives in one place. Other sheets pull via cross-sheet formula, not manual entry.
4. **Picklists for stable known values; cross-sheet formula lookups for values that drift** (suppliers, contractors).
5. **Folder structure serves human navigation.** Different teams see different folders.
6. **Folder moves and sheet renames are formula-safe.** Cross-sheet references use sheet IDs, not names or paths.
7. **Column renames may break formulas.** Audit cross-sheet references before any rename.

These principles drove Phase 2.5: financial columns cut from Programmes (rule 2), Build Partner formula-driven from Supplier Register (rule 4), Construction Register pulls from Construction Programme + Contract Register + Variation Log (rule 3), Procurement folder distinct from Sales and Civil/Construction (rule 5).

### Parked decisions (review dates locked)

| Decision | Status | Review by |
|---|---|---|
| Trade Package — TEXT_NUMBER free-text vs PICKLIST | Free-text on Variation Log, RFQ Register, Contract Register | 2026-11-01 |
| H&S Incidents Entry ID — manual TEXT_NUMBER vs AUTO_NUMBER | Manual entry — keep until volume justifies | 2026-11-01 |
| Cost Band threshold ($25,000) — baked into Variation Log formula vs parameter sheet | Baked in formula; change requires column edit | Review when finance wants per-stage thresholds |
| H&S naming divergence — `H&S` (Decision Log Decision Type, dashboards) vs `HS` (Risk Register Category) vs `H and S` (folder + sheet titles) | Accepted as-is; do NOT normalise this session | Revisit only if cross-sheet filter on H&S category becomes needed |
| RFQ Register shared AUTO_NUMBER on parent (RFQ) + child (Quote) rows | Accepted as-is. Separate `Quote ID` column added in Phase 2.5 for derived child IDs (`107-RFQ-001-Q01` format) — manual entry initially. | If procurement finds mixed IDs confusing, swap Quote ID to formula |
| Insurance Expiry on Contract Register — manual entry vs cross-sheet formula to Supplier Register | Manual for now (Insurance Verified + Insurance Expiry + H and S Inducted columns were cut in Phase 2.5; `Supplier Insurance Status` formula column added in their place — pending UI conversion to actual cross-sheet formula) | Phase 3 |
| Archive strategy for completed contracts | No archive sheet yet | Decide before contract volume grows |
| Operations workspace (cross-village resident/maintenance work) | Conversation needed; not now | When Operations arm signals readiness |
| Cross-village role-based dashboards (GM Developments, GM Sales and Operations) | Phase 5 (after Phase 4 villages on same structure) | Phase 5 |
| Variation threshold review | Quarterly until pattern stabilises, then annual | Quarterly from Q3 2026 |
| QS role addition (currently no QS — PM handles quantities) | Watch as KPV org structure expands | When volume/complexity demands |
| Email-to-workflow integration (Variations first) | Phase 6 — after Phase 4 lands | Phase 6 |

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

Read this file first, then the generic files for the underlying patterns. For detailed column/picklist/AUTO_NUMBER/cross-sheet-reference naming, see [`kpv-naming-conventions.md`](kpv-naming-conventions.md).

---

## 16. Organisational structure (added 2026-05-22)

KPV operates as two arms under a single Senior Leadership Team.

```
Liam (CEO)
├── Julie (CFO)
├── Kyle Dickinson (GM Developments)
│   └── Matt (Delivery Lead / Project Manager)
└── Stu (GM Sales and Operations)
    └── Deborah (Operations Lead)
```

**Senior Leadership Team (SLT):** Liam, Julie, Stu, Kyle.

### Two arms of operation

| Arm | Scope | Lead |
|---|---|---|
| **Developments** | New villages, construction, greenfield through site handover | Kyle (GM Developments) |
| **Operations** | Management of existing villages, completed units, residents, maintenance | Stu (GM Sales and Operations) |

### Crossover principle

Matt (Delivery Lead) sits in Developments but handles construction-related maintenance issues raised by Operations. He is the operational bridge between the two arms for any post-handover construction work (defects, warranty, maintenance involving build trades).

### Implications for Smartsheet design

- Column labels for approvers carry the role qualifier: `L1 Approver (Delivery Lead)`, `L2 Approver (GM Developments)`, etc. — per `kpv-naming-conventions.md` §1.
- Module-arm split shapes sheet access patterns: Developments arm sees the per-village 04 Civil and Construction + 03 Procurement folders; Operations arm primarily sees 02 Sales + the (future) Operations workspace.
- Cross-functional decisions (Decision Log) require Stu OR Kyle approval depending on focus; Kyle has final commercial sign-off on development feasibility.

---

## 17. Approval Matrix (added 2026-05-22)

KPV uses three approval patterns depending on item type:

1. **Approval workflow** — formal sign-off before action (Variations, Contracts, certain Decisions)
2. **Ownership assignment** — named owner manages, no approval-to-exist (Risks, RFQ requests)
3. **Notification / record** — communication only (H&S incidents, operational decisions)

### Matrix

| Item type | Raise | Approve L1 | Approve L2 | Final sign-off | Escalation |
|---|---|---|---|---|---|
| Variation ≤ $5k | Matt | Matt approves | — | — | — |
| Variation $5k–$25k | Matt | Matt raises | Kyle approves | — | — |
| Variation $25k–$50k | Matt | Matt raises | Kyle approves | Julie co-signs (CFO) | — |
| Variation > $50k | Matt | Matt raises | Kyle + Julie | Liam (CEO) | — |
| Sales decision (typology/pricing/commercial) | Deborah | Deborah raises | Stu approves (sales side) | Kyle approves (development side) | Liam if material |
| RFQ request (issue an RFQ) | Anyone | Matt or designate | — | — | — |
| Contract award (low/medium) | Matt | Matt raises | Kyle approves | Liam OR SLT member signs | — |
| Contract award (material) | Matt | Matt raises | Kyle approves | Julie + Liam co-sign | — |
| Risk Register entry | Anyone | n/a (ownership not approval) | n/a | Matt + Kyle accountable for portfolio | SLT for portfolio-significant |
| Decision Log — operational | Anyone | Matt or Deborah | — | — | Kyle or Stu if cross-functional |
| Decision Log — cross-functional | Matt or Deborah | Stu OR Kyle (depending on focus) | Kyle final commercial sign-off | — | Liam if strategic |
| Decision Log — strategic | SLT | Recorded post-decision | — | — | — |
| H&S incident / serious near-miss | Anyone | Matt logs | — | — | Notify SLT per H&S policy |

### Variation threshold rationale

Thresholds are conservative starting points (May 2026). Adjust as KPV's variation volume matures and patterns stabilise.

- **$5k** — operational autonomy for Matt (small site decisions don't escalate)
- **$25k** — development-level decisions (Kyle approves; significant but routine)
- **$50k** — material commercial impact (CFO co-signs; budget visibility critical)
- **>$50k** — strategic / portfolio-level (CEO sign-off required)

> **Smartsheet implementation status (as of 2026-05-22):** the live Variation Log uses a 2-tier Cost Band formula (PM vs Director at $25k threshold) inherited from Phase 2. The 4-tier matrix above is a Phase 2.5+ change that requires a Cost Band reformulation + restructured approval columns. Not yet executed — see `smartsheet/sheet-registry.md` anomalies.

### Final commercial sign-off principle

For sales decisions, Stu approves from the sales perspective (does it make sense commercially?). Kyle has **final commercial sign-off** to confirm the development side can deliver the change within budget and programme. This is not a veto on Stu's authority — it is a development-side feasibility check.

---

## 18. Data Ownership Matrix (added 2026-05-22)

Each data concept has a single canonical home. Other sheets pull via cross-sheet formula. This matrix is the authoritative source for "where does this fact live?"

| Data concept | Canonical sheet | Editable by | Read by | Automation dependencies |
|---|---|---|---|---|
| Supplier identity | Supplier Register (000 Overview) | Kyle or designated admin | All villages' RFQ, Contract, Construction Register, H&S Monthly Indicators | Updates flow downstream via cross-sheet formulas |
| Typology specifications | Typology Register (000 Overview) | Kyle or designated admin | All villages' Unit Register | Typology field changes auto-pull |
| Unit identity (Number, Stage, Typology) | Unit Register (per village) | Matt + Kyle | Sales Register, Construction Register, all reports, Decision Log refs | Sales Status formula chain reads from here |
| Sales Status (per unit) | Sales Register (per village) | Deborah + Stu | Unit Register (formula), Dashboard, reports | Unit Register auto-pulls; cross-village rollups planned |
| Construction Status (per building) | Construction Programme (per village) | Matt | Construction Register (formula), Unit Register (formula chain), reports | Status flows downstream automatically |
| Consent Status (per building) | Construction Register (per village) | Matt | Unit Register (formula), PCG Building Consent Status report | Days to Approval derived |
| Contract Value (signed) | Contract Register (per village) | Matt + Kyle | Construction Register (formula), Project Finance | Contract Price flows to Construction Register |
| Variation Cost Impact | Variation Log (per village) | Matt, with approvals per matrix | Contract Register (SUMIFS), Construction Register (SUMIFS), reports | Variations to Date auto-aggregates in Contract Register |
| Risk identity and Score | Risk Register (per village) | Matt + Kyle accountable; anyone can raise | Dashboard, PCG Risk reports | Score and RAG formula-derived |
| Decision record | Decision Log (per village) | Anyone can raise; approvals per matrix | Dashboard, PCG Top Decisions report | Cross-functional decisions flagged |
| H&S incident detail | H&S Incidents and Observations | Matt logs; anyone can raise | H&S Monthly Indicators (COUNTIFS), Dashboard, PCG H&S reports | Monthly counts auto-aggregate |
| Monthly RAG ratings | Monthly RAG Log (per village) | Matt + Kyle for Developments arm; Stu + Deborah for Operations arm | Dashboard, PCG monthly report | Manual entry monthly |
| Budget per building | Project Finance workspace (per village budget sheet) | Julie + Kyle | Construction Register (formula pull) | Budget formula already wired |
| Building identity (Building Reference) | Construction Register (per village) | Matt + Kyle | Construction Programme, Variation Log, Contract Register | Building Reference is the cross-sheet join key |

### Architectural rule

**No fact is manually duplicated across sheets.** If a value appears in two places, exactly one is canonical and the other is a cross-sheet formula pull. Any sheet whose only role is duplicating canonical data should be evaluated for deletion. This rule is the operational expression of Sheet design rule 3 (canonical source per concept) from §11.
