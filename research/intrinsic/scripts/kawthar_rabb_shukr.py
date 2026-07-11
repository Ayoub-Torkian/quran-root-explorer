# -*- coding: utf-8 -*-
"""Collective continuous abundance (barakāt, ghadaq) + rabb(nurture) vs khāliq + shukr-as-self-increase. Unicode-safe."""
import json, csv
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
a=json.load(open(f"{R}/arabic.json",encoding='utf-8')); m=json.load(open(f"{R}/meaning.json",encoding='utf-8'))
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا') if s else s
rd={}
for d in csv.DictReader(open(f"{R}/exports/root_dictionary.csv",encoding='utf-8-sig')):
    rd[fa(d['root'])]=d
def occ(r):
    d=rd.get(fa(r),{}); return d.get('total_occurrences','?'),d.get('n_ayahs','?')
for r,l in {'ربب':'rabb Lord/nurturer','خلق':'khalaqa create','شکر':'shukr gratitude','زید':'zāda increase',
            'برک':'baraka blessing','غدق':'ghadaq abundant(water)','درر':'midrār pouring','نمو':'namā grow'}.items():
    o,ay=occ(r); print(f"  {r:5s} {l:24s} occ={o:>4} ayahs={ay}")
def show(keys,label):
    print(f"\n== {label} ==")
    for k in keys: print(' ',k,'|',(m.get(k,{}).get('en','') or '')[:124])
# Thread A: collective continuous abundance for the righteous people
show(['7:96','72:16','71:11','71:12','5:66','65:2','65:3'],"COLLECTIVE righteousness -> sustained/flowing abundance (barakāt, ghadaq, midrār)")
# Thread B: rabb = nurturer (raise/rear), distinct from khalq (create once)
show(['26:18','1:2','17:24','89:6'],"rabb = to REAR/nurture (Pharaoh: 'did we not RAISE you', root r-b-b) — ongoing, vs one-time khalq")
# shukr -> self-increase (object = YOU), not a transactional payout
show(['14:7','34:13','27:40','2:152','3:145'],"shukr -> 'I will INCREASE YOU' (azīdannakum); 'WORK in gratitude' (action built in)")
import re
DIAC=re.compile(r'[ؐ-ًؚ-ٰٟۖ-ۭـ]'); strip=lambda s:DIAC.sub('',s)
print("\n14:7 rasm:", strip(a['14:7']))
print("108:2 says li-RABBIKA (rabb), not khaliq:", 'رَبّ' in a['108:2'] or 'ربک' in strip(a['108:2']))
