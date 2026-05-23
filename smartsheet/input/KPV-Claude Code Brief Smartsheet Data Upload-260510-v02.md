# Claude Code Brief - Smartsheet Data Upload

**Owner:** Kyle Dickinson, Development Lead, Karaka Pines Villages (KPV)
**Purpose:** Reusable instruction for loading Excel or CSV source data into existing Smartsheet sheets via the Smartsheet API
**Version:** 2.0 - 10 May 2026

---

## 1. Scope and intent

This brief governs every data upload from a source file (Excel or CSV) into an existing Smartsheet target sheet. It applies across all KPV village workspaces and all sheet types (Unit Register, Civil and Construction Programme, Resource Consent Register, Variation Log, RFQ and Quote Register, Risk Register, Health and Safety Register, etc).

The user (Kyle) will provide:
- A source file (xlsx or csv) at a known path
- A target sheet, identified by sheet ID **or** by sheet name (e.g. "107 - Unit Register")
- Any task-specific overrides (e.g. "skip column X", "load only Stage 3 rows")

Claude Code will execute the upload following the rules in this brief.

**Sheet IDs change.** New sheets are created and old ones deleted regularly. Workspace IDs and folder IDs also change. Claude Code must never trust a sheet ID from memory, prior session, or hard-coded reference. Every session begins with a fresh self-audit.

---

## 2. Core principles

These are non-negotiable.

1. **Self-audit every session.** At the start of every session, before any data work, Claude Code walks the workspace structure and builds a current inventory of workspaces, folders, sheets, reports and dashboards. The inventory built in this session is the only source of truth. No memory, no caching across sessions, no trusting earlier briefs.

2. **Smartsheet target wins.** The target sheet's column layout, types, picklists, formulas, and formatting take precedence. The source file is data only - structural decisions on the target sheet are not changed by what the source file contains, unless Kyle explicitly directs otherwise.

3. **Never overwrite formula-driven columns.** Any column on the target sheet that has a column-level formula (typically VLOOKUPs that pull from the Unit Register or another sheet) must not receive values from the source file. The formula computes the value live - sending a value would either be silently ignored or break the column. Identify these by reading the column metadata before loading.

4. **Hierarchy must be preserved.** Smartsheet sheets are hierarchical. Parent rows roll up children for sums, dates, RAG status, and Gantt rollups. The source file's hierarchy (whether expressed via Excel outline level, indentation, or naming pattern) must be reconstructed in Smartsheet using `parentId`.

5. **No em dashes anywhere.** KPV convention: hyphens only. Filter source data, sheet names, row values, file names. If the source has em dashes, replace with hyphens before loading.

6. **Validate before loading.** Always inspect both the source file and the target sheet before writing rows. Report the plan to the user, get confirmation, then execute.

7. **Batches small enough to avoid rate limits.** Smartsheet API caps at 500 rows per call but practical limit is lower due to payload size. Use 50-100 rows per batch unless the row payload is very small (then up to 200).

8. **Report progress in plain numbers.** "Batch 3 of 12 - 240 of 690 rows loaded" not vague status. Stop and ask if anything errors.

---

## 3. The self-audit (run this first, every session)

Before doing anything else, run the self-audit. This builds a fresh inventory of every workspace, folder, sheet, report and dashboard the user can access. The inventory generated here is what Claude Code uses to validate Kyle's input and locate the target sheet.

### 3.1 Audit steps

1. **Discover workspaces.** Use `search_smartsheet` with `scopes=["workspaceNames"]` to find every KPV-related workspace. Search terms to run, in order:
   - `Overview` (catches `000 - Overview` and the portfolio overview workspace)
   - `Drury` (catches `104 - Drury - KLE`)
   - `Rototuna` (catches `105 - Rototuna`)
   - `Waihi` (catches `106 - Waihi Beach`)
   - `Papamoa` (catches `107 - Papamoa`)
   - `Template` (catches `XXX - Village Template`)
   - `Karaka` (catch-all for any new KPV-related workspace)

   Capture each workspace's `asset_id` and exact name.

