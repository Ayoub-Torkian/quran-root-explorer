"""De-risking battery for the Sequence-Scale plan. Tests the methods BEFORE we
build, on the real letter stream, with known-answer controls.

Pillars tested:
 (A) estimator validation: IID and Markov-2 synthetic -> method must NOT
     manufacture power-law/long-range structure from them.
 (B) THE decisive test: is real structure BEYOND low-order Markov? Compare real
     MI(d) to Markov-1/2/3 surrogates of the SAME stream.
 (C) feasibility of the other Phase-1 signatures on real data:
     block-entropy rate, DFA long-range exponent, compression redundancy.
"""
from __future__ import annotations
import sys, time, gzip, math
import numpy as np
from collections import Counter, defaultdict

sys.path.insert(0, ".")
import analysis as A
from analysis import COL_SURAH, COL_AYAH, normalize_letters

t0 = time.time()
corpus = A.load_corpus("Book6.xlsx")
df = corpus.df
order = np.lexsort((df[COL_AYAH].astype(int).to_numpy(),
                    df[COL_SURAH].astype(int).to_numpy()))
letters = []
for i in order:
    for t in corpus.seg_tokens[i]:
        nt = normalize_letters(t)
        for ch in nt:
            if ch.strip():
                letters.append(ch)
vocab = {s: k for k, s in enumerate(sorted(set(letters)))}
L = np.array([vocab[s] for s in letters], dtype=np.int32)
K = len(vocab); N = L.size
rng = np.random.default_rng(0)
print(f"[load {time.time()-t0:.1f}s] N={N} alphabet={K}")

def mi_hat(arr, d, K):
    x = arr[:-d]; y = arr[d:]; n = x.size
    j = np.bincount(x.astype(np.int64) * K + y, minlength=K*K).astype(float) / n
    pj = j.reshape(K, K); px = pj.sum(1); py = pj.sum(0)
    nz = pj > 0; outer = np.outer(px, py)
    return float(np.sum(pj[nz] * np.log2(pj[nz] / outer[nz])))

def mi_excess(arr, K, ds, nshuf=3):
    real = np.array([mi_hat(arr, d, K) for d in ds])
    bias = np.zeros(len(ds))
    for _ in range(nshuf):
        sh = arr.copy(); rng.shuffle(sh)
        bias += np.array([mi_hat(sh, d, K) for d in ds])
    return real - bias / nshuf

def markov_surrogate(arr, K, order):
    """Generate a stream of same length matching arr's order-k conditionals."""
    if order == 0:
        p = np.bincount(arr, minlength=K) / arr.size
        return rng.choice(K, size=arr.size, p=p)
    ctx = defaultdict(lambda: np.zeros(K))
    a = arr
    for i in range(order, a.size):
        ctx[tuple(a[i-order:i])][a[i]] += 1
    probs = {c: v / v.sum() for c, v in ctx.items()}
    out = np.empty(a.size, dtype=np.int32)
    out[:order] = a[:order]
    backoff = np.bincount(arr, minlength=K) / arr.size
    for i in range(order, a.size):
        c = tuple(out[i-order:i])
        p = probs.get(c, backoff)
        out[i] = rng.choice(K, p=p)
    return out

ds = [1,2,3,4,5,6,8,10,13,16,20,25,32,40,50]
real = mi_excess(L, K, ds)

# (A) controls
iid = rng.integers(0, K, size=N).astype(np.int32)
mk2_synth_p = np.zeros((K, K));
tmp = markov_surrogate(L, K, 2)  # a real markov2 surrogate doubles as control
e_iid = mi_excess(iid, K, ds)
print("\n(A) ESTIMATOR VALIDATION (known answers)")
print(f"  IID control  MI_excess: d1={e_iid[0]:+.4f} d5={e_iid[4]:+.4f} d20={e_iid[10]:+.5f}  (expect ~0)")

