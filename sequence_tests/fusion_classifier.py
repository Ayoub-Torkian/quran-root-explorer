import re, time, warnings
import numpy as np, pandas as pd
from collections import Counter
warnings.filterwarnings("ignore")
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import roc_auc_score
ROOT = "/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2"
rng = np.random.default_rng(13); t0 = time.time()
_DIA = re.compile(r"[ً-ٰٟۖ-ۭ]"); _TAT = re.compile("ـ"); WA = re.compile(r"[^\W\d_]+", re.UNICODE)
def nl(t):
    t = _TAT.sub("", _DIA.sub("", str(t)))
    t = re.sub(r"[آأإٱ]", "ا", t); t = re.sub(r"[ىی]", "ي", t); t = re.sub(r"[ةھ]", "ه", t)
    return t.replace("ک", "ك").replace("ؤ", "ء").replace("ئ", "ء").strip()
def words(s): return [w for w in WA.findall(nl(str(s))) if w]   # strip diacritics FIRST, then tokenize
def yuleK(w):
    c = Counter(w); N = len(w); vi = Counter(c.values())
    return 1e4 * (sum(v*(i*i) for i, v in vi.items()) - N) / (N*N + 1e-9)
def crep(toks, n=12):
    s = " ".join(toks)
    if len(s) <= n: return 0.0
    g = Counter(s[i:i+n] for i in range(len(s)-n)); return 1 - len(g)/max(len(s)-n, 1)
def feats(units):              # units = list of token-lists
    flat = [w for u in units for w in u]
    if len(flat) < 30 or len(units) < 4: return None
    ends = [u[-1][-2:] if u and len(u[-1]) >= 2 else (u[-1] if u else "") for u in units]
    ec = Counter([e for e in ends if e]); dom = max(ec.values())/len(ends) if ends else 0
    ulen = np.array([len(u) for u in units])
    wl = np.array([len(w) for w in flat])
    top = set(w for w, _ in Counter(flat).most_common(15))
    content = [w for w in flat if w not in top]
    return dict(rhyme=dom,
                unit_cv=ulen.std()/(ulen.mean()+1e-9),
                std_wl=wl.std(),
                frac_long=float(np.mean(wl >= 7)),
                rep12=crep(content, 12),
                yuleK=yuleK(flat))

# ---- Quran: units=ayat per surah ----
raw = pd.read_excel(ROOT + "/Book6.xlsx", header=None, nrows=8); hdr = 0
for i in range(len(raw)):
    if raw.iloc[i].map(lambda x: nl(x)).str.contains("سوره").any(): hdr = i; break
df = pd.read_excel(ROOT + "/Book6.xlsx", header=hdr); df.columns = [str(c).strip() for c in df.columns]
scol = [c for c in df.columns if "سوره" in nl(c) and "اسم" not in nl(c)][0]
tcol = [c for c in df.columns if "متن" in nl(c) and "توكن" not in nl(c)][0]  # FULL-WORD diacritized col (apples-to-apples)
print("Quran word col:", repr(tcol))
sur = {}
for s, txt in zip(df[scol].tolist(), df[tcol].tolist()):
    try: si = int(float(s))
    except Exception: continue
    if 1 <= si <= 114: sur.setdefault(si, []).append(words(txt))
Qrows = [feats(ay) for ay in sur.values()]; Qrows = [r for r in Qrows if r]

# ---- poetry: units=lines, windows of 24 lines step 12 ----
plines = [words(ln) for ln in open("corpus/ar_poetry.txt", encoding="utf-8", errors="ignore") if words(ln)]
Lrows = []
for i in range(0, len(plines) - 24, 12):
    r = feats(plines[i:i+24]); 
    if r: Lrows.append(r)

# ---- prose: units=8-word pseudo-ayat, windows of 24 units step 12 ----
SENT = re.compile(r"[.!?\u061f\u061b\n]+")
psents = []
for fn in ("ar_tabari", "ar_classical2", "ar_novel", "ar_news"):
    raw_txt = open("corpus/%s.txt" % fn, encoding="utf-8", errors="ignore").read()
    for seg in SENT.split(raw_txt):
        w = words(seg)
        if len(w) >= 3: psents.append(w)
