"""#77 — REFERENT-SPLIT re-audit of #62 (D11, the #74 method catch) + the D12 COL_SURFACE sweep verdict.

QUESTION: #74 showed ending-word classes are REFERENT-MIXED (عليم caps God AND the sorcerer). Does #62's
content-fit survive when each strong class is split by referent — or was it riding the mixture?
METHOD: pre-stated divine-marker rule (a token matching الله/رب*/هو/انه-family within the LAST 6 surface
words, nl-normalized); split each of #62's top-16 morphology-grain classes into divine/other; re-run the
exact #62 cohesion statistic (body root-TF-IDF cosine, ending-root stripped) per subset vs 600 same-N nulls.

RESULT: #62 PASSES — the fit survives the split ON BOTH SIDES in 15/16 classes (every subset with n≥8):
  divine subsets:  قدیر +31.2(34) · رحیم +29.6(73) · حکیم +24.7(57) · عالمین +19.2(41) · علیم +11.4(68)
  other subsets:   صادقین +27.7(34) · ألیم +16.1(40) · مؤمنین +8.2(52) · مبین +6.5(64) · عظیم +4.1(37)
REFINED READING: the fāṣila content-fit is REFERENT-GENERAL — a property of the seal SYSTEM, not of
divine naming alone. The divine-attribute seals are the strongest fitted subclasses in their divine use;
human/event seals (the ṣādiqīn-challenges, the ʿadhāb-alīm warnings) are equally fitted in theirs. The
'seal that interprets' generalizes: the verse-end names whatever the verse is about — attribute,
judgment, or human class — and the naming is content-fitted either way.
FLAG: the ن class (n=1070) is a coarse final-MORPHEME bucket (all -ūn/-īn verbs); its non-divine side is
the lone non-fit (−1.4) — segmentation granularity, recommend excluding bare-affix buckets from Lens 17
headlines. Composition estimates ride the crude (pre-stated) marker rule.

D12 SWEEP (same session): repo-wide audit of COL_SURFACE (lemma column) in cross-text scripts.
Affected filed findings: E1-comparator and #65-comparator — in BOTH the lemma layer biases IN THE
QUR'AN'S FAVOR (lemma collapse raises overlap/clustering) and the Qur'an still lost/tied → verdicts
ROBUST (conservative direction). wazn_fasila (#41-reopen, register-level non-claim): low-priority
re-check flagged. Wavelet/posdir/signals preliminary probes: no claims to protect. #63: corrected (#76).
EVIDENCE #77. RUN DISCIPLINE: /tmp heredoc; host copy for the user.
"""
import os, re, sys, warnings
import numpy as np
warnings.filterwarnings("ignore")
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import analysis as A
from analysis import COL_ROOTS as R, COL_SEGMENTED as SEG, COL_DIACRITIZED as DC

rng = np.random.default_rng(77)
_DIA = re.compile(r"[ً-ْٰـۖ-ۭ]"); WA = re.compile(r"[^\W\d_]+", re.UNICODE)


def nl(t):
    t = _DIA.sub("", str(t)); t = re.sub(r"[آأإٱ]", "ا", t); t = re.sub(r"[ىیئ]", "ي", t)
    t = re.sub(r"[ةھ]", "ه", t)
    return t.replace("ک", "ك").replace("ؤ", "ء").strip()


DIV = re.compile(r"^(الله|ولله|لله|بالله|فالله|والله|تالله|هو|وهو|انه|وانه|فانه)$|^رب(ي|ك|ه|ها|نا|كم|هم)?$")


def main():
    df = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")).df
    roots = [[w for w in str(df.iloc[i][R]).split() if w and w != 'nan'] for i in range(len(df))]
    segs = [[w for w in str(df.iloc[i][SEG]).split() if w] for i in range(len(df))]
    surf = [WA.findall(nl(df.iloc[i][DC])) for i in range(len(df))]
    keep = [i for i in range(len(df)) if len(roots[i]) >= 4 and segs[i] and surf[i]]
    end = [segs[i][-1] for i in keep]
    body = [" ".join(w for w in roots[i][:-1] if w != roots[i][-1]) for i in keep]
    dv = [any(DIV.match(w) for w in surf[i][-6:]) for i in keep]
    V = normalize(TfidfVectorizer(analyzer=str.split, min_df=2)
                  .fit_transform([b if b.strip() else "x" for b in body]).toarray())

    def coh(ix):
        if len(ix) < 2:
            return np.nan
        M = V[ix] @ V[ix].T; iu = np.triu_indices(len(ix), 1)
        return M[iu].mean()

    allidx = np.arange(len(keep))
    ec = Counter(end); top = [w for w, n in ec.most_common(60) if n >= 15][:16]
    print(f"{'class':12s} {'n':>4s} {'%div':>5s} | z_div(n)  z_oth(n)")
    for w in top:
        ix = [k for k in range(len(keep)) if end[k] == w]
        ixd = [k for k in ix if dv[k]]; ixo = [k for k in ix if not dv[k]]
        zs = []
        for sub in (ixd, ixo):
            if len(sub) >= 8:
                o = coh(sub)
                null = np.array([coh(rng.choice(allidx, len(sub), replace=False)) for _ in range(600)])
                zs.append(((o - null.mean()) / null.std(), len(sub)))
            else:
                zs.append((np.nan, len(sub)))
        (zd, nd), (zo, no) = zs
        print(f"{w:12s} {len(ix):4d} {100*len(ixd)/len(ix):4.0f}% | {zd:+6.1f}({nd:3d}) {zo:+6.1f}({no:3d})")


if __name__ == "__main__":
    main()