2. **Walk every workspace.** For each workspace ID found, call `browse_workspace`. This returns the workspace's top-level children (folders and any sheets at workspace root).

3. **Walk every folder.** For each folder found, call `browse_folder`. This returns sheets, reports, dashboards, and nested folders inside that folder.

4. **Recurse if needed.** If a folder contains nested folders, walk those too. KPV's standard structure is one level deep (workspace → folder → assets) but the audit must handle deeper nesting if it exists.

5. **Identify asset types correctly.** The MCP tools return `resource_type: sheet` for everything. The actual type is in the URL:
   - `/sheets/...` = Sheet
   - `/reports/...` = Report
   - `/dashboards/...` = Dashboard
   - `/folders/...` = Folder

6. **Build the inventory.** Hold the discovered inventory in memory as a structured object: every workspace with its folders, every folder with its assets, every asset with its ID, name, type, URL, and parent path.

### 3.2 Audit output

Output a brief summary to Kyle at the end of the audit. Format:

```
Self-audit complete - 10 May 2026 14:32
- 6 workspaces found: 000 - Overview, 104 - Drury - KLE, 105 - Rototuna, 106 - Waihi Beach, 107 - Papamoa, XXX - Village Template
- 9 folders, 27 sheets, 38 reports, 1 dashboard
- Anomalies flagged: [list any below]
```

### 3.3 Anomalies to flag during audit

If any of these are found, list them in the audit output but do not block - Kyle decides what to action:

- **Naming drift.** Reports or sheets with a village code prefix that doesn't match their parent workspace (e.g. a report called "104 - Sale Variance Watch" living inside `105 - Rototuna`).
- **"Untitled" assets.** Any sheet or report named "Untitled report", "Untitled sheet" etc.
- **Orphan summary sheets.** Sheets named "Design Status Summary" or similar - these were earlier mistakes and should generally be deleted in favour of the matching report.
- **Missing standard assets.** A village workspace that doesn't have the expected sheets (Unit Register, Construction Programme, Civil Programme, Resource Consent Register, RFQ and Quote Register, Variation Log).
- **Duplicate names.** Two sheets with the same name in the same folder.

### 3.4 Inventory persistence (optional)

If Kyle has previously instructed Claude Code to maintain an inventory file in the working directory (default name: `kpv-smartsheet-inventory.json`), write the fresh inventory there at the end of the audit, overwriting the previous version. Always overwrite - the file is a snapshot, not a history.

If no such instruction exists, hold the inventory in memory only.

---

## 4. Resolving the target sheet

Kyle will name the target sheet in one of three ways. Resolve in this order:

1. **Numeric sheet ID provided.** Validate it against the audit inventory. If the ID exists and is a sheet (not a report or dashboard), confirm the sheet name with Kyle ("Target: `107 - Unit Register` in workspace `107 - Papamoa` - correct?"). If the ID doesn't exist in the inventory, stop and tell Kyle - the sheet was likely renamed or deleted.

2. **Sheet name provided.** Look up the name in the audit inventory. If unique match, confirm with Kyle. If multiple matches across workspaces, list them all and ask Kyle to pick. If no match, stop.

3. **Ambiguous reference** (e.g. "the Construction Programme"). Treat as a sheet name lookup - if multiple villages have one, list them and ask Kyle which.

Never proceed with a target sheet ID that hasn't been validated against the current audit inventory.

---

## 5. Inputs Kyle will provide

For each upload task Kyle will give:

- **Source file path** - e.g. `/path/to/107 - Civil and Construction Programme.xlsx`
- **Target sheet** - by ID, by name, or by description (Section 4 covers resolution)
- **Task-specific notes** (optional) - any overrides, exclusions, or special handling

