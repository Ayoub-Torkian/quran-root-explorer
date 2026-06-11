import re, sys, time
import numpy as np
from collections import Counter
sys.path.insert(0,"/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2")
import analysis as A
from analysis import normalize_letters
rng=np.random.default_rng(0); t0=time.time(); W=re.compile(r"[^\W\d_]+",re.UNICODE)
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
def feats(a,K):
    return dict(rep8=rep(a,8),rep12=rep(a,12),rep20=rep(a,20),
                MI_near=MIlag(a,K,1)+MIlag(a,K,2))
def win(s,N=3500,step=1750,maxw=24):
    a,K=encode(s); rows=[]
    for c in range(0,max(1,len(a)-N+1),step):
        sub=a[c:c+N]
        if sub.size<N*0.6: break
        rows.append(feats(sub,K))
        if len(rows)>=maxw: break
    ks=rows[0].keys(); return {k:np.array([r[k] for r in rows]) for k in ks}, len(rows)
def load_ar(p):
    out=[]
    for ln in open(p,encoding="utf-8",errors="ignore"):
        ss=ln.strip()
        if not ss or ss.startswith(("صحيح","أرض السافلين")): continue
        out+=[normalize_letters(w) for w in W.findall(ss) if normalize_letters(w)]
    return " ".join(out)
corp=A.load_corpus("/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2/Book6.xlsx")
col='متن آیه با حرکت'
qs=" ".join(normalize_letters(w) for i in range(len(corp.df)) for w in str(corp.df.iloc[i][col]).split() if normalize_letters(w))
tab=load_ar("corpus/ar_tabari.txt"); nov=load_ar("corpus/ar_novel.txt")
Q,nq=win(qs); T,nt=win(tab); Nv,nn=win(nov)
# pooled ordinary-Arabic baseline = Tabari windows + Novel windows
def pool(k): return np.concatenate([T[k],Nv[k]])
print(f"[{time.time()-t0:.1f}s] TIGHTENED non-local: Quran vs TWO ordinary-Arabic baselines (equal-N 3500c)")
print(f"  windows: Quran={nq}  Tabari={nt}  Novel={nn}  pooled-ordinary={nt+nn}")
print(f"\n  {'metric':9s}{'QURAN':>11}{'Tabari':>11}{'Novel':>11}{'ORD pool':>12}   Q vs pooled-ORD")
for k in ["rep8","rep12","rep20","MI_near"]:
    qmu,qsd=Q[k].mean(),Q[k].std(); po=pool(k)
    g_q=(qmu-po.mean())/(qsd+1e-9)            # in Quran-window sd
    # 2-sample-ish: difference over combined sd
    csd=np.sqrt((Q[k].var()+po.var())/2)+1e-9
    g2=(qmu-po.mean())/csd
    print(f"  {k:9s}{qmu:11.4f}{T[k].mean():11.4f}{Nv[k].mean():11.4f}{po.mean():12.4f}   {g2:+.1f} pooled-sd")
print(f"\n[total {time.time()-t0:.1f}s]")
