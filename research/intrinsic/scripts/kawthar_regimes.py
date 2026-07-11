# -*- coding: utf-8 -*-
"""Transport regimes across the rarity spectrum: per frequency band, measure betweenness (convective carrying),
local clustering (conductive embedding), and giant-component participation (islands?). Tests 'both regimes, local<->global'."""
import collections, itertools, statistics as st
import networkx as nx
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
# full graph over ALL roots (edge if co>=2) to see who is island vs connected across the whole spectrum
G=nx.Graph()
G.add_nodes_from(cnt)
for (a,b),w in co.items():
    if w>=2: G.add_edge(a,b)
gc=set(max(nx.connected_components(G),key=len))
# betweenness (sampled) + clustering on the giant component
GC=G.subgraph(gc).copy()
bet=nx.betweenness_centrality(GC,k=min(200,GC.number_of_nodes()),seed=11,normalized=True)
clu=nx.clustering(GC)
def band(c): return "hapax(1)" if c==1 else "rare(2-15)" if c<=15 else "mid(16-60)" if c<=60 else "common(61-300)" if c<=300 else "ubiq(>300)"
bands=["hapax(1)","rare(2-15)","mid(16-60)","common(61-300)","ubiq(>300)"]
agg=collections.defaultdict(lambda: {"n":0,"ingc":0,"bet":[],"clu":[],"deg":[]})
for r in cnt:
    b=band(cnt[r]); a=agg[b]; a["n"]+=1
    if r in gc:
        a["ingc"]+=1; a["bet"].append(bet[r]); a["clu"].append(clu[r]); a["deg"].append(GC.degree(r))
print(f"giant component: {len(gc)} of {len(cnt)} roots")
print(f"{'band':14s} {'#roots':>7} {'%in GC':>7} {'med betweenness':>16} {'med clustering':>15} {'med deg':>8}")
for b in bands:
    a=agg[b]
    if a["bet"]:
        print(f"{b:14s} {a['n']:7d} {100*a['ingc']/a['n']:6.0f}% {st.median(a['bet']):16.5f} {st.median(a['clu']):15.3f} {st.median(a['deg']):8.0f}")
    else:
        print(f"{b:14s} {a['n']:7d} {100*a['ingc']/a['n']:6.0f}% {'(mostly islands)':>16}")
print("\nReading: convection capacity = betweenness (carrying global paths); conduction = local clustering.")
# al-Kawthar roots
print("\nal-Kawthar roots:")
for r in [fa(x) for x in ['ربب','کثر','صلو','عطو','شنء','نحر','بتر']]:
    if r in gc: print(f"  {r} ({band(cnt[r])}): betweenness={bet[r]:.5f}, clustering={clu[r]:.2f}, deg={GC.degree(r)}")
    else: print(f"  {r} ({band(cnt[r])}): ISLAND (not in giant component)")
