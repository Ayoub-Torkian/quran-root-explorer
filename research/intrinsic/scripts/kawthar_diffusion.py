# -*- coding: utf-8 -*-
"""Cross-methodology batch (internal, ONE-LAW): (1) BURSTINESS B of root recurrences vs Poisson-shuffle null;
(2) DISTINCTIVENESS fingerprint of al-Kawthar's 7 roots across axes; (3) DEPENDENCY-graph diffusion proxy
(directed P(b|a), PageRank/influence) as internal 'spread'. Honest, null-anchored."""
import collections, math, itertools, random
import networkx as nx
random.seed(11)
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا')
rows=[]
for line in open(f"{R}/research/two_books_genome/roots_by_ayah.tsv",encoding='utf-8'):
    line=line.rstrip('\n')
    if '\t' in line: k,rs=line.split('\t',1); rows.append((k,[fa(x) for x in rs.split()]))
rows.sort(key=lambda kv:(int(kv[0].split(':')[0]),int(kv[0].split(':')[1])))
order={k:i for i,(k,_) in enumerate(rows)}            # canonical verse index
Nv=len(rows)
occ=collections.defaultdict(list)
for i,(k,rsr) in enumerate(rows):
    for r in set(rsr): occ[r].append(i)
cnt={r:len(occ[r]) for r in occ}

# ---- (1) BURSTINESS B = (sd-mean)/(sd+mean) of inter-occurrence gaps; >0 bursty, 0 Poisson ----
import statistics as st
def burst(positions):
    g=[positions[i+1]-positions[i] for i in range(len(positions)-1)]
    if len(g)<2: return None
    m=st.mean(g); s=st.pstdev(g)
    return (s-m)/(s+m) if (s+m)>0 else 0.0
recur=[r for r in occ if cnt[r]>=5]
Bobs=[b for r in recur if (b:=burst(occ[r])) is not None]
# null: place cnt[r] occurrences uniformly at random among Nv verses
def burst_null():
    out=[]
    for r in recur:
        pos=sorted(random.sample(range(Nv),cnt[r])); b=burst(pos)
        if b is not None: out.append(b)
    return out
Bnull=burst_null()
print("== (1) BURSTINESS ==")
print(f"recurring roots (>=5 occ): {len(recur)}")
print(f"median B observed = {st.median(Bobs):+.3f} ; null (Poisson-shuffle) median = {st.median(Bnull):+.3f}")
print(f"frac bursty (B>0): obs={100*sum(1 for b in Bobs if b>0)/len(Bobs):.0f}%  null={100*sum(1 for b in Bnull if b>0)/len(Bnull):.0f}%")

# ---- (2) co-occurrence + PPMI for centrality/distinctiveness ----
co=collections.Counter()
for k,rsr in rows:
    for a,b in itertools.combinations(sorted(set(rsr)),2): co[(a,b)]+=1
def pair(a,b): return co.get((a,b),0)+co.get((b,a),0)
def ppmi(a,b):
    c=pair(a,b); return max(0.0,math.log2(c*Nv/(cnt[a]*cnt[b]))) if c>0 else 0.0
def maxppmi(r): return max((ppmi(r,o) for o in cnt if o!=r and pair(r,o)>0),default=0.0)
rootsuras=collections.defaultdict(set)
for k,rsr in rows:
    s=int(k.split(':')[0])
    for r in rsr: rootsuras[r].add(s)
spread={r:len(rootsuras[r]) for r in rootsuras}
def pctile(val, arr): return 100*sum(1 for x in arr if x<val)/len(arr)
allcnt=list(cnt.values()); allspread=list(spread.values()); allmax=[maxppmi(r) for r in list(cnt)[:0]] # skip heavy
KW=[fa(x) for x in ['عطو','کثر','صلو','ربب','نحر','شنء','بتر']]
print("\n== (2) DISTINCTIVENESS FINGERPRINT of al-Kawthar's 7 roots (percentile in corpus; low rarity-pct = rarer) ==")
print("root | count(pct) | spread(pct) | maxPPMI | burstiness B")
Bmap={r:burst(occ[r]) for r in KW if cnt[r]>=5}
for r in KW:
    print(f"  {r}: cnt={cnt[r]}(p{pctile(cnt[r],allcnt):.0f}) spread={spread[r]}(p{pctile(spread[r],allspread):.0f}) maxPPMI={maxppmi(r):.1f} B={Bmap.get(r,'n/a (rare)')}")

# ---- (3) DEPENDENCY-graph diffusion proxy: directed P(b|a), PageRank (influence sink) ----
D=nx.DiGraph()
common=[r for r in cnt if cnt[r]>=3]
for a in common:
    for b in common:
        if a!=b and pair(a,b)>0:
            w=pair(a,b)/cnt[a]                      # P(b|a): a depends on/points to b
            if w>=0.25: D.add_edge(a,b,weight=w)
def pagerank_manual(G,d=0.85,it=100):
    N=G.number_of_nodes(); pr={n:1.0/N for n in G}
    outw={n:sum(G[n][m]['weight'] for m in G.successors(n)) or 1.0 for n in G}
    for _ in range(it):
        nw={n:(1-d)/N for n in G}
        for n in G:
            for m in G.successors(n): nw[m]+=d*pr[n]*G[n][m]['weight']/outw[n]
        pr=nw
    return pr
pr=pagerank_manual(D) if D.number_of_nodes() else {}
top=sorted(pr,key=lambda r:-pr[r])[:10]
print("\n== (3) DEPENDENCY DIFFUSION (directed P(b|a)>=0.25), PageRank top sinks ==")
print("  top-PageRank roots (everything 'flows to' these):", [(r,round(pr[r],4)) for r in top])
for r in KW:
    if r in D: print(f"  {r}: PageRank={pr.get(r,0):.4f}, out-deg={D.out_degree(r)}, in-deg={D.in_degree(r)}, reach={len(nx.descendants(D,r))}")
    else: print(f"  {r}: not in dependency graph (too rare, cnt={cnt[r]})")
