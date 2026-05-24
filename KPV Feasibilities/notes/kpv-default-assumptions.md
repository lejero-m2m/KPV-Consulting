# KPV Default Assumptions — Provenance Log

**Last updated:** 2026-05-23
**Purpose:** Source-of-truth for every default value used across the four KPV gateway feasibility workbooks. Each entry records what the default is, where it came from, and when it was last reviewed.

This is the **provenance log**. The live editable copy of these assumptions lives in the `Assumptions` sheet of each workbook (Excel users tune defaults there; this file documents *why* the defaults are what they are).

---

## Retirement Village — Gateway 1 & Gateway 2 defaults

| Assumption | Default | Source | Last reviewed |
|---|---|---|---|
| DMF percentage (on resale price) | 24% | NZ retirement village industry typical; RetireIQ Cromwell/Henley examples both use 24-25% | 2026-05-23 |
| Resident tenure (years) | 8 | NZ ILU industry average 7-9 years; midpoint adopted | 2026-05-23 |
| Resale fee | 1% | NZ retirement village industry typical | 2026-05-23 |
| Capital growth (annual) | 2% | Conservative; Lake Dunstan feasibility uses similar | 2026-05-23 |
| Cost inflation (annual) | 2% | Matched to capital growth for sensitivity neutrality at base case | 2026-05-23 |
| Discount rate (terminal value) | 15% | Stabilised RV asset cap rate proxy | 2026-05-23 |
| Preferred return on capital (A-Class) | 8% | RetireIQ Cromwell/Henley examples — preferred coupon on JV capital | 2026-05-23 |
| Vacancy between residents (months) | 3 | NZ RV industry typical 2-6 months; midpoint | 2026-05-23 |
| Refurb cost on resale per unit | $40,000 | RV industry range $20k-$80k; midpoint | 2026-05-23 |
| Build rate per m² (incl GST) | $3,718 | Lake Dunstan feasibility April 2026 baseline ($3,719/m²); 107 Papamoa contract rates corroborate ($3,400-$4,200/m² range) | 2026-05-23 |
| Average ORA price (incl GST) | $859,722 | Cromwell 105u baseline; Lake Dunstan uses $914k avg | 2026-05-23 |
| Average unit size (m²) | 130 | Cromwell mid-range; KPV Papamoa N2 typology = 165m², WC = 140m² | 2026-05-23 |

### Land scenario factors (peak capital approximation)

| Scenario | Peak capital factor | Source |
|---|---|---|
| Ownership | 35% | Skill spec; reflects full land cash drag |
| Deferred | 30% | Skill spec; land cash drag deferred to midpoint |
| Lease | 30% | Skill spec; ground rent amortised |
| Vendor Finance | 20% | Skill spec; vendor carries land at their cost of capital with ORA sweep |

### Vendor finance defaults (when scenario = Vendor Finance)

| Assumption | Default | Source |
|---|---|---|
| Vendor interest rate | 4% p.a. | Henley benchmark — Counter Payment Terms model |
| Long Stop Date | 7 years | Henley benchmark; 5-7 yr typical |
| ORA sweep percentage | 10% | Henley benchmark — % of monthly ORA sales |
| Sweep start period | Month 16 | Henley benchmark — when ORA sweep begins |
| Initial deposit | $3,500,000 | Project-specific; placeholder from Henley |
| 2nd lump sum | $3,000,000 at month 16 | Project-specific; placeholder from Henley |

---

## Residential — Gateway 1 & Gateway 2 defaults

Sources: Kyle's existing Stage 2 + Stage 3 templates (Lejero-branded), KPV's BOP/Canterbury portfolio context.

