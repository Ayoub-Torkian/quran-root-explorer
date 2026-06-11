"""Scrutiny: is the within-surah long-range signal genuine fine structure, or just
COARSE within-surah compositional drift? Segment-shuffle null preserves each
surah's coarse positional composition (drift) but destroys finer order.
  total excess     = real - full_shuffle           (all order)
  drift-explained  = seg_shuffle - full_shuffle     (coarse positional drift)
  BEYOND drift     = real - seg_shuffle             (structure finer than drift)
If BEYOND-drift ~ 0 -> the signal is trivial drift -> reinterpret, score drops.
"""
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
top=[r for r,_ in freq.most_common(500)]; vmap={r:i for i,r in enumerate(top)}; OTHER=500; KR=501
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
def full_shuf(): return [rng.permutation(a) for a in arrs]
def seg_shuf(S):
    out=[]
    for a in arrs:
        if a.size<S: out.append(rng.permutation(a)); continue
        bnd=np.linspace(0,a.size,S+1).astype(int); b=a.copy()
        for q in range(S):
            seg=b[bnd[q]:bnd[q+1]]; b[bnd[q]:bnd[q+1]]=rng.permutation(seg)
        out.append(b)
    return out
real=LR(arrs)
full=np.mean([LR(full_shuf()) for _ in range(8)])
for S in (3,6,12):
    seg=np.mean([LR(seg_shuf(S)) for _ in range(6)])
    total=real-full; drift=seg-full; beyond=real-seg
    print(f"  S={S:>2} segments | total excess={total:.4f} ({100*total/H1:.2f}% H1) | "
          f"drift-explained={drift:.4f} ({100*drift/max(total,1e-9):.0f}% of total) | "
          f"BEYOND-drift={beyond:.4f} ({100*beyond/H1:.2f}% H1) -> "
          f"{'survives' if 100*beyond/H1>=1 else 'COLLAPSES (mostly drift)'}")
print(f"\n[total {time.time()-t0:.1f}s]")
