"""
107 Papamoa Budget — Smartsheet build script.

Executes the remaining rows from the Claude Code build brief (16 May 2026)
against sheet 5631895457976196.

Usage:
    python3 build_budget.py state          # read-only: dump section parents
    python3 build_budget.py step1           # Stage 1 children (35)
    python3 build_budget.py rest            # Steps 2-7
    python3 build_budget.py verify          # pull 8 section parents, print totals

Host: api.smartsheet.com (token authenticates against .com, NOT .au).
Rules honoured:
  - one parentId per add_rows call (error 1123)
  - parents get =SUM(CHILDREN()) on all 8 numeric columns
  - children: direct values for Base/Contingency/Actual/EstStill; formulas for
    Budget Approved, Budget Remaining, Expected Total Cost, Expected Total Variance
  - never DESCENDANTS()
"""

import json
import sys
import urllib.request
import urllib.error

API = "https://api.smartsheet.com/2.0"
SHEET_ID = 5631895457976196
TOKEN = open("/home/kyle/KPV-Consulting/smartsheet/input/Smartsheet API.txt").read().strip()

COL = {
    "Line Item": 2413490345381764,
    "Section": 7247788361682820,
    "Category": 1618288827469700,
    "Base Price": 6121888454840196,
    "Contingency Amount": 3870088641154948,
    "Budget Approved": 8373688268525444,
    "Actual per Xero": 1055338874048388,
    "Budget Remaining": 5558938501418884,
    "Estimated Still to Spend": 3307138687733636,
    "Expected Total Cost": 7810738315104132,
    "Expected Total Variance": 2181238780891012,
    "Variance Status": 6684838408261508,
    "Notes": 4433038594576260,
}

SECTION = {
    "Pre-Construction": 5425069889617796,
    "Stage 1": 3173270075932548,
    "Stage 2": 7676869703303044,
    "Stage 3": 2047370169089924,
    "Stage 4 and 5": 6550969796460420,
    "Stage 5": 4299169982775172,
    "Pavilion": 8802769610145668,
    "Project Costs": 217782820470660,
}

STAGE1_CAT = {
    "Design": 2411502865153924,
    "Supervision": 6915102492524420,
    "Civil": 1285602958311300,
    "Technology": 5789202585681796,
    "Landscaping": 3537402771996548,
    "Council Fees": 8041002399367044,
    "Buildings": 722653004889988,
}

NUMERIC_PARENT_COLS = [
    "Base Price", "Contingency Amount", "Budget Approved", "Actual per Xero",
    "Budget Remaining", "Estimated Still to Spend", "Expected Total Cost",
    "Expected Total Variance",
]

CHILD_FORMULAS = {
    "Budget Approved": "=[Base Price]@row + [Contingency Amount]@row",
    "Budget Remaining": "=[Budget Approved]@row - [Actual per Xero]@row",
    "Expected Total Cost": "=[Actual per Xero]@row + [Estimated Still to Spend]@row",
    "Expected Total Variance": "=[Budget Approved]@row - [Expected Total Cost]@row",
}


def _req(method, path, body=None):
    url = API + path
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Authorization", "Bearer " + TOKEN)
    r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.read().decode())
        raise


def child_cells(line_item, section, category, base, cont, actual, est_still):
    cells = [
        {"columnId": COL["Line Item"], "value": line_item},
        {"columnId": COL["Section"], "value": section, "strict": False},
        {"columnId": COL["Category"], "value": category, "strict": False},
        {"columnId": COL["Base Price"], "value": base},
        {"columnId": COL["Contingency Amount"], "value": cont},
        {"columnId": COL["Actual per Xero"], "value": actual},
        {"columnId": COL["Estimated Still to Spend"], "value": est_still},
    ]
    for name, f in CHILD_FORMULAS.items():
        cells.append({"columnId": COL[name], "formula": f})
    return cells


