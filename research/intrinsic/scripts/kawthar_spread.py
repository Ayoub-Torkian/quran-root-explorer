# -*- coding: utf-8 -*-
"""SPREAD-OF-MESSAGE: independent-cascade (IC) diffusion on directed conditional graph a->b=P(b|a).
Reach = fraction of lexicon activated from a seed. Null = out-degree-preserving rewire."""
import collections, random, itertools, statistics as st
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
def pair(a,b): return co.get((a,b),0)+co.get((b,a),0)
nodes=[r for r in cnt if cnt[r]>=5]; Nn=len(nodes)
adj=collections.defaultdict(list)
for a in nodes:
    for b in nodes:
        if a!=b and pair(a,b)>0:
            p=pair(a,b)/cnt[a]
            if p>=0.15: adj[a].append((b,min(p,0.9)))
def IC(seed,A,sims=50):
    if seed not in nodes: return 0.0
    tot=0
    for _ in range(sims):
        act={seed}; frontier=[seed]
        while frontier:
            nf=[]
            for a in frontier:
                for b,p in A.get(a,[]):
                    if b not in act and random.random()<p: act.add(b); nf.append(b)
            frontier=nf
        tot+=len(act)
    return tot/sims/Nn
def rewire(A):
    tg=[b for a in nodes for (b,p) in A.get(a,[])]; pr=[p for a in nodes for (b,p) in A.get(a,[])]
    random.shuffle(tg); out=collections.defaultdict(list); i=0
    for a in nodes:
        for _ in range(len(A.get(a,[]))): out[a].append((tg[i],pr[i])); i+=1
    return out
print(f"nodes(count>=5)={Nn}, edges={sum(len(v) for v in adj.values())}")
allreach={s:IC(s,adj,40) for s in nodes}
vals=sorted(allreach.values())
print(f"IC message-reach: median={st.median(vals):.3f} mean={st.mean(vals):.3f} p90={vals[int(.9*len(vals))]:.3f} max={max(vals):.3f}")
top=sorted(allreach,key=lambda s:-allreach[s])[:10]
print("super-spreaders:", [(s,round(allreach[s],3)) for s in top])
def pct(v): return 100*sum(1 for x in vals if x<v)/len(vals)
KW=[fa(x) for x in ['عطو','کثر','صلو','ربب','نحر','شنء','بتر']]
print("\nal-Kawthar roots' message-reach:")
for r in KW:
    if r in nodes: print(f"  {r}: reach={allreach[r]:.3f} (pct {pct(allreach[r]):.0f}), out-deg={len(adj.get(r,[]))}")
    else: print(f"  {r}: island (count={cnt[r]}) -> reach 0")
Anull=rewire(adj)
print("\nNULL (rewired) vs observed reach:")
for r in [x for x in KW if x in nodes]:
    nr=st.mean([IC(r,rewire(adj),25) for _ in range(4)])
    print(f"  {r}: observed {allreach[r]:.3f} vs null {nr:.3f}")
