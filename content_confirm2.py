"""Confirm within-surah ROOT-seq long-range candidate (streamlined: top-N roots
+ OTHER bucket). Gates: significance, effect size, beyond-Markov-1, robustness."""
from __future__ import annotations
import sys, time
import numpy as np
from collections import defaultdict, Counter
sys.path.insert(0,".")
import analysis as A
from analysis import COL_SURAH, COL_AYAH, normalize_letters
rng=np.random.default_rng(0); t0=time.time()
corpus=A.load_corpus("Book6.xlsx"); K=normalize_letters
su=corpus.df[COL_SURAH].astype(int).to_numpy()
order=np.lexsort((corpus.df[COL_AYAH].astype(int).to_numpy(),su)); su2=su[order]
per=defaultdict(list)
for k,i in enumerate(order):
    per[int(su2[k])].extend(K(t) for t in corpus.root_tokens[i])
freq=Counter(r for v in per.values() for r in v)
TOPN=500
top=[r for r,_ in freq.most_common(TOPN)]
vmap={r:i for i,r in enumerate(top)}; OTHER=TOPN; KR=TOPN+1
arrs=[np.array([vmap.get(r,OTHER) for r in per[s]],dtype=np.int64) for s in per]
allr=np.concatenate(arrs); cnt=np.bincount(allr,minlength=KR)/allr.size
H1=float(-np.sum(cnt[cnt>0]*np.log2(cnt[cnt>0])))
DS=[5,8,12,20]
def mi(A_,d):
    j=np.zeros(KR*KR); n=0
    for a in A_:
        if a.size>d:
            j+=np.bincount(a[:-d]*KR+a[d:],minlength=KR*KR); n+=a.size-d
    if n==0: return 0.0
    pj=(j/n).reshape(KR,KR); px=pj.sum(1); py=pj.sum(0); nz=pj>0
    return float(np.sum(pj[nz]*np.log2(pj[nz]/np.outer(px,py)[nz])))
def LR(A_): return sum(mi(A_,d) for d in DS)
def exc(A_,reps=8):
    r=LR(A_); n=np.mean([LR([rng.permutation(a) for a in A_]) for _ in range(reps)]); return r,n
real,floor=exc(arrs,reps=20)
nl=np.array([LR([rng.permutation(a) for a in arrs]) for _ in range(20)])
p_sig=(np.sum(nl>=real)+1)/(len(nl)+1)
ex=real-floor
# markov-1 surrogate
trans=defaultdict(Counter)
for a in arrs:
    for i in range(1,a.size): trans[a[i-1]][a[i]]+=1
succ={};cdf={}
for s,c in trans.items():
    ks=np.array(list(c.keys())); vs=np.array(list(c.values()),float)
    succ[s]=ks; cdf[s]=np.cumsum(vs/vs.sum())
def genmk():
    out=[]
    for a in arrs:
        s=a.copy()
        for i in range(1,a.size):
            p=s[i-1]
            s[i]=succ[p][np.searchsorted(cdf[p],rng.random())] if p in succ else rng.integers(KR)
        out.append(s)
    return out
mk=genmk(); mkr,mkf=exc(mk,reps=8); mkex=mkr-mkf
beyond=ex/max(mkex,1e-9)
print(f"[{time.time()-t0:.1f}s] capped KR={KR} (top {TOPN}+OTHER) H1={H1:.2f}")
print(f"  G2 significance : real LR={real:.4f} shuffle {nl.mean():.4f}+/-{nl.std():.4f}  p={p_sig:.3g}")
print(f"  G5 effect size  : excess={ex:.4f} = {100*ex/H1:.2f}% of H1 -> {'PASS' if 100*ex/H1>=1 else 'FAIL'}")
print(f"  beyond-Markov-1 : real-excess {ex:.4f} vs markov1-excess {mkex:.4f}  ratio={beyond:.1f}x -> {'PASS(>3x)' if beyond>=3 else 'FAIL'}")
def exsub(sel):
    sub=[arrs[i] for i in sel]; al=np.concatenate(sub); c=np.bincount(al,minlength=KR)/al.size
    h=float(-np.sum(c[c>0]*np.log2(c[c>0]))); r,f=exc(sub,reps=5); return 100*(r-f)/h
n=len(arrs); big=int(np.argmax([a.size for a in arrs]))
print(f"  G6 robustness   : split-half {exsub(range(0,n,2)):.2f}% / {exsub(range(1,n,2)):.2f}% ; "
      f"drop-largest {exsub([i for i in range(n) if i!=big]):.2f}% (stay >1%)")
print(f"\n[total {time.time()-t0:.1f}s]")
