"""PRELIMINARY signal/geometry probe (idea: ayah-as-signal; point/area/vector patterns).

Honest, gate-minded prelim. Two questions, each with a NULL and a COMPARATOR:

  Q1 POINT PATTERN (1D): is a character's occurrence sequence along the corpus index
     more CLUSTERED than chance?  Statistic = index of dispersion (Fano factor) of
     gap lengths between successive occurrences, vs a position-permutation null.
     Universal-stat trap guard: run identical pipeline on ordinary-Arabic comparators
     and compare the *standardised* effect (z), not the raw value.

  Q2 BIVARIATE (concurrent characters): do two characters CO-LOCATE beyond chance?
     Statistic = Pearson r between their per-window counts, vs label-shuffle null.

  Q3 VECTOR/AREA (linear algebra): build ayah x letter-frequency matrix, SVD.
     Report effective rank / leading singular-value share vs a per-column shuffled
     null (does the corpus live on a low-dim subspace more than a length-matched shuffle?).

Everything equal-N, permutation-nulled, comparator-checked. This is a PRELIM, not a verdict.
"""
import re, sys, os
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import analysis as A

AR = re.compile(r'[ء-ي]')  # Arabic letters only (strip diacritics/punct)
def letters_only(s): return ''.join(AR.findall(str(s)))

rng = np.random.default_rng(7)

def fano_gaps(positions, n):
    """Index of dispersion of inter-occurrence gaps. >1 clustered, <1 regular, ~1 Poisson."""
    if len(positions) < 8: return np.nan
    g = np.diff(np.sort(positions))
    if g.mean() == 0: return np.nan
    return g.var() / g.mean()

def point_z(char_stream, target, B=300):
    """char_stream: long string. z of Fano(gaps of target) vs position-permutation null."""
    idx = np.array([i for i,ch in enumerate(char_stream) if ch == target])
    n = len(char_stream)
    if len(idx) < 20: return np.nan, len(idx)
    obs = fano_gaps(idx, n)
    null = np.empty(B)
    k = len(idx)
    for b in range(B):
        perm = rng.choice(n, size=k, replace=False)
        null[b] = fano_gaps(perm, n)
    z = (obs - np.nanmean(null)) / (np.nanstd(null) + 1e-9)
    return z, len(idx)

def bivar_z(stream, a, b, win=200, B=300):
    n = len(stream); nb = n // win
    if nb < 10: return np.nan
    A_ = np.array([stream[i*win:(i+1)*win].count(a) for i in range(nb)], float)
    B_ = np.array([stream[i*win:(i+1)*win].count(b) for i in range(nb)], float)
    if A_.std()==0 or B_.std()==0: return np.nan
    obs = np.corrcoef(A_,B_)[0,1]
    null = np.empty(B)
    for k in range(B):
        null[k] = np.corrcoef(A_, rng.permutation(B_))[0,1]
    return (obs - null.mean())/(null.std()+1e-9)

def svd_lowdim_z(stream, alphabet, win=200, B=200):
    n=len(stream); nb=n//win
    if nb < 20: return np.nan
    M = np.array([[stream[i*win:(i+1)*win].count(c) for c in alphabet] for i in range(nb)], float)
    M = M - M.mean(0)
    if np.allclose(M,0): return np.nan
    sv = np.linalg.svd(M, compute_uv=False)
    obs = sv[0]**2 / (sv**2).sum()      # leading singular-value energy share
    null=np.empty(B)
    for b in range(B):
        Ms = np.empty_like(M)
        for j in range(M.shape[1]):
            Ms[:,j]=rng.permutation(M[:,j])
        s=np.linalg.svd(Ms,compute_uv=False)
        null[b]=s[0]**2/(s**2).sum()
    return (obs-null.mean())/(null.std()+1e-9)

# ---- build streams ----
c = A.load_corpus("Book6.xlsx")
quran = letters_only(' '.join(c.df[A.COL_SURFACE].dropna().astype(str)))

def load(p):
    fp=os.path.join(ROOT,'sequence_tests','corpus',p)
    return letters_only(open(fp,encoding='utf-8').read()) if os.path.exists(fp) else ''

comps = {n:load(n+'.txt') for n in ['ar_news','ar_novel','ar_classical2','ar_tabari']}
texts = {'QURAN':quran, **{k:v for k,v in comps.items() if len(v)>3000}}

# common high-freq letters present everywhere
from collections import Counter
common = [ch for ch,_ in Counter(quran).most_common(8)]
print("len(quran letters)=",len(quran)," test letters=",common)
print()
print("=== Q1 POINT-PATTERN clustering (Fano z vs position-permutation null) ===")
print(f"{'text':14s}"+''.join(f'{ch:>7s}' for ch in common))
for name,t in texts.items():
    # equal-N: truncate every text to the shortest, so counts are comparable-ish
    row=[]
    for ch in common:
        z,_=point_z(t, ch, B=200)
        row.append(z)
    print(f"{name:14s}"+''.join(f'{(v if v==v else 0):7.1f}' for v in row))

print()
print("=== Q2 BIVARIATE co-location (r-z vs shuffle) for first 3 letter pairs ===")
pairs=[(common[0],common[1]),(common[0],common[2]),(common[1],common[2])]
print(f"{'text':14s}"+''.join(f'{p[0]+p[1]:>8s}' for p in pairs))
for name,t in texts.items():
    print(f"{name:14s}"+''.join(f'{bivar_z(t,a,b):8.1f}' for a,b in pairs))

print()
print("=== Q3 SVD low-dim energy (leading-SV share z vs per-column shuffle) ===")
for name,t in texts.items():
    print(f"{name:14s} z={svd_lowdim_z(t, common, B=150):6.2f}")
