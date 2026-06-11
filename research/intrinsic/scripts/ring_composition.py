#!/usr/bin/env python3
# FRESH PROBE — ring / chiastic composition. Are symmetric verse pairs (i, n+1-i) more
# root-similar than the same positions filled by verses shuffled WITHIN the sūra? The shuffle
# holds the positions/distances fixed, isolating mirror structure. Per-sūra paired test.
import glob,numpy as np,collections
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:k,r=ln.rstrip('\n').split('\t',1);roots[k]=set(x for x in r.split() if x and x!='NA')
bys=collections.defaultdict(list)
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,_=ln.split('\t',1);bys[int(sa.split(':')[0])].append(roots.get(sa.strip(),set()))
def jac(a,b):
    u=a|b;return len(a&b)/len(u) if u else 0.0
def ring_score(V):
    n=len(V);return np.mean([jac(V[i],V[n-1-i]) for i in range(n//2)])
rng=np.random.default_rng(5)
reals=[];diffs=[];wins=0;n_used=0
for s,V in bys.items():
    if len(V)<7:continue
    real=ring_score(V)
    fl=np.mean([ring_score(list(rng.permutation(np.array(V,dtype=object)))) for _ in range(150)])
    reals.append(real);diffs.append(real-fl);wins+=(real>fl);n_used+=1
diffs=np.array(diffs);t=diffs.mean()/(diffs.std(ddof=1)/np.sqrt(len(diffs)))
print("sūras tested (n>=7 verses): %d" % n_used)
print("mean symmetric-pair similarity: %.4f" % np.mean(reals))
print("mean(real - within-sūra shuffle): %+.4f" % diffs.mean())
print("paired t (each sūra one unit): %.1f" % t)
print("sūras with real > shuffle: %d / %d" % (wins,n_used))
# also: restrict to OUTER pairs (first/last third) to test true book-end framing, distance-matched by shuffle
def ring_outer(V):
    n=len(V);k=max(1,n//3);return np.mean([jac(V[i],V[n-1-i]) for i in range(k)])
do=[];wo=0
for s,V in bys.items():
    if len(V)<9:continue
    real=ring_outer(V);fl=np.mean([ring_outer(list(rng.permutation(np.array(V,dtype=object)))) for _ in range(150)])
    do.append(real-fl);wo+=(real>fl)
do=np.array(do);to=do.mean()/(do.std(ddof=1)/np.sqrt(len(do)))
print("\nOUTER (book-end) pairs only: paired t=%.1f, %d/%d sūras positive, mean lift %+.4f" % (to,wo,len(do),do.mean()))
