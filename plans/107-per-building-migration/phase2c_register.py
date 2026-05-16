"""Phase 2c — set Construction Register Contract Block = Building Reference.

Join by Unit Number (separator-normalised) to mapping.json. Mitigation:
preserve old values to mapping.json + a 'Contract Block (Legacy)' column.

Usage:
  python3 phase2c_register.py dryrun   # read-only: coverage report, no writes
  python3 phase2c_register.py apply    # add legacy col, write old+new values
"""
import json, sys, urllib.request

TOKEN = open("/home/kyle/KPV-Consulting/smartsheet/input/Smartsheet API.txt").read().strip()
REG = 2635310868418436
UNIT_COL = 2571606051557252
CB_COL = 8060368097415044
MAPPING = "/home/kyle/KPV-Consulting/plans/107-per-building-migration/mapping.json"


def api(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request("https://api.smartsheet.com/2.0" + path, data=data, method=method)
    r.add_header("Authorization", "Bearer " + TOKEN)
    r.add_header("Content-Type", "application/json")
    return json.loads(urllib.request.urlopen(r).read())


def get_all(sid):
    rows, pg = [], 1
    while True:
        d = api("GET", f"/sheets/{sid}?pageSize=500&page={pg}")
        rows += d["rows"]
        if len(rows) >= d["totalRowCount"]:
            return rows, {c["title"]: c["id"] for c in d["columns"]}
        pg += 1


def ukey(u):
    s = str(u).strip()
    if s.endswith(".0"):
        s = s[:-2]
    return s.replace("/", "-")


# Kyle decision 2026-05-16 (Checkpoint 2c): bare Register rows 180/182 are
# block-level rows for S4-B01 / S4-B03 — tag them with the building reference.
BARE_OVERRIDE = {"180": "S4-B01", "182": "S4-B03"}


def build_unit_to_br():
    mp = json.load(open(MAPPING))
    u2br = {}
    for e in mp["building_reference_mapping"]:
        us = e.get("units")
        if not us:
            continue
        for tok in str(us).split(","):
            tok = tok.strip()
            if tok:
                u2br[ukey(tok)] = e["building_reference"]
    u2br.update(BARE_OVERRIDE)
    return u2br, mp


def resolve():
    u2br, mp = build_unit_to_br()
    rows, cm = get_all(REG)

    def cv(r, t):
        for c in r.get("cells", []):
            if c.get("columnId") == cm.get(t):
                return c.get("value")
        return None

    plan, unmapped = [], []
    for r in rows:
        un = cv(r, "Unit Number")
        if un is None or str(un).strip() == "" or str(un).strip().lower().startswith("stage"):
            continue  # section header / blank
        br = u2br.get(ukey(un))
        old_cb = cv(r, "Contract Block")
        if br is None:
            unmapped.append((str(un), old_cb))
        else:
            plan.append({"row_id": r["id"], "unit": str(un),
                         "old_cb": old_cb, "new_br": br})
    return plan, unmapped, mp


def dryrun():
    plan, unmapped, _ = resolve()
    print(f"real unit rows to update: {len(plan)}")
    print(f"unmapped unit rows (NO building reference): {len(unmapped)}")
    for u, cb in unmapped:
        print(f"  UNMAPPED unit {u!r} (old Contract Block {cb!r})")
    have_old = [p for p in plan if p["old_cb"]]
    print(f"rows with an existing Contract Block (will be preserved): {len(have_old)}")
    for p in sorted(plan, key=lambda x: x["new_br"])[:12]:
        print(f"  unit {p['unit']:<7} old={p['old_cb']!r:<12} -> {p['new_br']}")
    print("RESULT:", "CLEAN — safe to apply" if not unmapped else "STOP — unmapped units present")


def apply():
    plan, unmapped, mp = resolve()
    if unmapped:
        print("ABORT — unmapped units present, not writing:", unmapped)
        sys.exit(1)
    # 1) preserve old values to mapping.json
    mp["register_contract_block_old_to_new"] = [
        {"row_id": p["row_id"], "unit": p["unit"], "old": p["old_cb"], "new": p["new_br"]}
        for p in plan]
    json.dump(mp, open(MAPPING, "w"), indent=2)
    print(f"preserved {len(plan)} old Contract Block values to mapping.json")
    # 2) add legacy column
    res = api("POST", f"/sheets/{REG}/columns",
              [{"title": "Contract Block (Legacy)", "type": "TEXT_NUMBER",
                "index": 11, "width": 120}])
    legacy_id = res["result"][0]["id"] if isinstance(res.get("result"), list) else res["result"]["id"]
    print(f"added Contract Block (Legacy) column id={legacy_id}")
    # 3) write old->legacy and new->Contract Block (batched)
    body = [{"id": p["row_id"], "cells": [
        {"columnId": legacy_id, "value": p["old_cb"] if p["old_cb"] is not None else ""},
        {"columnId": CB_COL, "value": p["new_br"]},
    ]} for p in plan]
    r = api("PUT", f"/sheets/{REG}/rows", body)
    print(f"updated {len(r.get('result', []))} Register rows (Contract Block -> Building Reference)")
    mp["_meta"]["status"] = "Phase 2c done — Register Contract Block = Building Reference; legacy preserved. Pre-Checkpoint-2c verify."
    mp["new_programme"].setdefault("register_legacy_col_id", legacy_id)
    json.dump(mp, open(MAPPING, "w"), indent=2)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "dryrun"
    {"dryrun": dryrun, "apply": apply}.get(cmd, dryrun)()
