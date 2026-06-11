#!/usr/bin/env python3
# CANDIDATE — form<->content coupling. Is a verse's RHYME-CLASS (sound/form) statistically
# bound to its ROOT-FIELD (meaning)? If sound & meaning were independent channels, verses
# sharing a rhyme would share roots no more than chance. Test on rasm.
# 3 angles: (A) mutual information rhyme<->dominant-root vs shuffle; (B) verses sharing a
# rhyme share >=1 root above chance; (C) AUC: can rhyme-class predict root-field cluster.
import glob,unicodedata,numpy as np
from collections import defaultdict,Counter
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
AR=set(chr(c) for c in range(0x621,0x64B))
def skel(s):
    s=unicodedata.normalize('NFD',s);return ''.join(c for c in s if c in AR)
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:k,r=ln.rstrip('\n').split('\t',1);roots[k]=set(x for x in r.split() if x and x!='NA')
keys=[];rhyme=[];vr=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1);sk=skel(tx.strip())
    if len(sk)<2:continue
    keys.append(sa.strip());rhyme.append(sk[-2:]);vr.append(roots.get(sa.strip(),set()))   # rhyme = last 2 rasm consonants
N=len(keys)
# keep rhyme classes with >=8 members
rc=Counter(rhyme);keep={r for r,c in rc.items() if c>=8}
idx=[i for i in range(N) if rhyme[i] in keep]
print(f"verses: {N}; rhyme-classes(>=8): {len(keep)}; verses in those classes: {len(idx)}")
# (B) within-rhyme vs cross-rhyme root sharing
import random
rng=np.random.default_rng(3)
def share_rate(pairs):
    return np.mean([1 if (vr[i]&vr[j]) else 0 for i,j in pairs])
by=defaultdict(list)
for i in idx:by[rhyme[i]].append(i)
within=[]
for r,members in by.items():
    if len(members)<2:continue
    for _ in range(min(300,len(members)*2)):
        a,b=rng.choice(members,2,replace=False);within.append((int(a),int(b)))
cross=[]
for _ in range(len(within)):
    a,b=rng.choice(idx,2,replace=False)
    if rhyme[a]!=rhyme[b]:cross.append((int(a),int(b)))
wr=share_rate(within);cr=share_rate(cross)
print(f"(B) root-sharing: same-rhyme pairs {wr:.3f} vs different-rhyme pairs {cr:.3f}  (lift {wr/cr:.2f}x)")
# shuffle floor: permute rhyme labels, recompute
floor=[]
for _ in range(200):
    perm=rng.permutation(idx)
    rmap={idx[k]:rhyme[perm[k]] for k in range(len(idx))}
    byp=defaultdict(list)
    for i in idx:byp[rmap[i]].append(i)
    wp=[]
    for r,m in byp.items():
        if len(m)<2:continue
        for _ in range(2):
            a,b=rng.choice(m,2,replace=False);wp.append(1 if vr[a]&vr[b] else 0)
    floor.append(np.mean(wp))
floor=np.array(floor)
z=(wr-floor.mean())/(floor.std()+1e-9)
print(f"    shuffle floor {floor.mean():.3f}±{floor.std():.3f}  ->  z={z:.1f}")
# (A) mutual information between rhyme-class and dominant-root
def dom_root(i):
    return next(iter(vr[i])) if vr[i] else None
xs=[rhyme[i] for i in idx if dom_root(i)];ys=[dom_root(i) for i in idx if dom_root(i)]
def MI(xs,ys):
    n=len(xs);px=Counter(xs);py=Counter(ys);pxy=Counter(zip(xs,ys));mi=0
    for (x,y),c in pxy.items():
        mi+=c/n*np.log2((c/n)/((px[x]/n)*(py[y]/n)))
    return mi
mi=MI(xs,ys)
mif=[]
for _ in range(200):
    mif.append(MI(xs,list(rng.permutation(ys))))
mif=np.array(mif)
print(f"(A) MI(rhyme; dominant-root)={mi:.3f} bits  vs shuffle {mif.mean():.3f}±{mif.std():.3f}  z={(mi-mif.mean())/(mif.std()+1e-9):.1f}")