# (B) decisive: beyond-Markov?
print("\n(B) BEYOND-MARKOV TEST  (real vs order-k surrogates of the same stream)")
print(f"  {'d':>4} | {'real':>9} | {'mk1':>9} | {'mk2':>9} | {'mk3':>9}")
sur = {k: mi_excess(markov_surrogate(L, K, k), K, ds, nshuf=2) for k in (1,2,3)}
for idx, d in enumerate(ds):
    if d in (1,2,5,10,20,50):
        print(f"  {d:>4} | {real[idx]:>9.5f} | {sur[1][idx]:>9.5f} | {sur[2][idx]:>9.5f} | {sur[3][idx]:>9.5f}")
# ratio of total excess-MI mass at d>=5 (long-range) real vs mk3
mask = np.array(ds) >= 5
lr_real = real[mask].clip(min=0).sum()
lr_mk3 = sur[3][mask].clip(min=0).sum()
print(f"  long-range mass (sum MI_excess, d>=5): real={lr_real:.4f}  mk3={lr_mk3:.4f}  "
      f"ratio={lr_real/max(lr_mk3,1e-9):.2f}x")

# (C1) block-entropy rate
print("\n(C) FEASIBILITY OF OTHER PHASE-1 SIGNATURES")
def block_H(arr, n):
    if n == 1:
        c = np.bincount(arr, minlength=K).astype(float)
    else:
        keys = arr[:arr.size-(arr.size%n)]  # not used; do sliding
        c = Counter(tuple(arr[i:i+n]) for i in range(arr.size-n+1))
        c = np.array(list(c.values()), dtype=float)
    p = c / c.sum(); p = p[p>0]
    return float(-(p*np.log2(p)).sum())
Hs = [block_H(L, n) for n in range(1,5)]
hrate = [Hs[0]] + [Hs[i]-Hs[i-1] for i in range(1,4)]
sh = L.copy(); rng.shuffle(sh)
hrate_sh = [block_H(sh,1)] + [block_H(sh,n)-block_H(sh,n-1) for n in range(2,4)]
print(f"  block-entropy rate h_n real:     {[round(x,3) for x in hrate]}  (falling => memory)")
print(f"  block-entropy rate h_n shuffled: {[round(x,3) for x in hrate_sh]}  (flat => none)")

# (C2) DFA, two encodings for robustness
def dfa(x):
    x = x - x.mean(); y = np.cumsum(x)
    scales = np.unique(np.logspace(np.log10(16), np.log10(len(x)//8), 16).astype(int))
    F = []
    for s in scales:
        nseg = len(y)//s
        if nseg < 1: continue
        rms = []
        for k in range(nseg):
            seg = y[k*s:(k+1)*s]; t = np.arange(s)
            c = np.polyfit(t, seg, 1); fit = c[0]*t+c[1]
            rms.append(np.sqrt(np.mean((seg-fit)**2)))
        F.append(np.mean(rms))
    F = np.array(F); sc = scales[:len(F)]
    a = np.polyfit(np.log(sc), np.log(F), 1)[0]
    return a
freq = np.bincount(L, minlength=K)/N
enc_freq = freq[L]                      # map each letter to its probability
rank = {c:r for r,c in enumerate(np.argsort(-freq))}
enc_rank = np.array([rank[c] for c in L], dtype=float)
dfa_real_f = dfa(enc_freq); dfa_real_r = dfa(enc_rank)
dfa_sh = dfa(enc_freq[np.random.default_rng(1).permutation(N)])
print(f"  DFA exponent (freq-encoding) real={dfa_real_f:.3f}  (rank-encoding) real={dfa_real_r:.3f}  "
      f"shuffled={dfa_sh:.3f}  (0.5=no LRC, >0.5=persistent)")

# (C3) compression redundancy
b_real = "".join(chr(int(c)) for c in L).encode("latin-1","ignore")
b_sh = "".join(chr(int(c)) for c in sh).encode("latin-1","ignore")
r_real = len(gzip.compress(b_real,9))/len(b_real)
r_sh = len(gzip.compress(b_sh,9))/len(b_sh)
print(f"  gzip ratio real={r_real:.3f}  shuffled={r_sh:.3f}  "
      f"redundancy gain={(r_sh-r_real)/r_sh*100:.1f}%  (real compresses better => structure)")
print(f"\n[total {time.time()-t0:.1f}s]")
