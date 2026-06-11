import re, sys, time
import numpy as np
from collections import Counter
sys.path.insert(0,"/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2")
import analysis as A
from analysis import normalize_letters
t0=time.time(); W=re.compile(r"[^\W\d_]+",re.UNICODE)
def encode(s):
    al=sorted(set(s)); vm={c:i for i,c in enumerate(al)}
    return np.array([vm[c] for c in s],dtype=np.int64), len(al)
def MIlag(a,K,d):
    if a.size<=d: return 0.0
    x=a[:-d];y=a[d:]; j=np.bincount(x*K+y,minlength=K*K).astype(float)/x.size; pj=j.reshape(K,K)
    px=pj.sum(1);py=pj.sum(0);nz=pj>0; return float(np.sum(pj[nz]*np.log2(pj[nz]/np.outer(px,py)[nz])))
def rep(a,n):
    if len(a)<=n: return 0.0
    g=Counter(a[i:i+n].tobytes() for i in range(len(a)-n)); return 1-len(g)/max(sum(g.values()),1)
def feats(a,K): return dict(rep8=rep(a,8),rep12=rep(a,12),rep20=rep(a,20),MI_near=MIlag(a,K,1)+MIlag(a,K,2))
def win(s,N=2500,step=1250,maxw=40):
    a,K=encode(s); rows=[]
    for c in range(0,max(1,len(a)-N+1),step):
        sub=a[c:c+N]
        if sub.size<N*0.7: break
        rows.append(feats(sub,K))
        if len(rows)>=maxw: break
    ks=rows[0].keys(); return {k:np.array([r[k] for r in rows]) for k in ks}, len(rows)
def load_ar(p):
    out=[]
    for ln in open(p,encoding="utf-8",errors="ignore"):
        ss=ln.strip()
        if not ss or ss.startswith(("صحيح","أرض السافلين","نص إخباري")): continue
        out+=[normalize_letters(w) for w in W.findall(ss) if normalize_letters(w)]
    return " ".join(out)
corp=A.load_corpus("/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2/Book6.xlsx")
col='متن آیه با حرکت'
qs=" ".join(normalize_letters(w) for i in range(len(corp.df)) for w in str(corp.df.iloc[i][col]).split() if normalize_letters(w))
srcs={"Quran":qs,"Tabari(classical)":load_ar("corpus/ar_tabari.txt"),
      "Novel(literary)":load_ar("corpus/ar_novel.txt"),"News-BBC(MSA)":load_ar("corpus/ar_news.txt")}
D={k:win(v) for k,v in srcs.items()}
print(f"[{time.time()-t0:.1f}s] THREE-register ordinary-Arabic test (equal-N 2500c windows)")
for k in srcs: print(f"   {k:20s} windows={D[k][1]}")
ordkeys=["Tabari(classical)","Novel(literary)","News-BBC(MSA)"]
print(f"\n  {'metric':8s}{'QURAN':>10}{'Tabari':>9}{'Novel':>9}{'News':>9}{'ORDpool':>9}   Q vs pooled-ORD")
for m in ["rep8","rep12","rep20","MI_near"]:
    Q=D["Quran"][0][m]; pool=np.concatenate([D[k][0][m] for k in ordkeys])
    csd=np.sqrt((Q.var()+pool.var())/2)+1e-9
    g=(Q.mean()-pool.mean())/csd
    vals=[D[k][0][m].mean() for k in ordkeys]
    print(f"  {m:8s}{Q.mean():10.4f}{vals[0]:9.4f}{vals[1]:9.4f}{vals[2]:9.4f}{pool.mean():9.4f}   {g:+.1f} sd")
print(f"\n[total {time.time()-t0:.1f}s]")
