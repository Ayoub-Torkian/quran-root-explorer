# -*- coding: utf-8 -*-
"""k=1 floor: is hapax DENSITY uniform or clustered? + the hapax graph (intra-verse co-occ; inter via shared context).
All density-normalized. Pre-registered: dispersion>1 (vs Poisson)=clustered; surah a 'hotspot' if density>95th of a
random-relocation null. Graph edge = host verses share a non-hapax context root (normalized)."""
import collections, random, statistics as st, itertools
random.seed(11)
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا')
vr={}
for line in open(f"{R}/research/two_books_genome/roots_by_ayah.tsv",encoding='utf-8'):
    line=line.rstrip('\n')
    if '\t' in line: k,rs=line.split('\t',1); vr[k]=[fa(x) for x in rs.split()]
cnt=collections.Counter(); rootsuras=collections.defaultdict(set)
for k,rs in vr.items():
    s=int(k.split(':')[0])
    for r in rs: cnt[r]+=1; rootsuras[r].add(s)
hapax={r for r,c in cnt.items() if c==1}              # count==1 (408)
spread1={r for r in cnt if len(rootsuras[r])==1}      # one-sura (476)
print("count==1 (true hapax):",len(hapax)," | spread==1 sura:",len(spread1)," | repeaters-in-one-sura:",len(spread1-hapax))
print("examples of the 68 (repeat>=2 but one sura):",[(r,cnt[r]) for r in list(spread1-hapax)[:6]])

# ---- DENSITY per verse & dispersion (uniform vs clustered) ----
hpv=[sum(1 for r in rs if r in hapax) for rs in vr.values()]
mean=st.mean(hpv); var=st.pvariance(hpv); disp=var/mean
print(f"\nhapax/verse: mean={mean:.3f} var={var:.3f}  index-of-dispersion={disp:.2f}  ({'CLUSTERED (>1)' if disp>1.15 else 'Poisson-like'})")
multi=sum(1 for h in hpv if h>=2); print(f"verses with >=2 hapax: {multi}  (Poisson expectation ~{len(hpv)*(mean**2/2)* (2.718**-mean):.0f})")

# ---- per-sura DENSITY + relocation null -> which suras are hotspots ----
sura_v=collections.defaultdict(list)
for k,rs in vr.items(): sura_v[int(k.split(':')[0])].append(rs)
def dens(s): 
    vs=sura_v[s]; return sum(1 for rs in vs for r in rs if r in hapax)/len(vs)
obs={s:dens(s) for s in sura_v}
# null: relocate each hapax to a random verse (preserve verse count & sizes approx) -> recompute per-sura density
allk=list(vr); vlen={k:len(vr[k]) for k in allk}
def null_density_dist(nsim=600):
    per_sura=collections.defaultdict(list)
    for _ in range(nsim):
        # throw len(hapax) hapax-hits into random verses (weighted by verse length)
        hits=collections.Counter(random.choices(allk, weights=[vlen[k] for k in allk], k=len(hapax)))
        d=collections.Counter()
        for k,h in hits.items(): d[int(k.split(':')[0])]+=h
        for s in sura_v: per_sura[s].append(d[s]/len(sura_v[s]))
    return per_sura
nd=null_density_dist()
hot=[s for s in sura_v if 100*sum(1 for x in nd[s] if x<obs[s])/len(nd[s])>=95]
print(f"\nhapax-density HOTSPOTS (>95th pct of relocation null): {len(hot)} suras")
print("  top by density:", [(s,round(obs[s],2)) for s in sorted(hot,key=lambda s:-obs[s])[:12]])
print(f"  al-Kawthar(108) density={obs[108]:.2f}, hotspot={108 in hot}")
# clustering of hapax across suras: Gini of per-sura hapax counts vs null
def gini(x):
    x=sorted(x); n=len(x); cum=sum((i+1)*v for i,v in enumerate(x)); 
    return (2*cum)/(n*sum(x)) - (n+1)/n if sum(x)>0 else 0
obs_counts=[sum(1 for rs in sura_v[s] for r in rs if r in hapax) for s in sura_v]
print(f"  Gini of hapax-per-sura (raw): {gini(obs_counts):.2f}  (higher=more concentrated)")

# ---- HAPAX GRAPH ----
# host verse of each hapax
host={}
for k,rs in vr.items():
    for r in rs:
        if r in hapax: host[r]=k
# (a) intra-verse co-occurrence: hapax sharing a verse
byverse=collections.defaultdict(list)
for h,k in host.items(): byverse[k].append(h)
cooc=[v for v in byverse.values() if len(v)>=2]
print(f"\nINTRA-verse: {len(cooc)} verses host >=2 hapax (direct hapax-hapax co-occurrence edges)")
# (b) context graph: edge if host verses share a NON-hapax content root
import networkx as nx
G=nx.Graph()
hl=list(hapax); 
ctx={h:set(r for r in vr[host[h]] if r not in hapax) for h in hl}
for h1,h2 in itertools.combinations(hl,2):
    sh=ctx[h1]&ctx[h2]
    if len(sh)>=2:  # share >=2 context roots (normalized threshold)
        G.add_edge(h1,h2,w=len(sh))
print(f"CONTEXT graph: {G.number_of_nodes()} hapax nodes, {G.number_of_edges()} edges (share>=2 context roots)")
comps=sorted(nx.connected_components(G),key=len,reverse=True)
print(f"  connected components: {len(comps)}; largest sizes: {[len(c) for c in comps[:6]]}")
# al-Kawthar hapax in graph?
for h in [fa('نحر'),fa('بتر')]:
    if h in G: print(f"  {h}: degree {G.degree(h)}, neighbors {list(G.neighbors(h))[:6]}")
    else: print(f"  {h}: isolated (no shared-context neighbors)")
