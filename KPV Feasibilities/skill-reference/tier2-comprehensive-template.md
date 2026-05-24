# Tier 2 Comprehensive Feasibility - Build Template

Read this when running Mode 1 against a retirement village model. This is the build pattern for the larger of the two-tier output pair.

## Purpose

A 15-year monthly cashflow model. Project-level economics only. Partnership waterfall (A-Class / B-Class share splits, Hāpai / KPV / Vendor allocations) is handled separately if needed.

## Structure

Six sheets in this order:
1. **Inputs** - all assumptions
2. **Cashflow** - 180 monthly columns plus 4 label columns
3. **Vendor Schedule** - vendor finance amortisation if applicable (otherwise hidden or showing zero balances)
4. **Outputs** - key metrics and verdict
5. **Sensitivity** - one-way scenario table
6. **Notes** - method, limitations, conventions

## Inputs sheet layout

Sections, in order:
- **PROJECT** - Project name (text), Model commencement date (real Excel date, not string), Land scenario (Ownership / Deferred / Lease / Vendor Finance)
- **SITE & LAND** - Land area (m²), Land price excl GST, Ground rent annual incl GST (Lease only), Deferred land payment month (Deferred only)
- **VENDOR FINANCE (if Land scenario = Vendor Finance)** - Initial payment at settlement, 2nd lump sum amount, 2nd lump sum month, Long Stop Date (period number), ORA sales sweep percentage (typically 10%), Vendor interest rate (annual, compounded annually on opening balance), Sweep start period (when ORA-sweep replaces fixed schedule)
- **UNITS** - Total unit count, Average ORA price (incl GST), Average unit size (m²)
- **DEVELOPMENT COSTS (itemised, incl GST)** - Build rate per m², Site works total, Community centre total, Preliminary costs, Holding/marketing/insurance/rates, KPV fees (transaction + management)
- **TIMING** - Development duration (months), Sales lag from completion (months)
- **KPV DEFAULTS (override if needed)** - DMF %, Tenure years, Resale fee, Capital growth annual, Cost inflation annual, Vacancy between residents (months), Refurb cost per resale, Discount rate (terminal value)

## Cashflow sheet layout

Columns A-D are labels. Columns E onwards are months 1-180 (15 years × 12).

Row sections, in order:

**TIMING block:**
- Month index (R8) - hardcoded 1, 2, 3... 180
- Development phase flag (1 if month ≤ dev months)
- Capital growth factor cumulative: `(1 + capital_growth)^((month - 1) / 12)`
- Cost inflation factor cumulative: `(1 + cost_inflation)^((month - 1) / 12)`
- Units completed cumulative: linear ramp `MIN(total_units, ROUND(total_units * month / dev_months, 0))`
- Units settled cumulative: lagged from completion by sales lag
- Units settled this month: delta of cumulative settled

**DEVELOPMENT block:**
- Land payment - varies by scenario:
  - Ownership: month 1 lump sum
  - Deferred: lump sum at specified month
  - Lease: zero here (handled on Ground rent row)
  - Vendor Finance: pulled from Vendor Schedule sheet, payment row by period
- Ground rent - monthly if Lease scenario, else zero
- Vendor interest - paid annually on outstanding vendor balance if Vendor Finance scenario, else zero. References the Vendor Schedule.
- Vertical construction - spread linearly across dev period, inflated
- Site works - spread linearly, inflated
- Community centre - spread linearly, inflated
- Preliminary costs - first 12 months only
- Holding / marketing / insurance - spread across dev period (not inflated)
- KPV fees - spread across dev period
- ORA sales (initial settlements) - units_this_month × ORA_price × growth_factor
- Net development cashflow - SUM of all above

**OPERATING (DMF cycling) block:**
- Monthly resales (count) - INDEX into Units settled cumulative one full tenure ago, divided by tenure × 12
  - Use `MAX(1, month - tenure*12)` as the lookup index
  - Range references: full row range from start_col to end_col
- DMF income on resale price: `resales × ORA_price × growth_factor × (DMF_pct - resale_fee)`
- Refurb cost on resale: `-resales × refurb_per_unit × cost_inflation_factor`
- Net operating cashflow - SUM

**TOTAL block:**
- Net cashflow (development + operating)
- Cumulative cashflow - first month = current, subsequent = prior + current
- Date (for XIRR) - `EDATE(start_date, month - 1)` for each column

## Vendor Schedule sheet layout (only needed if Vendor Finance is in use)

Standalone amortisation schedule that proves the vendor finance mechanics. Two blocks:

**Block 1: Annual Summary (rows 9-19, one row per year 1-10)**
Columns: Year, Period Range, Opening Balance, Payments, Interest @ rate, Closing Balance, Refinanced at LSD, Total Settled.

Payments per year are summed from the Cashflow Land Payment row. Interest is calculated as `IF(year × 12 ≤ Long Stop Date, opening_balance × rate, 0)`. Refinance only triggers in the year containing the Long Stop Date and equals the remaining closing balance.

**Block 2: Monthly Amortisation (rows 23-143, one row per period 1-120)**
Columns: Period, Date, Opening Balance, Payment, Closing Balance.

