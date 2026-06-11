"""Head-to-head: does the SEQUENCE (letter) or SEMANTIC (root) scale hold more
GENUINE latent structure to discover? Fair, normalized, beyond-own-baseline.

Discovery potential != raw MI. It is structure BEYOND what a low-order model of
that same stream already explains, normalized by the stream's own entropy so the
two alphabets are comparable.
"""
from __future__ import annotations
import sys, time, gzip
import numpy as np
from collections import Counter, defaultdict
sys.path.insert(0, ".")
import analysis as A
from analysis import COL_SURAH, COL_AYAH, normalize_letters

t0=time.time()
corpus=A.load_corpus("Book6.xlsx")
df=corpus.df
order=np.lexsort((df[COL_AYAH].astype(int).to_numpy(), df[COL_SURAH].astype(int).to_numpy()))
letters=[]; roots=[]
for i in order:
    for tk in corpus.seg_tokens[i]:
        nt=normalize_letters(tk)
        for ch in nt:
            if ch.strip(): letters.append(ch)
    roots.extend(corpus.root_tokens[i])
def enc(seq):
    v={s:k for k,s in enumerate(sorted(set(seq)))}
    return np.array([v[s] for s in seq],dtype=np.int64), len(v)
L,KL=enc(letters); R,KR=enc(roots)
rng=np.random.default_rng(0)

def H1(arr,K):
    p=np.bincount(arr,minlength=K).astype(float); p=p/p.sum(); p=p[p>0]
    return float(-(p*np.log2(p)).sum())
def mi_hat(arr,d,K):
    x=arr[:-d]; y=arr[d:]; n=x.size
    j=np.bincount(x*K+y,minlength=K*K).astype(float)/n
    pj=j.reshape(K,K); px=pj.sum(1); py=pj.sum(0); nz=pj>0; o=np.outer(px,py)
    return float(np.sum(pj[nz]*np.log2(pj[nz]/o[nz])))
def mi_exc(arr,K,ds,nshuf=2):
    real=np.array([mi_hat(arr,d,K) for d in ds]); bias=np.zeros(len(ds))
    for _ in range(nshuf):
        sh=arr.copy(); rng.shuffle(sh); bias+=np.array([mi_hat(sh,d,K) for d in ds])
    return real-bias/nshuf
def markov(arr,K,o):
    if o==0:
        p=np.bincount(arr,minlength=K)/arr.size; return rng.choice(K,size=arr.size,p=p)
    ctx=defaultdict(lambda: np.zeros(K))
    for i in range(o,arr.size): ctx[tuple(arr[i-o:i])][arr[i]]+=1
    pr={c:v/v.sum() for c,v in ctx.items()}
    bo=np.bincount(arr,minlength=K)/arr.size
    out=np.empty(arr.size,dtype=np.int64); out[:o]=arr[:o]
    for i in range(o,arr.size):
        out[i]=rng.choice(K,p=pr.get(tuple(out[i-o:i]),bo))
    return out

ds=[1,2,3,4,5,6,8,10,13,16,20,25,32,40,50]
def report(name,arr,K,max_order):
    h1=H1(arr,K)
    real=mi_exc(arr,K,ds)
    # highest estimable order: contexts must be << tokens
    est=max(o for o in range(0,max_order+1) if K**o < arr.size/20)
    sur=mi_exc(markov(arr,K,est),K,ds)
    mask=np.array(ds)>=5
    lr_real=real[mask].clip(min=0).sum(); lr_sur=sur[mask].clip(min=0).sum()
    near=real[:4].clip(min=0).sum()
    # effective memory: largest d whose excess>0.2% of H1
    thr=0.002*h1; mem=max([d for d,v in zip(ds,real) if v>thr] or [0])
    return dict(name=name,K=K,N=arr.size,H1=h1,est_order=est,
                near_norm=near/h1, lr_norm=lr_real/h1,
                beyond_ratio=lr_real/max(lr_sur,1e-9), mem=mem)

rl=report("SEQUENCE (letters)",L,KL,3)
rr=report("SEMANTIC (roots)",R,KR,3)

# compression redundancy both scales (vs shuffled), byte-encoded
def redun(arr):
    b=arr.astype(np.int16).tobytes(); sh=arr.copy(); rng.shuffle(sh); bs=sh.astype(np.int16).tobytes()
    rr=len(gzip.compress(b,9))/len(b); rs=len(gzip.compress(bs,9))/len(bs)
    return (rs-rr)/rs*100
redL=redun(L); redR=redun(R)

print(f"[{time.time()-t0:.1f}s]")
hdr=f"{'metric':<34}{'SEQUENCE/letters':>20}{'SEMANTIC/roots':>20}"
print(hdr); print("-"*len(hdr))
def row(lbl,a,b,f="{:.4f}"):
    print(f"{lbl:<34}{f.format(a):>20}{f.format(b):>20}")
row("alphabet K",rl['K'],rr['K'],"{:d}")
row("stream length N",rl['N'],rr['N'],"{:d}")
row("marginal entropy H1 (bits)",rl['H1'],rr['H1'])
row("highest estimable Markov order",rl['est_order'],rr['est_order'],"{:d}")
row("near MI / H1  (d=1..4)",rl['near_norm'],rr['near_norm'])
row("long-range MI / H1  (d>=5)",rl['lr_norm'],rr['lr_norm'])
row("BEYOND own-Markov ratio (d>=5)",rl['beyond_ratio'],rr['beyond_ratio'],"{:.2f}")
row("effective memory length (symbols)",rl['mem'],rr['mem'],"{:d}")
row("compression redundancy %",redL,redR,"{:.1f}")
