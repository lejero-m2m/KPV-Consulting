"""Phase 1.1 (READ-ONLY): generate the Building Reference sequence mapping.

Produces the proposed S{stage}-B{nn} assignments and flags every
Budget-section vs Register-stage conflict. Writes mapping.json.
NO sheet writes. Stops at Checkpoint 1.1 for Kyle's review.
"""
import json, re, urllib.request

TOKEN = open("/home/kyle/KPV-Consulting/smartsheet/input/Smartsheet API.txt").read().strip()
BUDGET, PROG, REG, UR = 5631895457976196, 5063906232848260, 2635310868418436, 5289542339743620
PARENTS = {"Stage 1 Buildings (x30)", "Stage 2 Buildings (x34)", "Stage 3 Buildings (x32)",
           "Stage 4 Buildings (x32)", "Stage 5 Buildings", "Pavilion"}


def get(sid):
    r = urllib.request.Request(f"https://api.smartsheet.com/2.0/sheets/{sid}?pageSize=500")
    r.add_header("Authorization", "Bearer " + TOKEN)
    return json.loads(urllib.request.urlopen(r).read())


def colmap(sheet):
    return {c["title"]: c["id"] for c in sheet["columns"]}


def cell(row, cols, title):
    for c in row.get("cells", []):
        if c.get("columnId") == cols.get(title):
            return c.get("value")
    return None


def parse_units(units_str):
    """'182/1, 182/2' -> [182,182..]; '103, 101' -> [103,101]. Returns ints."""
    out = []
    for tok in str(units_str).split(","):
        tok = tok.strip()
        m = re.match(r"(\d+)", tok)
        if m:
            out.append(int(m.group(1)))
    return out


def main():
    budget, reg = get(BUDGET), get(REG)
    bcols, rcols = colmap(budget), colmap(reg)

    # unit -> register stage
    unit_stage = {}
    for row in reg["rows"]:
        u = cell(row, rcols, "Unit Number")
        s = cell(row, rcols, "Stage")
        if u is None:
            continue
        unit_stage[str(u).split(".")[0]] = s

    # collect Budget Buildings leaves
    blds = []
    for row in budget["rows"]:
        if cell(row, bcols, "Category") != "Buildings":
            continue
        li = cell(row, bcols, "Line Item")
        if li in PARENTS:
            continue
        units_str = cell(row, bcols, "Units") or li
        units = parse_units(units_str)
        lowest = min(units) if units else None
        # register stages for each constituent unit
        rstages = sorted({unit_stage.get(str(u)) for u in units})
        rstages = [s for s in rstages if s]
        blds.append({
            "budget_row_id": row["id"],
            "line_item": li,
            "units": units_str,
            "budget_section": cell(row, bcols, "Section"),
            "lowest_unit": lowest,
            "register_stages": rstages,
        })

    # Determine effective stage per building (brief rule: Register/Programme Stage is truth)
    def eff_stage(b):
        rs = b["register_stages"]
        if len(rs) == 1:
            return rs[0], False
        if len(rs) == 0:
            return None, True  # no register stage -> conflict/flag
        return rs[0], True  # mixed stages within a building -> flag

    anomalies = []
    for b in blds:
        es, mixed = eff_stage(b)
        b["effective_stage"] = es
        # normalise Budget section for comparison
        bs = b["budget_section"]
        bs_norm = {"Stage 4 and 5": ("Stage 4", "Stage 5"), }.get(bs, (bs,))
        conflict = False
        if es is None:
            conflict = True
            anomalies.append(f'{b["line_item"]}: NO Register stage for its units (Budget section {bs!r})')
        elif mixed:
            conflict = True
            anomalies.append(f'{b["line_item"]}: MIXED Register stages {b["register_stages"]} (Budget section {bs!r})')
        elif es not in bs_norm:
            conflict = True
            anomalies.append(f'{b["line_item"]}: Budget section {bs!r} but Register stage {es!r}  <-- CONFLICT')
        b["conflict"] = conflict

    # Assign sequence per effective stage, ascending lowest unit
    STAGE_CODE = {"Stage 1": "S1", "Stage 2A": "S2A", "Stage 2B": "S2B", "Stage 2C": "S2C",
                  "Stage 2D": "S2D", "Stage 2E": "S2E", "Stage 3": "S3", "Stage 4": "S4",
                  "Stage 5": "S5"}
    from collections import defaultdict
    groups = defaultdict(list)
    for b in blds:
        groups[b["effective_stage"]].append(b)
    for st, items in groups.items():
        items.sort(key=lambda x: (x["lowest_unit"] is None, x["lowest_unit"]))
        code = STAGE_CODE.get(st, f"?{st}")
        for i, b in enumerate(items, 1):
            b["building_reference"] = f"{code}-B{i:02d}"

    blds.sort(key=lambda b: (str(b["budget_section"]), b["lowest_unit"] or 0))

    print(f"{'BudgetSec':<15}{'LineItem':<28}{'Lowest':>7}{'RegStage':<12}{'BuildingRef':<12}{'Flag'}")
    for b in blds:
        flag = "CONFLICT" if b["conflict"] else ""
        print(f'{str(b["budget_section"]):<15}{b["line_item"]:<28}{b["lowest_unit"]!s:>7} '
              f'{str(b["effective_stage"]):<12}{b["building_reference"]:<12}{flag}')
    print(f"\nTotal buildings: {len(blds)}")
    print(f"Conflicts/anomalies: {len(anomalies)}")
    for a in anomalies:
        print("  - " + a)

    # write to mapping.json (preserve old values for rollback)
    mp = json.load(open("/home/kyle/KPV-Consulting/plans/107-per-building-migration/mapping.json"))
    mp["building_reference_mapping"] = [{
        "budget_row_id": b["budget_row_id"],
        "line_item": b["line_item"],
        "units": b["units"],
        "budget_section": b["budget_section"],
        "register_stage": b["effective_stage"],
        "register_stages_all": b["register_stages"],
        "lowest_unit": b["lowest_unit"],
        "building_reference": b["building_reference"],
        "conflict": b["conflict"],
    } for b in blds]
    mp["_meta"]["status"] = "pre-Checkpoint-1.1 — mapping proposed, awaiting Kyle approval"
    mp["anomalies"] = anomalies
    json.dump(mp, open("/home/kyle/KPV-Consulting/plans/107-per-building-migration/mapping.json", "w"), indent=2)
    print("\nmapping.json written. STOP — Checkpoint 1.1 (Kyle approval required).")


if __name__ == "__main__":
    main()
