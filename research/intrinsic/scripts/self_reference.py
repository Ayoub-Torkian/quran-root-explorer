import unicodedata, numpy as np
from collections import defaultdict, Counter
def skel(t):
    t=unicodedata.normalize('NFD',t); t=''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
toks=[]
for ln in open('/sessions/gifted-tender-cori/mnt/Quran_Root_Explorer_Web_v1.2/research/two_books_genome/data/quran/quran_arabic_verses.tsv',encoding='utf-8'):
    if '\t' not in ln: continue
    toks+=skel(ln.split('\t',1)[1])
toks=np.array(toks); N=len(toks)
cnt=Counter(toks); stop=set(w for w,_ in cnt.most_common(40))
bins=[(1,4),(5,16),(17,64),(65,256),(257,1024),(1025,4096),(4097,16384),(16385,70000)]
def curve(seq):
    pos=defaultdict(list)
    for i,w in enumerate(seq):
        if w not in stop: pos[w].append(i)
    hits=np.zeros(len(bins))
    for ps in pos.values():
        if len(ps)<2: continue
        for a,b in zip(ps,ps[1:]):
            d=b-a
            for k,(lo,hi) in enumerate(bins):
                if lo<=d<=hi: hits[k]+=1; break
    return hits
obs=curve(toks)
rng=np.random.default_rng(0); nsh=20; shf=np.zeros((nsh,len(bins)))
for s in range(nsh):
    shf[s]=curve(toks[rng.permutation(N)])
mu=shf.mean(0); sd=shf.std(0)+1e-9
print(f"N tokens={N}")
print(f"{'dist':>13} {'observed':>9} {'shuffle':>9} {'o/s':>6} {'z':>8}")
for k,(lo,hi) in enumerate(bins):
    z=(obs[k]-mu[k])/sd[k]
    print(f"{f'{lo}-{hi}':>13} {int(obs[k]):>9} {mu[k]:>9.0f} {obs[k]/max(mu[k],1):>6.2f} {z:>8.1f}")
