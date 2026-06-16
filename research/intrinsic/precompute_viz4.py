#!/usr/bin/env python3
"""precompute_viz4.py — surface the order-ladder findings L24/L25/L26 into viz_data.json.

Provenance: these are the per-sūra paired control-comparison statistics already MEASURED
and approved in latent_features.json (each feature's `chart.items`). This script does not
re-measure; it lifts the locked measured values into the viz pipeline so the ledger card
(pages/25_Latent_Features.py) and the Signal module (pages/15_Signal.py) can draw them as
real control-comparison bar charts (same family as L23's z-by-granularity chart).

Run:  python3 research/intrinsic/precompute_viz4.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
LF = os.path.join(HERE, "latent_features.json")
VZ = os.path.join(HERE, "viz_data.json")

lf = json.load(open(LF, encoding="utf-8"))
by_id = {f["id"]: f for f in lf["features"]}

def controls(fid):
    """Lift the approved measured chart.items into a {labels, vals, stat} block."""
    ch = by_id[fid].get("chart", {}) or {}
    items = ch.get("items", [])
    labels = [it[0] for it in items]
    vals = [round(float(it[1]), 2) for it in items]
    stat = items[0][2] if items and len(items[0]) > 2 else "z"
    return {"labels": labels, "vals": vals, "stat": stat, "title": ch.get("title", "")}

viz = json.load(open(VZ, encoding="utf-8"))
viz["l24_controls"] = controls("L24")  # inter-sūra sequence order (z vs nested nulls)
viz["l25_controls"] = controls("L25")  # uniform information density (t vs nulls)
viz["l26_controls"] = controls("L26")  # closing cadence (t vs nulls)
json.dump(viz, open(VZ, "w", encoding="utf-8"), ensure_ascii=False, indent=0)

for k in ("l24_controls", "l25_controls", "l26_controls"):
    print(k, "->", json.dumps(viz[k], ensure_ascii=False))
print("viz_data.json updated.")
