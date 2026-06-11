#!/usr/bin/env python3
# RESOLUTION-FREE organ test: is each sura denser INSIDE than ACROSS its boundary? (community, any size)
import collections, random
import numpy as np
random.seed(1)
RBA="research/two_books_genome/roots_by_ayah.tsv"
verses=[]
for ln in open(RBA,encoding='utf-8'):
    if '\t' not in ln: continue
    k,r=ln.rstrip('\n').split('\t',1); s=int(k.split(':')[0])
    verses.append((s,[x for x in r.split() if x and x!='NA']))
Nv=len(verses)
df=collections.Counter()
for _,rs in verses:
    for r in set(rs): df[r]+=1
LO,HI=2,80
vrare=[set(x for x in rs if LO<=df[x]<=HI) for _,rs in verses]
def ratios(comm):
    by=collections.defaultdict(list)
    for i,c in enumerate(comm): by[c].append(i)
    out=[]
    for c,vs in by.items():
        size=len(vs)
        if size<2: out.append((c,size,np.nan)); continue
        cnt=collections.Counter()
        for i in vs:
            for r in vrare[i]: cnt[r]+=1
        Win=sum(n*(n-1)//2 for n in cnt.values())
        Wout=sum(n*(df[r]-n) for r,n in cnt.items())
        din=Win/(size*(size-1)/2)
        dout=Wout/(size*(Nv-size)) if size<Nv else np.nan
        out.append((c,size,(din/dout) if dout>0 else np.inf))
    return out
comm=[s for s,_ in verses]
R=ratios(comm)
rv=np.array([r for _,_,r in R if np.isfinite(r)])
print(f"CANONICAL: {len(rv)} suras with finite ratio; median d_in/d_out = {np.median(rv):.1f}")
print(f"  fraction denser-inside (ratio>1) = {(rv>1).mean():.0%}   (organ = denser inside than across boundary)")
print(f"  fraction ratio>3 = {(rv>3).mean():.0%}   ratio>10 = {(rv>10).mean():.0%}")
# small suras incl Kawthar
first={}
for i,(s,_) in enumerate(verses): first.setdefault(s,i)
by=collections.defaultdict(list)
for i,(s,_) in enumerate(verses): by[s].append(i)
Rd={c:r for c,sz,r in R}
for sx in [108,103,110,112,114,1,113]:
    print(f"  sura {sx} (size {len(by[sx])}): d_in/d_out = {Rd.get(sx,float('nan')):.1f}")
# random same-size contiguous null
order_sizes=[]; cur=None;c=0
for s,_ in verses:
    if s!=cur:
        if cur is not None: order_sizes.append(c)
        cur=s;c=1
    else:c+=1
order_sizes.append(c)
meds=[]; fr=[]
for _ in range(60):
    sz=order_sizes[:]; random.shuffle(sz); cm=[]; ci=0
    for z in sz: cm+=[ci]*z; ci+=1
    rr=np.array([r for _,_,r in ratios(cm) if np.isfinite(r)])
    meds.append(np.median(rr)); fr.append((rr>1).mean())
print(f"\nRANDOM same-size cuts: median ratio {np.mean(meds):.1f}±{np.std(meds):.1f}; frac>1 {np.mean(fr):.0%}")
print(f"CANONICAL median {np.median(rv):.1f} vs random {np.mean(meds):.1f}  -> z={(np.median(rv)-np.mean(meds))/np.std(meds):+.1f}")
