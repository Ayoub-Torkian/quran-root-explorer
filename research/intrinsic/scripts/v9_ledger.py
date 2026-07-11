# -*- coding: utf-8 -*-
import openpyxl, collections
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
ws=openpyxl.load_workbook(R+"/Book6.xlsx",read_only=True)['Sheet1']
rows={}
for row in ws.iter_rows(min_row=8,values_only=True):
    try: su,ay=int(row[5]),int(row[6])
    except: continue
    rows[(su,ay)]=dict(roots=(row[8]or'').split(),toks=(row[9]or'').split(),surf=(row[10]or'').split())
# index: root -> list of (su,ay, has_2sg_k, is_perfect)
def isperf(tok): return not (tok[:1] in ('ی','ي','ت','ن','أ','ا') and tok[:1] in ('ی','ي','ت','ن'))
def perfect(tok): return tok[:1] not in ('ی','ي','ت','ن')   # imperfect prefixes -> not perfect
# find candidate FUTURE-to-2sg-k verses (markers: سوف, س, عسی/عسى, nun-tawkid pattern verb+ن)
futmark=lambda s:[i for i,w in enumerate(s) if w in ('سوف','س','عسی','عسى')]
print("=== ALL prospective (future/عسی/sa-) constructions with a 2sg ک ===")
cands=[]
for (su,ay),d in sorted(rows.items()):
    s=d['surf']
    idxs=futmark(s)
    if not idxs: continue
    for i in idxs:
        seg=s[i:i+6]
        if 'ک' in seg:
            # find the verb root in this verse near i
            cands.append((su,ay,s[i],"".join(' '+w for w in s[max(0,i-1):i+6])))
            break
for su,ay,mk,win in cands:
    print("  %-7s [%s] %s"%(f"{su}:{ay}",mk,win[:52]))
print("  total prospective+ک verses:",len(cands))

# For each, is the verb-root also attested as a PERFECT with ک elsewhere? (discharge test)
# collect root->set of (perfect?,has-k) occurrences
root_perf_k=collections.defaultdict(lambda:[False,False])  # root -> [has_perfect_with_k, has_future_with_k]
for (su,ay),d in rows.items():
    s=d['surf']
    for ri,rt in enumerate(d['roots']):
        tok=d['toks'][ri] if ri<len(d['toks']) else ''
        vi=next((i for i,w in enumerate(s) if w==tok or w.endswith(tok) or (tok and tok.endswith(w))),None)
        if vi is None: continue
        hask='ک' in s[vi+1:vi+4]
        if not hask: continue
        if perfect(tok): root_perf_k[rt][0]=True
print("\n=== discharge status of the divine-to-Prophet promise verbs ===")
for rt,gl in [('عطو','give'),('کفی','suffice'),('قرء','recite'),('لقی','cast'),('ولی','turn(qibla)'),('بعث','raise(maqam)')]:
    pk=root_perf_k.get(rt,[False])[0]
    print("  %-5s %-12s perfect-with-ک elsewhere? %s"%(rt,gl,'YES (dischargeable)' if pk else 'no'))
