import unicodedata, numpy as np
from collections import Counter
def skel(t):
    t=unicodedata.normalize('NFD',t); t=''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
V=[]  # list of token-lists per verse
for ln in open('/sessions/gifted-tender-cori/mnt/Quran_Root_Explorer_Web_v1.2/research/two_books_genome/data/quran/quran_arabic_verses.tsv',encoding='utf-8'):
    if '\t' in ln: V.append(skel(ln.split('\t',1)[1]))
ALL=[w for v in V for w in v]; uni=Counter(ALL); words=list(uni); wp=np.array([uni[w] for w in words],float); wp/=wp.sum()
stop=set(w for w,_ in uni.most_common(40))
rng=np.random.default_rng(0)
def finals(verses): return [v[-1][-1] if v and v[-1] else '' for v in verses]
def vlen(verses): return np.array([len(v) for v in verses],float)
def dfa(x):
    x=x-x.mean(); y=np.cumsum(x); N=len(y)
    sc=np.unique(np.floor(np.logspace(np.log10(8),np.log10(N//4),12)).astype(int)); F=[]
    for n in sc:
        ns=N//n
        if ns<2: continue
        r=[]
        for s in range(ns):
            seg=y[s*n:(s+1)*n]; t=np.arange(n); c=np.polyfit(t,seg,1); r.append(np.sqrt(np.mean((seg-np.polyval(c,t))**2)))
        F.append((n,np.mean(r)))
    F=np.array(F); return np.polyfit(np.log(F[:,0]),np.log(F[:,1]),1)[0]
def slope(x):
    x=x-x.mean(); f=np.fft.rfftfreq(len(x)); P=np.abs(np.fft.rfft(x))**2; m=(f>0)&(f<0.1)
    return -np.polyfit(np.log(f[m]),np.log(P[m]),1)[0]
def rhyme_adj(verses):
    fz=finals(verses); return np.mean([fz[i]==fz[i+1] for i in range(len(fz)-1)])
def netrec(verses):
    toks=[w for v in verses for w in v if w not in stop]; seen={}; hit=0
    for i,w in enumerate(toks):
        if w in seen and i-seen[w]<=32: hit+=1
        seen[w]=i
    return hit/max(len(toks),1)
def metrics(verses):
    return dict(H=dfa(vlen(verses)), pink=slope(vlen(verses)), rhyme=rhyme_adj(verses), net=netrec(verses))
def MOVE_global(verses): return list(rng.permutation(np.array(verses,dtype=object)))
def MOVE_local(verses,f=0.2):
    v=verses[:]; idx=rng.choice(len(v)-1,int(f*len(v)),replace=False)
    for i in idx: v[i],v[i+1]=v[i+1],v[i]
    return v
def DELETE(verses,f=0.10):
    keep=rng.random(len(verses))>f; return [v for v,k in zip(verses,keep) if k]
def ADD(verses,f=0.10):
    v=verses[:]; 
    for _ in range(int(f*len(verses))):
        j=rng.integers(len(v)); v.insert(rng.integers(len(v)+1), v[j])
    return v
def REPLACE(verses,f=0.20):
    out=[]
    for v in verses:
        nv=[ (words[rng.choice(len(words),p=wp)] if rng.random()<f else w) for w in v ]
        out.append(nv)
    return out
base=metrics(V)
conds={'MOVE-global':MOVE_global(V),'MOVE-local20%':MOVE_local(V),'DELETE10%':DELETE(V),'ADD10%':ADD(V),'REPLACE20%':REPLACE(V)}
print(f"{'condition':>14} {'DFA_H':>7} {'1/f':>6} {'rhyme':>7} {'net':>7}")
print(f"{'TRUE':>14} {base['H']:>7.3f} {base['pink']:>6.2f} {base['rhyme']:>7.3f} {base['net']:>7.3f}")
for name,vv in conds.items():
    m=metrics(vv)
    print(f"{name:>14} {m['H']:>7.3f} {m['pink']:>6.2f} {m['rhyme']:>7.3f} {m['net']:>7.3f}")
