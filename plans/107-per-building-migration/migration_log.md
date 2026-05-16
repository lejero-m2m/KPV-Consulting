# 107 Papamoa — Per-Building Architecture Migration — Log

Source brief: `smartsheet/input/107-per-building-architecture-migration.md`
Operator: Claude (gated execution — stops at every brief checkpoint for Kyle's confirmation)

---

## 2026-05-16 — Setup

- Created `plans/107-per-building-migration/`
- Verified 4 sheet IDs against `api.smartsheet.com` (web app is `app.smartsheet.au`; API host is `.com`):
  - `5631895457976196` → 107 - Papamoa Budget — HTTP 200
  - `5063906232848260` → 107 - Construction Programme — HTTP 200
  - `2635310868418436` → 107 - Construction Register — HTTP 200
  - `5289542339743620` → 107 - Unit Register — HTTP 200
- Setup complete.

## 2026-05-16 — Phase 0 (Archive folder)

- "02 - Civil and Construction" folder = `2549523147974532`
- No Archive subfolder existed → created `Archive` = `6798331356702596` (empty, reversible)
- Build-alongside pattern confirmed: old Programme stays untouched as live backup.

## 2026-05-16 — Phase 1.1 (sequence mapping, read-only) — CHECKPOINT 1.1

- 52 Buildings leaf rows read from Budget; Register unit→stage map built.
- Proposed Building References written to `mapping.json` (old values preserved).
- Sequence by ascending lowest unit per effective (Register) stage.
- 13 flags raised: 12 benign (Stage 2 → sub-stage refinement, per locked decision) + **1 real conflict: `178,176`** (Budget "Stage 4 and 5" vs Register "Stage 3").
- Pavilion (`PAV-B01`) NOT yet assigned — parent-row special case, pending Kyle confirm.
- Checkpoint 1.1 — Kyle approved 2026-05-16: `178,176` → S3-B05 (trust Register); PAV-B01 on Pavilion parent; proceed.

## 2026-05-16 — Phase 1.2 / 1.3 — CHECKPOINT 1.3 PASS

- Added `Building Reference` column to Budget (id `7028778852454276`, TEXT_NUMBER, index 12, before Units).
- Populated 53 rows in one batched PUT (52 buildings + Pavilion parent `8802769610145668` → PAV-B01).
- Verify: 53 expected = 53 live, 0 mismatches, 0 unexpected rows, 0 duplicate references. **PASS.**
- **FLAGGED for later:** Budget row `178,176` still has Section = "Stage 4 and 5" but its Building Reference is S3-B05 (Register stage = Stage 3). Per Kyle's decision the Register is truth; the Budget Section is mis-tagged. Out of Phase 1 scope (Phase 1 only adds/populates Building Reference) — surface for a decision before/at cutover.
- Kyle: "Continue please." → proceeded to Phase 2a.

## 2026-05-16 — Phase 2a (read-only dependency audit) — CHECKPOINT 2a

- Full report: `phase_2a_audit.md`. Pagination bug found+fixed (Programme = 658 rows over 2 pages; first run truncated at 500).
- Counts match brief: 658 rows / 114 units / 544 non-unit.
- LOW risk: unit predecessors = 0; unit rows as predecessors = 0; cross-sheet consumers = 0.
- **HIGH risk / brief wrong:** 108/114 unit rows are parents with ~5 construction sub-tasks each (553 descendant rows). Brief assumed unit rows are leaves. Phase 2b consolidation rules don't define sub-task handling — **Phase 2b is blocked on a Kyle decision.**
- Orphan `402.0` (no Stage) → Budget says unit 402 = building S3-B15.
- 2 reports source from Programme (repoint at cutover); one is the external Signature Homes report.
- Checkpoint 2a — Kyle decided 2026-05-16: (1) **consolidate to 1 set of 5 phase sub-tasks per building** (merge matching phases across the building's units using Start=earliest / End=latest / %=avg→5% / RAG=worst); (2) **orphan 402 → Stage 3 / S3-B15** (fold into that building).

## 2026-05-16 — Phase 2b.1 (create new sheet) — CHECKPOINT 2b.1

- Building new `107 - Construction Programme (per building)` alongside (old Programme untouched = live backup).
- Non-Gantt columns created via API; Duration/Predecessors + Gantt date behaviour require Dependencies enabled in the UI (API cannot set this).
- New sheet `107 - Construction Programme (per building)` = `4820480841174916`. Gantt-at-creation rejected (error 1032) per brief; created non-Gantt then Kyle enabled Dependencies in UI. UI auto-added Duration + Predecessors, tagged Start/End/% as Gantt. RAG RYGG symbol deferred to UI cleanup (API quirk 1235 — cosmetic).
- Kyle: "done" (Dependencies enabled). Verified dependenciesEnabled=true, ganttEnabled=true.

## 2026-05-16 — Phase 2b.2 / 2b.4 — CHECKPOINT 2b.4 PASS

- Populated 53 building rows + 250 consolidated phase children (one set of 5 per building per Kyle's Checkpoint 2a rule).
- Bug found+fixed: Programme uses hyphen unit names (`180-1`), Budget uses slash (`180/1`). S4-B01 + S4-B03 initially empty; targeted re-fix with separator-normalised matching → both now 5 units / 5 phases. No other building affected.
- Final: **313 rows = 53 buildings + 260 phase children.** Every building has 5 phase children except PAV-B01 (0 — Pavilion has no Programme units, expected).
- Manual sample S1-B02 (units 102,104): Foundation consolidated Start = 2025-01-15 = min(102,104) ✓. Parent Gantt rollup correct (Start 2025-01-15 / End 2025-06-18).
- **Row count differs from brief's ~602 estimate by design:** brief assumed copying 544 task rows verbatim; Kyle's Checkpoint 2a decision (consolidate to 5/building) supersedes that → 313 rows, leaner. Not missing data.
- Predecessor rebuild (Step 2b.3): moot — Phase 2a found 0 unit predecessors.
- Old Programme, Register, Unit Register untouched; Budget unchanged except Phase 1 Building Reference column. Fully reversible (delete new sheet + drop Budget column).
- Kyle: "continue" → Phase 2c.

## 2026-05-16 — Phase 2c (Register Contract Block) — CHECKPOINT 2c PASS

- Dry-run found only 17/128 rows had a Contract Block (Stage 1 only); 111 blank. Intent: set Contract Block = Building Reference for every real unit row (join key to Budget/Programme).
- Anomaly: bare `180`/`182` Register rows (siblings of 180-1..5 / 182-1..5, Stanaway, Stage 4, no children). Kyle decided 2026-05-16: **tag bare 180→S4-B01, bare 182→S4-B03** (block-level rows).
- Mitigation applied: 116 old Contract Block values preserved to `mapping.json`; added `Contract Block (Legacy)` column (id `1026239933747076`) populated with old values.
- Wrote Building References to Contract Block for 116 rows.
- Verify: 116 rows, 0 Contract Block mismatches, 0 legacy mismatches, 0 Register values absent from Budget's 53 Building References. **PASS — full Budget↔Register join integrity.**
- **PAUSED at Checkpoint 2c. Next is Phase 3 — Sales Status picklist conversion on the live Unit Register (cleans existing free-text sales values). Awaiting Kyle go-ahead.**

- Kyle: "continue" → Phase 3.

## 2026-05-16 — Phase 3 (Sales Status picklist) — CHECKPOINT 3.4 PASS

- Audit: 116 real units; only 5 distinct values (Settled 6, Available 6, Application 5, Not Available 4, Unconditional 1) + 94 blank. Data already clean — no Step 3.3 cleanup needed.
- Kyle approved (Checkpoint 3.2): 5 in-use values, validation ON. Brief's generic set rejected (didn't match data).
- Converted col 8282836699484036 → PICKLIST, options [Not Available, Available, Application, Unconditional, Settled], validation=true.
- Verify: type PICKLIST, validation true, counts identical to pre-conversion audit — **zero data loss. PASS.**

## 2026-05-16 — API PHASES COMPLETE

- Done & verified: Phase 1 (Building Reference), 2a (audit), 2b (per-building Programme), 2c (Register Contract Block), 3 (Sales Status picklist).
- Remaining Phases 4 (cross-sheet named ranges) & 5 (cutover/rename/move/repoint reports/memory) are **UI-only — Kyle**. Full step list: `phase_4_5_UI_checklist.md`.
- Old Programme untouched (live backup). Migration fully reversible — rollback steps in the checklist.
