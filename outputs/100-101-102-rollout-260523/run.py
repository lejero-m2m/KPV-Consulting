"""
100/101/102 rollout + 100/101/102/103 Build Year columns.
Brief: KPV 100/101/102 Rollout + Building Age Columns Brief (2026-05-23).
Kyle's choices: Issue1=A (clone template as-is), Issue2=A (brief folders), Issue3=A (Phase 4 AUTO_NUMBER).
"""
import json, time, openpyxl, re, sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from pathlib import Path

with open("/home/kyle/KPV-Consulting/smartsheet/input/Smartsheet API.txt") as f:
    TOKEN = f.read().strip()
HDR = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
BASE = "https://api.smartsheet.com/2.0"
OUT = Path("/home/kyle/KPV-Consulting/outputs/100-101-102-rollout-260523")

def api(method, path, body=None, override_validation=False):
    url = f"{BASE}{path}"
    if override_validation and "?" not in url:
        url += "?overrideValidation=true"
    data = json.dumps(body, default=str).encode() if body else None
    req = Request(url, data=data, headers=HDR, method=method)
    try:
        with urlopen(req) as r:
            return json.loads(r.read())
    except HTTPError as e:
        body_txt = e.read().decode()
        raise SystemExit(f"\nFATAL: HTTP {e.code} on {method} {path}\n  body: {json.dumps(body, default=str)[:400]}\n  resp: {body_txt[:500]}")

TEMPLATE_SHEETS = {
    "Unit Register":             7737437206826884,
    "Civil Programme":           3923860045909892,
    "Construction Programme":    1507473327345540,
    "Resource Consent Register": 3572291202928516,
    "RFQ and Quote Register":    896569527193476,
    "Variation Log":             6208456229867396,
}

FOLDER_NAMES = [
    "00 - Dashboards",
    "01 - Project Control",
    "02 - Civil and Construction",
    "03 - Sales and Marketing",
    "04 - Health and Safety",
    "05 - Reports Internal",
    "06 - Reports External",
]

SHEET_TO_FOLDER = {
    "Unit Register":             "01 - Project Control",
    "Civil Programme":           "02 - Civil and Construction",
    "Construction Programme":    "02 - Civil and Construction",
    "Resource Consent Register": "02 - Civil and Construction",
    "RFQ and Quote Register":    None,  # top-level
    "Variation Log":             None,  # top-level
}

VILLAGES = [
    ("100", "Regency Park"),
    ("101", "Kempton Park"),
    ("102", "Roseland Park"),
]

XLSX = "/home/kyle/KPV-Consulting/smartsheet/input/100-103-Insurance-Building-Age-260523-v01.xlsx"

# V100 refurbished units (~2020-2022) — 22 units per brief §6.3
V100_REFURB = {1,3,8,10,14,15,16,17,23,25,26,32,35,36,37,40,46,47,50,54,59,61}

report = {
    "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    "kyle_choices": {"issue1":"A clone template as-is","issue2":"A brief folders","issue3":"A Phase 4 AUTO_NUMBER pattern"},
    "villages": {},
    "v103_column_add": {},
    "anomalies": [],
}

def log(msg):
    print(msg, flush=True)

def get_columns(sid):
    r = api("GET", f"/sheets/{sid}/columns?includeAll=true")
    return r["data"]

def col_by_title(sid):
    return {c["title"]: c for c in get_columns(sid)}

