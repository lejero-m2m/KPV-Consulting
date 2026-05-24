# KPV Gateway Verdict Thresholds

**Purpose:** Document the verdict logic and thresholds across all four workbooks, and the rationale for each. Calibration history goes here.

---

## Retirement Village (Gateway 1 + Gateway 2)

Same logic in both. Two metrics, three outcomes.

### Logic

```
IF margin_on_cost >= 15% AND IRR >= 15%  → PROCEED
ELSE IF margin_on_cost < 8% OR IRR < 10%  → DECLINE
ELSE                                       → PROCEED WITH CAUTION
```

### Threshold values (default — editable on Assumptions sheet)

| Threshold | Value | Source |
|---|---|---|
| PROCEED margin (min) | 15% | Skill spec; conservative RV development margin floor |
| PROCEED IRR (min) | 15% | Skill spec; reflects KPV's required return for non-trivial RV development |
| DECLINE margin (max) | 8% | Skill spec; below this, the project doesn't justify the operational drag |
| DECLINE IRR (max) | 10% | Skill spec; below this, capital is better deployed elsewhere |

### Conditional formatting

- Margin cell:
  - Green if ≥ 15%
  - Amber if 8-15%
  - Red if < 8%
- IRR cell:
  - Green if ≥ 15%
  - Amber if 10-15%
  - Red if < 10%
- Verdict cell:
  - Green fill on "PROCEED"
  - Amber fill on "PROCEED WITH CAUTION"
  - Red fill on "DECLINE"

### Sanity benchmarks

From the skill's reference benchmarks (used during validation):

| Scenario shape | Expected verdict | Why |
|---|---|---|
| Cromwell-shaped Ownership | DECLINE (margin -2%, IRR -4%) | Full land cash drag plus standard build costs makes Cromwell unviable at freehold |
| Cromwell-shaped Deferred Land | PROCEED WITH CAUTION (margin thin, IRR strong) | Capital recycling rescues IRR; margin still tight |
| Henley-shaped Vendor Finance | PROCEED or PROCEED WITH CAUTION | Vendor carries the land position; peak capital 60-65% lower than Ownership at same project scale |

---

## Residential (Gateway 1 + Gateway 2)

Different logic — combines 5 threshold tests via a single IF/OR formula in the Summary sheet.

### Logic

```
IF (margin >= 20%) AND (ROC >= 25%) AND (L/I <= 4.5) AND (peak_debt/GDV <= 65%) AND (break_even_safety >= 10%)
    → GO
ELSE IF any of (margin < some_floor) OR (ROC < some_floor) OR (peak_debt/GDV > 70%)
    → NO-GO
ELSE
    → INVESTIGATE
```

(Exact thresholds in the Stage 2 + Stage 3 template Summary sheet formula — `notes/kpv-default-assumptions.md` lists them.)

### Threshold values (default — editable on Assumptions sheet, "Capital Discipline Thresholds" section)

| Threshold | Value | Source |
|---|---|---|
| Min Gross Margin | 20% | KPV Standard — flag if below, do not proceed without review |
| Min ROC (Return on Cost) | 25% | KPV Standard — industry-standard hurdle |
| Max L/I Ratio | 4.5x | KPV Standard — above this, recommend decline |
| Max Peak Debt / GDV | 65% | KPV Standard — industry-standard bank limit |
| Min Break-even Safety | 10% | KPV Standard — break-even must be ≥ 10% below comparable median |

### Conditional formatting

Per Stage 2 template:
- Each threshold cell shows PASS / FAIL with green / red fill
- Summary verdict cell shows GO (green) / INVESTIGATE (amber) / NO-GO (red)

---

## Calibration history

| Date | Workbook | Threshold | Change | Reason |
|---|---|---|---|---|
| 2026-05-23 | All RV | PROCEED 15/15, DECLINE 8/10 | Initial adoption from skill | Skill spec defaults |
| 2026-05-23 | All Residential | 5 KPV Standard thresholds | Initial adoption from Stage 2/3 templates | Lejero Standard defaults |

Add rows here whenever a threshold changes. Pair every change with:
- New value on the workbook's Assumptions sheet
- Updated entry in `notes/kpv-default-assumptions.md`
- Updated `Last calibrated` cell on the Assumptions sheet
- Commit message that names the change

---

## Open validation items

These need Kyle's first-open-in-Excel pass (the build environment can't recalculate, so threshold validation against Cromwell historicals is deferred):

- [ ] Run Gateway 1 with Lake Dunstan inputs — verdict expected: PROCEED
- [ ] Run Gateway 1 with each of the 4 historical Cromwell variants (91u / 100u / 105u / Hapai)
  - Record verdict per variant
  - Confirm aligns with documented decision at the time
  - If misfire, adjust thresholds + log here
- [ ] Run Residential Gateway 1 with a known-marginal opportunity — verdict expected: INVESTIGATE
- [ ] Run Residential Gateway 1 with a known-bad opportunity (high land cost, low yield) — verdict expected: NO-GO

Surface results in a future session and the table above gets populated.
