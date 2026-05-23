"""Continuation after V100 RC AUTO_NUMBER failure.
Uses formula-helper pattern for Resource Consent Register (primary col can't be AUTO_NUMBER).
- Finishes V100 from RC step onwards
- Does V101 + V102 in full
- Does V103 column-add + row update
"""
import json, time, openpyxl, sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from pathlib import Path

with open("/home/kyle/KPV-Consulting/smartsheet/input/Smartsheet API.txt") as f:
    TOKEN = f.read().strip()
HDR = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
BASE = "https://api.smartsheet.com/2.0"
OUT = Path("/home/kyle/KPV-Consulting/outputs/100-101-102-rollout-260523")

def api(method, path, body=None):
    data = json.dumps(body, default=str).encode() if body else None
    req = Request(f"{BASE}{path}", data=data, headers=HDR, method=method)
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
    "00 - Dashboards","01 - Project Control","02 - Civil and Construction",
    "03 - Sales and Marketing","04 - Health and Safety",
    "05 - Reports Internal","06 - Reports External",
]
SHEET_TO_FOLDER = {
    "Unit Register":"01 - Project Control",
    "Civil Programme":"02 - Civil and Construction",
    "Construction Programme":"02 - Civil and Construction",
    "Resource Consent Register":"02 - Civil and Construction",
    "RFQ and Quote Register":None,"Variation Log":None,
}
XLSX = "/home/kyle/KPV-Consulting/smartsheet/input/100-103-Insurance-Building-Age-260523-v01.xlsx"
V100_REFURB = {1,3,8,10,14,15,16,17,23,25,26,32,35,36,37,40,46,47,50,54,59,61}

def log(m): print(m, flush=True)

def get_cols(sid): return api("GET", f"/sheets/{sid}/columns?includeAll=true")["data"]
def col_by_title(sid): return {c["title"]: c for c in get_cols(sid)}

# === V100 — already partial. Pull what we have, finish the rest. ===
V100_STATE = {
    "code":"100","name":"Regency Park",
    "workspace_id":3978690771085188,
    "folder_ids":{
        "00 - Dashboards":2665635709773700,
        "01 - Project Control":1539735802931076,
        "02 - Civil and Construction":6043335430301572,
        "03 - Sales and Marketing":8295135243986820,
        "04 - Health and Safety":976785849509764,
        "05 - Reports Internal":5480385476880260,
        "06 - Reports External":2102685756352388,
    },
    "sheet_ids":{
        "Unit Register":5351643322208132,
        "Civil Programme":3483843649556356,
        "Construction Programme":2852960198414212,
        "Resource Consent Register":3792673272975236,
        "RFQ and Quote Register":2551176468844420,
        "Variation Log":7987443276926852,
    },
    "autonumber":{
        "RFQ":"100-RFQ-0001 (via formula + Auto# fill=0000)",
        "VAR":"100-VAR-0001 (via formula + Auto# AUTO_NUMBER 0000)",
        # RC still to do
    },
    "village_formula":"skipped: template Unit Register has no Village column (per brief §4.5)",
}

report = {
    "started_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    "kyle_choices":{"issue1":"A clone template","issue2":"A brief folders","issue3":"A Phase 4 AUTO_NUMBER (formula-helper for RC primary per HTTP1057 workaround)"},
    "villages":{},
    "v103_column_add":{},
    "anomalies":[],
}

def setup_rc_autonum(rc_sid, code):
    """RC primary can't be AUTO_NUMBER (err 1057). Add Auto # helper + formula on primary. Idempotent."""
    rc_cols = col_by_title(rc_sid)
    if "Auto #" not in rc_cols:
        api("POST", f"/sheets/{rc_sid}/columns", [{
            "title": "Auto #", "type": "TEXT_NUMBER",
            "systemColumnType": "AUTO_NUMBER",
            "autoNumberFormat":{"prefix":"","fill":"0000","suffix":""},
            "index": 1,
        }])
    cr_col = rc_cols["Consent Reference"]
    if cr_col.get("formula") != f'="{code}-RC-" + [Auto #]@row':
        api("PUT", f"/sheets/{rc_sid}/columns/{cr_col['id']}", {
            "type":"TEXT_NUMBER",
            "formula": f'="{code}-RC-" + [Auto #]@row',
        })
    return f"{code}-RC-0001 (formula on primary + Auto# helper col)"

