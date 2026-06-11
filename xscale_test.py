"""CROSS-SCALE BINDING — tested on real data, with permutation nulls.

Q1 (phonosemantic Mantel): does a root's SPELLING (character composition)
    predict its MEANING (distributional/semantic neighbourhood) beyond chance?
Q2 (consonant-slot / codon): for triliteral roots, does sharing the consonant
    in slot 1/2/3 predict semantic proximity — and which slot carries the load?
"""
from __future__ import annotations
import sys, time
import numpy as np
from collections import Counter, defaultdict
sys.path.insert(0, ".")
import analysis as A
from analysis import normalize_letters

t0=time.time()
corpus=A.load_corpus("Book6.xlsx")
# root frequency + per-ayah root sets (normalized root spelling)
K=normalize_letters
freq=Counter()
ayah_sets=[]
for toks in corpus.root_tokens:
    s={K(t) for t in toks if K(t)}
    ayah_sets.append(s)
    for r in s: freq[r]+=1

MINF=8
roots=[r for r,c in freq.items() if c>=MINF]
idx={r:i for i,r in enumerate(roots)}
n=len(roots)
print(f"[{time.time()-t0:.1f}s] roots with freq>={MINF}: {n}")

# ---- semantic embedding: within-ayah co-occurrence -> PPMI -> SVD ----
C=np.zeros((n,n))
for s in ayah_sets:
    present=[idx[r] for r in s if r in idx]
    for a in range(len(present)):
        for b in range(a+1,len(present)):
            C[present[a],present[b]]+=1; C[present[b],present[a]]+=1
tot=C.sum()
rowsum=C.sum(1)
with np.errstate(divide='ignore',invalid='ignore'):
    P=C/tot; pr=rowsum/tot
    PPMI=np.log2(np.maximum(P/(np.outer(pr,pr)+1e-12),1e-12))
PPMI[PPMI<0]=0
U,S,Vt=np.linalg.svd(PPMI,full_matrices=False)
d=100
E=U[:,:d]*S[:d]                       # semantic vectors
En=E/ (np.linalg.norm(E,axis=1,keepdims=True)+1e-12)
Ssem=En@En.T                          # cosine similarity

# ---- char-composition vectors (letter multi-hot over the alphabet) ----
alpha=sorted({ch for r in roots for ch in r})
aidx={c:i for i,c in enumerate(alpha)}
Xc=np.zeros((n,len(alpha)))
for r in roots:
    for ch in r: Xc[idx[r],aidx[ch]]=1.0
Xn=Xc/(np.linalg.norm(Xc,axis=1,keepdims=True)+1e-12)
Schar=Xn@Xn.T

# ---- Mantel: correlate semantic vs char similarity, permutation null ----
iu=np.triu_indices(n,1)
sv=Ssem[iu]; cv=Schar[iu]
def pear(a,b):
    a=a-a.mean(); b=b-b.mean()
    return float(a@b/((np.linalg.norm(a)*np.linalg.norm(b))+1e-12))
r_obs=pear(sv,cv)
rng=np.random.default_rng(0)
NP=2000; cnt=0; null=np.empty(NP)
for k in range(NP):
    p=rng.permutation(n)
    Sp=Ssem[p][:,p][iu]
    null[k]=pear(Sp,cv)
p_mantel=(np.sum(null>=r_obs)+1)/(NP+1)
print(f"\nQ1 PHONOSEMANTIC MANTEL (n={n} roots)")
print(f"  observed r(spelling,meaning) = {r_obs:.4f}")
print(f"  permutation null: mean={null.mean():.4f} sd={null.std():.4f}  p={p_mantel:.4g}")
print(f"  -> {'SIGNAL' if p_mantel<0.05 else 'no signal'} (effect size {r_obs:.3f})")

# ---- Q2 consonant-slot / codon (triliteral roots) ----
tri=[r for r in roots if len(r)==3]
ti={r:i for i,r in enumerate(tri)}
m=len(tri)
Etri=En[[idx[r] for r in tri]]
Stri=Etri@Etri.T
iu2=np.triu_indices(m,1)
sim2=Stri[iu2]
print(f"\nQ2 CONSONANT-SLOT / CODON (triliteral roots n={m})")
for slot in (0,1,2):
    letters=np.array([list(r)[slot] for r in tri])
    # pairs sharing the same letter at this slot
    same=(letters[iu2[0]]==letters[iu2[1]])
    obs=sim2[same].mean()-sim2[~same].mean()      # semantic-sim lift for shared-slot pairs
    nd=2000; nl=np.empty(nd)
    for k in range(nd):
        perm=rng.permutation(letters)
        sm=(perm[iu2[0]]==perm[iu2[1]])
        nl[k]=sim2[sm].mean()-sim2[~sm].mean()
    p=(np.sum(nl>=obs)+1)/(nd+1)
    z=(obs-nl.mean())/(nl.std()+1e-12)
    print(f"  slot {slot+1}: semantic lift for shared letter = {obs:+.4f}  z={z:+.2f}  p={p:.4g}")
print(f"\n[total {time.time()-t0:.1f}s]")
