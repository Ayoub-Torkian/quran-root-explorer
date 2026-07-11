# -*- coding: utf-8 -*-
"""Deep dive on the grammatical line, validated against Book6 morphology (root+token+surface).
A) the عطو tense-grid (mechanical tense from the surface morphemes);
B) the divine-bestowal-to-the-Prophet verb set: is promise(imperfect)->fulfilment(perfect) a system?"""
import openpyxl, collections
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
wb=openpyxl.load_workbook(f"{R}/Book6.xlsx",read_only=True); ws=wb['Sheet1']
rows={}  # (su,ay) -> dict
for row in ws.iter_rows(min_row=8,values_only=True):
    try: su,ay=int(row[5]),int(row[6])
    except: continue
    roots=(row[8] or '').split()
    toks=(row[9] or '').split()
    surf=(row[10] or '').split()
    rows[(su,ay)]=dict(name=row[7],roots=roots,toks=toks,surf=surf,vocal=row[11] or '')
print("Book6 ayat loaded:",len(rows))

def tense_of(token, surf):
    """classify an Arabic content-token by tense from its consonantal shape + nearby particles."""
    t=token
    # noun forms of giving
    if t in ('عطاء','عطاؤ','نعمة','فضل','رحمة'): return 'noun'
    # future particle present anywhere adjacent
    fut = ('سوف' in surf) or any(x.startswith('س') and len(x)<=2 for x in surf)
    # imperfect prefixes (mudari): ی ت ن or ء(used as 1sg) -- but أ+CCC perfect (form IV) is ماضی
    if t and t[0] in ('ی','ي','ت','ن'):
        return 'future' if fut else 'imperfect'
    if t.startswith('أ') or t.startswith('ا'):
        # form IV perfect (أعطی, آتی) vs 1sg-imperfect; treat as perfect (lemma choice in Book6)
        return 'perfect'
    if t.startswith('است') or t.startswith('ان') or t.startswith('ت'):
        return 'perfect'
    # bare triliteral perfect (فعل) or imperative; check imperative by leading ا/و+ا
    return 'perfect'

def recipient_2sg(surf, vi):
    """is there a 2nd-person-singular clitic ک right after the verb token index vi?"""
    return 'ک' in surf[vi+1:vi+3] if vi is not None else ('ک' in surf)

# ---------- A) عطو grid ----------
print("\n=== A) عطو (give): every occurrence, mechanical tense ===")
print("%-7s %-9s %-9s %-6s %-4s %s"%("ref","root-tok","tense","2sg-ک","سوف","surface"))
giv=[]
for (su,ay),d in sorted(rows.items()):
    if 'عطو' not in d['roots']: continue
    # find the عطو token: index in roots -> matching tok
    ri=d['roots'].index('عطو'); tok=d['toks'][ri] if ri<len(d['toks']) else '?'
    # locate token in surface (best effort)
    vi=next((i for i,w in enumerate(d['surf']) if w==tok or w.endswith(tok) or tok.endswith(w)), None)
    te=tense_of(tok,d['surf']); k2=recipient_2sg(d['surf'],vi); suf='سوف' in d['surf']
    giv.append((su,ay,tok,te,k2,suf))
    print("%-7s %-9s %-9s %-6s %-4s %s"%(f"{su}:{ay}",tok,te,'yes' if k2 else '-', 'yes' if suf else '-'," ".join(d['surf'])[:46]))
# the key claim: God->Prophet (2sg ک) finite giving
prophet=[(su,ay,tok,te) for su,ay,tok,te,k2,suf in giv if k2 and te in('perfect','imperfect','future')]
print("\n  2nd-person (ک) finite عطو givings:",[(f"{s}:{a}",tk,te) for s,a,tk,te in prophet])

# ---------- B) divine-bestowal-to-the-Prophet verb set ----------
BEST={'عطو':'give','ءتی':'give','اتی':'give','وهب':'grant','فتح':'open/grant','شرح':'expand',
 'هدی':'guide','غنی':'enrich','ءوی':'shelter','رفع':'raise','وضع':'lift-off','زید':'increase','علم':'teach'}
print("\n=== B) divine bestowal verbs addressed to 2nd-sg (ک), with tense ===")
print("(filtering to verses whose verb carries a 2nd-sg ک recipient/object)")
tab=[]
for (su,ay),d in sorted(rows.items()):
    for ri,rt in enumerate(d['roots']):
        if rt not in BEST: continue
        tok=d['toks'][ri] if ri<len(d['toks']) else '?'
        vi=next((i for i,w in enumerate(d['surf']) if w==tok or w.endswith(tok) or tok.endswith(w)), None)
        if vi is None: continue
        # require a 2nd-sg ک within next 2 morphemes (object/recipient) AND a divine 1st-person giver nearby (نا/ن or no human subj)
        k2= 'ک' in d['surf'][vi+1:vi+3]
        if not k2: continue
        te=tense_of(tok,d['surf'])
        if te=='noun': continue
        tab.append((su,ay,rt,BEST[rt],tok,te,'سوف' in d['surf']))
from collections import Counter
print("%-7s %-6s %-9s %-9s %-9s %s"%("ref","root","gloss","tok","tense","سوف"))
for su,ay,rt,gl,tok,te,suf in tab:
    print("%-7s %-6s %-9s %-9s %-9s %s"%(f"{su}:{ay}",rt,gl,tok,te,'yes' if suf else '-'))
print("\n  tense counts (bestowal+ک):",dict(Counter(te for *_,te,_ in tab)))
print("  FUTURE (سوف) bestowals to ک:",[(f"{s}:{a}",rt,tok) for s,a,rt,gl,tok,te,suf in tab if suf])
