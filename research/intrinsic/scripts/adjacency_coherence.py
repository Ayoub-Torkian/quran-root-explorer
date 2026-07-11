# -*- coding: utf-8 -*-
"""Pre-registered: does CANONICAL muṣḥaf-adjacency cohere in the closing block (suras 90-114)?
idf-weighted root vectors (rasm) -> cosine(n,n+1); permutation null over the 25 suras' ORDER;
revelation-order comparator; per-pair ranking incl. al-Kawthar (107-108, 108-109). MEASURED."""
import openpyxl, math, random
from collections import defaultdict, Counter
random.seed(17)
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
wb=openpyxl.load_workbook(R+"/Book6.xlsx", read_only=True, data_only=True); ws=wb.active
sura_roots=defaultdict(Counter)          # sura -> Counter(root)
sura_nuzul={}
for r in ws.iter_rows(min_row=9, values_only=True):
    try:
        s=int(r[5])
    except (TypeError,ValueError):
        continue
    roots=str(r[8] or "").split()
    sura_roots[s].update(roots)
    if r[12] is not None: sura_nuzul[s]=int(r[12])
# corpus df per root (document = sura, 114 docs)
df=Counter()
for s,c in sura_roots.items():
    for rt in c: df[rt]+=1
Nsuras=len(sura_roots)
idf={rt: math.log((Nsuras+1)/(df[rt]+1))+1 for rt in df}
def vec(s):
    return {rt: cnt*idf[rt] for rt,cnt in sura_roots[s].items()}
def cos(a,b):
    common=set(a)&set(b)
    num=sum(a[k]*b[k] for k in common)
    na=math.sqrt(sum(v*v for v in a.values())); nb=math.sqrt(sum(v*v for v in b.values()))
    return num/(na*nb) if na and nb else 0.0
BLOCK=list(range(90,115))                 # 90..114 inclusive (25 suras)
V={s:vec(s) for s in BLOCK}
def mean_adj(order):
    return sum(cos(V[order[i]],V[order[i+1]]) for i in range(len(order)-1))/(len(order)-1)
obs=mean_adj(BLOCK)
# permutation null over ORDER of the 25 suras
NPERM=5000; nulls=[]
for _ in range(NPERM):
    o=BLOCK[:]; random.shuffle(o); nulls.append(mean_adj(o))
mu=sum(nulls)/NPERM; sd=(sum((x-mu)**2 for x in nulls)/NPERM)**0.5
z=(obs-mu)/sd if sd else 0.0
pct=100*sum(1 for x in nulls if x<obs)/NPERM
# revelation-order comparator (same 25 suras, ordered by nuzul)
rev=sorted(BLOCK, key=lambda s: sura_nuzul.get(s,9999))
obs_rev=mean_adj(rev)
# per-pair ranking among ALL C(25,2) pairs
pairs=[]
for i in range(len(BLOCK)):
    for j in range(i+1,len(BLOCK)):
        pairs.append(((BLOCK[i],BLOCK[j]), cos(V[BLOCK[i]],V[BLOCK[j]])))
pairs.sort(key=lambda x:-x[1])
rank={p:r+1 for r,(p,_) in enumerate(pairs)}
NP=len(pairs)
def pair_line(a,b):
    p=(a,b) if (a,b) in rank else (b,a)
    return f"  {a}-{b}: cos={dict(pairs)[p]:.3f}  rank {rank[p]}/{NP} (top {100*rank[p]/NP:.0f}%)"
# adjacency z per consecutive pair vs the all-pairs distribution
allv=[v for _,v in pairs]; amu=sum(allv)/NP; asd=(sum((x-amu)**2 for x in allv)/NP)**0.5
print("=== CANONICAL adjacency coherence, suras 90-114 (idf-weighted rasm roots) ===")
print(f"observed mean adj cosine = {obs:.4f}")
print(f"permutation null (order shuffled, {NPERM}x): mean {mu:.4f} sd {sd:.4f}")
print(f"  -> z = {z:+.2f} , percentile {pct:.1f}")
print(f"revelation-order mean adj cosine = {obs_rev:.4f}  (canonical {'>' if obs>obs_rev else '<='} revelation)")
print(f"all-pairs cosine: mean {amu:.3f} sd {asd:.3f}")
print("=== al-Kawthar neighbourhood ===")
print(pair_line(107,108)); print(pair_line(108,109))
print("=== top 6 adjacent (consecutive) pairs by coherence ===")
adj=sorted([((BLOCK[i],BLOCK[i+1]),cos(V[BLOCK[i]],V[BLOCK[i+1]])) for i in range(len(BLOCK)-1)],key=lambda x:-x[1])
for (a,b),c in adj[:6]: print(f"  {a}-{b}: {c:.3f} (z vs all-pairs {(c-amu)/asd:+.2f})")
print("=== weakest 3 adjacent pairs ===")
for (a,b),c in adj[-3:]: print(f"  {a}-{b}: {c:.3f}")
