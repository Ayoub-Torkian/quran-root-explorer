import json,re,math,numpy as np
import analysis as A, spatial_patterns as SP
from collections import defaultdict,Counter
c=A.load_corpus('Book6.xlsx'); N=len(c.df)
su=[int(c.df[A.COL_SURAH].iat[i]) for i in range(N)]
ay=[int(c.df[A.COL_AYAH].iat[i]) for i in range(N)]
W=SP.contiguity_W(114)
def tally(tbr,K,rowmask):
    yl=defaultdict(list); cnt=defaultdict(lambda:np.zeros(115)); fr=Counter()
    for i in range(N):
        if not rowmask[i]: continue
        toks=tbr[i]
        if not toks: continue
        seen=set()
        for t in toks:
            r=K(t)
            if not r: continue
            if r not in seen: seen.add(r); fr[r]+=1
            yl[r].append(i)
            s=su[i]
            if 1<=s<=114: cnt[r][s]+=1
    rows=[]
    for r,f in fr.items():
        if f<8: continue
        ys=sorted(yl[r])
        if len(ys)<4: continue
        g=[ys[k+1]-ys[k] for k in range(len(ys)-1)]
        fano=SP._fano_factor(g); vec=cnt[r][1:115]
        rows.append((fano,int((vec>0).sum())/114,SP.morans_I_analytic(vec,W)['klass']))
    m=len(rows) or 1
    p=lambda pr: round(100*sum(1 for x in rows if pr(x))/m,1)
    return dict(n_roots=len(rows),local_clustered=p(lambda x:x[0]>1.5),
        mean_coverage=round(float(np.mean([x[1] for x in rows])),3) if rows else 0.0,
        I_clustered=p(lambda x:x[2]=='clustered'),I_regular=p(lambda x:x[2]=='regular'),
        I_random=p(lambda x:x[2]=='random'))
def scr(tbr,seed,rowmask):
    rng=np.random.default_rng(seed)
    idx=[i for i in range(N) if rowmask[i]]
    flat=[t for i in idx for t in tbr[i]]; rng.shuffle(flat)
    out=[[] for _ in range(N)]; k=0
    for i in idx:
        n=len(tbr[i]); out[i]=flat[k:k+n]; k+=n
    return out
def runlang(tbr,K,rowmask):
    real=tally(tbr,K,rowmask)
    ks=['local_clustered','mean_coverage','I_clustered','I_regular','I_random']
    sims={k:[] for k in ks}
    for sd in range(3):
        s=tally(scr(tbr,sd,rowmask),K,rowmask)
        for k in ks: sims[k].append(s[k])
    null={k:(round(float(np.mean(v)),2),round(float(np.std(v)),2)) for k,v in sims.items()}
    verd={}
    for k in ks:
        mu,sd=null[k]; d=real[k]-mu
        z=d/sd if sd>0 else (float('inf') if abs(d)>1e-6 else 0.0)
        verd[k]=dict(real=real[k],null_mean=mu,null_sd=sd,diff=round(d,2),
            z=round(z,1) if math.isfinite(z) else None,
            beyond_chance=bool(abs(z)>=2) if math.isfinite(z) else True)
    return dict(real=real,null={k:null[k][0] for k in ks},verdict=verd)

# ARABIC: all rows
allmask=[True]*N
ar=runlang(c.surface_tokens,A.normalize_letters,allmask)

# ENGLISH: from collected (surah,ayah)->text
enc=json.load(open('.stage/en_collected.json',encoding='utf-8'))
endict={}
for k,v in enc.items():
    s,a=k.split(':'); endict[(int(s),int(a))]=v
def en_tok(text):
    return re.findall(r"[a-z]+", text.lower())
en_tbr=[[] for _ in range(N)]; enmask=[False]*N
for i in range(N):
    t=endict.get((su[i],ay[i]))
    if t is not None:
        en_tbr[i]=en_tok(t); enmask[i]=True
en_cov=sum(enmask)
ident=lambda x:x
en=runlang(en_tbr,ident,enmask)
en_cov_pct=round(100*en_cov/N,1)

import datetime
out={"generated":"2026-06-04",
 "method":"word-type, unit=surah, mushaf, min_freq=8, vs frequency-matched scramble (3 seeds)",
 "langs":{
   "arabic":{"coverage_pct":100.0,"ayahs_matched":N,"real":ar['real'],"null":ar['null'],"verdict":ar['verdict']},
   "english":{"coverage_pct":en_cov_pct,"ayahs_matched":en_cov,
     "note":"Sahih International (Umm Muhammad) via fawazahmed0/quran-api; only fully-saved surahs 2,3,4,7 retrievable within tool limits","real":en['real'],"null":en['null'],"verdict":en['verdict']},
   "persian":{"coverage_pct":0.0,"ayahs_matched":0,
     "note":"Not sourced at scale: fawazahmed0 has Ansarian (fas-hussainansarian) and tanzil.net serves Fooladvand, but the web_fetch ~112KB/token cap and lack of a range/offset endpoint made assembling all 6236 ayahs infeasible without exhausting context. Arabic+English provided per task allowance.","real":None,"null":None,"verdict":None}
 }}
json.dump(out,open('benchmark_translations.json','w'),ensure_ascii=False,indent=1)
print("=== ARABIC real ===",json.dumps(ar['real']))
print("=== ARABIC null ===",json.dumps(ar['null']))
print("=== ENGLISH cov% ===",en_cov_pct,"ayahs",en_cov)
print("=== ENGLISH real ===",json.dumps(en['real']))
print("=== ENGLISH null ===",json.dumps(en['null']))
import os
print("BYTES",os.path.getsize('benchmark_translations.json'))
