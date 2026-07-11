# -*- coding: utf-8 -*-
"""SUFFICIENCY: can the discontinuity signal RE-DERIVE the canonical 113 sūra cuts (NECESSITY), or are the
boundaries real-but-not-unique (NECESSARY only)? top-K recovery, best-F1 unsupervised segmentation, and a
relaxation gap g_seg = how far canonical sits below the signal-optimal cut-set. MEASURED on rasm."""
import openpyxl, statistics as st
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
wb=openpyxl.load_workbook(R+"/Book6.xlsx", read_only=True, data_only=True); ws=wb.active
sura=[]; roots=[]; rhyme=[]
for r in ws.iter_rows(min_row=9, values_only=True):
    try: s=int(r[5])
    except (TypeError,ValueError): continue
    sura.append(s); roots.append(set(str(r[8] or "").split()))
    toks=str(r[10] or "").split(); w=toks[-1] if toks else ""; rhyme.append(w[-2:] if len(w)>=2 else w)
n=len(sura); G=n-1
def jac(a,b):
    u=a|b; return len(a&b)/len(u) if u else 0.0
lex=[1-jac(roots[i],roots[i+1]) for i in range(G)]
rhy=[1.0 if rhyme[i]!=rhyme[i+1] else 0.0 for i in range(G)]
comb=[0.5*lex[i]+0.5*rhy[i] for i in range(G)]
bset=set(i for i in range(G) if sura[i]!=sura[i+1]); nb=len(bset)
mx=max(comb); sat=sum(1 for v in comb if v>=mx-1e-9)
print("gaps:",G,"boundaries:",nb,"| saturated gaps (comb==max=%.2f):"%mx, sat)
# top-K recovery (tie-break by lexical then rhyme)
order=sorted(range(G), key=lambda i:(-comb[i], -lex[i], -rhy[i]))
topK=set(order[:nb])
rec=len(topK & bset)/nb
print("recovery: canonical boundaries in the top-%d discontinuity gaps = %.0f%% (precision=recall, ties broken by lexical)"%(nb,100*rec))
# best-F1 unsupervised threshold
best=(0,0,0,0)
for t in sorted(set(comb)):
    pred=set(i for i in range(G) if comb[i]>=t)
    if not pred: continue
    tp=len(pred&bset); P=tp/len(pred); Rc=tp/nb; F=2*P*Rc/(P+Rc) if P+Rc else 0
    if F>best[0]: best=(F,P,Rc,t)
print("best unsupervised F1 = %.2f (precision %.2f, recall %.2f, at threshold %.2f)"%best)
# relaxation gap: canonical cut-set mean vs optimal (top-nb) vs random
canon=st.mean(comb[i] for i in bset); opt=st.mean(comb[i] for i in order[:nb]); rnd=st.mean(comb)
g=(opt-canon)/(opt-rnd+1e-9)
print("cut-set mean discontinuity: canonical %.3f | optimal(top) %.3f | random %.3f -> relaxation gap g_seg=%.2f"%(canon,opt,rnd,g))
print("DONE")
