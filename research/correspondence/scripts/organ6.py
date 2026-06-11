#!/usr/bin/env python3
# SURA-as-ORGAN: prove INTRA-organ and INTER-organ organization (clean, size-normalized).
import collections, random
import numpy as np
random.seed(1); np.random.seed(1)
RBA="research/two_books_genome/roots_by_ayah.tsv"
V=[]  # (sura,ayah,[roots]) in order, valid suras only
for ln in open(RBA,encoding='utf-8'):
    if '\t' not in ln: continue
    k,r=ln.rstrip('\n').split('\t',1)
    try: s,a=k.split(':'); s=int(s); a=int(a)
    except: continue
    if not (1<=s<=114): continue
    V.append((s,a,[x for x in r.split() if x and x!='NA']))
suras=sorted(set(s for s,_,_ in V)); S=len(suras); idx={s:i for i,s in enumerate(suras)}
print(f"loaded {len(V)} verses, {S} suras (expect 114)")
df=collections.Counter()
for _,_,rs in V:
    for r in set(rs): df[r]+=1

# ===== INTRA-ORGAN: internal organization (verses work together; framed unit) =====
within=[]; across=[]
for i in range(len(V)-1):
    a=set(V[i][2]); b=set(V[i+1][2]); sh=len(a&b)
    (within if V[i][0]==V[i+1][0] else across).append(sh)
print("\n[INTRA] internal weave — adjacent verses share roots:")
print(f"   within-sura {np.mean(within):.3f}  vs  across-boundary {np.mean(across):.3f}  ratio={np.mean(within)/max(np.mean(across),1e-9):.2f}x  (organ coheres inside, breaks at edge)")
# onset framing: first verse vs interior — fresh-root rate (a sura opens distinctly)
seen=set(); onset=[]; interior=[]
cur=None
for s,a,rs in V:
    fresh=sum(1 for r in set(rs) if r not in seen)/max(len(set(rs)),1)
    (onset if a==1 else interior).append(fresh)
    seen|=set(rs)
print(f"[INTRA] onset framing — first-verse fresh-root rate {np.mean(onset):.2f} vs interior {np.mean(interior):.2f} (a sura opens on new material)")

# ===== INTER-ORGAN: system organization =====
# (A) IDENTITY / division of labor: unique markers
uniq=collections.Counter()
root_sura={}
for s,_,rs in V:
    for r in rs: root_sura.setdefault(r,set()).add(s)
for r,ss in root_sura.items():
    if len(ss)==1: uniq[next(iter(ss))]+=1
has=sum(1 for s in suras if uniq[s]>0)
print(f"\n[INTER-A] IDENTITY — {has}/{S} suras ({has/S:.0%}) carry >=1 unique marker root (distinct function).")

# size-normalized connectivity: association A[i,j]=shared rare roots / sqrt(deg_i deg_j)
rare=[r for r,d in df.items() if 2<=d<=60]
sroots=[set(r for r in (set().union(*[set(rs) for ss,aa,rs in V if ss==sx]) ) if r in rare) for sx in suras]
M=np.zeros((S,S))
for r in rare:
    h=[idx[s] for s in root_sura[r] if s in idx]
    for x in range(len(h)):
        for y in range(x+1,len(h)): M[h[x],h[y]]+=1; M[h[y],h[x]]+=1
deg=M.sum(1)+1e-9
A=M/np.sqrt(np.outer(deg,deg))
# (B) specific connectivity: named classical twin pairs should score high
pairs={"113-114 mu'awwidhatan":(113,114),"105-106 Fil/Quraysh":(105,106),"93-94 Duha/Sharh":(93,94),
       "73-74 Muzzammil/Muddathir":(73,74),"2-3 Baqara/ImrAn":(2,3),"8-9 Anfal/Tawba":(8,9)}
allv=A[np.triu_indices(S,1)]; 
print(f"\n[INTER-B] CONNECTIVITY — size-normalized association; do KNOWN twin pairs rank high?  (median pair pct):")
for nm,(p,q) in pairs.items():
    if p in idx and q in idx:
        v=A[idx[p],idx[q]]; pct=(allv<v).mean()
        print(f"   {nm}: assoc pctile = {pct:.0%}")
# (C) LOCATION: canonical neighbours associate above random order (size-normalized)
adj=np.mean([A[i,i+1] for i in range(S-1)])
nulls=np.array([np.mean([A[p[i],p[i+1]] for i in range(S-1)]) for p in (np.random.permutation(S) for _ in range(400))])
print(f"\n[INTER-C] LOCATION — neighbour association {adj:.3f} vs random-order {nulls.mean():.3f}±{nulls.std():.3f}  z={(adj-nulls.mean())/nulls.std():+.1f}")
# position determined by profile: PC1 of keyness signatures vs canonical order
Sig=np.zeros((S,len(rare))); ri={r:i for i,r in enumerate(rare)}
for s,_,rs in V:
    for r in rs:
        if r in ri: Sig[idx[s],ri[r]]+=1
Sig=Sig/ (Sig.sum(1,keepdims=True)+1e-9)
Sig-=Sig.mean(0)
U,sv,Vt=np.linalg.svd(Sig,full_matrices=False)
pc1=U[:,0]; r=np.corrcoef(pc1,np.arange(S))[0,1]
print(f"[INTER-C] position from profile — PC1 vs canonical order |r|={abs(r):.2f} (L09-style: location written into the statistics)")
