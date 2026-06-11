#!/usr/bin/env python3
# Phase B — Necessary AND sufficient unit definition by Minimum Description Length.
# The text is its own model. A boundary exists IFF a model-reset there lowers the
# text's total self-description length. Interior = self-predictable (sufficient);
# boundary = self-surprising (necessary). Entirely internal; the only null is the
# text's own shuffle.  (M1, M3 of ROADMAP.md)
#
# Channels (>=3 converging modalities, M2):
#   symbol  : final letter of verse (rhyme / fāṣila)
#   wave    : binned verse length (word count)
#   lexical : content-word identities (top-V vocabulary + OOV) — network/theme modality
#
# Segment code = prequential (Dirichlet-Multinomial / KT, alpha=0.5) marginal code
# length per channel.  This is parameter-free: the per-segment model-complexity
# penalty is built into the marginal likelihood, not hand-tuned (احسن تقویم as MDL).
# Per-segment boundary pointer cost lambda = log2(N) bits (derived, not tuned).

import sys, glob, unicodedata, numpy as np
from collections import Counter
from scipy.special import gammaln

LN2 = np.log(2.0)

# ---- locate data (don't hardcode the session id) ----
cands = glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2/research/two_books_genome/data/quran/quran_arabic_verses.tsv')
DATA = cands[0]

def skel(t):
    t = unicodedata.normalize('NFD', t)
    t = ''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء' <= c <= 'ي' and c != 'ـ') for tok in t.split()) if w]

# ---- load ----
sura=[]; fin=[]; nwords=[]; words=[]; ALL=[]
for ln in open(DATA, encoding='utf-8'):
    if '\t' not in ln: continue
    sa, tx = ln.split('\t', 1)
    su = int(sa.split(':')[0]); w = skel(tx)
    sura.append(su)
    fin.append(w[-1][-1] if w and w[-1] else '')
    nwords.append(len(w)); words.append(w); ALL += w
N = len(sura)
sura = np.array(sura)
truth = np.array([sura[i+1] != sura[i] for i in range(N-1)])   # 113 internal sūra boundaries

# ---- channel alphabets ----
# symbol: final letters
fl_alpha = sorted(set(fin))
fl_id = {c:i for i,c in enumerate(fl_alpha)}
FL = np.array([fl_id[c] for c in fin]); A_fl = len(fl_alpha)

# wave: log-spaced length bins
edges = np.array([0,1,2,3,4,5,6,8,10,13,17,22,29,38,50,66,87,115,300,10**9])
LB = np.digitize(np.array(nwords), edges) - 1; A_lb = LB.max()+1

# lexical: top-V content vocabulary (drop 40 stopwords), rest -> OOV
stop = set(w for w,_ in Counter(ALL).most_common(40))
content = [w for w in ALL if w not in stop]
V = 300
top = [w for w,_ in Counter(content).most_common(V)]
lx_id = {w:i for i,w in enumerate(top)}                 # 0..V-1 ; V == OOV
A_lx = V+1
# per-verse list of lexical ids (content words only)
verse_lx = [[lx_id.get(w, V) for w in ws if w not in stop] for ws in words]

# ---- prefix counts ----
def prefix_counts(ids_per_step, A):
    P = np.zeros((N+1, A), dtype=np.int64)
    for k in range(N):
        P[k+1] = P[k]
        if np.isscalar(ids_per_step[k]):
            P[k+1, ids_per_step[k]] += 1
        else:
            for x in ids_per_step[k]:
                P[k+1, x] += 1
    return P
Pfl = prefix_counts(FL, A_fl)
Plb = prefix_counts(LB, A_lb)
Plx = prefix_counts(verse_lx, A_lx)
Pwords = Plx.sum(axis=1)            # cumulative content-word count

ALPHA = 0.5                         # KT estimator
MAXSEG = 300                        # cap (longest sūra = 286 verses)
LAMBDA = np.log2(N)                 # boundary pointer cost in bits

# gammaln lookup tables (counts are integers)
maxcount = int(max(N, Pwords[-1])) + 5
Gfl = gammaln(np.arange(maxcount) + ALPHA)          # gammaln(k+alpha)
Gfull = gammaln(np.arange(maxcount) + 1.0)          # placeholder; per-channel below
def full_table(A):
    return gammaln(np.arange(maxcount) + A*ALPHA)
