"""Phase 2b.2 — populate the new per-building Programme.

Consolidation rules (Kyle, Checkpoint 2a):
  - one set of 5 phase sub-tasks per building
  - per phase across the building's units: Start=earliest, End=latest,
    %Complete=avg rounded to nearest 5%, RAG=worst, Notes concatenated
  - building parent rows roll up dates/% from children (Gantt); RAG set explicitly (worst)
  - unit 402 folds into S3-B15

Dependency-enabled target: leaf rows get Start + Duration (End auto-computes;
direct End writes are rejected with 1080). Parent dates/Duration auto-roll-up.

Sequence (error 1123 = one parentId per add_rows call):
  1. add all building rows in one call (top-level) -> capture ids by BR
  2. per building, add its <=5 phase children (parentId = building row id)
"""
import json, urllib.request, datetime
from collections import Counter

TOKEN = open("/home/kyle/KPV-Consulting/smartsheet/input/Smartsheet API.txt").read().strip()
OLD = 5063906232848260
NEW = 4820480841174916
PHASES = ["Foundation and slab", "Framing and roof structure",
          "Cladding and weathertight", "Internal fitout", "Practical completion"]
RAG_ORD = {None: -1, "Gray": 0, "Green": 1, "Yellow": 2, "Red": 3}
RAG_INV = {v: k for k, v in RAG_ORD.items()}

NC = {  # new sheet column ids
    "Building Reference": 7746806653161348, "Building Name": 2117307118948228,
    "Stage": 6620906746318724, "Units": 4369106932633476, "Unit Count": 8872706560003972,
    "Typology": 76613537795972, "Construction Status": 4580213165166468,
    "Build Partner": 2328413351481220, "Building Consent Numbers": 6832012978851716,
    "Contract Package": 1202513444638596, "Contract Price (incl GST)": 5706113072009092,
    "Variations (incl GST)": 3454313258323844, "% Complete": 7957912885694340,
    "RAG": 639563491217284, "Start Date": 5143163118587780, "End Date": 2891363304902532,
    "Notes/Latest": 7394962932273028, "Budget Approved": 1765463398059908,
    "Expected Total Cost": 6269063025430404, "Expected Variance": 4017263211745156,
    "Predecessors": 7585736319864708, "Duration": 1956236785651588,
}


