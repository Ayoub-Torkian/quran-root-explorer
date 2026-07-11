# -*- coding: utf-8 -*-
"""PRE-REGISTERED validation harness (internal pilot; papers untouched).
Primary F = mean over a surah's content roots of each root's MAX PPMI bond.
Null = rarity-matched bootstrap (same freq-bin per root). Decision: >95th pct=outlier."""
import json, collections, itertools, math, random
random.seed(11)
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا')
ay_roots={}
for line in open(f"{R}/research/two_books_genome/roots_by_ayah.tsv",encoding='utf-8'):
    line=line.rstrip('\n')
    if '\t' in line:
        k,rs=line.split('\t',1); ay_roots[k]=set(fa(x) for x in rs.split())
ayahs=list(ay_roots.values()); N=len(ayahs)
cnt=collections.Counter(); co=collections.Counter()
for s in ayahs:
    for r in s: cnt[r]+=1
    for a,b in itertools.combinations(sorted(s),2): co[(a,b)]+=1
def pair(a,b): return co.get((a,b),0)+co.get((b,a),0)
def ppmi(a,b):
    c=pair(a,b)
    return max(0.0, math.log2(c*N/(cnt[a]*cnt[b]))) if c>0 else 0.0
def maxbond(r):
    best=0.0
    for o in cnt:
        if o!=r and pair(r,o)>0:
            p=ppmi(r,o); best=p if p>best else best
    return best
# precompute maxbond for all roots (cache)
MB={}
def mb(r):
    if r not in MB: MB[r]=maxbond(r)
    return MB[r]
def F(roots): 
    rs=[r for r in roots if r in cnt]
    return sum(mb(r) for r in rs)/len(rs) if rs else 0.0
# frequency bins
def fbin(c):
    if c==1: return 0
    if c<=5: return 1
    if c<=20: return 2
    if c<=100: return 3
    if c<=500: return 4
    return 5
binroots=collections.defaultdict(list)
for r,c in cnt.items(): binroots[fbin(c)].append(r)
def boot_F(template_roots, n=10000):
    tb=[fbin(cnt[r]) for r in template_roots if r in cnt]
    out=[]
    for _ in range(n):
        draw=[random.choice(binroots[b]) for b in tb]
        out.append(F(draw))
    return out
def pct(val, dist): return 100.0*sum(1 for x in dist if x<val)/len(dist)

SURAS={108:['عطو','کثر','صلو','ربب','نحر','شنء','بتر'],103:None,110:None,112:None,113:None,114:None}
# derive content roots for panel from corpus
def surah_roots(s):
    rs=set()
    for k,v in ay_roots.items():
        if int(k.split(':')[0])==s: rs|=v
    return sorted(rs)
print("="*64); print("PRIMARY NULL: F = mean(max-PPMI bond), rarity-matched bootstrap"); print("="*64)
for s in [108,103,110,112,113,114]:
    roots=SURAS[108] if s==108 else surah_roots(s)
    f=F(roots); dist=boot_F(roots,10000)
    import statistics as st
    z=(f-st.mean(dist))/ (st.pstdev(dist) or 1e-9)
    print(f"  surah {s:3d}: nroots={len([r for r in roots if r in cnt]):2d}  F={f:.2f}  null_mean={st.mean(dist):.2f}  pct={pct(f,dist):5.1f}  z={z:+.2f}")
print("\n"+"="*64); print("HAPAX TEST: do نحر/بتر bind more than the typical hapax?"); print("="*64)
hapax=[r for r,c in cnt.items() if c==1]
hb=sorted(mb(r) for r in hapax)
import statistics as st
for r in ['نحر','بتر']:
    v=mb(r); p=100.0*sum(1 for x in hb if x<v)/len(hb)
    print(f"  {fa(r)}: maxbond={v:.2f}  vs {len(hapax)} hapax (median={st.median(hb):.2f})  pct={p:.1f}")
print("\n"+"="*64); print("SMALL-COUNT HONESTY (Fisher-exact, one-tailed) for hapax co-occurrence"); print("="*64)
from math import comb
def fisher_one(a,b):  # P(>= observed co-occurrence | marginals), hypergeometric tail
    na,nb=cnt[a],cnt[b]; k=pair(a,b)
    # hypergeometric: drawing na ayahs, how many hit the nb that contain b
    p=sum(comb(nb,i)*comb(N-nb,na-i) for i in range(k,min(na,nb)+1))/comb(N,na)
    return k,na,nb,p
for a,b in [('بتر','شنء'),('نحر','صلو'),('نحر','کثر')]:
    k,na,nb,p=fisher_one(a,b)
    print(f"  {fa(a)}×{fa(b)}: co={k}, n({fa(a)})={na}, n({fa(b)})={nb}  ->  P(chance) = {p:.4g}")

print("\n"+"="*64); print("ROBUSTNESS: does al-Maida rank #1 as Kawthar's elaborator under metric sweeps?"); print("="*64)
KW={'عطو','کثر','صلو','ربب','نحر','شنء','بتر'}
# surah-level root sets and counts
surahs=collections.defaultdict(set); surah_len=collections.Counter()
for k,v in ay_roots.items():
    s=int(k.split(':')[0]); surahs[s]|=v; surah_len[s]+=len(v)
# surah-frequency of a root (in how many surahs it appears) for idf
sfreq=collections.Counter()
for s,rs in surahs.items():
    for r in rs: sfreq[r]+=1
import math
def idf(r): return math.log(114/(sfreq[r] or 1))
def rank_maida(alpha,beta):
    sc={}
    for s,rs in surahs.items():
        if s==108: continue
        shared=KW & rs
        val=sum(idf(r)**alpha for r in shared)
        val=val/ (surah_len[s]**beta if beta else 1)
        sc[s]=val
    order=sorted(sc,key=lambda s:-sc[s])
    return order.index(5)+1, order[:3]
for beta in (0,1):
    for alpha in (0,0.5,1,2):
        rk,top3=rank_maida(alpha,beta)
        print(f"  rarity-exp={alpha}, length-norm={'on' if beta else 'off'}:  al-Maida rank = {rk}   (top3 surahs: {top3})")
# which sharers carry it
print("\n  roots al-Maida(5) shares with Kawthar:", sorted(KW & surahs[5]), " | شنء in surahs:", sorted(s for s,rs in surahs.items() if 'شنء' in rs))
