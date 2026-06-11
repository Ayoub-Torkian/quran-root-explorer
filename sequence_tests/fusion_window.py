"""DoE D1 — defensible window-fusion at ONE grain: window-of-8-units, rate-based features (no length leak),
logistic 5-fold CV, Qur'an vs ordinary Arabic. Reports per-feature univariate AUC + fused AUC + drop-one-out.
RESULT: dominated by rhyme-persistence (univariate AUC 0.863); fused 0.875 (no synergy); other features ≈0
contribution. Principled: survivors live at different grains (fāṣila #63 corpus-level; muqaṭṭaʿāt sūra-level)
so a single-grain classifier can't fuse them — the honest fusion is the conceptual synthesis + the #35 cell.
Caveats: ord n=53 windows; vs ordinary is the easy comparator (no rhyme).
"""
import os, re, sys, warnings
import numpy as np
warnings.filterwarnings("ignore")
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_auc_score
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); import analysis as A
from analysis import COL_SURFACE as SF
DIA = re.compile(r"[ً-ْٰـ]"); WA = re.compile(r"[^\W\d_]+", re.UNICODE)
def nrm(t):
    t = DIA.sub("", str(t)); t = re.sub(r"[آأإٱ]", "ا", t); t = re.sub(r"[ىئ]", "ي", t)
    t = t.replace("ة", "ه").replace("ؤ", "و"); return WA.findall(t)
def is_attr(w): return (len(w) == 4 and w[2] in "ايو") or (len(w) >= 5 and (w.endswith("ين") or w.endswith("ون")))
def feats(units):
    units = [u for u in units if len(u) >= 2]; X = []
    for st in range(0, len(units) - 8, 8):
        w = units[st:st + 8]; ends = [u[-1] for u in w]; allw = [t for u in w for t in u]
        ec = {}
        for e in ends: ec[e[-2:]] = ec.get(e[-2:], 0) + 1
        ttr = len(set(allw)) / len(allw); lens = np.array([len(u) for u in w])
        X.append([max(ec.values()) / len(ends), np.mean([is_attr(e) for e in ends]), 1 - ttr, ttr,
                  lens.std() / lens.mean() if lens.mean() else 0])
    return np.array(X)
def main():
    df = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")).df
    q = [nrm(df.iloc[i][SF]) for i in range(len(df))]
    SENT = re.compile(r"[.!؟?\n،؛:]+"); CP = os.path.join(ROOT, "sequence_tests", "corpus")
    def comp(names):
        txt = "".join("\n" + open(os.path.join(CP, n + ".txt"), encoding="utf-8", errors="ignore").read() for n in names if os.path.exists(os.path.join(CP, n + ".txt")))
        return [nrm(s) for s in SENT.split(txt)]
    Xq = feats(q); Xo = feats(comp(["ar_tabari", "ar_classical2", "ar_novel", "ar_news", "ar_news2"]))
    names = ["rhyme-persistence", "attr-ending", "local-rep", "variety(TTR)", "len-CV"]
    X = np.vstack([Xq, Xo]); y = np.r_[np.ones(len(Xq)), np.zeros(len(Xo))]
    print(f"windows: Qur'an {len(Xq)}, ord {len(Xo)}")
    for j, nm in enumerate(names):
        a = roc_auc_score(y, X[:, j]); print(f"  {nm:18s} AUC={max(a,1-a):.3f}")
    clf = LogisticRegression(max_iter=1000); auc = cross_val_score(clf, X, y, cv=5, scoring="roc_auc").mean()
    print(f"FUSED AUC={auc:.3f}")
    for j, nm in enumerate(names):
        a = cross_val_score(clf, np.delete(X, j, 1), y, cv=5, scoring="roc_auc").mean()
        print(f"  without {nm:18s} AUC={a:.3f} (Δ={auc-a:+.3f})")

if __name__ == "__main__":
    main()
