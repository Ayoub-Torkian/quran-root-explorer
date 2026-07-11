# -*- coding: utf-8 -*-
"""REFERENT-GROUPING engine. Sense-anchored groups (descriptor disambiguates). Measure EMERGENCE
(first-appearance in revelation order) + era distribution. Plus PROPHET referent class (fixed external order)."""
import openpyxl
from collections import defaultdict
def norm(s): return (s or '').replace('ي','ی').replace('ك','ک').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ة','ه')
wb=openpyxl.load_workbook("Book6.xlsx",read_only=True); ws=wb['Sheet1']
A=[]
for row in ws.iter_rows(min_row=9,values_only=True):
    try: su,ay=int(row[5]),int(row[6])
    except: continue
    A.append(dict(su=su,ay=ay,name=row[7],nuzul=int(row[12]),
                  roots=[norm(r) for r in (row[8]or'').split()],
                  toks=[norm(t) for t in (row[9]or'').split()],
                  surf=[norm(t) for t in (row[10]or'').split()]))
def has_seq(surf,seq):
    L=len(seq)
    for i in range(len(surf)-L+1):
        if surf[i:i+L]==seq: return True
    return False
def detect(d):
    g=set(); s=d['surf']; tk=d['toks']
    def lem(*p): return any(any(t.startswith(x) for x in p) for t in tk)
    # BELIEVERS (community)
    if has_seq(s,['الذین','امن']) or lem('مؤمن','مومن','مسلم'): g.add('believers')
    # DISBELIEVERS
    if has_seq(s,['الذین','کفر']) or lem('کافر') or 'کفار' in tk: g.add('disbelievers')
    # HYPOCRITES
    if lem('منافق') or has_seq(s,['الذین','نافق']) or has_seq(s,['قلوب','هم','مرض']) or has_seq(s,['فی','قلوب','هم','مرض']): g.add('hypocrites')
    # POLYTHEISTS
    if has_seq(s,['الذین','اشرک']) or lem('مشرک'): g.add('polytheists')
    # PEOPLE OF THE BOOK / Jews / Christians
    if has_seq(s,['اهل','ال','کتاب']) or has_seq(s,['الذین','اوت','ال','کتاب']) or has_seq(s,['الذین','هاد']) or lem('یهود','نصار','نصرانی'): g.add('people_of_book')
    # MECCAN DENIERS
    if has_seq(s,['الذین','کذب']) or lem('مکذب','مستکبر') or has_seq(s,['الذین','استکبر']): g.add('meccan_deniers')
    return g
groups=defaultdict(list)
for d in A:
    for g in detect(d): groups[g].append(d['nuzul'])
def era(n): return 'E' if n<=38 else ('M' if n<=77 else 'L')
print("=== REFERENT-GROUP emergence across revelation order (nuzul 1..114) ===")
print(f"{'group':16s} {'n_ayat':>6} {'1st_nuzul':>9} {'median':>7}   era E/M/L      late%")
for g in ['meccan_deniers','polytheists','disbelievers','believers','people_of_book','hypocrites']:
    nz=sorted(groups[g]); n=len(nz)
    import statistics as st
    e=sum(era(x)=='E' for x in nz);m=sum(era(x)=='M' for x in nz);l=sum(era(x)=='L' for x in nz)
    print(f"{g:16s} {n:6d} {nz[0]:9d} {int(st.median(nz)):7d}   {e:3d}/{m:3d}/{l:3d}    {l/n:.0%}")

print("\n=== PROPHET referent class: deployment across revelation (fixed external order as anchor) ===")
# external historical order (anchor axis)
PROPH=[('ادم','Adam',['ادم']),('نوح','Noah',['نوح']),('هود','Hud',['هود']),('صالح','Salih',['صالح']),
 ('ابراهیم','Abraham',['ابراهیم','ابرهیم']),('لوط','Lot',['لوط']),('یوسف','Joseph',['یوسف']),
 ('شعیب','Shuayb',['شعیب']),('موسی','Moses',['موسی','موس']),('داود','David',['داود','داوود']),
 ('سلیمان','Solomon',['سلیمان']),('زکریا','Zechariah',['زکریا']),('یحیی','John',['یحیی']),
 ('عیسی','Jesus',['عیسی','عیس']),('محمد','Muhammad',['محمد','احمد'])]
def era3(n): return 'E' if n<=38 else ('M' if n<=77 else 'L')
print(f"{'prophet':10s} {'n_ayat':>6} {'1st_nuzul':>9} {'median_nuzul':>12}   E/M/L")
for ar,en,pats in PROPH:
    nz=[d['nuzul'] for d in A if any(any(t.startswith(p) for p in pats) for t in d['toks'])]
    if not nz: print(f"{en:10s} {'0':>6}"); continue
    import statistics as st
    e=sum(era3(x)=='E' for x in nz);m=sum(era3(x)=='M' for x in nz);l=sum(era3(x)=='L' for x in nz)
    print(f"{en:10s} {len(nz):6d} {min(nz):9d} {int(st.median(nz)):12d}   {e}/{m}/{l}")
# Moses vs Children-of-Israel framing shift (early=exemplar, late=covenant/law)
mus=[d['nuzul'] for d in A if any(t.startswith('موس') for t in d['toks'])]
isr=[d['nuzul'] for d in A if has_seq(d['surf'],['بنی','اسرائیل']) or any(t.startswith('اسرائیل') for t in d['toks'])]
import statistics as st
print(f"\nMoses mentions median nuzul={int(st.median(mus))}  |  'Banu Israel' median nuzul={int(st.median(isr)) if isr else 'NA'} (n={len(isr)})  -> covenant framing later?")
