"""IDEAS SWEEP batch 1/2 — each idea run on real data with a null. Facts only."""
from __future__ import annotations
import sys, time
import numpy as np
sys.path.insert(0,".")
import analysis as A
from analysis import COL_SURAH, COL_AYAH, normalize_letters
rng=np.random.default_rng(0); t0=time.time()
corpus=A.load_corpus("Book6.xlsx")
su=corpus.df[COL_SURAH].astype(int).to_numpy()
ay=corpus.df[COL_AYAH].astype(int).to_numpy()
order=np.lexsort((ay,su)); su=su[order]
# per-ayah letter string + length, ayah-final letter
vlen=np.zeros(len(order)); finals=[]
seg=[corpus.seg_tokens[i] for i in order]
for k,i in enumerate(order):
    s="".join(normalize_letters(t) for t in corpus.seg_tokens[i])
    s="".join(ch for ch in s if ch.strip())
    vlen[k]=len(s); finals.append(s[-1] if s else "")
def dfa(x):
    x=x-x.mean(); y=np.cumsum(x)
    sc=np.unique(np.logspace(np.log10(16),np.log10(len(x)//8),16).astype(int)); F=[]
    for s in sc:
        ns=len(y)//s
        if ns<1: continue
        g=y[:ns*s].reshape(ns,s); t=np.arange(s)
        F.append(np.mean([np.sqrt(np.mean((r-np.polyval(np.polyfit(t,r,1),t))**2)) for r in g]))
    F=np.array(F); sc=sc[:len(F)]
    return float(np.polyfit(np.log(sc),np.log(F),1)[0])

print(f"[{time.time()-t0:.1f}s] ayahs={len(order)}")
res={}

# IDEA 1: verse-length long-range memory (DFA) vs shuffled
a_real=dfa(vlen); sh=[dfa(rng.permutation(vlen)) for _ in range(30)]
z=(a_real-np.mean(sh))/(np.std(sh)+1e-9)
res["1 verse-length DFA (long memory)"]=(f"alpha={a_real:.3f} shuffled={np.mean(sh):.3f}", f"z={z:.1f}")

# IDEA 2: verse-length autocorrelation lag-1 vs shuffle
v=vlen-vlen.mean(); den=np.dot(v,v)
ac1=np.dot(v[:-1],v[1:])/den
nl=[]
for _ in range(1000):
    q=rng.permutation(vlen); q=q-q.mean(); nl.append(np.dot(q[:-1],q[1:])/np.dot(q,q))
p=(np.sum(np.array(nl)>=ac1)+1)/1001
res["2 verse-length autocorr lag-1"]=(f"ac1={ac1:.3f}", f"p={p:.4g}")

# IDEA 3: verse-length 1/f spectral slope vs shuffle
def slope(x):
    x=x-x.mean(); P=np.abs(np.fft.rfft(x))**2; f=np.arange(1,len(P))
    return float(np.polyfit(np.log(f),np.log(P[1:]+1e-12),1)[0])
s_real=slope(vlen); s_sh=np.mean([slope(rng.permutation(vlen)) for _ in range(30)])
res["3 verse-length spectral slope (1/f^b)"]=(f"slope={s_real:.3f} shuffled={s_sh:.3f}", "b>0 => long-range")

# IDEA 4: rhyme/fawasil — per-surah ayah-final-letter entropy vs shuffle (lower=rhyme)
fin=np.array(finals)
def mean_final_entropy(labels):
    tot=0; n=0
    for s in np.unique(su):
        ff=labels[su==s]
        if len(ff)<3: continue
        _,c=np.unique(ff,return_counts=True); p=c/c.sum()
        tot+=-(p*np.log2(p)).sum(); n+=1
    return tot/n
H_real=mean_final_entropy(fin)
nl=[mean_final_entropy(rng.permutation(fin)) for _ in range(300)]
p=(np.sum(np.array(nl)<=H_real)+1)/301
res["4 rhyme: ayah-final-letter entropy"]=(f"H={H_real:.3f} shuffled={np.mean(nl):.3f}", f"p={p:.4g} (lower=rhyme)")

# IDEA 5: root burstiness vs Poisson (CV of inter-occurrence gaps)
from collections import Counter
K=normalize_letters
rt=[ [K(t) for t in corpus.root_tokens[i]] for i in order]
pos=Counter(); occ={}
for k,toks in enumerate(rt):
    for r in set(toks):
        occ.setdefault(r,[]).append(k)
cvs=[]
for r,ks in occ.items():
    if len(ks)>=20:
        g=np.diff(ks); cv=g.std()/ (g.mean()+1e-9); cvs.append(cv)
cvs=np.array(cvs)
res["5 root burstiness (CV gaps, Poisson=1)"]=(f"median CV={np.median(cvs):.2f} frac>1.2={np.mean(cvs>1.2):.2f}", f"n_roots={len(cvs)}")

print(f"\n{'idea':<44}{'result':<40}{'null/effect'}")
print("-"*104)
for k,(a,b) in res.items():
    print(f"{k:<44}{a:<40}{b}")
print(f"\n[total {time.time()-t0:.1f}s]")
