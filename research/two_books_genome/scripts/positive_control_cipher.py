#!/usr/bin/env python3
"""POSITIVE CONTROL v2 (validated) — resolves referee M1 & M2.

Plant a substitution cipher into LANGUAGE-structured text (the Arabic letter sequence) and
score candidate decryptions against THAT TEXT'S OWN trigram model (not a foreign model).
Crack with bijection swap-SA. A correct convergence instrument must (a) recover the planted
key and (b) make two independently-cracked disjoint halves agree — both far above chance.

Result (logged 2026-06-09): recovery=1.000, cross-portion convergence=1.000, chance=0.032.
=> The convergence machinery is correct (M2: the genome nulls are NOT search-weakness).
   The same instrument stays at chance when the TARGET is the flat genome (C1, target-side),
   which is why no forward text->genome substitution map is identifiable at ANY Word-side
   granularity. (M1: the framework DOES return a positive when a true signal exists.)
"""
import os, unicodedata, time, json
import numpy as np
HERE=os.path.dirname(__file__); ROOT=os.path.join(HERE,"..")
q=open(os.path.join(ROOT,"data","quran","quran_arabic_concat.txt"),encoding="utf-8").read()
q=unicodedata.normalize("NFD",q); q="".join(c for c in q if not unicodedata.combining(c))
q="".join(c for c in q if "ء"<=c<="ي" and c!="ـ")
alpha=sorted(set(q)); idx={c:i for i,c in enumerate(alpha)}; A=len(alpha)
S=np.array([idx[c] for c in q])

def trimodel(x):
    i=x[:-2]*A*A+x[1:-1]*A+x[2:]; c=np.bincount(i,minlength=A**3).astype(float)+0.2
    return np.log(c/c.sum())
def trilik(x,LP):
    if len(x)<80: return -1e9
    i=x[:-2]*A*A+x[1:-1]*A+x[2:]; return float(LP[i].mean())
def crack(C,LP,seed,iters=40000,restarts=3,T0=0.4):
    rng=np.random.default_rng(seed); gb=-1e9; gm=None
    for _ in range(restarts):
        g=rng.permutation(A); cur=trilik(g[C],LP); best=cur; bm=g.copy()
        for t in range(iters):
            T=T0*(1-t/iters)+1e-3; i,j=int(rng.integers(A)),int(rng.integers(A))
            if i==j: continue
            g[i],g[j]=g[j],g[i]; e=trilik(g[C],LP)
            if e>cur or rng.random()<np.exp((e-cur)/max(T,1e-6)):
                cur=e
                if e>best: best=e; bm=g.copy()
            else: g[i],g[j]=g[j],g[i]
        if best>gb: gb=best; gm=bm
    return gm

def main():
    LP=trimodel(S); rng=np.random.default_rng(0)
    pi=rng.permutation(A); C=pi[S]; truth=np.argsort(pi)
    t=time.time()
    ghat=crack(C[:8000],LP,5); rec=float(np.mean(ghat==truth))
    g1=crack(C[:8000],LP,11); g2=crack(C[8000:16000],LP,12); conv=float(np.mean(g1==g2))
    out={"ts":time.strftime("%Y-%m-%d %H:%M"),"alphabet":A,"recovery":round(rec,3),
         "cross_portion":round(conv,3),"chance":round(1/A,3),"sec":round(time.time()-t,1)}
    print(json.dumps(out,indent=2))
    json.dump(out,open(os.path.join(HERE,"positive_control_cipher_result.json"),"w"),indent=2)

if __name__=="__main__": main()