def parent_cells(line_item, section, category):
    cells = [
        {"columnId": COL["Line Item"], "value": line_item},
        {"columnId": COL["Section"], "value": section, "strict": False},
    ]
    if category:
        cells.append({"columnId": COL["Category"], "value": category, "strict": False})
    for name in NUMERIC_PARENT_COLS:
        cells.append({"columnId": COL[name], "formula": "=SUM(CHILDREN())"})
    return cells


def add_children(parent_id, section, rows):
    """rows: list of (line_item, category, base, cont, actual, est_still)"""
    body = [
        {"parentId": parent_id, "toBottom": True,
         "cells": child_cells(li, section, cat, b, c, a, e)}
        for (li, cat, b, c, a, e) in rows
    ]
    res = _req("POST", f"/sheets/{SHEET_ID}/rows", body)
    return [r["id"] for r in res["result"]]


def add_category_parents(section_id, section, cat_defs):
    """cat_defs: list of (line_item_label, category). One add_rows call (one parent)."""
    body = [
        {"parentId": section_id, "toBottom": True,
         "cells": parent_cells(label, section, cat)}
        for (label, cat) in cat_defs
    ]
    res = _req("POST", f"/sheets/{SHEET_ID}/rows", body)
    out = {}
    for cat_def, row in zip(cat_defs, res["result"]):
        out[cat_def[1]] = row["id"]
    return out


# ----------------------------------------------------------------------------
# DATA — transcribed verbatim from the build brief
# tuples: (line_item, category, base, contingency, actual, est_still)
# ----------------------------------------------------------------------------

STAGE1 = {
    "Design": [
        ("Building Architecture", "Design", 20000, 0, 20, 0),
        ("Landscape Design", "Design", 50000, 0, 96493, 0),
        ("Infrastructure Detailed (Civil Design)", "Design", 250000, 0, 82206, 0),
        ("Technology Design", "Design", 0, 0, 0, 0),
    ],
    "Supervision": [
        ("Building Supervision", "Supervision", 0, 0, 0, 0),
        ("Landscape Supervision", "Supervision", 32062, 0, 17740, 14322),
        ("Civil Supervision", "Supervision", 64125, 32062, 179064, 0),
        ("Quantity Survey", "Supervision", 0, 0, 29900, 90000),
        ("Cultural Monitoring", "Supervision", 0, 0, 33060, 0),
    ],
    "Civil": [
        ("P&G", "Civil", 120241, 90563, 123857, 0),
        ("Site Clearance", "Civil", 23000, 0, 3866, 0),
        ("Earthworks and Other", "Civil", 207801, 38157, 267602, 0),
        ("Stormwater", "Civil", 341452, 27899, 372155, 0),
        ("Sewer", "Civil", 147143, 11481, 145660, 0),
        ("Water", "Civil", 194884, 28510, 210383, 0),
        ("Roading", "Civil", 395352, 42085, 329777, 0),
        ("Retaining", "Civil", 33724, 1276, 41834, 0),
    ],
    "Technology": [
        ("Lighting and Security", "Technology", 180262, 0, 99258, 0),
        ("Fibre", "Technology", 6607, 0, 14835, 0),
        ("Power", "Technology", 335240, 0, 358101, 0),
    ],
    "Landscaping": [
        ("Site Landscaping", "Landscaping", 392800, 0, 112623, 5000),
        ("Fences and Gates", "Landscaping", 190950, 0, 181259, 0),
        ("Other", "Landscaping", 0, 0, 0, 0),
        ("Unit Landscaping", "Landscaping", 437000, 0, 167638, 269362),
    ],
    "Council Fees": [
        ("Council Development fees", "Council Fees", 478428, 0, 458684, 0),
    ],
    "Buildings": [
        ("103,101", "Buildings", 762189, 21811, 734774, 0),
        ("105,107", "Buildings", 758395, 51319, 629813, 88128),
        ("109,111", "Buildings", 765829, 63886, 0, 780959),
        ("115,113", "Buildings", 830390, 90467, 38165, 792225),
        ("102,104", "Buildings", 720124, 53019, 731167, 0),
        ("106,108", "Buildings", 781980, 61591, 767431, 0),
        ("112", "Buildings", 472335, 21736, 414103, 0),
        ("117,119", "Buildings", 861429, 43714, 805822, 0),
        ("121,123", "Buildings", 830390, 90467, 36263, 794127),
        ("116,118", "Buildings", 793740, 49831, 34276, 759464),
    ],
}

