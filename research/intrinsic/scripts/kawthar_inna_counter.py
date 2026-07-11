# -*- coding: utf-8 -*-
"""Counter-example check for the innā/innī register claim. Unicode-safe."""
import json, re
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
a=json.load(open(f"{R}/arabic.json",encoding='utf-8')); m=json.load(open(f"{R}/meaning.json",encoding='utf-8'))
DIAC=re.compile(r'[ؐ-ًؚ-ٰٟۖ-ۭـ]')
strip=lambda s:DIAC.sub('',s)
# singular divine acts of making/placing/creating (possible counters to 'plural=power')
print("== singular 'I' + act of making/creating (counter-cases) ==")
for k in ['2:30','38:71','15:28','38:72','7:144']:
    print(k, strip(a[k])[:75], '| EN:', m.get(k,{}).get('en','')[:80])
# is there ANY innī/innanī + giving (ʿaṭā/ātā) addressed as a grant?  scan
print("\n== scan: any divine first-person SINGULAR giving (innī + a3ta/ata)? ==")
hits=[]
for k,t in a.items():
    s=strip(t)
    if ('انی' in s or 'اننی' in s) and ('اعطی' in s or 'اعطیت' in s or 'اتیت' in s):
        hits.append(k)
print('hits:',hits)
# and the tight sub-claim: grants to the Prophet ('laka'/'naka') — are they all plural?
print("\n== openings 'innā ...nā + laka/ka' (grants to the Prophet) ==")
for k,t in a.items():
    s=strip(t)
    if s.startswith('انا ') and ('لک' in s.split()[:6] or 'ناک' in s):
        print(' ',k, s[:55])
