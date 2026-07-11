# -*- coding: utf-8 -*-
"""V4 probe #6 — is there a clean 'concept-coining' class? For every short sura, list its hapax and
classify each as CONCEPT-type (distinct: its rare context is shared with no other hapax -> a coined,
under-determined term) vs OBJECT-type (its rare context is shared -> a concrete once-named thing).
Tests whether al-Kawthar/al-Ikhlas form a separable class, not just 'short suras with rare words'."""
import collections, itertools, math
import numpy as np
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا')
sura_ay=collections.defaultdict(list); ayahs=[]; spread=collections.defaultdict(set)
for line in open(f"{R}/research/two_books_genome/roots_by_ayah.tsv",encoding='utf-8'):
    line=line.rstrip('\n')
    if '\t' not in line: continue
    ref,rs=line.split('\t',1); su=int(ref.split(':')[0]); rl=[fa(x) for x in rs.split()]
    ayahs.append(set(rl)); sura_ay[su].append(rl)
    for r in rl: spread[r].add(su)
N=len(ayahs); cnt=collections.Counter(); co=collections.Counter()
for s in ayahs:
    for r in s: cnt[r]+=1
    for a,b in itertools.combinations(sorted(s),2): co[(a,b)]+=1
# a hapax's "rare context" = its co-occurring NON-ubiquitous roots (spread<=20)
hapax_all=[r for r in cnt if cnt[r]==1]
def rare_ctx(r):
    ctx=set()
    for (a,b),c in co.items():
        if a==r: o=b
        elif b==r: o=a
        else: continue
        if len(spread[o])<=20: ctx.add(o)
    return frozenset(ctx)
hctx={r:rare_ctx(r) for r in hapax_all}
# distinct = no OTHER hapax shares any rare-context root
from collections import defaultdict
ctx_owners=defaultdict(set)
for r,cx in hctx.items():
    for o in cx: ctx_owners[o].add(r)
def is_distinct(r):
    for o in hctx[r]:
        if len(ctx_owners[o])>1: return False
    return True
NAMES={108:'al-Kawthar',112:'al-Ikhlas',103:'al-ʿAsr',110:'al-Nasr',102:'al-Takathur',106:'Quraysh',111:'al-Masad',113:'al-Falaq',114:'al-Nas',107:'al-Maʿun',105:'al-Fil',109:'al-Kafirun',104:'al-Humaza',101:'al-Qariʿa',100:'al-ʿAdiyat',99:'al-Zalzala'}
shorts=[su for su in range(1,115) if len(set(r for rl in sura_ay[su] for r in rl)) and len(sura_ay[su])<=6]
print("short suras (<=6 verses):",len(shorts))
print("%-4s %-12s %-3s %-5s %-7s %s"%("su","name","hpx","dist","class","hapax roots (distinct*)"))
concept=[];obj=[];none=[]
for su in sorted(shorts):
    uniq=sorted(set(r for rl in sura_ay[su] for r in rl))
    hpx=[r for r in uniq if cnt[r]==1]
    dist=[r for r in hpx if is_distinct(r)]
    if not hpx: cls='none'; none.append(su)
    elif dist: cls='CONCEPT'; concept.append(su)
    else: cls='object'; obj.append(su)
    tag=" ".join((r+'*' if r in dist else r) for r in hpx) if hpx else '-'
    print("%-4d %-12s %-3d %-5d %-7s %s"%(su,NAMES.get(su,str(su)),len(hpx),len(dist),cls,tag))
print("\nCONCEPT-class (>=1 DISTINCT hapax): %d suras -> %s"%(len(concept),concept))
print("object-class (hapax but none distinct): %d -> %s"%(len(obj),obj))
print("no-hapax: %d -> %s"%(len(none),none))
print("\n108 al-Kawthar hapax:",[r for r in sorted(set(r for rl in sura_ay[108] for r in rl)) if cnt[r]==1],
      "| 112 al-Ikhlas hapax:",[r for r in sorted(set(r for rl in sura_ay[112] for r in rl)) if cnt[r]==1])
