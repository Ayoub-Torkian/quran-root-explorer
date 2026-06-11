#!/usr/bin/env python3
# CONTROL — does rhyme<->root coupling survive removing the rhyme-bearing (final) word's root?
# If yes: genuine sound<->meaning binding. If it collapses: it's formulaic end-words (less novel).
import glob,unicodedata,numpy as np
from collections import defaultdict,Counter
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'
# need per-word roots to drop the last word; use morphology root-per-token if available, else approx:
# roots_by_ayah is a bag; we instead rebuild from the per-token roots file if present
import os
TOK=R+'/research/two_books_genome/roots_by_token.tsv'
print('token-root file present:',os.path.exists(TOK))
AR=set(chr(c) for c in range(0x621,0x64B))
def skel(s):
    s=unicodedata.normalize('NFD',s);return ''.join(c for c in s if c in AR)
# Build per-ayah ordered token roots
tokroots=defaultdict(list)
if os.path.exists(TOK):
    for ln in open(TOK,encoding='utf-8'):
        p=ln.rstrip('\n').split('\t')
        if len(p)>=2 and p[1] and p[1]!='NA':tokroots[p[0].strip()].append(p[1])
keys=[];rhyme=[];allr=[];minus_last=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1);k=sa.strip();sk=skel(tx.strip())
    if len(sk)<2:continue
    tr=tokroots.get(k,[])
    keys.append(k);rhyme.append(sk[-2:]);allr.append(set(tr));minus_last.append(set(tr[:-1]) if len(tr)>1 else set())
N=len(keys);rng=np.random.default_rng(3)
rc=Counter(rhyme);keep={r for r,c in rc.items() if c>=8}
idx=[i for i in range(N) if rhyme[i] in keep and allr[i]]
by=defaultdict(list)
for i in idx:by[rhyme[i]].append(i)
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
    floor=np.array(floor);z=(wr-floor.mean())/(floor.std()+1e-9)
    print(f"{label}: same-rhyme sharing {wr:.3f} vs shuffle {floor.mean():.3f}±{floor.std():.3f}  z={z:.1f}")
print(f"verses usable (token roots): {len(idx)}")
if len(idx)>500:
    test(allr,'(full verse roots)')
    test(minus_last,'(MINUS rhyme-bearing last word)')
else:
    print('token-root file missing/insufficient -> cannot run control cleanly')
