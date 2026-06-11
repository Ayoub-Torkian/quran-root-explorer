#!/usr/bin/env python3
# FRESH PROBE — is the ORDER of the 114 sūras determined? Are adjacent sūras more lexically
# similar (shared roots) than under a shuffle of sūra order? Two views:
# (A) whole-sūra root-bag Jaccard between neighbours; (B) edge handoff: last 8 verses of sūra k
# vs first 8 of sūra k+1. Null: shuffle sūra order.
import glob,numpy as np,collections
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:k,r=ln.rstrip('\n').split('\t',1);roots[k]=set(x for x in r.split() if x and x!='NA')
bys=collections.defaultdict(list)
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,_=ln.split('\t',1);bys[int(sa.split(':')[0])].append(roots.get(sa.strip(),set()))
S=sorted(bys)
bag={s:set().union(*bys[s]) for s in S}
head={s:set().union(*bys[s][:8]) for s in S}
tail={s:set().union(*bys[s][-8:]) for s in S}
def jac(a,b):
    u=a|b;return len(a&b)/len(u) if u else 0
def adj_bag(order):
    return np.mean([jac(bag[order[i]],bag[order[i+1]]) for i in range(len(order)-1)])
def adj_edge(order):
    return np.mean([jac(tail[order[i]],head[order[i+1]]) for i in range(len(order)-1)])
rng=np.random.default_rng(7)
realA=adj_bag(S);realB=adj_edge(S)
flA=[];flB=[]
for _ in range(2000):
    p=list(rng.permutation(S));flA.append(adj_bag(p));flB.append(adj_edge(p))
flA=np.array(flA);flB=np.array(flB)
print("(A) whole-sūra neighbour Jaccard: canonical %.3f vs shuffled-order %.3f ± %.3f  z=%+.1f  (perm p: %d/2000 >= real)"
      % (realA,flA.mean(),flA.std(),(realA-flA.mean())/flA.std(),int((flA>=realA).sum())))
print("(B) edge handoff (tail8→head8):   canonical %.3f vs shuffled-order %.3f ± %.3f  z=%+.1f  (perm p: %d/2000 >= real)"
      % (realB,flB.mean(),flB.std(),(realB-flB.mean())/flB.std(),int((flB>=realB).sum())))
