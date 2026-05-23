# 107 Papamoa — Per-Building Architecture Migration

## Brief for Claude Code

**Owner:** Kyle Dickinson
**Village:** 107 Papamoa (trial village)
**Date created:** 2026-05-16
**Status:** Ready to execute

---

## Purpose

Migrate the 107 Papamoa data architecture from its current mixed-grain state (Budget per-building, Programme per-unit, Register per-unit, Unit Register per-unit) to a clean, consistent per-building + per-unit model joined by a Building Reference key.

This migration:
- Establishes a durable architecture pattern that will be replicated across all KPV villages (104 Drury next, then 105 Rototuna, 106 Waihi Beach, etc.)
- Consolidates the duplicate Construction Programme rows for duplex pairs into single per-building rows
- Creates a canonical Building Reference (`S1-B01` format) that joins financial, schedule, and unit-level data
- Converts the Sales Status column from free text to controlled picklist
- Removes drift risk by making Construction Status sourced from a single authoritative sheet (Construction Register)

**Critical:** this is a destructive migration with a complex Gantt consolidation step. Do not skip the backup/checkpoint structure.

---

## Decisions already locked (do not relitigate)

These were settled in conversation before this brief was written. Follow them exactly:

| Decision | Locked value |
|---|---|
| Building Reference format | `S1-B01`, `S2A-B01`, `S2B-B01`, ... `S5-B01` (stage + sequential building number) |
| Stage 2 sub-stages | Use sub-stages in Building Reference: `S2A-B01`, `S2B-B01`, `S2C-B01`, `S2D-B01`, `S2E-B01` |
| Stage 4 / Stage 4 and 5 | **Defer** — leave Budget as `Stage 4 and 5` for now, do not split |
| Pavilion grain | One Building Reference for the whole Pavilion: `PAV-B01` |
| Construction Programme grain | **Option Y** — consolidate to per-building (one row per building, not per unit) |
| Construction Status source of truth | **Construction Register** (per-unit). Programme's Construction Status column converts to a cross-sheet pull from Register |
| Sales Status | Stays on Unit Register, convert to controlled picklist with validation |
| Sequence numbering rule | Number buildings sequentially per stage in ascending order of the lowest unit number in the block |
| Programme consolidation rules | Start Date = earliest, End Date = latest, Duration = auto-recalc, % Complete = average rounded to nearest 5%, RAG = worst (most pessimistic), Notes/Latest = concatenate with separator |

---

## Sheets in scope

| Sheet | Sheet ID | Current grain | Target grain |
|---|---|---|---|
| `107 - Papamoa Budget` | `5631895457976196` | Per-building (already correct) | Per-building (no change to grain) |
| `107 - Construction Programme` | `5063906232848260` | Per-unit (114 unit rows + ~544 task/milestone rows = 658 total) | **Per-building** (consolidate to ~58 building rows + retained task rows) |
| `107 - Construction Register` | `2635310868418436` | Per-unit (128 rows) | Per-unit (keep grain, owns Construction Status truth) |
| `107 - Unit Register` | `5289542339743620` | Per-unit (~117 unit rows) | Per-unit (no change to grain) |

**Note on memory drift:** The `userMemories` for Kyle have stale sheet IDs. The correct current IDs are above. The Unit Register ID `5755996724324228` in memories is wrong — current ID is `5289542339743620`. The Civil and Construction Programme sheet `309322136741764` no longer exists — it was split into Construction Programme and Construction Register. Update memories at the end of this migration.

---

## Existing sheet structures (audit findings, 2026-05-16)

### 107 - Papamoa Budget (5631895457976196)

**14 columns** (just had 3 added before this migration started):

