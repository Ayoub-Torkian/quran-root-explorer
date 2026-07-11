# -*- coding: utf-8 -*-
"""Gift/election -> 'fa-' (so) -> commanded RESPONSE. Is 108:2 unique? what follows ātā/wahaba/ijtabā? Unicode-safe."""
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
def show(keys,label):
    print(f"\n== {label} ==")
    for k in keys: print(' ',k,'|',(m.get(k,{}).get('en','') or '')[:120])

# 1. all aʿṭā verses — does any coupling with an imperative response besides 108:2?
print("== all عطو (aʿṭā) verses — look for a commanded response ==")
for k in sorted(idx['عطو'],key=lambda k:(int(k.split(':')[0]),int(k.split(':')[1]))):
    print(' ',k,'|',(m.get(k,{}).get('en','') or '')[:110])

# 2. election ijtabā -> 'so establish prayer' (22:78)
show(['22:77','22:78'],"ELECTION (ijtabākum) -> 'so' bow, prostrate, worship; establish PRAYER, give ZAKAT")
# 3. favour/provision -> 'so let them worship' (Quraysh 106)
show(['106:1','106:2','106:3','106:4'],"PROVISION+SECURITY (Quraysh) -> 'so let them WORSHIP the Lord of this House'")
# 4. the giving-surah 93 (yuʿṭīka) -> fa- commands (orphan, beggar, proclaim the favour)
show(['93:5','93:9','93:10','93:11'],"GIVING (93) -> 'so' do not oppress orphan / repel beggar / PROCLAIM the favour")
# 5. wahaba -> praise (14:39); ātā kitāb -> recite/believe (2:121); remember/thank (2:152)
show(['14:39','2:121','2:152','6:162'],"wahaba->ḥamd; ātā Book->recite; favour->remember/thank; 'my prayer & sacrifice for God'")
# fa- check on 108:2
print("\n108:2 opens with fa- (so/therefore):", a['108:2'][:6])