def add_build_year_cols(ur_sid):
    cols_pre = get_cols(ur_sid)
    by_title = {c["title"]: c for c in cols_pre}
    if "Approx Build Year" in by_title and "Year of Refurbishment" in by_title:
        return by_title["Approx Build Year"]["id"], by_title["Year of Refurbishment"]["id"]
    next_idx = max(c["index"] for c in cols_pre) + 1
    new_cols = []
    aby = by_title.get("Approx Build Year", {}).get("id")
    yor = by_title.get("Year of Refurbishment", {}).get("id")
    if not aby:
        resp = api("POST", f"/sheets/{ur_sid}/columns", [{"title":"Approx Build Year","type":"TEXT_NUMBER","index":next_idx}])
        aby = resp["result"][0]["id"]
    if not yor:
        next_idx2 = max(c["index"] for c in get_cols(ur_sid)) + 1
        resp = api("POST", f"/sheets/{ur_sid}/columns", [{"title":"Year of Refurbishment","type":"TEXT_NUMBER","index":next_idx2}])
        yor = resp["result"][0]["id"]
    return aby, yor

def populate_units(code, ur_sid, aby_col_id, yor_col_id):
    wb = openpyxl.load_workbook(XLSX, data_only=True)
    sheet_name = next(sn for sn in wb.sheetnames if sn.startswith(f"{code} -") or sn.startswith(f"{code} —"))
    ws = wb[sheet_name]
    rows = list(ws.iter_rows(values_only=True))
    headers = list(rows[2])
    u_idx = headers.index("Unit Number")
    y_idx = headers.index("Approx Build Year")
    ur_cols = col_by_title(ur_sid)
    un_id = ur_cols["Unit Number"]["id"]
    notes_id = ur_cols["Notes"]["id"]

    payloads = []
    nonnum = []
    refurb = []
    for r in rows[3:]:
        u = r[u_idx]
        if u is None: continue
        us = str(u).strip()
        if us.upper()=="TOTAL": continue
        try:
            uval = int(us); is_int = True
        except:
            uval = us; is_int = False; nonnum.append(us)
        cells = [{"columnId":un_id,"value":uval,"strict":False}]
        by = r[y_idx]
        if by is not None:
            cells.append({"columnId":aby_col_id,"value":by})
        if code=="100" and is_int and uval in V100_REFURB:
            cells.append({"columnId":yor_col_id,"value":"~2020-2022"})
            cells.append({"columnId":notes_id,"value":"Refurbished per Regency register 28/07/22"})
            refurb.append(uval)
        payloads.append({"toBottom":True,"cells":cells})

    inserted = 0
    BATCH=50
    for i in range(0, len(payloads), BATCH):
        resp = api("POST", f"/sheets/{ur_sid}/rows?overrideValidation=true", payloads[i:i+BATCH])
        n = len(resp.get("result",[]))
        inserted += n
        log(f"    batch {i//BATCH+1}: +{n} (total {inserted})")
    return inserted, nonnum, refurb

# === Finish V100 ===
log("\n========== V100 — finishing from RC step ==========")
v100 = V100_STATE
rc_sid = v100["sheet_ids"]["Resource Consent Register"]
v100["autonumber"]["RC"] = setup_rc_autonum(rc_sid, "100")
log(f"  RC AUTO_NUMBER: {v100['autonumber']['RC']}")