| Assumption | Default | Source | Last reviewed |
|---|---|---|---|
| Infrastructure deduction % | 10% | Lejero benchmark — roads, reserves, easements typical | 2026-05-23 |
| Land development contingency % | 5% | Lejero benchmark | 2026-05-23 |
| Vertical contingency % | 3% | Lejero benchmark | 2026-05-23 |
| Renovation contingency % | 8% | Lejero benchmark (Stage 3 only) | 2026-05-23 |
| Project duration | 18 months (G1), 24 months (G2) | Stage 2 + Stage 3 benchmarks | 2026-05-23 |
| Avg floor area per unit | 120 m² | Stage 2 benchmark | 2026-05-23 |
| Build rate (incl GST) | $3,200-$3,600/m² | MGH benchmark per Stage 2 | 2026-05-23 |
| GST rate | 15% | NZ statutory | 2026-05-23 |
| Commission rate | 3.0% | NZ residential agent benchmark | 2026-05-23 |
| Legal costs per unit | $5,000 | Lejero benchmark | 2026-05-23 |
| Advertising budget | $5,000 total | Lejero benchmark | 2026-05-23 |
| Legal — purchase | $3,500 | Lejero benchmark | 2026-05-23 |
| LIM report | $591 | Council standard | 2026-05-23 |
| Due diligence / survey | $2,500 | Lejero benchmark | 2026-05-23 |
| LINZ & BOPRC fees | $1,350 | LINZ 223/224 processing | 2026-05-23 |
| Rates & sundries | $2,000 | Lejero benchmark | 2026-05-23 |
| Statutory contingency % | 3% | Lejero benchmark | 2026-05-23 |
| Equity % | 20% | Lejero benchmark | 2026-05-23 |
| Interest rate (p.a.) | 10% | Dev finance rate; confirm with lender per project | 2026-05-23 |
| Arrangement fee % | 2.0% | Lejero benchmark | 2026-05-23 |

### Professional fees ($/m² useable land)

| Item | Default | Source |
|---|---|---|
| Pre-development (geotech, hazard) | $12/m² | Lejero benchmark |
| Civil design | $20/m² | Lejero benchmark |
| Authority processing | $5/m² | Lejero benchmark |
| Supervision / QA | $8/m² | Lejero benchmark |
| Survey / legal / LINZ | $30/m² | Lejero benchmark |

### Civil & infrastructure ($/m² useable land)

| Item | Default | Source |
|---|---|---|
| Earthworks | $20/m² | Lejero benchmark |
| Roads / footpaths | $40/m² | Lejero benchmark |
| Stormwater | $7/m² | Lejero benchmark |
| Wastewater | $7/m² | Lejero benchmark |
| Water supply | $7/m² | Lejero benchmark |
| Power / telecom | $5/m² | Lejero benchmark |
| Lighting / landscaping | $5/m² | Lejero benchmark |

### Council fee benchmarks

| Council | Building consent fee | Notes |
|---|---|---|
| TCC (Tauranga City Council) | ~$38,000 | Stage 2 reference |
| WBOPDC (Western Bay of Plenty) | ~$12,000 | Stage 2 reference |
| Matamata-Piako DC | ~$7,600 | Stage 2 reference |
| SDC (Selwyn District Council) | TBC for 103 Rolleston | Add when verified |
| CODC (Central Otago District Council) | TBC for Lake Dunstan | Add when verified |

### Capital discipline thresholds (Lejero standard — do not change per project)

| Threshold | Value | Rationale |
|---|---|---|
| Min gross margin | 20% | Flag if below; do not proceed without review |
| Min ROC (Return on Cost) | 25% | Industry-standard hurdle |
| Max L/I ratio | 4.5x | Above this = recommend decline |
| Max peak debt / GDV | 65% | Industry standard bank limit |
| Min break-even safety | 10% | Break-even must be ≥10% below comparable median |

---

## Retirement Village verdict thresholds

| Verdict | Trigger | Rationale |
|---|---|---|
| PROCEED | margin ≥ 15% AND IRR ≥ 15% | Skill spec; conservative for RV |
| PROCEED WITH CAUTION | All other cases | Default middle state |
| DECLINE | margin < 8% OR IRR < 10% | Skill spec; firm floor |

Conditional formatting on margin and IRR cells:
- Green: margin ≥ 15% or IRR ≥ 15%
- Amber: 8-15% margin or 10-15% IRR
- Red: margin < 8% or IRR < 10%

---

## Residential verdict logic

Per Stage 2 template, the verdict combines 5 threshold tests (Min Gross Margin, Min ROC, Max L/I, Max Peak Debt/GDV, Min Break-even Safety). Single IF/OR formula in the Summary sheet routes to GO / NO-GO / INVESTIGATE.

---

## Village Reference Rates (live KPV portfolio benchmarks — added 2026-05-23)

Per-unit and per-hectare rates derived from the 2027 Master Project Budgets of three operational/in-construction villages. Now embedded in each workbook's `Assumptions` sheet (RV G1 + Res G1 + Res G2 append the block at the bottom; RV G2 has its own `Village Benchmarks` tab).

### Source workbooks (kept under `examples/budgets/`)

