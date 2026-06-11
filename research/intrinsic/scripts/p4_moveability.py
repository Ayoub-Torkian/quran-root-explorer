#!/usr/bin/env python3
# P4 — per-verse necessity ("moveability") map on the RASM. For each verse, is it more
# predictable in its TRUE place than where it would land elsewhere? Surprise = -logP of
# its final letter (rhyme) + length bin under the LOCAL neighbourhood model (window ±W,
# verse excluded). Compare in-place vs many random insertion points. Shuffle floor.
import glob,unicodedata,numpy as np
from collections import Counter
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'
def skel(t):
    t=unicodedata.normalize('NFD',t);t=''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
sura=[];fin=[];nw=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1); su=int(sa.split(':')[0]); w=skel(tx)
    sura.append(su); fin.append(w[-1][-1] if w and w[-1] else ''); nw.append(len(w))
N=len(fin); sura=np.array(sura)
fa=sorted(set(fin)); fid={c:i for i,c in enumerate(fa)}; FL=np.array([fid[c] for c in fin]); A=len(fa)
edges=np.array([0,1,2,3,4,5,6,8,10,13,17,22,29,38,50,66,87,115,300,10**9]); LB=np.digitize(np.array(nw),edges)-1; B=LB.max()+1
W=12; ALPHA=0.5
def surprise(flv,lbv,pos,order):
    # local window around 'pos' in the given order (exclude pos itself)
    lo=max(0,pos-W); hi=min(len(order),pos+W+1)
    idx=[order[k] for k in range(lo,hi) if k!=pos]
    if not idx: return 0.0
    fc=np.bincount(FL[idx],minlength=A)+ALPHA; lc=np.bincount(LB[idx],minlength=B)+ALPHA
    pf=fc[flv]/fc.sum(); pl=lc[lbv]/lc.sum()
    return -np.log2(pf)-np.log2(pl)
rng=np.random.default_rng(0)
order=np.arange(N)
def run(order,label,nrand=24):
    inpl=np.zeros(N); frac=np.zeros(N)
    # map verse-id -> its index in this order
    posof=np.empty(N,int); posof[order]=np.arange(N)
    for vid in range(N):
        p=posof[vid]; s_in=surprise(FL[vid],LB[vid],p,order)
        rp=rng.integers(0,N,nrand)
        s_rand=np.array([surprise(FL[vid],LB[vid],int(r),order) for r in rp])
        inpl[vid]=s_in; frac[vid]=np.mean(s_in<s_rand)   # fraction of random spots where in-place is BETTER (more predictable)
    print(f"  {label:22s} mean in-place surprise={inpl.mean():.2f} bits  |  verses more predictable in place than a random spot: {frac.mean()*100:.1f}%")
    return inpl,frac
print(f"N={N} verses · window ±{W} · rasm rhyme+length local model")
inpl,frac=run(order,"true order")
# shuffle floor: same on a globally shuffled verse order
sh=order.copy(); rng.shuffle(sh)
run(sh,"shuffled order (floor)")
# which verses are most 'locked in' (predictable in place) vs most surprising (load-bearing edges)
import numpy as np
rank=np.argsort(-frac)   # most locked-in first
print("\n  most LOCKED-IN verses (predictable in place, high %):")
# need sura:ayah; rebuild keys
keys=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' in ln: keys.append(ln.split('\t',1)[0])
for vid in rank[:5]: print(f"     {keys[vid]:8s} frac={frac[vid]*100:.0f}%")
print("  most SURPRISING-in-place verses (potential boundaries/edges):")
for vid in np.argsort(frac)[:5]: print(f"     {keys[vid]:8s} frac={frac[vid]*100:.0f}%")
# correlation: are sūra-edge verses (first/last) the most surprising-in-place?
is_edge=np.array([sura[i]!=sura[i-1] if i>0 else True or (i<N-1 and sura[i]!=sura[i+1]) for i in range(N)])
print(f"\n  mean frac at sūra-opening verses={frac[ (np.r_[True,sura[1:]!=sura[:-1]]) ].mean()*100:.1f}%  vs interior={frac[~np.r_[True,sura[1:]!=sura[:-1]]].mean()*100:.1f}%")