| Col | Title | Type | Notes |
|---|---|---|---|
| 0 | Line Item | TEXT_NUMBER | Primary; values like "102,104", "Stage 1 Buildings (x30)", etc. |
| 1 | Section | PICKLIST | Stage 1, Stage 2, Stage 3, Stage 4 and 5, Stage 5, Pre-Construction, Pavilion, Project Costs |
| 2 | Category | PICKLIST | Buildings, Civil, Landscaping, Supervision, Design, Technology, Council Fees, Feasibility, Pavilion, Project Management, Processing, Marketing |
| 3 | Base Price | TEXT_NUMBER | Currency |
| 4 | Contingency Amount | TEXT_NUMBER | Currency |
| 5 | Budget Approved | TEXT_NUMBER | Currency. Formula at leaves: `=[Base Price]@row + [Contingency Amount]@row` |
| 6 | Actual per Xero | TEXT_NUMBER | Currency |
| 7 | Budget Remaining | TEXT_NUMBER | Currency. **Column-level formula:** `=[Budget Approved]@row - [Actual per Xero]@row` |
| 8 | Estimated Still to Spend | TEXT_NUMBER | Currency. Cell-level (parent rows `=SUM(CHILDREN())`, leaves manual) |
| 9 | Expected Total Cost | TEXT_NUMBER | Currency. **Column-level:** `=[Actual per Xero]@row + [Estimated Still to Spend]@row` |
| 10 | Expected Total Variance | TEXT_NUMBER | Currency. **Column-level:** `=[Budget Approved]@row - [Expected Total Cost]@row` |
| 11 | Confirmed Permanent Difference | TEXT_NUMBER | Currency. **Column-level:** `=IF([Estimated Still to Spend]@row = 0, [Expected Total Variance]@row, 0)` |
| 12 | Units | TEXT_NUMBER | Plain text, e.g. "102, 104". Populated for Buildings rows only |
| 13 | Unit Count | TEXT_NUMBER | Plain integer. **Column-level:** `=IF(AND(Units@row <> "", Category@row = "Buildings"), LEN(Units@row) - LEN(SUBSTITUTE(Units@row, ",", "")) + 1, 0)` |
| 14 | Variance Status | PICKLIST (Symbols, RYG balls) | **Column-level:** `=IF([Expected Total Variance]@row > 0, "Green", IF([Expected Total Variance]@row = 0, "Yellow", "Red"))` |
| 15 | Last Updated | DATETIME | System column, MODIFIED_DATE |
| 16 | Notes | TEXT_NUMBER | |

**Total rows: 211.** Of those, 51 are leaf rows in Buildings category (Stage 1 through Stage 5 + Pavilion sub-components).

**Sheet Summary fields:** Built earlier — `Total Budget Approved`, `Total Actual per Xero`, `Total Budget Remaining`, `Total Estimated Still to Spend`, `Total Expected Total Cost`, `Total Expected Variance`, `Percent Spent`, `Percent Variance`, `Count Red Variance Status`, plus Stage 1 and Stage 2 versions of each.

### 107 - Construction Programme (5063906232848260)

**17 columns**, **658 rows**:

| Col | Title | Type | Notes |
|---|---|---|---|
| 0 | Task Name | TEXT_NUMBER | Primary |
| 1 | Is Unit | CHECKBOX | Flags unit rows vs task/milestone rows |
| 2 | Include in Report | CHECKBOX | |
| 3 | Stage | TEXT_NUMBER | Cross-sheet pull from Unit Register |
| 4 | Typology | TEXT_NUMBER | Cross-sheet pull from Unit Register (via VLOOKUP `{Unit Register Range}`) |
| 5 | Construction Status | PICKLIST | Currently editable. **Convert to cross-sheet pull from Construction Register on Unit Number** |
| 6 | Build Partner | PICKLIST | Currently only "Signature Homes" option |
| 7 | Building Consent Number | TEXT_NUMBER | Cross-sheet pull from Construction Register |
| 8 | Contract Price (incl GST) | TEXT_NUMBER | Cross-sheet pull from Construction Register |
| 9 | Variations (incl GST) | TEXT_NUMBER | Cross-sheet pull from Construction Register |
| 10 | % Complete | TEXT_NUMBER | Gantt column |
| 11 | RAG | PICKLIST (RYGG) | Red, Yellow, Green, Gray |
| 12 | Start Date | ABSTRACT_DATETIME | Gantt |
| 13 | End Date | ABSTRACT_DATETIME | Gantt |
| 14 | Duration | DURATION | Gantt |
| 15 | Predecessors | PREDECESSOR | Gantt |
| 16 | Notes/Latest | TEXT_NUMBER | |

**Dependency-enabled sheet** (has Gantt with predecessors).

