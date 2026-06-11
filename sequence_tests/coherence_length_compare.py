"""E1-comparator — is local coherence DISTINCTIVE? Coherence-length decay on SURFACE words per corpus
(lag-L cosine within document; ratio lag1/baseline). RESULT: NOT distinctive — ordinary Arabic has HIGHER
local coherence (ratio 1.82 > Qur'an 1.50; abs neighbour-similarity 0.099 > 0.045). Tempers #57: canonical-
order coherence is internally real but not cross-text distinctive. The Qur'an's coherence is long-range
(return, #42), not local flow. saj' baseline degenerate (unreliable). Divinely-rooted comparison on surface words.
"""
import os, re, sys, warnings
import numpy as np
warnings.filterwarnings("ignore")
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); import analysis as A
from analysis import COL_SURFACE as SF, COL_SURAH as S, COL_AYAH as AY
rng = np.random.default_rng(1)
DIA = re.compile(r"[ً-ْٰـ]"); WA = re.compile(r"[^\W\d_]+", re.UNICODE)
def nrm(t):
    t = DIA.sub("", str(t)); t = re.sub(r"[آأإٱ]", "ا", t); t = re.sub(r"[ىئ]", "ي", t)
    t = t.replace("ة", "ه").replace("ؤ", "و"); return WA.findall(t)
def decay(docs, label):
    units = [u for d in docs for u in d]
    if sum(len(d) for d in docs) < 80: print(f"  {label:11s} too few"); return
    V = normalize(TfidfVectorizer(analyzer=str.split, min_df=2).fit_transform([" ".join(u) if u else "x" for u in units]).toarray())
    pos = 0; di = []
    for d in docs: di.append(list(range(pos, pos + len(d)))); pos += len(d)
    lag = lambda L: np.mean([float(V[ix[i]] @ V[ix[i + L]]) for ix in di for i in range(len(ix) - L)] or [np.nan])
    base = [float(V[ix[a]] @ V[ix[b]]) for ix in di if len(ix) >= 2 for a, b in [rng.choice(len(ix), 2, replace=False)]]
    bl = np.mean(base) if base else np.nan; l1 = lag(1)
    print(f"  {label:11s} lag1={l1:.4f} lag3={lag(3):.4f} lag5={lag(5):.4f} base={bl:.4f} ratio={l1/bl if bl else float('nan'):.2f}")
def main():
    df = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")).df
    sur = np.array([int(df.iloc[i][S]) for i in range(len(df))]); ay = np.array([float(df.iloc[i][AY]) for i in range(len(df))])
    qd = []
    for s in range(1, 115):
        idx = np.where(sur == s)[0]
        if len(idx): qd.append([nrm(df.iloc[i][SF]) for i in idx[np.argsort(ay[idx])]])
    SENT = re.compile(r"[.!؟?\n،؛:]+"); CP = os.path.join(ROOT, "sequence_tests", "corpus")
    def comp(names):
        out = []
        for n in names:
            p = os.path.join(CP, n + ".txt")
            if os.path.exists(p): out.append([nrm(s) for s in SENT.split(open(p, encoding="utf-8", errors="ignore").read()) if nrm(s)])
        return out
    decay(qd, "QURAN")
    decay(comp(["ar_tabari", "ar_classical2", "ar_novel", "ar_news", "ar_news2"]), "ord-Arabic")
    decay(comp(["ar_poetry", "ar_poetry_b", "ar_poetry_c"]), "poetry")
    decay(comp(["ar_sajprose", "ar_saj_hariri"]), "saj'")

if __name__ == "__main__":
    main()
