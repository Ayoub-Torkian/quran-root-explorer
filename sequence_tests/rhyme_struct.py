import re, time
import numpy as np, pandas as pd
from collections import Counter
ROOT="/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2"
rng=np.random.default_rng(17); t0=time.time()
_DIA=re.compile(r"[ً-ٰٟۖ-ۭ]"); _TAT=re.compile("ـ"); WA=re.compile(r"[^\W\d_]+",re.UNICODE)
def nl(t):
    t=_TAT.sub("",_DIA.sub("",str(t)))
    t=re.sub(r"[آأإٱ]","ا",t); t=re.sub(r"[ىی]","ي",t); t=re.sub(r"[ةھ]","ه",t)
    return t.replace("ک","ك").replace("ؤ","ء").replace("ئ","ء").strip()
def words(s): return [w for w in WA.findall(nl(str(s))) if w]
def end2(u): return (u[-1][-2:] if u and len(u[-1])>=2 else (u[-1] if u else ""))

def metrics(endings):
    n=len(endings)
    if n<6: return None
    c=Counter([e for e in endings if e]); fr=np.array(list(c.values()),float)/n
    dom=fr.max(); chance=float(np.sum(fr**2))
    adj=np.mean([endings[i]==endings[i+1] for i in range(n-1)])
    adj_excess=adj-chance
    # mean run length of identical consecutive endings
    runs=1; nr=1
    for i in range(1,n):
        if endings[i]==endings[i-1]: runs+=1
        else: nr+=1
    mean_run=n/nr
    return dict(adj_excess=adj_excess, mean_run=mean_run, dom=dom)

def win_metrics(units, U=20, step=10):
    out=[]
    for c in range(0,max(1,len(units)-U+1),step):
        seg=units[c:c+U]
        if len(seg)<U*0.8: break
        m=metrics([end2(u) for u in seg])
        if m: out.append(m)
        if len(out)>=120: break
    if not out:
        m=metrics([end2(u) for u in units]); out=[m] if m else []
    ks=["adj_excess","mean_run","dom"]; 
    return {k:np.array([o[k] for o in out]) for k in ks} if out else None

# Quran ayat per surah -> one long unit list (ayah units), but compute per-surah windows
raw=pd.read_excel(ROOT+"/Book6.xlsx",header=None,nrows=8); hdr=0
for i in range(len(raw)):
    if raw.iloc[i].map(lambda x: nl(x)).str.contains("سوره").any(): hdr=i;break
df=pd.read_excel(ROOT+"/Book6.xlsx",header=hdr); df.columns=[str(c).strip() for c in df.columns]
scol=[c for c in df.columns if "سوره" in nl(c) and "اسم" not in nl(c)][0]
tcol=[c for c in df.columns if "متن" in nl(c) and "توكن" not in nl(c)][0]
sur={}
for s,txt in zip(df[scol].tolist(),df[tcol].tolist()):
    try: si=int(float(s))
    except: continue
    if 1<=si<=114: sur.setdefault(si,[]).append(words(txt))
Q=[]
for ay in sur.values():
    if len(ay)>=20:
        d=win_metrics(ay)
        if d: Q.append(d)
def stack(lst):
    return {k:np.concatenate([d[k] for d in lst]) for k in ["adj_excess","mean_run","dom"]}
Q=stack(Q)

# poetry bayt-final units
pl=[words(ln) for ln in open("corpus/ar_poetry.txt",encoding="utf-8",errors="ignore") if words(ln)]
bayt=pl[1::2]
L=win_metrics(bayt, U=20, step=10)

# prose sentences
SENT=re.compile(r"[.!?؟؛\n]+")
psent=[words(x) for fn in ("ar_tabari","ar_classical2","ar_novel","ar_news")
       for x in SENT.split(open("corpus/%s.txt"%fn,encoding="utf-8",errors="ignore").read()) if len(words(x))>=2]
P=win_metrics(psent, U=20, step=10)

# saj' clauses
sclause=[words(x) for x in re.split(r"[،.؛:!؟]+",open("corpus/ar_sajprose.txt",encoding="utf-8").read()) if len(words(x))>=2]
S=win_metrics(sclause, U=20, step=6)

print("[%.1fs] windows: Q=%d poetry=%d prose=%d SAJ=%d (clauses: saj=%d)"%(time.time()-t0,len(Q['dom']),len(L['dom']),len(P['dom']),len(S['dom']),len(sclause)))

# ---- gate ----
def m1(ends): return metrics(ends)
mono=["ون"]*20; pair=[x for i in range(10) for x in (("a%d"%i,)*2)]
rndp=["r%d"%rng.integers(1e6) for _ in range(20)]
print("\nGATE: monorhyme=%s ; paired(aabb)=%s ; random=%s"%(
  {k:round(v,2) for k,v in m1(mono).items()},{k:round(v,2) for k,v in m1(pair).items()},{k:round(v,2) for k,v in m1(rndp).items()}))

def g(a,b): return (a.mean()-b.mean())/(np.sqrt((a.var()+b.var())/2)+1e-9)
print("\n metric     | Quran | poetry| prose | SAJ   | Q-vs-SAJ | Q-vs-prose")
for k in ["adj_excess","mean_run","dom"]:
    print("  %-9s | %5.2f | %5.2f | %5.2f | %5.2f | %+.1fsd  | %+.1fsd"%(k,Q[k].mean(),L[k].mean(),P[k].mean(),S[k].mean(),g(Q[k],S[k]),g(Q[k],P[k])))
print("\n[%.1fs]"%(time.time()-t0))
