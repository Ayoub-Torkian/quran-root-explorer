"""D2 (cross-impact re-open of #46) — do semantic FIELDS recur in BURSTS across the sequence?
#46 found field SEQUENCING null; this re-opens it through the recurrence modality. Equal-N Fano factor of
field inter-occurrence gaps vs random-position null, mean over 5 seed fields, Qur'an vs comparators.
RESULT: QURAN z=+0.59, ord-Arabic −0.09, poetry −1.36 (saj' n/a). Mildly positive but SUB-significant —
#46 region stays null even as recurrence. ('Nothing is final' → re-checked → still null.) Divinely-rooted.
"""
import os, re, sys, warnings
import numpy as np
warnings.filterwarnings("ignore")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); import analysis as A
from analysis import COL_ROOTS as R
rng = np.random.default_rng(46)
DIA = re.compile(r"[ً-ْٰـۖ-ۭ]"); WA = re.compile(r"[^\W\d_]+", re.UNICODE)
def nl(t):
    t = DIA.sub("", str(t)); t = re.sub(r"[آأإٱ]", "ا", t); t = re.sub(r"[ىی]", "ي", t)
    t = re.sub(r"[ةھ]", "ه", t); return t.replace("ک", "ك").replace("ؤ", "ء").replace("ئ", "ء")
L = lambda s: {nl(w) for w in s.split()}
FIELDLEX = {
 "MERCY": L("رحمه رحمن رحيم غفور غفر رزق نعمه فضل رحم عفو كريم احسان بركه"),
 "JUDG": L("عذاب نار جهنم قيامه حساب عقاب جزاء خلود اليم لعنه غضب جحيم يومئذ ويل هلاك"),
 "NATURE": L("سماء سموات ارض شمس قمر نجوم ليل نهار جبال بحر مطر رياح سحاب نبات شجر ماء انعام فلك نور"),
 "LAW": L("صلاه زكاه صوم حج حلال حرام حدود ميراث طلاق نكاح ربا قصاص شهاده احل حرم دين"),
 "COVENANT": L("ايمان امنوا عهد ميثاق كتاب رسول نبي وحي هدي اسلام شرك كفر عباد طاعه صراط"),
}
def fano(pos):
    if len(pos) < 6: return np.nan
    g = np.diff(np.sort(pos)); return g.var() / g.mean() if g.mean() > 0 else np.nan
def burst(labels):
    n = len(labels); zs = []
    for f in FIELDLEX:
        pos = np.array([i for i in range(n) if f in labels[i]])
        if len(pos) < 6: continue
        obs = fano(pos); null = np.array([fano(rng.choice(n, len(pos), replace=False)) for _ in range(200)])
        zs.append((obs - np.nanmean(null)) / (np.nanstd(null) + 1e-9))
    return np.nanmean(zs) if zs else np.nan

def main():
    df = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")).df
    tag = lambda S: {f for f in FIELDLEX if S & FIELDLEX[f]}
    q = [tag(set(w for w in str(df.iloc[i][R]).split() if w and w != 'nan')) for i in range(len(df))]
    SENT = re.compile(r"[.!؟?\n،؛:]+"); CP = os.path.join(ROOT, "sequence_tests", "corpus")
    def comp(names):
        txt = "".join("\n" + open(os.path.join(CP, n + ".txt"), encoding="utf-8", errors="ignore").read() for n in names if os.path.exists(os.path.join(CP, n + ".txt")))
        return [tag(set(WA.findall(nl(s)))) for s in SENT.split(txt) if len(WA.findall(nl(s))) >= 2]
    corp = {"QURAN": q, "ord-Arabic": comp(["ar_tabari", "ar_classical2", "ar_novel", "ar_news", "ar_news2"]),
            "poetry": comp(["ar_poetry", "ar_poetry_b", "ar_poetry_c"]), "saj'": comp(["ar_sajprose", "ar_saj_hariri"])}
    N = min(len(v) for v in corp.values())
    for k, v in corp.items():
        zs = [burst([v[i] for i in sorted(rng.choice(len(v), N, replace=False))]) for _ in range(5)]
        print(f"  {k:11s} field-burst z = {np.nanmean(zs):+.2f}")

if __name__ == "__main__":
    main()
