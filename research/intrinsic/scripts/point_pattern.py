#!/usr/bin/env python3
# POINT PATTERN with root as anchor. Each occurrence = point (y=āyah index 1..6236, x=position
# within āyah, normalized 0..1). Per frequent root, characterize:
#  (A) x-concentration (tight positional band?)  -> = L27 territory
#  (B) y-clustering (occurrences clump in book regions?) -> = topical (L08) territory
#  (C) DRIFT: does x depend on y (verse-position changes through the book)? -> the NOVEL test
import glob,numpy as np,collections
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
rows=[]  # (yidx, root, xpos)
yi=0
for ln in open(RBA,encoding='utf-8'):
    if '\t' not in ln:continue
    _,r=ln.split('\t',1);v=[x for x in r.split() if x and x!='NA']
    L=len(v)
    for i,root in enumerate(v):
        rows.append((yi, root, (i/(L-1)) if L>1 else 0.5))
    yi+=1
NY=yi
pts=collections.defaultdict(list)
for y,r,x in rows: pts[r].append((y,x))
common=[r for r in pts if len(pts[r])>=40]
rng=np.random.default_rng(0)
ndrift=0; drifters=[]
xsd=[]
for r in common:
    P=np.array(pts[r]); y=P[:,0]/NY; x=P[:,1]
    xsd.append(x.std())
    # (C) drift: corr(x,y) vs shuffle of x
    rc=np.corrcoef(x,y)[0,1]
    fl=[np.corrcoef(rng.permutation(x),y)[0,1] for _ in range(200)]
    z=(rc-np.mean(fl))/(np.std(fl)+1e-9)
    if abs(z)>3:
        ndrift+=1; drifters.append((r,rc,z,len(P)))
print("frequent roots (>=40 occ): %d ; total points: %d over %d āyāt"%(len(common),len(rows),NY))
print("(A) within-āyah position spread: median root x-std = %.3f (0.29=uniform)"%np.median(xsd))
print("(C) DRIFT — roots whose verse-position changes through the book (|z|>3): %d / %d"%(ndrift,len(common)))
drifters.sort(key=lambda t:-abs(t[2]))
print("   strongest drifters (root, corr(x,book), z, n):")
for r,rc,z,n in drifters[:10]:
    print("     %-6s corr=%+.2f  z=%+.1f  n=%d  (%s)"%(r,rc,z,n,'moves LATER in verse over book' if rc>0 else 'moves EARLIER'))
