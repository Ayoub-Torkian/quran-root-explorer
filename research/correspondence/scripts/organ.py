#!/usr/bin/env python3
# SURA-as-ORGAN: each sura = a distinct, non-redundant FUNCTION in the corpus-body (relational, scale-invariant).
# Function signature = keyness (log-odds vs corpus) of its roots. Test distinctiveness + canonical vs random cuts.
import collections, math, random
import numpy as np
random.seed(1); np.random.seed(1)
RBA="research/two_books_genome/roots_by_ayah.tsv"
verses=[]  # ordered: (sura, [roots])
for ln in open(RBA,encoding='utf-8'):
    if '\t' not in ln: continue
    k,r=ln.rstrip('\n').split('\t',1); s=int(k.split(':')[0])
    verses.append((s,[x for x in r.split() if x and x!='NA']))
allroots=[r for _,rs in verses for r in rs]
corp=collections.Counter(allroots); CT=sum(corp.values())
vocab={r:i for i,r in enumerate(corp)}; Vn=len(vocab)
def sig(groot):   # keyness vector for a group's root multiset
    n=sum(groot.values()); v=np.zeros(Vn)
    for r,c in groot.items():
        exp=n*corp[r]/CT
        v[vocab[r]]=math.log((c+0.3)/(exp+0.3))   # enriched(+)/depleted(-)
    return v
def groups_to_sigs(groups):
    S=np.zeros((len(groups),Vn))
    for i,g in enumerate(groups):
        gc=collections.Counter(r for vi in g for r in verses[vi][1]); S[i]=sig(gc)
    nrm=np.linalg.norm(S,axis=1,keepdims=True)+1e-9
    return S/nrm
def mean_nearest(S):   # each organ's max cosine sim to ANY other organ (redundancy); lower=more non-redundant
    C=S@S.T; np.fill_diagonal(C,-9); return C.max(1)
# canonical partition
canon=collections.defaultdict(list)
for vi,(s,_) in enumerate(verses): canon[s].append(vi)
suras=sorted(canon); cg=[canon[s] for s in suras]
sizes=[len(g) for g in cg]
Sc=groups_to_sigs(cg); nn=mean_nearest(Sc)
print(f"CANONICAL 114 organs: mean nearest-organ similarity = {nn.mean():.3f}  (lower = each more unique)")
print(f"  every organ distinct? max nearest-sim = {nn.max():.3f}  (most-redundant pair)")
# Kawthar (108) specifically
ki=suras.index(108)
sim108=(Sc@Sc[ki]); sim108[ki]=-9
print(f"  KAWTHAR (108, {sizes[ki]} verses): nearest organ sim = {sim108.max():.3f} -> sura {suras[int(sim108.argmax())]}")
uniq=[r for r in set(r for vi in cg[ki] for r in verses[vi][1]) if corp[r]<=2]
print(f"  Kawthar carries {len(uniq)} near-unique roots (<=2x in corpus): {uniq[:8]}")
# NULL: random contiguous partition with SAME size multiset
nulls=[]
for _ in range(120):
    sz=sizes[:]; random.shuffle(sz)
    gs=[]; idx=0
    for z in sz: gs.append(list(range(idx,idx+z))); idx+=z
    nulls.append(mean_nearest(groups_to_sigs(gs)).mean())
nulls=np.array(nulls)
z=(nn.mean()-nulls.mean())/nulls.std()
print(f"\nCANONICAL mean nearest-sim {nn.mean():.3f}  vs RANDOM same-size cuts {nulls.mean():.3f}±{nulls.std():.3f}  z={z:+.1f}")
print(f"  => canonical organs are {'MORE' if nn.mean()<nulls.mean() else 'LESS'} non-redundant than arbitrary cuts (negative z = more distinct)")
