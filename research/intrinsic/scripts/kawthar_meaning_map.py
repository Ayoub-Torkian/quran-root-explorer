# -*- coding: utf-8 -*-
"""GROUNDED meaning instrument + rearrangement lens for al-Kawthar's content roots.
(1) self-interpretation: for each root, the distinctive (PPMI) and reliable (P(a|b)) interpreters across the WHOLE corpus.
(2) rearrangement lenses: edit-distance [HUMAN CONSTRUCT] vs co-occurrence semantic distance [divine substrate] — do FORM and MEANING agree?
Computation LOCALIZES/RANKS for human reading; it does not generate meaning."""
import openpyxl, math, itertools
from collections import defaultdict, Counter
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
wb=openpyxl.load_workbook(R+"/Book6.xlsx", read_only=True, data_only=True); ws=wb.active
ayah=[]; k_roots=[]
for r in ws.iter_rows(min_row=9, values_only=True):
    try: s=int(r[5])
    except (TypeError,ValueError): continue
    rt=str(r[8] or "").split()
    ayah.append(set(rt))
    if s==108: k_roots+=rt
Nv=len(ayah)
df=Counter()
for a in ayah:
    for x in a: df[x]+=1
def co(a,b): return sum(1 for s in ayah if a in s and b in s)
# al-Kawthar content roots (dedup, keep order of first appearance), drop pure-structural if any
seen=[]; [seen.append(x) for x in k_roots if x not in seen]
print("al-Kawthar roots (Book6 rasm):", seen, " | df:", {x:df[x] for x in seen})
# function-ish roots to skip as INTERPRETERS (ubiquitous); keep for the target list
STOP={'ال','من','ما','لا','ان','الذ','هو','کل','علی','الی','فی','ب','ل','و','قول','کون'}
def interpreters(b, topn=6):
    out=[]
    for a in df:
        if a==b or a in STOP: continue
        c=co(a,b)
        if c<2: continue
        pab=c/Nv; pa=df[a]/Nv; pb=df[b]/Nv
        ppmi=math.log2(pab/(pa*pb)) if pa*pb>0 else 0
        pcond=c/df[b]              # P(a present | b present)
        out.append((a,c,round(ppmi,2),round(pcond,2)))
    out.sort(key=lambda t:-t[2])   # by distinctiveness (PPMI)
    return out[:topn]
print("\n=== GROUNDED self-interpretation (who interprets each root) ===")
for b in seen:
    if df[b]==0: continue
    ints=interpreters(b)
    tag="HAPAX" if df[b]==1 else f"{df[b]} ayat"
    print(f"\n[{b}] ({tag})  top interpreters  root: PPMI / P(co|root):")
    for a,c,p,pc in ints: print(f"    {a:6} PPMI {p:+.2f}  P {pc:.2f}  (co {c})")
# --- rearrangement lenses over the content roots ---
content=[x for x in seen if x not in STOP and df[x]>0]
def lev(a,b):
    m,n=len(a),len(b); d=[[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1): d[i][0]=i
    for j in range(n+1): d[0][j]=j
    for i in range(1,m+1):
        for j in range(1,n+1):
            d[i][j]=min(d[i-1][j]+1,d[i][j-1]+1,d[i-1][j-1]+(a[i-1]!=b[j-1]))
    return d[m][n]
# semantic vector = co-occurrence profile over all roots (idf-ish via df cap), cosine
def vec(b): return {a:co(a,b) for a in df if a!=b and co(a,b)>0}
def cos(u,v):
    cm=set(u)&set(v); num=sum(u[k]*v[k] for k in cm)
    nu=math.sqrt(sum(x*x for x in u.values())); nv=math.sqrt(sum(x*x for x in v.values()))
    return num/(nu*nv) if nu and nv else 0.0
V={b:vec(b) for b in content}
print("\n=== rearrangement lenses (pairwise) ===")
print("pair            edit-dist[HUMAN]   semantic-cos[divine]")
eds=[]; sims=[]
for a,b in itertools.combinations(content,2):
    e=lev(a,b); s=cos(V[a],V[b]); eds.append(e); sims.append(s)
    print(f"  {a:5}-{b:5}      {e}                {s:.3f}")
# correlation form vs meaning
n=len(eds); me=sum(eds)/n; ms=sum(sims)/n
cov=sum((eds[i]-me)*(sims[i]-ms) for i in range(n))/n
sde=(sum((e-me)**2 for e in eds)/n)**.5; sds=(sum((s-ms)**2 for s in sims)/n)**.5
rho=cov/(sde*sds) if sde and sds else 0
print(f"\nFORM (edit-dist) vs MEANING (co-occurrence) correlation r = {rho:+.2f}")
print("(near 0 => the Qur'an's word-relationships are NOT explained by spelling similarity; meaning is its own axis.)")
