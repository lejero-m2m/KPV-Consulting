# KPV Feasibilities

**Gateway feasibility tooling for KPV development opportunities.**

Four Excel workbooks supporting two asset classes (retirement village + standard residential) at two stages (Gateway 1 sense check + Gateway 2 full feasibility).

---

## The four workbooks

| Workbook | Asset class | Stage | When to use |
|---|---|---|---|
| [`KPV_Gateway_One_Feasibility.xlsx`](KPV_Gateway_One_Feasibility.xlsx) | Retirement village | Gateway 1 | **30-min sense check on vendor pitch / land listing** — adopted from FEASO Ohaupo Road template (2026-05-24) with PROJECT IDENTITY block, per-unit-rate cost scaling, 3-tier pavilion, LEVER DIAGNOSTICS section |
| [`KPV Retirement Gateway 2.xlsx`](KPV%20Retirement%20Gateway%202.xlsx) | Retirement village | Gateway 2 | Full 15-year monthly cashflow after G1 passes |
| [`KPV Residential Gateway 1.xlsx`](KPV%20Residential%20Gateway%201.xlsx) | Standard residential | Gateway 1 | 30-min sense check on subdivision opportunity |
| [`KPV Residential Gateway 2.xlsx`](KPV%20Residential%20Gateway%202.xlsx) | Standard residential | Gateway 2 | 24-month monthly cashflow after G1 passes |

**Workflow:** always Gateway 1 first. If it fails, stop. If it passes, take inputs across to Gateway 2.

---

## How they work (in 30 seconds)

Each workbook has an **`Assumptions` sheet** — the only sheet you edit. Every other sheet pulls values from it via cell references and named ranges.

Conventions on Assumptions:
- **Blue font** = your project-specific value (you must enter this)
- **Yellow fill** = KPV default (editable but pre-populated from Lake Dunstan / Papamoa / Cromwell / Henley evidence)
- **Plain text** = calculated or fixed; do not edit

Each workbook produces a single coloured verdict:
- RV: **PROCEED** (green) / **PROCEED WITH CAUTION** (amber) / **DECLINE** (red)
- Residential: **GO** (green) / **INVESTIGATE** (amber) / **NO-GO** (red)

Drill into the Outputs / Summary sheet for the headline numbers; into the Sensitivity sheet for tolerance to assumption shifts.

---

## Folder layout

```
KPV Feasibilities/
├── KPV Retirement Gateway 1.xlsx       # 3 sheets, ~22 formulas
├── KPV Retirement Gateway 2.xlsx       # 7 sheets (incl Village Benchmarks), ~4,400 formulas (15-yr monthly cashflow)
├── KPV Residential Gateway 1.xlsx      # 5 sheets, ~136 formulas
├── KPV Residential Gateway 2.xlsx      # 10 sheets, ~413 formulas (24-mo monthly cashflow)
├── README.md                            # This file
├── build_workbooks.py                   # Build script (rerun to refresh defaults)
├── enrich_workbooks.py                  # v2 enrichment: dropdowns + village rates block
├── examples/                            # Source examples Kyle dropped
│   ├── Cromwell RV - Financial Analysis 105 units 16042026 - gated (1).xlsx
│   ├── Henley RV - Financial Analysis 96 units 24042026 - gated - Counter payment terms.xlsx
│   ├── Stage 2 - gateway report - example.docx   # Word output report template
│   ├── Stage2_Gateway_Feasibility_example Template.xlsx
│   ├── Stage3_Full_Feasibility_example.xlsx
│   └── budgets/                         # KPV 2027 Master Project Budgets (source for village benchmarks)
│       ├── 2027 Master Projected Budget - KP Papamoa (1).xlsx
│       ├── 2027 Master Project Budget - KP Rototuna 08052026.xlsx
│       ├── 2027 Master Project Budget - KP Waihi Beach.xlsx
│       └── 2027 Master Project Budget - KLE.xlsx
├── notes/
│   ├── kpv-default-assumptions.md       # Provenance log — every default with source + last reviewed
│   ├── calibration-evidence.md          # Gateway 2 vs Lake Dunstan deltas (to be filled on Kyle's first run)
│   ├── gate-thresholds.md               # Verdict logic + threshold rationale + change history
│   └── user-guide.md                    # How to drive each workbook
└── skill-reference/                     # Claude-commissioned feasibility-model-expert skill (read-only reference)
    ├── SKILL.md
    ├── RV_Tier1_Gateway_Feasibility.xlsx
    ├── RV_Tier2_Comprehensive_Feasibility.xlsx
    ├── retirement-village-model-patterns.md
    ├── tier1-gateway-template.md
    └── tier2-comprehensive-template.md
```

---

## Pending validation (Kyle's first-open-in-Excel pass)

The build environment couldn't recalculate the workbooks (no usable JRE for LibreOffice headless conversion). Three calibration items deferred to you:

1. **Open `KPV Retirement Gateway 2.xlsx`**, enter Lake Dunstan inputs (4.91 ha, 100 units, $914k avg ORA, $3,719/m², Lease scenario). Confirm the 10 headline outputs sit within ±5% of `KPV-Knowledge-Base/cromwell/Lake Dunstan Feasibility - April 2026.xlsx`. Fill in `notes/calibration-evidence.md`.

2. **Run `KPV Retirement Gateway 1.xlsx` with Lake Dunstan inputs.** Confirm verdict = PROCEED.

3. **Run Gateway 1 against each of the 4 historical Cromwell variants** in `KPV-Knowledge-Base/opportunities/extracted/Lake Dunstan/Financial Models/`. Confirm verdicts align with documented decisions. Adjust thresholds if not — log in `notes/gate-thresholds.md`.

Surface results so we can recalibrate defaults if any outputs drift outside tolerance.

---

## When defaults change

If you adjust a yellow-cell default:
1. Edit the value on the Assumptions sheet (yellow cell)
2. Update the matching entry in `notes/kpv-default-assumptions.md`
3. Update the `Last calibrated` cell at top of the Assumptions sheet
4. Commit both changes together

---

## Out of scope (deferred)

- **Word doc output reports** generated from workbook outputs — pattern exists at `examples/Stage 2 - gateway report - example.docx`; templates not yet automated.
- **Partnership waterfall** modelling (A-Class / B-Class JV splits) — handled separately when needed.
- **Smartsheet integration** — these workbooks live as files; not linked to a Smartsheet opportunities register yet.
- **Stochastic / Monte Carlo sensitivity** — current sensitivity is deterministic one-way scenarios.
