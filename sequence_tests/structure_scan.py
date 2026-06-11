import re, time
import numpy as np, pandas as pd
from collections import Counter
ROOT = "/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2"
rng = np.random.default_rng(3); t0 = time.time()
_DIA = re.compile(r"[ً-ٰٟۖ-ۭ]"); _TAT = re.compile("ـ"); WA = re.compile(r"[^\W\d_]+", re.UNICODE)
def nl(t):
    t = _TAT.sub("", _DIA.sub("", str(t)))
    t = re.sub(r"[آأإٱ]", "ا", t); t = re.sub(r"[ىی]", "ي", t); t = re.sub(r"[ةھ]", "ه", t)
    return t.replace("ک", "ك").replace("ؤ", "ء").replace("ئ", "ء").strip()
raw = pd.read_excel(ROOT + "/Book6.xlsx", header=None, nrows=8); hdr = 0
for i in range(len(raw)):
    if raw.iloc[i].map(lambda x: nl(x)).str.contains("سوره").any(): hdr = i; break
df = pd.read_excel(ROOT + "/Book6.xlsx", header=hdr); df.columns = [str(c).strip() for c in df.columns]
scol = [c for c in df.columns if "سوره" in nl(c) and "اسم" not in nl(c)][0]
rcol = [c for c in df.columns if "ريشه" in nl(c) and "توك" not in nl(c)][0]
df = df[[scol, rcol]].copy()
df["__r"] = df[rcol].fillna("").map(lambda s: [nl(w) for w in WA.findall(str(s)) if nl(w)])
sur = {}
for s, r in zip(df[scol].tolist(), df["__r"].tolist()):
    try: si = int(float(s))
    except Exception: continue
    if 1 <= si <= 114: sur.setdefault(si, []).append(r)
allroots = Counter(w for ay in sur.values() for r in ay for w in r)
TOPDROP = set(w for w, _ in allroots.most_common(15))

# ordinary pooled -> pseudo-ayat (8 tokens each)
otoks = []
for fn in ("ar_tabari", "ar_classical2", "ar_novel", "ar_news"):
    for ln in open("corpus/%s.txt" % fn, encoding="utf-8", errors="ignore"):
        otoks += [nl(x) for x in WA.findall(ln) if nl(x)]
opseudo = [otoks[i:i+8] for i in range(0, len(otoks) - 8, 8)]
print("[%.1fs] Quran surahs=%d ; ordinary pseudo-ayat=%d" % (time.time()-t0, len(sur), len(opseudo)))

def blocks(ayat, B):
    n = len(ayat); idx = np.linspace(0, n, B + 1).astype(int); out = []
    for j in range(B):
        s = set()
        for k in range(idx[j], idx[j+1]): s |= set(w for w in ayat[k] if w not in TOPDROP)
        out.append(s)
    return out
def jac(a, b): return 0.0 if not a or not b else len(a & b) / len(a | b)
def ring(bl): B = len(bl); return np.mean([jac(bl[i], bl[B-1-i]) for i in range(B//2)])
def ringz(bl, R=300):
    real = ring(bl); B = len(bl); nu = np.empty(R)
    for t in range(R): nu[t] = ring([bl[p] for p in rng.permutation(B)])
    return (real - nu.mean()) / (nu.std() + 1e-9)
def gap(a, b): return (a.mean()-b.mean())/(np.sqrt((a.var()+b.var())/2)+1e-9)

print("\nMULTI-SCALE RING SCAN  (Quran surahs vs ordinary pseudo-surahs)")
print(" B  | Qz_mean Qz>2%% (nQ) | Oz_mean Oz>2%% (nO) | gap")
for B in (4, 6, 8, 12):
    QZ = [ringz(blocks(ay, B)) for ay in sur.values() if len(ay) >= B]
    QZ = np.array(QZ)
    # ordinary pseudo-surahs sized to ~median Quran surah length in pseudo-ayat
    med = int(np.median([len(ay) for ay in sur.values() if len(ay) >= B]))
    step = max(med, B)
    OZ = []
    for i in range(0, len(opseudo) - step, step):
        OZ.append(ringz(blocks(opseudo[i:i+step], B)))
    OZ = np.array(OZ)
    print(" %2d | %+.2f  %3.0f%% (%3d) | %+.2f  %3.0f%% (%3d) | %+.1fsd"
          % (B, QZ.mean(), 100*np.mean(QZ>2), len(QZ), OZ.mean(), 100*np.mean(OZ>2), len(OZ), gap(QZ, OZ)))
print("\n[total %.1fs]" % (time.time()-t0))