ur_sid = v100["sheet_ids"]["Unit Register"]
aby, yor = add_build_year_cols(ur_sid)
v100["new_columns"] = {"Approx Build Year": aby, "Year of Refurbishment": yor}
log(f"  Unit Register cols: ABY={aby} YOR={yor}")

log("Populating 100 unit rows…")
inserted, nonnum, refurb = populate_units("100", ur_sid, aby, yor)
v100["unit_rows_inserted"] = inserted
v100["non_numeric_unit_ids"] = nonnum
v100["v100_refurb_tagged"] = sorted(refurb)
missing = sorted(V100_REFURB - set(refurb))
if missing:
    v100["v100_refurb_missing"] = missing
    report["anomalies"].append(f"V100 refurb units not found in XLSX: {missing}")
report["villages"]["100"] = v100
log(f"V100 complete: {inserted} rows inserted, {len(refurb)} refurb tagged.")

# === V101 + V102 — full rollout ===
for code, name in [("101","Kempton Park"),("102","Roseland Park")]:
    log(f"\n========== V{code} - {name} ==========")
    v = {"code":code,"name":name}
    ws_name = f"{code} - {name}"
    log(f"Creating workspace: {ws_name}")
    ws_id = api("POST","/workspaces",{"name":ws_name})["result"]["id"]
    v["workspace_id"] = ws_id
    log(f"  ws_id={ws_id}")

    folder_ids = {}
    for fn in FOLDER_NAMES:
        folder_ids[fn] = api("POST", f"/workspaces/{ws_id}/folders", {"name":fn})["result"]["id"]
    v["folder_ids"] = folder_ids
    log(f"  folders: {list(folder_ids.values())}")

    sheet_ids = {}
    for sn, src in TEMPLATE_SHEETS.items():
        fname = SHEET_TO_FOLDER[sn]
        dt, di = ("folder", folder_ids[fname]) if fname else ("workspace", ws_id)
        new = f"{code} - {sn}"
        sheet_ids[sn] = api("POST", f"/sheets/{src}/copy?include=filters,forms",
                            {"destinationType":dt,"destinationId":di,"newName":new})["result"]["id"]
        log(f"  {new} -> {sheet_ids[sn]} ({fname or 'top'})")
    v["sheet_ids"] = sheet_ids

    # AUTO_NUMBER setup
    log("AUTO_NUMBER…")
    autonum = {}
    rfq_sid = sheet_ids["RFQ and Quote Register"]
    rfq_cols = col_by_title(rfq_sid)
    api("PUT", f"/sheets/{rfq_sid}/columns/{rfq_cols['Auto #']['id']}", {
        "type":"TEXT_NUMBER","systemColumnType":"AUTO_NUMBER",
        "autoNumberFormat":{"prefix":"","fill":"0000","suffix":""},
    })
    api("PUT", f"/sheets/{rfq_sid}/columns/{rfq_cols['RFQ Number']['id']}", {
        "type":"TEXT_NUMBER","formula":f'="{code}-RFQ-" + [Auto #]@row',
    })
    autonum["RFQ"] = f"{code}-RFQ-0001"

    var_sid = sheet_ids["Variation Log"]
    var_cols = col_by_title(var_sid)
    api("PUT", f"/sheets/{var_sid}/columns/{var_cols['Auto #']['id']}", {
        "type":"TEXT_NUMBER","systemColumnType":"AUTO_NUMBER",
        "autoNumberFormat":{"prefix":"","fill":"0000","suffix":""},
    })
    api("PUT", f"/sheets/{var_sid}/columns/{var_cols['VAR ID']['id']}", {
        "type":"TEXT_NUMBER","formula":f'="{code}-VAR-" + [Auto #]@row',
    })
    autonum["VAR"] = f"{code}-VAR-0001"

    rc_sid = sheet_ids["Resource Consent Register"]
    autonum["RC"] = setup_rc_autonum(rc_sid, code)
    v["autonumber"] = autonum
    log(f"  {autonum}")
    v["village_formula"] = "skipped: template has no Village column (brief §4.5)"

    ur_sid = sheet_ids["Unit Register"]
    aby, yor = add_build_year_cols(ur_sid)
    v["new_columns"] = {"Approx Build Year":aby,"Year of Refurbishment":yor}
    log(f"  Unit Register cols: ABY={aby} YOR={yor}")

    log(f"Populating {code} unit rows…")
    inserted, nonnum, _ = populate_units(code, ur_sid, aby, yor)
    v["unit_rows_inserted"] = inserted
    v["non_numeric_unit_ids"] = nonnum
    v["v100_refurb_tagged"] = None
    report["villages"][code] = v
    log(f"V{code} complete: {inserted} rows inserted.")

