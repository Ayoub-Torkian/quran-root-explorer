#!/usr/bin/env python3
# Which suras play HEART (central pump), BRAIN (integrative router), LEG (peripheral limb)?
# Derived intrinsically from the inter-sura connectome (shared rare roots).
import collections
import numpy as np
RBA="research/two_books_genome/roots_by_ayah.tsv"
sur=collections.defaultdict(collections.Counter)
for ln in open(RBA,encoding='utf-8'):
    if '\t' not in ln: continue
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
deg=M.sum(1)+1e-9
A=M/np.sqrt(np.outer(deg,deg))          # size-normalized association
np.fill_diagonal(A,0)
NAME={1:"Fatiha",2:"Baqara",3:"Al-Imran",4:"Nisa",5:"Ma'ida",6:"An'am",9:"Tawba",24:"Nur",
 36:"YaSin",55:"Rahman",112:"Ikhlas",113:"Falaq",114:"Nas",108:"Kawthar",110:"Nasr",1:"Fatiha"}
nm=lambda i: f"{suras[i]} {NAME.get(suras[i],'')}".strip()
# eigenvector centrality (power iteration on A) -> HEART (central pump)
v=np.ones(S)
for _ in range(200): v=A@v; v/=np.linalg.norm(v)+1e-12
# information/integration -> BRAIN: high unique-marker load AND high connectivity
uniq=collections.Counter()
rs2={}
for s in suras:
    for r in sur[s]: rs2.setdefault(r,[]).append(s)
for r,ss in rs2.items():
    if len(ss)==1: uniq[ss[0]]+=1
umark=np.array([uniq[s] for s in suras],float); umark/=umark.max()+1e-9
brain=v*0.5+umark*0.5
try:
    import networkx as nx
    G=nx.from_numpy_array(A); bet=nx.betweenness_centrality(G,weight='weight',normalized=True)
    betv=np.array([bet[i] for i in range(S)])
except Exception as e:
    betv=v.copy()
def top(x,k=5,rev=True): 
    o=np.argsort(x); o=o[::-1] if rev else o; return [nm(i) for i in o[:k]]
print("HEART  — central pump (eigenvector centrality, most-connected-to-the-well-connected):")
print("   ", top(v))
print("BRAIN  — integrative router (betweenness: controls flow between regions):")
print("   ", top(betv))
print("BRAIN' — information core (unique markers + centrality):")
print("   ", top(brain))
print("LEG/LIMB — peripheral, specialized (lowest centrality):")
print("   ", top(v,6,rev=False))
