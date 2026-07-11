# -*- coding: utf-8 -*-
"""Why shāniʾ (hater) not ʿaduww (enemy) / khaṣm (litigant) / etc.? Unicode-safe."""
import json, csv, collections
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
rd={}
for d in csv.DictReader(open(f"{R}/exports/root_dictionary.csv",encoding='utf-8-sig')):
    rd[fa(d['root'])]=d
def occ(r):
    d=rd.get(fa(r),{}); return d.get('total_occurrences','?'),d.get('n_ayahs','?')
print("== the 'enemy/opposition' words, by frequency ==")
for r,l in {'عدو':'ʿaduww enemy (hostility/transgress)','خصم':'khaṣm litigant/disputant','شنء':'shāniʾ hater (detest)',
            'بغض':'baghḍāʾ hatred','کره':'kariha to dislike','ضدد':'ḍidd opposite'}.items():
    o,ay=occ(r); print(f"  {r:5s} {l:34s} occ={o:>4} ayahs={ay}")
def show(keys,label):
    print(f"\n== {label} ==")
    for k in keys: print(' ',k,'|',(m.get(k,{}).get('en','') or '')[:120])
# all 3 shāniʾ uses
print("\n== ALL شنء (shāniʾ) occurrences ==")
for k in sorted(idx['شنء'],key=lambda k:(int(k.split(':')[0]),int(k.split(':')[1]))):
    print(' ',k,'|',(m.get(k,{}).get('en','') or '')[:124])
# ʿaduww — external hostility (Satan, disbelievers)
show(['2:168','35:6','60:1','8:60'],"ʿaduww = external ENEMY / hostility (Satan; the disbelievers)")
# khaṣm — litigant in dispute
show(['38:21','38:22','22:19','36:77'],"khaṣm = ADVERSARY in dispute/litigation")
# shana'ān corrupts its bearer (5:8) — hatred distorts the hater
show(['5:2','5:8'],"shanaʾān (hatred) must not derail YOU — hatred corrupts the one who holds it")
