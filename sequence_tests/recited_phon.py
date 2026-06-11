"""MODALITY 49 / Lens 14 — RECITED / PHONOLOGICAL LAYER (the vocalized stratum; tartīl trace).

The one region text-stats structurally could not reach (Lens 6 hit this wall): syllable WEIGHT, MADD
(vowel lengthening), GHUNNA (nasalization), and syllable-count ISOCHRONY — all of which need FULLY
VOCALIZED text. We HAVE the vocalized Qur'an (COL_DIACRITIZED). The block is the COMPARATORS (ordinary
Arabic / poetry / sajʿ are unvocalized here).

STATUS:
  * DETECTOR built (rule-based syllabifier from harakat -> weight sequence + features).
  * Qur'an-INTERNAL validation DONE (no comparator needed) and POSITIVE: short Meccan surahs are more
    isochronous (syllable-count CV 0.36 vs 0.48 long); syllable-weight sequence shows significant rhythmic
    ALTERNATION vs shuffle (al-Baqara z=-10.8, al-Raḥmān z=-6.5). The recited features capture real rhythm.
  * DISTINCTIVENESS = DATA-BLOCKED: needs vocalized comparators. No diacritizer installs in the sandbox
    (mishkal unavailable; no torch for CAMeL/Shakkala) and vocalized corpora can't be fetched here.

FAIRNESS PROTOCOL (critical — avoid the gold-vs-noisy confound that inflated #42):
  - BEST: GOLD vocalized comparators (Tashkeela = vocalized Classical prose; vocalized dīwān poetry).
    Then gold-Qur'an vs gold-comparator, apples-to-apples.
  - ELSE: if comparators must be AUTO-diacritized by a tool, then STRIP the Qur'an's gold harakat and
    re-diacritize it with the SAME tool, so BOTH are in the identical (noisy) condition. Never compare
    gold-Qur'an against auto-comparators.

HOW TO COMPLETE (local): place a vocalized comparator file in sequence_tests/corpus/ as
  ar_tashkeela.txt (vocalized prose) and/or ar_poetry_voc.txt (vocalized poetry), then run this script;
  it auto-detects them and runs the equal-N comparison. See run_recited_phon.py for a guided local runner.
"""
import re, os, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); import analysis as A
from analysis import COL_DIACRITIZED as D, COL_SURAH as S
rng = np.random.default_rng(49)

SHORT = "َُِ"; SUK = "ْ"; TAN = "ًٌٍ"; LONG = "اوي"; SHAD = "ّ"
HARAKAT = SHORT + SUK + TAN + SHAD + "ٰ"

def weights(text):
    """Rule-based CV-weight syllabification of vocalized Arabic. 1 = heavy (CVV/CVC/CVN), 0 = light (CV)."""
    ch = list(str(text)); out = []
    for j, c in enumerate(ch):
        if c in SHORT or c in TAN:
            nxt = ch[j + 1] if j + 1 < len(ch) else ""
            nxt2 = ch[j + 2] if j + 2 < len(ch) else ""
            if nxt in LONG and nxt2 not in SHORT and nxt2 not in TAN: out.append(1)
            elif nxt2 == SUK or c in TAN: out.append(1)
            else: out.append(0)
    return out

def unit_features(text):
    w = weights(text)
    if len(w) < 3: return None
    s = str(text)
    nuclei = max(1, len([c for c in s if c in SHORT or c in TAN]))
    return {
        "heavy_ratio": float(np.mean(w)),
        "madd_rate":   len(re.findall("[" + SHORT + "][" + LONG + "]", s)) / nuclei,
        "ghunna_rate": (len(re.findall("[نم]" + SHAD, s)) + len(re.findall("[" + TAN + "]", s))) / max(1, len(s.split())),
        "syl_count":   float(len(w)),
        "rhythm":      _lag1(w),
    }

def _lag1(seq):
    x = np.array(seq, float)
    if x.std() == 0 or len(x) < 8: return np.nan
    return float(np.corrcoef(x[:-1], x[1:])[0, 1])

