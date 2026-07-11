# -*- coding: utf-8 -*-
"""Remaining motif types: (A) undirected graphlets (triangles, 4-cliques) vs degree null;
(B) typed-role hierarchy (source/relay/sink flow) vs role-shuffle null; (C) sequence motif (adjacent-ayah root reuse) vs within-sura order shuffle. MEASURED."""
import openpyxl, math, random, statistics as st
import networkx as nx
from collections import defaultdict, Counter
random.seed(17)
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
wb=openpyxl.load_workbook(R+"/Book6.xlsx", read_only=True, data_only=True); ws=wb.active
ayah=[]; sura=[]
for r in ws.iter_rows(min_row=9, values_only=True):
    try: s=int(r[5])
    except (TypeError,ValueError): continue
    ayah.append(set(str(r[8] or "").split())); sura.append(s)
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
# directed (for roles) + undirected
G=nx.DiGraph(); G.add_nodes_from(NODES)
for (a,b),c in co.items():
    if c>=5 and c/df[a]>=0.25: G.add_edge(a,b)
Gu=nx.Graph(); Gu.add_nodes_from(NODES)
for (a,b),c in co.items():
    if c>=5: Gu.add_edge(a,b)
# (A) undirected graphlets
realT=nx.transitivity(Gu)
def n4clique(g):
    return sum(1 for c in nx.find_cliques(g) if len(c)>=4)
real4=n4clique(Gu)
Tn=[]; C4n=[]
for _ in range(8):
    h=Gu.copy(); 
    try: nx.double_edge_swap(h,nswap=5*h.number_of_edges(),max_tries=50*h.number_of_edges())
    except Exception: pass
    Tn.append(nx.transitivity(h)); C4n.append(n4clique(h))
zT=(realT-st.mean(Tn))/(st.pstdev(Tn) or 1e-9); z4=(real4-st.mean(C4n))/(st.pstdev(C4n) or 1e-9)
print("=== (A) UNDIRECTED graphlets (co-occurrence graph %d nodes %d edges) ==="%(Gu.number_of_nodes(),Gu.number_of_edges()))
print(f"  transitivity {realT:.3f} vs null {st.mean(Tn):.3f}±{st.pstdev(Tn):.3f} -> z={zT:+.1f}")
print(f"  maximal 4+cliques {real4} vs null {st.mean(C4n):.1f}±{st.pstdev(C4n):.1f} -> z={z4:+.1f}")
# (B) typed-role hierarchy: source/relay/sink by directed degree
rank={}
for nd in G.nodes():
    o=G.out_degree(nd); i=G.in_degree(nd); rank[nd]=(o-i)/(o+i+1e-9)
def role(nd): return 'src' if rank[nd]>0.33 else ('sink' if rank[nd]<-0.33 else 'rly')
cnt=Counter(role(nd) for nd in G.nodes())
# downhill = edge goes from higher source-rank to lower (src->rly->sink)
def downhill(rk):
    d=sum(1 for a,b in G.edges() if rk[a]>rk[b]); return d/G.number_of_edges()
realD=downhill(rank)
vals=list(rank.values())
Dn=[]
for _ in range(150):
    sh=dict(zip(list(rank.keys()), random.sample(vals,len(vals))))
    Dn.append(downhill(sh))
zD=(realD-st.mean(Dn))/(st.pstdev(Dn) or 1e-9)
print("=== (B) TYPED-ROLE hierarchy (grounded: in/out-degree) ===")
print(f"  roles: {dict(cnt)}")
print(f"  edges flowing source->sink (downhill): {realD:.3f} vs role-shuffle null {st.mean(Dn):.3f}±{st.pstdev(Dn):.3f} -> z={zD:+.1f}")
# (C) sequence motif: adjacent-ayah shared-root vs within-sura order shuffle
bounds=defaultdict(list)
for i,s in enumerate(sura): bounds[s].append(i)
def adj_share(order_idx):
    tot=0;n=0
    for s,ix in order_idx.items():
        for k in range(len(ix)-1):
            tot+= 1 if (ayah[ix[k]] & ayah[ix[k+1]]) else 0; n+=1
    return tot/n
base={s:ix[:] for s,ix in bounds.items()}
realS=adj_share(base)
Sn=[]
for _ in range(80):
    shf={s:random.sample(ix,len(ix)) for s,ix in bounds.items()}
    Sn.append(adj_share(shf))
zS=(realS-st.mean(Sn))/(st.pstdev(Sn) or 1e-9)
print("=== (C) SEQUENCE motif (adjacent-ayah root reuse) ===")
print(f"  adjacent-ayah share-a-root: {realS:.3f} vs within-sura order-shuffle {st.mean(Sn):.3f}±{st.pstdev(Sn):.3f} -> z={zS:+.1f}")
print("DONE")
