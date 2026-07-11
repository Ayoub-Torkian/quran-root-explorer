# -*- coding: utf-8 -*-
import openpyxl, collections, statistics
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
ws=openpyxl.load_workbook(R+"/Book6.xlsx",read_only=True)['Sheet1']
rows={}; nuzul={}
for row in ws.iter_rows(min_row=8,values_only=True):
    try: su,ay=int(row[5]),int(row[6])
    except: continue
    rows[(su,ay)]=dict(roots=(row[8]or'').split(),toks=(row[9]or'').split(),surf=(row[10]or'').split())
    try: nuzul[su]=int(row[12])
    except: pass

# ===== #1 divine subject-person: is WORSHIP ever directed to the majestic 'We' (1pl), vs 'Me'(1sg) / 'Lord'? =====
W={'عبد','سجد','صلو','سبح','حمد','رکع','قنت','دعو','ذکر','نسک'}
me=us=lord=0; me_ex=[]; us_ex=[]
for (su,ay),d in rows.items():
    s=d['surf']; rts=set(d['roots'])
    if not (rts&W): continue
    # worship verb indices
    wi=[i for i,w in enumerate(s) if w in ('اعبد','نعبد','اعبدو','اسجد','سبح','اذکر','ادع','نسجد','نسبح')]
    obj1sg = ('إیای' in s) or ('ایای' in s) or any(s[i+1:i+2]==['ی'] or s[i+1:i+2]==['نی'] or s[i+1:i+2]==['ن'] for i in wi)
    obj1pl = any(s[i+1:i+2]==['نا'] for i in wi)
    if obj1sg: me+=1; (me_ex.append(f"{su}:{ay}") if len(me_ex)<8 else None)
    if obj1pl: us+=1; us_ex.append(f"{su}:{ay}")
    if rts&{'ربب','اله'}: lord+=1
print("=== #1 person-of-worship ===")
print("  worship -> 1st-SINGULAR 'Me' :",me,me_ex)
print("  worship -> 1st-PLURAL 'We/Us':",us,us_ex)
print("  worship -> 'Lord/Allah'      :",lord)

# ===== #2 diachronic mood: perfect vs imperfect share per sura, by revelation order =====
def is_imperf(tok): return bool(tok) and tok[0] in ('ی','ي','ت','ن','أ','ا') and tok[0] in ('ی','ي','ت','ن')
prof={}
for (su,ay),d in rows.items():
    for tok in d['toks']:
        if not tok: continue
        # crude finite-verb filter: skip obvious nouns? just classify all tokens by prefix as proxy
        prof.setdefault(su,[0,0])
        if tok[0] in ('ی','ي','ت','ن'): prof[su][1]+=1   # imperfect-ish
        elif tok[0] in ('أ','ا') or len(tok)<=4: prof[su][0]+=1  # perfect/other (rough)
import statistics
bins=collections.defaultdict(list)
for su,(p,i) in prof.items():
    if su not in nuzul or (p+i)<5: continue
    frac_imperf=i/(p+i); bins[(nuzul[su]-1)//30].append(frac_imperf)
print("\n=== #2 diachronic mood (imperfect-share by revelation-order bin of 30) ===")
for b in sorted(bins): print("  nuzul %3d-%3d : mean imperfect-share %.2f  (n=%d suras)"%(b*30+1,b*30+30,statistics.mean(bins[b]),len(bins[b])))
ki=prof.get(108); print("  al-Kawthar(108) tokens perf/impf:",ki,"nuzul",nuzul.get(108))

# ===== #3 ridaa micro-law: every 2nd-sg ridaa (رضو) verse =====
print("\n=== #3 riḍā (رضو) with 2nd-sg ک — every occurrence ===")
for (su,ay),d in sorted(rows.items()):
    if 'رضو' in d['roots'] and 'ک' in d['surf']:
        print("  %-7s %s"%(f"{su}:{ay}"," ".join(d['surf'])[:50]))
