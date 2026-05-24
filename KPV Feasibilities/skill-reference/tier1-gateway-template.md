# Tier 1 Gateway Feasibility - Build Template

Read this when running Mode 1 against a retirement village model. This is the build pattern for the smaller of the two-tier output pair.

## Purpose

A single-sheet gating test. The user fills it in during a 30-minute conversation with a vendor or landowner. It answers one question: does this project clear the bar to justify building a Tier 2 feasibility?

## Structure

Two sheets:
1. **Gateway** - inputs on the left (columns B-C), calculations on the right (columns F-G), verdict at the bottom of column F
2. **Notes** - method, thresholds, limitations, transition to Tier 2

## Input layout (Gateway sheet, left column)

Sections, in order:
- **Site** - Land area (m²), Land price (NZD excl GST), Land scenario (Ownership / Deferred / Lease / Vendor Finance)
- **Units** - Unit count, Average ORA price per unit (incl GST), Average unit size (m²)
- **Development costs (itemised)** - Build rate per m², Site works total, Community centre total, Preliminary costs, Holding/marketing/insurance/rates, KPV management & transaction fees. No loading factor. Each line is an itemised input.
- **Timing** - Development duration (years), Sales velocity (units/month)
- **Vendor finance (only if Land scenario = Vendor Finance)** - Vendor interest rate (annual), Long Stop Date in years (default 7)
- **KPV defaults (override if needed)** - DMF %, Tenure years, Resale fee, Capital growth, Cost inflation, Discount rate (terminal), Preferred return on capital

## Calculation layout (Gateway sheet, right column)

Sections, in order:
- **Revenue** - Gross ORA sales (initial nominal), ORA sales with capital growth during dev (mid-period inflation)
- **Costs (with mid-period inflation)** - Land payment (varies by scenario, see below), Vertical construction, Site works, Community centre, Preliminary costs, Holding, KPV fees, Resale fee on initial sales, Vendor interest cost (only if Vendor Finance), Total development cost
- **Development surplus (pre-preferred)** - Surplus, Preferred interest cost (approximation, scenario-aware), Surplus after preferred
- **Steady-state operating cashflow** - Annual DMF income on resale price, Terminal value
- **Gateway metrics** - Development margin on cost, Margin on capital (post-preferred), Indicative project IRR (15-year), Peak capital required
- **Verdict** - large coloured cell with PROCEED / PROCEED WITH CAUTION / DECLINE

## Land scenario logic

The land cost line uses an IF on the Land scenario input:
- **Ownership**: full land price at month 1, no escalation
- **Deferred**: full land price at the deferred month (assume midpoint of development for Tier 1 approximation)
- **Lease**: ground rent (6% of incl-GST land value default) × development duration years, paid as a stream during development
- **Vendor Finance**: land cost spread approximately over the Long Stop Date period. Vendor interest is a separate line below.

## Vendor interest approximation (Vendor Finance scenario only)

```
vendor_interest = land_price * vendor_rate * long_stop_years * 0.55
```

Approximation: outstanding balance averages 55% of the original obligation over the long-stop period because principal is paid down progressively (heavily from period 16 onwards via ORA sweep).

This is a cost line, not a financing line. It is paid in cash to the vendor and reduces development surplus.

## Key formula patterns

**Revenue with mid-period inflation:**
```
ORA_inflated = unit_count * avg_ORA_price * (1 + capital_growth)^(dev_years/2)
```

**Vertical construction with mid-period inflation:**
```
vertical_cost = unit_count * unit_size * build_rate * (1 + cost_inflation)^(dev_years/2)
```

**Preferred interest approximation (scenario-aware):**

```
peak_capital_factor = IF(scenario="Vendor Finance", 0.20,
                       IF(scenario="Lease", 0.30,
                         IF(scenario="Deferred", 0.30, 0.35)))
preferred_cost = total_cost * peak_capital_factor * preferred_rate * dev_years * 0.6
```

Peak capital is materially lower when the vendor or lessor is financing the land position. The factors reflect: Ownership 35% (full land cash drag), Deferred/Lease 30% (land cash drag deferred or amortised), Vendor Finance 20% (vendor carries the land at their cost of capital, with ORA-sweep paying it down).

**Annual DMF at steady state (on resale price, industry convention):**
```
annual_DMF = (unit_count / tenure) * ORA_price * (1 + capital_growth)^tenure * (DMF_pct - resale_fee)
```
Resale price grows for one full tenure period before first cycle.

**Terminal value:**
```
terminal_value = annual_DMF / discount_rate
```

**Project IRR proxy (15-year):**
```
project_IRR = RATE(15, 0, -total_cost * peak_capital_factor, terminal_value + dev_surplus)
```
Uses peak capital (scenario-aware factor as above) as average invested. 15-year horizon. Future value is terminal value plus development surplus. Vendor Finance scenarios will produce higher IRR than Ownership at equal margin because invested capital is lower.

**Peak capital approximation (scenario-aware):**
```
peak_capital = total_cost * peak_capital_factor
```
Where peak_capital_factor follows the same logic as above: 35% Ownership, 30% Deferred or Lease, 20% Vendor Finance.

## Verdict logic

```
verdict = IF(AND(margin_on_cost >= 15%, IRR >= 15%), "PROCEED",
          IF(OR(margin_on_cost < 8%, IRR < 10%), "DECLINE",
          "PROCEED WITH CAUTION"))
```

Conditional formatting on margin and IRR cells:
- Green: margin ≥ 15% or IRR ≥ 15%
- Amber: margin 8-15% or IRR 10-15%
- Red: margin < 8% or IRR < 10%

Conditional formatting on the verdict cell:
- Green fill on "PROCEED"
- Amber fill on "PROCEED WITH CAUTION"
- Red fill on "DECLINE"

## Style conventions

- Blue font on input cells
- Yellow fill (FFF2CC) on KPV-default inputs (still editable, visually flagged)
- Section headers: white bold on mid-blue fill (2E75B6)
- Title bar: white 14pt bold on dark blue fill (1F3864)
- Subtotal rows: bold black on light blue fill (DEEBF7)
- Cell comments on KPV-default cells explaining the norm

## Notes sheet content

Headings: PURPOSE, INPUTS, METHOD, THRESHOLDS, LIMITATIONS, IF THIS PROJECT PASSES THE GATE.

Be explicit about the limitations:
- No staging or tranche timing - all cash assumed at midpoint
- No partnership waterfall
- No GST timing
- No sensitivity analysis (use Tier 2 for that)
- DMF income assumes steady state from year 1 (in reality it ramps)
- No allowance for vacancy between residents
- No refurbishment cost on resale

## Verification

After saving, run the recalc script and confirm `total_errors: 0`. Then load with `data_only=True` and sanity-check the verdict against the user's expectation. Reference benchmarks:
- Cromwell-shaped Ownership inputs typically produce DECLINE (margin -2%, IRR -4%).
- Cromwell-shaped Deferred Land inputs typically produce PROCEED WITH CAUTION (margin thin, IRR strong because of capital recycling).
- Henley-shaped Vendor Finance inputs typically produce PROCEED or PROCEED WITH CAUTION at base assumptions, with peak capital approximately 60-65% lower than Ownership at the same project scale.

## File output

Save to `/mnt/user-data/outputs/RV_Tier1_Gateway_Feasibility.xlsx` (or with the project name prefixed if known: e.g. `Cromwell_RV_Tier1_Gateway.xlsx`).
