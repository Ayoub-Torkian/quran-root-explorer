"""Precompute the corpus-wide ('forest') spatial classification to JSON.

One pass per FEATURE (root, surface form) over the corpus builds, per item, the
y-position list under each ordering (for the local Fano/clustering reading) and
the per-unit count vector under each areal partition (for coverage + analytic
Moran's I). The page loads the JSON instantly; heavy CSR kernels stay live for
single-item drill-down.

Re-run after any data change:  python precompute_spatial.py
"""
import json
import time
from collections import Counter, defaultdict

import numpy as np

import analysis as A
import spatial_patterns as SP

# feature -> list of (order, unit) pairs to precompute
PLAN = {
    "root": [("mushaf", "surah"), ("ayah_major", "ayah_band"),
             ("revelation", "revelation")],
    "surface": [("mushaf", "surah"), ("ayah_major", "ayah_band")],
}
MIN_FREQ = 8
FANO_CLUSTERED = 1.5


def _run_feature(c, feature, pairs, has_rev):
    src = c.surface_tokens if feature == "surface" else c.root_tokens
    df = c.df
    n = len(df)
    su = df[A.COL_SURAH].astype(int).to_numpy()
    ay = df[A.COL_AYAH].astype(int).to_numpy()
    rev_of = c.rev_order_of_surah if has_rev else {}
    orders = sorted({o for o, _ in pairs})
    units = sorted({u for _, u in pairs})
    oidx = {o: SP._order_index(c, o) for o in orders
            if o != "revelation" or has_rev}
    ylists = {o: defaultdict(list) for o in oidx}
    def _zeros(sz):
        return lambda: np.zeros(sz)
    counts = {u: defaultdict(_zeros(287 if u == "ayah_band" else 115))
              for u in units if u != "revelation" or has_rev}
    freq = Counter()
    K = A.normalize_letters
    for i in range(n):
        toks = src[i]
        if not toks:
            continue
        s = int(su[i]); a = int(ay[i])
        rev_s = rev_of.get(s, 999) if has_rev else None
        seen = set()
        for j, t in enumerate(toks):
            r = K(t)
            if r not in seen:
                seen.add(r); freq[r] += 1
            for o in oidx:
                ylists[o][r].append(int(oidx[o][i]))
            if "surah" in counts:
                counts["surah"][r][s] += 1
            if "ayah_band" in counts and a <= 286:
                counts["ayah_band"][r][a] += 1
            if "revelation" in counts and has_rev and rev_s <= 114:
                counts["revelation"][r][rev_s] += 1

    items = [r for r, f in freq.items() if f >= MIN_FREQ]
    W = {114: SP.contiguity_W(114), 286: SP.contiguity_W(286)}
    out = {}
    for order, unit in pairs:
        if order not in oidx or unit not in counts:
            continue
        size = 286 if unit == "ayah_band" else 114
        rows = []
        for r in items:
            ys = sorted(ylists[order][r])
            if len(ys) < 4:
                continue
            gaps = [ys[k + 1] - ys[k] for k in range(len(ys) - 1)]
            fano = SP._fano_factor(gaps)
            vec = counts[unit][r][1:size + 1]
            cov = int((vec > 0).sum()) / size
            mi = SP.morans_I_analytic(vec, W[size])
            rows.append(dict(root=r, freq=int(freq[r]), fano=round(fano, 3),
                             local=("clustered" if fano > FANO_CLUSTERED else "dispersed"),
                             coverage=round(cov, 3), I=mi["I"],
                             I_class=mi["klass"], I_p=mi["p"]))
        m = len(rows) or 1

        def pct(field, val):
            return round(100 * sum(1 for x in rows if x[field] == val) / m, 1)
        covs = [x["coverage"] for x in rows]
        summary = dict(
            feature=feature, order=order, unit=unit, n_roots=len(rows),
            min_freq=MIN_FREQ, fano_threshold=FANO_CLUSTERED,
            local_clustered=pct("local", "clustered"),
            mean_coverage=round(float(np.mean(covs)), 3),
            median_coverage=round(float(np.median(covs)), 3),
            max_coverage=round(float(np.max(covs)), 3),
            saturated_pct=round(100 * sum(1 for v in covs if v >= 0.999) / m, 1),
            I_clustered=pct("I_class", "clustered"),
            I_regular=pct("I_class", "regular"),
            I_random=pct("I_class", "random"))
        rows.sort(key=lambda x: -x["freq"])
        out[f"{feature}:{order}|{unit}"] = dict(summary=summary, rows=rows)
    return out


def build(xlsx="Book6.xlsx", out="spatial_forest.json"):
    t0 = time.time()
    c = A.load_corpus(xlsx)
    has_rev = c.has_rev_order
    scenarios = {}
    for feature, pairs in PLAN.items():
        scenarios.update(_run_feature(c, feature, pairs, has_rev))
    payload = dict(generated=time.strftime("%Y-%m-%d %H:%M"), n_ayahs=len(c.df),
                   has_rev=bool(has_rev), min_freq=MIN_FREQ, scenarios=scenarios)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False)
    print("wrote %s  (%d scenarios, %.1fs)" % (out, len(scenarios), time.time() - t0))
    for k, v in scenarios.items():
        s = v["summary"]
        print("  %-26s n=%4d local=%.0f%% cov=%.2f satur=%.0f%% "
              "I[clu=%.0f reg=%.0f rand=%.0f]" % (
                  k, s["n_roots"], s["local_clustered"], s["mean_coverage"],
                  s["saturated_pct"], s["I_clustered"], s["I_regular"], s["I_random"]))


if __name__ == "__main__":
    build()
