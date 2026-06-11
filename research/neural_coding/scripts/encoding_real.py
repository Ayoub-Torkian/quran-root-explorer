#!/usr/bin/env python3
"""Real-data adapter — language encoding model on ONE Narratives 'Pieman' fMRI subject.

Same control stack as the validated simulation (encoding_sim.py): phase-shuffled FLOOR,
held-out time split, and the built-in POSITIVE CONTROL (double dissociation: low-level features
should predict AUDITORY cortex; semantic features should predict the LANGUAGE network). The only
new machinery is what real data needs: (1) load BOLD into ROIs, (2) build word-onset features,
(3) HRF-convolve and resample to the TR grid.

Run locally (data is multi-GB; network is restricted in the assistant sandbox). See RUN section at
the bottom for the exact download + run commands.

Dependencies:  pip install nibabel nilearn numpy pandas
Optional (recommended) semantic features: a GloVe text file (word v1 v2 ... per line). Without it,
the script falls back to a deterministic per-word random vector and SAYS SO (semantic arm is then
only a placeholder — download GloVe for a real test).
"""
import os, sys, json, argparse
import numpy as np

# ----------------------------- config (override via CLI) -----------------------------
TR_DEFAULT = 1.5                      # Narratives TR (seconds)
AUDITORY_COORDS = [(-42,-26,10), (42,-26,10)]            # Heschl's gyrus L/R (MNI)
LANGUAGE_COORDS = [(-54,-48,8), (-48,18,18), (54,-40,4)] # LH pSTS, LH IFG, RH STS (MNI)
SPHERE_R = 8                          # mm

# ----------------------------- shared control math -----------------------------
def r2(Y,P):
    ss=((Y-P)**2).sum(0); tot=((Y-Y.mean(0))**2).sum(0)
    return float(np.mean(1-ss/np.maximum(tot,1e-9)))
