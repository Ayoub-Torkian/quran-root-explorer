import pandas as pd, numpy as np, json, time
COL_S="ش  سوره"; COL_A="ش  آیه"; COL_R="ریشه نحوی"
df=pd.read_excel("/tmp/Book6_real.xlsx", header=7)
df=df[pd.to_numeric(df[COL_S],errors="coerce").notna()].copy()
roots_per_verse=[set(str(r).split()) for r in df[COL_R].fillna("")]
roots_per_verse=[s for s in roots_per_verse]  # keep all 6236 (incl. empty)
N=len(roots_per_verse)
vocab=sorted({r for s in roots_per_verse for r in s})
vid={r:i for i,r in enumerate(vocab)}; V=len(vocab)
X=np.zeros((N,V),dtype=np.float32)
for i,s in enumerate(roots_per_verse):
    for r in s: X[i,vid[r]]=1.0
L=X.sum(1)  # distinct-root count per verse
df_root=X.sum(0)  # document frequency per root
w=df_root/df_root.sum()

def count_T(Xm, Lm):
    I=Xm @ Xm.T              # intersection counts NxN
    Lsum=Lm[:,None]+Lm[None,:]
    qual=(3.0*I >= Lsum) & (I>0)
    np.fill_diagonal(qual, False)
    T=int(qual.sum()//2)
    S=float((qual.any(1)).mean())
    return T,S

T_obs,S_obs=count_T(X,L)
open("observed.json","w").write(json.dumps({"N":N,"V":V,"T_obs":T_obs,"S_obs":round(S_obs,4)}))
print("OBSERVED T=%d  S=%.4f  (N=%d V=%d)"%(T_obs,S_obs,N,V))

# null
B=300; rng=np.random.RandomState(7); Tn=[]
Lint=L.astype(int)
t0=time.time()
for b in range(B):
    Xn=np.zeros((N,V),dtype=np.float32)
    # Efraimidis-Spirakis weighted sampling w/o replacement, vectorized
    U=rng.random_sample((N,V)).astype(np.float32)
    keys=np.log(U)/w[None,:]          # larger key = selected (log(U)/w, take top-k = largest)
    # pick top L_i per row
    for i in range(N):
        k=Lint[i]
        if k<=0: continue
        idx=np.argpartition(keys[i], -k)[-k:]
        Xn[i, idx]=1.0
    Ln=Xn.sum(1)
    t,_=count_T(Xn,Ln); Tn.append(t)
    if (b+1)%25==0:
        open("progress.txt","w").write("done %d/%d  elapsed %.0fs  mean_null=%.0f\n"%(b+1,B,time.time()-t0,np.mean(Tn)))
Tn=np.array(Tn)
z=(T_obs-Tn.mean())/(Tn.std()+1e-9)
p=(np.sum(Tn>=T_obs)+1)/(B+1)
res={"T_obs":T_obs,"S_obs":round(S_obs,4),"null_mean":round(float(Tn.mean()),1),
     "null_sd":round(float(Tn.std()),1),"z":round(float(z),2),"p":p,
     "ratio":round(T_obs/max(Tn.mean(),1),2),"B":B}
open("results.json","w").write(json.dumps(res,indent=2))
open("progress.txt","w").write("DONE\n"+json.dumps(res,indent=2))
print("RESULT", res)