**Row breakdown:**
- 114 rows have `Is Unit = true`
- ~544 rows are task/milestone/civil works rows (do NOT touch these — they stay)

**Stage values on unit rows:** `Stage 1`, `Stage 2A`, `Stage 2B`, `Stage 2C`, `Stage 2D`, `Stage 2E`, `Stage 3`, `Stage 4`, `Stage 5`. Note one orphan row with Task Name "402.0" missing Stage value — flag if found during migration.

### 107 - Construction Register (2635310868418436)

**20 columns**, **128 rows** (per unit + Stage header rows):

| Col | Title | Type | Notes |
|---|---|---|---|
| 0 | Unit Number | TEXT_NUMBER | Primary |
| 1 | Stage | TEXT_NUMBER | Cross-sheet pull from Unit Register |
| 2 | Typology | TEXT_NUMBER | |
| 3 | Consent Lodged | DATE | |
| 4 | Consent Approved | DATE | |
| 5 | Building Consent Number | TEXT_NUMBER | |
| 6 | Days to Approval | TEXT_NUMBER | Formula: `=IFERROR([Consent Approved]@row - [Consent Lodged]@row, "")` |
| 7 | Consent Status | PICKLIST | Not Yet Lodged, Ready to Lodge, Design Approval, Lodged, Approved |
| 8 | Construction Status | PICKLIST | **Source of truth for construction status going forward.** Not Started, Ready to Start, Civil Works, Under Construction, Practical Completion, Complete, On Hold, Future planning |
| 9 | Build Partner | PICKLIST | 17 options including Signature Homes BOP, Classic Builders, etc. |
| 10 | Contract Block | TEXT_NUMBER | Currently free-text values like "101-103", "102-104", "112", "113-115". **This column is the existing per-building grouping. Will be renamed to the new S-Bxx sequence.** |
| 11 | Contract Package | TEXT_NUMBER | KPV tender pack naming, e.g. "107-S1-V01" |
| 12 | Contract Price (incl GST) | TEXT_NUMBER | |
| 13 | Post Contract Variations (incl GST) | TEXT_NUMBER | |
| 14 | Construction Budget (incl GST) | TEXT_NUMBER | |
| 15 | Budget Remaining (incl GST) | TEXT_NUMBER | Formula: `=IF(COUNT(CHILDREN()) > 0, SUM(CHILDREN()), [Construction Budget (incl GST)]@row - [Contract Price (incl GST)]@row - [Post Contract Variations (incl GST)]@row)` |
| 16 | Budget Flag | PICKLIST (DIRECTIONS_3_WAY) | Up/Unchanged/Down |
| 17 | Latest Comment | TEXT_NUMBER | System |
| 18 | Notes | TEXT_NUMBER | |
| 19 | Include in Report | CHECKBOX | |

### 107 - Unit Register (5289542339743620)

**21 columns**, ~117 unit rows:

| Col | Title | Type | Notes |
|---|---|---|---|
| 0 | Unit Number | TEXT_NUMBER | Primary |
| 1 | Stage | PICKLIST | Stage 1, Stage 2, Stage 2A-E, Stage 3, Stage 4, Stage 5 |
| 2 | Typology | PICKLIST | 27 options (Berkeley, Eastwood, Harris, Jasmine, Juniper, Melrose, Monterey, Robertson, Stanaway, each with DG/SG variants) |
| 3 | Up Next | CHECKBOX | |
| 4 | Exterior Scheme | PICKLIST | Option A/B/C/D |
| 5 | Interior Scheme | PICKLIST | TBD - linked to Interior Scheme Register |
| 6 | F&F Scheme | PICKLIST | Signature Spec |
| 7 | Landscape Approved | CHECKBOX | |
| 8 | Design Approved | CHECKBOX | |
| 9 | Design Status (Internal Process) | PICKLIST | Not Started, Up Next, Underway, Awaiting Sales Approval, Awaiting CEO Approval, Design Approved |
| 10 | Contract Signed | CHECKBOX | |
| 11 | CEO Approval | CHECKBOX | |
| 12 | Consent Status | TEXT_NUMBER | Cross-sheet pull from Construction Register |
| 13 | Construction Status | TEXT_NUMBER | Cross-sheet pull from Construction Register |
| 14 | **Sales Status** | TEXT_NUMBER | **Currently free text. Convert to PICKLIST.** Need to audit current values first |
| 15 | Beds | TEXT_NUMBER | |
| 16 | Garage | TEXT_NUMBER | |
| 17 | Attachment Type | TEXT_NUMBER | |
| 18 | Floor Area (m²) | TEXT_NUMBER | |
| 19 | Latest Comment | TEXT_NUMBER | System |
| 20 | Notes | TEXT_NUMBER | |

