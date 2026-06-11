# -*- coding: utf-8 -*-
"""#78 — THE SEAL DICTIONARY (invert #62). Internal instrument, gate-validated.
For each ending-class (8<=n<=300): content profile (log-odds top roots), class fit-z
(#62 statistic), referent mix (#77 rule), per-verse fit -> DEVIANTS."""
import re, sys, time
import numpy as np
ROOT = "/sessions/vigilant-sharp-knuth/mnt/Quran_Root_Explorer_Web_v1.2"
sys.path.insert(0, ROOT)
import analysis as A
rng = np.random.default_rng(78); t0 = time.time()

_DIA = re.compile(r"[ً-ْٰـۖ-ۭ]"); WA = re.compile(r"[^\W\d_]+", re.UNICODE)
DIVRE = re.compile(r"^(الله|ولله|لله|بالله|فالله|والله|تالله|هو|وهو|انه|وانه|فانه)$|^رب(ي|ك|ه|ها|نا|كم|كما|هم|هن)?$")
def nl(t):
    t = _DIA.sub("", str(t)); t = re.sub(r"[آأإٱ]", "ا", t); t = re.sub(r"[ىیئ]", "ي", t)
    t = re.sub(r"[ةھ]", "ه", t)
    return t.replace("ک", "ك").replace("ؤ", "ء").strip()

c = A.load_corpus(ROOT + "/Book6.xlsx"); df = c.df
D = A.COL_DIACRITIZED
sur = df[A.COL_SURAH].astype(int).to_numpy(); ay = df[A.COL_AYAH].astype(int).to_numpy()
surf = [WA.findall(nl(t)) for t in df[D]]
roots = [str(t).split() for t in df[A.COL_ROOTS]]
finals = [w[-1] if w else "" for w in surf]
div = [any(DIVRE.match(w) for w in s[-6:]) for s in surf]
N = len(df)

# body = roots minus the final root (the #62 body definition)
body = [[r for r in rr[:-1] if r != rr[-1]] if len(rr) > 1 else [] for rr in roots]
vocab = {}
for b in body:
    for r in b: vocab.setdefault(r, len(vocab))
V = np.zeros((N, len(vocab)), dtype=np.float32)
for i, b in enumerate(body):
    for r in b: V[i, vocab[r]] += 1
dfreq = (V > 0).sum(0); idf = np.log((N + 1) / (dfreq + 1)) + 1
Vt = V * idf
nrm = np.linalg.norm(Vt, axis=1, keepdims=True); nrm[nrm == 0] = 1
Vn = Vt / nrm
bg_rate = (V > 0).mean(0)  # background doc-rate per root
inv_vocab = {j: r for r, j in vocab.items()}

classes = {}
for i, f in enumerate(finals):
    if f: classes.setdefault(f, []).append(i)
CL = {f: ix for f, ix in classes.items() if 8 <= len(ix) <= 300}
print(f"[{time.time()-t0:.0f}s] classes in bounds: {len(CL)} (of {len(classes)})")

def coh(ix):
    M = Vn[ix] @ Vn[ix].T; iu = np.triu_indices(len(ix), 1)
    return float(M[iu].mean())

def fit_z(ix, B=150):
    o = coh(ix)
    null = np.array([coh(rng.choice(N, len(ix), replace=False)) for _ in range(B)])
    return (o - null.mean()) / (null.std() + 1e-12), o

# GATE: planted class — random verses + injected shared content
gate_ix = rng.choice(N, 30, replace=False)
Vg = Vn.copy(); j0 = 0
Vg[gate_ix, j0] += 3.0
ngr = np.linalg.norm(Vg[gate_ix], axis=1, keepdims=True); Vg[gate_ix] = Vg[gate_ix]/ngr
def coh_g(ix, M_):
    Mm = M_[ix] @ M_[ix].T; iu = np.triu_indices(len(ix), 1); return float(Mm[iu].mean())
og = coh_g(gate_ix, Vg)
nullg = np.array([coh_g(rng.choice(N, 30, replace=False), Vn) for _ in range(100)])
zg = (og - nullg.mean()) / (nullg.std() + 1e-12)
print(f"GATE planted-class z = {zg:+.1f} (must fire >>2)")
rnd_ix = rng.choice(N, 30, replace=False)
zr, _ = fit_z(list(rnd_ix), B=100)
print(f"GATE random-class z = {zr:+.1f} (must be ~0)")

rows = []
deviants = []
for f, ix in sorted(CL.items(), key=lambda kv: -len(kv[1])):
    n = len(ix)
    z, o = fit_z(ix)
    # content profile: log-odds of root presence in class vs background
    cr = (V[ix] > 0).mean(0)
    lo = np.log((cr + 0.01) / (bg_rate + 0.01))
    support = (V[ix] > 0).sum(0)
    cand = [(lo[j], inv_vocab[j]) for j in np.argsort(-lo)[:30] if support[j] >= max(3, n*0.12)]
    top = [r for _, r in cand[:8]]
    dshare = float(np.mean([div[i] for i in ix]))
    # per-verse fit: mean cosine to classmates vs null (random verse vs this class)
    M = Vn[ix] @ Vn[ix].T
    vfit = (M.sum(1) - 1.0) / (n - 1)
    rs = rng.choice(N, 200, replace=False)
    rnull = (Vn[rs] @ Vn[ix].T).mean(1)
    thr = float(np.median(rnull))
    for k, i in enumerate(ix):
        if vfit[k] < thr and z > 3:   # deviant only in well-fitted classes
            deviants.append((f, f"{sur[i]}:{ay[i]}", float(vfit[k]), thr))
    rows.append(dict(ending=f, n=n, fit_z=round(float(z), 1), coh=round(o, 3),
                     div_share=round(dshare, 2), top_roots=" ".join(top)))
print(f"[{time.time()-t0:.0f}s] classes scored: {len(rows)}, deviants flagged: {len(deviants)}")

import csv
with open("/tmp/r78/seal_dictionary.csv", "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.DictWriter(fh, fieldnames=["ending", "n", "fit_z", "coh", "div_share", "top_roots"])
    w.writeheader()
    for r in sorted(rows, key=lambda r: -r["fit_z"]): w.writerow(r)
with open("/tmp/r78/seal_deviants.csv", "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.writer(fh); w.writerow(["ending", "verse", "fit", "null_median"])
    for d in sorted(deviants): w.writerow(d)

zs = np.array([r["fit_z"] for r in rows])
print(f"fit_z: {np.mean(zs>2):.0%} of classes >2σ · {np.mean(zs>5):.0%} >5σ · median {np.median(zs):+.1f}")
print("TOP 12 by fit_z:")
for r in sorted(rows, key=lambda r: -r["fit_z"])[:12]:
    print(f"  {r['ending']:>12s} n={r['n']:>3d} z={r['fit_z']:>+6.1f} div={r['div_share']:.2f} | {r['top_roots']}")
print("BOTTOM 5 (least content-bound seals):")
for r in sorted(rows, key=lambda r: r["fit_z"])[:5]:
    print(f"  {r['ending']:>12s} n={r['n']:>3d} z={r['fit_z']:>+6.1f}")
print(f"sample deviants: {deviants[:8]}")
print(f"[total {time.time()-t0:.0f}s]")
