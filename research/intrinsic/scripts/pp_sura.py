#!/usr/bin/env python3
# SŪRA-scale point pattern. y = normalized verse position WITHIN sūra (0=first..1=last),
# x = position within āyah. Per root: (A) does it prefer sūra-early vs sūra-late verses?
# (B) DRIFT: does verse-position (x) depend on within-sūra position (y)?
import glob,numpy as np,collections
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
ord_=[]
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:k,r=ln.rstrip('\n').split('\t',1);ord_.append((int(k.split(':')[0]),[x for x in r.split() if x and x!='NA']))
# within-sūra verse index
from collections import defaultdict
sver=defaultdict(int); slen=defaultdict(int)
rows=[]
order=[]
for s,v in ord_: order.append((s,v))
# compute sūra lengths
for s,v in order: slen[s]+=1
idxs=defaultdict(int)
pts=defaultdict(list)
for s,v in order:
    yv=idxs[s]; sl=slen[s]; ynorm=yv/(sl-1) if sl>1 else .5; idxs[s]+=1
    L=len(v)
    for i,root in enumerate(v):
        pts[root].append((ynorm,(i/(L-1)) if L>1 else .5))
common=[r for r in pts if len(pts[r])>=40]
rng=np.random.default_rng(0)
ndrift=0; nclus=0
for r in common:
    P=np.array(pts[r]); y=P[:,0]; x=P[:,1]
    # (A) sūra-early vs late preference
    z_y=(y.mean()-0.5)/(y.std()/np.sqrt(len(y))+1e-9)
    if abs(z_y)>3: nclus+=1
    # (B) drift corr(x,y)
    rc=np.corrcoef(x,y)[0,1]; fl=[np.corrcoef(rng.permutation(x),y)[0,1] for _ in range(120)]
    if abs((rc-np.mean(fl))/(np.std(fl)+1e-9))>3: ndrift+=1
print("frequent roots: %d"%len(common))
print("(A) roots preferring sūra-EARLY or sūra-LATE verses (|z|>3): %d/%d"%(nclus,len(common)))
print("(B) roots with verse-position DRIFT across the sūra (|z|>3): %d/%d"%(ndrift,len(common)))
