# MODALITY 46 (variant A, seed-lexicon) — LEXICAL-SEMANTIC / TOPICAL FIELD DYNAMICS.
# Result: NULL. Per-unit semantic-field label -> shuffle-controlled sequencing (switch, MI) +
# cohesion (run-length) excess; equal-N windows; comparators; gate. Mirrors discourse.py (#44).
# RUN DISCIPLINE: author/run in /tmp via heredoc (mount read lags); set ROOT to this session's mount.
import re, sys, time
import numpy as np
from collections import Counter
ROOT = __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__)))
sys.path.insert(0, ROOT); import analysis as A
from analysis import COL_DIACRITIZED as D
rng = np.random.default_rng(42); t0 = time.time()
_DIA = re.compile(r"[ً-ْٰـۖ-ۭ]"); WA = re.compile(r"[^\W\d_]+", re.UNICODE)
def nl(t):
    t=_DIA.sub("",str(t)); t=re.sub(r"[آأإٱ]","ا",t); t=re.sub(r"[ىی]","ي",t)
    t=re.sub(r"[ةھ]","ه",t); return t.replace("ک","ك").replace("ؤ","ء").replace("ئ","ء").strip()
def words(s): return [w for w in WA.findall(nl(s)) if w]
def Lx(s): return {nl(w) for w in s.split()}
FIELDLEX = {
 "MERCY":   Lx("رحمه رحمن رحيم غفور غفر مغفره رزق رزقكم نعمه نعم فضل رضوان رضي رحم عفو تواب ودود حليم كريم احسان بركه طيبات"),
 "JUDGMENT":Lx("عذاب نار جهنم قيامه حساب عقاب جزاء خلود اليم لعنه غضب وعيد سعير جحيم حميم يومئذ الساعه ويل صاعقه هلاك"),
 "NATURE":  Lx("سماء سموات ارض شمس قمر نجوم نجم ليل نهار جبال جبل بحر بحار مطر رياح ريح سحاب نبات شجر ماء ثمرات زرع انعام دواب فلك ظلمات نور"),
 "LAW":     Lx("صلاه زكاه صيام صوم حج حلال حرام حدود ميراث طلاق نكاح ربا قصاص شهاده فرض اوفوا كتب عليكم احل حرم وصيه دين بيع"),
 "COVENANT":Lx("ايمان امنوا عهد ميثاق كتاب رسول رسل نبي وحي هدي اسلام مسلمين شرك كفر كافرين توحيد عباد طاعه اطيعوا صراط مستقيم اولياء"),
}
FIELDS = list(FIELDLEX) + ["OTHER"]
def tag_unit(ws):
    if not ws: return "OTHER"
    sw=set(ws); sc={f:len(sw & FIELDLEX[f]) for f in FIELDLEX}
    best=max(FIELDLEX, key=lambda f: sc[f]); return best if sc[best]>0 else "OTHER"
def switch_rate(lab): return float(np.mean([lab[i]!=lab[i+1] for i in range(len(lab)-1)])) if len(lab)>1 else None
def transition_mi(lab):
    if len(lab)<3: return None
    idx={m:k for k,m in enumerate(FIELDS)}; M=np.zeros((len(FIELDS),len(FIELDS)))
    for x,y in zip(lab[:-1],lab[1:]): M[idx[x],idx[y]]+=1
    P=M/M.sum(); Px=P.sum(1,keepdims=True); Py=P.sum(0,keepdims=True)
    with np.errstate(divide="ignore",invalid="ignore"): mi=np.nansum(P*np.log((P+1e-12)/(Px*Py+1e-12)))
    Hx=-np.nansum(Px*np.log(Px+1e-12)); return float(mi/(Hx+1e-12)) if Hx>0 else 0.0
def run_len(lab):
    if len(lab)<2: return None
    r=1
    for i in range(1,len(lab)):
        if lab[i]!=lab[i-1]: r+=1
    return len(lab)/r
def stat_excess(lab,W,B,fn):
    if len(lab)<W: return None
    v=[]
    for _ in range(B):
        s=rng.integers(0,len(lab)-W+1); win=lab[s:s+W]; a=fn(win); sh=list(win); rng.shuffle(sh); b=fn(sh)
        if a is not None and b is not None: v.append(a-b)
    return np.array(v) if v else None
def g(a,b): return (a.mean()-b.mean())/(np.sqrt((a.var()+b.var())/2)+1e-9) if (a is not None and b is not None and len(a)>1 and len(b)>1) else float("nan")
def boot_p(a,b,R=2000):
    ai=rng.integers(0,len(a),R); bi=rng.integers(0,len(b),R); return float(np.mean(a[ai]>b[bi])+0.5*np.mean(a[ai]==b[bi]))

def main():
    import os
    c=A.load_corpus(os.path.join(ROOT,"Book6.xlsx"))
    q=[tag_unit(words(str(c.df.iloc[i][D]))) for i in range(len(c.df))]
    US=re.compile(r"[.!؟?\n،؛:]+")
    def file_labels(paths):
        txt="".join("\n"+open(p,encoding="utf-8",errors="ignore").read() for p in paths)
        return [tag_unit(words(u)) for u in US.split(txt) if len(words(u))>=2]
    CP=os.path.join(ROOT,"sequence_tests","corpus")+"/"
    corp={"QURAN":q,
     "ord-Arabic":file_labels([CP+f+".txt" for f in("ar_tabari","ar_classical2","ar_novel","ar_news","ar_news2")]),
     "poetry":file_labels([CP+"ar_poetry.txt"]),
     "saj'":file_labels([CP+"ar_sajprose.txt",CP+"ar_saj_hariri.txt"])}
    print("units:",{k:len(v) for k,v in corp.items()})
    W,B=40,400
    EX={k:{s:stat_excess(corp[k],W,B,fn) for s,fn in [("switch",switch_rate),("MI",transition_mi),("run",run_len)]} for k in corp}
    for s in ("switch","MI","run"):
        print(f"\n-- {s} excess --")
        for k in corp: print(f"   {k:11s} mean={EX[k][s].mean():+.4f}")
        for comp in ("ord-Arabic","poetry","saj'"):
            print(f"   QURAN vs {comp:11s}: g={g(EX['QURAN'][s],EX[comp][s]):+.2f}sd  P={boot_p(EX['QURAN'][s],EX[comp][s]):.2f}")

if __name__ == "__main__": main()
