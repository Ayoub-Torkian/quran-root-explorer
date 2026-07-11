# -*- coding: utf-8 -*-
"""'Given' (grace) vs 'earned' (deed) — the Qurʾān's two vocabularies. Unicode-safe."""
import json, csv, collections
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
a=json.load(open(f"{R}/arabic.json",encoding='utf-8')); m=json.load(open(f"{R}/meaning.json",encoding='utf-8'))
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا') if s else s
rd={}
for d in csv.DictReader(open(f"{R}/exports/root_dictionary.csv",encoding='utf-8-sig')):
    rd[fa(d['root'])]=d
def occ(r):
    d=rd.get(fa(r),{}); return d.get('total_occurrences','?'),d.get('n_ayahs','?')

GIVEN={'عطو':'aʿṭā give','وهب':'wahaba gift','فضل':'faḍl bounty/grace','نعم':'niʿma favour',
       'رحم':'raḥma mercy','رزق':'rizq provision','هدی':'hudā guidance'}
EARNED={'کسب':'kasaba earn','سعی':'saʿā strive','عمل':'ʿamal work/deed','اجر':'ajr wage/reward',
        'جزی':'jazā recompense','کدح':'kadaḥa toil'}
print("== GIVEN (grace) vocabulary ==")
for r,l in GIVEN.items(): o,ay=occ(r); print(f"  {r:5s} {l:20s} occ={o:>4} ayahs={ay}")
print("== EARNED (deed) vocabulary ==")
for r,l in EARNED.items(): o,ay=occ(r); print(f"  {r:5s} {l:20s} occ={o:>4} ayahs={ay}")

def show(keys,label):
    print(f"\n== {label} ==")
    for k in keys: print(' ',k,'|',(m.get(k,{}).get('en','') or '')[:108])

show(['2:269','3:73','24:38','38:39','62:4','57:21','35:32'],"GIVEN: 'to whom He wills', 'bounty in God's hand', 'without reckoning'")
show(['2:286','53:39','99:7','99:8','45:22','52:21','74:38'],"EARNED: each soul has what it earned / only what he strove for")
show(['2:261','4:40','35:30','64:17'],"GRACE EXCEEDS DESERT: reward multiplied / increased from His bounty")
show(['29:69','47:17','18:30'],"INTERPLAY: strive → He guides; deeds not wasted")
show(['108:1','108:2','108:3','84:6'],"AL-KAWTHAR cycle: gift (v1) → 'so' worship (v2) → hater cut off (v3); 84:6 toil")
print("\n108:2 begins with fa- (so/therefore):", a['108:2'][:12])
