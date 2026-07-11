# -*- coding: utf-8 -*-
import openpyxl, collections
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
wb=openpyxl.load_workbook(R+"/Book6.xlsx",read_only=True); ws=wb['Sheet1']
rows={}
for row in ws.iter_rows(min_row=8,values_only=True):
    try: su,ay=int(row[5]),int(row[6])
    except: continue
    rows[(su,ay)]=dict(roots=(row[8]or'').split(),toks=(row[9]or'').split(),surf=(row[10]or'').split(),vocal=row[11]or'')

# ---- #1: the divine 'We...you[PROPHET]' gift litany, addressee hand-tagged ----
# candidate gift verses (root,ref) with hand addressee tag (P=Prophet, else who)
cand=[("ءتی",(15,87),"P","seven mathani"),("ءتی",(20,99),"P","a remembrance"),
 ("فتح",(48,1),"P","manifest victory"),("شرح",(94,1),"P","breast expanded"),
 ("وضع",(94,2),"P","burden lifted"),("رفع",(94,4),"P","remembrance raised"),
 ("عطو",(108,1),"P","al-Kawthar"),("عطو",(93,5),"P","[FUTURE promise]"),
 # non-Prophet controls caught by the loose filter:
 ("ءتی",(15,64),"angels->Lot","truth"),("ءتی",(20,58),"Moses->Pharaoh","magic"),
 ("ءتی",(27,40),"jinn->Solomon","throne"),("وهب",(19,19),"angel->Mary","a boy"),("هدی",(79,19),"Moses->Pharaoh","guidance")]
def tense(tok,surf):
    if 'سوف' in surf or ('س' in surf): pass
    if tok[:1] in('ی','ي','ت','ن'): return 'future' if 'سوف' in surf else 'imperfect'
    return 'perfect'
print("=== #1  divine gift verbs to 2sg, addressee hand-tagged ===")
litany=[]
for rt,(su,ay),who,gift in cand:
    d=rows.get((su,ay),{})
    surf=d.get('surf',[]); ri=d['roots'].index(rt) if rt in d.get('roots',[]) else -1
    tok=d['toks'][ri] if 0<=ri<len(d['toks']) else '?'
    te=tense(tok,surf)
    mark='PROPHET' if who=='P' else who
    print("  %-7s %-5s %-9s %-9s %-18s %s"%(f"{su}:{ay}",rt,tok,te,mark,gift))
    if who=='P': litany.append((su,ay,rt,tok,te,gift))
pc=[x for x in litany if x[4]=='perfect']; fc=[x for x in litany if x[4]=='future']
print("\n  PROPHET gift-litany: %d perfect (accomplished), %d future (promise)"%(len(pc),len(fc)))
print("  perfect:",[f"{s}:{a}({tok})" for s,a,rt,tok,te,g in pc])
print("  future :",[f"{s}:{a}({tok})" for s,a,rt,tok,te,g in fc])

# ---- #2a: ALL explicit-future (سوف / سـ) verbs to 2sg-ک across the corpus ----
print("\n=== #2a  every explicit-future verb addressed to 2sg ک (سوف or سـ proclitic) ===")
futs=[]
for (su,ay),d in sorted(rows.items()):
    s=d['surf']
    for i,w in enumerate(s):
        isfut = (w=='سوف') or (w=='س')
        if not isfut: continue
        # next imperfect verb + a ک within 3 tokens
        seg=s[i:i+5]
        if 'ک' in seg:
            futs.append((su,ay," ".join(s[max(0,i-1):i+5])))
            break
for su,ay,win in futs: print("  %-7s %s"%(f"{su}:{ay}",win[:55]))
print("  TOTAL future-to-2sg verses:",len(futs))

# ---- #2b: consolation cluster 93,94,108 — divine verb tense profile ----
print("\n=== #2b  consolation cluster (93,94,108): every token + tense ===")
for su in (93,94,108):
    for ay in range(1,30):
        d=rows.get((su,ay))
        if not d: continue
        toks=d['toks']
        prof=[]
        for ri,tok in enumerate(toks):
            te=tense(tok,d['surf'])
            prof.append("%s:%s"%(tok,te[:4]))
        print("  %d:%d  %s"%(su,ay," ".join(prof)))