Ffl = full_table(A_fl); Flb = full_table(A_lb); Flx = full_table(A_lx)
constfl = gammaln(A_fl*ALPHA) - A_fl*gammaln(ALPHA)
constlb = gammaln(A_lb*ALPHA) - A_lb*gammaln(ALPHA)
constlx = gammaln(A_lx*ALPHA) - A_lx*gammaln(ALPHA)

def seg_cost_matrix(P, Ftab, const, n_seg):
    """For fixed end j, return vector over starts i in [lo,j) of channel code (bits).
       Called inside DP with precomputed P[j]."""
    raise NotImplementedError

def channel_code_bits(counts_2d, n_vec, Gtab, Ftab, const):
    # counts_2d : (n_starts, A) integer counts ; n_vec : (n_starts,) total
    s = Gtab[counts_2d].sum(axis=1)                  # sum_c gammaln(n_c+alpha)
    nats = -(s + const - Ftab[n_vec])
    return nats / LN2

def run_dp(use_fl=True, use_lb=True, use_lx=True, lam=LAMBDA):
    INF = 1e18
    cost = np.full(N+1, INF); cost[0] = 0.0
    back = np.full(N+1, -1, dtype=np.int64)
    for j in range(1, N+1):
        lo = max(0, j-MAXSEG)
        starts = np.arange(lo, j)
        total = 0.0
        if use_fl:
            c = Pfl[j] - Pfl[lo:j]; n = (j - starts)
            total = total + channel_code_bits(c, n, Gfl, Ffl, constfl)
        if use_lb:
            c = Plb[j] - Plb[lo:j]; n = (j - starts)
            total = total + channel_code_bits(c, n, Gfl, Flb, constlb)
        if use_lx:
            c = Plx[j] - Plx[lo:j]; n = (Pwords[j] - Pwords[lo:j])
            total = total + channel_code_bits(c, n, Gfl, Flx, constlx)
        cand = cost[lo:j] + total + lam
        k = np.argmin(cand)
        cost[j] = cand[k]; back[j] = lo + k
    # backtrace boundaries
    bnds = []; j = N
    while j > 0:
        i = back[j]
        if i > 0: bnds.append(i)
        j = i
    bnds = sorted(bnds)
    return cost[N], bnds

def total_cost_of_partition(boundaries, use_fl=True, use_lb=True, use_lx=True, lam=LAMBDA):
    """code length (bits) of an arbitrary partition given by sorted internal boundary indices."""
    cuts = [0] + list(boundaries) + [N]
    tot = 0.0
    for a,b in zip(cuts[:-1], cuts[1:]):
        if use_fl:
            c = (Pfl[b]-Pfl[a]); tot += float(channel_code_bits(c[None,:], np.array([b-a]), Gfl, Ffl, constfl)[0])
        if use_lb:
            c = (Plb[b]-Plb[a]); tot += float(channel_code_bits(c[None,:], np.array([b-a]), Gfl, Flb, constlb)[0])
        if use_lx:
            c = (Plx[b]-Plx[a]); nn = np.array([Pwords[b]-Pwords[a]]); tot += float(channel_code_bits(c[None,:], nn, Gfl, Flx, constlx)[0])
    tot += lam * (len(cuts)-1)
    return tot

def eval_boundaries(pred_idx, tol=0):
    """precision & recall of predicted boundary transition-indices vs canonical, ±tol."""
    truth_idx = set(np.where(truth)[0])     # transition i means boundary between verse i and i+1
    pred = set(int(b)-1 for b in pred_idx)   # segment start b -> transition b-1
    if tol == 0:
        tp = len(pred & truth_idx)
    else:
        tp = sum(1 for p in pred if any((p+d) in truth_idx for d in range(-tol,tol+1)))
    prec = tp/len(pred) if pred else 0.0
    rec  = tp/len(truth_idx) if truth_idx else 0.0
    f1 = 2*prec*rec/(prec+rec) if (prec+rec) else 0.0
    return prec, rec, f1, len(pred)