# Category parent label lists per section: (label, category)
STAGE2_CATS = [
    ("Stage 2 Preliminary and Developed Design", "Design"),
    ("Stage 2 Preliminary Supervision", "Supervision"),
    ("Stage 2 Civil", "Civil"),
    ("Stage 2 Technology", "Technology"),
    ("Stage 2 Landscaping", "Landscaping"),
    ("Stage 2 Council Development Fees", "Council Fees"),
    ("Stage 2 Buildings (x34)", "Buildings"),
]
STAGE2 = {
    "Design": [
        ("Building Architecture", "Design", 20000, 0, 0, 20000),
        ("Landscape Design", "Design", 50000, 0, 0, 50000),
        ("Infrastructure Detailed (Civil Design)", "Design", 50000, 0, 20060, 29940),
        ("Technology Design", "Design", 0, 0, 0, 0),
    ],
    "Supervision": [
        ("Building Supervision", "Supervision", 0, 0, 0, 0),
        ("Landscape Supervision", "Supervision", 32062, 0, 0, 32062),
        ("Civil Supervision", "Supervision", 64125, 32062, 43985, 52202),
        ("Technology Supervision", "Supervision", 0, 0, 0, 0),
    ],
    "Civil": [
        ("P&G", "Civil", 80669, 90562, 49576, 121656),
        ("Site Clearance", "Civil", 0, 0, 0, 0),
        ("Earthworks and Other", "Civil", 103569, 19260, 196481, 5000),
        ("Stormwater", "Civil", 159965, 27859, 0, 187824),
        ("Sewer", "Civil", 66654, 11471, 0, 78125),
        ("Water", "Civil", 35397, 9832, 0, 45230),
        ("Roading", "Civil", 222180, 38238, 0, 260418),
        ("Retaining", "Civil", 75878, 8431, 77386, 6923),
    ],
    "Technology": [
        ("Lighting and Security", "Technology", 49162, 0, 0, 49162),
        ("Fibre", "Technology", 8259, 0, 0, 8259),
        ("Power", "Technology", 135830, 0, 0, 135830),
    ],
    "Landscaping": [
        ("Site Landscaping (incl Stream, excl Wetland)", "Landscaping", 0, 0, 0, 0),
        ("Fences and Gates", "Landscaping", 150000, 0, 0, 100000),
        ("Other", "Landscaping", 0, 0, 0, 0),
        ("Unit Landscaping", "Landscaping", 529000, 0, 0, 529000),
    ],
    "Council Fees": [
        ("Council Development fees", "Council Fees", 579149, 0, 0, 579149),
    ],
    "Buildings": [
        ("122,124", "Buildings", 730825, 47317, 0, 778143),
        ("125,127", "Buildings", 861429, 105285, 0, 966714),
        ("126,128", "Buildings", 730825, 47317, 0, 778143),
        ("129,131", "Buildings", 765829, 68886, 0, 834714),
        ("133,135", "Buildings", 812208, 97935, 0, 910143),
        ("132,134", "Buildings", 730825, 122746, 0, 853571),
        ("137,139", "Buildings", 765829, 68886, 0, 834714),
        ("136,138", "Buildings", 730825, 47317, 0, 778143),
        ("141,143", "Buildings", 765829, 68886, 0, 834714),
        ("144", "Buildings", 443620, 80594, 0, 524214),
        ("147,145", "Buildings", 793740, 59831, 0, 853571),
        ("149,151", "Buildings", 793740, 59831, 0, 853571),
    ],
}

