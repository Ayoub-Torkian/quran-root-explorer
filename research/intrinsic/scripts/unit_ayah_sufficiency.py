# -*- coding: utf-8 -*-
"""Instrument 4: ĀYAH sufficiency / uniqueness. Necessity (canonical beats random shuffles) is established; this
asks whether the canonical order is UNIQUELY re-derivable from content or sits on a coherence PLATEAU.
 (R) spectral seriation: Fiedler vector of each sūra's āyah-cohesion matrix -> reconstructed order; Kendall τ vs
     canonical (reflection-adjusted).
 (G) optimum-gap: 2-opt best adjacent-coherence vs canonical's -> is canonical AT the content optimum?
 (P) plateau-degeneracy: 2-opt from many random starts -> how many DISTINCT near-optimal (>=95% best) orderings
     far (Kendall) from canonical exist. Large plateau = content UNDER-determines order = necessary-not-sufficient.
Decision: SUFFICIENT iff mean τ>=0.5 AND plateau small. MEASURED."""
import numpy as np, statistics as st
np.random.seed(41)
d=np.load("/tmp/unit.npz"); VV=d["VV"].astype(np.float64); sura=d["sura"]; n=len(sura)
Vn=VV/(np.linalg.norm(VV,axis=1,keepdims=True)+1e-12)
bounds={}; cur=sura[0]; start=0
for i in range(1,n):
    if sura[i]!=cur: bounds[int(cur)]=(start,i); cur=sura[i]; start=i
bounds[int(cur)]=(start,n)
def kendall(a,b):
    L=len(a); ra={v:i for i,v in enumerate(a)}; rb={v:i for i,v in enumerate(b)}; c=di=0
    for i in range(L):
        for j in range(i+1,L):
            s=(ra[a[i]]-ra[a[j]])*(rb[a[i]]-rb[a[j]])
            if s>0: c+=1
            elif s<0: di+=1
    return (c-di)/(c+di) if (c+di) else 1.0
def adjcoh_order(order,Cm): return float(np.mean([Cm[order[i],order[i+1]] for i in range(len(order)-1)]))
def twoopt(order,Cm,iters=60):
    o=order[:]; L=len(o); best=adjcoh_order(o,Cm); imp=True; t=0
    while imp and t<iters:
        imp=False; t+=1
        for i in range(L-1):
            for j in range(i+1,L):
                no=o[:i]+o[i:j+1][::-1]+o[j+1:]; v=adjcoh_order(no,Cm)
                if v>best+1e-9: o=no; best=v; imp=True
    return o,best
taus=[]; gaps=[]; plats=[]
for s,(a,b) in bounds.items():
    L=b-a
    if L<4: continue
    sub=Vn[a:b]; Cm=sub@sub.T
    # (R) Fiedler seriation
    W=np.clip(Cm,0,None); np.fill_diagonal(W,0); Dg=np.diag(W.sum(1)); Lap=Dg-W
    ev,evec=np.linalg.eigh(Lap); f=evec[:,1]; rec=list(np.argsort(f))
    can=list(range(L)); t=kendall(rec,can); taus.append(max(t,-t))
    if L<=34:
        # (G) optimum gap + (P) plateau via 2-opt restarts
        canc=adjcoh_order(can,Cm); opt=can[:]; optc=canc; locopt=[]
        for r in range(10):
            st0=can[:] if r==0 else list(np.random.permutation(L))
            o,c=twoopt(st0,Cm); locopt.append((o,c))
            if c>optc+1e-9: opt,optc=o,c
        gaps.append(canc/optc if optc>0 else 1.0)
        thr=0.95*optc; far=[]
        for o,c in locopt:
            if c>=thr:
                kt=kendall(o,can)
                if max(kt,-kt)<0.7: far.append(o)  # near-optimal but far from canonical
        plats.append(len(far)/len(locopt))
N=len(taus); M=len(gaps)
print("=== Instrument 4: āyah sufficiency / uniqueness ===")
print(f"suras seriated (L>=4): {N}")
print(f"(R) spectral recovery: mean Kendall τ(recovered, canonical) = {st.mean(taus):+.2f} | median {st.median(taus):+.2f} | %d%% of suras τ>=0.5"%int(100*sum(t>=0.5 for t in taus)/N))
print(f"(G) optimum-gap (L<=34, {M} suras): canonical reaches {st.mean(gaps):.0%} of the 2-opt best adjacent-coherence (100%% = canonical IS the optimum)")
print(f"(P) plateau: mean {st.mean(plats):.0%} of local optima are near-best (>=95%) BUT far from canonical (|τ|<0.7) -> {'LARGE plateau (under-determined)' if st.mean(plats)>0.3 else 'small plateau'}")
import itertools
a,b=bounds[108]; sub=Vn[a:b]; Cm=sub@sub.T; can=[0,1,2]
allo=[(adjcoh_order(list(p),Cm),list(p)) for p in itertools.permutations(can)]
allo.sort(reverse=True); canc=adjcoh_order(can,Cm)
print(f"al-Kawthar(108) L=3: canonical coherence {canc:.3f} = rank {[o for _,o in allo].index(can)+1}/6; best {allo[0][0]:.3f}; canonical/best {canc/allo[0][0]:.0%}")
print(f"VERDICT: {'SUFFICIENT' if (st.mean(taus)>=0.5 and st.mean(plats)<=0.3) else 'NECESSARY-NOT-SUFFICIENT'} (rule: τ>=0.5 AND small plateau)")
print("DONE")
