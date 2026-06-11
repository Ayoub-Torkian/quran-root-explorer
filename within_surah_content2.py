"""Option 1 refinement (optimized): decisive gate numbers.
(A) within-surah ROOT-sequence long-range order (content lens) vs shuffle.
(B) cross-word letter MI (morphology removed) vs all-pairs.
"""
from __future__ import annotations
import sys, time
import numpy as np
from collections import defaultdict
sys.path.insert(0,".")
import analysis as A
from analysis import COL_SURAH, COL_AYAH, normalize_letters
rng=np.random.default_rng(0); t0=time.time()
corpus=A.load_corpus("Book6.xlsx"); K=normalize_letters
su=corpus.df[COL_SURAH].astype(int).to_numpy()
order=np.lexsort((corpus.df[COL_AYAH].astype(int).to_numpy(),su)); su2=su[order]

# ---- (A) root sequences per surah ----
per=defaultdict(list)
for k,i in enumerate(order):
    per[int(su2[k])].extend(K(t) for t in corpus.root_tokens[i])
vocab={}
for v in per.values():
    for r in v: vocab.setdefault(r,len(vocab))
KR=len(vocab)
arrs=[np.array([vocab[r] for r in v],dtype=np.int64) for v in per.values()]
allr=np.concatenate(arrs); cnt=np.bincount(allr,minlength=KR)/allr.size
H1=float(-np.sum(cnt[cnt>0]*np.log2(cnt[cnt>0])))
def mi(arrs,d,Kd):
    j=np.zeros(Kd*Kd); n=0
    for a in arrs:
        if a.size>d:
            j+=np.bincount(a[:-d]*Kd+a[d:],minlength=Kd*Kd); n+=a.size-d
    if n==0: return 0.0
    pj=(j/n).reshape(Kd,Kd); px=pj.sum(1); py=pj.sum(0); nz=pj>0
    return float(np.sum(pj[nz]*np.log2(pj[nz]/np.outer(px,py)[nz])))
ds=[1,2,3,5,8,12,20,30]
real=np.array([mi(arrs,d,KR) for d in ds])
shuf=np.mean([np.array([mi([rng.permutation(a) for a in arrs],d,KR) for d in ds]) for _ in range(2)],axis=0)
exc=real-shuf; mask=np.array(ds)>=5; lr=exc[mask].clip(min=0).sum()
print(f"[{time.time()-t0:.1f}s] (A) ROOT seq tokens={allr.size} KR={KR} H1={H1:.2f}")
print("  excess: "+"  ".join(f"d{d}:{exc[j]:+.4f}" for j,d in enumerate(ds)))
print(f"  LONG-RANGE d>=5 excess={lr:.4f}  effect LR/H1={100*lr/H1:.2f}%  (G5 floor 1%) -> {'PASS' if 100*lr/H1>=1 else 'FAIL'}")

# ---- (B) cross-word letter MI ----
plet=defaultdict(list); pwid=defaultdict(list); wc=0
for k,i in enumerate(order):
    s=int(su2[k])
    for t in corpus.seg_tokens[i]:
        wc+=1
        for ch in K(t):
            if ch.strip(): plet[s].append(ai if False else ch); pwid[s].append(wc)
alpha=sorted({c for v in plet.values() for c in v}); ai={c:j for j,c in enumerate(alpha)}; KL=len(alpha)
Ls=[(np.array([ai[c] for c in plet[s]],dtype=np.int64), np.array(pwid[s])) for s in plet]
alll=np.concatenate([a for a,_ in Ls]); cl=np.bincount(alll,minlength=KL)/alll.size
HL=float(-np.sum(cl[cl>0]*np.log2(cl[cl>0])))
def mi_letters(pairs_list,d,crossword):
    j=np.zeros(KL*KL); n=0
    for a,w in pairs_list:
        if a.size>d:
            x=a[:-d]; y=a[d:]
            if crossword:
                m=w[:-d]!=w[d:]; x=x[m]; y=y[m]
            if x.size: j+=np.bincount(x*KL+y,minlength=KL*KL); n+=x.size
    if n==0: return 0.0
    pj=(j/n).reshape(KL,KL); px=pj.sum(1); py=pj.sum(0); nz=pj>0
    return float(np.sum(pj[nz]*np.log2(pj[nz]/np.outer(px,py)[nz])))
dl=[5,8,12,20]
allp=np.array([mi_letters(Ls,d,False) for d in dl])
cw=np.array([mi_letters(Ls,d,True) for d in dl])
# bias floor: shuffle letters within surah (keeps word-ids), cross-word MI
bias=np.zeros(len(dl))
for _ in range(2):
    Lsh=[(rng.permutation(a),w) for a,w in Ls]
    bias+=np.array([mi_letters(Lsh,d,True) for d in dl])
bias/=2
cw_exc=cw-bias
print(f"\n  (B) letter MI d>=5  (HL={HL:.2f}):")
for j,d in enumerate(dl):
    print(f"    d={d}: all-pairs={allp[j]:.5f}  cross-word={cw[j]:.5f}  cw-excess={cw_exc[j]:+.5f}")
cwlr=cw_exc.clip(min=0).sum()
print(f"  cross-word LR excess sum={cwlr:.5f}  ({100*cwlr/HL:.3f}% of H1) -> "
      f"{'PASS' if 100*cwlr/HL>=1 else 'FAIL (LR letter order = morphology/word-periodicity, not new structure)'}")
print(f"\n[total {time.time()-t0:.1f}s]")
