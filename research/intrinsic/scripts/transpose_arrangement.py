#!/usr/bin/env python3
# Does the (ayah-position, sura)-sorted arrangement (the TRANSPOSE) carry NEW latent structure?
# Neighbors in this order are mostly SAME-POSITION verses across different sūras.
# Test: do same-position cross-sūra verse pairs share roots above the cross-sūra chance baseline?
# Control for the known opening-formulae effect (L18) by reporting per-position AND excluding p<=2.
import glob,numpy as np
from collections import defaultdict
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:k,r=ln.rstrip('\n').split('\t',1);roots[k]=set(x for x in r.split() if x and x!='NA')
sura=[];pos=[];vr=[]
cur=None;p=0
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,_=ln.split('\t',1);s,a=sa.split(':');s=int(s);a=int(a)
    sura.append(s);pos.append(a);vr.append(roots.get(sa.strip(),set()))
sura=np.array(sura);pos=np.array(pos);N=len(sura)
rng=np.random.default_rng(7)
def share(i,j):return 1 if vr[i]&vr[j] else 0
# baseline: random CROSS-sūra pairs
base=np.mean([share(*rng.choice(N,2,replace=False)) for _ in range(20000)
              if True])
# recompute base ensuring cross-sūra
bs=[]
while len(bs)<20000:
    i,j=rng.integers(0,N),rng.integers(0,N)
    if sura[i]!=sura[j]:bs.append(share(i,j))
base=np.mean(bs)
print(f"cross-sūra random-pair baseline (chance for the transpose): {base:.3f}")
# same-position cross-sūra pairs, per position
byp=defaultdict(list)
for i in range(N):byp[pos[i]].append(i)
print("\nsame-position cross-sūra root-sharing vs baseline:")
allsame=[]
for pp in range(1,13):
    idx=byp[pp]
    if len(idx)<20:continue
    pr=[]
    for _ in range(4000):
        i,j=rng.choice(idx,2,replace=False)
        if sura[i]!=sura[j]:pr.append(share(i,j))
    allsame+= [(pp,np.mean(pr),len(idx))]
    print(f"  pos {pp:>2}: {np.mean(pr):.3f}  (n={len(idx)} sūras)  {'<= opening formulae (L18)' if pp<=2 else ''}")
# pooled same-position EXCLUDING p<=2 (remove known opening effect), with permutation null
pairs=[]
for pp in range(3,400):
    idx=byp.get(pp,[])
    if len(idx)<3:continue
    for _ in range(min(2000,len(idx)*3)):
        i,j=rng.choice(idx,2,replace=False)
        if sura[i]!=sura[j]:pairs.append((int(i),int(j)))
real=np.mean([share(i,j) for i,j in pairs])
# permutation null: shuffle POSITION labels among verses (break position structure), recompute same stat
posarr=pos.copy()
floor=[]
for _ in range(300):
    perm=rng.permutation(N); pmap={k:posarr[perm[k]] for k in range(N)}
    bp=defaultdict(list)
    for k in range(N):
        if pmap[k]>=3:bp[pmap[k]].append(k)
    acc=[]
    for pp,idx in bp.items():
        if len(idx)<3:continue
        for _ in range(2):
            i,j=rng.choice(idx,2,replace=False)
            if sura[i]!=sura[j]:acc.append(share(i,j))
    floor.append(np.mean(acc))
floor=np.array(floor)
print(f"\nPOOLED same-position (pos>=3, excludes opening formulae): real {real:.3f} vs baseline {base:.3f}")
print(f"   permutation null (position labels shuffled): {floor.mean():.3f} ± {floor.std():.3f}  -> z={(real-floor.mean())/(floor.std()+1e-9):.1f}")