# === V103 column add + populate ===
log("\n========== V103 — column add + Build Year populate ==========")
V103_UR = 471418012651396
aby3, yor3 = add_build_year_cols(V103_UR)
report["v103_column_add"]["new_columns"] = {"Approx Build Year":aby3,"Year of Refurbishment":yor3}
log(f"  103 cols: ABY={aby3} YOR={yor3}")

wb = openpyxl.load_workbook(XLSX, data_only=True)
ws103 = wb["103 - Woodcroft Estate"]
rows103 = list(ws103.iter_rows(values_only=True))
hdr = list(rows103[2])
u_idx = hdr.index("Unit Number")
y_idx = hdr.index("Approx Build Year")
xlsx_by_unit = {}
for r in rows103[3:]:
    u = r[u_idx]
    if u is None: continue
    if str(u).upper()=="TOTAL": continue
    try: xlsx_by_unit[int(str(u).strip())] = r[y_idx]
    except: report["anomalies"].append(f"103 XLSX non-numeric unit: {u}")

s = api("GET", f"/sheets/{V103_UR}?includeAll=true")
cols103 = {c["id"]:c["title"] for c in s["columns"]}
un_col = next(cid for cid,t in cols103.items() if t=="Unit Number")
row_by_unit = {}
for row in s["rows"]:
    for c in row["cells"]:
        if c["columnId"]==un_col:
            v = c.get("value")
            if v is None: continue
            try: row_by_unit[int(v)] = row["id"]
            except: pass

upd, matched, xlsx_only = [], [], []
for u, yr in xlsx_by_unit.items():
    if u in row_by_unit:
        upd.append({"id":row_by_unit[u],"cells":[{"columnId":aby3,"value":yr}]})
        matched.append(u)
    else:
        xlsx_only.append(u)
existing_only = sorted(set(row_by_unit) - set(xlsx_by_unit))
log(f"  XLSX units: {len(xlsx_by_unit)}, existing rows: {len(row_by_unit)}, matched: {len(matched)}")
if xlsx_only: log(f"  XLSX-only: {xlsx_only}"); report["anomalies"].append(f"103 XLSX-only units: {xlsx_only}")
if existing_only: log(f"  existing-only: {existing_only}"); report["anomalies"].append(f"103 register-only units: {existing_only}")

updated = 0
BATCH=50
for i in range(0,len(upd),BATCH):
    resp = api("PUT", f"/sheets/{V103_UR}/rows?overrideValidation=true", upd[i:i+BATCH])
    updated += len(resp.get("result",[]))
    log(f"    update batch {i//BATCH+1}: +{len(resp.get('result',[]))}")
report["v103_column_add"]["rows_updated"] = updated
report["v103_column_add"]["matched_units"] = sorted(matched)
report["v103_column_add"]["xlsx_only_units"] = xlsx_only
report["v103_column_add"]["register_only_units"] = existing_only

report["finished_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
(OUT/"run-report.json").write_text(json.dumps(report, indent=2, default=str))
log(f"\nDONE. Anomalies: {len(report['anomalies'])}")
for a in report["anomalies"]:
    log(f"  - {a}")
