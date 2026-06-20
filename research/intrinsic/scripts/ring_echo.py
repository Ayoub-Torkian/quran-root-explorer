#!/usr/bin/env python3
"""RING / ECHO-GEOMETRY detector — deciphering the mathani (repetition) signal.
Known: the Qur'an repeats more than chance. UNKNOWN (this test): is that repetition arranged as a
RING / chiasmus — i.e. are symmetric-position ayah pairs (i, n+1-i) more root-similar than the
average pair, beyond what ayah-ORDER shuffling gives?
  metric  M = mean IDF-weighted root overlap over symmetric (anti-diagonal) ayah pairs of a sura
  null     = shuffle ayah ORDER within the sura (divine-default vs shuffle), R times
  z_sura   = (M_real - mean M_shuffle) / sd       (+ = ring, - = monotonic gradient)
Aggregate: Stouffer Z over qualifying suras + count individually significant. Substrate ROOT content
(drop ~10 ubiquitous roots); arrangement DIVINE-DEFAULT. Confounds: local adjacency does NOT touch the
anti-diagonal; a monotonic topic drift gives NEGATIVE z (opposite sign), so it cannot fake a ring.
"""
import os, sys, json, math, random, time
import numpy as np
random.seed(5); np.random.seed(5)
APP = "/sessions/jolly-admiring-hamilton/mnt/Quran_Root_Explorer_Web_v1.2"
sys.path.insert(0, APP)
import analysis as A
HERE = os.path.dirname(os.path.abspath(__file__))

NMIN = 7          # min ayahs in a sura to have a meaningful ring
DROP = 10         # drop the N globally most frequent roots (ubiquitous)
R = 300           # shuffle replicates

def main():
    t0 = time.time()
    c = A.load_corpus(os.path.join(APP, "Book6.xlsx"))
    N = len(c.df)
    # per-ayah root SETS, grouped by sura in canonical order
    from collections import Counter, defaultdict
    gfreq = Counter(r for rl in c.root_tokens for r in rl if r and r != "-")
    drop = {r for r, _ in gfreq.most_common(DROP)}
    # IDF over ayahs (document = ayah)
    df = Counter()
    rootsets = []
    for i in range(N):
        s = {r for r in c.root_tokens[i] if r and r != "-" and r not in drop}
        rootsets.append(s)
        for r in s: df[r] += 1
    idf = {r: math.log(N / df[r]) for r in df}
    suras = defaultdict(list)
    for i in range(N):
        suras[int(c.df.iloc[i][A.COL_SURAH])].append(i)

    def overlap(a, b):
        sh = rootsets[a] & rootsets[b]
        return sum(idf[r] for r in sh)

    def ring_M(order):
        n = len(order); pairs = [(order[i], order[n - 1 - i]) for i in range(n // 2)]
        return np.mean([overlap(a, b) for a, b in pairs]) if pairs else 0.0

    rows = []
    for s in sorted(suras):
        idxs = suras[s]; n = len(idxs)
        if n < NMIN: continue
        M = ring_M(idxs)
        nulls = []
        for r in range(R):
            o = idxs[:]; random.shuffle(o); nulls.append(ring_M(o))
        nulls = np.array(nulls); sd = nulls.std()
        z = (M - nulls.mean()) / (sd + 1e-9)
        # empirical one-sided p (ring = M above null)
        p = (1 + np.sum(nulls >= M)) / (R + 1)
        rows.append({"sura": s, "n": n, "M": round(float(M), 3),
                     "null": round(float(nulls.mean()), 3), "z": round(float(z), 2), "p": round(float(p), 4)})

    zs = np.array([r["z"] for r in rows])
    stou = float(zs.sum() / math.sqrt(len(zs)))
    sig_pos = [r for r in rows if r["z"] >= 2]
    sig_neg = [r for r in rows if r["z"] <= -2]
    out = {
        "n_suras_tested": len(rows),
        "stouffer_Z": round(stou, 2),
        "mean_z": round(float(zs.mean()), 3),
        "n_sig_ring(z>=2)": len(sig_pos),
        "n_sig_gradient(z<=-2)": len(sig_neg),
        "frac_positive": round(float((zs > 0).mean()), 3),
        "top_ring": sorted(sig_pos, key=lambda r: -r["z"])[:12],
        "params": {"NMIN": NMIN, "DROP": DROP, "R": R, "sec": round(time.time() - t0, 1)},
        "all": rows,
    }
    json.dump(out, open(os.path.join(HERE, "ring_echo_result.json"), "w"), ensure_ascii=False, indent=2)
    print(json.dumps({k: v for k, v in out.items() if k != "all"}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
