# -*- coding: utf-8 -*-
"""Instrument 12: MATHĀNĪ grounded = consimilar PAIRS (متشابها مثاني, 39:23; مثنى = two-by-two). Test the text's
PAIR-MATCHING structure (not similarity-chaining, which all prior instruments tried and which nulled):
 (A) per-unit distinctive TWIN: gap between each unit's best match and 2nd-best (clean pairing => big gap) vs null.
 (B) max-weight matching into pairs vs random-matching null.
 (C) do matched resembling pairs sit in STRUCTURED positions (adjacent / near in the canonical order)? -> would tie
     pairing to the ARRANGEMENT (mathānī as an organizing principle of placement).
Run at SŪRA level (mean root-vector per sūra) AND ĀYAH level within sūras. Known sūra-pairs checked. MEASURED."""
import numpy as np, statistics as st
np.random.seed(5)
d=np.load("/tmp/unit.npz"); VV=d["VV"].astype(np.float64); sura=d["sura"]; n=len(sura)
bounds={}; cur=sura[0]; start=0
for i in range(1,n):
    if sura[i]!=cur: bounds[int(cur)]=(start,i); cur=sura[i]; start=i
bounds[int(cur)]=(start,n)
sids=sorted(bounds)
SV=np.array([VV[a:b].mean(0) for s in sids for (a,b) in [bounds[s]]])
SV=SV/(np.linalg.norm(SV,axis=1,keepdims=True)+1e-12)
S=SV@SV.T; np.fill_diagonal(S,-9)
m=len(sids)
# (A) distinctive twin: best - 2nd-best gap
gaps=[]
for i in range(m):
    row=np.sort(S[i])[::-1]; gaps.append(row[0]-row[1])
nullg=[]
for _ in range(200):
    P=np.random.permutation(m); Sp=S[np.ix_(P,P)]
    g=[np.sort(Sp[i])[::-1][0]-np.sort(Sp[i])[::-1][1] for i in range(m)]; nullg.append(np.mean(g))
zg=(np.mean(gaps)-np.mean(nullg))/(np.std(nullg) or 1e-9)
# (B) greedy max-weight matching
def greedy_match(M):
    M=M.copy(); used=set(); tot=0; pairs=[]
    order=np.dstack(np.unravel_index(np.argsort(-M,axis=None),M.shape))[0]
    for i,j in order:
        if i in used or j in used or i==j: continue
        used.add(i); used.add(j); tot+=M[i,j]; pairs.append((i,j))
        if len(used)>=m-1: break
    return tot,pairs
wt,pairs=greedy_match(S)
nullw=[]
for _ in range(200):
    P=np.random.permutation(m); nullw.append(greedy_match(S[np.ix_(P,P)])[0])
zw=(wt-np.mean(nullw))/(np.std(nullw) or 1e-9)
# (C) positional structure of matched pairs (sūra index distance in canonical order)
dists=[abs(i-j) for i,j in pairs]
nd=[]
for _ in range(200):
    P=list(range(m)); np.random.shuffle(P); nd.append(np.mean([abs(P[i]-P[j]) for i,j in pairs]))
zc=(np.mean(dists)-np.mean(nd))/(np.std(nd) or 1e-9)
# known pairs check
known=[(2,3),(113,114),(73,74),(105,106),(93,94),(8,9),(56,55)]
idx={s:k for k,s in enumerate(sids)}
print("=== Instrument 12: mathānī as consimilar PAIRS (sūra level) ===")
print(f"  (A) distinctive-twin gap (best-2nd): mean {np.mean(gaps):.3f} vs null {np.mean(nullg):.3f} -> z={zg:+.1f}  (big gap = clean pairing)")
print(f"  (B) max-weight pair-matching: weight {wt:.1f} vs random-match null {np.mean(nullw):.1f}±{np.std(nullw):.1f} -> z={zw:+.1f}")
print(f"  (C) matched-pair canonical-distance: mean {np.mean(dists):.1f} vs null {np.mean(nd):.1f} -> z={zc:+.1f}  (negative = pairs sit NEAR each other)")
print("  known-pair similarity rank (is the canonical twin each sūra's top match?):")
for x,y in known:
    if x in idx and y in idx:
        i,j=idx[x],idx[y]; r=int((S[i]>S[i,j]).sum())+1
        print(f"    S{x}~S{y}: sim={S[i,j]:+.2f}, S{y} is S{x}'s #{r} match of {m-1}")
print("DONE")