---

## Execution plan

### Setup

1. Confirm API token is loaded and authenticates against `api.smartsheet.com` (global endpoint — not `api.smartsheet.au`).
2. Create a working directory: `plans/107-per-building-migration/`.
3. Create `migration_log.md` and append a timestamped entry at the start of each phase.
4. Create `mapping.json` to record all old-to-new value mappings (Building Reference assignments, row consolidations, etc.).
5. **Verify all four sheet IDs return 200 OK before proceeding.**

### Phase 0 — Backup strategy

**Decision:** rather than copying the Programme sheet (risk of broken predecessor references in the clone), use the **build-alongside** pattern:

- The existing Programme sheet **stays untouched** until the very end of the migration. It serves as the live backup.
- A new sheet `107 - Construction Programme (per building)` is built alongside it.
- Once verified, cross-sheet references are repointed and the old Programme is renamed to `107 - Construction Programme (ARCHIVE - per unit)` and moved to an Archive folder. Not deleted.

This way the original is always recoverable, no race conditions.

**Step 0.1:** Confirm the workspace folder layout. Find or create:
- `107 - Papamoa > 02 - Civil and Construction > Archive` (folder for old per-unit Programme)
  - Use `browse_folder` on the parent `02 - Civil and Construction` folder. If no `Archive` subfolder exists, create one.

**Checkpoint 0:** Log all current sheet IDs and the discovered Archive folder ID to `mapping.json`. Confirm with user before proceeding.

---

### Phase 1 — Sequence numbering: design and Budget update

**Step 1.1: Generate the sequence mapping**

Read every Buildings row from the Budget sheet (`Category = "Buildings"`, `Line Item not in ("Stage 1 Buildings (x30)", "Stage 2 Buildings (x34)", "Stage 3 Buildings (x32)", "Stage 4 Buildings (x32)", "Stage 5 Buildings", "Pavilion")`).

For each, parse the lowest unit number from the `Units` column or `Line Item`. Group by Section (Stage 1, Stage 2, Stage 3, Stage 4 and 5, Stage 5, Pavilion).

Then assign Building Reference values:

- **Stage 1:** sort by lowest unit number ascending, number `S1-B01` through `S1-B10`
- **Stage 2:** look up each building's sub-stage from the Construction Register `Stage` column (Stage 2A/2B/2C/2D/2E). Group by sub-stage. Number within each sub-stage: `S2A-B01, S2A-B02, S2B-B01, ...`
- **Stage 3:** number `S3-B01` through `S3-Bxx`
- **Stage 4 and 5 (on Budget):** all rows assigned to this section. Cross-reference Programme/Register `Stage` to determine which are actually Stage 4 vs Stage 5. Assign `S4-B01, S4-B02, ..., S5-B01, S5-B02, ...` accordingly.
- **Stage 5 (on Budget):** number `S5-Bxx` continuing from where Stage 4 and 5's Stage 5 buildings ended (avoid collisions)
- **Pavilion:** single Building Reference = `PAV-B01` applied to the "Pavilion" parent row only (the sub-components like Country Club, Workshop, Pool stay as child rows under PAV-B01 conceptually, but only the parent gets the BR)

**Important Stage 4/5 split clarification:** The Budget has "Stage 4 and 5" as a single Section but the Programme/Register split them. The Budget rows under "Stage 4 and 5" cover units 178-198 and 501-504, plus the slash-notated 180/1-5 and 182/1-5 units. The Budget rows under "Stage 5" cover 601-805. Use Programme/Register Stage values to determine the true Stage for sequencing.

Write the proposed mapping to `mapping.json` in this structure:

