import re, time, warnings
import numpy as np, pandas as pd
warnings.filterwarnings("ignore")
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize
ROOT = "/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2"
rng = np.random.default_rng(5); t0 = time.time()
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
df["__doc"] = df[rcol].fillna("").map(lambda s: " ".join(nl(w) for w in WA.findall(str(s)) if nl(w)))

# ordered ayah docs grouped by surah
sur_docs = {}
for s, d in zip(df[scol].tolist(), df["__doc"].tolist()):
    try: si = int(float(s))
    except Exception: continue
    if 1 <= si <= 114: sur_docs.setdefault(si, []).append(d)

def embed(docs, k=100):
    vec = TfidfVectorizer(analyzer=str.split, min_df=2)
    X = vec.fit_transform(docs)
    k = min(k, X.shape[1] - 1, X.shape[0] - 1)
    if k < 5: return None
    V = TruncatedSVD(n_components=k, random_state=0).fit_transform(X)
    return normalize(V)   # L2

def blocks_vec(vecs, B):
    n = len(vecs); idx = np.linspace(0, n, B + 1).astype(int); out = []
    for j in range(B):
        seg = vecs[idx[j]:idx[j + 1]]
        v = seg.mean(0) if len(seg) else np.zeros(vecs.shape[1])
        nrm = np.linalg.norm(v); out.append(v / nrm if nrm > 0 else v)
    return np.array(out)
def ring(bv):
    B = len(bv); return float(np.mean([bv[i] @ bv[B - 1 - i] for i in range(B // 2)]))
def ringz(bv, R=300):
    real = ring(bv); B = len(bv); nu = np.empty(R)
    for t in range(R): nu[t] = ring(bv[rng.permutation(B)])
    return (real - nu.mean()) / (nu.std() + 1e-9)
def gap(a, b): return (a.mean() - b.mean()) / (np.sqrt((a.var() + b.var()) / 2) + 1e-9)

# Quran: embed ALL ayat in one global LSA space, then map back per surah (order preserved)
all_docs, owner = [], []
for s in sorted(sur_docs): 
    for d in sur_docs[s]: all_docs.append(d); owner.append(s)
QV = embed(all_docs, 100)
print("[%.1fs] Quran ayat embedded: %s" % (time.time() - t0, QV.shape))
qvecs = {}
pos = 0
for s in sorted(sur_docs):
    n = len(sur_docs[s]); qvecs[s] = QV[pos:pos + n]; pos += n

# ordinary pooled -> pseudo-ayat docs, own LSA space
otoks = []
for fn in ("ar_tabari", "ar_classical2", "ar_novel", "ar_news"):
    for ln in open("corpus/%s.txt" % fn, encoding="utf-8", errors="ignore"):
        otoks += [nl(x) for x in WA.findall(ln) if nl(x)]
opsa = [" ".join(otoks[i:i + 8]) for i in range(0, len(otoks) - 8, 8)]
OV = embed(opsa, 80)
print("[%.1fs] ordinary pseudo-ayat embedded: %s" % (time.time() - t0, OV.shape))

# ---- GATE (semantic pipeline) ----
print("\n===== SEMANTIC DETECTOR GATE =====")
base = blocks_vec(OV[:80], 8)
palin = np.array(list(base[:4]) + list(base[3::-1]))
print("  (1) synthetic palindrome ring-z = %+.1f  [expect >>2]" % ringz(palin))
print("  (2) degradation ladder:")
for frac in (0.0, 0.25, 0.5, 1.0):
    bl = palin.copy(); k = int(frac * len(bl))
    if k >= 2:
        ids = rng.choice(len(bl), k, replace=False); v = bl[ids].copy(); rng.shuffle(v); bl[ids] = v
    print("        shuffle %3d%%: ring-z = %+.1f" % (int(frac * 100), ringz(bl)))

print("\n===== MULTI-SCALE SEMANTIC RING: Quran vs ordinary =====")
print(" B  | Qz_mean Qz>2%% (nQ) | Oz_mean Oz>2%% (nO) | gap")
for B in (4, 6, 8, 12):
    QZ = np.array([ringz(blocks_vec(qvecs[s], B)) for s in sorted(sur_docs) if len(qvecs[s]) >= B])
    med = int(np.median([len(qvecs[s]) for s in sur_docs if len(qvecs[s]) >= B]))
    step = max(med, B)
    OZ = np.array([ringz(blocks_vec(OV[i:i + step], B)) for i in range(0, len(OV) - step, step)])
    print(" %2d | %+.2f  %3.0f%% (%3d) | %+.2f  %3.0f%% (%3d) | %+.1fsd"
          % (B, QZ.mean(), 100 * np.mean(QZ > 2), len(QZ), OZ.mean(), 100 * np.mean(OZ > 2), len(OZ), gap(QZ, OZ)))
    if B == 8:
        order = np.argsort(-QZ); ss = [s for s in sorted(sur_docs) if len(qvecs[s]) >= B]
        print("     top ring surahs @B=8:", ", ".join("S%d(%.1f)" % (ss[i], QZ[i]) for i in order[:10]))
print("\n[total %.1fs]" % (time.time() - t0))
