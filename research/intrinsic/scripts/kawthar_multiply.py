# -*- coding: utf-8 -*-
"""The multiplication-of-reward economy + 'jāʾa bi-l-ḥasana' (brought, not merely did). Unicode-safe."""
import json, csv
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
a=json.load(open(f"{R}/arabic.json",encoding='utf-8')); m=json.load(open(f"{R}/meaning.json",encoding='utf-8'))
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا') if s else s
rd={}
for d in csv.DictReader(open(f"{R}/exports/root_dictionary.csv",encoding='utf-8-sig')):
    rd[fa(d['root'])]=d
def occ(r):
    d=rd.get(fa(r),{}); return d.get('total_occurrences','?'),d.get('n_ayahs','?'),d.get('busiest_surah','')

for r,l in {'ضعف':'ḍiʿf/yuḍāʿif multiply','وسع':'wasiʿa vast/embrace','جیء':'jāʾa come/bring',
            'حسن':'ḥasana good deed','حبب':'ḥabba grain/love','سنبل':'sunbul ear of grain','مثل':'mithl like'}.items():
    o,ay,b=occ(r); print(f"  {r:5s} {l:24s} occ={o:>4} ayahs={ay:>4} busiest={b}")

def show(keys,label):
    print(f"\n== {label} ==")
    for k in keys: print(' ',k,'|',(m.get(k,{}).get('en','') or '')[:120])

show(['6:160','27:89','28:84'],"jāʾa bi-l-ḥasana — 'whoever COMES WITH a good deed' → tenfold; (good ×10, evil ×1)")
show(['2:261','2:245','2:265'],"the parable: grain→7 ears→100 each (700×); yuḍāʿif li-man yashāʾ; wāsiʿ ʿalīm; kathīr(2:245)")
show(['2:268','2:247','3:73','24:32'],"wāsiʿ ʿalīm — paired with faḍl/grace (God is All-embracing, All-knowing)")
show(['64:17','4:40','30:39','57:11','35:30'],"yuḍāʿif applied elsewhere; reward exceeds desert")
# verify exact wording of 6:160 and the 'jaa bi' vs 'fa3ala' contrast
import re
DIAC=re.compile(r'[ؐ-ًؚ-ٰٟۖ-ۭـ]'); strip=lambda s:DIAC.sub('',s)
print("\n6:160 rasm:", strip(a['6:160']))
print("2:261 rasm:", strip(a['2:261']))
# does 6:160 say 'jaa bi' (came with) not 'fa3ala' (did)?
print("\n6:160 contains جاء (came/brought):", 'جَاءَ' in a['6:160'], "| 27:89:", 'جَاءَ' in a['27:89'])
