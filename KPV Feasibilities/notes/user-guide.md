# KPV Gateway Feasibilities — User Guide

**Purpose:** Quick reference for driving each of the four feasibility workbooks.

---

## Workbook map

| Workbook | Asset class | Stage | When to use |
|---|---|---|---|
| `KPV Retirement Gateway 1.xlsx` | Retirement village | Gateway 1 | 30-min sense check on a vendor pitch or land listing |
| `KPV Retirement Gateway 2.xlsx` | Retirement village | Gateway 2 | After G1 passes — full 15-year monthly cashflow |
| `KPV Residential Gateway 1.xlsx` | Standard residential | Gateway 1 | 30-min sense check on a subdivision opportunity |
| `KPV Residential Gateway 2.xlsx` | Standard residential | Gateway 2 | After G1 passes — 24-month monthly cashflow + threshold tests |

**Rule:** always run Gateway 1 first. If it fails the gate, stop. If it passes, take inputs across to Gateway 2.

---

## How to drive a workbook

### Step 1 — Open the Assumptions sheet first

Every workbook has an `Assumptions` sheet. This is the **only sheet you edit**. Every other sheet references this one.

Convention on the Assumptions sheet:
- **Blue font** = your project-specific value (you must enter this)
- **Yellow fill** = KPV default (editable but pre-populated)
- **Plain text** = calculated or reference value (do not edit)

### Step 2 — Enter project-specific values (blue font cells)

For all four workbooks the user-input cells you must fill in include:
- Site address, council, land area
- Unit count and average unit size
- Target ORA price (RV) or target sale price (residential)
- Land purchase price

### Step 3 — Review the KPV defaults (yellow fill cells)

The defaults are pre-populated from Lake Dunstan, Papamoa, Cromwell + Henley historicals (RV), and Lejero/MGH benchmarks (residential). Provenance is in `notes/kpv-default-assumptions.md`.

Tune any default if you have better local evidence (e.g. confirmed build rate from a recent contract; council fee from current schedule).

### Step 4 — Read the verdict

**Retirement Gateway 1 + 2** — verdict on the Gateway/Outputs sheet:
- **PROCEED** = margin ≥ 15% AND IRR ≥ 15% (green)
- **PROCEED WITH CAUTION** = anything in between (amber)
- **DECLINE** = margin < 8% OR IRR < 10% (red)

**Residential Gateway 1 + 2** — verdict on the Summary sheet:
- **GO** = all 5 thresholds pass (margin ≥ 20%, ROC ≥ 25%, L/I ≤ 4.5x, peak debt/GDV ≤ 65%, break-even safety ≥ 10%)
- **INVESTIGATE** = some pass, some fail
- **NO-GO** = any critical threshold fails

### Step 5 — Use the Sensitivity sheet

Each workbook has a Sensitivity sheet showing how the answer moves when you vary key inputs (ORA price, build rate, unit count, growth, etc.). Use it to find your break-evens and your buffer.

For Gateway 2 only: type a scenario value into Assumptions, read the Outputs sheet, then return to base. (Automatic sensitivity tables aren't included — they're fragile via openpyxl. Manual scenario runs are reliable.)

---

## Sheet-by-sheet contents

### Retirement Gateway 1 (3 sheets, ~22 formulas)
- `Gateway` — your verdict at a glance: project inputs on the left, calculations on the right, verdict at bottom
- `Assumptions` — editable defaults + project inputs (the only sheet you edit)
- `Notes` — method, limitations, transition to Gateway 2

### Retirement Gateway 2 (6 sheets, ~4,400 formulas, 15-year monthly cashflow)
- `Inputs` — project inputs + KPV defaults (editable; labelled "Inputs & Assumptions" at top)
- `Cashflow` — 180-month cashflow with full DMF cycling and vendor finance amortisation
- `Vendor Schedule` — vendor finance amort table (relevant only when scenario = Vendor Finance)
- `Outputs` — peak debt, margin, project IRR, NPV, terminal value, verdict
- `Sensitivity` — one-way scenario table for ORA price, build rate, units, DMF%, tenure, growth, inflation, discount, vendor rate
- `Notes` — method, gotchas, deliberately excluded items

### Residential Gateway 1 (5 sheets, ~136 formulas)
- `Cover` — project metadata
- `Assumptions` — 7 sections: Site / Development Model / Revenue / Acquisition / Professional Fees / Civil / Statutory / Finance / Thresholds (the only sheet you edit)
- `Financial Model` — pulls all inputs through, computes NRV and dev cost
- `Sensitivity` — 2-way matrix: margin by price vs cost variation
- `Summary` — single-page verdict + headline numbers

### Residential Gateway 2 (10 sheets, ~413 formulas, 24-month cashflow)
- `Cover` — project metadata
- `Assumptions` — extended (83 rows; adds zoning, MDRS, vendor terms)
- `Revenue` — per-unit and total realisation, GST, commissions
- `Dev Costs` — detailed cost breakdown by category
- `Finance` — loan structure, interest, drawdowns
- `Cashflow` — 24-month monthly cashflow
- `Returns` — ROC, ROE, profit/lot, L/I ratio, break-even
- `Sensitivity` — multi-variable sensitivity tables
- `Risk Register` — risk scoring and tracking
- `Summary` — verdict + headline numbers

---

## Updating defaults

When market conditions change (e.g. a new build rate becomes evidenced):
1. Edit the value in the workbook's Assumptions sheet (yellow cell)
2. Update the provenance entry in `notes/kpv-default-assumptions.md`
3. Update the `Last calibrated` cell at the top of the Assumptions sheet
4. Commit both changes together so the workbook + provenance log stay in sync

---

## Limitations

- **No partnership waterfall in RV models** — these are project-level. JV split modelling (A-Class / B-Class) is a separate step.
- **No staging in RV models** — units are assumed to deliver linearly over development duration. Real staging effects are not captured.
- **GST timing assumed neutral** — net-of-GST inputs throughout; no cashflow timing for GST returns.
- **Residential Gateway 1 has no cashflow** — it's a single-point P&L. Gateway 2 adds the 24-month timing.
- **Sensitivity is manual on Gateway 2** — type a value, read the output, return to base.
- **All numbers are NZD incl GST unless stated otherwise** in the assumption row.

---

## Open validation items (Kyle's first-use checklist)

Calibration deliberately deferred to Kyle's first open in Excel (the build environment can't recalculate workbooks):

1. Open `KPV Retirement Gateway 2.xlsx`, enter Lake Dunstan inputs (4.91 ha, 100 units, $914k avg ORA, $3,719/m²). Confirm the 10 headline outputs sit within ±5% of `KPV-Knowledge-Base/cromwell/Lake Dunstan Feasibility - April 2026.xlsx`.
2. Open `KPV Retirement Gateway 1.xlsx` and run the same Lake Dunstan inputs. Verdict should be PROCEED (matches actual KPV decision to take Lake Dunstan to deeper feasibility).
3. Run Gateway 1 with each of the 4 historical Cromwell variants in `KPV-Knowledge-Base/opportunities/extracted/Lake Dunstan/Financial Models/`. Confirm verdicts align with what was decided at the time.
4. If any verdict misfires, adjust the threshold defaults on the Assumptions sheet, document the change in `notes/gate-thresholds.md`.

Surface any unexpected results when you've run them — happy to recalibrate.
