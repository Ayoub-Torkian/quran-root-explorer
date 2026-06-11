#!/usr/bin/env python3
# O9 integration (one body, small-world), O10 organ-systems (sura groups cluster), O11 necessity (irreplaceable).
import collections, random
import numpy as np
random.seed(1); np.random.seed(1)
RBA="research/two_books_genome/roots_by_ayah.tsv"
sur=collections.defaultdict(collections.Counter)
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:
        k,r=ln.rstrip('\n').split('\t',1); s=int(k.split(':')[0])
        if 1<=s<=114:
            for x in r.split():
                if x and x!='NA': sur[s][x]+=1
suras=sorted(sur); S=len(suras); idx={s:i for i,s in enumerate(suras)}
df=collections.Counter()
for s in suras:
    for r in sur[s]: df[r]+=1
rare=[r for r,d in df.items() if 2<=d<=60]
M=np.zeros((S,S))
for r in rare:
    h=[idx[s] for s in suras if r in sur[s]]
    for a in range(len(h)):
        for b in range(a+1,len(h)): M[h[a],h[b]]+=1; M[h[b],h[a]]+=1
dg=M.sum(1)+1e-9; A=M/np.sqrt(np.outer(dg,dg))
print("O9 · INTEGRATION — one connected body + small-world?")
try:
    import networkx as nx
    G=nx.Graph((suras[i],suras[j]) for i in range(S) for j in range(i+1,S) if M[i,j]>0)
    cc=nx.number_connected_components(G); C=nx.average_clustering(G); L=nx.average_shortest_path_length(G) if cc==1 else float('nan')
    m=G.number_of_edges()
    Cr=[];Lr=[]
    for _ in range(20):
        R=nx.gnm_random_graph(S,m)
        Cr.append(nx.average_clustering(R)); 
        if nx.is_connected(R): Lr.append(nx.average_shortest_path_length(R))
    sigma=(C/np.mean(Cr))/(L/np.mean(Lr))
    print(f"   components={cc} (1 = one body); clustering C={C:.2f} vs random {np.mean(Cr):.2f}; path L={L:.2f} vs random {np.mean(Lr):.2f}")
    print(f"   small-world sigma={sigma:.1f}  ({'SMALL-WORLD (integrated like a body: clustered + short paths)' if sigma>1.5 else 'not small-world'})")
except Exception as e:
    print("   networkx unavailable:",e)

print("\nO10 · ORGAN SYSTEMS — do known sura-groups cluster (a 'system' of organs)?")
def group_z(members,label):
    mi=[idx[s] for s in members if s in idx]
    within=np.mean([A[i,j] for a,i in enumerate(mi) for j in mi[a+1:]])
    nul=[]
    for _ in range(2000):
        g=random.sample(range(S),len(mi)); nul.append(np.mean([A[g[a],g[b]] for a in range(len(g)) for b in range(a+1,len(g))]))
    z=(within-np.mean(nul))/np.std(nul)
    print(f"   {label} (suras {members}): within-assoc {within:.3f} vs random group {np.mean(nul):.3f}  z={z:+.1f}  {'CLUSTERS' if z>2 else 'no'}")
group_z(list(range(40,47)),"Ḥawāmīm (حم openings)")
group_z(list(range(2,10)),"Al-Ṭiwāl (7 long)")
group_z([57,59,61,62,64],"Musabbiḥāt (partial)")

print("\nO11 · NECESSITY — each organ irreplaceable (unique function lost on removal)?")
rs2=collections.defaultdict(set)
for s in suras:
    for r in sur[s]: rs2[r].add(s)
uniq=collections.Counter()
for r,ss in rs2.items():
    if len(ss)==1: uniq[next(iter(ss))]+=1
have=sum(1 for s in suras if uniq[s]>0)
print(f"   {have}/{S} suras carry >=1 IRREPLACEABLE root (found in no other sura) -> removing them deletes a function")
nomark=[s for s in suras if uniq[s]==0]
print(f"   {len(nomark)} suras have NO unique root: {nomark[:15]}{'...' if len(nomark)>15 else ''}")
print(f"   (those are mostly short/late; their necessity is the unique COMBINATION, not a unique root — to test separately)")
