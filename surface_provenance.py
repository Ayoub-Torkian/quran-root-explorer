"""Provenance gate (G0): does the within-surah long-range sequence signal survive
on actual SURFACE WORD-FORMS (fully Tier-1) instead of morphological roots?
Streamlined: top-500 surface forms + OTHER."""
from __future__ import annotations
import sys, time
import numpy as np
from collections import defaultdict, Counter
sys.path.insert(0,".")
import analysis as A
from analysis import COL_SURAH, COL_AYAH, normalize_letters
rng=np.random.default_rng(0); t0=time.time()
corpus=A.load_corpus("Book6.xlsx")
su=corpus.df[COL_SURAH].astype(int).to_numpy()
order=np.lexsort((corpus.df[COL_AYAH].astype(int).to_numpy(),su)); su2=su[order]
# surface tokens per surah (the actual words, normalized letters, no diacritics)
per=defaultdict(list)
src = corpus.surface_tokens if hasattr(corpus,'surface_tokens') and corpus.surface_tokens else corpus.seg_tokens
for k,i in enumerate(order):
    for t in src[i]:
        w=normalize_letters(t)
        if w: per[int(su2[k])].append(w)
freq=Counter(w for v in per.values() for w in v)
TOPN=500; top=[w for w,_ in freq.most_common(TOPN)]; vmap={w:i for i,w in enumerate(top)}; OTHER=TOPN; KR=TOPN+1
arrs=[np.array([vmap.get(w,OTHER) for w in per[s]],dtype=np.int64) for s in per]
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
real=LR(arrs); nl=np.array([LR([rng.permutation(a) for a in arrs]) for _ in range(15)])
ex=real-nl.mean(); z=ex/(nl.std()+1e-9); p=(np.sum(nl>=real)+1)/(len(nl)+1)
# beyond-markov-1
trans=defaultdict(Counter)
for a in arrs:
    for i in range(1,a.size): trans[a[i-1]][a[i]]+=1
succ={};cdf={}
for s,c in trans.items():
    ks=np.array(list(c.keys())); vs=np.array(list(c.values()),float); succ[s]=ks; cdf[s]=np.cumsum(vs/vs.sum())
def genmk():
    out=[]
    for a in arrs:
        s=a.copy()
        for i in range(1,a.size):
            p0=s[i-1]; s[i]=succ[p0][np.searchsorted(cdf[p0],rng.random())] if p0 in succ else rng.integers(KR)
        out.append(s)
    return out
mk=genmk(); mkr=LR(mk); mkf=np.mean([LR([rng.permutation(a) for a in mk]) for _ in range(5)]); mkex=mkr-mkf
print(f"[{time.time()-t0:.1f}s] SURFACE words (Tier-1) capped KR={KR} H1={H1:.2f} tokens={allr.size}")
print(f"  significance: excess LR={ex:.4f}  z={z:.1f}  p={p:.3g}")
print(f"  effect size : {100*ex/H1:.2f}% of H1 -> {'PASS' if 100*ex/H1>=1 else 'FAIL'}")
print(f"  beyond-Markov-1: {ex/max(mkex,1e-9):.1f}x -> {'PASS(>3x)' if ex/max(mkex,1e-9)>=3 else 'FAIL'}")
print(f"\n[total {time.time()-t0:.1f}s]")
