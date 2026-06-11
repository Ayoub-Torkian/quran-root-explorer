#!/usr/bin/env python3
# FRESH PROBE — spacing regularity / refrain structure. For each frequent root, is its sequence
# of inter-occurrence GAPS unusually REGULAR (low coefficient of variation, CV) — a refrain —
# or bursty (CV>1, clustered)? Null: shuffle that root's occurrence slots (keeps its count).
import glob,numpy as np
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
seq=[]
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:
        k,r=ln.rstrip('\n').split('\t',1);seq.append([x for x in r.split() if x and x!='NA'])
N=len(seq)
from collections import defaultdict
posof=defaultdict(list)
for i,rs in enumerate(seq):
    for r in set(rs):posof[r].append(i)
def cv(positions):
    g=np.diff(positions)
    return g.std()/g.mean() if len(g)>1 and g.mean()>0 else None
rng=np.random.default_rng(3)
reg=[];burst=[];rows=[]
for r,ps in posof.items():
    c=len(ps)
    if c<25:continue
    realcv=cv(ps)
    # null: place c occurrences at random slots, 200x
    fl=[cv(sorted(rng.choice(N,c,replace=False))) for _ in range(200)]
    fl=np.array([x for x in fl if x is not None]); z=(realcv-fl.mean())/(fl.std()+1e-9)
    rows.append((r,c,realcv,fl.mean(),z))
    if z<-3:reg.append(r)
    if z>3:burst.append(r)
rows.sort(key=lambda x:x[4])
print("frequent roots tested (count>=25): %d" % len(rows))
print("significantly REGULAR (refrain-like, CV below random, z<-3): %d" % len(reg))
print("significantly BURSTY (clustered, z>3): %d" % len(burst))
print("\nmost REGULAR roots (lowest z = most evenly spaced):")
for r,c,rc,fm,z in rows[:8]:
    print("  %-6s count=%-4d CV=%.2f vs random %.2f  z=%+.1f" % (r,c,rc,fm,z))
print("\nmost BURSTY roots (highest z = most clustered):")
for r,c,rc,fm,z in rows[-6:]:
    print("  %-6s count=%-4d CV=%.2f vs random %.2f  z=%+.1f" % (r,c,rc,fm,z))
