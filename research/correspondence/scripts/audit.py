#!/usr/bin/env python3
# HONEST re-audit with PROPER nulls: O1 identity (canonical vs arbitrary segments), O3 connectivity (config model).
import collections, math, random
import numpy as np
random.seed(1); np.random.seed(1)
RBA="research/two_books_genome/roots_by_ayah.tsv"
V=[]
for ln in open(RBA,encoding='utf-8'):
    if '\t' not in ln: continue
    k,r=ln.rstrip('\n').split('\t',1); s=int(k.split(':')[0])
    if 1<=s<=114: V.append((s,[x for x in r.split() if x and x!='NA']))
N=len(V)
df=collections.Counter()
for s,rs in V:
    for r in set(rs): df[r]+=1
S=114; idf={r:math.log(S/df[r]) for r in df}

def classify_acc(seg):   # seg: list giving segment-id per verse
    cent=collections.defaultdict(lambda: collections.Counter())
    test=[]
    for i,(s,rs) in enumerate(V):
        if i%2==0:
            for r in rs: cent[seg[i]][r]+=1
        else:
            if rs: test.append((seg[i],rs))
    segs=list(cent)
    cvec={c:{r:cent[c][r]*idf.get(r,0) for r in cent[c]} for c in segs}
    cnrm={c:math.sqrt(sum(w*w for w in cvec[c].values()))+1e-9 for c in segs}
    ok=0
    for home,rs in test:
        q={r:idf[r] for r in rs if r in idf}; qn=math.sqrt(sum(w*w for w in q.values()))+1e-9
        best=None;bs=-1
        for c in segs:
            d=sum(q.get(r,0)*cvec[c].get(r,0) for r in q)/(qn*cnrm[c])
            if d>bs: bs=d; best=c
        ok+= (best==home)
    return ok/len(test)
canon=[s for s,_ in V]
acc_c=classify_acc(canon)
# arbitrary contiguous segments, same size multiset
sizes=[]; cur=None;c=0
for s,_ in V:
    if s!=cur:
        if cur is not None: sizes.append(c)
        cur=s;c=1
    else:c+=1
sizes.append(c)
accs=[]
for _ in range(15):
    sz=sizes[:]; random.shuffle(sz); seg=[]; cid=0
    for z in sz: seg+=[cid]*z; cid+=1
    accs.append(classify_acc(seg))
print("O1 IDENTITY — held-out verse -> home-segment accuracy:")
print(f"   canonical suras = {acc_c:.1%}   |   arbitrary same-size segments = {np.mean(accs):.1%}±{np.std(accs):.1%}")
print(f"   verdict: {'canonical SPECIAL (identity real)' if acc_c>np.mean(accs)+2*np.std(accs) else 'NOT special — local coherence, not sura-identity'}  (chance 0.9%)")

# O3 CONNECTIVITY config-model null
rare=[r for r in df if 2<=df[r]<=60]
sroots=collections.defaultdict(set)
for s,rs in V:
    for r in rs:
        if r in set(rare): sroots[s].add(r)
suras=sorted(sroots); rc={s:len(sroots[s]) for s in suras}
rd={r:sum(1 for s in suras if r in sroots[s]) for r in rare}
E=sum(rc.values())  # total incidences
M=collections.Counter()
for r in rare:
    h=[s for s in suras if r in sroots[s]]
    for i in range(len(h)):
        for j in range(i+1,len(h)): M[(h[i],h[j])]+=1
# expected shared under config model: sum_r p_ir p_jr, p_sr = rc[s]*rd[r]/E
import itertools
sig=0; tested=0
for (i,j),o in M.items():
    exp=sum((rc[i]*rd[r]/E)*(rc[j]*rd[r]/E) for r in rare if r in sroots[i] or r in sroots[j])
    if exp<=0: continue
    z=(o-exp)/math.sqrt(exp); tested+=1
    if z>3: sig+=1
print(f"\nO3 CONNECTIVITY — significant specific pairs under DEGREE-PRESERVING (config) null:")
print(f"   {sig}/{tested} pairs z>3 = {sig/max(tested,1):.0%}   (vs my earlier inflated 62% from a weak hypergeometric null)")
