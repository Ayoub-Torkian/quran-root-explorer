#!/usr/bin/env python3
# ERROR-CORRECTION capacity. (1) RHYME as parity: how many bits does the verse-final rhyme
# determine the final root (entropy reduction)? (2) REDUNDANCY coverage: fraction of verses
# whose content is recoverable from a recurring frozen formula (backup copy).
import glob,unicodedata,collections,math,numpy as np
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
AR=set(chr(c) for c in range(0x621,0x64B)); skel=lambda s:''.join(c for c in unicodedata.normalize('NFD',s) if c in AR)
ordroots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:k,r=ln.rstrip('\n').split('\t',1);ordroots[k]=[x for x in r.split() if x and x!='NA']
finals=[];rhy=[];allr=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1);k=sa.strip();sk=skel(tx.strip());tr=ordroots.get(k,[])
    if not tr or len(sk)<2:continue
    finals.append(tr[-1]);rhy.append(sk[-2:]);allr.append(tr)
def H(counter):
    n=sum(counter.values());return -sum((c/n)*math.log2(c/n) for c in counter.values())
H0=H(collections.Counter(finals))
# conditional entropy of final root given rhyme class
byr=collections.defaultdict(collections.Counter)
for f,r in zip(finals,rhy):byr[r][f]+=1
n=len(finals);Hc=sum((sum(c.values())/n)*H(c) for c in byr.values())
print("(1) RHYME-as-parity: H(final root)=%.2f bits ; H(final|rhyme)=%.2f ; rhyme DETERMINES %.2f bits (%.0f%% of the ending)"%(H0,Hc,H0-Hc,100*(H0-Hc)/H0))
# (2) redundancy: fraction of verses containing a frozen trigram (recurs >=5x) = backup-recoverable
tri=collections.Counter()
for rs in allr:
    for i in range(len(rs)-2):tri[tuple(rs[i:i+3])]+=1
frozen=set(t for t,c in tri.items() if c>=5)
cov=np.mean([any(tuple(rs[i:i+3]) in frozen for i in range(len(rs)-2)) for rs in allr if len(rs)>=3])
print("(2) REDUNDANCY coverage: %.0f%% of verses contain a frozen (>=5x) formula -> partial backup copy"%(100*cov))
print("    distinct frozen trigrams: %d (the redundancy 'codebook')"%len(frozen))
