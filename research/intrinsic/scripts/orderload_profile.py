#!/usr/bin/env python3
# CANDIDATE — positional order-load. Is the sequential binding between adjacent verses
# (how much the order matters) non-uniform along the sūra? Measure adjacent-verse root
# sharing by NORMALIZED position decile, vs a within-sūra order shuffle (the order null).
# If edges are more bound than the middle -> the sūra spine has a positional grammar.
import glob,numpy as np
from collections import defaultdict
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:k,r=ln.rstrip('\n').split('\t',1);roots[k]=set(x for x in r.split() if x and x!='NA')
sura=[];vr=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,_=ln.split('\t',1);sura.append(int(sa.split(':')[0]));vr.append(roots.get(sa.strip(),set()))
sura=np.array(sura)
bounds={}
for s in np.unique(sura):
    ix=np.where(sura==s)[0];bounds[s]=(ix[0],ix[-1]+1)
B=10
real=[[] for _ in range(B)]
for s,(a,b) in bounds.items():
    L=b-a
    if L<10:continue
    for i in range(a,b-1):
        p=(i-a)/(L-1); d=min(B-1,int(p*B))
        real[d].append(1 if vr[i]&vr[i+1] else 0)
prof=[np.mean(x) for x in real]
print("adjacent-verse root-sharing by normalized position decile (sūra start->end):")
for d in range(B):
    bar='#'*int(prof[d]*60)
    print(f"  {d*10:>3}-{d*10+10:>3}%  {prof[d]:.3f} {bar}")
# order null: shuffle verse order WITHIN each sūra, recompute profile, 200x
rng=np.random.default_rng(7)
floor=np.zeros((200,B))
order=[]
for s,(a,b) in bounds.items():
    if b-a>=10:order.append((a,b))
for t in range(200):
    buckets=[[] for _ in range(B)]
    for a,b in order:
        L=b-a;perm=rng.permutation(range(a,b))
        for k in range(L-1):
            p=k/(L-1);d=min(B-1,int(p*B))
            buckets[d].append(1 if vr[perm[k]]&vr[perm[k+1]] else 0)
    floor[t]=[np.mean(x) for x in buckets]
fm=floor.mean(0);fs=floor.std(0)
print("\nz-score vs within-sūra order shuffle (how much MORE bound than random order):")
for d in range(B):
    z=(prof[d]-fm[d])/(fs[d]+1e-9)
    print(f"  {d*10:>3}-{d*10+10:>3}%  real {prof[d]:.3f}  shuffle {fm[d]:.3f}  z={z:+.1f}")
edges=( (prof[0]+prof[-1])/2 ); mid=np.mean(prof[3:7])
print(f"\nEDGE mean (first+last decile) {edges:.3f}  vs  MIDDLE mean (30-70%) {mid:.3f}  -> edge/mid={edges/mid:.2f}x")
