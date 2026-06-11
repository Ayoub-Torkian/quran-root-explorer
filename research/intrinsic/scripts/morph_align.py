#!/usr/bin/env python3
# Refined sequential alignment + verb/noun classification + proper C6 (cognate accusative).
import glob,unicodedata,collections,numpy as np
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
AR=set(chr(c) for c in range(0x621,0x64B)); skel=lambda s:''.join(c for c in unicodedata.normalize('NFD',s) if c in AR)
ordroots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:k,r=ln.rstrip('\n').split('\t',1);ordroots[k]=[x for x in r.split() if x and x!='NA']
def subseq(word,root):
    j=0;pos=[]
    for i,ch in enumerate(word):
        if j<len(root) and ch==root[j]:pos.append(i);j+=1
    return pos if j==len(root) else None
def classify(word,pos):
    pre=word[:pos[0]]; suf=word[pos[-1]+1:]
    # strip leading conjunction/prep particles و ف ب ك ل then ال
    p=pre
    while p[:1] in ('و','ف','ب','ك','ل','س'): p=p[1:]
    art = p[:2]=='ال'; 
    if art: p=p[2:]
    # imperfect verb prefix: ي ت ن ء (alif-hamza) at stem start, no article
    if (not art) and p[:1] in ('ي','ت','ن','ا','ء') and len(p)>=1:
        return 'VERB'
    return 'NOUN'
verses=[]; tot=0; matched=0; content=0
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1);roots=ordroots.get(sa.strip(),[]);toks=[skel(w) for w in tx.strip().split()]
    j=0; vlist=[]
    for w in toks:
        tot+=1
        if len(w)<2: continue
        assigned=None
        for dj in (0,1,2):
            if j+dj<len(roots):
                p=subseq(w,roots[j+dj])
                if p: assigned=(roots[j+dj],p); j=j+dj+1; break
        if assigned:
            matched+=1; r,pos=assigned; vlist.append((r,classify(w,pos)))
    verses.append(vlist)
content=sum(len(v) for v in verses)
print("tokens %d ; aligned to a root %d (%.0f%%)"%(tot,matched,100*matched/tot))
# C6: verses where SAME root appears as both VERB and NOUN
def has_cog(vl):
    byr=collections.defaultdict(set)
    for r,c in vl: byr[r].add(c)
    return any(len(s)>=2 for s in byr.values())
real=np.mean([has_cog(v) for v in verses if len(v)>=2])
rng=np.random.default_rng(0)
alllab=[c for v in verses for r,c in v]
fl=[]
for _ in range(200):
    sh=rng.permutation(alllab);idx=0;acc=[]
    for v in verses:
        n=len(v);vl=[(v[k][0],sh[idx+k]) for k in range(n)];idx+=n
        if n>=2: acc.append(has_cog(vl))
    fl.append(np.mean(acc))
fl=np.array(fl);print("(C6) verses w/ same root as VERB+NOUN: real %.3f vs label-shuffle %.3f±%.3f  z=%+.1f"%(real,fl.mean(),fl.std(),(real-fl.mean())/fl.std()))
