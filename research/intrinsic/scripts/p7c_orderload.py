#!/usr/bin/env python3
# C4 honest measure — ORDER-LOAD (not frequency-fooled): bigram prequential bits/token in
# TRUE order vs the channel's own SHUFFLE, in 3 rasm channels. Margin = bits/token of
# collocational order structure. Averaged over several shuffles for a floor + spread.
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
wlen=[str(min(len(w),12)) for w in words]
def enc(seq):
    V={};out=[]
    for x in seq:
        if x not in V: V[x]=len(V)
        out.append(V[x])
    return np.array(out),len(V)
def bits(seq):
    s,A=seq; M=len(s); uni=np.zeros(A); big=defaultdict(lambda: defaultdict(float)); b=0.0
    for i in range(M):
        c=s[i]
        if i==0: p=(uni[c]+0.1)/(uni.sum()+0.1*A)
        else:
            d=big[s[i-1]]; ds=sum(d.values()); pb=(d.get(c,0)+0.1)/(ds+0.1*A); pu=(uni[c]+0.1)/(uni.sum()+0.1*A)
            lam=ds/(ds+5.0); p=lam*pb+(1-lam)*pu
        b+=-np.log2(p); uni[c]+=1
        if i>0: big[s[i-1]][c]+=1
    return b/M
rng=np.random.default_rng(0)
def report(seq,name):
    s,A=enc(seq); M=len(s); real=bits((s,A))
    sh=[bits((s[rng.permutation(M)],A)) for _ in range(3)]; shm=np.mean(sh)
    print(f"  {name:22s} true={real:.3f} b/tok  shuffle={shm:.3f}±{np.std(sh):.3f}  ORDER-LOAD={shm-real:.3f} b/tok  ({(shm-real)*M:,.0f} bits)")
    return shm-real
print("C4 honest — root/word/length ORDER-LOAD (bigram bits/token saved over own shuffle):")
m=[report(roots,"root collocation"),report(words,"surface-word collocation"),report(wlen,"word-length collocation")]
print(f"\n  channels with positive order-load: {sum(x>0.02 for x in m)}/3")