# -------- per-village rollout --------
for code, name in VILLAGES:
    log(f"\n========== Village {code} - {name} ==========")
    v_rep = {"code": code, "name": name}

    # 1. Create workspace
    ws_name = f"{code} - {name}"
    log(f"Creating workspace: {ws_name}")
    ws_resp = api("POST", "/workspaces", {"name": ws_name})
    ws_id = ws_resp["result"]["id"]
    v_rep["workspace_id"] = ws_id
    log(f"  ws_id={ws_id}")

    # 2. Create folders
    log(f"Creating {len(FOLDER_NAMES)} folders…")
    folder_ids = {}
    for fname in FOLDER_NAMES:
        fr = api("POST", f"/workspaces/{ws_id}/folders", {"name": fname})
        folder_ids[fname] = fr["result"]["id"]
    v_rep["folder_ids"] = folder_ids
    log(f"  folders created: {list(folder_ids.values())}")

    # 3. Clone sheets
    log(f"Cloning {len(TEMPLATE_SHEETS)} sheets…")
    sheet_ids = {}
    for sname, src_id in TEMPLATE_SHEETS.items():
        new_name = f"{code} - {sname}"
        folder_name = SHEET_TO_FOLDER[sname]
        if folder_name:
            dest_id = folder_ids[folder_name]
            dest_type = "folder"
        else:
            dest_id = ws_id
            dest_type = "workspace"
        cr = api("POST", f"/sheets/{src_id}/copy?include=filters,forms",
                 {"destinationType": dest_type, "destinationId": dest_id, "newName": new_name})
        sheet_ids[sname] = cr["result"]["id"]
        log(f"  {new_name} -> {sheet_ids[sname]}  (in {folder_name or 'top-level'})")
    v_rep["sheet_ids"] = sheet_ids

    # 4. AUTO_NUMBER updates
    log("Configuring AUTO_NUMBER on RFQ, Variation Log, Resource Consent Register…")
    autonum_log = {}

    # 4a. RFQ Register — update Auto # fill to 0000, update RFQ Number formula
    rfq_sid = sheet_ids["RFQ and Quote Register"]
    rfq_cols = col_by_title(rfq_sid)
    auto_col = rfq_cols["Auto #"]
    rfq_num_col = rfq_cols["RFQ Number"]
    api("PUT", f"/sheets/{rfq_sid}/columns/{auto_col['id']}", {
        "type": "TEXT_NUMBER",
        "systemColumnType": "AUTO_NUMBER",
        "autoNumberFormat": {"prefix": "", "fill": "0000", "suffix": ""},
    })
    api("PUT", f"/sheets/{rfq_sid}/columns/{rfq_num_col['id']}", {
        "type": "TEXT_NUMBER",
        "formula": f'="{code}-RFQ-" + [Auto #]@row',
    })
    autonum_log["RFQ"] = f"{code}-RFQ-0001 (via formula + Auto# fill=0000)"

    # 4b. Variation Log — convert Auto # to AUTO_NUMBER (was plain TEXT_NUMBER), add VAR ID formula
    var_sid = sheet_ids["Variation Log"]
    var_cols = col_by_title(var_sid)
    api("PUT", f"/sheets/{var_sid}/columns/{var_cols['Auto #']['id']}", {
        "type": "TEXT_NUMBER",
        "systemColumnType": "AUTO_NUMBER",
        "autoNumberFormat": {"prefix": "", "fill": "0000", "suffix": ""},
    })
    api("PUT", f"/sheets/{var_sid}/columns/{var_cols['VAR ID']['id']}", {
        "type": "TEXT_NUMBER",
        "formula": f'="{code}-VAR-" + [Auto #]@row',
    })
    autonum_log["VAR"] = f"{code}-VAR-0001 (via formula + Auto# AUTO_NUMBER 0000)"

    # 4c. Resource Consent Register — convert Consent Reference (primary, plain TEXT) to AUTO_NUMBER directly
    rc_sid = sheet_ids["Resource Consent Register"]
    rc_cols = col_by_title(rc_sid)
    api("PUT", f"/sheets/{rc_sid}/columns/{rc_cols['Consent Reference']['id']}", {
        "type": "TEXT_NUMBER",
        "systemColumnType": "AUTO_NUMBER",
        "autoNumberFormat": {"prefix": f"{code}-RC-", "fill": "0000", "suffix": ""},
    })
    autonum_log["RC"] = f"{code}-RC-0001 (direct AUTO_NUMBER on primary)"
    v_rep["autonumber"] = autonum_log
    log(f"  {autonum_log}")

    # 5. Village formula column — template has no Village col, skip per brief §4.5
    v_rep["village_formula"] = "skipped: template Unit Register has no Village column (per brief §4.5)"

    # 6. Add 2 new columns to Unit Register
    log("Adding Approx Build Year + Year of Refurbishment columns to Unit Register…")
    ur_sid = sheet_ids["Unit Register"]
    ur_cols_pre = get_columns(ur_sid)
    last_idx = max(c["index"] for c in ur_cols_pre)
    add_resp = api("POST", f"/sheets/{ur_sid}/columns", [
        {"title": "Approx Build Year", "type": "TEXT_NUMBER", "index": last_idx + 1},
        {"title": "Year of Refurbishment", "type": "TEXT_NUMBER", "index": last_idx + 2},
    ])
    aby_col_id = next(c["id"] for c in add_resp["result"] if c["title"] == "Approx Build Year")
    yor_col_id = next(c["id"] for c in add_resp["result"] if c["title"] == "Year of Refurbishment")
    v_rep["new_columns"] = {"Approx Build Year": aby_col_id, "Year of Refurbishment": yor_col_id}
    log(f"  Approx Build Year col_id={aby_col_id}")
    log(f"  Year of Refurbishment col_id={yor_col_id}")

    # 7. Populate unit rows from XLSX
    log(f"Reading XLSX village sheet {code}…")
    wb = openpyxl.load_workbook(XLSX, data_only=True)
    sheet_name = None
    for sn in wb.sheetnames:
        if sn.startswith(f"{code} -") or sn.startswith(f"{code} —"):
            sheet_name = sn
            break
    if not sheet_name:
        raise SystemExit(f"Could not find XLSX sheet for {code}")
    ws = wb[sheet_name]
    rows = list(ws.iter_rows(values_only=True))
    headers = list(rows[2])
    unit_col = headers.index("Unit Number")
    aby_col = headers.index("Approx Build Year")

    ur_cols_after = col_by_title(ur_sid)
    unit_number_col_id = ur_cols_after["Unit Number"]["id"]
    notes_col_id = ur_cols_after["Notes"]["id"]

    # Build row payloads
    payloads = []
    skipped_nonnumeric = []
    refurb_applied = []
    for r in rows[3:]:
        unit = r[unit_col]
        if unit is None: continue
        unit_str = str(unit).strip()
        if unit_str.upper() == "TOTAL": continue
        # Try integer for numeric units; keep string otherwise (Smartsheet preserves)
        try:
            unit_val = int(unit_str)
            is_int = True
        except:
            unit_val = unit_str
            is_int = False
            skipped_nonnumeric.append(unit_str)
        build_yr = r[aby_col]
        cells = [
            {"columnId": unit_number_col_id, "value": unit_val, "strict": False},
        ]
        if build_yr is not None:
            cells.append({"columnId": aby_col_id, "value": build_yr})
        # V100 refurb tag
        if code == "100" and is_int and unit_val in V100_REFURB:
            cells.append({"columnId": yor_col_id, "value": "~2020-2022"})
            cells.append({"columnId": notes_col_id, "value": "Refurbished per Regency register 28/07/22"})
            refurb_applied.append(unit_val)
        payloads.append({"toBottom": True, "cells": cells})

    log(f"  {len(payloads)} rows to insert (skipped TOTAL; non-numeric kept as strings: {skipped_nonnumeric})")
    inserted = 0
    BATCH = 50
    for i in range(0, len(payloads), BATCH):
        batch = payloads[i:i+BATCH]
        resp = api("POST", f"/sheets/{ur_sid}/rows?overrideValidation=true", batch)
        inserted += len(resp.get("result", []))
        log(f"    batch {i//BATCH + 1}: +{len(resp.get('result', []))}  (total {inserted})")
    v_rep["unit_rows_inserted"] = inserted
    v_rep["non_numeric_unit_ids"] = skipped_nonnumeric
    v_rep["v100_refurb_tagged"] = sorted(refurb_applied) if code == "100" else None
    if code == "100":
        missing_refurb = sorted(V100_REFURB - set(refurb_applied))
        if missing_refurb:
            v_rep["v100_refurb_missing"] = missing_refurb
            report["anomalies"].append(f"V100 refurb units in brief not found in XLSX: {missing_refurb}")
    report["villages"][code] = v_rep
    log(f"Village {code} complete: {inserted} rows inserted.")

