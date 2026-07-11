# -*- coding: utf-8 -*-
"""Two axes: k-th-r = QUANTITY (atemporal), b-t-r/d-b-r = CONTINUITY/sequel (temporal). Unicode-safe."""
import json, re, collections
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
a=json.load(open(f"{R}/arabic.json",encoding='utf-8')); m=json.load(open(f"{R}/meaning.json",encoding='utf-8'))
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا') if s else s
roots={}
for line in open(f"{R}/research/two_books_genome/roots_by_ayah.tsv",encoding='utf-8'):
    line=line.rstrip('\n')
    if '\t' in line: k,rs=line.split('\t',1); roots[k]=[fa(x) for x in rs.split()]
idx=collections.defaultdict(list)
for k,rs in roots.items():
    for r in set(rs): idx[r].append(k)

# sample the QUANTITY senses of k-th-r in the glosses: do any carry duration/time?
qty=re.compile(r'\b(many|much|most|more|abundance|abundant|numerous|multitude|number|increase)\b',re.I)
tmp=re.compile(r'\b(forever|everlasting|lasting|endure|perpetual|continu|always|eternal|abiding)\b',re.I)
ks=sorted(idx['کثر'],key=lambda k:(int(k.split(':')[0]),int(k.split(':')[1])))
nq=sum(1 for k in ks if qty.search(m.get(k,{}).get('en','') or ''))
nt=sum(1 for k in ks if tmp.search(m.get(k,{}).get('en','') or ''))
print(f"k-th-r verses: {len(ks)} | gloss has QUANTITY word: {nq} | gloss has DURATION/time word: {nt}")
print("any with a duration word (potential temporal use):")
for k in ks:
    g=m.get(k,{}).get('en','') or ''
    if tmp.search(g): print('  ',k,'|',g[:100])

# d-b-r 'what follows behind / sequel' — the temporal back-end
print("\n== d-b-r (dābir = the following/rear; the sequel that gets 'cut off') ==")
for k in ['6:45','7:72','8:7','15:66','29:20']:
    print(' ',k,'|',(m.get(k,{}).get('en','') or '')[:104])
# contrast: the simple antonyms NOT used
print("\nNote: simple opposite of 'much' = qalīl (little); simple opposite of 'cut-off' = mawṣūl/bāqī.")
print("The surah pairs a QUANTITY word (kawthar) against a CONTINUITY word (abtar) — across axes, not within one.")
