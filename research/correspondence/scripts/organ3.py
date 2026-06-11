#!/usr/bin/env python3
# PROOF test: is the canonical sura partition a LOCAL OPTIMUM of wiring-modularity?
# Merge any 2 adjacent suras (remove a boundary) or split one (add a boundary) -> does Q DROP?  (احسن تقویم)
import collections
import numpy as np
RBA="research/two_books_genome/roots_by_ayah.tsv"
verses=[]
for ln in open(RBA,encoding='utf-8'):
    if '\t' not in ln: continue
    k,r=ln.rstrip('\n').split('\t',1); s=int(k.split(':')[0])
    verses.append((s,[x for x in r.split() if x and x!='NA']))
Nv=len(verses)
df=collections.Counter()
for _,rs in verses:
    for r in set(rs): df[r]+=1
LO,HI=2,80
rare=lambda r: LO<=df[r]<=HI
vrare=[set(x for x in rs if rare(x)) for _,rs in verses]
k=np.array([sum(df[r]-1 for r in s) for s in vrare],float)
m=sum(df[r]*(df[r]-1)//2 for r in df if rare(r))
# canonical communities (contiguous), in order
comm=[]; cur=None;ci=-1; bounds=[]
for i,(s,_) in enumerate(verses):
    if s!=cur: cur=s; ci+=1; bounds.append([i,i])
    comm.append(ci); bounds[ci][1]=i
ncomm=ci+1
# per-root per-community counts
rootcomm=collections.defaultdict(lambda: collections.Counter())
for i,sset in enumerate(vrare):
    for r in sset: rootcomm[r][comm[i]]+=1
inc=collections.Counter(); 
for r,cc in rootcomm.items():
    for c,n in cc.items(): inc[c]+=n*(n-1)//2
tot=np.zeros(ncomm)
for i in range(Nv): tot[comm[i]]+=k[i]
def e_between(setc1,setc2):  # inter edge weight between two verse-index sets
    # sum over rare roots of count_in_1 * count_in_2
    c1=collections.Counter(); 
    for i in setc1:
        for r in vrare[i]: c1[r]+=1
    e=0
    for i in setc2:
        for r in vrare[i]:
            if r in c1: e+=c1[r]
    return e
# MERGE test (remove boundary between k,k+1): dQ = e/m - tot_k*tot_{k+1}/(2 m^2)
verts_by_c=collections.defaultdict(list)
for i in range(Nv): verts_by_c[comm[i]].append(i)
merge_dq=[]
for c in range(ncomm-1):
    e=e_between(verts_by_c[c],verts_by_c[c+1])
    dq=e/m - tot[c]*tot[c+1]/(2*m*m)
    merge_dq.append(dq)
merge_dq=np.array(merge_dq)
# SPLIT test (add boundary at midpoint of each sura): dQ_split = -(e_halves/m - totA*totB/(2 m^2))
split_dq=[]
for c in range(ncomm):
    vs=verts_by_c[c]
    if len(vs)<2: split_dq.append(0.0); continue
    mid=len(vs)//2; A=vs[:mid]; B=vs[mid:]
    e=e_between(A,B); tA=k[A].sum(); tB=k[B].sum()
    dq=-(e/m - tA*tB/(2*m*m))
    split_dq.append(dq)
split_dq=np.array(split_dq)
print(f"MERGE (remove a boundary): {(merge_dq<0).mean():.0%} of {len(merge_dq)} merges LOWER Q  (mean ΔQ={merge_dq.mean():.2e})")
print(f"SPLIT (add a boundary):    {(split_dq<0).mean():.0%} of {len(split_dq)} splits LOWER Q  (mean ΔQ={split_dq.mean():.2e})")
print(f"  => canonical is a LOCAL OPTIMUM on {((merge_dq<0).mean()>0.5) and ((split_dq<0).mean()>0.5)} (both majorities lower Q = nothing to add/remove)")
# scale-invariance: Kawthar(108) and a few small suras — does merging them help (resolution limit) or hurt?
order=[s for s,_ in verses]; first={}
for i,(s,_) in enumerate(verses): first.setdefault(s,len(first))
for sx in [108,103,110,112,114,93]:
    c=first[sx]
    md = merge_dq[c] if c<len(merge_dq) else merge_dq[c-1]
    print(f"  sura {sx} (size {len(verts_by_c[c])}): merge-with-next ΔQ={md:+.2e} ({'hurts=organ' if md<0 else 'helps=resolution-limit'})")
