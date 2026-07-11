# -*- coding: utf-8 -*-
"""Explore motif types: (1) reciprocity (2-node) vs degree-preserving null; (2) directed triad census vs a
RECIPROCITY-PRESERVING null. Names the tight mutual pairs. MEASURED; grounded topology."""
import openpyxl, math, random
import networkx as nx
from collections import defaultdict, Counter
random.seed(17)
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
wb=openpyxl.load_workbook(R+"/Book6.xlsx", read_only=True, data_only=True); ws=wb.active
ayah=[]
for r in ws.iter_rows(min_row=9, values_only=True):
    try: int(r[5])
    except (TypeError,ValueError): continue
    ayah.append(set(str(r[8] or "").split()))
df=Counter()
for a in ayah:
    for x in a: df[x]+=1
NODES=[r for r in df if df[r]>=25]; idx=set(NODES)
co=defaultdict(int)
for a in ayah:
    pr=[x for x in a if x in idx]
    for i in range(len(pr)):
        for j in range(len(pr)):
            if i!=j: co[(pr[i],pr[j])]+=1
G=nx.DiGraph(); G.add_nodes_from(NODES)
for (a,b),c in co.items():
    if c>=5 and c/df[a]>=0.25: G.add_edge(a,b)
m=G.number_of_edges()
# --- (1) reciprocity ---
mut_pairs=set(); asym=[]
for a,b in G.edges():
    if G.has_edge(b,a): mut_pairs.add(frozenset((a,b)))
    else: asym.append((a,b))
recip=2*len(mut_pairs)/m
# degree-preserving null (destroys reciprocity)
def swap_dp(g,ns):
    E=list(g.edges()); ed=set(E); M=len(E)
    for _ in range(ns):
        i,j=random.randrange(M),random.randrange(M); a,b=E[i]; c,d=E[j]
        if len({a,b,c,d})<4 or (a,d) in ed or (c,b) in ed: continue
        ed.discard((a,b));ed.discard((c,d));ed.add((a,d));ed.add((c,b));E[i]=(a,d);E[j]=(c,b)
    h=nx.DiGraph();h.add_nodes_from(g.nodes());h.add_edges_from(ed);return h
import statistics as st
rn=[]
for _ in range(40):
    h=swap_dp(G,10*m); hm=sum(1 for a,b in h.edges() if h.has_edge(b,a))/h.number_of_edges(); rn.append(hm)
zr=(recip-st.mean(rn))/(st.pstdev(rn) or 1e-9)
print("=== (1) RECIPROCITY (2-node motif) ===")
print(f"observed reciprocal-edge fraction {recip:.3f} vs degree-preserving null {st.mean(rn):.3f}±{st.pstdev(rn):.3f} -> z={zr:+.1f}")
tp=sorted(mut_pairs,key=lambda p:-min(co[tuple(p)],co[tuple(p)[::-1]] if len(p)==2 else 0))
def Pmin(p):
    a,b=tuple(p); return min(co[(a,b)]/df[a],co[(b,a)]/df[b])
tp=sorted(mut_pairs,key=lambda p:-Pmin(p))[:12]
print("tightest mutual (reciprocal) pairs [min P each way]:")
for p in tp:
    a,b=tuple(p); print(f"    {a}<->{b}   P {co[(a,b)]/df[a]:.2f}/{co[(b,a)]/df[b]:.2f}")
# --- (2) reciprocity-PRESERVING null + triad census ---
CONN=['021D','021U','021C','111D','111U','030T','030C','120D','120U','120C','201','210','300']
real=nx.triadic_census(G); realc={k:real[k] for k in CONN}
def recip_pres_null(ns_m,ns_a):
    mp=[tuple(p) for p in mut_pairs]; A=list(asym)
    edset=set(); 
    for a,b in mp: edset.add((a,b)); edset.add((b,a))
    for e in A: edset.add(e)
    # swap mutual pairs
    for _ in range(ns_m):
        i,j=random.randrange(len(mp)),random.randrange(len(mp)); a,b=mp[i]; c,d=mp[j]
        if len({a,b,c,d})<4: continue
        if (a,d) in edset or (d,a) in edset or (c,b) in edset or (b,c) in edset: continue
        for e in [(a,b),(b,a),(c,d),(d,c)]: edset.discard(e)
        for e in [(a,d),(d,a),(c,b),(b,c)]: edset.add(e)
        mp[i]=(a,d); mp[j]=(c,b)
    # swap asym edges (avoid creating mutual)
    for _ in range(ns_a):
        i,j=random.randrange(len(A)),random.randrange(len(A)); a,b=A[i]; c,d=A[j]
        if len({a,b,c,d})<4: continue
        if (a,d) in edset or (d,a) in edset or (c,b) in edset or (b,c) in edset: continue
        edset.discard((a,b)); edset.discard((c,d)); edset.add((a,d)); edset.add((c,b)); A[i]=(a,d); A[j]=(c,b)
    h=nx.DiGraph(); h.add_nodes_from(G.nodes()); h.add_edges_from(edset); return h
acc={k:[] for k in CONN}
for _ in range(40):
    h=recip_pres_null(10*len(mut_pairs),10*len(asym)); tc=nx.triadic_census(h)
    for k in CONN: acc[k].append(tc[k])
print("\n=== (2) triad census vs RECIPROCITY-PRESERVING null (does anything survive?) ===")
z={}
for k in CONN:
    mu=st.mean(acc[k]); sd=st.pstdev(acc[k]) or 1e-9; z[k]=(realc[k]-mu)/sd
for k in sorted(CONN,key=lambda x:-abs(z[x])):
    flag=" <== survives" if abs(z[k])>=3 and k not in ('030T',) else ""
    print(f"  {k}: real {realc[k]:7d}  null {st.mean(acc[k]):8.1f}  z {z[k]:+7.1f}{flag}")
print("DONE")
