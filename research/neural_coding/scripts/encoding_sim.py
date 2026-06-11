#!/usr/bin/env python3
"""Neural-coding FIRST STEP — encoding-model harness, validated on a simulation with a KNOWN
feature->response mapping (the neural analogue of our planted-cipher positive control).

Why simulation first: the genome program taught us never to interpret a result from an
un-validated instrument. Before downloading real fMRI/ECoG, we prove the encoding pipeline
(a) recovers a planted feature->response mapping above a phase-shuffled FLOOR, on HELD-OUT data,
normalized by a noise CEILING, and (b) shows the built-in POSITIVE CONTROL — a double
dissociation: low-level features predict the 'early' region, semantic features predict the
'association' region, and not vice versa. When that fires, the same harness is ready for real data.

CPU only. No real neural data yet — this is the validation rig.
"""
import os, sys, unicodedata, json
import numpy as np
from numpy.linalg import lstsq

HERE=os.path.dirname(os.path.abspath(__file__))
# a real language stream for realistic feature statistics (reuse the Gutenberg English corpus)
ENG=os.path.join(HERE,"..","..","two_books_genome","data","languages","english_moby_dick.txt")

def words(path, cap=4000):
    t=open(path,encoding="utf-8",errors="ignore").read().lower()
    t=unicodedata.normalize("NFD",t); t="".join(c for c in t if not unicodedata.combining(c))
    w=[x for x in ''.join(c if c.isalpha() else ' ' for c in t).split() if x]
    return w[:cap]

def z(x):
    x=np.asarray(x,float); s=x.std(); return (x-x.mean())/(s if s>1e-9 else 1)

def low_level_features(W):
    """interpretable, low-level: word length, vowel ratio, log-rank frequency."""
    from collections import Counter
    fr=Counter(W);
    length=z([len(w) for w in W])
    vowels=z([sum(c in "aeiou" for c in w)/max(len(w),1) for w in W])
    logfreq=z([np.log(fr[w]) for w in W])
    return np.column_stack([length,vowels,logfreq])           # (T,3)

def semantic_features(W, D=48, seed=0):
    """stand-in 'semantic' embedding: fixed random vector per word TYPE (deterministic).
    For the simulation positive control this is the ground-truth driver of the assoc region."""
    rng=np.random.default_rng(seed); types={w:i for i,w in enumerate(sorted(set(W)))}
    E=rng.standard_normal((len(types),D))
    return np.array([E[types[w]] for w in W])                  # (T,D)

def make_responses(F, n_vox, weight_seed, noise_sd, rng):
    """region responses = F @ W + temporally-smoothed noise; two repeats for a noise ceiling.
    Signal is standardized per voxel so noise_sd sets the SNR directly (comparable ceilings)."""
    Wt=np.random.default_rng(weight_seed).standard_normal((F.shape[1], n_vox))
    signal=F@Wt
    signal=(signal-signal.mean(0))/np.maximum(signal.std(0),1e-9)   # unit-variance signal per voxel
    def rep():
        e=rng.standard_normal(signal.shape)
        # mild temporal autocorrelation (AR1) to mimic measurement structure
        for t in range(1,len(e)): e[t]=0.4*e[t-1]+e[t]
        return signal + noise_sd*e
    return rep(), rep()

def ridge_cv(Xtr,Ytr,Xte,alphas=(1,10,100,1000)):
    best=None; bestpred=None
    n=len(Xtr); k=n//5
    for a in alphas:
        # simple holdout-within-train to pick alpha
        Xt,Yt,Xv,Yv=Xtr[:-k],Ytr[:-k],Xtr[-k:],Ytr[-k:]
        A=Xt.T@Xt + a*np.eye(Xt.shape[1]); B=Xt.T@Yt
        Wt=np.linalg.solve(A,B); r=_r2(Yv,Xv@Wt)
        if best is None or r>best: best=r; besta=a
    A=Xtr.T@Xtr + besta*np.eye(Xtr.shape[1]); Wt=np.linalg.solve(A,Xtr.T@Ytr)
    return Xte@Wt, besta

def _r2(Y,P):
    ss=((Y-P)**2).sum(0); tot=((Y-Y.mean(0))**2).sum(0)
    return float(np.mean(1-ss/np.maximum(tot,1e-9)))

def evaluate(F, Y1, Y2, shift=None):
    """held-out R2 (contiguous split), noise-ceiling-normalized. shift!=None => FLOOR."""
    if shift is not None: F=np.roll(F,shift,axis=0)
    T=len(F); cut=int(T*0.7)
    Y=(Y1+Y2)/2.0
    Xtr,Ytr,Xte,Yte=F[:cut],Y[:cut],F[cut:],Y[cut:]
    P,_=ridge_cv(Xtr,Ytr,Xte)
    r2=_r2(Yte,P)
    # noise ceiling on test block: predictivity of one repeat from the other
    ceil=_r2(Y2[cut:],Y1[cut:])
    return r2, ceil, (r2/ceil if ceil>0.05 else float('nan'))

def main():
    if not os.path.exists(ENG): raise SystemExit("English corpus not found at "+ENG)
    W=words(ENG, cap=4000)
    Flow=low_level_features(W); Fsem=semantic_features(W)
    rng=np.random.default_rng(1)
    # TRUE generative model: early region driven by LOW-LEVEL, assoc region by SEMANTIC
    early1,early2=make_responses(Flow, 8, weight_seed=11, noise_sd=0.8, rng=rng)
    assoc1,assoc2=make_responses(Fsem, 8, weight_seed=22, noise_sd=0.8, rng=rng)
    blocks={"early_region":(early1,early2),"assoc_region":(assoc1,assoc2)}
    feats={"low_level":Flow,"semantic":Fsem}
    res={}
    for rn,(Y1,Y2) in blocks.items():
        res[rn]={}
        for fn,F in feats.items():
            r2,ceil,norm=evaluate(F,Y1,Y2)
            fr2,_,fnorm=evaluate(F,Y1,Y2,shift=len(F)//2)   # phase/floor
            res[rn][fn]={"r2":round(r2,3),"ceiling":round(ceil,3),
                         "r2_over_ceiling":round(norm,3) if norm==norm else None,
                         "floor_r2":round(fr2,3)}
    print(json.dumps(res,indent=2))
    # double-dissociation positive control
    d_low = res["early_region"]["low_level"]["r2_over_ceiling"]
    d_lowA= res["assoc_region"]["low_level"]["r2_over_ceiling"]
    d_semA= res["assoc_region"]["semantic"]["r2_over_ceiling"]
    d_semE= res["early_region"]["semantic"]["r2_over_ceiling"]
    print("\nPOSITIVE CONTROL (double dissociation):")
    print(f"  low-level -> early {d_low} vs assoc {d_lowA}  (expect early >> assoc)")
    print(f"  semantic  -> assoc {d_semA} vs early {d_semE}  (expect assoc >> early)")
    g=lambda v: v if isinstance(v,(int,float)) else -1.0
    above_floor=all(res[r][f]["r2"]>res[r][f]["floor_r2"]+0.05
                    for r in blocks for f in feats if res[r][f]["r2"]>0.1)
    ok = (g(d_low)>g(d_lowA)) and (g(d_semA)>g(d_semE)) and above_floor
    print("INSTRUMENT FIRES (dissociation + above-floor):", ok)
    out={"results":res,"double_dissociation_ok":bool(ok)}
    json.dump(out,open(os.path.join(HERE,"encoding_sim_result.json"),"w"),indent=2)

if __name__=="__main__": main()
