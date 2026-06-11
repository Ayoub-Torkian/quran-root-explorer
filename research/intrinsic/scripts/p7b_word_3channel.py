#!/usr/bin/env python3
# C4 promotion — word-order necessity in 3 INDEPENDENT rasm channels. Per-token: is each
# token more predictable from its TRUE preceding token than from a random one? (bigram +
# unigram backoff, full-data). Channels: (1) ROOT collocation, (2) SURFACE-word collocation
# (incl. particles/syntax), (3) word-LENGTH collocation. vs shuffled-stream floor.
import glob,unicodedata,numpy as np
from collections import defaultdict
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'
def skel(t):
    t=unicodedata.normalize('NFD',t);t=''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
words=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' in ln: words+=skel(ln.split('\t',1)[1])
roots=[r for r in open(R+'/research/two_books_genome/roots_seq.txt',encoding='utf-8').read().split() if r!='NA']
wlen=[min(len(w),9) for w in words]
def encode(seq):
    V=sorted(set(seq)); d={x:i for i,x in enumerate(V)}; return np.array([d[x] for x in seq]),len(V)
rng=np.random.default_rng(0)
def necessity(seq,name,sample=8000):
    s,A=encode(seq); M=len(s)
    uni=np.bincount(s,minlength=A).astype(float); big=defaultdict(lambda: defaultdict(float))
    for i in range(1,M): big[s[i-1]][s[i]]+=1
    def surp(tok,prev):
        b=big[prev]; bs=sum(b.values()); pb=(b.get(tok,0)+0.1)/(bs+0.1*A); pu=(uni[tok]+0.1)/(uni.sum()+0.1*A)
        lam=bs/(bs+5.0); return -np.log2(lam*pb+(1-lam)*pu)
    idx=rng.choice(np.arange(1,M),min(sample,M-1),replace=False); nr=15; acc=0
    for i in idx:
        si=surp(s[i],s[i-1]); rp=rng.integers(1,M,nr)
        acc+=np.mean([si<surp(s[i],s[r-1]) for r in rp])
    # shuffle floor
    sh=s[rng.permutation(M)]; bigs=defaultdict(lambda: defaultdict(float))
    for i in range(1,M): bigs[sh[i-1]][sh[i]]+=1
    def surps(tok,prev):
        b=bigs[prev]; bs=sum(b.values()); pb=(b.get(tok,0)+0.1)/(bs+0.1*A); pu=(uni[tok]+0.1)/(uni.sum()+0.1*A)
        lam=bs/(bs+5.0); return -np.log2(lam*pb+(1-lam)*pu)
    accs=0
    for i in idx[:3000]:
        si=surps(sh[i],sh[i-1]); rp=rng.integers(1,M,nr); accs+=np.mean([si<surps(sh[i],sh[r-1]) for r in rp])
    print(f"  {name:22s} in-place predictable: {acc/len(idx)*100:.1f}%   shuffle floor: {accs/min(3000,len(idx))*100:.1f}%")
print("C4 — word-order necessity, 3 rasm channels (% token more predictable from TRUE preceding token):")
necessity(roots,"root collocation")
necessity(words,"surface-word collocation")
necessity([str(x) for x in wlen],"word-length collocation")
