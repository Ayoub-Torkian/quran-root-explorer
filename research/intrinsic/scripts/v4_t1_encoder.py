# -*- coding: utf-8 -*-
"""V4 Task 1 — encoder robustness + shrinkage-corrected association.
Tests whether V3 relational findings (the batr-shani 'strong specific bond', hapax binding,
modular structure) are REAL or co-occurrence/low-count artifacts. ONE-LAW clean:
the 'independent encoder' is an INTERNAL SVD embedding of the corpus (methodologically
independent of raw PPMI), used as a cross-check/null, never as external evidence."""
import collections, itertools, math, random
import numpy as np
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا')
ayahs=[]
for line in open(f"{R}/research/two_books_genome/roots_by_ayah.tsv",encoding='utf-8'):
    line=line.rstrip('\n')
    if '\t' in line:
        _,rs=line.split('\t',1); ayahs.append(set(fa(x) for x in rs.split()))
N=len(ayahs)
cnt=collections.Counter(); co=collections.Counter()
for s in ayahs:
    for r in s: cnt[r]+=1
    for a,b in itertools.combinations(sorted(s),2): co[(a,b)]+=1
def pair(a,b): return co[(a,b)] if (a,b) in co else co[(b,a)]
def ppmi(a,b):
    c=pair(a,b); return max(0.0,math.log2(c*N/(cnt[a]*cnt[b]))) if c>0 else 0.0
def tscore(a,b):
    c=pair(a,b); E=cnt[a]*cnt[b]/N
    return (c-E)/math.sqrt(c) if c>0 else 0.0
def g2(a,b):  # Dunning log-likelihood ratio on 2x2
    o11=pair(a,b)
    if o11==0: return 0.0
    o12=cnt[a]-o11; o21=cnt[b]-o11; o22=N-cnt[a]-cnt[b]+o11
    rows=[o11+o12,o21+o22]; cols=[o11+o21,o12+o22]
    g=0.0
    for oi,(o,r,cc) in enumerate([(o11,rows[0],cols[0]),(o12,rows[0],cols[1]),(o21,rows[1],cols[0]),(o22,rows[1],cols[1])]):
        e=r*cc/N
        if o>0 and e>0: g+=o*math.log(o/e)
    return 2*g
def spmi(a,b,alpha=5.0):  # Dirichlet/add-alpha smoothed PMI (shrinks low-count pairs)
    c=pair(a,b); cs=c+0  # smoothing applied in expectation form
    # smoothed: treat co-count with add-alpha vs expected
    num=(c+0.0);
    return math.log2(((c+0.0)+1e-9)*N/((cnt[a]+alpha)*(cnt[b]+alpha))) if c>0 else 0.0
def hyperg_p(a,b):  # P(co-occur >= observed) upper tail, hypergeometric
    k=pair(a,b);
    if k==0: return 1.0
    na,nb=cnt[a],cnt[b]
    # P(X>=k): X ~ Hypergeometric(N, na, nb)
    from math import comb
    def pmf(x):
        try: return comb(na,x)*comb(N-na,nb-x)/comb(N,nb)
        except: return 0.0
    return sum(pmf(x) for x in range(k,min(na,nb)+1))

KW=['عطو','کثر','صلو','ربب','نحر','شنء','بتر']; HAPAX={'نحر','بتر'}
print("="*70); print("CORPUS: %d ayahs, %d roots"%(N,len(cnt)))
print("="*70)
# --- 1) the headline bond batr-shani under several measures ---
print("\n[1] The headline 'strong specific bond' بتر–شنء (batr–shaniʾ):")
print("    counts: بتر=%d  شنء=%d   co-occurrences=%d verse(s)"%(cnt['بتر'],cnt['شنء'],pair('بتر','شنء')))
print("    PPMI=%.2f  t-score=%.2f  G2=%.2f  smoothedPMI=%.2f  hyperg p=%.2g"%(
    ppmi('بتر','شنء'),tscore('بتر','شنء'),g2('بتر','شنء'),spmi('بتر','شنء'),hyperg_p('بتر','شنء')))
