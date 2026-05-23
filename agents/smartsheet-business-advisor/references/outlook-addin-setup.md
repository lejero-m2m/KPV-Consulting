# Outlook → Smartsheet Add-in Setup (KPV)

**Audience:** KPV PMs and other team members who receive structured emails (progress, H&S figures, supplier quotes) that need to land as rows on a 107 Smartsheet.

**Why this exists:** Phase 2 build (2026-05-22) introduced four new registers on 107 Papamoa: Variation Log, RFQ and Quote Register, Contract Register, Decision Log. Combined with the existing Construction/Civil Programmes, Construction Register, H&S sheets and Sales Register, the team now has a wide intake surface. **Forms are the canonical intake for internal users** (Variation Submission, RFQ Creation) and **public form URLs are for external suppliers** (Quote Submission). The Outlook Add-in is the third intake path — for **email-borne updates from consultants, contractors, and council** that don't have a form pre-built.

> Source-of-truth caveat: the exact behaviour of the Smartsheet Outlook Add-in was last documented some years ago. Expect to verify the field-mapping flow on first use per sheet and adjust this doc accordingly.

---

## What the add-in does

The Smartsheet for Outlook add-in lives in the Outlook ribbon (desktop and web). It opens a side-panel inside an email view that lets you:

1. Pick a Smartsheet sheet you have edit access to.
2. Map fields from the email (sender, subject, received date, body) plus free-text inputs into the columns on that sheet.
3. Create a **new row** with one click, optionally attaching the email itself as a file attachment on the new row.

It does not replace forms for structured intake — it is best for emails that arrive in formats you don't fully control, where a human curates fields before saving.

---

## Install

Two paths:

**a) User-level install (no admin required)**

1. Outlook (web or desktop) → **Get Add-ins** (or **Apps** in the new Outlook ribbon).
2. Search **Smartsheet for Outlook**.
3. Add. Sign in with the KPV Smartsheet account (`kyle@karakapines.co.nz` for Kyle's PCs; PMs use their own).
4. Confirm the icon appears in the message-read ribbon.

**b) Tenant-wide deployment (KPV IT admin)**

If KPV IT prefers a centrally managed install, ask them to push it from the Microsoft 365 admin centre → **Settings → Integrated apps → Get apps → Smartsheet for Outlook**. Assign to the KPV development team group.

---

## Sheet → email mapping (107 Papamoa)

Until forms cover every intake, use the add-in for these flows:

| Incoming email | Target sheet | Notes |
|---|---|---|
| Signature Homes weekly progress email | `107 - Construction Programme` (per-building) or `107 - Construction Register` | Programme for phase-level updates (foundation/framing/etc); Register for building-level Construction Status, Practical Completion. Choose whichever the email actually updates. |
| Signature Homes monthly H&S figures (Inductions / Audits / Near Miss / MTI / LTI / LTI Days) | `107 - H and S Monthly Indicators` | One row per month. Drives `107 - PCG - H&S Monthly Indicators` report. |
| H&S incident or observation reported via email | `107 - H and S Incidents and Observations` | One row per incident/observation, with `Entry Type` set to Incident or Observation. |
| Civil contractor (Matco) progress updates | `107 - Civil Programme` | Section-level rows (100/200/.../800). |
| Council consent decisions / inspection outcomes | `107 - Construction Register` | Update `Consent Status` (PICKLIST), `Consent Approved` (date), `Building Consent Number`. The standalone Resource Consent Register was removed 2026-05-22 — consent status now lives here. |
| Supplier quote received by email (when supplier emails the quote PDF rather than using the public form) | `107 - RFQ and Quote Register` | Add as a **child row** indented under the relevant RFQ parent. Set `Type = Quote`. Reference the parent's RFQ ID. |
| Board paper / PCG minutes containing a new decision | `107 - Decision Log` | One row per decision. Set `Forum` and `Status`. Save Linked Document URL. |
| Variation request raised by Kyle or PM via email | `107 - Variation Log` | Better to use the `FORM - Variation Submission` form when it's built. Use the add-in only when the form route isn't available. |

---

## Standard workflow per email

1. Open the email in Outlook.
2. Click the Smartsheet icon in the ribbon → **Add to Smartsheet**.
3. Pick the target sheet from your recent or favourite sheets list.
4. Map fields the add-in suggests, then complete the rest manually:
   - **Primary column** (e.g. Variation Title, Decision Title, Building Reference): write a short human-readable name. Don't paste the email subject verbatim unless it's already concise.
   - **Date** columns: confirm the date — Outlook can prefill received-date which is often *not* the date you want (you usually want the date the *event* happened, not the date you read about it).
   - **Status / Picklist** columns: choose carefully — these drive downstream reports and automations.
   - **Notes** column: paste a short excerpt of the email body if helpful for future readers; full body is overkill.
5. Optional: attach the email as a file on the new row (one-click in the add-in panel). Useful for variation, quote, and decision audit trails.
6. Save. Verify the row appeared on the live sheet in a browser tab before closing the email.

---

## Sheets you should NOT add rows to via the add-in

- `107 - Unit Register` — driven by design conventions; rows here are managed by Kyle, not email-derived.
- `107 - Sales Register` — sales pipeline is managed by the sales team via Zoho CRM → Sales Register handoff.
- `107 - Civil Programme` and `107 - Construction Programme` parent rows — leave the section/building hierarchy alone; only add task children or update existing rows.
- Any sheet inside `05 - Reports Internal` or `06 - Reports External` — those are reports, not data sheets, and don't accept rows.

---

## Troubleshooting

- **Add-in doesn't appear in the ribbon:** Outlook may need a restart, or IT hasn't pushed the install — try the user-level install path above.
- **Sign-in fails:** confirm you're using your KPV Smartsheet credentials (not a personal Smartsheet account). KPV's region is North America — the sign-in screen should redirect to `app.smartsheet.com`.
- **Sheet doesn't appear in the picker:** you need edit access to that sheet. Ask Kyle to share it with you as Editor.
- **Wrong sheet picked by mistake — row created on the wrong sheet:** open the sheet in a browser, delete the row, redo on the correct sheet. There's no undo from the add-in itself.
- **Field-mapping behaviour looks wrong on first use of a sheet:** add one test row, inspect what landed where, adjust the next mapping; update this doc with what you learnt.

---

## Pattern alternatives (for reference)

- **Smartsheet form** (`FORM - …`): best for structured intake when the submitter is a known user with a Smartsheet licence or via public URL. Forms enforce field completion and picklist values.
- **Public URL form**: best for external suppliers (no Smartsheet account required). Used by `FORM - Quote Submission` for Phase 2 RFQ-and-Quote flow.
- **Power Automate**: reserved for high-volume or fully-structured email flows (e.g. inbound JSON from a council API). Not used for normal PM email at KPV — would be overkill and adds an opaque integration to maintain.
- **Outlook Add-in**: this doc.

Pick the lightest pattern that works. If volume on a particular email type grows to several per week and the format becomes predictable, escalate from add-in to form to Power Automate in that order.

---

## Update log

- 2026-05-22 — Initial creation as part of Phase 2 build. Sheet list aligned with Phase 2 state (4 new registers + existing 107 surface).
