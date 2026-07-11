# -*- coding: utf-8 -*-
"""Instrument 11: MATHĀNĪ (مثاني) — the text's self-described structure (15:87, 39:23): doubling / pairing /
folding / oft-repeated. Distinct from RING (mirror i<->L-1-i, instrument 10 = null). Tests, all internal:
 (P) parallel-panel/fold: sim(v_i, v_{i+⌈L/2⌉}) elevated — does the 2nd half PARALLEL the 1st (folded in two)?
 (2) period-2 pairing: within-pair sim(2k,2k+1) > between-pair sim(2k+1,2k+2) — āyāt grouped in twos?
 (R) recurrence/oft-repeated: mean best non-adjacent self-similarity — does content RECUR across the sūra?
All vs within-sūra order-shuffle null -> z. MEASURED, root embedding on rasm, divine substrate."""
import numpy as np, statistics as st, math
d=np.load("/tmp/unit.npz"); VV=d["VV"].astype(np.float64); sura=d["sura"]; n=len(sura)
Vn=VV/(np.linalg.norm(VV,axis=1,keepdims=True)+1e-12)
bounds={}; cur=sura[0]; start=0
for i in range(1,n):
    if sura[i]!=cur: bounds[int(cur)]=(start,i); cur=sura[i]; start=i
bounds[int(cur)]=(start,n)
def parallel(C,perm=None):
    L=C.shape[0]; idx=list(range(L)) if perm is None else perm; h=(L+1)//2
    v=[C[idx[i],idx[i+h]] for i in range(L-h)]; return np.mean(v) if v else 0.0
def pairing(C,perm=None):
    L=C.shape[0]; idx=list(range(L)) if perm is None else perm
    win=[C[idx[2*k],idx[2*k+1]] for k in range((L)//2)]
    btw=[C[idx[2*k+1],idx[2*k+2]] for k in range((L-1)//2)]
    return (np.mean(win) if win else 0)-(np.mean(btw) if btw else 0)
def recurr(C,perm=None):
    L=C.shape[0]; idx=list(range(L)) if perm is None else perm; best=[]
    for i in range(L):
        cand=[C[idx[i],idx[j]] for j in range(L) if abs(i-j)>2]
        if cand: best.append(max(cand))
    return np.mean(best) if best else 0.0
zP=[]; z2=[]; zR=[]
for s,(a,b) in bounds.items():
    L=b-a
    if L<6: continue
    C=Vn[a:b]@Vn[a:b].T
    for fn,acc in ((parallel,zP),(pairing,z2),(recurr,zR)):
        m0=fn(C); nl=[]
        for _ in range(200):
            p=list(range(L)); np.random.shuffle(p); nl.append(fn(C,p))
        acc.append((m0-st.mean(nl))/(st.pstdev(nl) or 1e-9))
N=len(zP)
def rep(z): return f"mean z={st.mean(z):+.2f} | median {st.median(z):+.2f} | {100*sum(x>2 for x in z)/len(z):.0f}% z>2 | Stouffer Z={sum(z)/math.sqrt(len(z)):+.0f}"
print("=== Instrument 11: MATHĀNĪ (doubling / pairing / recurrence) ===")
print(f"suras (L>=6): {N}")
print(f"  (P) parallel-panel/fold (i ↔ i+L/2):  {rep(zP)}")
print(f"  (2) period-2 pairing (within>between): {rep(z2)}")
print(f"  (R) recurrence / oft-repeated:         {rep(zR)}")
print(f"  [contrast] ring/mirror (instr 10) was Stouffer Z=-1 (null)")
# al-Fatiha = al-sab' al-mathānī (sūra 1, 7 āyāt)
a,b=bounds[1]; C=Vn[a:b]@Vn[a:b].T; L=b-a
print(f"  al-Fātiḥa (sūra 1, L={L} 'the seven mathānī'): parallel={parallel(C):+.3f} pairing={pairing(C):+.3f} recurrence={recurr(C):+.3f}")
print("DONE")