# -------- 103 column add + Build Year populate --------
log(f"\n========== 103 Woodcroft Estate column add ==========")
V103_UR = 471418012651396  # existing 103 Unit Register
ur_cols_pre = get_columns(V103_UR)
last_idx = max(c["index"] for c in ur_cols_pre)
add_resp = api("POST", f"/sheets/{V103_UR}/columns", [
    {"title": "Approx Build Year", "type": "TEXT_NUMBER", "index": last_idx + 1},
    {"title": "Year of Refurbishment", "type": "TEXT_NUMBER", "index": last_idx + 2},
])
aby103 = next(c["id"] for c in add_resp["result"] if c["title"] == "Approx Build Year")
yor103 = next(c["id"] for c in add_resp["result"] if c["title"] == "Year of Refurbishment")
log(f"  Approx Build Year col_id={aby103}")
log(f"  Year of Refurbishment col_id={yor103}")
report["v103_column_add"]["new_columns"] = {"Approx Build Year": aby103, "Year of Refurbishment": yor103}

# Read XLSX 103
wb = openpyxl.load_workbook(XLSX, data_only=True)
ws103 = wb["103 - Woodcroft Estate"]
rows103 = list(ws103.iter_rows(values_only=True))
hdr103 = list(rows103[2])
u_idx = hdr103.index("Unit Number")
y_idx = hdr103.index("Approx Build Year")
xlsx_year_by_unit = {}
for r in rows103[3:]:
    u = r[u_idx]
    if u is None: continue
    if str(u).upper() == "TOTAL": continue
    try:
        u_int = int(str(u).strip())
        xlsx_year_by_unit[u_int] = r[y_idx]
    except:
        report["anomalies"].append(f"103 XLSX non-numeric unit '{u}' — skipped")

