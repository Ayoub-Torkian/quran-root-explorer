# -*- coding: utf-8 -*-
"""Antonyms (qalīl/amsaka/qabḍ) + irrevocability of the gift (35:2) + forfeit-by-self-change (8:53,13:11). Unicode-safe."""
import json, csv
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
a=json.load(open(f"{R}/arabic.json",encoding='utf-8')); m=json.load(open(f"{R}/meaning.json",encoding='utf-8'))
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا') if s else s
rd={}
for d in csv.DictReader(open(f"{R}/exports/root_dictionary.csv",encoding='utf-8-sig')):
    rd[fa(d['root'])]=d
def occ(r):
    d=rd.get(fa(r),{}); return d.get('total_occurrences','?'),d.get('n_ayahs','?')
for r,l in {'قلل':'qalīl little (antonym of kathīr)','مسک':'amsaka withhold (antonym of give)',
            'قبض':'qabḍ contract','بسط':'basṭ expand','غیر':'ghayyara change','زید':'zāda increase','نقص':'naqaṣa decrease'}.items():
    o,ay=occ(r); print(f"  {r:5s} {l:32s} occ={o:>4} ayahs={ay}")
def show(keys,label):
    print(f"\n== {label} ==")
    for k in keys: print(' ',k,'|',(m.get(k,{}).get('en','') or '')[:122])
show(['2:249','8:65','4:66'],"qalīl vs kathīr — a SMALL band overcomes a LARGE one (quality beats quantity)")
show(['35:2','17:100','67:21','38:39'],"GIVE vs WITHHOLD (amsaka): what God opens none can withhold — fa-lā mumsika lahā")
show(['2:245','13:26','17:30'],"EXPAND vs STRAITEN provision (yabsuṭ / yaqdir·yaqbiḍ)")
show(['8:53','13:11'],"FORFEIT only by self-change: God changes not a favour/people until they change themselves")
import re
DIAC=re.compile(r'[ؐ-ًؚ-ٰٟۖ-ۭـ]'); strip=lambda s:DIAC.sub('',s)
print("\n35:2 rasm:", strip(a['35:2']))
