import re, time
import numpy as np, pandas as pd
from collections import defaultdict
ROOT = "/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2"
rng = np.random.default_rng(7); t0 = time.time()
_DIA = re.compile(r"[ً-ٰٟۖ-ۭ]"); _TAT = re.compile("ـ"); WA = re.compile(r"[^\W\d_]+", re.UNICODE)
def nl(t):
    t = _TAT.sub("", _DIA.sub("", str(t)))
    t = re.sub(r"[آأإٱ]", "ا", t); t = re.sub(r"[ىی]", "ي", t); t = re.sub(r"[ةھ]", "ه", t)
    return t.replace("ک", "ك").replace("ؤ", "ء").replace("ئ", "ء").strip()
def toks(s): return frozenset(nl(w) for w in WA.findall(str(s)) if nl(w))
THR = 0.6
raw = pd.read_excel(ROOT + "/Book6.xlsx", header=None, nrows=8); hdr = 0
for i in range(len(raw)):
    if raw.iloc[i].map(lambda x: nl(x)).str.contains("سوره").any(): hdr = i; break
df = pd.read_excel(ROOT + "/Book6.xlsx", header=hdr); df.columns = [str(c).strip() for c in df.columns]
scol = [c for c in df.columns if "سوره" in nl(c) and "اسم" not in nl(c)][0]
tcol = [c for c in df.columns if "متن" in nl(c) and "بي" in nl(c)][0]
sur = {}
for s, txt in zip(df[scol].tolist(), df[tcol].tolist()):
    try: si = int(float(s))
    except Exception: continue
    if 1 <= si <= 114: sur.setdefault(si, []).append(toks(txt))

def jac(a, b): return 0.0 if not a or not b else len(a & b) / len(a | b)
def cluster_labels(ayat):
    n = len(ayat); par = list(range(n))
    def f(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for i in range(n):
        if len(ayat[i]) < 2: continue
        for j in range(i + 1, n):
            if len(ayat[j]) < 2: continue
            if jac(ayat[i], ayat[j]) >= THR: par[f(i)] = f(j)
    return [f(i) for i in range(n)]
def refrain_stat(labels):
    pos = defaultdict(list)
    for i, l in enumerate(labels): pos[l].append(i)
    best, bc = 0.0, 0
    counts = defaultdict(int)
    for l in labels: counts[l] += 1
    for l, ps in pos.items():
        if len(ps) < 3: continue
        g = np.diff(ps); reg = 1.0 / (1.0 + g.std() / (g.mean() + 1e-9))
        if reg > best: best, bc = reg, len(ps)
    return best, bc
def refrain_z(labels, R=500):
    real, c = refrain_stat(labels)
    if c < 3: return None
    arr = list(labels); nu = np.empty(R)
    for t in range(R): rng.shuffle(arr); nu[t] = refrain_stat(arr)[0]
    return real, c, (real - nu.mean()) / (nu.std() + 1e-9)

print("[%.1fs] NEAR-MATCH refrain (Jaccard>=%.2f)" % (time.time() - t0, THR))
print("===== GATE =====")
known = {55: "ar-Rahman", 77: "al-Mursalat", 54: "al-Qamar", 26: "ash-Shu'ara", 56: "al-Waqi'a"}
labs = {s: cluster_labels(sur[s]) for s in [55, 77, 54, 26, 56]}
for s in [55, 77, 54, 26, 56]:
    r = refrain_z(labs[s])
    print(("  S%-3d %-12s reg=%.2f count=%2d z=%+.1f" % (s, known[s], r[0], r[1], r[2])) if r
          else "  S%-3d %-12s no near-refrain >=3" % (s, known[s]))

print("\n===== ALL SURAHS =====")
res = []
for s, ay in sorted(sur.items()):
    r = refrain_z(cluster_labels(ay))
    if r: res.append((s, r[0], r[1], r[2]))
zz = np.array([x[3] for x in res])
print("  surahs with a near-refrain (count>=3): %d / 114  (exact-match was 5)" % len(res))
print("  of those: frac z>2 = %.0f%% (%d surahs) | mean z = %+.2f" % (100*np.mean(zz > 2), int(np.sum(zz > 2)), zz.mean()))
print("  top (surah, reg, count, z):")
for s, reg, c, z in sorted(res, key=lambda x: -x[3])[:18]:
    print("     S%-3d reg=%.2f count=%2d z=%+.1f" % (s, reg, c, z))
print("\n[total %.1fs]" % (time.time() - t0))
