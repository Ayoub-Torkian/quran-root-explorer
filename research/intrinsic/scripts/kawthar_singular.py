# -*- coding: utf-8 -*-
"""shāniʾaka SINGULAR & unnamed (108) vs Abu Lahab NAMED (111); tabba ~ abtar; 'what he EARNED availed not'. Unicode-safe."""
import json, csv
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
a=json.load(open(f"{R}/arabic.json",encoding='utf-8')); m=json.load(open(f"{R}/meaning.json",encoding='utf-8'))
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا') if s else s
rd={}
for d in csv.DictReader(open(f"{R}/exports/root_dictionary.csv",encoding='utf-8-sig')):
    rd[fa(d['root'])]=d
def occ(r):
    d=rd.get(fa(r),{}); return d.get('total_occurrences','?'),d.get('n_ayahs','?'),d.get('busiest_surah','')
for r in ['تبب','بتر','کسب','غنی','لهب']:
    o,ay,b=occ(r); print(f"  {r:5s} occ={o:>4} ayahs={ay:>3} busiest={b}")
def show(keys,label):
    print(f"\n== {label} ==")
    for k in keys: print(' ',k,'|',(m.get(k,{}).get('en','') or '')[:124])
# Surah 111 in full
show(['111:1','111:2','111:3','111:4','111:5'],"SURAH 111 (al-Masad): named by EPITHET 'Abu Lahab'; tabba(ruin); his wealth & what he EARNED availed not")
# tabb elsewhere (ruin/loss)
show(['40:37'],"tabb = ruin/loss elsewhere (Pharaoh's plot ended only 'in ruin', tabāb)")
# 108:3 singular hater (unnamed) vs the plural-enemies pattern elsewhere
show(['108:3'],"108:3 — SINGULAR, unnamed hater")
show(['2:98','4:101','60:1'],"the Qurʾān's usual PLURAL enemies (ʿaduww/aʿdāʾ of God and the faithful)")
import re
DIAC=re.compile(r'[ؐ-ًؚ-ٰٟۖ-ۭـ]'); strip=lambda s:DIAC.sub('',s)
print("\n111:1 rasm:", strip(a['111:1']),"| 111:2 rasm:", strip(a['111:2']))
print("note: 'Abu Lahab' is named by EPITHET (father of flame) — matched by 111:3 'a flaming fire'.")