```json
{
  "building_reference_mapping": [
    {
      "budget_row_id": 1110033150967684,
      "line_item": "102,104",
      "units": "102, 104",
      "budget_section": "Stage 1",
      "register_stage": "Stage 1",
      "building_reference": "S1-B02",
      "lowest_unit": 102
    }
  ]
}
```

**Checkpoint 1.1:** Print the full mapping table to the log and **stop**. User must review and confirm the sequence assignments before any sheet writes happen.

**Step 1.2: Add `Building Reference` column to Budget sheet**

API: `add_columns`
- Sheet: `5631895457976196` (Budget)
- Title: `Building Reference`
- Type: `TEXT_NUMBER`
- Index: 12 (insert before `Units`)
- Width: 100
- Formula: none (manual values)

**Step 1.3: Populate Building Reference values on Budget**

API: `update_rows` (single batched call, max 500 rows per call)
- For each row in the mapping, write the Building Reference value to the new column

**Checkpoint 1.3:** Verify each Building Reference appears correctly on the Budget sheet. Re-fetch a sample of rows and confirm.

---

### Phase 2a — Programme dependency audit (read-only)

Before any destructive changes, audit what depends on the Programme sheet.

**Step 2a.1:** Pull all 658 rows from Programme. For each row, record:
- Row ID
- Task Name
- Is Unit value
- Parent row ID (if child)
- Predecessor value (if any)
- Children count

**Step 2a.2:** For each unit row, identify:
- Its predecessor (does it point to another unit row that will also be consolidated?)
- Its dependents (other rows pointing TO it as their predecessor)
- Its children (sub-tasks if any)

**Step 2a.3:** Identify cross-sheet references that point TO the Programme. Cross-sheet references can only be inspected from the consumer side. Check:
- Construction Register columns
- Unit Register columns
- Budget columns
- Any chart source sheets in the workspace
- Any reports

Cross-sheet references look like `{Some Named Range}` in formulas. Look for ones whose definition points to Programme sheet ID `5063906232848260`.

**Step 2a.4:** Generate an audit report `phase_2a_audit.md` with:
- Total unit rows: should be 114
- Unit rows with predecessors: count and list
- Unit rows that ARE predecessors to other rows: count and list
- Unit rows with children: count and list (should be 0 or low)
- Orphan rows (the "402.0" one and any others)
- Cross-sheet consumers of Programme

**Checkpoint 2a:** Stop and present audit to user. User must confirm migration risk before proceeding.

---

### Phase 2b — Build new Construction Programme alongside

**Decision:** Build the new per-building Programme as a **fresh sheet**. Easier to verify, doesn't risk breaking the live Programme.

**Step 2b.1: Create new sheet** `107 - Construction Programme (per building)` via `create_sheet_in_folder` in the `02 - Civil and Construction` folder.

Columns (mirror the existing Programme but with Building Reference as primary join):

| Index | Title | Type | Notes |
|---|---|---|---|
| 0 | Building Reference | TEXT_NUMBER | Primary (e.g. `S1-B01`) |
| 1 | Building Name | TEXT_NUMBER | Human label (e.g. "Building 102-104") |
| 2 | Stage | PICKLIST | Stage 1, Stage 2A, 2B, 2C, 2D, 2E, Stage 3, Stage 4, Stage 5, Pavilion |
| 3 | Units | TEXT_NUMBER | List of unit numbers (e.g. "102, 104") |
| 4 | Unit Count | TEXT_NUMBER | Plain integer |
| 5 | Typology | TEXT_NUMBER | (May contain multiple typologies if duplex pairs differ) |
| 6 | Construction Status | TEXT_NUMBER | **Cross-sheet pull from Construction Register** — set up in Phase 4 |
| 7 | Build Partner | PICKLIST | All 17 partner options from Register |
| 8 | Building Consent Numbers | TEXT_NUMBER | Concatenated if multiple |
| 9 | Contract Package | TEXT_NUMBER | KPV tender pack ref |
| 10 | Contract Price (incl GST) | TEXT_NUMBER | Sum of unit-level contract prices for buildings in this row |
| 11 | Variations (incl GST) | TEXT_NUMBER | Sum |
| 12 | % Complete | TEXT_NUMBER | Gantt column; average of consolidated unit values, rounded to nearest 5% |
| 13 | RAG | PICKLIST (RYGG) | Worst (most pessimistic) of consolidated unit values |
| 14 | Start Date | ABSTRACT_DATETIME | Earliest of consolidated unit values |
| 15 | End Date | ABSTRACT_DATETIME | Latest of consolidated unit values |
| 16 | Duration | DURATION | Auto-calc from Start/End |
| 17 | Predecessors | PREDECESSOR | Rebuild at building level |
| 18 | Notes/Latest | TEXT_NUMBER | Concatenated from consolidated unit values with `; ` separator |
| 19 | Budget Approved | TEXT_NUMBER | **Cross-sheet pull from Budget on Building Reference** — set up in Phase 4 |
| 20 | Expected Total Cost | TEXT_NUMBER | **Cross-sheet pull from Budget on Building Reference** — set up in Phase 4 |
| 21 | Expected Variance | TEXT_NUMBER | **Cross-sheet pull from Budget on Building Reference** — set up in Phase 4 |

