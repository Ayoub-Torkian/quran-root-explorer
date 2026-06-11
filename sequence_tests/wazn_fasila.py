"""CROSS-REF — re-open #41 (wazn, null corpus-wide) at the VERSE-END: is the faʿīl/attribute template
enriched at the fāṣila distinctively vs comparators' sentence-ends? Surface-word grain (crude detector).
RESULT: Qur'an has the HIGHEST absolute attribute-ending density (end 0.141, enrich 1.21×) but the
END-ENRICHMENT is SHARED with saj' (1.32×); ordinary none (0.97×), poetry depleted (0.56×). #41 stays
register-level even at the fāṣila — wazn-class PRESENCE at the end is a rhymed-register trait. Sharpens #63:
the fāṣila distinctive is the heavy REPETITION of the SAME attributes + content-fit, not the template class.
"""
import os, re, sys, warnings
import numpy as np
warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); import analysis as A
from analysis import COL_SURFACE as SF
DIA = re.compile(r"[ً-ْٰـ]"); WA = re.compile(r"[^\W\d_]+", re.UNICODE)
def nrm(t):
    t = DIA.sub("", str(t)); t = re.sub(r"[آأإٱ]", "ا", t); t = re.sub(r"[ىئ]", "ي", t)
    t = t.replace("ة", "ه").replace("ؤ", "و"); return WA.findall(t)
def is_attr(w):
    if len(w) == 4 and w[2] in "ايو": return True            # faʿīl / faʿūl / faʿāl
    if len(w) >= 5 and (w.endswith("ين") or w.endswith("ون")): return True  # sound-plural attributes
    return False
def shares(units):
    units = [u for u in units if len(u) >= 3]
    es = np.mean([is_attr(u[-1]) for u in units]); bs = np.mean([is_attr(w) for u in units for w in u])
    return es, bs, (es / bs if bs > 0 else np.nan), len(units)
def main():
    df = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")).df
    q = [nrm(df.iloc[i][SF]) for i in range(len(df))]
    SENT = re.compile(r"[.!؟?\n،؛:]+"); CP = os.path.join(ROOT, "sequence_tests", "corpus")
    def comp(names):
        txt = "".join("\n" + open(os.path.join(CP, n + ".txt"), encoding="utf-8", errors="ignore").read() for n in names if os.path.exists(os.path.join(CP, n + ".txt")))
        return [nrm(s) for s in SENT.split(txt)]
    corp = {"QURAN": q, "ord-Arabic": comp(["ar_tabari", "ar_classical2", "ar_novel", "ar_news", "ar_news2"]),
            "poetry": comp(["ar_poetry", "ar_poetry_b", "ar_poetry_c"]), "saj'": comp(["ar_sajprose", "ar_saj_hariri"])}
    for k, v in corp.items():
        es, bs, en, nn = shares(v)
        print(f"  {k:11s} end-attr={es:.3f} base-attr={bs:.3f} END-enrichment={en:.2f}x (units={nn})")

if __name__ == "__main__":
    main()
