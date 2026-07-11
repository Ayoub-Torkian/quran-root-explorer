# -*- coding: utf-8 -*-
"""Directed triad-motif census of the self-interpretation root web vs degree-preserving null.
Significance profile (Milo superfamily) + al-Kawthar focal triads. MEASURED; grounded topology (no role labels)."""
import openpyxl, math, random, json
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
CONN=['021D','021U','021C','111D','111U','030T','030C','120D','120U','120C','201','210','300']
real=nx.triadic_census(G); realc={k:real[k] for k in CONN}
def swap(g,nsw):
    E=list(g.edges()); ed=set(E); m=len(E)
    for _ in range(nsw):
        i,j=random.randrange(m),random.randrange(m)
        a,b=E[i]; c,d=E[j]
        if len({a,b,c,d})<4: continue
        if (a,d) in ed or (c,b) in ed: continue
        ed.discard((a,b)); ed.discard((c,d)); ed.add((a,d)); ed.add((c,b))
        E[i]=(a,d); E[j]=(c,b)
    h=nx.DiGraph(); h.add_nodes_from(g.nodes()); h.add_edges_from(ed); return h
NN=60; acc={k:[] for k in CONN}
for t in range(NN):
    h=swap(G,10*G.number_of_edges()); tc=nx.triadic_census(h)
    for k in CONN: acc[k].append(tc[k])
import statistics as st
z={}
for k in CONN:
    mu=st.mean(acc[k]); sd=st.pstdev(acc[k]) or 1e-9; z[k]=(realc[k]-mu)/sd
# significance profile (unit-normalized z over connected triads)
norm=math.sqrt(sum(v*v for v in z.values())) or 1; SP={k:z[k]/norm for k in CONN}
print("=== directed triad census (self-interpretation web, 346 nodes) ===")
for k in sorted(CONN,key=lambda x:-abs(z[x])):
    print(f"  {k}: real {realc[k]:7d}  z {z[k]:+8.1f}  SP {SP[k]:+.2f}")
# al-Kawthar focal: FFLs (030T) containing a kawthar root
Kset={'کثر','صلو','ربب','عطو','نحر','شنء','بتر'}
ffl=[]
for a in G:
    for b in G.successors(a):
        for c in G.successors(b):
            if c!=a and G.has_edge(a,c):   # a->b->c & a->c = FFL
                if {a,b,c}&Kset: ffl.append((a,b,c))
print("=== al-Kawthar roots in feed-forward triads (a->b->c, a->c) — sample ===")
for tr in ffl[:12]: print("   ",tr)
print("total FFLs touching a kawthar root:",len(ffl))
json.dump({"z":z,"SP":SP,"real":realc,"n":G.number_of_nodes(),"m":G.number_of_edges()},
          open(R+"/research/intrinsic/anatomy_figs/motif_census.json","w",encoding='utf-8'),ensure_ascii=False,indent=1)
print("DONE")
