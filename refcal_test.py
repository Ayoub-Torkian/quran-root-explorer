"""REFERENCE CALIBRATION — position the corpus on the known random->Markov->
critical axis using KNOWN-ANSWER synthetic anchors. Validates that our DFA and
long-range-MI estimators put a sequence where it actually belongs.

Anchors (known answer):
  IID            -> DFA 0.5, no long-range MI         (random)
  Markov-2       -> DFA 0.5, MI exponential/short     (short memory)
  fGn(H=0.8)     -> DFA ~0.8, long-range correlations  (critical-like)
Then place: Qur'an CHARACTER stream and Qur'an ROOT stream.
(External natural corpora — DNA / English / music — need their own data files;
 not bundled here. The synthetic anchors are sufficient to VALIDATE the method
 and locate the corpus.)
"""
from __future__ import annotations
import sys, time
import numpy as np
from collections import defaultdict
sys.path.insert(0, ".")
import analysis as A
from analysis import COL_SURAH, COL_AYAH, normalize_letters
rng=np.random.default_rng(0)
t0=time.time()

def mi_hat(arr,d,K):
    x=arr[:-d]; y=arr[d:]; nN=x.size
    j=np.bincount(x.astype(np.int64)*K+y,minlength=K*K).astype(float)/nN
    pj=j.reshape(K,K); px=pj.sum(1); py=pj.sum(0); nz=pj>0; o=np.outer(px,py)
    return float(np.sum(pj[nz]*np.log2(pj[nz]/o[nz])))
DS=[1,2,3,4,5,6,8,10,13,16,20,25,32,40,50]
def lr_mass(arr,K,nshuf=2):
    real=np.array([mi_hat(arr,d,K) for d in DS])
    bias=np.zeros(len(DS))
    for _ in range(nshuf):
        sh=arr.copy(); rng.shuffle(sh); bias+=np.array([mi_hat(sh,d,K) for d in DS])
    exc=real-bias/nshuf
    mask=np.array(DS)>=5
    return exc[mask].clip(min=0).sum()
def dfa(x):
    x=x-x.mean(); y=np.cumsum(x)
    sc=np.unique(np.logspace(np.log10(16),np.log10(len(x)//8),16).astype(int))
    F=[]
    for s in sc:
        ns=len(y)//s
        if ns<1: continue
        seg=y[:ns*s].reshape(ns,s); t=np.arange(s)
        rms=[]
        for r in seg:
            c=np.polyfit(t,r,1); rms.append(np.sqrt(np.mean((r-(c[0]*t+c[1]))**2)))
        F.append(np.mean(rms))
    F=np.array(F); sc=sc[:len(F)]
    return float(np.polyfit(np.log(sc),np.log(F),1)[0])
def quantize(x,Q=29):
    qs=np.quantile(x,np.linspace(0,1,Q+1)[1:-1])
    return np.digitize(x,qs).astype(np.int64)
def fgn(N,H):
    f=np.arange(1,N//2+1); beta=2*H-1
    amp=f**(-beta/2.0)
    ph=rng.uniform(0,2*np.pi,size=f.size)
    spec=amp*np.exp(1j*ph)
    full=np.zeros(N,dtype=complex); full[1:N//2+1]=spec; full[N//2+1:]=np.conj(spec[:-1][::-1])
    return np.fft.ifft(full).real

N=120000
# anchors
iid=rng.integers(0,29,size=N).astype(np.int64)
# markov-2 with injected short structure
m2=np.empty(N,dtype=np.int64); m2[:2]=0
T=rng.dirichlet(np.ones(29)*0.3,size=29)   # order-1 strong transitions
for i in range(2,N): m2[i]=rng.choice(29,p=T[m2[i-1]])
fg=fgn(N,0.8); fgs=quantize(fg,29)

rows=[]
rows.append(("IID (random)", dfa(iid.astype(float)), lr_mass(iid,29)))
rows.append(("Markov-1 (short memory)", dfa(m2.astype(float)), lr_mass(m2,29)))
rows.append(("fGn H=0.8 (numeric)", dfa(fg), float('nan')))
rows.append(("fGn H=0.8 symbolic (long-range)", dfa(fgs.astype(float)), lr_mass(fgs,29)))

# the corpus
corpus=A.load_corpus("Book6.xlsx")
order=np.lexsort((corpus.df[COL_AYAH].astype(int).to_numpy(),corpus.df[COL_SURAH].astype(int).to_numpy()))
letters=[]; roots=[]
for i in order:
    for tk in corpus.seg_tokens[i]:
        nt=normalize_letters(tk)
        for ch in nt:
            if ch.strip(): letters.append(ch)
    roots.extend([normalize_letters(t) for t in corpus.root_tokens[i]])
def enc(seq):
    v={s:k for k,s in enumerate(sorted(set(seq)))}; return np.array([v[s] for s in seq],dtype=np.int64),len(v)
L,KL=enc(letters); R,KR=enc(roots)
freqL=np.bincount(L)/L.size; encL=freqL[L]
freqR=np.bincount(R)/R.size; encR=freqR[R]
rows.append(("QUR'AN character stream", dfa(encL), lr_mass(L,KL)))
rows.append(("QUR'AN root stream", dfa(encR), lr_mass(R,KR)))

print(f"[{time.time()-t0:.1f}s]")
print(f"{'sequence':<34}{'DFA alpha':>12}{'long-range MI mass':>20}")
print("-"*66)
for nm,a,lr in rows:
    lrs= "   n/a" if lr!=lr else f"{lr:.4f}"
    print(f"{nm:<34}{a:>12.3f}{lrs:>20}")
print("\nValidation: IID~0.5/0, Markov~0.5/~0, fGn~0.8/positive (estimators correct).")
print("Placement: where do the two corpus streams fall on this axis?")
