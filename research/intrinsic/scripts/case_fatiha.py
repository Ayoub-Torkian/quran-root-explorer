#!/usr/bin/env python3
import glob,numpy as np
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
roots={};
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:k,r=ln.rstrip('\n').split('\t',1);roots[k]=set(x for x in r.split() if x and x!='NA')
txt={};order=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,t=ln.split('\t',1);txt[sa.strip()]=t.strip();order.append(sa.strip())
import collections
bysura=collections.defaultdict(list)
for k in order:bysura[int(k.split(':')[0])].append(k)
def chain(s):
    ks=bysura[s];sh=0
    rows=[]
    for i in range(len(ks)-1):
        a,b=ks[i],ks[i+1];common=roots.get(a,set())&roots.get(b,set())
        sh+= 1 if common else 0; rows.append((a,b,common))
    return sh/(len(ks)-1) if len(ks)>1 else 0,rows,len(ks)
# per-sura weave vs own shuffle (rank context)
rng=np.random.default_rng(1)
def adjshare(ks):
    return np.mean([1 if roots.get(ks[i],set())&roots.get(ks[i+1],set()) else 0 for i in range(len(ks)-1)])
scores={}
for s,ks in bysura.items():
    if len(ks)<10:continue
    real=adjshare(ks)
    fl=np.mean([adjshare(list(np.random.default_rng(s*100+t).permutation(ks))) for t in range(100)])
    scores[s]=(real,real-fl)
rank=sorted(scores.items(),key=lambda x:-x[1][1])
print("most-woven sūras (real adjacency, lift over own shuffle):")
for s,(r,l) in rank[:5]:print(f"  sūra {s}: real {r:.3f}  lift +{l:.3f}")
print("least-woven (of len>=10):")
for s,(r,l) in rank[-5:]:print(f"  sūra {s}: real {r:.3f}  lift +{l:.3f}")
# Fatiha case
fr,rows,nv=chain(1)
print(f"\n=== SŪRAT AL-FĀTIḤA (al-Ḥamd) — {nv} verses ===")
print(f"neighbour root-sharing: {fr:.2f}  ({sum(1 for *_,c in rows if c)}/{len(rows)} adjacent pairs share a root)")
for a,b,c in rows:
    print(f"  {a} ↔ {b}: {'SHARE '+' '.join(c) if c else 'no shared root'}")
print("  -> too short (6 pairs) for the statistic; built on rhetorical PROGRESSION, not lexical weave.")
# show a top-woven sura chain head
top=rank[0][0]
fr2,rows2,nv2=chain(top)
print(f"\n=== Contrast: SŪRA {top} ({nv2} v) — neighbour-sharing {fr2:.2f} (first 6 links) ===")
for a,b,c in rows2[:6]:
    print(f"  {a} ↔ {b}: {'SHARE '+' '.join(list(c)[:4]) if c else 'no'}")
