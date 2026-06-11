#!/usr/bin/env python3
# O8 re-find — CIRCULATION as PERFUSION: does the core message reach every region (even gaps) vs random?
import collections, random
import numpy as np
random.seed(1); np.random.seed(1)
RBA="research/two_books_genome/roots_by_ayah.tsv"
verses=[]
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:
        k,r=ln.rstrip('\n').split('\t',1); s=int(k.split(':')[0])
        if 1<=s<=114: verses.append(set(x for x in r.split() if x and x!='NA'))
N=len(verses)
def perfusion(carrier):
    mark=np.array([1 if (carrier & v) else 0 for v in verses])
    pos=np.where(mark)[0]
    if len(pos)<2: return None
    gaps=np.diff(np.concatenate([[-1],pos,[N]]))
    return mark.sum(), gaps.max(), gaps.std()/gaps.mean()
for name,carrier in [("God-reference ءله/ربب",{'ءله','ربب'}),("core 6 roots",{'ءله','ربب','کون','قول','علم','ءمن'})]:
    cnt,maxg,cv=perfusion(carrier)
    # null: random placement of same count
    nm=[];ncv=[]
    for _ in range(500):
        p=np.zeros(N); idx=np.random.choice(N,cnt,replace=False); p[idx]=1
        pos=np.where(p)[0]; g=np.diff(np.concatenate([[-1],pos,[N]])); nm.append(g.max()); ncv.append(g.std()/g.mean())
    zmax=(maxg-np.mean(nm))/np.std(nm); zcv=(cv-np.mean(ncv))/np.std(ncv)
    print(f"{name}: present in {cnt}/{N} verses ({cnt/N:.0%})")
    print(f"   max dry-gap {maxg} verses vs random {np.mean(nm):.0f}±{np.std(nm):.0f} (z={zmax:+.1f})  | gap-CV {cv:.2f} vs {np.mean(ncv):.2f} (z={zcv:+.1f})")
    print(f"   => {'MORE even than random (PERFUSION/circulation)' if zcv<-2 else 'clumpier than random (concentration, not perfusion)' if zcv>2 else 'about as even as random'}")
