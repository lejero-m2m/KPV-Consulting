# Smartsheet Business Plan Implementation Guide

## Design Principles

1. Business plan first
   - Assume the user has Smartsheet Business, not Enterprise.
   - Avoid Enterprise-only recommendations unless clearly marked optional.
   - Use workspace discipline, permissions, ownership registers, and naming standards as substitutes for enterprise governance tooling.

2. Layer the system
   - Intake sheets collect new data.
   - Operational sheets manage work.
   - Metrics sheets calculate KPIs.
   - Reports create filtered views.
   - Dashboards present decisions and actions.
   - Teams provides collaboration and visibility.

3. One source of truth
   - Each key data point should have one primary home.
   - Do not duplicate status, dates, owners, or approval outcomes across many sheets unless there is a deliberate reporting reason.

4. Dashboard last
   - A dashboard is only as good as the data structure behind it.
   - Build dashboard-ready data before building charts.

## Workspace Architecture

Recommended workspace set:

| Workspace | Purpose | Typical Owners |
|---|---|---|
| OPS - Operations | Active working sheets | operations manager, project managers |
| AUTO - Intake and Automations | forms, intake queues, automation staging | system owner |
| RPT - Reporting and Metrics | KPI and chart source sheets, reports | system owner, leadership |
| MGT - Management Dashboards | executive and management dashboards | leadership, system owner |
| ARCH - Archive | closed or historical rows/sheets | system owner |

## Permission Model

Use the lowest permission that lets the person do their job.

| Role | Typical Permission | Notes |
|---|---|---|
| System owner | Admin | Limit to one or two people |
| Senior manager | Editor or Admin on limited assets | Avoid broad Admin access |
| Project manager | Editor | Can update operational data |
| Site/team member | Editor or Commenter | Use reports/forms for focused access |
| External subcontractor | Form-only or Viewer | Avoid full sheet access where possible |
| Client | Viewer or published dashboard if appropriate | Only expose approved information |

## Naming Standards

Use prefixes to make assets easy to find:

- `OPS -` operational sheets
- `AUTO -` intake and automation sheets
- `RPT -` reports and metric sheets
- `DB -` dashboards
- `FORM -` forms if forms are documented separately
- `ARCH -` archive sheets

Examples:

- `OPS - Active Jobs`
- `OPS - Variations`
- `AUTO - New Maintenance Requests`
- `RPT - Overdue Tasks`
- `RPT - Executive KPI Summary`
- `DB - Executive Overview`

## Recommended Build Sequence

1. Define outcomes
   - What decisions should the dashboard support?
   - Who needs to act on the data?
   - What KPIs matter?

2. Standardize data
   - Column names
   - dropdown values
   - contact fields
   - date fields
   - naming conventions

3. Build intake
   - forms
   - required fields
   - conditional logic
   - hidden classification fields

4. Build operations
   - core working sheets
   - owners and due dates
   - status workflows
   - document links

5. Build approvals
   - approval statuses
   - approval contacts
   - timestamps
   - rejection reasons

6. Build metrics
   - KPI summary sheet
   - trend sheet
   - chart source sheet
   - helper columns

7. Build reports
   - overdue items
   - assigned-to-me
   - open approvals
   - exceptions
   - meeting reports

8. Build dashboards
   - executive
   - operations
   - team
   - project-specific where needed

9. Integrate Teams
   - add dashboards and reports as tabs
   - route key notifications to channels
   - use reports in meeting routines

10. Govern and iterate
   - automation register
   - dashboard owner
   - monthly cleanup
   - archive closed rows

## Microsoft Teams Integration

Use Teams to increase adoption.

Best practice:

- Put dashboards where people already work.
- Add executive dashboard to leadership channel.
- Add operations dashboard to operations channel.
- Add maintenance form and open request report to maintenance channel.
- Add H&S incident form and H&S report to H&S channel.
- Use alerts sparingly to avoid notification fatigue.

Avoid:

- sending every minor row update to Teams
- creating duplicate discussions in comments and Teams
- relying on Teams messages as the approval record

## Common Mistakes

- Building the dashboard before the data model.
- Letting every sheet have different status values.
- Using reports as the calculation layer.
- Giving too many people Admin access.
- Using one massive sheet for everything.
- Creating too many dashboards with overlapping information.
- Using attachments as a document management system instead of linking to SharePoint or OneDrive.
- Building large, fragile automations instead of small focused automations.
