# Smartsheet Business Plan Templates

> **For KPV work**: the sheet name examples in this file (`OPS - Active Jobs`, `OPS - Variations`, etc.) are generic. KPV's locked sheet names — `Unit Register`, `Civil and Construction Programme`, `RFQ and Quote Register`, `Contract Register`, `Variation Log`, `Resource Consent Register`, `Risk Register`, `Health and Safety Register`, `Supplier Register`, `Maintenance Register`, `Village Register`, `Build Status` — are documented in `kpv-conventions.md` §7. **Use those exact names** when working in the KPV context. The column patterns, status dropdowns, approval workflows, and dashboard widget structures below still apply — only the sheet names differ.

## Core Operational Sheet Template

| Column | Type | Purpose |
|---|---|---|
| Job Number | Text/Number | Unique identifier |
| Project Name | Text/Number | Human-readable project name |
| Client | Text/Number | Client or customer |
| Region | Dropdown | Reporting filter |
| Owner | Contact | Accountable person |
| Assigned To | Contact | Person doing the work |
| Status | Dropdown | Current state |
| Stage | Dropdown | Project/workflow stage |
| Priority | Dropdown | Low, Medium, High, Critical |
| Start Date | Date | Start date |
| Due Date | Date | Required completion date |
| Completed Date | Date | Actual completion date |
| Risk Flag | Checkbox or Dropdown | Dashboard indicator |
| Notes | Text/Number | Working notes |
| Link to Supporting Documents | Text/Number | SharePoint/OneDrive/Teams link |

## Status Dropdown Example

Use controlled statuses such as:

- Not Started
- In Progress
- Waiting on Information
- Waiting on Approval
- Blocked
- Complete
- Cancelled

Avoid vague statuses such as:

- Ongoing
- Maybe
- Sort of done
- Followed up

## Approval Sheet Template

| Column | Type | Purpose |
|---|---|---|
| Request ID | Auto-number | Unique request reference |
| Request Type | Dropdown | Variation, PO, maintenance, H&S, admin |
| Submitted By | Contact | Request originator |
| Submitted Date | Created Date | System timestamp |
| Description | Text/Number | Request detail |
| Estimated Cost | Currency | Financial impact |
| Urgency | Dropdown | Low, Medium, High, Critical |
| Approval Status | Dropdown | Draft, Submitted, L1 Approved, L2 Approved, Approved, Rejected |
| Level 1 Approver | Contact | First approver |
| Level 1 Approval Date | Date | First approval timestamp/date |
| Level 2 Approver | Contact | Second approver |
| Level 2 Approval Date | Date | Second approval timestamp/date |
| Final Approved By | Contact | Final decision maker |
| Final Approval Date | Date | Final approval date |
| Rejection Reason | Text/Number | Required if rejected |
| Approval Notes | Text/Number | Audit trail notes |

## KPI Summary Sheet Template

| Metric | Value | Target | Status | Owner | Notes |
|---|---:|---:|---|---|---|
| Open Jobs | 0 | 0 | On Track | Manager | |
| Overdue Tasks | 0 | 0 | On Track | Manager | |
| Variations Awaiting Approval | 0 | 0 | Watch | Manager | |
| H&S Incidents This Month | 0 | 0 | On Track | Manager | |
| Average Completion Days | 0 | 0 | Watch | Manager | |

## Monthly Trend Sheet Template

| Month | New Jobs | Completed Jobs | Open Jobs | Overdue Tasks | Approved Variations | H&S Incidents |
|---|---:|---:|---:|---:|---:|---:|
| Jan | 0 | 0 | 0 | 0 | 0 | 0 |
| Feb | 0 | 0 | 0 | 0 | 0 | 0 |

## Report List Template

| Report Name | Source | Purpose | Audience |
|---|---|---|---|
| RPT - My Open Tasks | Task sheets | Assigned user action list | team members |
| RPT - Overdue Tasks | Task sheets | Exception management | managers |
| RPT - Open Approvals | Approval sheets | Items waiting for approval | managers |
| RPT - Active Jobs by Stage | Active Jobs | Operations overview | operations |
| RPT - Maintenance Requests Open | Maintenance | Maintenance workflow | maintenance team |
| RPT - H&S Incidents Current Month | H&S | Safety review | leadership/H&S |

## Dashboard Widget Template

Executive dashboard:

- Title widget: dashboard name and reporting period
- Metric widgets: open jobs, overdue tasks, approvals waiting, incidents, monthly completions
- Chart widget: jobs by stage
- Chart widget: monthly completions trend
- Report widget: top overdue or high-risk items
- Report widget: open approvals
- Shortcut widget: key forms and reports
- Rich text widget: interpretation and next actions

Operations dashboard:

- Metric widgets: active jobs, blocked jobs, overdue tasks, upcoming milestones
- Chart widget: workload by owner
- Chart widget: jobs by stage or region
- Report widget: tasks due this week
- Report widget: blocked or delayed items
- Shortcut widget: operations forms

Team dashboard:

- Report widget: my assigned tasks
- Report widget: due this week
- Shortcut widget: submit request forms
- Rich text widget: weekly priorities

## Automation Register Template

| Automation Name | Source Sheet | Trigger | Condition | Action | Owner | Last Reviewed | Risk if Broken |
|---|---|---|---|---|---|---|---|
| New Request Alert | AUTO - New Requests | Row added | Request Type is not blank | Alert owner | system owner | | Missed intake |
| Approval Request L1 | Approval Sheet | Status changes | Status = Submitted | Request approval | system owner | | Approval delay |
| Overdue Reminder | Task Sheet | Daily | Due Date in past and Status not Complete | Alert Assigned To | system owner | | Tasks missed |
| Archive Closed Rows | Operational Sheet | Status changes | Status = Complete | Move row to archive | system owner | | Sheet clutter |

## Teams Mapping Template

| Teams Channel | Smartsheet Asset | Purpose |
|---|---|---|
| Leadership | DB - Executive Overview | management review |
| Operations | DB - Operations | day-to-day operations |
| Maintenance | RPT - Maintenance Requests Open | action tracking |
| Projects | RPT - Active Jobs by Stage | project oversight |
| H&S | FORM - Incident Submission and RPT - H&S Incidents | reporting and review |