| Village | File | Units | Site area (approx ha) |
|---|---|---:|---:|
| KP Papamoa | `2027 Master Projected Budget - KP Papamoa (1).xlsx` | 114 | 5.7 |
| KP Rototuna | `2027 Master Project Budget - KP Rototuna 08052026.xlsx` | 131 | 5.5 |
| KP Waihi Beach | `2027 Master Project Budget - KP Waihi Beach.xlsx` | 96 | 4.8 |
| KLE (Drury) | `2027 Master Project Budget - KLE.xlsx` | — | — (per-unit-type structure, no consolidated rollup; not extracted) |

Site areas are approximate (confirm per project). Land area is not stated in the budget workbooks themselves — the "Land consumed" rows are dollar values (lease-basis allocation), not square metres.

### Per-unit benchmarks (NZD, incl GST)

| Metric | Papamoa | Rototuna | Waihi | KPV avg |
|---|---:|---:|---:|---:|
| Construction $/unit | 414,329 | 476,223 | 524,852 | 471,801 |
| Landscaping $/unit | 18,620 | 18,072 | 20,017 | 18,903 |
| Council Dev fees $/unit | 25,449 | 22,087 | 26,782 | 24,773 |
| Infrastructure $/unit | 100,740 | 42,869 | 108,212 | 83,940 |
| Other site works $/unit | 7,852 | 9,463 | 11,993 | 9,769 |
| Prof fees + Prelim $/unit | 16,858 | 20,147 | _(n/a)_ | 18,502 |
| Total Dev Cost $/unit | 630,314 | 633,486 | 871,630 | 711,810 |
| Sales $/unit | 908,322 | 937,563 | _(n/a)_ | 922,942 |
| Gross margin % | 30.6% | 32.4% | _(n/a)_ | 31.5% |

### Per-hectare proxy (derived using approximate site areas above — sanity check only)

| Metric | Papamoa | Rototuna | Waihi | KPV avg |
|---|---:|---:|---:|---:|
| Construction $/ha | $8.29M | $11.34M | $10.50M | $10.04M |
| Infrastructure $/ha | $2.01M | $1.02M | $2.16M | $1.73M |
| Total Dev Cost $/ha | $12.61M | $15.09M | $17.43M | $15.04M |

Per-hectare rates vary materially with density and site complexity. Use per-unit rates as primary benchmark for KPV RV work; per-ha as cross-check.

### Notable cross-village patterns

- **Construction per unit** trends up over time: Papamoa $414k (oldest) → Rototuna $476k → Waihi $525k (newest). Reflects build-cost inflation 2022–2026.
- **Infrastructure per unit** varies widely ($43k Rototuna vs $108k Waihi) — driven by site-specific civils and density.
- **Total dev cost per unit** clusters $630k-$870k across the portfolio. Use $700k as a back-of-envelope.
- **Gross margin** 30-32% on the two villages with sales data — consistent with KPV's expected return profile.
- **Council fees per unit** $22-27k across BoP/Waikato — Selwyn (103 Rolleston) and CODC (Lake Dunstan) likely differ.

## Data-validation dropdowns (added 2026-05-23)

Each workbook now has dropdown lists on picklist cells to prevent typos that silently fall through IF chains:

| Workbook | Sheet | Cell | Options |
|---|---|---|---|
| RV Gateway 1 | Assumptions | B8 | Ownership / Deferred / Lease / Vendor Finance |
| RV Gateway 2 | Inputs | C7 | Same |
| Residential G1 | Assumptions | B7 (Council) | TCC / WBOPDC / Matamata-Piako DC / SDC / CODC / Hamilton CC / Auckland Council / Other |
| Residential G1 | Assumptions | B12 (Keep dwelling) | Yes / No |
| Residential G1 | Assumptions | B13 (Title Type) | Fee Simple / Cross Lease / Unit Title |
| Residential G1 | Assumptions | B14 (Unit Type) | Stand Alone / Townhouse / Apartment / Duplex |
| Residential G1 | Assumptions | B15 (Topography) | Flat (0-5) / Gentle (5-10) / Moderate (10-20) / Steep (>20) |
| Residential G2 | Assumptions | matching rows | Same set as G1 |

## Review cadence

These defaults should be re-reviewed:
- **Quarterly** for cost rates (build rate, professional fees, civil rates) — construction market drift
- **Annually** for revenue rates (ORA prices, capital growth) — market conditions
- **On every major contract** (e.g. new village build) — actual rates vs default
- **On every regulatory change** (RV Act amendment, RMA reform, council fee schedule update)

When refreshed, update the `Last calibrated` cell at the top of each workbook's Assumptions sheet AND this file in the same commit.
