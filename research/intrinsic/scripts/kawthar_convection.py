# -*- coding: utf-8 -*-
"""Convection vs conduction (internal, data-driven): is global connection carried by hubs (convection) or
local diffusion (conduction)? Tests: small-world sigma; and targeted (hub) vs random node removal -> path length & giant comp."""
import collections, itertools, random, statistics as st
import networkx as nx
random.seed(11)
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا')
rows=[]
for line in open(f"{R}/research/two_books_genome/roots_by_ayah.tsv",encoding='utf-8'):
    line=line.rstrip('\n')
    if '\t' in line: k,rs=line.split('\t',1); rows.append([fa(x) for x in set(rs.split())])
cnt=collections.Counter(r for rs in rows for r in rs)
co=collections.Counter()
for rs in rows:
    for a,b in itertools.combinations(sorted(rs),2): co[(a,b)]+=1
nodes=[r for r in cnt if cnt[r]>=5]
G=nx.Graph()
G.add_nodes_from(nodes)
for (a,b),w in co.items():
    if a in cnt and b in cnt and cnt[a]>=5 and cnt[b]>=5 and w>=2: G.add_edge(a,b,w=w)
G=G.subgraph(max(nx.connected_components(G),key=len)).copy()
n,m=G.number_of_nodes(),G.number_of_edges()
print(f"giant component: {n} nodes, {m} edges, <k>={2*m/n:.1f}")
def avgL(g,samp=400):
    ns=list(g); tot=c=0
    for s in random.sample(ns,min(samp,len(ns))):
        d=nx.single_source_shortest_path_length(g,s)
        tot+=sum(d.values()); c+=len(d)-1
    return tot/c
C=nx.average_clustering(G); L=avgL(G)
# ER baseline
p=2*m/(n*(n-1)); import math
Crand=p; Lrand=math.log(n)/math.log(2*m/n)
sigma=(C/Crand)/(L/Lrand)
print(f"clustering C={C:.3f} (rand {Crand:.4f}) ; path L={L:.2f} (rand {Lrand:.2f}) ; small-world sigma={sigma:.1f}")
print("-> high C + short L = small-world: local conduction trapped, but short global paths exist (carried).")
# ATTACK: hub (degree) removal vs random removal
deg=dict(G.degree())
hubs=sorted(deg,key=lambda r:-deg[r])
print("\ntop carrier hubs (degree):", [(h,deg[h]) for h in hubs[:8]])
print("\n#removed | HUB-removal: GC% , L | RANDOM-removal: GC% , L")
for k in [0,5,10,20,40,80]:
    Gh=G.copy(); Gh.remove_nodes_from(hubs[:k])
    gch=max((len(c) for c in nx.connected_components(Gh)),default=0)
    Lh=avgL(G.subgraph(max(nx.connected_components(Gh),key=len)).copy()) if gch>2 else float('nan')
    Gr=G.copy(); Gr.remove_nodes_from(random.sample(nodes:=list(G),k)) if k else None
    gcr=max((len(c) for c in nx.connected_components(Gr)),default=0)
    Lr=avgL(G.subgraph(max(nx.connected_components(Gr),key=len)).copy()) if gcr>2 else float('nan')
    print(f"  {k:3d}   |  {100*gch/n:4.0f}% , {Lh:4.2f}  |  {100*gcr/n:4.0f}% , {Lr:4.2f}")
# al-Kawthar roots' roles
print("\nal-Kawthar roots in the transport graph:")
for r in [fa(x) for x in ['ربب','صلو','کثر','عطو','شنء','نحر','بتر']]:
    print(f"  {r}: {'deg '+str(deg[r])+(' (CARRIER hub)' if r in hubs[:20] else '') if r in deg else 'island / not in giant component'}")
