"""#70 — DEPLOYMENT DYNAMICS: do other rasm features arrive in nuzūl waves like the muqaṭṭaʿāt (#67)?

QUESTION (CROSS_IMPACT D9): #67 found muqaṭṭaʿāt families deployed as temporal blocks. Generalize:
do (a) fāṣila ending-classes (#62) and (b) recurrence anchors (Mūsā/Firʿawn/Nūḥ/Ibrāhīm/ʿĪsā, #42/#43)
also cluster in revelation order? Per-sūra feature rates -> Moran's I under canonical AND nuzūl orders
(rearrangement protocol), full-shuffle null + WITHIN-PERIOD null (Meccan/Medinan as control-only human
label, traditional 86/28 nuzūl split) so the gross register shift cannot masquerade as fine waves.
TOKENIZER RULE (#43) applied: normalize FIRST (incl. ک→ك, ی→ي), then split — the first run of this
script hit exactly that trap (fragment 'endings' رون/يم/ون and a zero-count Ibrāhīm) and was corrected.

RESULTS (positive control: MUQ indicator I_nuz=+0.306 z=+3.4, within-period z=+3.2 — reproduces #51 and
shows the letter-waves are FINER than the Meccan/Medinan split):
  (a) FĀṢILA CLASSES — PARTIAL YES, two kinds:
      TRUE WAVES (survive within-period null; Bonferroni×10 ok):
        تعملون I_nuz=+0.456 z=+5.2 (within z=+3.3) · يعلمون z=+3.3 (within +3.7) · اليم z=+3.5 (within +3.1)
        مبين marginal (z=+2.3, within +2.5).
      REGISTER-ONLY (cluster at the Meccan/Medinan grain, within-period z~0):
        رحيم (z_nuz=+2.6, within +0.2) · عليم (+2.4, +0.4) · الظالمين partial (+2.9, +1.7).
  (b) RECURRENCE ANCHORS — ALL NULL (Mūsā 135x, Firʿawn 74x, Ibrāhīm 69x, Nūḥ 43x, ʿĪsā 25x):
      narrative return is temporally DISTRIBUTED, not wave-like — the book re-tells its stories
      CONTINUOUSLY across revelation time.

VERDICT: deployment-in-waves generalizes PARTIALLY and INFORMATIVELY. Some verse-seal vocabulary
deploys in fine temporal waves (beyond the register split); other seals are register-level; and the
architecture-of-return characters return throughout the timeline — reinforcing the central thesis
(return spans revelation time rather than clustering in it). CAVEATS: Meccan/Medinan proxy = the
traditional 86/28 nuzūl cut (human layer, control-only); top-10 ending-classes pre-stated by frequency
(no cherry-pick), Bonferroni applied; smooth within-period drift not fully modeled.
EVIDENCE #70. Run discipline: /tmp heredoc; host copy for the user.
"""
import re, os, sys
import numpy as np
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import analysis as A
from analysis import COL_DIACRITIZED as D, COL_SURAH as S, COL_REV_ORDER as RO

rng = np.random.default_rng(70)
_DIA = re.compile(r"[ً-ْٰـۖ-ۭ]"); WA = re.compile(r"[^\W\d_]+", re.UNICODE)


def nl(t):
    t = _DIA.sub("", str(t)); t = re.sub(r"[آأإٱ]", "ا", t); t = re.sub(r"[ىی]", "ي", t)
    t = re.sub(r"[ةھ]", "ه", t)
    return t.replace("ک", "ك").replace("ؤ", "ء").replace("ئ", "ء").strip()


def toks(t):
    return WA.findall(nl(t))


MUQ = {2, 3, 7, 10, 11, 12, 13, 14, 15, 19, 20, 26, 27, 28, 29, 30, 31, 32, 36, 38,
       40, 41, 42, 43, 44, 45, 46, 50, 68}


def morans_I(x):
    x = np.asarray(x, float); n = len(x); d = x - x.mean()
    den = np.sum(d ** 2)
    if den == 0:
        return 0.0
    return (n / (2 * (n - 1))) * (2 * np.sum(d[:-1] * d[1:]) / den)


def main():
    c = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")); df = c.df
    nuz = {}
    for i in range(len(df)):
        try:
            nuz[int(df.iloc[i][S])] = int(float(df.iloc[i][RO]))
        except Exception:
            pass
    suras = list(range(1, 115))
    tok_count = {s: 0 for s in suras}; finals = {s: Counter() for s in suras}
    ANCH = ["موسي", "فرعون", "نوح", "نوحا", "ابراهيم", "عيسي"]
    anch = {a: {s: 0 for s in suras} for a in ANCH}
    nfin = Counter()
    for i in range(len(df)):
        s = int(df.iloc[i][S]); tt = toks(df.iloc[i][D])
        if not tt:
            continue
        tok_count[s] += len(tt)
        finals[s][tt[-1]] += 1; nfin[tt[-1]] += 1
        for a in ANCH:
            anch[a][s] += sum(1 for w in tt if w.endswith(a))
    nayah = {s: sum(finals[s].values()) for s in suras}
    TOPF = [w for w, _ in nfin.most_common(10)]
    print("top ending-words:", TOPF, [nfin[w] for w in TOPF])
    print("anchor totals:", {a: sum(anch[a].values()) for a in ANCH})

    feats = {"MUQ-indicator(ctrl)": np.array([1.0 if s in MUQ else 0.0 for s in suras])}
    for w in TOPF:
        feats[f"end:{w}"] = np.array([finals[s][w] / max(nayah[s], 1) for s in suras])
    for a in ANCH:
        feats[f"anchor:{a}"] = np.array([1000 * anch[a][s] / max(tok_count[s], 1) for s in suras])

    nuz_order = sorted(suras, key=lambda s: nuz.get(s, 999))
    nuz_rank = {s: r for r, s in enumerate(nuz_order)}
    mecc = np.array([nuz_rank[s] < 86 for s in suras])  # human label, CONTROL-ONLY
    NS = 5000
    print(f"\n{'feature':22s} {'I_can':>7s} {'z_can':>6s} | {'I_nuz':>7s} {'z_nuz':>6s} {'p':>7s} | within-period")
    for name, x in feats.items():
        out = {}
        for lab, order in (("can", suras), ("nuz", nuz_order)):
            v = np.array([x[s - 1] for s in order]); obs = morans_I(v)
            null = np.array([morans_I(rng.permutation(v)) for _ in range(NS)])
            out[lab] = (obs, (obs - null.mean()) / (null.std() + 1e-12), np.mean(null >= obs))
        v = np.array([x[s - 1] for s in nuz_order]); m = np.array([mecc[s - 1] for s in nuz_order])
        obs = morans_I(v); null = []
        for _ in range(NS):
            vv = v.copy(); vv[m] = rng.permutation(vv[m]); vv[~m] = rng.permutation(vv[~m])
            null.append(morans_I(vv))
        null = np.array(null)
        zw = (obs - null.mean()) / (null.std() + 1e-12); pw = np.mean(null >= obs)
        (Ic, zc, _), (In, zn, pn) = out["can"], out["nuz"]
        print(f"{name:22s} {Ic:+.3f} {zc:+6.1f} | {In:+.3f} {zn:+6.1f} {pn:7.4f} | z={zw:+.1f} (p={pw:.4f})")


if __name__ == "__main__":
    main()