print(f"N verses={N}  internal sūra boundaries={truth.sum()}  alphabets fl={A_fl} lb={A_lb} lx={A_lx}")
print(f"lambda(boundary)={LAMBDA:.2f} bits  alpha(KT)={ALPHA}")
print("="*70)

configs = [
    ("symbol(fin)",            dict(use_fl=True,  use_lb=False, use_lx=False)),
    ("wave(len)",              dict(use_fl=False, use_lb=True,  use_lx=False)),
    ("lexical(content)",       dict(use_fl=False, use_lb=False, use_lx=True)),
    ("symbol+wave",            dict(use_fl=True,  use_lb=True,  use_lx=False)),
    ("symbol+wave+lexical",    dict(use_fl=True,  use_lb=True,  use_lx=True)),
]
results = {}
for name, kw in configs:
    tc, bnds = run_dp(**kw)
    prec, rec, f1, npred = eval_boundaries(bnds, tol=0)
    prec1, rec1, f11, _ = eval_boundaries(bnds, tol=1)
    results[name] = (tc, bnds)
    print(f"{name:22s} segs={npred+1:4d}  P0={prec:.3f} R0={rec:.3f} F0={f1:.3f}  |  P±1={prec1:.3f} R±1={rec1:.3f} F±1={f11:.3f}  | code={tc/8/1024:.1f} KB")
print("="*70)

# ---------- نcessary AND sufficient: canonical vs MDL-optimal vs nulls ----------
np.random.seed(0)
KW = dict(use_fl=True, use_lb=True, use_lx=True)
canon = list(np.where(truth)[0]+1)                 # canonical segment starts
mdl_cost, mdl_bnds = results["symbol+wave+lexical"]
canon_cost = total_cost_of_partition(canon, **KW)
print("\n--- احسن تقویم: is the canonical partition MDL-load-bearing? (bits) ---")
print(f"MDL-optimal partition cost      = {mdl_cost:,.0f}  ({len(mdl_bnds)+1} segs)")
print(f"canonical sūra partition cost   = {canon_cost:,.0f}  (114 segs)")
print(f"single-segment (no boundaries)  = {total_cost_of_partition([], **KW):,.0f}")

# null 1: shifted boundaries (±5,±10,±20 verses)
print("\nshifted-boundary null (canonical boundaries jittered):")
for sh in (1,5,10,20):
    costs=[]
    for _ in range(20):
        jit = sorted(set(int(np.clip(b+np.random.randint(-sh,sh+1),1,N-1)) for b in canon))
        costs.append(total_cost_of_partition(jit, **KW))
    print(f"  jitter ±{sh:<3d}: mean cost = {np.mean(costs):,.0f}  (Δ vs canonical = +{np.mean(costs)-canon_cost:,.0f} bits)")

# null 2: random partitions with same #segments
rc=[]
for _ in range(50):
    rb = sorted(np.random.choice(np.arange(1,N), size=113, replace=False))
    rc.append(total_cost_of_partition(list(rb), **KW))
print(f"\nrandom 113-cut partitions: mean = {np.mean(rc):,.0f} ± {np.std(rc):,.0f}  (Δ vs canonical = +{np.mean(rc)-canon_cost:,.0f} bits)")

# null 3: verse-shuffle floor — destroy order, redo MDL
order = np.random.permutation(N)
Pfl_s = np.vstack([np.zeros(A_fl,int), np.cumsum(np.eye(A_fl,dtype=int)[FL[order]],axis=0)])
# quick shuffle test: cost of canonical-count cuts on shuffled stream vs real
def shuf_cost():
    # recompute prefix on shuffled, evaluate MDL-optimal on shuffled
    global Pfl,Plb,Plx,Pwords
    return None
print("\n(verse-shuffle floor computed in mdl_shuffle stage below)")

# Save MDL boundaries for downstream (paragraph units discovery)
import json, os
outdir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(outdir,'mdl_boundaries.json'),'w') as f:
    json.dump({"mdl_segment_starts": [int(b) for b in mdl_bnds],
               "canonical_starts": [int(b) for b in canon],
               "n_verses": N}, f)
print(f"\nsaved MDL boundaries -> mdl_boundaries.json ({len(mdl_bnds)+1} segments)")
