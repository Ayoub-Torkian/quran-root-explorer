#!/usr/bin/env python3
# P5 — per-WORD necessity (finest scale, rasm only). For each word: is it more predictable
# in its TRUE place than at random spots, under a LOCAL window model in 3 rasm channels —
# final letter, first letter, word length (letters)? vs shuffled-order floor. Completes the
# nothing-moved ladder: corpus(L14) -> sūra(L12) -> verse(L20) -> WORD.
import glob,unicodedata,numpy as np
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'
def skel(t):
    t=unicodedata.normalize('NFD',t);t=''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
W=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    _,tx=ln.split('\t',1); W+=skel(tx)
M=len(W)
fl=[w[-1] for w in W]; il=[w[0] for w in W]; ln_=np.array([len(w) for w in W])
fa=sorted(set(fl)); fid={c:i for i,c in enumerate(fa)}; FL=np.array([fid[c] for c in fl]); A=len(fa)
ia=sorted(set(il)); iid={c:i for i,c in enumerate(ia)}; IL=np.array([iid[c] for c in il]); Ai=len(ia)
lb=np.clip(ln_,1,9)-1; B=9
WIN=15; AL=0.5
def surp(wid,pos,order):
    lo=max(0,pos-WIN);hi=min(M,pos+WIN+1); idx=[order[k] for k in range(lo,hi) if k!=pos]
    if not idx: return 0,0,0
    fc=np.bincount(FL[idx],minlength=A)+AL; ic=np.bincount(IL[idx],minlength=Ai)+AL; lc=np.bincount(lb[idx],minlength=B)+AL
    return (-np.log2(fc[FL[wid]]/fc.sum()), -np.log2(ic[IL[wid]]/ic.sum()), -np.log2(lc[lb[wid]]/lc.sum()))
rng=np.random.default_rng(0)
def run(order,label,sample=6000,nr=15):
    pos=np.empty(M,int);pos[order]=np.arange(M)
    wins=rng.choice(M,sample,replace=False); acc=np.zeros((sample,3))
    for t,wid in enumerate(wins):
        si=surp(wid,pos[wid],order); rs=np.array([surp(wid,int(r),order) for r in rng.integers(0,M,nr)])
        for c in range(3): acc[t,c]=np.mean(si[c]<rs[:,c])
    print(f"  {label:20s} final-letter={acc[:,0].mean()*100:.1f}%  first-letter={acc[:,1].mean()*100:.1f}%  length={acc[:,2].mean()*100:.1f}%  mean={acc.mean()*100:.1f}%")
    return acc
print(f"M={M} words · window ±{WIN} · 3 rasm channels · % of words more predictable IN PLACE than a random spot")
run(np.arange(M),"true order")
run(rng.permutation(M),"shuffled (floor)")