STAGE3_CATS = [
    ("Stage 3 Preliminary and Developed Design", "Design"),
    ("Stage 3 Preliminary Supervision", "Supervision"),
    ("Stage 3 Civil", "Civil"),
    ("Stage 3 Technology", "Technology"),
    ("Stage 3 Landscaping", "Landscaping"),
    ("Stage 3 Council Development Fees", "Council Fees"),
    ("Stage 3 Buildings (x32)", "Buildings"),
]
STAGE3 = {
    "Design": [
        ("Building Architecture", "Design", 20000, 0, 0, 20000),
        ("Landscape Design", "Design", 50000, 0, 0, 50000),
        ("Infrastructure Detailed (Civil Design)", "Design", 50000, 0, 0, 50000),
        ("Technology Design", "Design", 0, 0, 0, 0),
    ],
    "Supervision": [
        ("Building Supervision", "Supervision", 0, 0, 0, 0),
        ("Landscape Supervision", "Supervision", 32062, 0, 0, 32062),
        ("Civil Supervision", "Supervision", 64125, 32062, 0, 96188),
        ("Technology Supervision", "Supervision", 0, 0, 0, 0),
    ],
    "Civil": [
        ("P&G", "Civil", 80669, 90562, 0, 171232),
        ("Site Clearance", "Civil", 0, 0, 0, 0),
        ("Earthworks and Other", "Civil", 3060042, 450000, 0, 3510042),
        ("Stormwater", "Civil", 130379, 27859, 0, 158238),
        ("Sewer", "Civil", 55062, 11471, 0, 66533),
        ("Water", "Civil", 35397, 9832, 0, 45230),
        ("Roading", "Civil", 183540, 38238, 0, 221778),
        ("Retaining", "Civil", 1280812, 142312, 0, 1423125),
    ],
    "Technology": [
        ("Lighting and Security", "Technology", 49162, 0, 0, 49162),
        ("Fibre", "Technology", 6686, 0, 0, 6686),
        ("Power", "Technology", 54910, 0, 0, 54910),
    ],
    "Landscaping": [
        ("Site Landscaping (incl Stream, excl Wetland)", "Landscaping", 364602, 0, 0, 364602),
        ("Fences and Gates", "Landscaping", 0, 0, 0, 0),
        ("Other", "Landscaping", 0, 0, 0, 0),
        ("Unit Landscaping", "Landscaping", 575000, 0, 0, 575000),
    ],
    "Council Fees": [
        ("Council Development fees", "Council Fees", 679871, 0, 0, 679871),
    ],
    "Buildings": [
        ("174", "Buildings", 479500, 57286, 0, 536786),
        ("172,170", "Buildings", 861429, 58991, 0, 920420),
        ("166,164", "Buildings", 729264, 4736, 0, 734000),
        ("153,155", "Buildings", 730825, 47317, 0, 778143),
        ("201,203", "Buildings", 730825, 47317, 0, 778143),
        ("205,207", "Buildings", 793740, 107117, 0, 900857),
        ("206,204", "Buildings", 793740, 107117, 0, 900857),
        ("202", "Buildings", 396870, 127344, 0, 524214),
        ("305", "Buildings", 396870, 127344, 0, 524214),
        ("303,301", "Buildings", 793740, 59831, 0, 853571),
        ("302", "Buildings", 396870, 127344, 0, 524214),
        ("304,306", "Buildings", 729264, 4736, 0, 734000),
        ("401,403,405,407,409", "Buildings", 1645500, 64143, 0, 1709643),
        ("404,402", "Buildings", 910650, 67064, 0, 977714),
    ],
}

