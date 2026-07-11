# -*- coding: utf-8 -*-
"""RARITY-PURE hapax graph: drop ubiquitous roots from context (df>UBIQ), weight remaining shared context by idf,
keep only rarity-driven edges -> real communities. + positional profile vs revelation_order. No ubiquitous conflation."""
import collections, math, csv, itertools
import networkx as nx
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا')
vr={}
for line in open(f"{R}/research/two_books_genome/roots_by_ayah.tsv",encoding='utf-8'):
    line=line.rstrip('\n')
    if '\t' in line: k,rs=line.split('\t',1); vr[k]=[fa(x) for x in rs.split()]
Nv=len(vr)
df=collections.Counter()                       # verses-per-root
for rs in vr.values():
    for r in set(rs): df[r]+=1
cnt=collections.Counter(r for rs in vr.values() for r in rs)
idf=lambda r: math.log(Nv/df[r])
hapax={r for r,c in cnt.items() if c==1}
UBIQ=150                                        # roots in >150 verses are 'ubiquitous' -> excluded from context
ubiq={r for r in df if df[r]>UBIQ}
print(f"hapax={len(hapax)}  ubiquitous(df>{UBIQ})={len(ubiq)} (excluded from context), e.g.", sorted(ubiq,key=lambda r:-df[r])[:8])
host={r:k for k,rs in vr.items() for r in rs if r in hapax}
# rarity-only context per hapax: drop self-hapax AND ubiquitous roots
ctx={h:set(r for r in vr[host[h]] if r not in ubiq and r not in hapax) for h in hapax}
THRESH=6.0                                      # edge kept if shared-context idf-sum >= ~one root in <=15 verses
G=nx.Graph()
G.add_nodes_from(hapax)
for h1,h2 in itertools.combinations(hapax,2):
    sh=ctx[h1]&ctx[h2]
    if sh:
        w=sum(idf(r) for r in sh)
        if w>=THRESH: G.add_edge(h1,h2,w=round(w,1),via=' '.join(sorted(sh,key=lambda r:-idf(r))[:3]))
nz=[n for n in G if G.degree(n)>0]
print(f"\nRARITY-PURE graph (thresh idf-sum>={THRESH}): {len(nz)}/{len(hapax)} hapax connected, {G.number_of_edges()} edges")
comps=sorted([c for c in nx.connected_components(G) if len(c)>1],key=len,reverse=True)
print(f"components(>1): {len(comps)}; sizes: {[len(c) for c in comps[:12]]}")
# community detection on the largest pieces
try:
    comm=list(nx.community.greedy_modularity_communities(G.subgraph(nz),weight='w'))
    print(f"greedy-modularity communities: {len(comm)}; sizes: {sorted([len(c) for c in comm],reverse=True)[:10]}")
except Exception as e: print("comm err",e); comm=comps
# show a few example clusters with the rare root that binds them
print("\nexample rarity clusters (hapax — bound by shared RARE context):")
for c in sorted(comps,key=len,reverse=True)[:5]:
    cl=list(c)
    # find a representative shared rare root among edges in this component
    edges=[(u,v,G[u][v]['via']) for u,v in itertools.combinations(cl,2) if G.has_edge(u,v)]
    via=collections.Counter(w for _,_,vv in edges for w in vv.split())
    print(f"  size {len(cl)}: {cl[:7]}  | bound via: {[w for w,_ in via.most_common(3)]}")
for h in [fa('نحر'),fa('بتر')]:
    print(f"  {h}: degree {G.degree(h)}", "neighbors "+str([ (n,G[h][n]['via']) for n in list(G.neighbors(h))[:4]]) if G.degree(h)>0 else "(isolated under rarity)")

# ---- POSITIONAL: hapax density vs revelation order ----
prof={}
for row in csv.DictReader(open(f"{R}/exports/surah_profile.csv",encoding='utf-8-sig')):
    try: prof[int(row['surah'])]={'rev':int(row['revelation_order']),'hpct':float(row['pct_unique_roots_hapax']),'nay':int(row['n_ayahs'])}
    except: pass
import statistics as st
xs=[prof[s]['rev'] for s in prof]; ys=[prof[s]['hpct'] for s in prof]
# spearman
def spearman(a,b):
    ra={v:i for i,v in enumerate(sorted(range(len(a)),key=lambda i:a[i]))}
    rb={v:i for i,v in enumerate(sorted(range(len(b)),key=lambda i:b[i]))}
    da=[ra[i] for i in range(len(a))]; db=[rb[i] for i in range(len(b))]
    n=len(a); d2=sum((da[i]-db[i])**2 for i in range(n)); return 1-6*d2/(n*(n*n-1))
print(f"\nPOSITIONAL: Spearman(revelation_order, hapax%) = {spearman(xs,ys):+.2f}  (negative = earlier-revealed are MORE hapax-dense)")
early=[prof[s]['hpct'] for s in prof if prof[s]['rev']<=45]; late=[prof[s]['hpct'] for s in prof if prof[s]['rev']>45]
print(f"  mean hapax%: first-45-revealed={st.mean(early):.1f}%  vs  rest={st.mean(late):.1f}%")
print(f"  al-Kawthar: revelation #{prof[108]['rev']}, hapax%={prof[108]['hpct']:.0f}")