Each row: closing = (opening - payment). Interest is added annually (when MOD(period, 12) = 0 and period < Long Stop Date) by multiplying by (1 + interest_rate).

This sheet validates the vendor finance numbers and gives the user a year-by-year amortisation they can show the vendor.

## Outputs sheet layout

**REVENUE section:** Total ORA sales, Total DMF income over 15 years.

**COSTS section:** Itemised - Land payments (or ground rent for Lease), Vendor interest (Vendor Finance only), Vertical construction, Site works, Community centre, Preliminary costs, Holding, KPV fees, Refurb on resale (cumulative).

**METRICS section:**
- Peak debt/capital required: `-MIN(cumulative_cashflow_row)`
- Development surplus (pre-finance): SUMPRODUCT of (dev_flag = 1) × net_dev_cashflow_row
- Total development cost: sum of all cost rows (sign-flipped)
- Development margin on cost: dev_surplus / total_dev_cost
- Project IRR (15-year, XIRR): `XIRR(net_cashflow_row, date_row)`
- NPV at discount rate: `NPV(discount_rate / 12, net_cashflow_row)`
- Annual DMF at maturity: `SUM(DMF_row, last 12 months)` - critical that this includes the `Cashflow!` sheet prefix
- Terminal value: annual_DMF / discount_rate

**VERDICT:** Same logic and thresholds as Tier 1 Gateway. Conditional formatting on margin, IRR, and verdict cells.

## Sensitivity sheet

One-way scenario table showing each variable at -20%, -10%, -5%, Base, +5%, +10%, +20%. Variables: ORA price, Build rate, Unit count, DMF percentage, Tenure, Capital growth, Cost inflation, Discount rate, Vendor interest rate (if Vendor Finance).

The table shows the input values at each scenario level. It does not automatically recalculate outputs for each scenario (that would require a data table, which is fragile via openpyxl). Instead, the Notes at the bottom of the sheet tell the user to type a scenario value into the Inputs sheet and read the Outputs sheet, then return to base.

For automated two-way sensitivity, recommend a separate scenario sheet rather than adding it here.

## Critical gotchas (learned from Cromwell and Henley rebuilds)

**Use real Excel dates, not strings.** Set the Model commencement date as a `datetime.date` object with number_format `'yyyy-mm-dd'`. A string `'2026-06-30'` will break EDATE in the cashflow date row.

**Reference the date row correctly.** When building the Outputs sheet XIRR formula, reference the date row in the Cashflow sheet, not a misremembered cell in Inputs.

**Always prefix cross-sheet ranges with the sheet name.** A common bug: `=SUM(FQ30:GB30)` instead of `=SUM(Cashflow!FQ30:GB30)`. The former silently returns 0 because it points to empty cells in the current sheet.

**Vendor finance has two interest-rate fields to reconcile.** Some Henley-shaped models hold the interest rate in two places (Model Inputs E80 says one figure, Vendor Schedule D6 holds the figure actually applied). When you see this, the Vendor Schedule rate is the operative one; flag the discrepancy.

**Vendor finance payment structure is hybrid by default.** Fixed scheduled payments (initial settlement + 2nd lump sum) cover the first 15 periods. From period 16 onwards, payment switches to 10% of monthly gross ORA sales. At the Long Stop Date, any remaining balance is refinanced (treated as a cash outflow). Hard-coding monthly payments will not reconcile to a Henley-shaped model.

**Run the recalc script.** After saving, run `python3 /mnt/skills/public/xlsx/scripts/recalc.py <path> 90` and require `total_errors: 0`. The Tier 2 model has ~4,400 formulas across 180 columns. A bug in one row template propagates to all 180 columns. The recalc script catches this in seconds.

**Verify against the original.** After recalc, load with `data_only=True` and check Project IRR against the original. A Cromwell-shaped freehold standard input should give roughly 7-8% IRR. A Cromwell-shaped Deferred Land input should give roughly 14-17%. A Henley-shaped Vendor Finance input should give a comparable IRR to Deferred Land but with much lower peak capital requirement (because the vendor is funding the land position rather than the operator). If the rebuild is far from those, there is a build bug to find.

## Style conventions (same as Tier 1)

- Blue font on input cells
- Yellow fill (FFF2CC) on KPV-default inputs
- Section headers: white bold on mid-blue fill
- Title bars: white 14pt bold on dark blue fill
- Subtotal rows: bold on light blue fill
- Conditional formatting (green/amber/red) on margin, IRR, and verdict cells

## File output

Save to `/mnt/user-data/outputs/RV_Tier2_Comprehensive_Feasibility.xlsx` (or with project name prefixed if known).

## What this model deliberately does NOT include

State these explicitly in the Notes sheet:
- Partnership waterfall (handled separately if needed)
- GST timing (assumed neutral over project)
- Stage-by-stage detail (linear approximation)
- S-curve construction cost timing (linear approximation)
- Operating costs in detail (assumed funded by weekly fees outside this model)
- Weekly fee income (excluded - offsets operating costs)

