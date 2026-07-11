# -*- coding: utf-8 -*-
"""The giving/granting/electing verb family — differentiating aʿṭā, ātā, wahaba,
iṣṭafā, ijtabā by their whole datasets. al-Qurʾān yufassiru baʿḍuhu baʿḍan. Unicode-safe."""
import json, csv, re, collections
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
a=json.load(open(f"{R}/arabic.json",encoding='utf-8')); m=json.load(open(f"{R}/meaning.json",encoding='utf-8'))
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا') if s else s
roots={}
for line in open(f"{R}/research/two_books_genome/roots_by_ayah.tsv",encoding='utf-8'):
    line=line.rstrip('\n')
    if '\t' in line:
        k,rs=line.split('\t',1); roots[k]=[fa(x) for x in rs.split()]
rd={}
for d in csv.DictReader(open(f"{R}/exports/root_dictionary.csv",encoding='utf-8-sig')):
    rd[fa(d['root'])]=d
idx=collections.defaultdict(list)
for k,rs in roots.items():
    for r in set(rs): idx[r].append(k)
sk=lambda k:(int(k.split(':')[0]),int(k.split(':')[1]))

fam={'عطو':'aʿṭā give','ءتی':'ātā give/confer','وهب':'wahaba gift(esp. progeny)',
     'صفو':'iṣṭafā elect/choose','جبی':'ijtabā elect/pick','رزق':'razaqa provide','نعم':'anʿama favour'}
print("== FAMILY SIZES ==")
for r,lbl in fam.items():
    d=rd.get(r,{}); print(f"  {r:5s} {lbl:26s} occ={d.get('total_occurrences','?'):>4} ayahs={d.get('n_ayahs','?'):>4} surahs={d.get('n_surahs','?')}")

def dump(r,lbl,keys=None,n=99):
    ks=sorted(keys or idx.get(r,[]),key=sk)
    print(f"\n== {r} ({lbl}) — {len(idx.get(r,[]))} verses; showing contexts ==")
    for k in ks[:n]:
        print(' ',k,'|',(m.get(k,{}).get('en','') or '')[:104])

# aʿṭā — ALL 14 (full dataset)
dump('عطو','aʿṭā give')
# wahaba — what is gifted? (progeny test)
dump('وهب','wahaba gift')
# iṣṭafā elect
dump('صفو','iṣṭafā elect')
# ijtabā elect
dump('جبی','ijtabā elect')
# key ātā cases: wisdom/abundant good (2:269), Book, to the Prophet
print("\n== ātā key cases (give a NAMED endowment; note 2:269 uses kathīr) ==")
for k in ['2:269','2:251','3:79','4:54','12:22','28:14','15:87','17:55','27:15','38:20']:
    print(' ',k,'|',(m.get(k,{}).get('en','') or '')[:104])
# aʿṭā to the Prophet elsewhere (93:5) + same satisfaction note
print("\n== aʿṭā to the Prophet — 93:5 (matched pair with 108:1) ==")
for k in ['93:5','108:1']:
    print(' ',k,'|',(m.get(k,{}).get('en','') or '')[:104])
# does the surah name progeny anywhere? (wahaba/walad/nasl/dhurriyya absent?)
print("\n== is progeny vocabulary present in 108? roots:",{f'108:{i}':roots.get(f'108:{i}',[]) for i in (1,2,3)})
