#!/usr/bin/env python3
import glob,unicodedata,numpy as np
from collections import defaultdict,Counter
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
AR=set(chr(c) for c in range(0x621,0x64B))
skel=lambda s:''.join(c for c in unicodedata.normalize('NFD',s) if c in AR)
ordroots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:k,r=ln.rstrip('\n').split('\t',1);ordroots[k]=[x for x in r.split() if x and x!='NA']
keys=[];rhyme=[];full=[];minus=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1);k=sa.strip();sk=skel(tx.strip())
    if len(sk)<2:continue
    tr=ordroots.get(k,[])
    if not tr:continue
    keys.append(k);rhyme.append(sk[-2:]);full.append(set(tr));minus.append(set(tr[:-1]))
N=len(keys);rng=np.random.default_rng(3)
rc=Counter(rhyme);keep={r for r,c in rc.items() if c>=8}
idx=[i for i in range(N) if rhyme[i] in keep and full[i]]
by=defaultdict(list)
for i in idx:by[rhyme[i]].append(i)
print(f"verses usable: {len(idx)}; rhyme-classes: {len(keep)}")
def test(field,label):
    within=[]
    for r,m in by.items():
        if len(m)<2:continue
        for _ in range(min(300,len(m)*2)):
            a,b=rng.choice(m,2,replace=False);within.append((int(a),int(b)))
    wr=np.mean([1 if field[i]&field[j] else 0 for i,j in within])
    floor=[]
    for _ in range(200):
        perm=rng.permutation(idx);rmap={idx[k]:rhyme[perm[k]] for k in range(len(idx))}
        byp=defaultdict(list)
        for i in idx:byp[rmap[i]].append(i)
        wp=[]
        for r,m in byp.items():
            if len(m)<2:continue
            for _ in range(2):
                a,b=rng.choice(m,2,replace=False);wp.append(1 if field[a]&field[b] else 0)
        floor.append(np.mean(wp))
    floor=np.array(floor);print(f"{label}: same-rhyme {wr:.3f} vs shuffle {floor.mean():.3f}±{floor.std():.3f}  z={(wr-floor.mean())/(floor.std()+1e-9):.1f}  lift={wr/floor.mean():.2f}x")
test(full,'(A) full verse roots         ')
test(minus,'(B) MINUS rhyme-bearing word ')