STAGE45_CATS = [
    ("Stage 4 and 5 Preliminary and Developed Design", "Design"),
    ("Stage 4 and 5 Preliminary Supervision", "Supervision"),
    ("Stage 4 and 5 Civil", "Civil"),
    ("Stage 4 and 5 Technology", "Technology"),
    ("Stage 4 and 5 Landscaping", "Landscaping"),
    ("Stage 4 Council Development Fees", "Council Fees"),
    ("Stage 4 Buildings (x32)", "Buildings"),
]
STAGE45 = {
    "Design": [
        ("Building Architecture", "Design", 28000, 0, 0, 28000),
        ("Landscape Design", "Design", 50000, 0, 0, 50000),
        ("Infrastructure Detailed (Civil Design)", "Design", 50000, 0, 0, 50000),
        ("Technology Design", "Design", 0, 0, 0, 0),
    ],
    "Supervision": [
        ("Building Supervision", "Supervision", 0, 0, 0, 0),
        ("Landscape Supervision", "Supervision", 32062, 0, 0, 32062),
        ("Civil Supervision", "Supervision", 64125, 32062, 0, 96188),
        ("Technology Supervision", "Supervision", 0, 0, 0, 0),
    ],
    "Civil": [
        ("P&G", "Civil", 80669, 90562, 0, 171232),
        ("Site Clearance", "Civil", 0, 0, 0, 0),
        ("Earthworks and Other", "Civil", 155353, 0, 0, 155353),
        ("Stormwater", "Civil", 371079, 27859, 0, 398937),
        ("Sewer", "Civil", 144538, 11471, 0, 156009),
        ("Water", "Civil", 70794, 9832, 0, 80626),
        ("Roading", "Civil", 571631, 38238, 0, 609868),
        ("Retaining", "Civil", 0, 0, 0, 0),
    ],
    "Technology": [
        ("Lighting and Security", "Technology", 49162, 0, 0, 49162),
        ("Fibre", "Technology", 17698, 0, 0, 17698),
        ("Power", "Technology", 52020, 0, 0, 52020),
    ],
    "Landscaping": [
        ("Site Landscaping (incl Stream, excl Wetland)", "Landscaping", 171400, 0, 0, 171400),
        ("Fences and Gates", "Landscaping", 150000, 0, 0, 150000),
        ("Other", "Landscaping", 0, 0, 0, 0),
        ("Unit Landscaping for Stage 4", "Landscaping", 437000, 0, 0, 437000),
    ],
    "Council Fees": [
        ("Council Development fees", "Council Fees", 654690, 0, 0, 654690),
    ],
    "Buildings": [
        ("198,196", "Buildings", 777000, 76571, 0, 853571),
        ("194,192,190,188,186,184", "Buildings", 1974600, 76971, 0, 2051571),
        ("182/1,182/2,182/3,182/4,182/5", "Buildings", 3655200, 12500, 0, 3667700),
        ("183,181", "Buildings", 793740, 59831, 0, 853571),
        ("502,504", "Buildings", 888845, 9298, 0, 898143),
        ("503,501", "Buildings", 830390, 47753, 0, 878143),
        ("180/1,180/2,180/3,180/4,180/5", "Buildings", 3655200, 32500, 0, 3687700),
        ("178,176", "Buildings", 777000, 76571, 0, 853571),
    ],
}

STAGE5_CATS = [
    ("Stage 5 Landscaping", "Landscaping"),
    ("Stage 5 Council Development Fees", "Council Fees"),
    ("Stage 5 Buildings", "Buildings"),
]
STAGE5 = {
    "Landscaping": [
        ("Site Landscaping (incl Stream, excl Wetland)", "Landscaping", 0, 0, 0, 0),
        ("Fences", "Landscaping", 0, 0, 0, 0),
        ("Gates", "Landscaping", 0, 0, 0, 0),
        ("Unit Landscaping for Stage 5", "Landscaping", 345000, 0, 0, 345000),
    ],
    "Council Fees": [
        ("Council Development fees", "Council Fees", 478428, 0, 0, 478428),
    ],
    "Buildings": [
        ("602", "Buildings", 396870, 127344, 0, 524214),
        ("604,606", "Buildings", 840490, 13081, 0, 853571),
        ("601,603,605,607,609", "Buildings", 1645500, 64143, 0, 1709643),
        ("701", "Buildings", 443620, 80594, 0, 524214),
        ("703,705", "Buildings", 793740, 59831, 0, 853571),
        ("702,704,706,708,710", "Buildings", 1645500, 64143, 0, 1709643),
        ("801", "Buildings", 443620, 80594, 0, 524214),
        ("803,805", "Buildings", 793740, 59831, 0, 853571),
    ],
}