def is_vocalized(s, thresh=0.3):
    s = str(s); letters = len(re.findall(r"[ء-ي]", s))
    return letters and (len(re.findall("[" + HARAKAT + "]", s)) / letters) > thresh

# ----------------------------------------------------------------- gate (Qur'an-internal)
def gate(df):
    print("=== GATE (degradation) ===")
    txt = str(df.iloc[1][D])  # al-Fatiha 1:2
    w = weights(txt); print(f"  vocalized: weights={''.join(map(str,w))} heavy={np.mean(w):.2f} rhythm={_lag1(w):+.2f}")
    bare = re.sub("[" + HARAKAT + "]", "", txt)
    print(f"  de-diacritized -> syllables found: {len(weights(bare))} (expect ~0; feature needs harakat)")

def quran_internal(df):
    print("=== Qur'an-INTERNAL validation ===")
    syl = [weights(df.iloc[i][D]) for i in range(len(df))]
    cnt = np.array([len(s) for s in syl], float)
    sur = np.array([int(df.iloc[i][S]) for i in range(len(df))])
    def cv(pred):
        v = [cnt[sur == su].std() / cnt[sur == su].mean()
             for su in np.unique(sur) if (sur == su).sum() >= 5 and pred((sur == su).sum()) and cnt[sur == su].mean() > 0]
        return np.mean(v), len(v)
    sc, ns = cv(lambda n: n <= 20); lc, nl = cv(lambda n: n >= 100)
    print(f"  isochrony: short surahs CV={sc:.3f} (n={ns}) vs long CV={lc:.3f} (n={nl}) -> short more isochronous: {sc<lc}")
    for nm, su in [("100", 100), ("55", 55), ("2", 2)]:
        seq = [w for i in np.where(sur == su)[0] for w in syl[i]]
        obs = _lag1(seq); null = np.array([_lag1(list(rng.permutation(seq))) for _ in range(200)])
        print(f"  surah {nm} weight-rhythm z = {(obs-np.nanmean(null))/(np.nanstd(null)+1e-9):+.2f}")

# ----------------------------------------------------------------- cross-corpus (needs vocalized comparators)
def cross_corpus(df):
    CP = os.path.join(ROOT, "sequence_tests", "corpus")
    comp_files = {"voc-prose": "ar_tashkeela.txt", "voc-poetry": "ar_poetry_voc.txt", "voc-saj": "ar_saj_voc.txt"}
    present = {k: os.path.join(CP, v) for k, v in comp_files.items() if os.path.exists(os.path.join(CP, v))}
    if not present:
        print("=== CROSS-CORPUS: DATA-BLOCKED ===")
        print("  No vocalized comparator found. Place ar_tashkeela.txt / ar_poetry_voc.txt in corpus/ "
              "(see run_recited_phon.py), then re-run. FAIRNESS: gold-vs-gold, or symmetric auto-diacritize.")
        return
    SENT = re.compile(r"[.!؟?\n]+")
    def feats(units):
        rows = [unit_features(u) for u in units]; rows = [r for r in rows if r]
        return {k: np.array([r[k] for r in rows]) for k in rows[0]}
    corp = {"QURAN": feats([str(df.iloc[i][D]) for i in range(len(df))])}
    for name, path in present.items():
        units = [s for s in SENT.split(open(path, encoding="utf-8").read()) if is_vocalized(s) and len(s.split()) >= 4]
        if units: corp[name] = feats(units)
    def g(a, b): return (a.mean() - b.mean()) / (np.sqrt((a.var() + b.var()) / 2) + 1e-9)
    for feat in ("heavy_ratio", "madd_rate", "ghunna_rate", "rhythm"):
        print(f"-- {feat} --  QURAN={corp['QURAN'][feat].mean():.3f}")
        for name in corp:
            if name != "QURAN":
                print(f"   vs {name:11s} mean={corp[name][feat].mean():.3f}  g={g(corp['QURAN'][feat], corp[name][feat]):+.2f}sd")

def main():
    c = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")); df = c.df
    gate(df); quran_internal(df); cross_corpus(df)

if __name__ == "__main__":
    main()
