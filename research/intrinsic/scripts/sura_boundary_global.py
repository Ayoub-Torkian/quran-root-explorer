# -*- coding: utf-8 -*-
"""GLOBAL: are the 113 sūra boundaries intrinsically justified? Discontinuity (lexical Jaccard + rhyme/rawiyy
change) at canonical seams vs within-sūra gaps vs random cuts; boundary-optimality (local max); recoverability AUC.
al-Kawthar (107|108, 108|109) located as percentiles. MEASURED on rasm; basmala not a separate ayah (Fatiha aside)."""
import openpyxl, random, statistics as st
random.seed(17)
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
wb=openpyxl.load_workbook(R+"/Book6.xlsx", read_only=True, data_only=True); ws=wb.active
sura=[]; roots=[]; rhyme=[]
for r in ws.iter_rows(min_row=9, values_only=True):
    try: s=int(r[5])
    except (TypeError,ValueError): continue
    sura.append(s); roots.append(set(str(r[8] or "").split()))
    toks=str(r[10] or "").split(); w=toks[-1] if toks else ""
    rhyme.append(w[-2:] if len(w)>=2 else w)        # rawiyy proxy = last 2 rasm letters
n=len(sura); G=n-1
def jac(a,b):
    u=a|b; return len(a&b)/len(u) if u else 0.0
lex=[1-jac(roots[i],roots[i+1]) for i in range(G)]   # lexical dissimilarity
rhy=[1.0 if rhyme[i]!=rhyme[i+1] else 0.0 for i in range(G)]
comb=[0.5*lex[i]+0.5*rhy[i] for i in range(G)]
isb=[sura[i]!=sura[i+1] for i in range(G)]           # true sura boundary?
bi=[i for i in range(G) if isb[i]]; wi=[i for i in range(G) if not isb[i]]
nb=len(bi)
def auc(score):
    # Mann-Whitney AUC: P(score_boundary > score_within)
    sb=sorted((score[i] for i in bi)); sw=sorted((score[i] for i in wi))
    import bisect; tot=0
    for v in sb: tot+=bisect.bisect_left(sw,v)+ (bisect.bisect_right(sw,v)-bisect.bisect_left(sw,v))/2
    return tot/(len(sb)*len(sw))
def perm_z(score):
    real=st.mean(score[i] for i in bi)-st.mean(score[i] for i in wi)
    idx=list(range(G)); ds=[]
    for _ in range(1000):
        random.shuffle(idx); b=idx[:nb]; w=idx[nb:]
        ds.append(st.mean(score[i] for i in b)-st.mean(score[i] for i in w))
    mu=st.mean(ds); sd=st.pstdev(ds) or 1e-9
    return real, (real-mu)/sd
print("ayat:",n," boundaries:",nb," within-gaps:",len(wi))
for name,sc in [("lexical",lex),("rhyme",rhy),("combined",comb)]:
    d,z=perm_z(sc); print(f"  [{name}] boundary mean {st.mean(sc[i] for i in bi):.3f} vs within {st.mean(sc[i] for i in wi):.3f}  Δ={d:+.3f} z={z:+.1f}  AUC={auc(sc):.3f}")
# (B) optimality: is each boundary a local max of combined within ±2?
def localmax_frac(positions):
    c=0
    for p in positions:
        win=[comb[q] for q in range(max(0,p-2),min(G,p+3)) if q!=p]
        if comb[p]>=max(win) if win else True: c+=1
    return c/len(positions)
realLM=localmax_frac(bi)
nulls=[localmax_frac(random.sample(range(G),nb)) for _ in range(1000)]
zLM=(realLM-st.mean(nulls))/(st.pstdev(nulls) or 1e-9)
print(f"  [optimality] boundaries that are local maxima: {realLM:.2f} vs random-cut null {st.mean(nulls):.2f} -> z={zLM:+.1f}")
# al-Kawthar seams
def gap_between(a,b):
    for i in range(G):
        if sura[i]==a and sura[i+1]==b: return i
    return None
allsorted=sorted(comb)
import bisect
for a,b in [(107,108),(108,109)]:
    p=gap_between(a,b)
    pct=100*bisect.bisect_left(allsorted,comb[p])/G
    lm = comb[p]>=max([comb[q] for q in range(max(0,p-2),min(G,p+3)) if q!=p] or [0])
    print(f"  [al-Kawthar {a}|{b}] combined {comb[p]:.2f} (lex {lex[p]:.2f}, rhyme {rhy[p]:.0f}) pct {pct:.0f} localmax {lm}")
print("DONE")
