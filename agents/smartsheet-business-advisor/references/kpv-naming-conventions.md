# KPV Naming Conventions

**Owner:** Kyle Dickinson
**Purpose:** Lock the naming conventions that govern columns, cross-sheet references, AUTO_NUMBER IDs, picklist values, form labels, automation names, and folder structures across all KPV systems (Smartsheet, SharePoint, Teams, Zoho). Consistent naming is the foundation that lets templates, automations, email parsing, and cross-platform integration work reliably at scale.
**Status:** Locked May 2026. Changes require Kyle's approval.

---

## Why this exists

Smartsheet columns are referenced by name in Power Automate flows, form labels, cross-sheet formulas, and email parsing rules. Inconsistent naming creates silent failure modes — a flow that referenced `[Cost Impact]` breaks when someone renames the column to `[Cost Impact (NZD)]`, and the breakage isn't reported.

Across 8 villages × 13+ sheets × dozens of forms and flows, naming inconsistency compounds quickly. This document is the single source of truth.

---

## Style rules (applies to everything)

These rules apply globally and override anything else in this document where there's conflict.

1. **NZ English throughout** — colour not color, organisation not organization, prioritise not prioritize
2. **Hyphens, not em dashes** — `Cost Band - Director Approval Required` is correct; `Cost Band — Director Approval Required` is wrong
3. **"and" not ampersands** — `Civil and Construction Programme` is correct; `Civil & Construction Programme` is wrong (one historical exception: "H&S" usage in Decision Log Decision Type picklist, accepted as-is)
4. **Title Case for labels** — every significant word capitalised
5. **Spaces between words** — `Cost Impact (NZD)` not `Cost_Impact_NZD` or `costImpactNZD`
6. **No leading/trailing whitespace** — labels trimmed
7. **No abbreviations in column names** unless universally known (LTI, MTI, PSIF are OK; ABC123 isn't)
8. **Apostrophes avoided** in column names — `Suppliers` not `Supplier's`
9. **Numbers in picklists** spelt out where they could confuse — `One`, `Two`, `Three` not `1`, `2`, `3` (exception: standard 1-4 likert scales)

---

## 1. Column names

Column names appear in: the Smartsheet UI, forms, reports, dashboards, Power Automate flows, cross-sheet references, email parsing rules.

### Format

```
[Concept] [Qualifier optional] ([Unit] optional)
```

### Examples
- `Cost Impact (NZD)`
- `Floor Area (m²)`
- `Variations to Date (NZD)`
- `Settled This Period`
- `Building Reference`
- `L1 Approver (Delivery Lead)`
- `Quote Submitted Date`

### Rules
- Use parentheses for units: `(NZD)`, `(m²)`, `(days)`, `(%)`
- Use parentheses for role qualifiers on approval columns: `L1 Approver (Delivery Lead)`, `L2 Approver (GM Developments)`
- Avoid redundancy: `Variation Cost Impact (NZD)` is wrong on Variation Log (the sheet context already implies "variation"); `Cost Impact (NZD)` is right
- Special characters fine only when standard: `m²`, `%`, `(NZD)` — avoid Unicode tricks
- Maximum length: 50 characters as a soft limit. Longer labels work but get truncated in many views
- Date columns: avoid "Date" suffix when the column type makes it obvious: `Submitted` not `Submitted Date` for a DATE column (but use `Submitted Date` when it disambiguates against `Submitted By`)

### System columns
Where Smartsheet provides system columns (CREATED_DATE, MODIFIED_DATE, CREATED_BY, MODIFIED_BY), use these standard labels:
- `Created` (CREATED_DATE)
- `Modified` (MODIFIED_DATE)
- `Created By` (CREATED_BY)
- `Modified By` (MODIFIED_BY)

---

## 2. Cross-sheet reference names

Cross-sheet references must be created in the Smartsheet UI (cannot be done via API per `smartsheet-capabilities-and-limits.md` §3). Each reference has a name that's used inside formulas.

### Format

```
[Sheet abbreviation] [Column name as it appears on source sheet]
```

### Sheet abbreviations (locked)

| Sheet | Abbreviation | Notes |
|---|---|---|
| Unit Register | UR | |
| Sales Register | SR | |
| Risk Register | RR | |
| Decision Log | DL | |
| Monthly RAG Log | MRL | |
| Construction Programme | ConP | C extended to ConP to disambiguate from CivP |
| Civil Programme | CivP | Civ extended to disambiguate from ConP |
| Construction Register | ConR | C extended to disambiguate from ContR |
| Contract Register | ContR | Cont extended to disambiguate from ConR |
| Variation Log | VL | |
| RFQ and Quote Register | RFQ | |
| H and S Incidents and Observations | HSI | |
| H and S Monthly Indicators | HSM | |
| Typology Register (portfolio) | TR | |
| Supplier Register (portfolio) | SuppR | |
| Project Finance (per village budget sheet) | PF | |

### Examples
- `UR Unit Number` — Unit Register's Unit Number column
- `SR Sales Status` — Sales Register's Sales Status column
- `TR Beds` — Typology Register's Beds column
- `VL Cost Impact (NZD)` — Variation Log's Cost Impact column (note: include the (NZD) unit suffix exactly as it appears on the source sheet)
- `SuppR Trading Name` — Supplier Register's Trading Name column
- `ConR Building Reference` — Construction Register's Building Reference column
- `ContR Contract Value (NZD)` — Contract Register's Contract Value column

### Rules
- The abbreviation matches what's in the table above (do not invent new abbreviations per village)
- The column name is **exactly** as it appears on the source sheet (including unit suffixes, casing, parentheses)
- One space between abbreviation and column name
- These names are case-sensitive in formulas — match exactly

### Per-village reference uniqueness

Each village has its own copy of Unit Register, Sales Register, etc. Cross-sheet references created in (say) 104 Drury's Sales Register pointing at 104 Drury's Unit Register would still be named `UR Sales Status` — the abbreviation doesn't need village prefix because the reference is created within one village's context.

However, references pointing at portfolio-level sheets (Typology Register, Supplier Register) are universal across all villages and use the same names (`TR Beds`, `SuppR Trading Name`).

---

## 3. AUTO_NUMBER ID formats

Every sheet that needs unique row identifiers uses AUTO_NUMBER (Smartsheet system column type, not the primary).

### Format

```
[VillageCode]-[Type]-[Sequence]
```

Where:
- **VillageCode** = 3-digit village number (100-107)
- **Type** = 3-letter UPPERCASE abbreviation
- **Sequence** = 4-digit zero-padded number (0001-9999)

### Type abbreviations (locked)

| Sheet | Type code | Example |
|---|---|---|
| Variation Log | VAR | `107-VAR-0001` |
| RFQ and Quote Register | RFQ | `107-RFQ-0001` |
| Contract Register | CON | `107-CON-0001` |
| Decision Log | DEC | `107-DEC-0001` |
| Risk Register | RSK | `107-RSK-0001` |
| H and S Incidents and Observations | HSE | `107-HSE-0001` |
| Resource Consent Register (where it exists) | RCN | `104-RCN-0001` |
| Maintenance Register (portfolio) | MNT | `MNT-0001` (no village prefix, portfolio-wide) |

### Quote ID format (RFQ child rows)

RFQ Register has parent/child structure where the parent is an RFQ and children are quote responses. Quotes use a derived ID format:

```
[Parent RFQ ID]-Q[2-digit sequence]
```

Example: parent `107-RFQ-0001` has quote children `107-RFQ-0001-Q01`, `107-RFQ-0001-Q02`, etc.

Quote ID is its own column (added in Phase 2.5 Section L), not the AUTO_NUMBER primary.

### Rules
- 4-digit sequence everywhere (0001-9999) — future-proof, consistent
- Type code is always 3 letters UPPERCASE
- Hyphens between components (no underscores, no spaces)
- Portfolio-wide sheets (Maintenance Register, Supplier Register) use `KPV-[Type]-NNNN` if a village prefix doesn't make sense

### Existing data with 3-digit sequences

Phase 2.5 brief includes a task to retrofit existing 3-digit sequences (`107-RFQ-001` → `107-RFQ-0001`) where they exist. Going forward, all new IDs use 4 digits.

---

## 4. Building, unit, and stage references

These are content-level references (referring to specific buildings or units), not sheet-level IDs.

### Stage references

Format: `S[N][Letter optional]`

Examples:
- `S1` (Stage 1)
- `S2A` (Stage 2A)
- `S3B` (Stage 3B)

Each village has its own stage list per its masterplan. Stage picklists are deliberately different per village (see `kpv-conventions.md` §13).

### Building references

Format: `S[Stage]-B[NN]`

Examples:
- `S1-B01` (Stage 1, Building 1)
- `S2A-B05` (Stage 2A, Building 5)

Building Reference is the primary cross-sheet join key in Construction Register, Construction Programme, Variation Log (Linked Building column), Contract Register (where applicable).

### Unit references

Format: numeric, matching the village's unit numbering scheme.

Examples:
- `101`, `103`, `205`, `307` — standard
- `108` (Clubhouse on 107 Papamoa — accepted, not renumbered)

### Edge case: 106 Waihi Beach synthetic identifiers

Stanaway and Clarence blocks on 106 are masterplan-addressed as blocks rather than individual units. They use synthetic identifiers:

Format: `S[Stage]-[BlockNum]-[UnitNumInBlock]`

Examples:
- `S5-216-1` (Stage 5, Block 216, Unit 1 within block)
- `S5-216-2` (Stage 5, Block 216, Unit 2 within block)

Documented in `kpv-conventions.md` §7 as a deliberate exception.

### Trade Package codes

Format: `[VillageCode]-[Stage]-[Trade]-[Sequence]`

Examples:
- `107-S1-V01` (Stage 1 Papamoa, Vertical Construction package 1)
- `104-S2A-E03` (Stage 2A Drury, Earthworks package 3)

Trade codes:
- `V` = Vertical Construction
- `C` = Civil
- `E` = Earthworks
- `R` = Roading
- `L` = Landscape
- `S` = Services (water, sewer, power)

Trade Package field is currently TEXT_NUMBER free-text per Phase 2 decision (review November 2026 to convert to picklist).

---

## 5. Picklist values

Picklist values appear in dropdowns and are used in cross-sheet formulas (matching), filters, and report grouping. Inconsistent values break formula matches silently.

### Universal rules
- Title Case throughout
- Identical option names across sheets where the meaning is identical (e.g. Sales Status options match exactly on Unit Register and Sales Register)
- No abbreviations unless universal (LTI, MTI, PSIF are OK because they're industry-standard)
- No trailing punctuation (no full stops, no question marks)
- Single space between words

### Locked picklist sets

#### Sales Status (used on Unit Register and Sales Register)

9 options, in display order:
1. Not Available
2. Available
3. Application
4. Conditional
5. Unconditional
6. Transfer
7. Settled
8. Occupied
9. Clubhouse

#### Construction Status

Standard 5-state picklist:
1. Not Started
2. Under Construction
3. Complete
4. On Hold
5. Cancelled

(Specific spelling and order to be confirmed against existing live picklist during Phase 2.5 execution; document any divergence found.)

#### Consent Status

5-state picklist (locked on Construction Register):
1. Not Submitted
2. Lodged
3. Under Review
4. Approved
5. Declined

#### Variation Approval Status (granular 9-state, set in Phase 2.5)

In workflow order:
1. Draft
2. Submitted
3. Pricing
4. Pending Approval
5. Approved
6. Rejected
7. Issued
8. Built
9. Closed

#### Variation Cost Category (new in Phase 2.5)

6 options:
1. Materials
2. Labour
3. Plant
4. Subcontractor
5. Design
6. Other

#### Variation Source (new in Phase 2.5)

7 options:
1. Client Request
2. Design Change
3. Site Conditions
4. Statutory / Consent
5. Error / Omission
6. Programme Acceleration
7. Other

#### RAG (used universally on Risk Register, Construction Programme, Civil Programme, Monthly RAG Log, etc.)

4 options with RYGG symbol set:
1. Red
2. Yellow (NOT "Amber" — use Yellow throughout)
3. Green
4. Gray

#### H and S Incident Type

6 options (locked after Phase 2.5 deduplication):
1. Near Miss - Minor
2. Near Miss - Serious (PSIF)
3. MTI
4. LTI
5. Observation
6. Other

### Pattern for status/state picklists

When a picklist represents progression through a workflow:
- Order options in workflow sequence (Draft before Submitted, Submitted before Approved, etc.)
- Use "Open" / "Closed" terminology consistently when applicable
- Terminal states (Closed, Cancelled, Rejected) at end of list

---

## 6. Form field labels

Forms expose column structure to non-Smartsheet users (suppliers, subcontractors, residents, contractors). Form labels can differ from internal column names to be more human-friendly.

### Pattern

```
Internal column: Cost Impact (NZD)
Form label: "Cost impact in NZ dollars (excluding GST)"

Internal column: Linked Building
Form label: "Which building does this variation affect?"

Internal column: Variation Source
Form label: "What caused this variation?"
```

### Rules
- Internal column name follows Section 1 conventions
- Form label can be a question or a friendly description
- If the form is for external users (suppliers via RFQ Quote Submission), prefer plain English over jargon
- If the form is internal, the form label can match the column name

### Form metadata to document

Each form should have a sheet-summary documentation row listing:
- Form URL
- Form purpose
- Required fields
- Auto-populated fields (URL parameters)
- Submitter audience (internal / external)
- Submission triggers (which automations fire on row added)

---

## 7. Automation and Power Automate flow names

Automations need clear names so the team can identify what they do without opening them. Same applies to Power Automate flows.

### Format

```
[Module] [Trigger] [Action]
```

### Examples
- `VAR Submitted Notify Matt`
- `VAR L2 Approved Notify Site`
- `VAR Pending > 7 Days Escalate`
- `HSE Serious Incident Notify SLT`
- `Contract Award Notify Julie`
- `RFQ New Quote Notify Procurement`
- `Risk High Score Notify Owner`

### Module abbreviations

| Module | Code |
|---|---|
| Variation | VAR |
| RFQ | RFQ |
| Contract | CON |
| Decision | DEC |
| Risk | RSK |
| H and S | HSE |
| Sales | SAL |
| Build / Construction | BLD |
| Civil | CIV |
| General | GEN |

### Automation register

Every automation and Power Automate flow goes in `Automation Register` (sheet — built in Phase 4 or 5). Columns:
- Automation Name (per format above)
- Module
- Source Sheet (or "Power Automate")
- Trigger
- Condition
- Action
- Owner
- Last Reviewed
- Risk if Broken
- Platform (Smartsheet / Power Automate)

---

## 8. SharePoint folder naming

Smartsheet and SharePoint structures should mirror each other where possible so users navigate the same way in both systems.

### Per-village SharePoint structure

```
[VillageCode] - [VillageName]/
├── 01 - Feasibility/
├── 02 - Design Civil and Construction/
├── 03 - Procurement/
└── 04 - Sales and Handover/
```

Matches per-village Smartsheet folder structure where applicable. Note SharePoint folders use slightly different organisation due to document lifecycle vs operational workflow split.

### File naming

Per `kpv-conventions.md`:

```
[VillageCode]-[Document Description]-[YYMMDD]-v[NN].[ext]
```

External documents add company name before date:
```
[VillageCode]-[Document Description]-[Company]-[YYMMDD]-v[NN].[ext]
```

Portfolio-level documents use `KPV` instead of village code.

Rules:
- Village code first (3-digit)
- Date YYMMDD (issue date)
- v01 two-digit only when revisions exist
- Hyphens between components, no spaces (spaces only inside description/company name)

---

## 9. Common mistakes to avoid

These are patterns we've already hit or seen in similar systems. Don't repeat them.

### Naming
- **Renaming columns after formulas/flows are built** — breaks them silently. Lock names early; rename only with full audit.
- **Using ampersands** — breaks Microsoft 365 URL handling (forms, SharePoint links). Use "and".
- **Mixed casing** — `Sales Status` vs `Sales status` vs `sales_status` — pick one (Title Case) and stick.
- **Synonyms across sheets** — `Supplier` vs `Counterparty` vs `Vendor` all meaning the same thing. Pick one term (Supplier — locked in Phase 2.5) and use it everywhere.

### IDs
- **Inconsistent digit padding** — `107-RFQ-1` vs `107-RFQ-01` vs `107-RFQ-001` all in the same sheet. 4 digits everywhere from Phase 2.5 forward.
- **Type codes not capitalised** — `107-var-0001` is wrong. Always UPPERCASE.

### Picklists
- **Adding options that are synonyms of existing ones** — `Approved` vs `Confirmed` vs `Signed Off`. Pick one and remove others.
- **Picklist values that drift across sheets** — Status `In Progress` on one sheet, `In progress` on another. Formula matches fail.
- **"Amber" vs "Yellow"** — mixing colours breaks dashboard tile rendering and confuses readers. Yellow throughout.

### Cross-sheet references
- **Inventing new reference names per village** — they should be standardised so a copy-paste of a formula between villages works (after re-pointing the ranges).
- **Using full sheet names** — `Construction Programme Is Unit` is verbose; `ConP Is Unit` is the locked pattern.
- **Including the (NZD) suffix in some references and not others** — match the source column name exactly.

---

## 10. Reference

This document supersedes naming guidance in any other reference file when there's conflict. Specifically:

- Overrides `templates.md` examples where column names differ
- Overrides `business-plan-guide.md` examples where column names differ
- Aligns with `kpv-conventions.md` §6 (naming conventions) — this document is the detailed expansion

Maintenance: update this file whenever a new convention is established. Tag the change with date and reason. This document is authoritative — if it says one thing and a sheet shows another, the sheet is wrong (not this document).

---

End of KPV Naming Conventions.
