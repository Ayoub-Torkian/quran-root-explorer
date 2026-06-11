#!/usr/bin/env python3
# C5 promotion — do refrains mark REAL sections? Two more independent channels vs a random-
# placement null, for the 5 refrain sūras: (B) WAVE — verse-length is more homogeneous within
# refrain-delimited sections than within random partitions; (C) CONTENT — root distribution
# SHIFTS across refrain boundaries more than across random boundaries.
import glob,unicodedata,numpy as np
from collections import defaultdict,Counter
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
def norm(t):
    t=unicodedata.normalize('NFD',t);t=''.join(c for c in t if not unicodedata.combining(c))
    return ' '.join(''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()).strip()
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln: k,r=ln.rstrip('\n').split('\t',1); roots[k]=set(x for x in r.split() if x and x!='NA')
sur=defaultdict(list)
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1); su,ay=map(int,sa.split(':')); sur[su].append((norm(tx),len(norm(tx).split()),roots.get(sa.strip(),set())))
rng=np.random.default_rng(0)
def sections(pos,n):
    cuts=[-1]+pos+[n]; return [(cuts[i]+1,cuts[i+1]) for i in range(len(cuts)-1)]
def within_len_var(pos,vs):
    s=sections(pos,len(vs)); v=[]
    for a,b in s:
        L=[vs[i][1] for i in range(a,b) if vs[i][0] not in REF]   # exclude refrain verses
        if len(L)>=2: v.append(np.var(L))
    return np.mean(v) if v else np.nan
def boundary_shift(pos,vs):
    d=[]
    for p in pos:
        before=set().union(*[vs[i][2] for i in range(max(0,p-4),p)]) if p>0 else set()
        after=set().union(*[vs[i][2] for i in range(p+1,min(len(vs),p+5))])
        if before or after: d.append(1-len(before&after)/(len(before|after)+1e-9))
    return np.mean(d) if d else np.nan
res=[]
for su in (55,77,26,37,54):
    vs=sur[su]; n=len(vs); c=Counter(x[0] for x in vs)
    ref=[v for v,k in c.items() if k>=3 and len(v)>=6]; 
    if not ref: continue
    REF={max(((v,c[v]) for v in ref),key=lambda t:t[1])[0]}
    pos=[i for i in range(n) if vs[i][0] in REF]; k=len(pos)
    rv=within_len_var(pos,vs); rs=boundary_shift(pos,vs)
    nullv=[];nulls=[]
    for _ in range(500):
        rp=sorted(rng.choice(n,k,replace=False)); nullv.append(within_len_var(rp,vs)); nulls.append(boundary_shift(rp,vs))
    res.append((su,rv,np.nanmean(nullv),rs,np.nanmean(nulls)))
    print(f"  sūra {su}: len-var within={rv:.1f} vs random {np.nanmean(nullv):.1f} ({'OK' if rv<np.nanmean(nullv) else 'no'}) | root-shift={rs:.2f} vs random {np.nanmean(nulls):.2f} ({'OK' if rs>np.nanmean(nulls) else 'no'})")
res=np.array([(r[1],r[2],r[3],r[4]) for r in res])
print(f"\n(B) WAVE: sections more length-homogeneous than random in {np.mean(res[:,0]<res[:,1])*100:.0f}% of sūras (real {res[:,0].mean():.1f} < random {res[:,1].mean():.1f})")
print(f"(C) CONTENT: root-shift bigger at refrains than random in {np.mean(res[:,2]>res[:,3])*100:.0f}% of sūras (real {res[:,2].mean():.2f} > random {res[:,3].mean():.2f})")
