import re, sys, time
import numpy as np, pandas as pd
from collections import Counter
ROOT = "/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2"
rng = np.random.default_rng(3); t0 = time.time()
_DIA = re.compile(r"[ً-ٰٟۖ-ۭ]"); _TAT = re.compile("ـ"); WA = re.compile(r"[^\W\d_]+", re.UNICODE)
def nl(t):
    t = _TAT.sub("", _DIA.sub("", str(t)))
    t = re.sub(r"[آأإٱ]", "ا", t); t = re.sub(r"[ىی]", "ي", t); t = re.sub(r"[ةھ]", "ه", t)
    return t.replace("ک", "ك").replace("ؤ", "ء").replace("ئ", "ء").strip()

# ---- load Quran roots per ayah, grouped by surah (row order = ayah order) ----
raw = pd.read_excel(ROOT + "/Book6.xlsx", header=None, nrows=8); hdr = 0
for i in range(len(raw)):
    if raw.iloc[i].map(lambda x: nl(x)).str.contains("سوره").any(): hdr = i; break
df = pd.read_excel(ROOT + "/Book6.xlsx", header=hdr); df.columns = [str(c).strip() for c in df.columns]
scol = [c for c in df.columns if "سوره" in nl(c) and "اسم" not in nl(c)][0]
rcol = [c for c in df.columns if "ريشه" in nl(c) and "توك" not in nl(c)][0]
df = df[[scol, rcol]].dropna(subset=[scol]).reset_index(drop=True)
df["__r"] = df[rcol].fillna("").map(lambda s: [nl(w) for w in WA.findall(str(s)) if nl(w)])
sur = {}
for s, r in zip(df[scol].tolist(), df["__r"].tolist()):
    try: si = int(float(s))
    except (ValueError, TypeError): continue
    if not (1 <= si <= 114): continue
    sur.setdefault(si, []).append(r)   # sur[surah] = list of ayah-root-lists, in order

# global frequent roots to drop (ubiquitous: الله، قال، الذي ...)
allroots = Counter(w for ay in sur.values() for r in ay for w in r)
TOPDROP = set(w for w, _ in allroots.most_common(15))

def blocks_from_ayat(ayat, B):
    # split ayah list into B contiguous blocks; block = set of roots (minus topdrop)
    n = len(ayat)
    idx = np.linspace(0, n, B + 1).astype(int)
    out = []
    for j in range(B):
        s = set()
        for k in range(idx[j], idx[j + 1]):
            s |= set(w for w in ayat[k] if w not in TOPDROP)
        out.append(s)
    return out

def jac(a, b):
    if not a or not b: return 0.0
    return len(a & b) / len(a | b)

def ring_score(blocks):
    B = len(blocks)
    return np.mean([jac(blocks[i], blocks[B - 1 - i]) for i in range(B // 2)])

def ring_z(blocks, R=400):
    real = ring_score(blocks)
    B = len(blocks)
    nulls = np.empty(R)
    for t in range(R):
        perm = list(rng.permutation(B))
        nulls[t] = ring_score([blocks[p] for p in perm])
    z = (real - nulls.mean()) / (nulls.std() + 1e-9)
    P = float(np.mean(nulls >= real))   # one-sided: chance of >= real under permutation
    return real, z, P

# ================= POSITIVE-CONTROL GATE (run BEFORE Quran) =================
print("[%.1fs] ===== DETECTOR SELF-VALIDATION (gate) =====" % (time.time() - t0))
# ordinary Arabic as material: Tabari, tokenized, chopped into pseudo-ayat
tab = []
for ln in open("corpus/ar_tabari.txt", encoding="utf-8", errors="ignore"):
    w = [nl(x) for x in WA.findall(ln) if nl(x)]
    if w: tab += w
pseudo_ayat = [tab[i:i+8] for i in range(0, len(tab) - 8, 8)]   # ~8-root "ayat"

# (1) synthetic palindrome: build blocks then mirror them -> must score very high
base = blocks_from_ayat(pseudo_ayat[:80], 8)
palin = base[:4] + base[3::-1]            # b0 b1 b2 b3 b3 b2 b1 b0  (perfect ring)
_, zP, pP = ring_z(palin)
print("  (1) synthetic palindrome ring-z = %+.1f  P=%.3f   [expect z>>2]" % (zP, pP))
# (2) degradation ladder: progressively corrupt the palindrome's order
print("  (2) degradation ladder (palindrome -> shuffled):")
for frac in (0.0, 0.25, 0.5, 1.0):
    bl = palin[:]
    k = int(frac * len(bl))
    if k >= 2:
        ids = list(rng.choice(len(bl), k, replace=False)); vals = [bl[i] for i in ids]
        rng.shuffle(vals)
        for i, v in zip(ids, vals): bl[i] = v
    _, z, _ = ring_z(bl)
    print("        shuffle %3d%%: ring-z = %+.1f" % (int(frac*100), z))
# (3) negative control: ordinary Arabic pseudo-surahs (matched ~ to Quran surah sizes)
neg = []
chunk = 96  # pseudo-ayat per pseudo-surah
for i in range(0, len(pseudo_ayat) - chunk, chunk):
    bl = blocks_from_ayat(pseudo_ayat[i:i+chunk], 8)
    _, z, _ = ring_z(bl, R=300); neg.append(z)
neg = np.array(neg)
print("  (3) ordinary Arabic pseudo-surahs: mean ring-z=%+.2f  frac z>2=%.0f%%  (n=%d) [expect ~0, ~5%%]"
      % (neg.mean(), 100*np.mean(neg > 2), len(neg)))

GATE = (zP > 2) and (neg.mean() < 1.0) and (np.mean(neg > 2) < 0.20)
print("  GATE PASSED:", GATE)

# ================= APPLY TO QURAN (only if gate passed) =================
if GATE:
    print("\n[%.1fs] ===== QURAN SURAHS =====" % (time.time() - t0))
    zs = []
    for s, ayat in sorted(sur.items()):
        if len(ayat) < 8: continue
        bl = blocks_from_ayat(ayat, 8)
        _, z, P = ring_z(bl, R=400); zs.append((s, len(ayat), z, P))
    Z = np.array([z for _, _, z, _ in zs])
    print("  surahs tested (>=8 ayat): %d" % len(zs))
    print("  mean ring-z = %+.2f  |  median = %+.2f  |  frac z>2 = %.0f%%  |  frac z>1 = %.0f%%"
          % (Z.mean(), np.median(Z), 100*np.mean(Z > 2), 100*np.mean(Z > 1)))
    def gap(a, b): return (a.mean()-b.mean())/(np.sqrt((a.var()+b.var())/2)+1e-9)
    print("  Quran vs ordinary-Arabic pseudo-surahs: %+.1fsd  (Quran %.2f vs ord %.2f)"
          % (gap(Z, neg), Z.mean(), neg.mean()))
    top = sorted(zs, key=lambda x: -x[2])[:12]
    print("  top ring surahs (surah, n_ayat, z, P):")
    for s, n, z, P in top: print("     S%-3d n=%-3d z=%+.1f P=%.3f" % (s, n, z, P))
print("\n[total %.1fs]" % (time.time() - t0))