def ridge(Xtr,Ytr,Xte,alphas=(1,10,100,1e3,1e4)):
    n=len(Xtr); k=max(n//5,1); best=None; besta=alphas[0]
    for a in alphas:
        Xt,Yt,Xv,Yv=Xtr[:-k],Ytr[:-k],Xtr[-k:],Ytr[-k:]
        Wt=np.linalg.solve(Xt.T@Xt+a*np.eye(Xt.shape[1]),Xt.T@Yt)
        rr=r2(Yv,Xv@Wt)
        if best is None or rr>best: best=rr; besta=a
    Wt=np.linalg.solve(Xtr.T@Xtr+besta*np.eye(Xtr.shape[1]),Xtr.T@Ytr)
    return Xte@Wt
def evaluate(F,Y,shift=None):
    """held-out (contiguous 70/30) R²; shift!=None => phase-shuffled FLOOR."""
    if shift is not None: F=np.roll(F,shift,axis=0)
    F=np.column_stack([F,np.ones(len(F))])                  # intercept
    cut=int(len(F)*0.7)
    P=ridge(F[:cut],Y[:cut],F[cut:]); return r2(Y[cut:],P)

# ----------------------------- HRF + features -----------------------------
def canonical_hrf(dt, length=32.0):
    """double-gamma (SPM-style) sampled at dt seconds."""
    from math import gamma
    t=np.arange(0,length,dt)
    def g(t,a,b): return (b**a)*(t**(a-1))*np.exp(-b*t)/gamma(a)
    h=g(t,6,1)-(1/6.0)*g(t,16,1)
    return h/np.abs(h).sum()
def convolve_to_tr(impulse_fine, dt, tr, n_tr):
    h=canonical_hrf(dt); conv=np.convolve(impulse_fine,h)[:len(impulse_fine)]
    idx=(np.arange(n_tr)*tr/dt).astype(int); idx=np.clip(idx,0,len(conv)-1)
    return conv[idx]
def load_words(path):
    """flexible parser: needs a word column and an onset(start) column (csv/tsv)."""
    import pandas as pd
    sep="\t" if path.endswith((".tsv",".txt")) else ","
    df=pd.read_csv(path,sep=sep)
    cols={c.lower():c for c in df.columns}
    wcol=next((cols[c] for c in ("word","text","token") if c in cols),df.columns[0])
    ocol=next((cols[c] for c in ("onset","start","start_time","begin") if c in cols),df.columns[1])
    w=df[wcol].astype(str).str.lower().str.replace(r"[^a-z']","",regex=True)
    on=pd.to_numeric(df[ocol],errors="coerce")
    keep=w.str.len().gt(0)&on.notna()
    return list(w[keep]), np.array(on[keep],float)
def load_glove(path):
    if not path or not os.path.exists(path): return None,0
    emb={}; D=0
    for ln in open(path,encoding="utf-8",errors="ignore"):
        p=ln.rstrip().split(" ")
        if len(p)<5: continue
        emb[p[0]]=np.array(p[1:],float); D=len(p)-1
    return emb,D
def build_features(words,onsets,tr,n_tr,glove):
    from collections import Counter
    dt=0.1; T=n_tr*tr; nf=int(T/dt)+1
    fr=Counter(words)
    def impulse(weights):
        v=np.zeros(nf)
        for w,t in zip(weights,onsets):
            j=int(t/dt)
            if 0<=j<nf: v[j]+=w
        return v
    # low-level impulse trains -> HRF -> TR grid
    wlen=[len(w) for w in words]; vrat=[sum(c in "aeiou" for c in w)/max(len(w),1) for w in words]
    lf=[np.log(fr[w]) for w in words]; ones=[1.0]*len(words)
    low=np.column_stack([convolve_to_tr(impulse(x),dt,tr,n_tr)
                         for x in [ones,wlen,vrat,lf]])   # rate,length,vowel,logfreq
    # semantic: per-word embedding, HRF-convolved per dimension
    if glove[0] is not None:
        emb,D=glove; vecs=[emb.get(w,np.zeros(D)) for w in words]; placeholder=False
    else:
        D=50; rng=np.random.default_rng(0); types={w:rng.standard_normal(D) for w in set(words)}
        vecs=[types[w] for w in words]; placeholder=True
    vecs=np.array(vecs)
    sem=np.column_stack([convolve_to_tr(impulse(vecs[:,d]),dt,tr,n_tr) for d in range(vecs.shape[1])])
    # z-score columns
    z=lambda M:(M-M.mean(0))/np.maximum(M.std(0),1e-9)
    return z(low), z(sem), placeholder

# ----------------------------- BOLD ROIs -----------------------------
def load_rois(nii):
    from nilearn.maskers import NiftiSpheresMasker
    aud=NiftiSpheresMasker(AUDITORY_COORDS,radius=SPHERE_R,standardize=True).fit_transform(nii)
    lang=NiftiSpheresMasker(LANGUAGE_COORDS,radius=SPHERE_R,standardize=True).fit_transform(nii)
    return {"auditory":aud,"language":lang}

# ----------------------------- main -----------------------------
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--bold",required=True,help="preprocessed BOLD NIfTI (MNI space)")
    ap.add_argument("--words",required=True,help="word-onset csv/tsv (Gentle align)")
    ap.add_argument("--glove",default="",help="optional GloVe txt for real semantic features")
    ap.add_argument("--tr",type=float,default=TR_DEFAULT)
    ap.add_argument("--trim",type=int,default=8,help="TRs to drop at start (lead-in silence)")
    a=ap.parse_args()
    rois=load_rois(a.bold); n_tr=len(next(iter(rois.values())))
    words,onsets=load_words(a.words)
    low,sem,placeholder=build_features(words,onsets,a.tr,n_tr,load_glove(a.glove))
    # drop lead-in
    sl=slice(a.trim,None)
    low,sem=low[sl],sem[sl]; rois={k:v[sl] for k,v in rois.items()}
    feats={"low_level":low,"semantic":sem}
    res={}
    for rn,Y in rois.items():
        res[rn]={}
        for fn,F in feats.items():
            res[rn][fn]={"r2":round(evaluate(F,Y),3),"floor_r2":round(evaluate(F,Y,shift=len(F)//2),3)}
    print(json.dumps(res,indent=2))
    dE=res["auditory"]; dL=res["language"]
    print("\nPOSITIVE CONTROL — expected double dissociation:")
    print("  low-level: auditory %.3f vs language %.3f (expect auditory>>language)"%(dE["low_level"]["r2"],dL["low_level"]["r2"]))
    print("  semantic : language %.3f vs auditory %.3f (expect language>>auditory)"%(dL["semantic"]["r2"],dE["semantic"]["r2"]))
    ok=(dE["low_level"]["r2"]>dL["low_level"]["r2"]) and (dL["semantic"]["r2"]>dE["semantic"]["r2"]) \
       and all(res[r][f]["r2"]>res[r][f]["floor_r2"]+0.02 for r in rois for f in feats if res[r][f]["r2"]>0.05)
    print("DOUBLE DISSOCIATION:",ok, "(placeholder semantic!)" if placeholder else "")
    json.dump({"results":res,"double_dissociation_ok":bool(ok),"placeholder_semantic":placeholder},
              open(os.path.join(os.path.dirname(__file__),"encoding_real_result.json"),"w"),indent=2)

if __name__=="__main__": main()

# ============================ RUN (local) ============================
# 1) deps:
#    pip install nibabel nilearn numpy pandas awscli
# 2) get ONE subject's preprocessed Pieman BOLD + the word-onset file from OpenNeuro ds002345.
#    The fMRIPrep MNI BOLD lives in the derivatives. Browse/download via the OpenNeuro S3 mirror
#    (no credentials needed):
#      aws s3 ls --no-sign-request s3://openneuro.org/ds002345/derivatives/  # find a sub-***/func
#      aws s3 cp --no-sign-request \
#        s3://openneuro.org/ds002345/derivatives/sub-001/func/sub-001_task-pieman_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz .
#    Word onsets (Gentle alignment) ship with the dataset stimuli, e.g.:
#      aws s3 cp --no-sign-request s3://openneuro.org/ds002345/stimuli/gentle/pieman/align.csv .
#    (Exact paths can vary; `aws s3 ls --no-sign-request s3://openneuro.org/ds002345/` to confirm.)
# 3) (recommended) GloVe for real semantic features:
#      curl -L -o glove.6B.zip http://nlp.stanford.edu/data/glove.6B.zip && unzip glove.6B.zip glove.6B.300d.txt
# 4) run:
#      python scripts/encoding_real.py \
#        --bold sub-001_task-pieman_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz \
#        --words align.csv --glove glove.6B.300d.txt
#    Expect: auditory R² high for low-level, language R² high for semantic, both > floor.
# =====================================================================
