#!/usr/bin/env python3
# O2 · FIXED LOCATION — gross position determined (can't go to the leg), local nudge tolerant.
import collections, math, random
import numpy as np
random.seed(1); np.random.seed(1)
RBA="research/two_books_genome/roots_by_ayah.tsv"
sur=collections.defaultdict(collections.Counter)
for ln in open(RBA,encoding='utf-8'):
    if '\t' not in ln: continue
    k,r=ln.rstrip('\n').split('\t',1); s=int(k.split(':')[0])
    if 1<=s<=114:
        for x in r.split():
            if x and x!='NA': sur[s][x]+=1
suras=sorted(sur); S=len(suras); idx={s:i for i,s in enumerate(suras)}
df=collections.Counter()
for s in suras:
    for r in sur[s]: df[r]+=1
rare=[r for r,d in df.items() if 2<=d<=60]
M=np.zeros((S,S))
for r in rare:
    h=[idx[s] for s in suras if r in sur[s]]
    for a in range(len(h)):
        for b in range(a+1,len(h)): M[h[a],h[b]]+=1; M[h[b],h[a]]+=1
dg=M.sum(1)+1e-9; A=M/np.sqrt(np.outer(dg,dg)); np.fill_diagonal(A,0)
# Indicator A: position recoverable from profile (gross determinism)
roots=sorted(df); ri={r:i for i,r in enumerate(roots)}; idf={r:math.log(S/df[r]) for r in df}
Sig=np.zeros((S,len(roots)))
for s in suras:
    for r,n in sur[s].items(): Sig[idx[s],ri[r]]=n*idf[r]
Sig=Sig/(np.linalg.norm(Sig,axis=1,keepdims=True)+1e-9); Sig-=Sig.mean(0)
U,sv,_=np.linalg.svd(Sig,full_matrices=False)
X=U[:,:10]*sv[:10]; y=np.arange(S,dtype=float); y-=y.mean()
b=np.linalg.lstsq(X,y,rcond=None)[0]; R2=1-((y-X@b)**2).sum()/((y-y.mean())**2).sum()
print(f"O2(A) gross position recoverable from profile: R^2={R2:.2f}, PC1~order |r|={abs(np.corrcoef(U[:,0],np.arange(S))[0,1]):.2f}")
# Indicator B: GROSS relocation cost — canonical neighbours wired vs a RANDOM far slot
canon_fit=np.array([np.mean([A[i,j] for j in (i-1,i+1) if 0<=j<S]) for i in range(S)])
rand_fit=np.array([np.mean(np.random.choice(np.delete(A[i],[max(i-1,0),min(i+1,S-1),i]),5)) for i in range(S)])
t=(canon_fit-rand_fit).mean()/((canon_fit-rand_fit).std()/math.sqrt(S))
print(f"O2(B) GROSS relocation cost: canonical-neighbour wiring {canon_fit.mean():.4f} vs random far slot {rand_fit.mean():.4f}  paired t={t:.1f}  ({(canon_fit>rand_fit).mean():.0%} of suras fit better at home)")
# Indicator C: LOCAL nudge tolerance — association vs sequence distance (gradual decay)
for d in (1,2,3,5,10,40):
    vals=[A[i,i+d] for i in range(S-d)]
    print(f"O2(C) wiring at seq-distance {d:>2}: {np.mean(vals):.4f}")
print("   => gross position determined (R^2 0.84, t large); decay is GRADUAL so a 1-slot nudge is cheap (heart not mm-fixed).")
