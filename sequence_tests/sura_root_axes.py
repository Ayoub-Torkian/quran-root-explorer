"""#72 — SIGNAL-GEOMETRY: SVD/NMF latent axes of the sūra×root matrix (114×857, 49,330 tokens).

THREE RESULTS:
 (1) SPECTRAL DIFFERENTIATION: effective rank (entropy of normalized σ²) of the log-tf row-normalized
     matrix = 28.51 vs token-reassignment null 20.20±0.24 (global root tokens shuffled, re-cut to sūra
     sizes — preserves sūra lengths AND root totals): z=+34.5. Sūras carry genuinely distinct root
     profiles far beyond frequency+length. BOUNDARY: register-level descriptive — any topical book
     should differentiate; no cross-text comparator run.
     GATE (bidirectional): planted exact rank-4 block matrix reads 4.0 (5.25 with noise);
     unstructured Poisson reads ~35.8 — the metric detects structure in both directions.
 (2) NMF AXES (k=8, TF-IDF, nndsvda) are interpretable: C1 narrative/prophetic (قول قوم ءتی جعل) ·
     C2 creed/faith-polemic (ءمن کفر رسل غفر) · C3 eschatology (یوم کذب ویل فجر) · C4 dhikr/ease
     devotional (یسر ذکر عسر صحف) · C6 legal/family (وصی ولد مول) · C7 REFUGE (وسوس حسد عوذ زلزل —
     the Muʿawwidhāt component, cf. #57) · C8 worship/dīn (عبد دین صرط).
 (3) ORDER TYPOLOGY of the axes (Moran's I of component scores over canonical AND nuzūl orders,
     2000-perm nulls; 16 tests, Bonferroni z≳3 read as safe):
       BOTH orders:      C1 (can z=+5.4 / nuz +6.1) · C2 (+5.3/+6.3) · C7 (+5.6/+3.4)
       CANONICAL-leaning: C3 eschatology (+5.3 vs +2.2) — grouped in the muṣḥaf beyond its temporal order
       NUZŪL-only:        C5 (+0.6/+3.5) and C4 (+2.7/+3.7) — revelation-time waves INVISIBLE in canon
       NEITHER:           C8; C6 canonical-marginal (+2.7/−0.6)
     Reading: the latent thematic axes are themselves ORDER-TYPED — some arranged canonically, some
     temporally, the great creed/narrative axes in both. Connects #57 (canonical adjacency), E4
     (grouping>chronology), #70/#71 (temporal waves) in one decomposition. Signal-geometry register
     (IDEA_SIGNALS_GEOMETRY): the pointer/mask formulation at sūra×root grain delivered.
CAVEATS: NMF axes are data-derived (exploratory typology, permutation-nulled per axis); k=8 pre-stated;
PPMI/TF-IDF normalization per the frequency rule. Qur'an-internal. EVIDENCE #72.
RUN DISCIPLINE: /tmp heredoc; host copy for the user.
"""
import os, sys, warnings
import numpy as np
warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import analysis as A
from analysis import COL_SURAH as S, COL_ROOTS as RR, COL_REV_ORDER as RO
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.preprocessing import normalize
from sklearn.decomposition import NMF

rng = np.random.default_rng(72)


def eff_rank(M):
    Mt = normalize(np.log1p(M))
    sv = np.linalg.svd(Mt, compute_uv=False)
    p = sv ** 2 / np.sum(sv ** 2)
    return float(np.exp(-(p * np.log(p + 1e-15)).sum())), sv


def morans_I(x):
    x = np.asarray(x, float); d = x - x.mean(); den = (d ** 2).sum()
    return (len(x) / (2 * (len(x) - 1))) * (2 * (d[:-1] * d[1:]).sum() / den) if den > 0 else 0.0


def main():
    df = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")).df
    sur = np.array([int(df.iloc[i][S]) for i in range(len(df))])
    nuz = {}
    for i in range(len(df)):
        try:
            nuz[int(df.iloc[i][S])] = int(float(df.iloc[i][RO]))
        except Exception:
            pass
    roots_ay = [str(df.iloc[i][RR]).split() for i in range(len(df))]
    suras = list(range(1, 115))
    docs = [" ".join(r for i in np.where(sur == s)[0] for r in roots_ay[i] if r and r != "nan") for s in suras]
    cv = CountVectorizer(analyzer=str.split, min_df=4)
    C = cv.fit_transform(docs).toarray().astype(float)
    print("matrix:", C.shape, "| tokens:", int(C.sum()))

    obs_er, sv = eff_rank(C)
    tok_idx = np.repeat(np.arange(C.shape[1]), C.sum(axis=0).astype(int))
    sizes = C.sum(axis=1).astype(int)
    ers = []
    for _ in range(200):
        perm = rng.permutation(tok_idx); M = np.zeros_like(C); pos = 0
        for si, nn in enumerate(sizes):
            np.add.at(M[si], perm[pos:pos + nn], 1); pos += nn
        ers.append(eff_rank(M)[0])
    ers = np.array(ers)
    print(f"EFFECTIVE RANK: obs={obs_er:.2f} null={ers.mean():.2f}±{ers.std():.2f} z={(obs_er-ers.mean())/ers.std():+.2f}")
    print(f"top-σ share: {sv[0]**2/np.sum(sv**2):.3f}")

    # GATE (bidirectional)
    B = np.zeros_like(C)
    blocks = np.array_split(np.arange(114), 4); vb = np.array_split(np.arange(C.shape[1]), 4)
    for rs, vs in zip(blocks, vb):
        prof = rng.integers(1, 6, len(vs))
        for r in rs:
            B[r, vs] = prof
    print(f"GATE planted rank-4: {eff_rank(B)[0]:.2f} (≈4) | unstructured Poisson: "
          f"{eff_rank(rng.poisson(0.5, C.shape).astype(float))[0]:.1f}")

    tf = TfidfVectorizer(analyzer=str.split, min_df=4)
    X = normalize(tf.fit_transform(docs))
    nm = NMF(n_components=8, init="nndsvda", random_state=72, max_iter=600)
    W = nm.fit_transform(X.toarray()); H = nm.components_
    voc = np.array(tf.get_feature_names_out())
    nuz_order = sorted(suras, key=lambda s: nuz.get(s, 999))
    print("\nNMF axes (top roots | Moran canonical / nuzūl, z vs 2000 perms):")
    for k in range(8):
        top = voc[np.argsort(-H[k])][:8]
        w = W[:, k]; res = []
        for order in (suras, nuz_order):
            v = np.array([w[s - 1] for s in order]); obs = morans_I(v)
            null = np.array([morans_I(rng.permutation(v)) for _ in range(2000)])
            res.append((obs, (obs - null.mean()) / (null.std() + 1e-12)))
        (Ic, zc), (In, zn) = res
        print(f"  C{k+1}: {' '.join(top)} | can I={Ic:+.2f} z={zc:+.1f} / nuz I={In:+.2f} z={zn:+.1f}")


if __name__ == "__main__":
    main()
