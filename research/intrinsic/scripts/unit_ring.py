# -*- coding: utf-8 -*-
"""Instrument 10: RING / concentric (chiastic) composition — a GLOBAL, internal organizing principle that local
recovery is blind to by construction. Hypothesis: āyah k is positioned to mirror āyah (L-1-k), so content
similarity at MIRROR positions is elevated. Per sūra: mean cos(v_i, v_{L-1-i}) over mirror pairs vs within-sūra
order-shuffle null -> z. Distance-controlled variant: mirror-pair sim vs same-|distance| non-mirror pairs.
Aggregate. MEASURED, embedding on rasm roots, divine substrate."""
import numpy as np, statistics as st, math
d=np.load("/tmp/unit.npz"); VV=d["VV"].astype(np.float64); sura=d["sura"]; n=len(sura)
Vn=VV/(np.linalg.norm(VV,axis=1,keepdims=True)+1e-12)
bounds={}; cur=sura[0]; start=0
for i in range(1,n):
    if sura[i]!=cur: bounds[int(cur)]=(start,i); cur=sura[i]; start=i
bounds[int(cur)]=(start,n)
def mirror_mean(C,perm=None):
    L=C.shape[0]; idx=list(range(L)) if perm is None else perm
    return np.mean([C[idx[i],idx[L-1-i]] for i in range(L//2)]) if L>=2 else 0.0
zs=[]; dctrl=[]; bigs=[]
for s,(a,b) in bounds.items():
    L=b-a
    if L<6: continue
    sub=Vn[a:b]; C=sub@sub.T
    m0=mirror_mean(C)
    nl=[]
    for _ in range(300):
        p=list(range(L)); np.random.shuffle(p); nl.append(mirror_mean(C,p))
    z=(m0-st.mean(nl))/(st.pstdev(nl) or 1e-9); zs.append(z)
    if z>3: bigs.append((z,s,L))
    # distance-controlled: for each mirror pair (i, L-1-i) at distance D, compare to mean sim of all pairs at distance D
    diffs=[]
    for i in range(L//2):
        j=L-1-i; D=j-i
        same=[C[x,x+D] for x in range(L-D)]
        diffs.append(C[i,j]-np.mean(same))
    dctrl.append(np.mean(diffs))
N=len(zs)
print("=== Instrument 10: ring / concentric composition ===")
print(f"suras (L>=6): {N}")
print(f"  mirror-pair elevation vs order-shuffle: mean z={st.mean(zs):+.2f} | median {st.median(zs):+.2f} | {100*sum(z>2 for z in zs)/N:.0f}% z>2 | Stouffer Z={sum(zs)/math.sqrt(N):+.0f}")
print(f"  distance-controlled (mirror sim - same-distance mean): mean {st.mean(dctrl):+.4f} ({100*sum(d>0 for d in dctrl)/N:.0f}% positive)")
bigs.sort(reverse=True)
print("  strongest ring-candidate sūras (z, sūra, L):", [(round(z,1),s,L) for z,s,L in bigs[:8]])
print("DONE")
