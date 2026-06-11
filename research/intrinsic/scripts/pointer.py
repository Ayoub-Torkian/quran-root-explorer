#!/usr/bin/env python3
# POINTER / indirection test. Define-then-reference: is a root's FIRST occurrence in a richer
# context (definition) than its later occurrences (pointers)? Context = #distinct other roots
# in the verse. Paired per root vs occurrence-order shuffle. Root level + char level (letters).
import glob,unicodedata,collections,numpy as np
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
AR=set(chr(c) for c in range(0x621,0x64B)); skel=lambda s:''.join(c for c in unicodedata.normalize('NFD',s) if c in AR)
versesR=[]
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln: versesR.append([x for x in ln.split('\t',1)[1].split() if x and x!='NA'])
def indirection(verses, minc=10):
    occ=collections.defaultdict(list)  # symbol -> list of (verse_idx, context_size)
    for vi,v in enumerate(verses):
        ctx=len(set(v))
        for s in set(v): occ[s].append((vi,ctx))
    d_first=[]; rng=np.random.default_rng(0); d_null=[]
    for s,lst in occ.items():
        if len(lst)<minc: continue
        lst=sorted(lst); ctxs=[c for _,c in lst]
        first=ctxs[0]; rest=np.mean(ctxs[1:])
        d_first.append(first-rest)
        sh=rng.permutation(ctxs); d_null.append(sh[0]-np.mean(sh[1:]))
    d_first=np.array(d_first); d_null=np.array(d_null)
    t=(d_first.mean()-d_null.mean())/np.sqrt(d_first.std()**2/len(d_first)+d_null.std()**2/len(d_null))
    return d_first.mean(), d_null.mean(), t, len(d_first)
mf,mn,t,n=indirection(versesR,10)
print("ROOT level — first-occurrence context minus later: real %+.2f vs shuffle %+.2f  t=%+.1f (n=%d roots)"%(mf,mn,t,n))
print("  (positive = first occurrence is richer = define-then-point indirection)")
# char level: letters per verse, context = #distinct letters
versesC=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' in ln: versesC.append(list(skel(ln.split('\t',1)[1].strip())))
mf2,mn2,t2,n2=indirection(versesC,30)
print("CHAR level — first-occurrence context minus later: real %+.2f vs shuffle %+.2f  t=%+.1f (n=%d letters)"%(mf2,mn2,t2,n2))
