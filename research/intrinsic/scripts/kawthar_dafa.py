# -*- coding: utf-8 -*-
"""Repel the bad ACT (sayyiʾa) with a BETTER act (dafʿ/dar', aḥsan), not eliminate the bad ACTOR. Unicode-safe."""
import json, csv
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
a=json.load(open(f"{R}/arabic.json",encoding='utf-8')); m=json.load(open(f"{R}/meaning.json",encoding='utf-8'))
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا') if s else s
rd={}
for d in csv.DictReader(open(f"{R}/exports/root_dictionary.csv",encoding='utf-8-sig')):
    rd[fa(d['root'])]=d
def occ(r):
    d=rd.get(fa(r),{}); return d.get('total_occurrences','?'),d.get('n_ayahs','?')
for r,l in {'دفع':'dafʿ repel/ward off','درا':'daraʾa avert','حسن':'ḥasan good/better','سوا':'sūʾ/sayyiʾa bad',
            'رفع':'rafʿ raise/elevate','صلح':'iṣlāḥ set right','عفو':'ʿafw pardon'}.items():
    o,ay=occ(r); print(f"  {r:5s} {l:22s} occ={o:>4} ayahs={ay}")
def show(keys,label):
    print(f"\n== {label} ==")
    for k in keys: print(' ',k,'|',(m.get(k,{}).get('en','') or '')[:128])
show(['23:96','41:34','13:22','28:54'],"REPEL the bad with the BETTER/good (idfaʿ/yadraʾūna bi-llatī hiya aḥsan / bi-l-ḥasanati l-sayyiʾa)")
show(['2:251','22:40'],"dafʿ as PREVENTIVE balance: without God's repelling people by one another, the earth/places would be ruined")
show(['41:35','42:40','42:43'],"the 'better' response: enemy becomes friend; reward of patience; forgiveness")
# rafʿ — what does it actually mean in the Qurʾān? (raise/elevate, not 'remove evil')
show(['2:253','12:76','94:4','58:11'],"rafʿ = RAISE/elevate in the Qurʾān (rank, the heavens, your renown) — not 'reactive removal'")
import re
DIAC=re.compile(r'[ؐ-ًؚ-ٰٟۖ-ۭـ]'); strip=lambda s:DIAC.sub('',s)
print("\n23:96 rasm:", strip(a['23:96']))
print("41:34 rasm:", strip(a['41:34']))
print("\nNote on aḥsan: appears as 'allatī hiya aḥsan' — NO 'al-' (no definite superlative marker), NO 'min' (no explicit comparative).")