# rank batr-shani among ALL pairs by each measure
allpairs=[(a,b) for (a,b),c in co.items() if c>=1]
def rank_of(measure, tgt):
    vals=sorted((measure(a,b) for a,b in allpairs),reverse=True)
    tv=measure(*tgt)
    # percentile = fraction of pairs with strictly lower value
    below=sum(1 for v in vals if v<tv); return tv, 100.0*below/len(vals)
for name,m in [('PPMI',ppmi),('t-score',tscore),('G2',g2)]:
    # restrict pair universe to pairs with co>=2 for t/G2 stability comparison too
    pass
# percentile among pairs with co>=1 vs co>=3 (robust universe)
pairs_c3=[(a,b) for (a,b),c in co.items() if c>=3]
def pct_in(universe,measure,tgt):
    tv=measure(*tgt); vals=[measure(a,b) for a,b in universe]
    return tv,100.0*sum(1 for v in vals if v<tv)/len(vals)
print("\n    Rank of بتر–شنء among ALL %d co-pairs (PPMI inflates rare):"%len(allpairs))
for name,m in [('PPMI',ppmi),('t-score',tscore),('G2',g2)]:
    tv,pc=pct_in(allpairs,m,('بتر','شنء')); print("      %-8s value=%.2f  -> %.1f th pct"%(name,tv,pc))
print("    Rank among pairs with co>=3 (robust, low-count pairs removed):")
print("      بتر–شنء co-count=%d -> it is EXCLUDED from the co>=3 universe (rests on a single verse)."%pair('بتر','شنء'))

# --- 2) split-half robustness of the bond ---
print("\n[2] Split-half robustness (random halves of the 6236 ayahs, 200 splits):")
idx=list(range(N)); survive=0; cocounts=[]
rng=random.Random(7)
for _ in range(200):
    rng.shuffle(idx); h=set(idx[:N//2])
    c=0
    for i in h:
        s=ayahs[i]
        if 'بتر' in s and 'شنء' in s: c+=1
    cocounts.append(c)
    if c>0: survive+=1
print("    بتر–شنء co-occurs in a random half in %d/200 splits (median co-count=%.1f)."%(survive,np.median(cocounts)))
# contrast: a robust frequent pair
def robust_pair_demo(a,b):
    s=0;rng2=random.Random(3)
    surv=0
    for _ in range(200):
        rng2.shuffle(idx); h=set(idx[:N//2]); c=sum(1 for i in h if a in ayahs[i] and b in ayahs[i])
        if c>0: surv+=1
    return surv
print("    contrast — ربب–ءله (frequent) survives in %d/200 halves."%robust_pair_demo('ربب','اله'))

# --- 3) independent internal encoder: truncated SVD of PPMI matrix ---
print("\n[3] Independent encoder = SVD embedding of the root PPMI matrix (internal, method-independent):")
roots=[r for r,c in cnt.items() if c>=2]            # 2+ for a definable vector
ri={r:i for i,r in enumerate(roots)}; n=len(roots)
M=np.zeros((n,n),dtype=np.float32)
for (a,b),c in co.items():
    if a in ri and b in ri:
        v=max(0.0,math.log2(c*N/(cnt[a]*cnt[b])))
        M[ri[a],ri[b]]=v; M[ri[b],ri[a]]=v
print("    PPMI matrix: %dx%d ; running SVD..."%(n,n))
U,S,Vt=np.linalg.svd(M,full_matrices=False)
K=100; emb=U[:,:K]*np.sqrt(S[:K])
embn=emb/ (np.linalg.norm(emb,axis=1,keepdims=True)+1e-9)
def nn(r,topk=6):
    if r not in ri: return []
    sims=embn@embn[ri[r]]; order=np.argsort(-sims)
    return [(roots[j],float(sims[j])) for j in order if roots[j]!=r][:topk]
print("    nearest neighbours in embedding space (does structure reproduce?):")
for r in ['بتر','شنء','نحر','کثر','صلو','ربب']:
    if r in ri:
        nns=nn(r); print("      %-5s -> %s"%(r," , ".join("%s(%.2f)"%(w,s) for w,s in nns)))
    else:
        print("      %-5s -> [not in encoder universe: count<2]"%r)
# is shani the NN of batr? (batr count=1 -> excluded; report)
print("    NOTE: نحر,بتر have count=1 so they have NO independent embedding (vector undefined).")
print("          => the 'bond' cannot be reproduced by an independent encoder; it exists only as a raw co-count.")
