#!/usr/bin/env python3
# ERROR-CORRECTION at the CHAR level.
# (1) parity: how constrained is the verse-FINAL letter (fāṣila) vs a general letter? and how
#     much do the preceding 2 letters determine the final letter (intra-word redundancy)?
# (2) redundancy coverage: fraction of verses containing a frozen (>=5x) letter-trigram.
import glob,unicodedata,collections,math,numpy as np
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'
AR=set(chr(c) for c in range(0x621,0x64B)); skel=lambda s:''.join(c for c in unicodedata.normalize('NFD',s) if c in AR)
finals=[];cond=collections.defaultdict(collections.Counter);allletters=collections.Counter();verses=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    _,tx=ln.split('\t',1);sk=skel(tx.strip())
    if len(sk)<3:continue
    verses.append(sk);finals.append(sk[-1])
    cond[sk[-3:-1]][sk[-1]]+=1
    for ch in sk:allletters[ch]+=1
def H(c):
    n=sum(c.values());return -sum((x/n)*math.log2(x/n) for x in c.values())
Hgen=H(allletters);Hfin=H(collections.Counter(finals))
n=len(finals);Hc=sum((sum(c.values())/n)*H(c) for c in cond.values())
print("(1) CHAR parity: H(any letter)=%.2f ; H(verse-final letter)=%.2f (ending is %.0f%% more constrained); H(final|prev 2)=%.2f -> preceding letters determine %.2f bits"%(Hgen,Hfin,100*(Hgen-Hfin)/Hgen,Hc,Hfin-Hc))
tri=collections.Counter()
for v in verses:
    for i in range(len(v)-2):tri[v[i:i+3]]+=1
frozen=set(t for t,c in tri.items() if c>=5)
cov=np.mean([any(v[i:i+3] in frozen for i in range(len(v)-2)) for v in verses])
print("(2) CHAR redundancy: %.0f%% of verses contain a frozen letter-trigram ; codebook size %d"%(100*cov,len(frozen)))
