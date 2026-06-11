#!/usr/bin/env python3
# BILATERAL PAIRS — matched near-identical sura pairs (reciprocal nearest neighbour + outlier similarity).
import collections, math
import numpy as np
RBA="research/two_books_genome/roots_by_ayah.tsv"
sur=collections.defaultdict(collections.Counter)
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:
        k,r=ln.rstrip('\n').split('\t',1); s=int(k.split(':')[0])
        if 1<=s<=114:
            for x in r.split():
                if x and x!='NA': sur[s][x]+=1
suras=sorted(sur); S=len(suras); idx={s:i for i,s in enumerate(suras)}
df=collections.Counter()
for s in suras:
    for r in sur[s]: df[r]+=1
roots=sorted(df); ri={r:i for i,r in enumerate(roots)}; idf={r:math.log(S/df[r]) for r in df}
X=np.zeros((S,len(roots)))
for s in suras:
    for r,n in sur[s].items(): X[idx[s],ri[r]]=n*idf[r]   # TF-IDF (distinctive shared roots)
X=X/(np.linalg.norm(X,axis=1,keepdims=True)+1e-9)
Cmat=X@X.T; np.fill_diagonal(Cmat,-1)
NAME={113:"Falaq",114:"Nas",105:"Fil",106:"Quraysh",73:"Muzzammil",74:"Muddathir",93:"Duha",94:"Sharh",
 81:"Takwir",82:"Infitar",87:"A'la",88:"Ghashiya",55:"Rahman",56:"Waqia",91:"Shams",92:"Layl",109:"Kafirun",112:"Ikhlas",95:"Tin",97:"Qadr"}
nm=lambda s: f"{s} {NAME.get(s,'')}".strip()
nn=Cmat.argmax(1)
allv=Cmat[np.triu_indices(S,1)]; mu,sd=allv.mean(),allv.std()
pairs=[]
for i in range(S):
    j=nn[i]
    if nn[j]==i and i<j:
        pairs.append((Cmat[i,j],suras[i],suras[j]))
pairs.sort(reverse=True)
print(f"all-pair similarity: mean {mu:.2f}, sd {sd:.2f}.  RECIPROCAL nearest-neighbour pairs (bilateral candidates):")
for c,a,b in pairs:
    z=(c-mu)/sd
    flag="<<< OUTLIER near-duplicate" if z>4 else ("strong" if z>3 else "")
    print(f"   {nm(a):16s} <-> {nm(b):16s}  sim={c:.2f}  z={z:+.1f}  {flag}")
print(f"\n   total reciprocal pairs: {len(pairs)}; outliers (z>4, true matched 'identical' pairs): {sum(1 for c,a,b in pairs if (c-mu)/sd>4)}")
