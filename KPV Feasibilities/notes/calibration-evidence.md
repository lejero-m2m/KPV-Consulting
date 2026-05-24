# KPV Gateway Workbooks — Calibration Evidence

**Purpose:** Track how the four gateway workbooks compare against KPV's existing reference models. Updated whenever a calibration run happens.

---

## Status

**Initial build complete (2026-05-23).** Calibration runs deferred to Kyle's first open in Excel — the build environment can't recalculate XLSX files (no usable JRE/LibreOffice for headless conversion).

When Kyle opens each workbook in Excel for the first time, the following calibration table should be filled in:

---

## Retirement Gateway 2 vs. Lake Dunstan Feasibility (April 2026)

**Reference:** `KPV-Knowledge-Base/cromwell/Lake Dunstan Feasibility - April 2026.xlsx`
**Inputs to enter:** 4.91 ha land area, 100 units (20 × 1bd, 50 × 2bd, 30 × 3bd), $914,000 avg ORA, $3,719/m² build rate, Lease scenario (5% cap rate ground rent ~$381k/yr per knowledge base).

Target tolerance: **±5% on each of the 10 headline outputs**.

| Output | Lake Dunstan reference | Gateway 2 result | Delta | Within ±5%? |
|---|---|---|---|---|
| Total ORA sales | _(populate)_ | _(populate)_ | | |
| Total development cost | | | | |
| Development surplus | | | | |
| Preferred interest accrual | | | | |
| Peak capital required | | | | |
| Development margin on cost | | | | |
| Margin on capital | | | | |
| Project IRR (15-yr, real) | | | | |
| Annual DMF at maturity | | | | |
| Terminal value | | | | |

If any output is > 5% out, hypothesise which default needs adjustment:
- Discount rate too low? (terminal value out)
- KPV fee structure not matched? (cost line out)
- Cost inflation/capital growth divergence from RetireIQ? (multi-output drift)
- Vendor finance peak capital factor wrong? (peak capital + IRR out)

---

## Retirement Gateway 2 vs. RetireIQ Cromwell 105u

**Reference:** `examples/Cromwell RV - Financial Analysis 105 units 16042026 - gated (1).xlsx`
**Inputs to enter:** Match Cromwell baseline (105 units, $859,722 avg ORA per the template defaults, 49,109 m² land, etc.)

| Output | RetireIQ Cromwell | Gateway 2 result | Delta | Within ±5%? |
|---|---|---|---|---|
| Total ORA sales | | | | |
| Total development cost | | | | |
| Development margin on cost | | | | |
| Project IRR | | | | |
| Peak capital | | | | |

---

## Retirement Gateway 2 vs. RetireIQ Henley 96u (Vendor Finance)

**Reference:** `examples/Henley RV - Financial Analysis 96 units 24042026 - gated - Counter payment terms.xlsx`
**Inputs to enter:** 96 units, Vendor Finance scenario (4% p.a., 7-year long stop date, $3.5m initial deposit, $3m 2nd lump sum at month 16, 10% ORA sweep from month 16).

| Output | RetireIQ Henley | Gateway 2 result | Delta | Within ±5%? |
|---|---|---|---|---|
| Total ORA sales | | | | |
| Total dev cost | | | | |
| Margin on cost | | | | |
| Project IRR | | | | |
| Peak capital | | | | |
| Vendor interest paid (total) | | | | |

Henley should produce a comparable IRR to Cromwell-Deferred but with materially lower peak capital (vendor carries land at their cost of capital).

---

## Retirement Gateway 1 verdict against historical decisions

**References:** `KPV-Knowledge-Base/opportunities/extracted/Lake Dunstan/Financial Models/*.xlsx` (4 historical Cromwell models)

| Source model | Scenario | Units | Documented decision | Gateway 1 verdict | Aligns? |
|---|---|---|---|---|---|
| _(populate when run)_ | | 91 | | | |
| | | 100 | | | |
| | | 105 | | | |
| | Hapai variant | | | | |

If a verdict misfires (e.g. Gateway 1 says DECLINE on a project that was historically approved), adjust the threshold defaults on the Assumptions sheet and log in `notes/gate-thresholds.md`.

---

## Residential Gateway 1 + 2 calibration

No KPV residential-feasibility reference outputs exist yet for calibration. Test approach when Kyle has a residential opportunity:
1. Run the live KPV residential feasibility (whatever method Kyle currently uses) on the same site
2. Compare Gateway 1 verdict + headline numbers
3. Run Gateway 2 against the live feasibility — should sit within ±10% (looser tolerance for residential without an established reference workflow)

---

## Limitations of this calibration

- **Reference workbooks may have errors of their own.** RetireIQ outputs aren't ground truth; they're another model. ±5% tolerance accepts that both have approximations.
- **Defaults that match RetireIQ may not match Lake Dunstan exactly.** RetireIQ outputs use Cromwell shape; Lake Dunstan is a different geography (Otago vs Otago — same region but different site). Some defaults may need to be Lake-Dunstan-specific.
- **Vendor finance peak capital factor is an approximation.** The 20% factor for Vendor Finance is the skill's stated approximation; actual peak capital depends on exact payment schedule, sweep timing, and refinance terms. If Henley calibration is off, this is the first knob to turn.

---

## Refresh cadence

Re-run calibration when:
- Defaults are changed (every change should trigger a re-calibration pass on whichever scenario is most affected)
- A new KPV village settles (provides fresh data points for build rate, ORA price, time-to-completion)
- The skill spec is updated (rare but worth a sweep)