def api(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request("https://api.smartsheet.com/2.0" + path, data=data, method=method)
    r.add_header("Authorization", "Bearer " + TOKEN)
    r.add_header("Content-Type", "application/json")
    return json.loads(urllib.request.urlopen(r).read())


def get_all(sid, extra=""):
    rows, pg = [], 1
    while True:
        d = api("GET", f"/sheets/{sid}?pageSize=500&page={pg}{extra}")
        rows += d["rows"]
        if len(rows) >= d["totalRowCount"]:
            return rows, {c["title"]: c["id"] for c in d["columns"]}
        pg += 1


def norm(u):
    return str(u).strip().split(".0")[0].strip() if u is not None else ""


def to_date(s):
    if not s:
        return None
    return datetime.date.fromisoformat(str(s)[:10])


def workdays(d1, d2):
    if not d1 or not d2 or d2 < d1:
        return 1
    n = 0
    d = d1
    while d <= d2:
        if d.weekday() < 5:
            n += 1
        d += datetime.timedelta(days=1)
    return max(n, 1)


def round5pct(vals):
    vals = [v for v in vals if v is not None]
    if not vals:
        return None
    avg = sum(vals) / len(vals)
    return round(avg / 0.05) * 0.05


def main():
    rows, oc = get_all(OLD, "&include=objectValue")

    def cv(r, t):
        for c in r.get("cells", []):
            if c.get("columnId") == oc.get(t):
                return c.get("value")
        return None

    unit_by_num = {}
    kids = {}
    for r in rows:
        p = r.get("parentId")
        if p:
            kids.setdefault(p, []).append(r)
    for r in rows:
        if cv(r, "Is Unit") is True:
            unit_by_num[norm(cv(r, "Task Name"))] = r

    mp = json.load(open("/home/kyle/KPV-Consulting/plans/107-per-building-migration/mapping.json"))
    brmap = mp["building_reference_mapping"]

    building_rows, building_children, report = [], {}, []
    for e in brmap:
        br = e["building_reference"]
        units_str = e.get("units")
        stage = e["register_stage"]
        # resolve unit numbers
        if units_str:
            unums = [norm(t) for t in str(units_str).split(",") if t.strip()]
        else:
            unums = []
        urows = [unit_by_num[u] for u in unums if u in unit_by_num]
        missing = [u for u in unums if u not in unit_by_num]

        # building-level aggregates
        rags = [cv(u, "RAG") for u in urows]
        worst = RAG_INV[max([RAG_ORD.get(x, -1) for x in rags], default=-1)] if rags else None
        typ = sorted({cv(u, "Typology") for u in urows if cv(u, "Typology")})
        bcn = sorted({str(cv(u, "Building Consent Number")) for u in urows if cv(u, "Building Consent Number")})
        bp = [cv(u, "Build Partner") for u in urows if cv(u, "Build Partner")]
        bp_mode = Counter(bp).most_common(1)[0][0] if bp else None
        cprice = sum(float(cv(u, "Contract Price (incl GST)") or 0) for u in urows)
        cvar = sum(float(cv(u, "Variations (incl GST)") or 0) for u in urows)
        notes = [str(cv(u, "Notes/Latest")) for u in urows if cv(u, "Notes/Latest")]

        cells = [
            {"columnId": NC["Building Reference"], "value": br},
            {"columnId": NC["Building Name"], "value": f"Building {units_str}" if units_str else "Pavilion"},
            {"columnId": NC["Stage"], "value": stage, "strict": False},
            {"columnId": NC["Units"], "value": units_str or ""},
            {"columnId": NC["Unit Count"], "value": len(unums)},
            {"columnId": NC["Typology"], "value": ", ".join(typ)},
            {"columnId": NC["Build Partner"], "value": bp_mode or "", "strict": False},
            {"columnId": NC["Building Consent Numbers"], "value": ", ".join(bcn)},
            {"columnId": NC["Contract Price (incl GST)"], "value": round(cprice, 2)},
            {"columnId": NC["Variations (incl GST)"], "value": round(cvar, 2)},
            {"columnId": NC["RAG"], "value": worst, "strict": False} if worst else None,
            {"columnId": NC["Notes/Latest"], "value": "; ".join(notes)} if notes else None,
        ]
        cells = [c for c in cells if c]
        building_rows.append({"_br": br, "toBottom": True, "cells": cells})

        # per-phase consolidation
        ph_rows = []
        for ph in PHASES:
            ph_kids = []
            for u in urows:
                for k in kids.get(u["id"], []):
                    if str(cv(k, "Task Name")).strip() == ph:
                        ph_kids.append(k)
            if not ph_kids:
                continue
            starts = [to_date(cv(k, "Start Date")) for k in ph_kids]
            ends = [to_date(cv(k, "End Date")) for k in ph_kids]
            starts = [d for d in starts if d]
            ends = [d for d in ends if d]
            s = min(starts) if starts else None
            en = max(ends) if ends else None
            pcts = [cv(k, "% Complete") for k in ph_kids]
            pc = round5pct(pcts)
            pn = [str(cv(k, "Notes/Latest")) for k in ph_kids if cv(k, "Notes/Latest")]
            pc_cells = [
                {"columnId": NC["Building Reference"], "value": ph},
                {"columnId": NC["Building Name"], "value": ph},
            ]
            if s:
                pc_cells.append({"columnId": NC["Start Date"], "value": s.isoformat()})
                pc_cells.append({"columnId": NC["Duration"], "value": f"{workdays(s, en)}d"})
            if pc is not None:
                pc_cells.append({"columnId": NC["% Complete"], "value": round(pc, 4)})
            if pn:
                pc_cells.append({"columnId": NC["Notes/Latest"], "value": "; ".join(pn)})
            ph_rows.append({"toBottom": True, "cells": pc_cells})
        building_children[br] = ph_rows

        report.append(f'{br:<9} units={units_str!r:24} urows={len(urows)} '
                      f'phases={len(ph_rows)} RAG={worst} miss={missing}')

    # 1) add all building rows (top-level) in one call
    res = api("POST", f"/sheets/{NEW}/rows", [{k: v for k, v in r.items() if k != "_br"} for r in building_rows])
    br_to_id = {}
    for src, got in zip(building_rows, res["result"]):
        br_to_id[src["_br"]] = got["id"]

    # 2) per building, add its phase children
    total_children = 0
    for br, children in building_children.items():
        if not children:
            continue
        pid = br_to_id[br]
        for ch in children:
            ch["parentId"] = pid
        r = api("POST", f"/sheets/{NEW}/rows", children)
        total_children += len(r["result"])

    print(f"building rows added: {len(br_to_id)}")
    print(f"phase child rows added: {total_children}")
    print("\n".join(report))

    mp["new_programme"]["building_row_ids"] = br_to_id
    mp["new_programme"]["children_added"] = total_children
    mp["_meta"]["status"] = f"Phase 2b.2 done — {len(br_to_id)} buildings + {total_children} sub-tasks populated; pre-Checkpoint-2b.4"
    json.dump(mp, open("/home/kyle/KPV-Consulting/plans/107-per-building-migration/mapping.json", "w"), indent=2)


if __name__ == "__main__":
    main()
