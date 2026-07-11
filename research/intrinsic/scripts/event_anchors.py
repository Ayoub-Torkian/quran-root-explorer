# -*- coding: utf-8 -*-
"""EVENT-ANCHOR corroboration layer [REPORT, never input]. (1) verify each event's cited ayahs carry the
event's OWN vocabulary internally (reconcile); (2) build event-based within-Medinan order; (3) test internal
fusion ranking against that order (does internal evidence corroborate the event chronology?)."""
import openpyxl, numpy as np
from collections import defaultdict
from scipy.stats import spearmanr
def norm(s): return (s or '').replace('ي','ی').replace('ك','ک').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ة','ه')
wb=openpyxl.load_workbook("Book6.xlsx",read_only=True); ws=wb['Sheet1']
R={}; S=defaultdict(list)
for row in ws.iter_rows(min_row=9,values_only=True):
    try: su,ay=int(row[5]),int(row[6])
    except: continue
    d=dict(su=su,ay=ay,nuzul=int(row[12]),roots=[norm(r) for r in (row[8]or'').split()],
           surf=[norm(t) for t in (row[10]or'').split()])
    R[(su,ay)]=d; S[su].append(d)
def gather(su,ays):
    rr=[]; ss=[]
    for a in ays:
        d=R.get((su,a))
        if d: rr+=d['roots']; ss.append(d['surf'])
    return rr,ss
def present(roots,surfs,markers,seqs=()):
    hit=[m for m in markers if any(r==m or r.startswith(m) for r in roots)]
    for seq in seqs:
        for s in surfs:
            if any(s[i:i+len(seq)]==seq for i in range(len(s)-len(seq)+1)): hit.append(' '.join(seq)); break
    return hit
# event -> (host sura, ayahs, approx AH order, internal markers, surface-seqs) ; AH is [REPORT]
EV=[
 ('Qibla change',2,list(range(142,151)),2.0,['شطر','وجه','حرم'],[['ال','مسجد','ال','حرام']]),
 ('Badr (named)',3,[123],2.0,['بدر','نصر'],[]),
 ('Badr spoils',8,list(range(41,45)),2.0,['غنم','نفل'],[]),
 ('Uhud',3,list(range(121,129))+list(range(140,148)),3.0,['قرح','غزو'],[]),
 ('Banu Nadir / Hashr',59,list(range(1,15)),4.0,['حشر','جلو','نضر'],[]),
 ('Khandaq / Ahzab',33,list(range(9,28)),5.0,['حزب','جند'],[['اذ','جاء','ت','کم','جنود']]),
 ('Hudaybiyya / Fath',48,[1,10,18,27],6.0,['فتح','بیع'],[]),
 ('Conquest of Mecca',110,[1,2,3],8.0,['نصر','فتح'],[]),
 ('Tabuk',9,list(range(38,53)),9.0,['خلف','ثقل','جهد'],[]),
 ('Masjid Dirar',9,list(range(107,111)),9.0,['ضرر','مسجد','فرق'],[]),
 ('Muhajirun & Ansar',9,[100,117],3.5,['هجر','نصر','سبق'],[]),
 ('Hajj / Umra',2,list(range(196,204)),6.0,['حجج','عمر','هدی'],[]),
]
print("=== (1) RECONCILE: do the cited ayahs carry the event's own vocabulary? [internal check] ===")
print(f"{'event':24s} {'host':>4} {'AH':>4}  internal markers found")
ok=0
for name,su,ays,ah,mk,seqs in EV:
    rr,ss=gather(su,ays); hit=present(rr,ss,mk,seqs)
    flag='OK' if hit else 'MISS'
    ok+= bool(hit)
    print(f"  {name:24s} {su:4d} {ah:4.1f}  [{flag}] {', '.join(hit)}")
print(f"  reconciled {ok}/{len(EV)} event-anchors carry their vocabulary internally")

print("\n=== (2)-(3) event-based within-Medinan order vs internal fusion ranking ===")
# event AH per HOST SURA (take earliest event in a sura as its anchor)
sura_ah={}
for name,su,ays,ah,mk,seqs in EV:
    sura_ah[su]=min(ah,sura_ah.get(su,99))
# add farewell/late Maida
sura_ah[5]=10.0
ah_suras=sorted(sura_ah, key=lambda s:sura_ah[s])
print("event-anchored Medinan sura order (AH [REPORT]):",[(s,sura_ah[s]) for s in ah_suras])
print("their raw nuzul-col order:",[(s,S[s][0]['nuzul']) for s in ah_suras])
# build fusion features quickly (reuse minimal set) and rank these suras
def hs(s,seq):
    L=len(seq); return any(s[i:i+L]==seq for i in range(len(s)-L+1))
def lem(tk,*p): return any(any(t.startswith(x) for x in p) for t in tk)
def feat(su):
    ay=S[su];n=len(ay);allr=[r for d in ay for r in d['roots']];nr=max(1,len(allr))
    f=[np.mean([len(d['surf']) for d in ay]),
       sum(hs(d['surf'],['الذین','امن']) for d in ay)/n,
       sum('نفق'==r for r in allr)/nr,
       sum(hs(d['surf'],['اهل','ال','کتاب']) for d in ay)/n,
       sum(r in set(map(norm,['جهد','قتل','حرب','نفر'])) for r in allr)/nr]
    return f
ev_ah=np.array([sura_ah[s] for s in ah_suras]); 
nuzul_rank=np.array([S[s][0]['nuzul'] for s in ah_suras])
print(f"\n  nuzul-col vs event-AH order  Spearman={spearmanr(nuzul_rank,ev_ah).correlation:.3f}")
# does a single internal proxy (jihad/qital density) track AH order?
X=np.array([feat(s) for s in ah_suras])
for i,nm in enumerate(['mean_len','believer_addr','munafiq','ahl_kitab','war_density']):
    print(f"  internal {nm:14s} vs event-AH  Spearman={spearmanr(X[:,i],ev_ah).correlation:+.3f}")
