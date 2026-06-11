#!/usr/bin/env python3
# Frontier 2 — morphology/collocation word-model on the RASM-derived ROOT sequence.
# P5 found word-order weak via surface letters (no word-level rhyme). Here we test whether
# word order is constrained by ROOT collocation: (A) order-load — bigram conditional entropy
# of the root sequence in true order vs its own shuffle (analog of L14 at word scale);
# (B) per-token necessity — each root more predictable from local context in place vs random.
import glob,numpy as np
from collections import Counter,defaultdict
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
roots=open(R+'/research/two_books_genome/roots_seq.txt',encoding='utf-8').read().split()
roots=[r for r in roots if r!='NA']
M=len(roots); V=sorted(set(roots)); vid={r:i for i,r in enumerate(V)}; A=len(V)
seq=np.array([vid[r] for r in roots])
print(f"root tokens={M}  distinct roots={A}")
def bigram_bits(s):
    # prequential bits/token under a Laplace bigram with unigram backoff (causal)
    uni=np.zeros(A); big=defaultdict(lambda: np.zeros(A)); bits=0.0; ut=0
    for i in range(len(s)):
        c=s[i]; prev=s[i-1] if i>0 else None
        if prev is None:
            p=(uni[c]+0.1)/(uni.sum()+0.1*A)
        else:
            b=big[prev]; pb=(b[c]+0.1)/(b.sum()+0.1*A); pu=(uni[c]+0.1)/(uni.sum()+0.1*A)
            lam=b.sum()/(b.sum()+5.0); p=lam*pb+(1-lam)*pu
        bits+= -np.log2(p); ut+=1
        uni[c]+=1
        if prev is not None: big[prev][c]+=1
    return bits/ut
rng=np.random.default_rng(0)
real=bigram_bits(seq)
sh=np.mean([bigram_bits(seq[rng.permutation(M)]) for _ in range(3)])
print(f"\n(A) root-sequence order-load (bits/token, lower=more predictable):")
print(f"    true order   = {real:.3f} bits/token")
print(f"    shuffled     = {sh:.3f} bits/token   ->  order-load = {sh-real:.3f} bits/token  ({(sh-real)*M:,.0f} bits total)")
# (B) per-token in-place vs random, static bigram model (full-data, leave-one-out-ish)
uni=np.bincount(seq,minlength=A).astype(float)
big=defaultdict(lambda: np.zeros(A))
for i in range(1,M): big[seq[i-1]][seq[i]]+=1
def surp_at(tok,prev):
    b=big[prev]; pb=(b[tok]+0.1)/(b.sum()+0.1*A); pu=(uni[tok]+0.1)/(uni.sum()+0.1*A)
    lam=b.sum()/(b.sum()+5.0); return -np.log2(lam*pb+(1-lam)*pu)
sample=rng.choice(np.arange(1,M),8000,replace=False); nr=15; acc=0
for i in sample:
    s_in=surp_at(seq[i],seq[i-1])
    rp=rng.integers(1,M,nr); s_rand=np.array([surp_at(seq[i],seq[r-1]) for r in rp])
    acc+=np.mean(s_in<s_rand)
print(f"\n(B) per-token necessity: root more predictable from its TRUE preceding context than a random one: {acc/len(sample)*100:.1f}%  (chance 50%)")
