#!/usr/bin/env python3
# SURA-as-ORGAN, test 2: is each sura a MODULE (network community) in the body's wiring?
# Wiring = shared RARE roots (specific connections, not the generic high-freq vocabulary).
# Newman modularity Q of canonical partition vs random same-size contiguous partitions.
import collections, math, random
import numpy as np
random.seed(1); np.random.seed(1)
RBA="research/two_books_genome/roots_by_ayah.tsv"
verses=[]   # ordered (sura,[roots])
for ln in open(RBA,encoding='utf-8'):
    if '\t' not in ln: continue
    k,r=ln.rstrip('\n').split('\t',1); s=int(k.split(':')[0])
    verses.append((s,[x for x in r.split() if x and x!='NA']))
Nv=len(verses)
df=collections.Counter()
for _,rs in verses:
    for r in set(rs): df[r]+=1
def modularity(comm_of, band):
    lo,hi=band
    rare=lambda r: lo<=df[r]<=hi
    # m and k_i over rare roots: each rare root r forms a clique among its df verses
    m=sum(df[r]*(df[r]-1)//2 for r in df if rare(r))
    if m==0: return float('nan')
    k=np.zeros(Nv)
    vrare=[]   # rare roots per verse (as set)
    for i,(_,rs) in enumerate(verses):
        s=set(x for x in rs if rare(x)); vrare.append(s)
        k[i]=sum(df[r]-1 for r in s)
    # internal weight per community: for each rare root, group its verses by community
    root_verses=collections.defaultdict(list)
    for i,s in enumerate(vrare):
        for r in s: root_verses[r].append(i)
    inc=collections.Counter()
    for r,vs in root_verses.items():
        by=collections.Counter(comm_of[i] for i in vs)
        for c,cnt in by.items(): inc[c]+=cnt*(cnt-1)//2
    tot=collections.Counter()
    for i in range(Nv): tot[comm_of[i]]+=k[i]
    Q=0.0
    for c in set(comm_of):
        Q+= inc[c]/m - (tot[c]/(2*m))**2
    return Q
# canonical
comm=[s for s,_ in verses]
sizes=collections.Counter(comm); sizelist=[len(list(g)) for _,g in __import__('itertools').groupby(comm)]
# build canonical sizes in order
order_sizes=[]; cur=None;c=0
for s,_ in verses:
    if s!=cur: 
        if cur is not None: order_sizes.append(c)
        cur=s;c=1
    else:c+=1
order_sizes.append(c)
for band in [(2,30),(2,80),(3,150)]:
    Qc=modularity(comm,band)
    rs=[]
    for _ in range(60):
        sz=order_sizes[:]; random.shuffle(sz)
        cm=[]; ci=0
        for z in sz: cm+= [ci]*z; ci+=1
        rs.append(modularity(cm,band))
    rs=np.array(rs); z=(Qc-rs.mean())/rs.std()
    print(f"band rare-root freq {band}: canonical Q={Qc:.3f}  random={rs.mean():.3f}±{rs.std():.3f}  z={z:+.1f}  -> {'ORGANS (communities)' if z>3 else 'not special'}")