PAVILION_CATS = [("Pavilion and grounds", "Pavilion")]
PAVILION = {
    "Pavilion": [
        ("Country Club", "Pavilion", 3959120, 0, 0, 3959120),
        ("Grounds", "Pavilion", 70000, 0, 0, 70000),
        ("Bowling Green", "Pavilion", 0, 0, 0, 0),
        ("Pool", "Pavilion", 500000, 0, 0, 500000),
        ("Workshop", "Pavilion", 30000, 0, 0, 30000),
        ("Fitout", "Pavilion", 719840, 0, 0, 719840),
    ],
}

PROJECT_COSTS = [
    ("Project Management", "Project Management", 2415000, 0, 805000, 1610000),
    ("Processing fee", "Processing", 2044903, 0, 147379, 1897524),
    ("Marketing", "Marketing", 848750, 0, 325495, 523255),
]


def do_step1():
    print("STEP 1 — Stage 1 children")
    for cat, pid in STAGE1_CAT.items():
        rows = STAGE1[cat]
        ids = add_children(pid, "Stage 1", rows)
        print(f"  {cat}: added {len(ids)} children under {pid}")


def do_section(section_name, cats, data):
    sid = SECTION[section_name]
    print(f"  {section_name}: adding {len(cats)} category parents under {sid}")
    cat_ids = add_category_parents(sid, section_name, cats)
    for label, cat in cats:
        pid = cat_ids[cat]
        rows = data[cat]
        ids = add_children(pid, section_name, rows)
        print(f"    {cat} ({label}) -> parent {pid}, {len(ids)} children")


def do_rest():
    print("STEP 2 — Stage 2")
    do_section("Stage 2", STAGE2_CATS, STAGE2)
    print("STEP 3 — Stage 3")
    do_section("Stage 3", STAGE3_CATS, STAGE3)
    print("STEP 4 — Stage 4 and 5")
    do_section("Stage 4 and 5", STAGE45_CATS, STAGE45)
    print("STEP 5 — Stage 5")
    do_section("Stage 5", STAGE5_CATS, STAGE5)
    print("STEP 6 — Pavilion")
    do_section("Pavilion", PAVILION_CATS, PAVILION)
    print("STEP 7 — Project Costs (direct under section)")
    ids = add_children(SECTION["Project Costs"], "Project Costs", PROJECT_COSTS)
    print(f"  Project Costs: {len(ids)} children direct under {SECTION['Project Costs']}")


def verify():
    res = _req("GET", f"/sheets/{SHEET_ID}?pageSize=500")
    by_id = {r["id"]: r for r in res["rows"]}
    print(f"{'Section':<18}{'Budget Approved':>18}{'Expected Cost':>16}")
    grand_ba = grand_ec = 0.0
    for name, rid in SECTION.items():
        row = by_id.get(rid, {})
        ba = ec = None
        for c in row.get("cells", []):
            if c.get("columnId") == COL["Budget Approved"]:
                ba = c.get("value")
            if c.get("columnId") == COL["Expected Total Cost"]:
                ec = c.get("value")
        ba = ba or 0.0
        ec = ec or 0.0
        grand_ba += ba
        grand_ec += ec
        print(f"{name:<18}{ba:>18,.0f}{ec:>16,.0f}")
    print(f"{'TOTAL':<18}{grand_ba:>18,.0f}{grand_ec:>16,.0f}")
    print("Expected:  Budget Approved 80,512,628  |  Expected Cost 79,373,579")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "state"
    if cmd == "step1":
        do_step1()
    elif cmd == "rest":
        do_rest()
    elif cmd == "verify":
        verify()
    elif cmd == "state":
        verify()
    else:
        print("unknown command:", cmd)
        sys.exit(1)
