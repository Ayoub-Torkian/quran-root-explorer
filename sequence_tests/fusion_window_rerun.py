"""#76 — D1 FUSION RE-RUN with the fāṣila features + an AUDIT that corrected #63.

PART 1 — THE AUDIT (the run's most important outcome). While building features, a #43-class asymmetric-
tokenization confound was caught: COL_SURFACE ("توکن ریشه نحوی") is a LEMMA column, not surface text —
and #63 had computed the Qur'an's ending-repetition on LEMMAS while comparators used raw words (lemma
collapse inflates recurrence: الرحيم/رحيم/رحيما merge). RE-RUN on TRUE SURFACE (nrm of COL_DIACRITIZED):
   QURAN-surface frac-recurs>=3x = 0.179±0.032  (old lemma-grain: 0.278)
   ord 0.101±0.017 · sajʿ 0.038 · poetry 0.019
VERDICT: #63 SURVIVES its second tokenization at REDUCED magnitude — corrected headline 0.18 (surface):
still ~4.7× sajʿ and ~9× poetry; the margin vs ORDINARY narrows to ≈+2.2σ. Filed as a correction in
EVIDENCE #63 (the #43 precedent: survive-but-shrink under honest re-tokenization).
STANDING RULE (locked): cross-text surface features MUST use nrm(COL_DIACRITIZED); COL_SURFACE is a
lemma layer (fine for Qur'an-internal morphology-grain work like #62, NOT for cross-text comparison).

PART 2 — FUSION (window grain K=25, equal-N windows, 5 features, logistic 5-fold; label-perm gate ~0.5):
   features: rhyme-persistence (dominant last-char share) · ending-REUSE (≥2 within window) ·
   ending-concentration (1−TTR) · within-window self-similarity (half-window TF cosine) · wāw-initial.
   vs ORDINARY: best single = rhyme-persist 0.926; FUSED 0.945 (synergy +0.020)
   vs SAJʿ:     self-similar 1.000 (content-return: 0.407 vs 0.145 — sajʿ rhymes but does not RETURN);
                ending-reuse 0.885; FUSED 1.000 (saturated; n=12 windows — small-N flagged)
   vs POETRY:   self-similar 0.961, ending-reuse 0.882; FUSED 0.978 (synergy +0.017)
VERDICT: D1's conclusion CONFIRMED with corrected features — no meaningful statistical synergy; the
signature remains a PROFILE, not a summed score: each comparator is beaten by a DIFFERENT axis
(ordinary by rhyme-persistence; sajʿ and poetry by content-return and ending-reuse). The real fusion
stays conceptual (the seventeen-lens synthesis + the #35 conjunction cell).
Feature means (K=25): QURAN rp=0.739 reuse=0.179 conc=0.100 selfsim=0.407 waw=0.355 | ord 0.310/0.058/
0.033/0.334/0.165 | sajʿ 0.340/0.020/0.010/0.145/0.520 | poetry 0.550/0.007/0.004/0.118/0.299.
CAVEATS: comparator window counts small (12–36; equal-N enforced); waw = register feature (#45: sajʿ
exceeds). EVIDENCE #76. RUN DISCIPLINE: /tmp heredoc; host copy for the user.
"""
import os, re, sys, warnings
import numpy as np
warnings.filterwarnings("ignore")
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import analysis as A
from analysis import COL_DIACRITIZED as DC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict, StratifiedKFold
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(76)
DIA = re.compile(r"[ً-ْٰـۖ-ۭ]"); WA = re.compile(r"[^\W\d_]+", re.UNICODE)


def nrm(t):
    t = DIA.sub("", str(t)); t = re.sub(r"[آأإٱ]", "ا", t); t = re.sub(r"[ىیئ]", "ي", t)
    t = t.replace("ک", "ك").replace("ة", "ه").replace("ؤ", "و")
    return WA.findall(t)


K = 25
FN = ["rhyme-persist", "ending-reuse", "ending-conc", "self-similar", "waw-rate"]


def feats(units):
    F = []
    for a in range(0, len(units) - K + 1, K):
        w = units[a:a + K]
        ends = [u[-1] for u in w]
        f1 = max(Counter(e[-1] for e in ends).values()) / K
        ce = Counter(ends)
        f2 = np.mean([ce[e] >= 2 for e in ends])
        f3 = 1 - len(ce) / K
        h1 = Counter(t for u in w[:K // 2] for t in u); h2 = Counter(t for u in w[K // 2:] for t in u)
        keys = set(h1) | set(h2)
        v1 = np.array([h1[t] for t in keys], float); v2 = np.array([h2[t] for t in keys], float)
        f4 = float(v1 @ v2 / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-9))
        f5 = np.mean([u[0].startswith("و") for u in w])
        F.append([f1, f2, f3, f4, f5])
    return np.array(F)


def main():
    df = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")).df
    q = [u for u in (nrm(df.iloc[i][DC]) for i in range(len(df))) if len(u) >= 4]
    SENT = re.compile(r"[.!؟?\n،؛:]+"); CP = os.path.join(ROOT, "sequence_tests", "corpus")

    def comp(names):
        txt = "".join("\n" + open(os.path.join(CP, n + ".txt"), encoding="utf-8", errors="ignore").read()
                      for n in names if os.path.exists(os.path.join(CP, n + ".txt")))
        return [u for u in (nrm(s) for s in SENT.split(txt)) if len(u) >= 4]

    corp = {"QURAN": q,
            "ord": comp(["ar_tabari", "ar_classical2", "ar_novel", "ar_news", "ar_news2"]),
            "saj": comp(["ar_sajprose", "ar_saj_hariri"]),
            "poetry": comp(["ar_poetry", "ar_poetry_b", "ar_poetry_c"])}
    FW = {k: feats(v) for k, v in corp.items()}
    for k, v in FW.items():
        print(k, "windows:", len(v), "| means:", " ".join(f"{f}={v[:, j].mean():.3f}" for j, f in enumerate(FN)))

    def table(A_, B_, lab):
        n = min(len(A_), len(B_))
        ia = rng.choice(len(A_), n, replace=False); ib = rng.choice(len(B_), n, replace=False)
        X = np.vstack([A_[ia], B_[ib]]); y = np.array([1] * n + [0] * n)
        Xs = StandardScaler().fit_transform(X)
        print(f"\n== QURAN vs {lab} (equal-N {n}) ==")
        best = 0
        for j, f in enumerate(FN):
            a = roc_auc_score(y, X[:, j]); a = max(a, 1 - a); best = max(best, a)
            print(f"  {f:14s} AUC={a:.3f}")
        cv = StratifiedKFold(5, shuffle=True, random_state=76)
        pr = cross_val_predict(LogisticRegression(max_iter=1000), Xs, y, cv=cv, method="predict_proba")[:, 1]
        fused = roc_auc_score(y, pr)
        null = [roc_auc_score(rng.permutation(y), pr) for _ in range(200)]
        print(f"  FUSED={fused:.3f} | best single={best:.3f} | synergy={fused-best:+.3f} | "
              f"perm-null {np.mean(null):.3f}±{np.std(null):.3f}")

    table(FW["QURAN"], FW["ord"], "ORDINARY")
    table(FW["QURAN"], FW["saj"], "SAJ'")
    table(FW["QURAN"], FW["poetry"], "POETRY")


if __name__ == "__main__":
    main()
