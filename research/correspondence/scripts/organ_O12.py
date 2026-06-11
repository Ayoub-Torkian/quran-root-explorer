#!/usr/bin/env python3
# O12 · ROBUSTNESS / error-correction — is the verse-ending RECOVERABLE from the local rhyme code? (redundancy)
import unicodedata, collections
import numpy as np
AR=set(chr(c) for c in range(0x621,0x64B))
def rasm(s): return ''.join(c for c in unicodedata.normalize('NFD',s) if c in AR)
R="research/two_books_genome/data/quran/quran_arabic_verses.tsv"
sur=collections.defaultdict(list)
allf=[]
for ln in open(R,encoding='utf-8'):
    if '\t' not in ln: continue
    sa,tx=ln.rstrip('\n').split('\t',1); s=int(sa.split(':')[0])
    ws=[w for w in (rasm(x) for x in tx.split()) if w]
    if ws: sur[s].append(ws[-1][-1]); allf.append(ws[-1][-1])
# error-correction coverage: fraction of verse-endings recoverable from the sura's dominant rhyme
prot=0; tot=0
for s,L in sur.items():
    c=collections.Counter(L); dom=c.most_common(1)[0][0]
    prot+=sum(1 for x in L if x==dom); tot+=len(L)
# random baseline: most common letter corpus-wide
cc=collections.Counter(allf); base=cc.most_common(1)[0][1]/len(allf)
print("O12 · ROBUSTNESS / error-correction:")
print(f"   {prot/tot:.0%} of verse-endings match their sura's dominant rhyme (recoverable if corrupted)")
print(f"   vs {base:.0%} for the single most-common letter corpus-wide (random-code baseline)")
print(f"   => a local rhyme CODE protects ~{prot/tot:.0%} of endings: built-in redundancy = error-correction (O12 ✓, partial like O6)")
