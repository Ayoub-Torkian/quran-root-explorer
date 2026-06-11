"""TENSOR DECOMPOSITION value test. Does a 3-way tensor reveal structure a 2-way
matrix (SVD/NMF, which the app already has) cannot?
Tensor X[root, surah, position-bin].  Fit non-negative CP (multiplicative updates).
Decisive test: is the POSITION mode informative -- do components specialize by
position -- vs a NULL where position labels are shuffled? If real ~ shuffled,
the 3rd mode is degenerate and a tensor adds nothing over 2-way.
"""
from __future__ import annotations
import sys, time
import numpy as np
from collections import Counter
sys.path.insert(0,".")
import analysis as A
from analysis import COL_SURAH, COL_AYAH, normalize_letters
rng=np.random.default_rng(0); t0=time.time()
corpus=A.load_corpus("Book6.xlsx"); K=normalize_letters
su=corpus.df[COL_SURAH].astype(int).to_numpy()
order=np.lexsort((corpus.df[COL_AYAH].astype(int).to_numpy(),su)); su=su[order]
rt=[[K(t) for t in corpus.root_tokens[i]] for i in order]
freq=Counter(r for toks in rt for r in set(toks))
roots=[r for r,c in freq.items() if c>=8]; ri={r:i for i,r in enumerate(roots)}
sl=sorted(set(su.tolist())); si={s:i for i,s in enumerate(sl)}
NP=3
def build(shuffle_pos=False):
    X=np.zeros((len(roots),len(sl),NP))
    for k,toks in enumerate(rt):
        L=len(toks)
        if L==0: continue
        for j,t in enumerate(toks):
            r=K(t)
            if r not in ri: continue
            pb=int(NP*j/L) if not shuffle_pos else int(rng.integers(NP))
            pb=min(pb,NP-1)
            X[ri[r],si[int(su[k])],pb]+=1
    return X
def kr(Aa,Bb):
    r=Aa.shape[1]
    return (Aa[:,None,:]*Bb[None,:,:]).reshape(Aa.shape[0]*Bb.shape[0],r)
def ncp(X,r=5,it=50):
    I,J,Kd=X.shape
    U=[np.abs(rng.standard_normal((d,r)))+0.1 for d in (I,J,Kd)]
    X0=X.reshape(I,J*Kd); X1=X.transpose(1,0,2).reshape(J,I*Kd); X2=X.transpose(2,0,1).reshape(Kd,I*J)
    for _ in range(it):
        U[0]*= (X0@kr(U[1],U[2]))/(U[0]@(kr(U[1],U[2]).T@kr(U[1],U[2]))+1e-9)
        U[1]*= (X1@kr(U[0],U[2]))/(U[1]@(kr(U[0],U[2]).T@kr(U[0],U[2]))+1e-9)
        U[2]*= (X2@kr(U[0],U[1]))/(U[2]@(kr(U[0],U[1]).T@kr(U[0],U[1]))+1e-9)
    # reconstruction
    Xhat=(U[0]@kr(U[1],U[2]).T).reshape(I,J,Kd)
    ev=1-np.sum((X-Xhat)**2)/np.sum(X**2)
    return U,ev
def posinfo(U2):  # how far each component's position profile is from uniform
    C=U2/ (U2.sum(0,keepdims=True)+1e-9)
    return float(np.mean(np.abs(C-1.0/U2.shape[0])))

X=build(False)
U,ev=ncp(X,5,50); real=posinfo(U[2])
# null: shuffle position labels
nl=[]
for _ in range(5):
    Xs=build(True); Us,_=ncp(Xs,5,50); nl.append(posinfo(Us[2]))
nl=np.array(nl)
print(f"[{time.time()-t0:.1f}s] tensor {X.shape} nnz={np.count_nonzero(X)}")
print(f"  rank-5 NTF reconstruction explained var = {ev:.3f}")
print(f"  position-mode non-uniformity: real={real:.4f}  shuffled={nl.mean():.4f}+/-{nl.std():.4f}")
z=(real-nl.mean())/(nl.std()+1e-9)
print(f"  z = {z:+.1f}  -> {'genuine 3-way position structure (tensor adds info)' if z>3 else 'position mode ~ degenerate (tensor adds little over 2-way)'}")
# also raw: does position carry root info at all? I(pos;root) on the margin
M=X.sum(1)  # root x pos
P=M/M.sum(); pr=P.sum(1); pp=P.sum(0); nz=P>0
mi=float(np.sum(P[nz]*np.log2(P[nz]/np.outer(pr,pp)[nz])))
print(f"  marginal I(position;root) = {mi:.4f} bits (small => position weakly tied to identity)")
print(f"\n[total {time.time()-t0:.1f}s]")
