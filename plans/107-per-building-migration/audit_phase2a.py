"""Phase 2a (READ-ONLY): Programme dependency audit.

Pulls all Programme rows, maps predecessors/dependents/children for unit
rows, finds orphans, and identifies cross-sheet consumers of the Programme.
Writes phase_2a_audit.md. NO writes. Stops at Checkpoint 2a.
"""
import json, urllib.request

TOKEN = open("/home/kyle/KPV-Consulting/smartsheet/input/Smartsheet API.txt").read().strip()
PROG = 5063906232848260
CONSUMERS = {
    "107 - Construction Register": 2635310868418436,
    "107 - Unit Register": 5289542339743620,
    "107 - Papamoa Budget": 5631895457976196,
    "107 - Civil Programme": 6233992763232132,
    "107 - Resource Consent Register": 1643703515959172,
}


def api(path):
    r = urllib.request.Request("https://api.smartsheet.com/2.0" + path)
    r.add_header("Authorization", "Bearer " + TOKEN)
    return json.loads(urllib.request.urlopen(r).read())


def get_all_rows(sid, extra=""):
    rows, page, cols = [], 1, None
    while True:
        d = api(f"/sheets/{sid}?pageSize=500&page={page}{extra}")
        batch = d.get("rows", [])
        rows += batch
        cols = d["columns"]
        total = d.get("totalRowCount", len(rows))
        if len(rows) >= total or not batch:
            return rows, cols
        page += 1


def main():
    rows, cols = get_all_rows(PROG, "&include=objectValue")
    cmap = {c["title"]: c["id"] for c in cols}

    def cell(row, title):
        for c in row.get("cells", []):
            if c.get("columnId") == cmap.get(title):
                return c
        return {}

    by_id = {r["id"]: r for r in rows}
    # children counts
    child_count = {}
    for r in rows:
        p = r.get("parentId")
        if p:
            child_count[p] = child_count.get(p, 0) + 1

    units = []
    for r in rows:
        isu = cell(r, "Is Unit").get("value")
        if isu is True:
            units.append(r)

    # predecessor extraction
    def preds(r):
        c = cell(r, "Predecessors")
        ov = c.get("objectValue") or {}
        out = []
        for p in ov.get("predecessors", []):
            out.append(p.get("rowId"))
        return [x for x in out if x]

    unit_ids = {r["id"] for r in units}
    # dependents: map predecessor target -> list of rows depending on it
    dependents = {}
    for r in rows:
        for tgt in preds(r):
            dependents.setdefault(tgt, []).append(r["id"])

    units_with_preds, units_are_preds, units_with_children, orphans = [], [], [], []
    for r in units:
        tn = cell(r, "Task Name").get("value")
        st = cell(r, "Stage").get("value")
        ps = preds(r)
        if ps:
            up = [(p, p in unit_ids) for p in ps]
            units_with_preds.append((tn, r["id"], up))
        if r["id"] in dependents:
            units_are_preds.append((tn, r["id"], dependents[r["id"]]))
        if child_count.get(r["id"], 0) > 0:
            units_with_children.append((tn, r["id"], child_count[r["id"]]))
        if st in (None, "", " "):
            orphans.append((tn, r["id"], "missing Stage"))

    # cross-sheet consumers of Programme
    xsheet_consumers = []
    for name, sid in CONSUMERS.items():
        d = api(f"/sheets/{sid}?pageSize=1&include=crossSheetReferences")
        for x in d.get("crossSheetReferences", []):
            if x.get("sourceSheetId") == PROG:
                xsheet_consumers.append((name, sid, x.get("name")))

    # reports referencing Programme (browse 05/06 report folders)
    report_consumers = []
    for fid in (1382941310904196, 6714388368385924):
        try:
            fl = api(f"/folders/{fid}?include=reports") if False else None
        except Exception:
            pass
    # use sights/reports listing via workspace browse instead
    try:
        ws = api("/workspaces/4481862027503492?loadAll=true")
        def walk(node):
            for rep in node.get("reports", []):
                rd = api(f"/reports/{rep['id']}?include=sourceSheets&pageSize=1")
                for s in rd.get("sourceSheets", []) or []:
                    if s.get("id") == PROG:
                        report_consumers.append((rep.get("name"), rep["id"]))
            for f in node.get("folders", []):
                walk(f)
        walk(ws)
    except Exception as e:
        report_consumers.append(("(report scan error: %s)" % e, None))

    L = []
    L.append("# Phase 2a — Programme Dependency Audit\n")
    L.append(f"Programme sheet `{PROG}` — total rows: **{len(rows)}**\n")
    L.append(f"- Unit rows (Is Unit = true): **{len(units)}** (brief expects 114)")
    L.append(f"- Non-unit task/milestone rows: **{len(rows) - len(units)}**")
    L.append(f"- Unit rows WITH predecessors: **{len(units_with_preds)}**")
    L.append(f"- Unit rows that ARE predecessors to other rows: **{len(units_are_preds)}**")
    L.append(f"- Unit rows WITH children: **{len(units_with_children)}**")
    L.append(f"- Orphan unit rows (missing Stage): **{len(orphans)}**")
    L.append(f"- Cross-sheet consumers of Programme: **{len(xsheet_consumers)}**")
    L.append(f"- Reports sourced from Programme: **{len(report_consumers)}**\n")

    L.append("## Unit rows with predecessors")
    L.append("(pred target id, is that target also a unit row that will be consolidated?)\n")
    for tn, rid, up in units_with_preds:
        L.append(f"- `{tn}` (row {rid}): " + ", ".join(f"{p}{'[UNIT]' if isu else '[task]'}" for p, isu in up))
    L.append("")
    L.append("## Unit rows that ARE predecessors (other rows depend on them)\n")
    for tn, rid, deps in units_are_preds:
        L.append(f"- `{tn}` (row {rid}) <- depended on by {len(deps)} rows: {deps}")
    L.append("")
    L.append("## Unit rows with children\n")
    for tn, rid, n in units_with_children:
        L.append(f"- `{tn}` (row {rid}): {n} children")
    L.append("")
    L.append("## Orphan rows\n")
    for tn, rid, why in orphans:
        L.append(f"- `{tn}` (row {rid}): {why}")
    L.append("")
    L.append("## Cross-sheet consumers of Programme\n")
    for name, sid, xn in xsheet_consumers:
        L.append(f"- {name} (`{sid}`) cross-sheet reference `{xn}` -> Programme")
    if not xsheet_consumers:
        L.append("- NONE — no sheet pulls from Programme via cross-sheet reference")
    L.append("")
    L.append("## Reports sourced from Programme\n")
    for nm, rid in report_consumers:
        L.append(f"- {nm} ({rid})")
    if not report_consumers:
        L.append("- NONE found in 107 workspace reports")
    L.append("")

    open("/home/kyle/KPV-Consulting/plans/107-per-building-migration/phase_2a_audit.md", "w").write("\n".join(L))
    print("\n".join(L[:14]))
    print("\n... full report written to phase_2a_audit.md")


if __name__ == "__main__":
    main()
