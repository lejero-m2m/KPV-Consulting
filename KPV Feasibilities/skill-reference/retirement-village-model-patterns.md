# Retirement Village Model Patterns

Read this when the workbook is a retirement village feasibility model. Identify by: ORA/DMF terminology, "occupation right", "deferred management fee", "resident tenure", "resale", "capital gain share", "weekly fees", or unit types like ILU (Independent Living Unit), serviced apartments, or care suites.

## The ORA/DMF engine

Every retirement village model has one. The structure varies but the inputs are universal.

### Core ORA inputs
- **Entry price per unit**: the Occupation Right Agreement price the incoming resident pays. Often differentiated by unit type and stage.
- **Number of units** by type
- **Sales rate / absorption**: units sold per month, often ramped (slower in months 1-6, hitting steady state by month 12)
- **Settlement timing**: months from contract to settlement (typically 2-4 months in NZ)
- **First settlement date** relative to construction completion (often 80% complete before settlements begin)

### Core DMF inputs
- **DMF percentage**: usually 20%, 25%, or 30%
- **DMF accrual period**: usually 3, 4, or 5 years (linear or stepped)
- **DMF base**: entry price or resale price (this matters; see common errors below)
- **Resident tenure assumption**: average years before resale. NZ industry average is around 7-9 years for ILUs, shorter for serviced apartments and care suites.
- **Resale price escalation**: annual % growth in unit prices. Often 3-5%.
- **Vacancy period between residents**: typically 2-6 months. Models that ignore this are optimistic.

### Capital gain share
- **Resident share of capital gain**: often 0% (operator keeps it all), sometimes 25% or 50%. RVA does not mandate any split; it's contractual.
- **Operator share of capital gain**: the complement

### Weekly fees (operational)
- Service fees / weekly fees from residents - covers operating costs
- Operator margin on services - usually thin or zero; the real margin is in DMF and capital gain

## The DMF cashflow timing trap

**This is the single most common error in retirement village feasibility models.**

DMF is accrued during the resident's tenure but **received in cash only on resale**. A model that recognises DMF in the year it accrues will overstate NPV dramatically because:
1. The cash is received years later
2. The discount factor at year 8 is meaningfully smaller than year 1

Check: does the cashflow show DMF cash receipts clustered around the resale events, or smeared across each year? If smeared, the model is wrong.

## The capital recycling pattern

On resale:
1. Operator pays the outgoing resident: `entry_price + resident_share_of_capital_gain - DMF_owed`
2. Operator receives from new resident: `new_entry_price` (escalated)
3. Net cash to operator: `new_entry_price - entry_price - resident_share_of_capital_gain + DMF_owed`

The operator's revenue per unit per cycle is:
- DMF on the previous resident (a lump sum)
- Plus the operator's share of capital gain
- Plus the price escalation between cycles if the resident share is less than 100%

This compounds over decades. Long-run retirement village models extending out 30+ years are common and necessary to capture the value properly.

## Land scenarios

Retirement village models in NZ typically support four land scenarios. Each has a different cashflow shape and a different impact on peak capital and IRR.

### Ownership (freehold or pre-paid ground lease)
Land is paid for in cash at settlement, usually month 1. Maximum cash drag on the project; highest peak capital; lowest IRR all else equal. Often used as the baseline scenario.

### Deferred Land
Land payment is deferred to a later milestone (commonly construction commencement or first settlements). Reduces early-stage cash drag without changing the total cost. Commonly used when the vendor wants certainty of payment but accepts a delay. Materially improves project IRR over Ownership at the same total cost.

### Ground Lease
Land is leased rather than purchased. Annual ground rent (typically 6% of incl-GST land value) is paid through the development and operating phases. Lowest upfront cash drag but ongoing rent reduces steady-state operating margin. Suits long-life retirement assets where the operator does not need land equity.