If anything is missing or ambiguous, ask before starting. Do not guess.

---

## 6. Workflow - the seven steps

Execute in this exact order, after the self-audit and target resolution are complete.

### Step 1 - Inspect the target sheet

Use `get_columns` on the target sheet ID. Capture for every column:

- Column ID
- Title
- Type (TEXT_NUMBER, PICKLIST, DATE, CHECKBOX, ABSTRACT_DATETIME, DURATION, PREDECESSOR, etc)
- Whether it has a column-level formula (`formula` field non-null) - **flag these as DO NOT WRITE**
- Picklist options (for PICKLIST and MULTI_PICKLIST columns)
- Validation flag
- Tags (especially GANTT_* tags)
- Symbol (e.g. RYGG for RAG columns)
- Format string

Also capture sheet-level facts:
- Total existing row count (use `get_sheet_summary` with no filters)
- Whether dependencies and Gantt are enabled
- Current parent row structure if any

### Step 2 - Inspect the source file

Read the source file (xlsx via openpyxl, csv via Python's csv module). Capture:

- Sheet/tab names if xlsx (work on the right one - usually the first, but confirm)
- Header row position (usually row 1, but confirm)
- All source column headers
- Total row count
- For xlsx: outline level (`row.outline_level`) for each row - this drives hierarchy
- Sample data from first 5 rows of each detected hierarchy level
- Any merged cells (these are bad for data extraction - flag and stop)

### Step 3 - Map source columns to target columns

Build a mapping table:

| Source column | Target column title | Target column ID | Target type | Action |
|---|---|---|---|---|
| Task Name | Task Name | 6646557238923140 | TEXT_NUMBER | Load |
| Stage | Stage | 102264030400388 | PICKLIST | Load (validate against picklist) |
| Typology | Typology | 4605863657770884 | TEXT_NUMBER | **SKIP - column has VLOOKUP formula** |
| ... | ... | ... | ... | ... |

Mapping rules:

- **Exact name match (case-sensitive)** = automatic map
- **Close name match** (whitespace, hyphen, ampersand differences) = automatic map, log for confirmation
- **No match** = ignore source column, log for Kyle's awareness
- **Target column not in source** = leave blank on the new rows (the formula or default will fill it, or it stays blank)
- **Target column has a column-level formula** = ALWAYS skip even if source has data for it

Output the mapping table to Kyle before loading and ask "Proceed?"

### Step 4 - Validate source data against target rules

Before any write, check every source row for:

- **PICKLIST values** - source value must exactly match an existing target picklist option. If not, either:
  - Add the option to the picklist (only if Kyle pre-approves picklist expansion for this task), or
  - Flag the row and either skip or set to blank
- **DATE columns** - source must be parseable as date. Excel serial dates from openpyxl come through as datetime; CSV dates need explicit parsing
- **CHECKBOX columns** - source `1`, `true`, `TRUE`, `yes`, `Y`, ✓ map to `true`. Anything else maps to `false`
- **TEXT_NUMBER columns receiving numbers** - send as numeric (not string) to preserve number formatting
- **Em dashes** - replace `—` and `–` with `-` in any text cell before sending
- **Ampersands in text where KPV convention says "and"** - flag but do not auto-replace, ask Kyle

### Step 5 - Reconstruct hierarchy

The source's hierarchy must be rebuilt in Smartsheet. Detection logic (try in order):

1. **xlsx outline_level** - if the source has Excel outline grouping, use `row.outline_level` (0 = top, 1 = child, 2 = grandchild, etc). Most reliable.
2. **Indentation in the primary column** - some files indent text with leading spaces or tabs to imply hierarchy. Strip and use as level signal.
3. **Naming pattern** - if column 1 has values like "Civil Works" → "Stage 1" → "Site clearance" → "Unit 101", and these are at different levels, infer from a known pattern provided by Kyle for that sheet type.
4. **Explicit "Parent" or "Level" column in the source** - if present, use directly.

Build the hierarchy by:

1. Adding all level-0 (top-level) parent rows first via `add_rows` with `toBottom: true`. Capture returned row IDs.
2. For each level-0 parent, add its level-1 children using `parentId: <captured ID>` and `toBottom: true`.
3. Recurse for deeper levels.
4. **One API call per parent** when adding children to that parent (the API requires all rows in a single call to share the same parent).
5. Track all created row IDs in a Python dict keyed by source row index, so cross-references (e.g. predecessors) can resolve.

### Step 6 - Load the data

Loading rules:

- Batch size: 50-100 rows per `add_rows` call. For very wide rows (15+ columns of data) drop to 30-50.
- Always use `toBottom: true` (or `parentId` + `toBottom: true` for children) so insertion order is deterministic.
- Never set values on formula-driven columns (Step 3 flagged these as SKIP).
- For PICKLIST cells, always use the exact picklist value string.
- For DATE cells, send ISO 8601 format `YYYY-MM-DD`.
- For DURATION cells, send Smartsheet duration format e.g. `5d`, `2w`, `3h`.
- For PREDECESSOR cells, the format is `<row_number>FS` for finish-to-start, but the row_number must reference rows already in the sheet. If predecessors exist in source, load all rows first WITHOUT predecessors, then do an `update_rows` second pass to wire predecessors using captured row IDs.
- Report progress every 5 batches: "Loaded 250 of 690 rows (36%)".

### Step 7 - Verify and report

After loading:

1. Run `get_sheet_summary` on the target sheet, no filters, capturing total row count.
2. Compare against expected count (source rows + parents added + any pre-existing rows that were preserved).
3. Spot-check 3 random rows: read a row from source, find its corresponding row in target via primary column match, confirm key fields match.
4. Report a final summary:
   - Rows loaded
   - Rows skipped and why
   - Picklist values added (if any)
   - Formula columns left untouched (list)
   - Any warnings or anomalies

---

## 7. Edge cases and how to handle them

| Situation | Action |
|---|---|
| Source file has a column the target doesn't have | Ignore the column, log it. Do not auto-create columns on the target. |
| Target has a column the source doesn't have | Leave blank on new rows. The formula or default fills it, or it stays blank. |
| Source column has more picklist values than target | Stop and ask Kyle whether to add to picklist or filter rows. |
| Target sheet already has data | Default behaviour: append. If Kyle wants a clean wipe, he must say so explicitly. |
| Source has merged cells | Stop and ask Kyle to fix the source - merged cells corrupt extraction. |
| Source has formulas | Read the computed value, not the formula. openpyxl `data_only=True` gives this. |
| Source date is a weird format | Try ISO, NZ (DD/MM/YYYY), US (MM/DD/YYYY) in that order. If still ambiguous, ask. |
| Hierarchy can't be reliably inferred | Stop. Ask Kyle to either flatten the source or provide an explicit hierarchy column. |
| API call fails partway through a batch | Smartsheet returns partial success info. Log which row IDs succeeded, retry only the failed rows. Do not retry the whole batch blindly. |
| Rate limit hit (HTTP 429) | Back off 30 seconds, then resume. Smartsheet's rate limit window is per-minute. |
| A row's parent ID is missing because the parent failed to add | Stop loading children for that branch. Surface to Kyle. |
| Sheet ID Kyle gave doesn't exist in the audit | Stop. Tell Kyle the ID isn't found - it was likely renamed or deleted. Ask him to provide the current name or re-confirm. |
| Audit finds two sheets with the same name | Surface both with their workspace and folder paths. Ask Kyle which is the target. |

---

## 8. KPV-specific naming and conventions

| Convention | Rule |
|---|---|
| Hyphens only | No em dashes (—) or en dashes (–) anywhere. Replace with hyphen (-). |
| "and" not "&" | KPV uses "and". Source files using "&" are flagged for confirmation, not auto-replaced. |
| Stage naming | Always "Stage 1", "Stage 2A" (no leading zero, capital S). Case must match exactly across sheets or VLOOKUPs break. |
| Village codes | Numeric 100-107, used as 3-digit prefix on workspaces and sheets. |
| File naming | `[VillageCode]-[Description]-[YYMMDD]-v[NN].[ext]`. Hyphens between components, no spaces (spaces only inside the description). |
| Currency | NZD. Send as plain number; column formatting renders it. |

---

## 9. What you must not do

- Do not skip the self-audit. Every session starts with one.
- Do not trust a sheet ID from memory, prior session, hard-coded reference, or any document that was generated more than a few minutes ago.
- Do not invent picklist values. If a source value isn't in the target picklist, ask.
- Do not auto-add columns to the target sheet. Column structure is owned by the target.
- Do not write to formula-driven columns. Even if the source has values for them.
- Do not load on top of existing data unless Kyle explicitly says append-or-overwrite.
- Do not use the Smartsheet UI Excel/CSV import for this task. That import replaces sheet structure and breaks cross-sheet references. API only.
- Do not load all rows in one giant call. Batch.
- Do not silently skip errors. Surface every skipped row and why.
- Do not change anything outside the target sheet without explicit instruction.

---

## 10. Output and reporting expectations

**At session start (after self-audit):**
- Workspace and asset counts
- Anomalies flagged for awareness
- Confirmation of resolved target sheet (name, workspace, folder, ID)

**Before loading:**
- Mapping table (source columns → target columns, with skip/load action and reason)
- Validation summary (row counts, picklist mismatches, date parse issues, em-dash count)
- Hierarchy plan (how many parents, how deep, sample structure)
- Estimated batch count and rough time
- Explicit ask: "Proceed?"

**During loading:**
- Progress every 5 batches: "Batch 12 of 23 - 600 of 1150 rows loaded - on track"
- Any errors immediately, with the offending row's source data and what failed

**After loading:**
- Total loaded, total skipped, total existing rows preserved
- Spot-check results
- List of columns left untouched (formula-driven)
- List of any picklist values added (if pre-approved)
- Any anomalies for Kyle's awareness
- Final sheet row count and current API version

---

## 11. Tools you will use

**Smartsheet MCP tools:**
- `search_smartsheet` - find workspaces by name during audit
- `browse_workspace` - list workspace contents during audit
- `browse_folder` - list folder contents during audit
- `get_columns` - target sheet column metadata
- `get_sheet_summary` - target sheet row count and existing data
- `add_rows` - load new rows (one call per parent for hierarchical loads)
- `update_rows` - second pass for predecessors or any post-load corrections
- `update_column` - only if Kyle pre-approves picklist expansion for this task
- `delete_rows` - only if Kyle explicitly requests a wipe before load

**Python libraries:**
- `openpyxl` for xlsx (always with `data_only=True` to get computed values not formulas)
- Built-in `csv` for csv files
- `datetime` for date parsing
- `json` for inventory persistence (optional)

---

## 12. Pre-flight checklist (run this every time)

Before writing any rows to Smartsheet, confirm:

- [ ] Self-audit completed this session
- [ ] Target sheet ID validated against current audit inventory
- [ ] Target sheet confirmed with Kyle (name, workspace, folder)
- [ ] Source file exists at the given path
- [ ] Source file is readable (no merge errors, no encryption)
- [ ] Column mapping table built and shown to Kyle
- [ ] Formula-driven columns identified and flagged SKIP
- [ ] Picklist mismatches identified
- [ ] Em dashes scrubbed
- [ ] Hierarchy strategy chosen and shown to Kyle
- [ ] Batch plan calculated
- [ ] Kyle has said "Proceed"

If any of the above is unchecked, do not start.

---

## End of brief
