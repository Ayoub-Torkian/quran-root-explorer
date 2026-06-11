#!/usr/bin/env python3
# Quick first probe of C12 — do root PAIRS hold a fixed signed gap within the āyah?
# For frequent ordered pairs co-occurring >=25x, measure gap concentration (modal-fraction)
# vs a within-verse token-shuffle null.
import glob,numpy as np,collections
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
verses=[]
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:
        _,r=ln.split('\t',1);v=[x for x in r.split() if x and x!='NA']
        if 3<=len(v)<=40:verses.append(v)
def gaps(vs):
    g=collections.defaultdict(list)
    for v in vs:
        for i in range(len(v)):
            for j in range(i+1,len(v)):
                if v[i]!=v[j]:g[(v[i],v[j])].append(j-i)
    return g
G=gaps(verses)
pairs=[(k,v) for k,v in G.items() if len(v)>=25]
def modal_frac(gl):
    c=collections.Counter(gl);return c.most_common(1)[0][1]/len(gl)
real=np.mean([modal_frac(v) for k,v in pairs])
rng=np.random.default_rng(0)
fl=[]
for _ in range(40):
    vs=[list(rng.permutation(v)) for v in verses];Gs=gaps(vs)
    mm=[modal_frac(Gs[k]) for k,v in pairs if k in Gs and len(Gs[k])>=25]
    fl.append(np.mean(mm))
fl=np.array(fl);z=(real-fl.mean())/fl.std()
print('frequent ordered pairs (>=25 co-occurrences): %d'%len(pairs))
print('mean modal-gap fraction: real %.3f vs within-verse shuffle %.3f±%.3f  z=%+.1f'%(real,fl.mean(),fl.std(),z))
# show tightest fixed-offset pairs (highest modal fraction, gap of the mode)
tight=sorted(pairs,key=lambda kv:-modal_frac(kv[1]))[:8]
print('tightest fixed-offset pairs (A,B -> modal gap, %% at that gap, n):')
for (a,b),gl in tight:
    c=collections.Counter(gl);mg,mc=c.most_common(1)[0]
    print('   %s→%s  gap=%d  %.0f%%  (n=%d)'%(a,b,mg,100*mc/len(gl),len(gl)))
