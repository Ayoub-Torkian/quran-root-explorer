# -*- coding: utf-8 -*-
"""Instrument 7: rhetorical-FORM directional structure (a genuinely non-lexical signal from the rasm). Per āyah,
detect rhetorical-form markers (qul-directive, conditional, question, vocative/address, oath); assign a form-type.
TEST 1 (directional asymmetry): over canonical adjacent pairs build transition matrix T[a,b]; is it DIRECTIONALLY
asymmetric (form A precedes form B more than B precedes A) beyond an āyah-order-shuffle null? TEST 2 (recovery):
leave-one-sūra-out Markov transition log-likelihood — find order maximizing it -> directed τ. MEASURED; rasm only."""
import numpy as np, statistics as st, openpyxl
np.random.seed(13)
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
wb=openpyxl.load_workbook(R+"/Book6.xlsx", read_only=True, data_only=True); ws=wb.active
sura=[]; rasm=[]
for r in ws.iter_rows(min_row=9, values_only=True):
    try: s=int(r[5])
    except (TypeError,ValueError): continue
    sura.append(s); rasm.append(str(r[10] or "").split())
n=len(sura)
COND={"اذا","إذا","لو","لولا"}; QW={"هل","كيف","اين","أين","متى","اني","أني","ماذا","لماذا"}
def form(ww):
    if not ww: return 5
    s=set(ww)
    if s&QW: return 0                       # question
    if s&COND: return 1                     # conditional
    if any(w.startswith("يا") for w in ww): return 2   # vocative/address
    if any(w=="قل" or w.startswith("قل") for w in ww): return 3  # qul-directive
    if any(w.endswith("كم") or w.endswith("تم") for w in ww): return 4  # 2nd-person address
    return 5                                # declarative
F=[form(w) for w in rasm]
bounds={}; cur=sura[0]; start=0
for i in range(1,n):
    if sura[i]!=cur: bounds[int(cur)]=(start,i); cur=sura[i]; start=i
bounds[int(cur)]=(start,n)
K=6
def transmat(order_by_sura):
    T=np.zeros((K,K))
    for s,(a,b) in bounds.items():
        idx=order_by_sura(a,b)
        for m in range(len(idx)-1): T[F[idx[m]],F[idx[m+1]]]+=1
    return T
Tc=transmat(lambda a,b: list(range(a,b)))
def asym(T): return np.abs(T-T.T).sum()/2
ac=asym(Tc)
nulls=[]
for _ in range(300):
    def od(a,b):
        idx=list(range(a,b)); np.random.shuffle(idx); return idx
    nulls.append(asym(transmat(od)))
z=(ac-st.mean(nulls))/(st.pstdev(nulls) or 1e-9)
print("=== Instrument 7: rhetorical-form directional structure (rasm) ===")
ft=["quest","cond","voc","qul","2nd","decl"]
print("form-type counts:", {ft[k]:int((np.array(F)==k).sum()) for k in range(K)})
print(f"TEST1 directional asymmetry of adjacent form-transitions: canonical={ac:.0f} vs shuffle-null {st.mean(nulls):.0f}±{st.pstdev(nulls):.0f} -> z={z:+.1f}")
# top directed pairs (A precedes B much more than reverse)
pairs=[]
for a in range(K):
    for b in range(K):
        if a!=b and Tc[a,b]+Tc[b,a]>30:
            d=Tc[a,b]-Tc[b,a]
            if d>0: pairs.append((d,ft[a],ft[b],int(Tc[a,b]),int(Tc[b,a])))
pairs.sort(reverse=True)
print("strongest directional form-pairs (A→B » B→A):")
for d,a,b,fwd,rev in pairs[:6]: print(f"   {a:5s} -> {b:5s}  {fwd} vs {rev} (net +{int(d)})")
# TEST2 recovery via leave-one-out Markov loglik (greedy order maximizing transition prob)
suras=[s for s,(a,b) in bounds.items() if b-a>=4]
def kendall(a,b):
    L=len(a); ra={v:i for i,v in enumerate(a)}; rb={v:i for i,v in enumerate(b)}; c=di=0
    for i in range(L):
        for j in range(i+1,L):
            sg=(ra[a[i]]-ra[a[j]])*(rb[a[i]]-rb[a[j]])
            c+=sg>0; di+=sg<0
    return (c-di)/(c+di) if (c+di) else 0.0
taus=[]
for s in suras:
    a,b=bounds[s]
    Tt=Tc.copy()
    # subtract this sūra's transitions (leave-one-out)
    for m in range(b-a-1): Tt[F[a+m],F[a+m+1]]-=1
    P=(Tt+0.5); P=P/P.sum(1,keepdims=True); LP=np.log(P)
    L=b-a; items=list(range(a,b)); remaining=items[:]; order=[]
    # greedy: start from highest-marginal-start form, then maximize next-transition
    start_score={i:LP[:,F[i]].sum() for i in remaining}
    cur=min(remaining,key=lambda i:start_score[i]); order=[cur]; remaining.remove(cur)
    while remaining:
        nxt=max(remaining,key=lambda i: LP[F[order[-1]],F[i]]+1e-6*np.random.randn())
        order.append(nxt); remaining.remove(nxt)
    taus.append(kendall(order,list(range(a,b))))
print(f"TEST2 order-recovery from form-transition Markov (LOO): mean directed τ={st.mean(taus):+.3f} | {100*sum(t>=0.5 for t in taus)/len(taus):.0f}% τ>=0.5 (baselines: lexical +0.16 / +0.10 / -0.00)")
print("DONE")
