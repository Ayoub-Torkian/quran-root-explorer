#!/usr/bin/env python3
# CANDIDATE — internal sound-echo (consonance). Do verses repeat consonants WITHIN themselves
# more than a corpus-letter-frequency null of the same length? 3 angles: (A) letter-repetition
# (fewer distinct letters than random), (B) word-initial alliteration (consecutive words sharing
# first letter), (C) root-echo (same root used >1× in a verse). Rasm, intrinsic.
import glob,unicodedata,numpy as np
from collections import Counter
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
def skel(t):
    t=unicodedata.normalize('NFD',t);t=''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln: k,r=ln.rstrip('\n').split('\t',1); roots[k]=[x for x in r.split() if x and x!='NA']
verses=[]; corpus=Counter()
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1); w=skel(tx); letters=''.join(w)
    verses.append((letters,[x[0] for x in w if x],roots.get(sa.strip(),[]))); corpus.update(letters)
alpha=list(corpus.keys()); pr=np.array([corpus[c] for c in alpha],float); pr/=pr.sum()
rng=np.random.default_rng(0)
# (A) letter repetition: distinct/total (LOWER = more internal repetition)
realA=[]; nullA=[]
for letters,_,_ in verses:
    T=len(letters)
    if T<8: continue
    realA.append(len(set(letters))/T)
    r=rng.choice(len(alpha),T,p=pr); nullA.append(len(set(r))/T)
realA=np.array(realA); nullA=np.array(nullA)
# (B) word-initial alliteration: fraction of adjacent word pairs sharing first letter
realB=[]; nullB=[]
for _,inits,_ in verses:
    if len(inits)<3: continue
    realB.append(np.mean([inits[i]==inits[i+1] for i in range(len(inits)-1)]))
    r=list(rng.choice(alpha,len(inits),p=pr)); nullB.append(np.mean([r[i]==r[i+1] for i in range(len(r)-1)]))
realB=np.array(realB); nullB=np.array(nullB)
# (C) root-echo: fraction of verses where some root repeats
realC=np.mean([len(rs)>len(set(rs)) and len(rs)>=3 for _,_,rs in verses if len(rs)>=3])
# null for C: shuffle roots across corpus into same-length verses
allr=[r for _,_,rs in verses for r in rs]; nl=[len(rs) for _,_,rs in verses if len(rs)>=3]
nullC=[]
for _ in range(200):
    pool=list(rng.permutation(allr)); k=0; hits=0; tot=0
    for L in nl:
        seg=pool[k:k+L]; k+=L; hits+= (len(seg)>len(set(seg))); tot+=1
    nullC.append(hits/tot)
print("internal sound-echo (consonance) — real vs corpus-frequency null:")
print(f"(A) distinct-letter ratio (LOWER=more repetition): real {realA.mean():.3f}  null {nullA.mean():.3f}  -> more repetition in {np.mean(realA<nullA)*100:.0f}% of verses")
print(f"(B) word-initial alliteration: real {realB.mean()*100:.1f}%  null {nullB.mean()*100:.1f}%")
print(f"(C) root-echo (a root repeats in the verse): real {realC*100:.1f}%  null {np.mean(nullC)*100:.1f}%")
