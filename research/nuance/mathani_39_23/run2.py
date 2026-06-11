import pandas as pd, numpy as np, json, time, os
COL_S="ش  سوره"; COL_R="ریشه نحوی"
df=pd.read_excel("/tmp/Book6_real.xlsx", header=7)
df=df[pd.to_numeric(df[COL_S],errors="coerce").notna()].copy()
rpv=[set(str(r).split()) for r in df[COL_R].fillna("")]
N=len(rpv); vocab=sorted({r for s in rpv for r in s}); vid={r:i for i,r in enumerate(vocab)}; V=len(vocab)
X=np.zeros((N,V),np.float32)
for i,s in enumerate(rpv):
    for r in s: X[i,vid[r]]=1.0
L=X.sum(1); Lint=L.astype(int); w=(X.sum(0)/X.sum()).astype(np.float32)
def T_of(Xm,Lm):
    I=Xm@Xm.T; Ls=Lm[:,None]+Lm[None,:]
    q=(3.0*I>=Ls)&(I>0); np.fill_diagonal(q,False); return int(q.sum()//2)
Tobs=T_of(X,L)
f="null_T.json"; Tn=json.load(open(f)) if os.path.exists(f) else []
seed=1000+len(Tn); rng=np.random.RandomState(seed); t0=time.time()
while time.time()-t0<38 and len(Tn)<300:
    U=rng.random_sample((N,V)).astype(np.float32); keys=np.log(U)/w[None,:]
    sk=np.sort(keys,axis=1); cut=sk[np.arange(N),(V-Lint).clip(0,V-1)]
    Xn=(keys>=cut[:,None]).astype(np.float32); Tn.append(T_of(Xn,Xn.sum(1)))
json.dump(Tn,open(f,"w"))
a=np.array(Tn); 
print("accumulated %d/300 | T_obs=%d null mean=%.0f sd=%.0f max=%d | z=%.2f | exceed=%d"%(
   len(Tn),Tobs,a.mean(),a.std(),a.max(),(Tobs-a.mean())/(a.std()+1e-9),int((a>=Tobs).sum())))
