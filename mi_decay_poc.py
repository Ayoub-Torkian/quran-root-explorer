"""Sequence/semantic-scale latent-feature PoC: mutual information vs distance.

Lin & Tegmark (2017): in critical/natural systems (DNA, natural language, music)
the mutual information between two symbols separated by distance d decays as a
POWER LAW  I(d) ~ d^(-alpha).  Markov/random sources decay EXPONENTIALLY and a
shuffled stream has I(d)=0.  Power-law long-range order is the statistical
signature that links a symbolic stream to physical systems near criticality.

We compute a SHUFFLE-BIAS-CORRECTED estimate:
    I_excess(d) = I_hat(d, real) - mean_k I_hat(d, shuffled_k)
so the finite-sample MI bias (large for big alphabets) is subtracted out.
Run at the CHARACTER (sequence) scale and the ROOT (semantic) scale.
"""
from __future__ import annotations
import sys, time
import numpy as np
from collections import Counter

sys.path.insert(0, ".")
import analysis as A
from analysis import COL_SURAH, COL_AYAH, normalize_letters

t0 = time.time()
corpus = A.load_corpus("Book6.xlsx")
df = corpus.df
order = np.lexsort((df[COL_AYAH].astype(int).to_numpy(),
                    df[COL_SURAH].astype(int).to_numpy()))  # canonical reading order

# ---- build the two streams in reading order ----
letters = []
roots = []
for i in order:
    for t in corpus.seg_tokens[i]:
        nt = normalize_letters(t)
        for ch in nt:
            if ch.strip():
                letters.append(ch)
    roots.extend(corpus.root_tokens[i])

def encode(seq):
    vocab = {s: k for k, s in enumerate(sorted(set(seq)))}
    return np.array([vocab[s] for s in seq], dtype=np.int32), len(vocab)

L, nL = encode(letters)
R, nR = encode(roots)
print(f"[load {time.time()-t0:.1f}s] letters: N={L.size} alphabet={nL} | "
      f"roots: N={R.size} alphabet={nR}")

def mi_hat(arr, d, K):
    """Plug-in MI (bits) between arr[i] and arr[i+d]."""
    x = arr[:-d]; y = arr[d:]
    n = x.size
    joint = np.bincount(x.astype(np.int64) * K + y, minlength=K * K).astype(np.float64)
    joint /= n
    pj = joint.reshape(K, K)
    px = pj.sum(1); py = pj.sum(0)
    nz = pj > 0
    outer = np.outer(px, py)
    return float(np.sum(pj[nz] * np.log2(pj[nz] / outer[nz])))

def mi_curve(arr, K, ds, nshuf=4, rng=None):
    rng = rng or np.random.default_rng(0)
    real = np.array([mi_hat(arr, d, K) for d in ds])
    # bias floor: shuffle the whole stream -> true MI 0, measured = finite-size bias
    bias = np.zeros(len(ds))
    for _ in range(nshuf):
        sh = arr.copy(); rng.shuffle(sh)
        bias += np.array([mi_hat(sh, d, K) for d in ds])
    bias /= nshuf
    return real, bias, real - bias

def fit_loglog(ds, y):
    m = y > 0
    if m.sum() < 4:
        return float("nan"), float("nan")
    lx = np.log(np.asarray(ds)[m]); ly = np.log(y[m])
    a, b = np.polyfit(lx, ly, 1)
    pred = a * lx + b
    ss = 1 - np.sum((ly - pred) ** 2) / np.sum((ly - ly.mean()) ** 2)
    return -a, ss  # power-law exponent alpha (I ~ d^-alpha), R^2

# character scale: dense, push to long range
dsL = [1,2,3,4,5,6,8,10,13,16,20,25,32,40,50,64,80,100,128,160,200]
rL, bL, eL = mi_curve(L, nL, dsL)
aL, r2L = fit_loglog(dsL, eL)

# root scale: sparser/large alphabet, shorter range, more shuffles for bias
dsR = [1,2,3,4,5,6,8,10,13,16,20,25,32,40,50]
rR, bR, eR = mi_curve(R, nR, dsR, nshuf=6)
aR, r2R = fit_loglog(dsR, eR)

print(f"\n[done {time.time()-t0:.1f}s]")
print("\n=== CHARACTER (sequence) scale ===")
print(f"  I_excess(d=1)={eL[0]:.4f}  I_excess(d=10)={eL[dsL.index(10)]:.4f}  "
      f"I_excess(d=100)={eL[dsL.index(100)]:.5f}  I_excess(d=200)={eL[-1]:.5f}")
print(f"  shuffle bias floor at d=1: {bL[0]:.5f} bits (real {rL[0]:.4f})")
print(f"  power-law fit: alpha={aL:.3f}  R^2(log-log)={r2L:.3f}")
print("\n=== ROOT (semantic) scale ===")
print(f"  I_excess(d=1)={eR[0]:.4f}  I_excess(d=5)={eR[dsR.index(5)]:.4f}  "
      f"I_excess(d=50)={eR[-1]:.5f}")
print(f"  shuffle bias floor at d=1: {bR[0]:.4f} bits (real {rR[0]:.4f})")
print(f"  power-law fit: alpha={aR:.3f}  R^2(log-log)={r2R:.3f}")

# exponential-vs-powerlaw discrimination on character scale (semilog R^2)
def fit_semilog(ds, y):
    m = y > 0
    lx = np.asarray(ds)[m]; ly = np.log(y[m])
    a, b = np.polyfit(lx, ly, 1)
    pred = a * lx + b
    return 1 - np.sum((ly - pred) ** 2) / np.sum((ly - ly.mean()) ** 2)
print("\n=== model discrimination (character scale) ===")
print(f"  power-law R^2={r2L:.3f}  vs  exponential R^2={fit_semilog(dsL, eL):.3f}")
print("  (higher R^2 = better description of the decay)")

import json
json.dump({"char":{"ds":dsL,"excess":eL.tolist(),"alpha":aL,"r2":r2L},
           "root":{"ds":dsR,"excess":eR.tolist(),"alpha":aR,"r2":r2R}},
          open("/sessions/epic-inspiring-gates/mnt/outputs/mi_decay_result.json","w"))
print("\nsaved mi_decay_result.json")