### Vendor Finance (Counter-payment terms)
Land vendor accepts deferred payment over a fixed term (typically 5-7 years) at an agreed interest rate (typically 4-6.5% p.a., compounded annually on the outstanding balance). Payment structure is usually hybrid:
- Initial deposit on settlement (e.g. $3-4m)
- A second scheduled lump sum at a specified month (e.g. month 16)
- From a sweep start period onwards (typically period 16), monthly payments equal a fixed percentage of gross ORA sales (typically 10%)
- A Long Stop Date by which all remaining balance must be refinanced or paid in full (commonly period 84 / year 7)
- Interest is paid annually on the average outstanding balance, capitalised or paid in cash

Vendor Finance materially reduces peak capital for the operator because the vendor is providing land finance at typically lower rates than equity preferred returns. It is the structure most likely to convert a marginal Ownership feasibility into a workable project. Henley-shaped models use this structure.

Check the vendor's stated interest rate against the rate actually applied in the amortisation table. A common bug is that the assumption sheet states one rate (e.g. 6.5%) while the amort table uses another (e.g. 4%). The amort rate is the operative one.

## Common structural errors

### Error: DMF computed on entry price
Most contracts compute DMF on the **resale price**: not the entry price. Computing on entry price understates DMF revenue significantly over long horizons because resale prices grow.

Check the formula: `=DMF_pct * entry_price` is usually wrong. Should be `=DMF_pct * resale_price`.

### Error: No vacancy between residents
Real-world resale takes 2-6 months. Models with zero vacancy overstate cashflow.

### Error: Construction cash outflows treated as straight-line
Construction costs follow an S-curve: slow start, fast middle, slow finish. Straight-line allocation understates peak debt.

### Error: Sales settlements assumed at construction completion
Settlements happen progressively as units are sold, typically starting once the building is 80% complete and continuing for months or years after physical completion. Lumping them at completion misstates timing.

### Error: No allowance for refurbishment between residents
Units typically need $20k-$80k of refurb on resale. Often missing.

### Error: Operating cost escalation lower than revenue escalation
Often weekly fees escalate at CPI but operating costs (staff, insurance, rates) escalate higher. Models with matched escalations understate operating cost growth.

### Error: IRR computed on operator cashflow but including resident equity
Operator cashflow should be net of resident money flowing through. Common to see resident entry payments treated as operator revenue without netting the obligation back out on resale.

### Error: GST treatment
Residential ORA payments are generally GST-exempt in NZ. But the construction cost includes GST that's typically recoverable for the operator only if the operator is GST-registered and treats the build as a taxable activity. Models often muddle this. Check whether costs are GST-inclusive or exclusive and whether GST is recovered.

## Key outputs to find

Every RV model should produce:
- **Peak debt / peak funding requirement**: when does the operator's cash position bottom out
- **Equity required**: the operator's contribution before debt
- **Stabilised cashflow**: the year cash turns durably positive
- **Project IRR** (unlevered) and **Equity IRR** (levered)
- **NPV at a discount rate**: usually 10-15% for retirement village development in NZ
- **Development margin**: total profit / total cost, or as a percentage of revenue

If any of these are missing, the model is incomplete.

## KPV-specific context

Karaka Pines Villages operates a portfolio across Papamoa, Waihi, Rotorua, and Drury, with feasibility models also developed for prospective sites including Cromwell and Henley. KPV uses a typology framework (Parks / Villages / Estates).

Naming conventions vary by site theme:
- Cromwell uses tree-themed unit names (Redwood, Titoki, Miro, Rosewood, Ironwood, Cypress, Olive, Juniper)
- Henley uses NZ bird-themed unit names (Takahe, Kea, Weka)
- KP Papamoa uses its own scheme

If you recognise these naming patterns, the model is KPV-shaped.

KP Papamoa is 114 units across 5 stages. Stage dependencies matter - Stage 2 civils typically gate later stages.

Cromwell is 105 units, modelled with A-Class / B-Class partnership waterfall.

Henley is 96 units, modelled with the same partnership structure but using Vendor Finance ("Counter payment terms") for the land position. It is the canonical Vendor Finance reference model in the KPV portfolio.
