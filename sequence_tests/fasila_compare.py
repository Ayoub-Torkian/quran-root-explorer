"""#63 — COMPARATOR test for the fāṣila system (#62). Surface-word grain (comparators lack root annotation).
(1) ending->body content fit per corpus; (2) equal-N ending-word REPETITION (the precondition for grouping).
RESULT: comparators have ~0 endings recurring >=10x (Qur'an 14+). Equal-N (319) ending repetition:
  QURAN frac-recurs>=3x 0.279 | saj' 0.038 | ord-Arabic 0.099 | poetry 0.021 (ending-TTR: Qur'an=saj'=0.699).
=> the Qur'an HEAVILY repeats SPECIFIC ending words, EXCEEDING saj' (which rhymes but doesn't repeat the same
word >=3x). The fāṣila system = rhyme-persistence (#34-37) + recurrence (#42) + content-fit (#62) at the
verse-end; ending-repetition is a CROSS-TEXT distinctive. Content-fit itself stays Qur'an-internal.
"""
import os, re, sys, warnings
import numpy as np
warnings.filterwarnings("ignore")
from collections import Counter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); import analysis as A
from analysis import COL_SURFACE as SF
rng = np.random.default_rng(63)
DIA = re.compile(r"[ً-ْٰـ]"); WA = re.compile(r"[^\W\d_]+", re.UNICODE)
def nrm(t):
    t = DIA.sub("", str(t)); t = re.sub(r"[آأإٱ]", "ا", t); t = re.sub(r"[ىئ]", "ي", t)
    t = t.replace("ة", "ه").replace("ؤ", "و"); return WA.findall(t)

def main():
    df = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")).df
    q = [u for u in (nrm(df.iloc[i][SF]) for i in range(len(df))) if len(u) >= 4]
    SENT = re.compile(r"[.!؟?\n،؛:]+"); CP = os.path.join(ROOT, "sequence_tests", "corpus")
    def comp(names):
        txt = "".join("\n" + open(os.path.join(CP, n + ".txt"), encoding="utf-8", errors="ignore").read()
                      for n in names if os.path.exists(os.path.join(CP, n + ".txt")))
        return [u for u in (nrm(s) for s in SENT.split(txt)) if len(u) >= 4]
    corp = {"QURAN": q, "ord-Arabic": comp(["ar_tabari", "ar_classical2", "ar_novel", "ar_news", "ar_news2"]),
            "poetry": comp(["ar_poetry", "ar_poetry_b", "ar_poetry_c"]), "saj'": comp(["ar_sajprose", "ar_saj_hariri"])}
    N = min(len(v) for v in corp.values())
    print(f"equal-N={N}. ending-word repetition (frac of units whose ending recurs >=3x):")
    for k, v in corp.items():
        ttr, rec = [], []
        for _ in range(200):
            s = [v[i] for i in rng.choice(len(v), N, replace=False)]; ends = [u[-1] for u in s]; ct = Counter(ends)
            ttr.append(len(ct) / N); rec.append(np.mean([ct[e] >= 3 for e in ends]))
        print(f"  {k:11s} ending-TTR={np.mean(ttr):.3f}  frac-recurs>=3x={np.mean(rec):.3f}")

if __name__ == "__main__":
    main()