Prows = []
for i in range(0, len(psents) - 16, 8):
    r = feats(psents[i:i+16])
    if r: Prows.append(r)

FEATS = ["rhyme", "unit_cv", "std_wl", "frac_long", "rep12", "yuleK"]
def mat(rows): return np.array([[r[f] for f in FEATS] for r in rows])
Q, L, P = mat(Qrows), mat(Lrows), mat(Prows)
print("[%.1fs] windows: Quran=%d poetry=%d prose=%d" % (time.time()-t0, len(Q), len(L), len(P)))
def g(a, b): return (a.mean()-b.mean())/(np.sqrt((a.var()+b.var())/2)+1e-9)
print("\nPER-AXIS sd-gaps (Quran vs each) -- shows no single axis separates Quran from BOTH:")
print("  feature   | Q mean | vs poetry | vs prose")
for j, f in enumerate(FEATS):
    print("  %-9s | %6.3f | %+8.1f | %+7.1f" % (f, Q[:, j].mean(), g(Q[:, j], L[:, j]), g(Q[:, j], P[:, j])))

# ===== multivariate: Quran vs (poetry+prose) =====
X = np.vstack([Q, L, P]); y = np.array([1]*len(Q) + [0]*(len(L)+len(P)))
clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, class_weight="balanced"))
cv = StratifiedKFold(5, shuffle=True, random_state=0)
auc = cross_val_score(clf, X, y, cv=cv, scoring="roc_auc")
print("\nQURAN vs (poetry+prose):")
print("  per-feature single AUC (Quran vs rest):")
for j, f in enumerate(FEATS):
    print("     %-9s AUC=%.3f" % (f, max(roc_auc_score(y, X[:, j]), roc_auc_score(y, -X[:, j]))))
print("  MULTIVARIATE 5-fold AUC = %.3f +/- %.3f" % (auc.mean(), auc.std()))
# label-shuffle null
nulls = []
for _ in range(30):
    yp = rng.permutation(y); nulls.append(cross_val_score(clf, X, yp, cv=cv, scoring="roc_auc").mean())
print("  label-shuffle null AUC  = %.3f +/- %.3f  (expect ~0.5)" % (np.mean(nulls), np.std(nulls)))

# interpretable conjunction: rhyme + unit_cv only
ri2, ci2 = FEATS.index("rhyme"), FEATS.index("unit_cv")
X2 = X[:, [ri2, ci2]]
auc2 = cross_val_score(clf, X2, y, cv=cv, scoring="roc_auc")
print("\n  INTERPRETABLE 2-axis (rhyme + unit_cv) 5-fold AUC = %.3f +/- %.3f" % (auc2.mean(), auc2.std()))
print("    (rhyme alone AUC=%.3f, unit_cv alone AUC=%.3f -> conjunction beats each)" % (
    max(roc_auc_score(y, X[:, ri2]), roc_auc_score(y, -X[:, ri2])),
    max(roc_auc_score(y, X[:, ci2]), roc_auc_score(y, -X[:, ci2]))))
# ===== the 2-axis cell: high rhyme AND irregular meter (unit_cv) =====
ri, ci = FEATS.index("rhyme"), FEATS.index("unit_cv")
rthr = np.median(P[:, ri]); cthr = np.median(L[:, ci])   # prose-rhyme median, poetry-meter median
def cell(M): return np.mean((M[:, ri] > rthr) & (M[:, ci] > cthr))
print("\n2-AXIS CELL (rhyme>prose-median AND unit_cv>poetry-median = 'rhymes like verse, irregular like prose'):")
print("  Quran %.0f%% | poetry %.0f%% | prose %.0f%%" % (100*cell(Q), 100*cell(L), 100*cell(P)))
print("\n[total %.1fs]" % (time.time()-t0))
