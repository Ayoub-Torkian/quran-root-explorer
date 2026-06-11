#!/usr/bin/env python3
# FEASIBILITY — intrinsic morphology from rasm. For each surface word, find its root (a root
# from the āyah, appearing as an ordered consonant-subsequence) and extract the RESIDUE pattern
# (prefix letters | infix gaps | suffix letters) — the wazn skeleton, derived only from rasm.
import glob,unicodedata,collections
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
AR=set(chr(c) for c in range(0x621,0x64B)); skel=lambda s:''.join(c for c in unicodedata.normalize('NFD',s) if c in AR)
rootset={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:k,r=ln.rstrip('\n').split('\t',1);rootset[k]=set(x for x in r.split() if x and x!='NA')
def subseq_span(word,root):
    # find ordered subsequence positions of root consonants in word; return positions or None
    pos=[];j=0
    for i,ch in enumerate(word):
        if j<len(root) and ch==root[j]:pos.append(i);j+=1
    return pos if j==len(root) else None
def residue(word,pos):
    rootset_i=set(pos)
    pre="".join(word[:pos[0]]); suf="".join(word[pos[-1]+1:])
    infix="".join(word[i] for i in range(pos[0]+1,pos[-1]) if i not in rootset_i)
    return (pre, infix, suf)
pat=collections.Counter(); matched=0; total=0
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1);rs=rootset.get(sa.strip(),set())
    for w in tx.strip().split():
        wk=skel(w)
        if len(wk)<2:continue
        total+=1
        best=None
        for r in rs:
            p=subseq_span(wk,r)
            if p and (best is None or len(r)>best[1]):best=(p,len(r),r)
        if best:
            matched+=1; pre,inf,suf=residue(wk,best[0])
            pat[("P:"+pre if pre else "", "I:"+inf if inf else "", "S:"+suf if suf else "")]+=1
print("tokens: %d ; matched to a root: %d (%.0f%%)"%(total,matched,100*matched/total))
print("top residue PATTERNS (prefix | infix | suffix) — the intrinsic wazn inventory:")
for k,v in pat.most_common(18):
    lbl=" ".join(x for x in k if x) or "(bare root)"
    print("  %6d  %s"%(v,lbl))
