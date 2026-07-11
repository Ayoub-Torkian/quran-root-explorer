# -*- coding: utf-8 -*-
import openpyxl
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
wb=openpyxl.load_workbook(R+"/Book6.xlsx",read_only=True); ws=wb['Sheet1']
rows={}
for row in ws.iter_rows(min_row=8,values_only=True):
    try: su,ay=int(row[5]),int(row[6])
    except: continue
    rows[(su,ay)]=dict(roots=(row[8]or'').split(),toks=(row[9]or'').split(),surf=(row[10]or'').split())
def tense(tok,surf):
    if tok[:1] in('ی','ي','ت','ن'): return 'future' if ('سوف' in surf or 'س' in surf) else 'imperfect'
    return 'perfect'
# the four promise-verbs (root) + gloss
VERBS={'عطو':'give','قرأ':'recite','لقی':'cast','کفی':'suffice'}
for rt,gl in VERBS.items():
    print(f"=== {rt} ({gl}) : every occurrence with a 2sg ک ===")
    found=[]
    for (su,ay),d in sorted(rows.items()):
        if rt not in d['roots']: continue
        s=d['surf']
        # token for this root
        ri=[i for i,r in enumerate(d['roots']) if r==rt]
        for idx in ri:
            tok=d['toks'][idx] if idx<len(d['toks']) else '?'
            vi=next((i for i,w in enumerate(s) if w==tok or w.endswith(tok) or (tok and tok.endswith(w))),None)
            if vi is None: continue
            k2='ک' in s[vi+1:vi+4]
            if not k2: continue
            te=tense(tok,s)
            found.append((su,ay,tok,te," ".join(s[max(0,vi-1):vi+5])))
    for su,ay,tok,te,win in found:
        print("   %-7s %-9s %-9s %s"%(f"{su}:{ay}",tok,te,win[:48]))
    tenses=set(t for *_,t,_ in [(f[0],f[1],f[2],f[3],f[4]) for f in found])
    print("   -> tenses present:",sorted(tenses)," | promise+fulfil pair:", ('future' in tenses and 'perfect' in tenses))
