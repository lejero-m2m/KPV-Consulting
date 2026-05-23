# Additions to kpv-conventions.md

These additions go into `kpv-conventions.md` to lock the org structure, approval matrix, and data ownership model.

---

## Section X (new) — Organisational structure

KPV operates as two arms under a single Senior Leadership Team.

```
Liam (CEO)
├── Julie (CFO)
├── Kyle Dickinson (GM Developments)
│   └── Matt (Delivery Lead / Project Manager)
└── Stu (GM Sales and Operations)
    └── Deborah (Operations Lead)
```

**Senior Leadership Team (SLT):** Liam, Julie, Stu, Kyle.

### Two arms of operation

| Arm | Scope | Lead |
|---|---|---|
| **Developments** | New villages, construction, greenfield through site handover | Kyle (GM Developments) |
| **Operations** | Management of existing villages, completed units, residents, maintenance | Stu (GM Sales and Operations) |

### Crossover principle

Matt (Delivery Lead) sits in Developments but handles construction-related maintenance issues raised by Operations. He is the operational bridge between the two arms for any post-handover construction work (defects, warranty, maintenance involving build trades).

---

## Section X+1 (new) — Approval Matrix

The KPV approval model uses three patterns depending on item type:

1. **Approval workflow** — items requiring formal sign-off before action (Variations, Contracts, certain Decisions)
2. **Ownership assignment** — items having a named owner who manages them but not requiring approval to exist (Risks, RFQ requests)
3. **Notification / record** — items needing communication to the right people but not formal approval (H&S incidents, operational decisions)

### Approval Matrix

| Item type | Raise | Approve L1 | Approve L2 | Final sign-off | Escalation |
|---|---|---|---|---|---|
| Variation ≤ $5k | Matt | Matt approves | — | — | — |
| Variation $5k–$25k | Matt | Matt raises | Kyle approves | — | — |
| Variation $25k–$50k | Matt | Matt raises | Kyle approves | Julie co-signs (CFO) | — |
| Variation > $50k | Matt | Matt raises | Kyle + Julie | Liam (CEO) | — |
| Sales decision (typology/pricing/commercial) | Deborah | Deborah raises | Stu approves (sales side) | Kyle approves (development side) | Liam if material |
| RFQ request (issue an RFQ) | Anyone | Matt or designate | — | — | — |
| Contract award (low/medium) | Matt | Matt raises | Kyle approves | Liam OR SLT member signs | — |
| Contract award (material) | Matt | Matt raises | Kyle approves | Julie + Liam co-sign | — |
| Risk Register entry | Anyone | n/a (ownership not approval) | n/a | Matt + Kyle accountable for portfolio | SLT for portfolio-significant |
| Decision Log — operational | Anyone | Matt or Deborah | — | — | Kyle or Stu if cross-functional |
| Decision Log — cross-functional | Matt or Deborah | Stu OR Kyle (depending on focus) | Kyle final commercial sign-off | — | Liam if strategic |
| Decision Log — strategic | SLT | Recorded post-decision | — | — | — |
| H&S incident / serious near-miss | Anyone | Matt logs | — | — | Notify SLT per H&S policy |

### Variation threshold rationale

Thresholds are conservative starting points (May 2026). Adjust as KPV's variation volume matures and patterns stabilise.

- **$5k** — operational autonomy for Matt (small site decisions don't escalate)
- **$25k** — development-level decisions (Kyle approves; significant but routine)
- **$50k** — material commercial impact (CFO co-signs; budget visibility critical)
- **>$50k** — strategic / portfolio-level (CEO sign-off required)

### Final commercial sign-off principle

For sales decisions, Stu approves from the sales perspective (does it make sense commercially?). Kyle has **final commercial sign-off** to confirm the development side can deliver the change within budget and programme. This is not a veto on Stu's authority — it is a development-side feasibility check.

---

## Section X+2 (new) — Data Ownership Matrix

Each data concept has a single canonical home. Other sheets pull via cross-sheet formula. This matrix is the authoritative source for "where does this fact live?"

| Data concept | Canonical sheet | Editable by | Read by | Automation dependencies |
|---|---|---|---|---|
| Supplier identity | Supplier Register (000 Overview) | Kyle or designated admin | All villages' RFQ, Contract, Construction Register, H&S Monthly Indicators | Updates flow downstream via cross-sheet formulas |
| Typology specifications | Typology Register (000 Overview) | Kyle or designated admin | All villages' Unit Register | Typology field changes auto-pull |
| Unit identity (Number, Stage, Typology) | Unit Register (per village) | Matt + Kyle | Sales Register, Construction Register, all reports, Decision Log refs | Sales Status formula chain reads from here |
| Sales Status (per unit) | Sales Register (per village) | Deborah + Stu | Unit Register (formula), Dashboard, reports | Unit Register auto-pulls; cross-village rollups planned |
| Construction Status (per building) | Construction Programme (per village) | Matt | Construction Register (formula), Unit Register (formula chain), reports | Status flows downstream automatically |
| Consent Status (per building) | Construction Register (per village) | Matt | Unit Register (formula), PCG Building Consent Status report | Days to Approval derived |
| Contract Value (signed) | Contract Register (per village) | Matt + Kyle | Construction Register (formula), Project Finance | Contract Price flows to Construction Register |
| Variation Cost Impact | Variation Log (per village) | Matt, with approvals per matrix | Contract Register (SUMIFS), Construction Register (SUMIFS), reports | Variations to Date auto-aggregates in Contract Register |
| Risk identity and Score | Risk Register (per village) | Matt + Kyle accountable; anyone can raise | Dashboard, PCG Risk reports | Score and RAG formula-derived |
| Decision record | Decision Log (per village) | Anyone can raise; approvals per matrix | Dashboard, PCG Top Decisions report | Cross-functional decisions flagged |
| H&S incident detail | H&S Incidents and Observations | Matt logs; anyone can raise | H&S Monthly Indicators (COUNTIFS), Dashboard, PCG H&S reports | Monthly counts auto-aggregate |
| Monthly RAG ratings | Monthly RAG Log (per village) | Matt + Kyle for Developments arm; Stu + Deborah for Operations arm | Dashboard, PCG monthly report | Manual entry monthly |
| Budget per building | Project Finance workspace (per village budget sheet) | Julie + Kyle | Construction Register (formula pull) | Budget formula already wired |
| Building identity (Building Reference) | Construction Register (per village) | Matt + Kyle | Construction Programme, Variation Log, Contract Register | Building Reference is the cross-sheet join key |

### Architectural rule

**No fact is manually duplicated across sheets.** If a value appears in two places, exactly one is canonical and the other is a cross-sheet formula pull. Any sheet whose only role is duplicating canonical data should be evaluated for deletion.

---

## Section X+3 (additions to parked decisions)

Add these to the existing parked decisions section:

| Decision | Trigger / timing |
|---|---|
| Operations workspace (cross-village resident/maintenance work) | Conversation needed; not now |
| Cross-village role-based dashboards (GM Developments, GM Sales and Operations) | Phase 5 (after Phase 4 villages on same structure) |
| Variation threshold review | Quarterly until pattern stabilises, then annual |
| Whether QS role added to KPV (currently no QS exists; PM handles quantities) | If KPV org structure expands |
| Email-to-workflow integration (Variations first) | Phase 6 — after Phase 4 lands |

