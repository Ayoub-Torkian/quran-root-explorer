# -*- coding: utf-8 -*-
"""Divine commerce: God 'buys' (ishtarā) what He gave, returns it manifold & everlasting. Unicode-safe."""
import json, csv
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
a=json.load(open(f"{R}/arabic.json",encoding='utf-8')); m=json.load(open(f"{R}/meaning.json",encoding='utf-8'))
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا') if s else s
rd={}
for d in csv.DictReader(open(f"{R}/exports/root_dictionary.csv",encoding='utf-8-sig')):
    rd[fa(d['root'])]=d
def occ(r):
    d=rd.get(fa(r),{}); return d.get('total_occurrences','?'),d.get('n_ayahs','?')
for r,l in {'شری':'sharā/ishtarā buy/sell','بیع':'bayʿ trade/sale','تجر':'tijāra commerce',
            'قرض':'qarḍ loan','بور':'bawār perish','ربح':'ribḥ profit','خسر':'khusr loss'}.items():
    o,ay=occ(r); print(f"  {r:5s} {l:24s} occ={o:>4} ayahs={ay}")
def show(keys,label):
    print(f"\n== {label} ==")
    for k in keys: print(' ',k,'|',(m.get(k,{}).get('en','') or '')[:118])
show(['9:111','2:207'],"GOD BUYS the believers' selves/wealth for the Garden; man sells himself for God's pleasure")
show(['35:29','61:10','61:11'],"a COMMERCE THAT NEVER PERISHES (tijāra lan tabūr — root bawār); a trade that saves")
show(['2:245','57:11','64:17','73:20'],"LEND God a goodly loan → multiplied")
show(['2:284','3:189','37:96','53:48'],"God OWNS / created all — incl. what He 'buys' (He created you and what you do)")
import re
DIAC=re.compile(r'[ؐ-ًؚ-ٰٟۖ-ۭـ]'); strip=lambda s:DIAC.sub('',s)
print("\n35:29 has بور (perish) negated 'lan tabur':", 'تَبُورَ' in a['35:29'] or 'تبور' in strip(a['35:29']))
print("9:111 has اشتری (bought):", 'اشتری' in strip(a['9:111']), "| has بیع:", 'بیع' in strip(a['9:111']))