# Fetch existing 103 rows and map unit number -> row_id
s = api("GET", f"/sheets/{V103_UR}?includeAll=true")
cols103 = {c["id"]: c["title"] for c in s["columns"]}
un_col_id = next(cid for cid, t in cols103.items() if t == "Unit Number")
row_by_unit = {}
for row in s["rows"]:
    for c in row["cells"]:
        if c["columnId"] == un_col_id:
            v = c.get("value")
            if v is None: continue
            try:
                row_by_unit[int(v)] = row["id"]
            except:
                pass

# Build PUT payload (update rows)
upd_payload = []
matched = []
unmatched_in_xlsx = []
for u, yr in xlsx_year_by_unit.items():
    if u in row_by_unit:
        upd_payload.append({"id": row_by_unit[u], "cells": [{"columnId": aby103, "value": yr}]})
        matched.append(u)
    else:
        unmatched_in_xlsx.append(u)
log(f"  103 XLSX rows: {len(xlsx_year_by_unit)}, existing 103 rows: {len(row_by_unit)}, matched: {len(matched)}")
if unmatched_in_xlsx:
    log(f"  XLSX units not in existing 103 register: {unmatched_in_xlsx}")
    report["anomalies"].append(f"103 XLSX units missing from existing 103 Unit Register: {unmatched_in_xlsx}")
existing_only = sorted(set(row_by_unit.keys()) - set(xlsx_year_by_unit.keys()))
if existing_only:
    log(f"  103 existing units not in XLSX: {existing_only}")
    report["anomalies"].append(f"103 existing register units missing from XLSX: {existing_only}")

# Execute in batches
updated = 0
BATCH = 50
for i in range(0, len(upd_payload), BATCH):
    batch = upd_payload[i:i+BATCH]
    resp = api("PUT", f"/sheets/{V103_UR}/rows?overrideValidation=true", batch)
    updated += len(resp.get("result", []))
    log(f"    update batch {i//BATCH + 1}: {len(resp.get('result', []))}  (total {updated})")
report["v103_column_add"]["rows_updated"] = updated
report["v103_column_add"]["matched_units"] = sorted(matched)
report["v103_column_add"]["xlsx_only_units"] = unmatched_in_xlsx
report["v103_column_add"]["register_only_units"] = existing_only

# -------- Write report --------
report["finished_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
out_json = OUT / "run-report.json"
out_json.write_text(json.dumps(report, indent=2, default=str))
log(f"\nReport JSON written: {out_json}")
log(f"Anomalies: {len(report['anomalies'])}")
for a in report["anomalies"]:
    log(f"  - {a}")
