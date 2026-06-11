"""#75 — CHARACTERIZE the nuzūl-only latent axes (C4/C5 of #72), with a robustness gate.

DESIGN: recover #72's NMF (same seed); for the two nuzūl-leaning axes report top roots + top-loading
sūras (canonical vs nuzūl positions); GATE the temporal claim with (a) the #70 WITHIN-PERIOD control
(Meccan/Medinan trad. cut, control-only) and (b) STABILITY across 10 random-init NMF restarts (axis
matched by H-cosine>0.7; nuzūl-Moran recomputed per restart).

RESULTS — a split verdict, exactly what the battery is for:
  C4 — EARLY-MECCAN DEVOTIONAL WAVE: GATED POSITIVE.
    roots: یسر ذکر عسر صحف شقو صلی زکو غنی سعی غشو; top sūras: al-Layl(nuz 9), al-Aʿlā(8), ash-Sharḥ(12),
    al-Muddaththir(4), al-Masad(6), ʿAbasa(24), an-Najm(23), ash-Shams(26) [canonical 53–111, partly the
    87–94 run, partly interleaved]. nuzūl Moran I=+0.310: full-shuffle z=+3.59, WITHIN-PERIOD z=+3.20
    (p=0.009 — a wave INSIDE the Meccan period, not the register split). STABILITY: recovered 10/10
    restarts, nuzūl-z = +3.72±0.31. A stable, gated devotional micro-campaign of revelation-time that
    the canon partially regroups (87–94) and partially disperses.
  C5 — THE FIRST-REVELATIONS AXIS: axis STABLE, wave claim FAILS the gate.
    roots: ربب رءی صلو عطو علم کذب یتم کثر وجد نهی; top sūras: al-ʿAlaq(nuz 1), al-Qalam(2), al-Fajr(10),
    aḍ-Ḍuḥā(11), al-Kawthar(15), at-Takāthur(16), al-Māʿūn(17) — the orphan/prayer/giving cluster of the
    earliest revelations (أرأيت، يتيم، صلو، عطو). Recovered 10/10 restarts AS AN AXIS, but its temporal
    clustering varies with init: nuzūl-z = +1.59±0.78 (the reference-seed +3.5 was partly init-luck).
    FILED DESCRIPTIVE ONLY — no gated wave claim.

VERDICT: one of #72's two nuzūl-only axes survives the full battery (C4); the other is honestly demoted.
Connects #70/#71: C4 is the whole-sūra-grain counterpart of the seal campaigns — revelation-time has
topical waves the canonical order partially redistributes (E4's grouping acting on time's bursts).
CAVEATS: axes data-derived (the restart battery is the defense); nuzūl = traditional chronology;
Qur'an-internal. EVIDENCE #75. RUN DISCIPLINE: /tmp heredoc; host copy for the user.
"""
import os, sys, warnings
import numpy as np
warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import analysis as A
from analysis import COL_SURAH as S, COL_ROOTS as RR, COL_REV_ORDER as RO
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
from sklearn.decomposition import NMF

rng = np.random.default_rng(75)


def morans_I(x):
    x = np.asarray(x, float); d = x - x.mean(); den = (d ** 2).sum()
    return (len(x) / (2 * (len(x) - 1))) * (2 * (d[:-1] * d[1:]).sum() / den) if den > 0 else 0.0


def main():
    df = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")).df
    sur = np.array([int(df.iloc[i][S]) for i in range(len(df))])
    NAME = [c for c in df.columns if "اسم" in c][0]
    sname = {int(df.iloc[i][S]): str(df.iloc[i][NAME]) for i in range(len(df))}
    nuz = {}
    for i in range(len(df)):
        try:
            nuz[int(df.iloc[i][S])] = int(float(df.iloc[i][RO]))
        except Exception:
            pass
    roots_ay = [str(df.iloc[i][RR]).split() for i in range(len(df))]
    suras = list(range(1, 115))
    docs = [" ".join(r for i in np.where(sur == s)[0] for r in roots_ay[i] if r and r != "nan") for s in suras]
    tf = TfidfVectorizer(analyzer=str.split, min_df=4)
    Xd = normalize(tf.fit_transform(docs)).toarray()
    voc = np.array(tf.get_feature_names_out())
    nm = NMF(n_components=8, init="nndsvda", random_state=72, max_iter=600)
    W = nm.fit_transform(Xd); H = nm.components_
    nuz_order = sorted(suras, key=lambda s: nuz.get(s, 999))
    nuz_rank = {s: r for r, s in enumerate(nuz_order)}
    mecc = np.array([nuz_rank[s] < 86 for s in suras])
    for k in (3, 4):
        w = W[:, k]; top = np.argsort(-w)[:10]
        print("=" * 78)
        print(f"C{k+1} roots:", " ".join(voc[np.argsort(-H[k])][:10]))
        for t in top:
            s = t + 1
            print(f"   {sname[s]:<12s} can={s:3d}  nuz={nuz.get(s, '-'):>3}  score={w[t]:.3f}")
        v = np.array([w[s - 1] for s in nuz_order]); m = np.array([mecc[s - 1] for s in nuz_order])
        obs = morans_I(v); null, nullW = [], []
        for _ in range(3000):
            null.append(morans_I(rng.permutation(v)))
            vv = v.copy(); vv[m] = rng.permutation(vv[m]); vv[~m] = rng.permutation(vv[~m])
            nullW.append(morans_I(vv))
        null, nullW = np.array(null), np.array(nullW)
        print(f"   nuzūl I={obs:+.3f}: full z={(obs-null.mean())/null.std():+.2f} | "
              f"within-period z={(obs-nullW.mean())/nullW.std():+.2f} (p={np.mean(nullW>=obs):.4f})")
    print("=" * 78, "\nSTABILITY (10 random restarts, H-cosine>0.7):")
    for k in (3, 4):
        zs = []; hits = 0
        for r in range(10):
            nm2 = NMF(n_components=8, init="random", random_state=100 + r, max_iter=600)
            W2 = nm2.fit_transform(Xd); H2 = nm2.components_
            Hn = H[k] / np.linalg.norm(H[k])
            cos = (H2 / np.linalg.norm(H2, axis=1, keepdims=True)) @ Hn
            j = int(np.argmax(cos))
            if cos[j] > 0.7:
                hits += 1
                v = np.array([W2[s - 1, j] for s in nuz_order]); obs = morans_I(v)
                null = np.array([morans_I(rng.permutation(v)) for _ in range(800)])
                zs.append((obs - null.mean()) / null.std())
        print(f"  C{k+1}: recovered {hits}/10; nuzūl-z = {np.mean(zs):+.2f}±{np.std(zs):.2f}")


if __name__ == "__main__":
    main()
