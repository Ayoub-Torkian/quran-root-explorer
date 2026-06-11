import re, time
import numpy as np, pandas as pd
from collections import Counter
ROOT="/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2"
rng=np.random.default_rng(31); t0=time.time()
_DIA=re.compile(r"[ً-ٰٟۖ-ۭ]"); _TAT=re.compile("ـ"); WA=re.compile(r"[^\W\d_]+",re.UNICODE)
AR="ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
def nl(t):
    t=_TAT.sub("",_DIA.sub("",str(t)))
    t=re.sub(r"[آأإٱ]","ا",t); t=re.sub(r"[ىی]","ي",t); t=re.sub(r"[ةھ]","ه",t)
    return t.replace("ک","ك").replace("ؤ","ء").replace("ئ","ء").strip()
def unit_letters(u):  # letter count of a unit (list of words)
    return sum(1 for w in u for ch in w if ch in AR)
def cv(u):
    s=""
    for w in u:
        for ch in w:
            if ch in AR: s+=("V" if ch in "اوي" else "C")
    return s

def isocolon_z(units, R=300):
    L=np.array([unit_letters(u) for u in units],float); L=L[L>0]
    n=len(L)
    if n<6: return None
    real=np.mean(np.abs(np.diff(L)))/(L.mean()+1e-9)         # adjacent length imbalance
    nul=np.empty(R)
    for t in range(R):
        p=rng.permutation(L); nul[t]=np.mean(np.abs(np.diff(p)))/(p.mean()+1e-9)
    z=(nul.mean()-real)/(nul.std()+1e-9)                      # +z = MORE balanced than chance (isocolon)
    return z
def metricality(units):  # CV-trigram predictability (meter proxy); high=regular
    s="".join(cv(u) for u in units)
    if len(s)<20: return None
    g=Counter(s[i:i+3] for i in range(len(s)-3)); tot=sum(g.values())
    p=np.array(list(g.values()),float)/tot; H=-np.sum(p*np.log2(p))
    return 1-H/np.log2(8)                                     # 8 possible CV trigrams; 1=fully regular

def win(units, U=18, step=9, maxw=120):
    iz=[]; mt=[]
    for c in range(0,max(1,len(units)-U+1),step):
        seg=units[c:c+U]
        if len(seg)<U*0.8: break
        z=isocolon_z(seg); m=metricality(seg)
        if z is not None: iz.append(z)
        if m is not None: mt.append(m)
        if len(iz)>=maxw: break
    return np.array(iz), np.array(mt)

# registers
raw=pd.read_excel(ROOT+"/Book6.xlsx",header=None,nrows=8); hdr=0
for i in range(len(raw)):
    if raw.iloc[i].map(lambda x: nl(x)).str.contains("سوره").any(): hdr=i;break
df=pd.read_excel(ROOT+"/Book6.xlsx",header=hdr); df.columns=[str(c).strip() for c in df.columns]
scol=[c for c in df.columns if "سوره" in nl(c) and "اسم" not in nl(c)][0]
tcol=[c for c in df.columns if "متن" in nl(c) and "توكن" not in nl(c)][0]
def W(s): return [w for w in WA.findall(nl(str(s))) if w]
sur={}
for s,t in zip(df[scol].tolist(),df[tcol].tolist()):
    try: si=int(float(s))
    except: continue
    if 1<=si<=114: sur.setdefault(si,[]).append(W(t))
Qiz=[];Qmt=[]
for ay in sur.values():
    if len(ay)>=18:
        a,b=win(ay); Qiz+=list(a); Qmt+=list(b)
Qiz,Qmt=np.array(Qiz),np.array(Qmt)
def reg_units(units): a,b=win(units); return a,b
SENT=re.compile(r"[.!?؟؛\n]+")
prose=[W(x) for fn in ("ar_tabari","ar_classical2","ar_novel","ar_news") for x in SENT.split(open("corpus/%s.txt"%fn,encoding="utf-8",errors="ignore").read()) if len(W(x))>=2]
poet=[W(l) for l in open("corpus/ar_poetry.txt",encoding="utf-8",errors="ignore") if len(W(l))>=2]
saj=[W(x) for x in re.split(r"[،.؛:!؟]+",open("corpus/ar_sajprose.txt",encoding="utf-8").read()) if len(W(x))>=2]
Piz,Pmt=reg_units(prose); Liz,Lmt=reg_units(poet); Siz,Smt=reg_units(saj)

# gate
eq=[["ابابابا"]]*18; rndu=[["ا"*int(rng.integers(2,12))] for _ in range(18)]
print("[%.1fs] GATE isocolon_z: equal-lengths=%.1f ; random-lengths=%.1f"%(time.time()-t0, isocolon_z(eq), isocolon_z(rndu)))
def g(a,b): return (a.mean()-b.mean())/(np.sqrt((a.var()+b.var())/2)+1e-9)
print("\n metric        | Quran | poetry| prose | saj   | Q-vs-prose | Q-vs-poetry | Q-vs-saj")
print("  isocolon_z   | %5.2f | %5.2f | %5.2f | %5.2f | %+.1fsd    | %+.1fsd     | %+.1fsd"%(Qiz.mean(),Liz.mean(),Piz.mean(),Siz.mean(),g(Qiz,Piz),g(Qiz,Liz),g(Qiz,Siz)))
print("  metricality  | %5.3f | %5.3f | %5.3f | %5.3f | %+.1fsd    | %+.1fsd     | %+.1fsd"%(Qmt.mean(),Lmt.mean(),Pmt.mean(),Smt.mean(),g(Qmt,Pmt),g(Qmt,Lmt),g(Qmt,Smt)))
print("\n[%.1fs]"%(time.time()-t0))
