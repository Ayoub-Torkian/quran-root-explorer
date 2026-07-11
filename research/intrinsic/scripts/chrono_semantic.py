# -*- coding: utf-8 -*-
"""SEMANTIC-dimension chronology (not correlation): (A) الذین+descriptor referent-group emergence across
revealed time; (B) recover a RULING-GRADIENT (khamr) from internal deontic markers, validate vs nuzul order."""
import openpyxl
from collections import defaultdict,Counter
def norm(s): return (s or '').replace('ي','ی').replace('ك','ک').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ة','ه')
wb=openpyxl.load_workbook("Book6.xlsx",read_only=True); ws=wb['Sheet1']
A=[]; 
for row in ws.iter_rows(min_row=9,values_only=True):
    try: su,ay=int(row[5]),int(row[6])
    except: continue
    A.append(dict(su=su,ay=ay,name=row[7],nuzul=int(row[12]),
                  roots=[norm(r) for r in (row[8]or'').split()],
                  surf=[norm(t) for t in (row[10]or'').split()]))
N=len(A); 
# nuzul tertiles for "early/mid/late revealed time"
nz=sorted(set(d['nuzul'] for d in A)); 
def era(n): return 'early' if n<=38 else ('mid' if n<=77 else 'late')   # 114 suras / 3

print("=== (A) الذین + descriptor : referent-groups across revealed time ===")
groups=defaultdict(lambda:Counter())   # descriptor -> era counts
raw=Counter()
for d in A:
    s=d['surf']
    for i,w in enumerate(s):
        if w=='الذین':
            nxt=[t for t in s[i+1:i+4] if t not in ('و','ا','ال','من','فی','هم','کم','نا')][:2]
            key=' '.join(nxt) if nxt else '(bare)'
            raw[key]+=1
            groups[key][era(d['nuzul'])]+=1
print("top الذین-descriptors (count) with era split [early|mid|late]:")
for k,c in raw.most_common(18):
    e=groups[k]; tot=sum(e.values())
    print(f"  {k:22s} n={c:4d}  early={e['early']:3d} mid={e['mid']:3d} late={e['late']:3d}  late%={e['late']/tot:.0%}")

print("\n=== (B) khamr/سکر ruling-gradient from INTERNAL deontic markers (no topic-specific labels) ===")
POS=set(map(norm,['رزق','نفع','منافع','حلل','طیب']))        # provision / permitted
SIN=set(map(norm,['اثم']))                                   # sin-noun (ambivalent)
PARTIAL=set(map(norm,['قرب','سکر']))                         # 'do not approach...while...'
PROHIB=set(map(norm,['حرم','رجس','جنب','نهی','نتهی','فسق']))  # full prohibition markers
def stance(d):
    r=set(d['roots']); su=d['surf']
    sc=0; tags=[]
    if r & POS: sc=max(sc,1); tags.append('provision')
    if r & SIN: sc=max(sc,2); tags.append('sin-noun')
    if (r & PARTIAL) and any(x=='لا' for x in su): sc=max(sc,3); tags.append('partial-prohib(لا تقربوا)')
    if r & PROHIB: sc=max(sc,4); tags.append('prohibition(رجس/اجتنبوا)')
    return sc,tags
verses=[d for d in A if ('خمر' in d['roots']) or ('سکر' in d['roots'])]
verses=sorted(verses,key=lambda d:(d['su'],d['ay']))
print("verses containing خمر or سکر:")
rows=[]
for d in verses:
    sc,tags=stance(d)
    rows.append((d['su'],d['ay'],d['nuzul'],sc,tags," ".join(d['surf'])[:60]))
for su,ay,nu,sc,tags,txt in rows:
    print(f"  {su}:{ay:<3} nuzul={nu:<3} stance={sc} {','.join(tags):32s} {txt}")
# recovered order by stance vs revelation order
byst=sorted(rows,key=lambda x:x[3])
print("\n  recovered semantic gradient (by internal stance, low->high):")
print("   ", " -> ".join(f"{su}:{ay}(s{sc},nz{nu})" for su,ay,nu,sc,tags,txt in byst))
# check monotonic vs nuzul
import itertools
conc=tot=0
for a,b in itertools.combinations(rows,2):
    if a[3]==b[3] or a[2]==b[2]: continue
    tot+=1; conc+= (a[3]-b[3])*(a[2]-b[2])>0
print(f"  stance vs revelation-order concordance: {conc}/{tot}")
print("  [REPORT] traditional gradual order: 16:67 -> 2:219 -> 4:43 -> 5:90/91 (history corroborates, not evidence)")
