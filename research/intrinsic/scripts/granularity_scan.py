#!/usr/bin/env python3
# DETERMINACY SPECTRUM across granularity. Group the global 1..6236 verse stream into consecutive
# blocks of size b; each block = the UNION of its roots. Measure adjacent-block similarity (Jaccard)
# vs shuffling the block order. lift(b) = how much the ARRANGEMENT matters at granularity b.
# b=1 -> verse weave (L22 scale); larger b -> passage/section scale.
import glob,numpy as np
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:k,r=ln.rstrip('\n').split('\t',1);roots[k]=set(x for x in r.split() if x and x!='NA')
seq=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,_=ln.split('\t',1);seq.append(roots.get(sa.strip(),set()))
N=len(seq);rng=np.random.default_rng(5)
def jacc(a,b):
    u=a|b; return (len(a&b)/len(u)) if u else 0.0
def blocks(order,b):
    out=[]
    for i in range(0,N-b+1,b):
        s=set()
        for j in order[i:i+b]:s|=seq[j]
        out.append(s)
    return out
def adj_sim(blks):
    return np.mean([jacc(blks[i],blks[i+1]) for i in range(len(blks)-1)])
canon=list(range(N))
print("granularity b | real adj-Jaccard | block-shuffle floor | lift | z")
results=[]
for b in [1,2,3,5,10,20,50,100]:
    cb=blocks(canon,b); real=adj_sim(cb)
    # null: shuffle which verses fill the blocks? No — shuffle BLOCK ORDER (keep blocks intact)
    nb=len(cb); fl=[]
    for _ in range(200):
        perm=rng.permutation(nb); fl.append(np.mean([jacc(cb[perm[i]],cb[perm[i+1]]) for i in range(nb-1)]))
    fl=np.array(fl); z=(real-fl.mean())/(fl.std()+1e-9)
    results.append((b,real,fl.mean(),real-fl.mean(),z))
    print("  %5d       |     %.3f       |       %.3f        | %+.3f | %5.1f" % (b,real,fl.mean(),real-fl.mean(),z))
print("\nInterpretation: lift>0 at block size b means the ARRANGEMENT of b-verse passages is determined")
print("(adjacent passages are more similar than reshuffled passages). Where lift -> 0 is the scale")
print("beyond which the order stops carrying local structure.")