**Important Smartsheet limitation:** Gantt-enabled sheets cannot be fully configured via API. The `dependenciesEnabled` flag and the DURATION/PREDECESSOR column types may need manual UI setup after the API creates the bare sheet.

**Workaround:** Create the sheet via API with all non-Gantt columns. Then **stop and ask user to:**
1. Open the new sheet in the UI
2. Right-click any column header → Edit Project Settings → Enable Dependencies
3. Then resume the script

**Checkpoint 2b.1:** Stop. User enables Dependencies in UI. Confirm before proceeding.

**Step 2b.2: Populate the new Programme**

For each Building Reference (from Phase 1 mapping):
1. Find the corresponding unit rows in the OLD Programme (by Task Name = unit number, where unit number is in the Building's Units list)
2. Aggregate per consolidation rules:
   - Start Date = MIN of unit rows' Start Date values
   - End Date = MAX of unit rows' End Date values
   - % Complete = AVG of unit rows' % Complete values, rounded to nearest 5%
   - RAG = worst (Red > Yellow > Green > Gray)
   - Notes/Latest = concatenate all unit rows' Notes with `; ` separator
   - Build Partner = MODE of unit rows (most common); if tie, use first
   - Building Consent Numbers = concatenate distinct values
   - Contract Price = SUM of unit-level values
   - Variations = SUM of unit-level values
   - Typology = concatenate distinct values
3. Add the row to the new sheet via `add_rows`

**Step 2b.3:** Rebuild predecessor relationships at building level

This is the trickiest part. Logic:
- For each Building Reference, find the predecessor(s) of its constituent unit rows in the old Programme
- Map those predecessor unit IDs back to their Building References
- If multiple unit predecessors map to the same Building predecessor, deduplicate
- If a unit had a predecessor that was a non-unit task row (civil works, milestones), that link is severed in the new building-only Programme — flag this for user review

Write predecessors to the new Programme. Note that Smartsheet predecessors use row positional references like "5FS" (finish-to-start with row 5). Need to use the new row IDs / row numbers from the new Programme sheet.

**Step 2b.4:** Pull civil works / milestone rows over to the new sheet

The old Programme has ~544 non-unit task rows (civil works, milestones, sub-tasks). These are still needed in the new Programme. Two options:
- **Option A:** Copy them verbatim to the new sheet
- **Option B:** Reference them from the old sheet (not really possible — would need rebuilding anyway)

**Recommend Option A.** Copy task rows preserving hierarchy. Skip the unit rows since those are consolidated.

**Checkpoint 2b.4:** Verify new Programme has:
- ~58 building rows
- ~544 task/milestone rows preserved
- Total ~602 rows (down from 658)
- Gantt structure intact
- Predecessor relationships working

User reviews before Phase 3.

---

### Phase 2c — Update Construction Register Contract Block values

Now that Building References are assigned and the new Programme exists, update the Construction Register's `Contract Block` column to use the new sequence values.

**Step 2c.1:** Build mapping: old Contract Block value → new Building Reference. For each unit row in the Register, look up its Contract Block (e.g. "102-104"), find which Building Reference covers those units (from Phase 1 mapping), and update.

Example: row with Contract Block `102-104` → update to `S1-B02`.

**Step 2c.2:** Batched `update_rows` call to write new values.

**Checkpoint 2c:** Verify Contract Block values match between Budget and Register. Each unit row in Register should have a Contract Block matching one of the Building References on Budget.

---

### Phase 3 — Sales Status to picklist

**Step 3.1: Audit current Sales Status values**

Pull all Unit Register rows, extract distinct Sales Status values. Generate report showing:
- Each distinct value
- Count of rows with that value
- Whether the value matches a "standard" sales status name

**Step 3.2:** Propose picklist values based on what's in the data. Likely set:
- Not For Sale
- For Sale
- Reserved
- Contract Signed
- Settled
- Resold

Build a value-mapping table: each existing value → which picklist value should replace it (or flag for manual review if ambiguous).

**Checkpoint 3.2:** User reviews proposed picklist and mapping. Confirm before changes.

**Step 3.3: Clean up existing values to match picklist**

API: `update_rows` with the mapped values.

**Step 3.4: Convert column to picklist**

API: `update_column` on column ID `8282836699484036`:
- Set `type` to `PICKLIST`
- Set `options` to the new picklist values
- Set `validation` to `true`

**Note:** Smartsheet may reject changing column type if any cell still holds a non-conforming value. The Step 3.3 cleanup must complete first.

**Checkpoint 3.4:** Verify column behaves as picklist in UI. Test entering a non-standard value should be rejected.

---

### Phase 4 — Cross-sheet references rebuild

This is mostly UI work; cross-sheet named ranges cannot be created via API.

**Step 4.1: Document the references needed**

Generate a printable checklist `phase_4_xsheet_refs.md` for the user to execute in the UI:

#### On the new Construction Programme (per building):

For each new cross-sheet column (`Construction Status`, `Budget Approved`, `Expected Total Cost`, `Expected Variance`):
1. Right-click column header → Edit Column Formula
2. Click `References Other Sheets`
3. Pick the source sheet (Construction Register for Construction Status; Budget for the three financial pulls)
4. Select range and name it
5. Save formula

Specific formulas:
- `Construction Status`:
  ```
  =IFERROR(INDEX({Register Construction Status}, MATCH([Building Reference]@row, {Register Contract Block}, 0)), "")
  ```
  Named ranges to create: `Register Construction Status` → Construction Register column "Construction Status"; `Register Contract Block` → Construction Register column "Contract Block"

- `Budget Approved`:
  ```
  =IFERROR(INDEX({Budget Budget Approved}, MATCH([Building Reference]@row, {Budget Building Reference}, 0)), "")
  ```
  Named ranges: `Budget Budget Approved` → Budget column "Budget Approved"; `Budget Building Reference` → Budget column "Building Reference"

- `Expected Total Cost`: similar pattern, change first named range
- `Expected Variance`: similar pattern

**Important caveat:** The cross-sheet INDEX/MATCH for Construction Status will return the value from ONE unit in the building (the first matching). If duplex units have different statuses (rare but possible), only one value shows. To handle this, an additional helper column on the Programme could compute MAX or worst-case status across all units in the building. Leave that as Phase 5 enhancement if needed.

#### On the existing Construction Programme (OLD, will be archived):

- Change `Construction Status` column from PICKLIST direct entry to cross-sheet pull from Register (so values stop drifting during the cutover):
  ```
  =IFERROR(INDEX({Register Construction Status}, MATCH([Task Name]@row, {Register Unit Number}, 0)), "")
  ```

**Step 4.2:** User executes the UI steps. Script provides exact instructions and pauses.

**Checkpoint 4.2:** Verify cross-sheet pulls return correct values on the new Programme.

---

### Phase 5 — Cutover and archive

**Step 5.1:** Update any consumers of the old Programme to point at the new Programme

Audit results from Phase 2a will list these. Likely zero or very few since most consumers go to Register, not Programme.

**Step 5.2:** Rename old Programme

- Old name: `107 - Construction Programme`
- New name: `107 - Construction Programme (ARCHIVE - per unit)`

API does not support sheet rename — **manual UI step** for user.

**Step 5.3:** Move old Programme to Archive folder

API does not support move — **manual UI step** for user.

**Step 5.4:** Rename new Programme

- Old name: `107 - Construction Programme (per building)`
- New name: `107 - Construction Programme`

This becomes the canonical Programme. Manual UI step.

**Step 5.5:** Update Budget report and dashboard

The Budget report (`RPT - 107 Budget vs Actual` or similar) should include `Building Reference` as a column. Manual UI update.

The Budget dashboard widgets do not need changes (they read Sheet Summary fields).

**Step 5.6:** Update Kyle's `userMemories`

Use the `memory_user_edits` tool to:
- Update Unit Register sheet ID to `5289542339743620`
- Note that Civil and Construction Programme split into Construction Programme + Construction Register
- Note Building Reference architecture is now standard for KPV

---

## Risks and rollback

### Phase 0-1 (Mapping, Budget column add)
- **Risk:** wrong sequence assignment
- **Rollback:** delete Building Reference column from Budget; re-run mapping with corrected logic

### Phase 2a (Audit)
- **Risk:** none, read-only
- **Rollback:** none needed

### Phase 2b (Build new Programme)
- **Risk:** consolidation math wrong, predecessors mis-wired
- **Rollback:** delete the new sheet; old Programme is untouched
- **Mitigation:** verify against a sample of buildings manually before declaring done

### Phase 2c (Register Contract Block update)
- **Risk:** breaks existing Register filters/views that reference old Contract Block values like "102-104"
- **Rollback:** restore old values from `mapping.json` (always write old values to mapping before updating)
- **Mitigation:** keep both old and new values in `mapping.json`; consider adding a "Contract Block (Legacy)" column on Register to preserve old values for reference

### Phase 3 (Sales Status picklist)
- **Risk:** existing free-text values lost during cleanup
- **Rollback:** restore from `mapping.json`
- **Mitigation:** capture original values in mapping before any updates

### Phase 4 (Cross-sheet references)
- **Risk:** named ranges defined incorrectly, formulas return blanks
- **Rollback:** delete the formula, recreate the named range
- **Mitigation:** test each formula against a single known-good row before applying

### Phase 5 (Cutover)
- **Risk:** consumers still pointing at old Programme
- **Rollback:** rename old Programme back to canonical name, rename new one back to alt
- **Mitigation:** Phase 2a audit identifies consumers; check each manually

---

## Recovery: what if it all goes wrong

The OLD Construction Programme sheet is never deleted, never modified destructively. If everything fails:
1. Delete the new Programme sheet
2. Roll back the Register `Contract Block` updates from `mapping.json`
3. Roll back the Budget `Building Reference` column (delete it)
4. Roll back the Unit Register `Sales Status` updates from `mapping.json`
5. Convert Sales Status column type back to TEXT_NUMBER

Original state restored. No data loss.

---

## Final checklist for user

When the script finishes, verify:

- [ ] Budget sheet has `Building Reference` column populated for all Buildings rows
- [ ] Construction Register `Contract Block` values match Building References on Budget
- [ ] New `107 - Construction Programme` (per-building) exists with ~58 building rows
- [ ] Cross-sheet pulls work: Programme's Construction Status, Budget Approved, etc., return values
- [ ] Unit Register Sales Status is now a controlled picklist
- [ ] Old Programme renamed and moved to Archive folder
- [ ] Budget report includes Building Reference column
- [ ] `userMemories` updated with new sheet IDs
- [ ] No broken cross-sheet references anywhere
- [ ] No `#REF` errors in any sheet

---

## Notes for the next village (104 Drury)

When this pattern is replicated to 104 Drury:

1. Building Reference format: same — `S1-B01`, `S2-B01`, etc., or with sub-stages if 104 has them
2. Budget sheet: same column structure including Building Reference
3. Construction Programme: build per-building from the start (don't repeat the consolidation pain)
4. Construction Register: same per-unit structure with Contract Block = Building Reference
5. Unit Register: same per-unit with controlled Sales Status picklist

This migration becomes the template for every village.

---

## Style conventions (KPV)

- NZ English throughout
- Use hyphens, not em dashes
- Use "and", not "&" (so "Stage 4 and 5", not "Stage 4 & 5")
- Sheet names use the convention `[VillageCode] - [Sheet Name]`
- File names follow `[VillageCode]-[Document Description]-[YYMMDD]-v[NN].[ext]`

---

End of brief.
