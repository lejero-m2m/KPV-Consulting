"""Targeted remediation: S4-B01 (180/1-5) and S4-B03 (182/1-5).

Programme uses hyphen unit names (180-1..), Budget uses slash (180/1..).
Match with separator-normalised keys, then update the (empty) building
rows + add their 5 consolidated phase children. Only these 2 buildings.
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
NC = {"Building Reference": 7746806653161348, "Building Name": 2117307118948228,
      "Stage": 6620906746318724, "Units": 4369106932633476, "Unit Count": 8872706560003972,
      "Typology": 76613537795972, "Build Partner": 2328413351481220,
      "Building Consent Numbers": 6832012978851716, "Contract Price (incl GST)": 5706113072009092,
      "Variations (incl GST)": 3454313258323844, "% Complete": 7957912885694340,
      "RAG": 639563491217284, "Start Date": 5143163118587780,
      "Notes/Latest": 7394962932273028, "Duration": 1956236785651588}
TARGETS = {"S4-B01": (4795526636044164, "180/1, 180/2, 180/3, 180/4, 180/5", "Stage 4"),
           "S4-B03": (7047326449729412, "182/1, 182/2, 182/3, 182/4, 182/5", "Stage 4")}


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


def keynorm(u):
    """Separator-agnostic unit key: 180/1, 180-1, '180-1.0' -> '180-1'."""
    s = str(u).strip()
    if s.endswith(".0"):
        s = s[:-2]
    return s.replace("/", "-")


def to_date(s):
    return datetime.date.fromisoformat(str(s)[:10]) if s else None


def workdays(d1, d2):
    if not d1 or not d2 or d2 < d1:
        return 1
    n, d = 0, d1
    while d <= d2:
        if d.weekday() < 5:
            n += 1
        d += datetime.timedelta(days=1)
    return max(n, 1)


def main():
    rows, oc = get_all(OLD, "&include=objectValue")

    def cv(r, t):
        for c in r.get("cells", []):
            if c.get("columnId") == oc.get(t):
                return c.get("value")
        return None

    unit_by_key = {}
    kids = {}
    for r in rows:
        p = r.get("parentId")
        if p:
            kids.setdefault(p, []).append(r)
    for r in rows:
        if cv(r, "Is Unit") is True:
            unit_by_key[keynorm(cv(r, "Task Name"))] = r

    for br, (rowid, units_str, stage) in TARGETS.items():
        unums = [keynorm(t) for t in units_str.split(",") if t.strip()]
        urows = [unit_by_key[u] for u in unums if u in unit_by_key]
        miss = [u for u in unums if u not in unit_by_key]
        rags = [cv(u, "RAG") for u in urows]
        worst = RAG_INV[max([RAG_ORD.get(x, -1) for x in rags], default=-1)] if rags else None
        typ = sorted({cv(u, "Typology") for u in urows if cv(u, "Typology")})
        bcn = sorted({str(cv(u, "Building Consent Number")) for u in urows if cv(u, "Building Consent Number")})
        bp = [cv(u, "Build Partner") for u in urows if cv(u, "Build Partner")]
        bp_mode = Counter(bp).most_common(1)[0][0] if bp else None
        cprice = sum(float(cv(u, "Contract Price (incl GST)") or 0) for u in urows)
        cvar = sum(float(cv(u, "Variations (incl GST)") or 0) for u in urows)
        notes = [str(cv(u, "Notes/Latest")) for u in urows if cv(u, "Notes/Latest")]

        upd = [
            {"columnId": NC["Unit Count"], "value": len(unums)},
            {"columnId": NC["Typology"], "value": ", ".join(typ)},
            {"columnId": NC["Build Partner"], "value": bp_mode or "", "strict": False},
            {"columnId": NC["Building Consent Numbers"], "value": ", ".join(bcn)},
            {"columnId": NC["Contract Price (incl GST)"], "value": round(cprice, 2)},
            {"columnId": NC["Variations (incl GST)"], "value": round(cvar, 2)},
        ]
        if worst:
            upd.append({"columnId": NC["RAG"], "value": worst, "strict": False})
        if notes:
            upd.append({"columnId": NC["Notes/Latest"], "value": "; ".join(notes)})
        api("PUT", f"/sheets/{NEW}/rows", [{"id": rowid, "cells": upd}])

        children = []
        for ph in PHASES:
            pk = [k for u in urows for k in kids.get(u["id"], [])
                  if str(cv(k, "Task Name")).strip() == ph]
            if not pk:
                continue
            starts = [to_date(cv(k, "Start Date")) for k in pk if cv(k, "Start Date")]
            ends = [to_date(cv(k, "End Date")) for k in pk if cv(k, "End Date")]
            s = min(starts) if starts else None
            en = max(ends) if ends else None
            pcts = [cv(k, "% Complete") for k in pk if cv(k, "% Complete") is not None]
            cells = [{"columnId": NC["Building Reference"], "value": ph},
                     {"columnId": NC["Building Name"], "value": ph}]
            if s:
                cells.append({"columnId": NC["Start Date"], "value": s.isoformat()})
                cells.append({"columnId": NC["Duration"], "value": f"{workdays(s, en)}d"})
            if pcts:
                cells.append({"columnId": NC["% Complete"],
                              "value": round(round((sum(pcts) / len(pcts)) / 0.05) * 0.05, 4)})
            children.append({"parentId": rowid, "toBottom": True, "cells": cells})
        r = api("POST", f"/sheets/{NEW}/rows", children) if children else {"result": []}
        print(f"{br}: urows={len(urows)} miss={miss} children_added={len(r['result'])} RAG={worst} "
              f"cprice={cprice:.0f}")


if __name__ == "__main__":
    main()
