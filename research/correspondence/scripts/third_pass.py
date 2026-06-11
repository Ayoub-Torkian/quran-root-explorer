#!/usr/bin/env python3
# THIRD PASS — does sura LENGTH drive the relational attributes (O3, symmetry, folding)?
import collections, math, random
import numpy as np
random.seed(3); np.random.seed(3)
RBA="research/two_books_genome/roots_by_ayah.tsv"
sur=collections.defaultdict(collections.Counter)
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:
        k,r=ln.rstrip('\n').split('\t',1); s=int(k.split(':')[0])
        if 1<=s<=114:
            for x in r.split():
                if x and x!='NA': sur[s][x]+=1
suras=sorted(sur); S=len(suras); idx={s:i for i,s in enumerate(suras)}
df=collections.Counter()
for s in suras:
    for r in sur[s]: df[r]+=1
length=np.array([sum(sur[s].values()) for s in suras],float); loglen=np.log(length)
rare=[r for r in df if 2<=df[r]<=60]
M=np.zeros((S,S))
for r in rare:
    h=[idx[s] for s in suras if r in sur[s]]
    for a in range(len(h)):
        for b in range(a+1,len(h)): M[h[a],h[b]]+=1; M[h[b],h[a]]+=1
dg=M.sum(1)+1e-9; A=M/np.sqrt(np.outer(dg,dg)); np.fill_diagonal(A,0)
iu=np.triu_indices(S,1)
av=A[iu]
# length-similarity per pair
lsim=-np.abs(loglen[iu[0]]-loglen[iu[1]])
r_len=np.corrcoef(av,lsim)[0,1]
print(f"THIRD PASS — connectivity vs length-similarity:")
print(f"   corr(association, length-similarity) = {r_len:+.2f}  (R²={r_len**2:.2f} of connectivity explained by length alone)")
# residualize length out of association
b=np.polyfit(lsim,av,1); resid=av-np.polyval(b,lsim)
Ar=np.zeros((S,S)); Ar[iu]=resid; Ar=Ar+Ar.T
# 1) O3 — do named twins survive on the length-residual?
print("   O3 named twins on LENGTH-RESIDUAL association (percentile):")
for nm,(p,q) in {"113-114":(113,114),"2-3":(2,3),"8-9":(8,9),"105-106":(105,106)}.items():
    if p in idx and q in idx:
        v=Ar[idx[p],idx[q]]; print(f"      {nm}: {(resid<v).mean():.0%}")
# 2) symmetry — adjacent twins on residual vs random order
thr=np.quantile(resid,0.95)
real=sum(1 for i in range(S-1) if Ar[i,i+1]>thr)
nul=[sum(1 for i in range(S-1) if Ar[np.random.permutation(S)][:,np.random.permutation(S)][i,i+1]>thr) for _ in range(5)]  # rough
nul=[]
for _ in range(2000):
    p=np.random.permutation(S); nul.append(sum(1 for i in range(S-1) if Ar[p[i],p[i+1]]>thr))
z=(real-np.mean(nul))/np.std(nul)
print(f"   SYMMETRY on length-residual: {real} adjacent pairs vs random {np.mean(nul):.1f}±{np.std(nul):.1f}  z={z:+.1f}")
# 3) folding — distance decay on residual
dist=(iu[1]-iu[0])
print(f"   FOLDING on length-residual: corr(residual assoc, -seq_distance) = {np.corrcoef(resid,-dist)[0,1]:+.2f}")
# 4) adjacent length-similarity (is the order itself length-sorted locally?)
adjlen=np.mean([abs(loglen[i]-loglen[i+1]) for i in range(S-1)])
ranlen=np.mean([abs(loglen[a]-loglen[b]) for a,b in np.random.randint(0,S,(20000,2))])
print(f"   (context) adjacent sūras' length-gap {adjlen:.2f} vs random {ranlen:.2f} -> neighbours ARE length-similar")
