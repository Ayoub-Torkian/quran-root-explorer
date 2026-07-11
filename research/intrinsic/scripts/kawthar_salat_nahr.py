# -*- coding: utf-8 -*-
"""Is ṣalāt only ritual prayer, or the broader 'turning/connection'? And what does the corpus license for hapax naḥr? Unicode-safe."""
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

# ṣalāt: classify the 90 verses by sense cue in gloss
ks=sorted(idx['صلو'],key=lambda k:(int(k.split(':')[0]),int(k.split(':')[1])))
bless=re.compile(r'\b(bless|blessings|invoke|send (his )?blessings|salawat|salutation)\b',re.I)
place=re.compile(r'\b(synagogue|place(s)? of worship|cloister|temple)\b',re.I)
ritual=re.compile(r'\b(pray|prayer|maintain the prayer|establish|worship|bow|prostrat)\b',re.I)
cnt=collections.Counter()
notable=[]
for k in ks:
    g=m.get(k,{}).get('en','') or ''
    if bless.search(g): cnt['blessing/connection']+=1; notable.append((k,'BLESS',g[:90]))
    elif place.search(g): cnt['place of worship']+=1; notable.append((k,'PLACE',g[:90]))
    elif ritual.search(g): cnt['ritual prayer']+=1
    else: cnt['other']+=1
print("ṣalāt sense distribution (cue-based, 90 verses):",dict(cnt))
print("\nNON-ritual ṣalāt uses (the broader root — blessing/connection, places):")
for k in ['33:43','33:56','9:99','9:103','2:157','22:40','8:35']:
    print(' ',k,'|',(m.get(k,{}).get('en','') or '')[:118])

print("\n== naḥr — the ONLY internal anchors (hapax): its corpus neighbours ==")
for k in ['108:2','22:36','22:37','22:34','6:162']:
    print(' ',k,'|',(m.get(k,{}).get('en','') or '')[:118])
# does the root n-h-r (chest/throat) appear elsewhere as a noun? check nahar (day) is DIFFERENT root n-h-r vs n-h-r
print("\nNote: 'nahār' (daytime) is root ن-ه-ر (with hā), NOT ن-ح-r (with ḥā) — distinct from naḥr.")
