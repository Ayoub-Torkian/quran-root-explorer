#!/usr/bin/env python3
# STATISTICAL VALIDITY of L22, three orthogonal framings:
#  (1) Per-sūra PAIRED test (each sūra = 1 independent unit) -> no pair-dependence assumption.
#  (2) Global PERMUTATION p-value (pooled, apples-to-apples real vs null) -> exact, non-parametric.
#  (3) Sign test across sūras -> distribution-free.
import glob,numpy as np
from math import comb
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
bnd={s:(np.where(sura==s)[0][0],np.where(sura==s)[0][-1]+1) for s in np.unique(sura)}
alls=[s for s in np.unique(sura) if bnd[s][1]-bnd[s][0]>=10]
rng=np.random.default_rng(2024)
def adj(order):return np.mean([1 if vr[order[k]]&vr[order[k+1]] else 0 for k in range(len(order)-1)])
# (1) per-sūra: real vs mean of 200 within-sūra shuffles
diffs=[];wins=0
for s in alls:
    a,b=bnd[s];real=adj(list(range(a,b)))
    sh=np.mean([adj(list(rng.permutation(range(a,b)))) for _ in range(200)])
    diffs.append(real-sh); wins+= (real>sh)
diffs=np.array(diffs);n=len(diffs)
t=diffs.mean()/(diffs.std(ddof=1)/np.sqrt(n))
print("(1) PER-SŪRA PAIRED TEST  (each of %d sūras = 1 independent unit)" % n)
print("    mean(real - own_shuffle) = %+.4f   paired t = %.1f   (df=%d)" % (diffs.mean(),t,n-1))
print("    sūras where real > own shuffle: %d / %d" % (wins,n))
# (3) sign test exact two-sided p
p_sign=2*sum(comb(n,k) for k in range(wins,n+1))/(2**n)
print("(3) SIGN TEST exact two-sided p = %.2e" % min(1,p_sign))
# (2) global permutation p: pooled statistic, 5000 perms
real_pairs=[(i,i+1) for s in alls for i in range(bnd[s][0],bnd[s][1]-1)]
realstat=np.mean([1 if vr[i]&vr[j] else 0 for i,j in real_pairs])
ge=0;NP=5000;floor=[]
for _ in range(NP):
    acc=[]
    for s in alls:
        a,b=bnd[s];p=rng.permutation(range(a,b));acc+=[1 if vr[p[k]]&vr[p[k+1]] else 0 for k in range(len(p)-1)]
    v=np.mean(acc);floor.append(v);ge+= (v>=realstat)
floor=np.array(floor)
print("(2) GLOBAL PERMUTATION TEST  (pooled, %d permutations, same statistic both sides)" % NP)
print("    real = %.4f   null = %.4f ± %.4f   permutations >= real: %d  -> p < %.1e" %
      (realstat,floor.mean(),floor.std(),ge,1.0/NP if ge==0 else (ge+1)/(NP+1)))
print("    effect size: real is %.1f null-SDs out; Cohen's-style d on per-sūra diffs = %.2f" %
      ((realstat-floor.mean())/floor.std(), diffs.mean()/diffs.std(ddof=1)))
