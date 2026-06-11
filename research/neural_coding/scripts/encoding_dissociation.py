#!/usr/bin/env python3
"""Step 3 (v3) — auditory-vs-language DOUBLE DISSOCIATION on real fMRI, registration-robust.
Run in the py3.11 conda env (see STEP3.md).

v3 fixes v2's unreliable point-sphere ROIs (auditory reliability was 0.018):
  * SyN (affine+nonlinear) registration of mean EPI -> MNI,
  * warp BOLD into MNI, then use ANATOMICAL atlas regions (Harvard-Oxford): AUDITORY = Heschl's
    gyrus; LANGUAGE = IFG + posterior STG/MTG + angular gyrus,
  * within each region keep only the RELIABLE voxels (top inter-run correlation) — robust to
    imperfect registration and gives a real noise ceiling per ROI,
  * gated verdict: trust the dissociation only if the auditory ROI is actually reliable and the
    margins exceed noise. Otherwise INCONCLUSIVE -> needs fMRIPrep.
"""
import os, json, argparse, tempfile
import numpy as np

def canonical_hrf(dt,length=32.0):
    from math import gamma; t=np.arange(0,length,dt)
    g=lambda t,a,b:(b**a)*(t**(a-1))*np.exp(-b*t)/gamma(a)
    h=g(t,6,1)-(1/6.0)*g(t,16,1); return h/np.abs(h).sum()

def main():
    import nibabel as nib, ants
    from nilearn.datasets import load_mni152_template, fetch_atlas_harvard_oxford
    from nilearn.image import resample_to_img
    from nilearn.signal import clean
    ap=argparse.ArgumentParser()
    ap.add_argument("--run1",required=True); ap.add_argument("--run2",required=True)
    ap.add_argument("--words",required=True); ap.add_argument("--glove",required=True)
    ap.add_argument("--keep_pct",type=float,default=50)
    a=ap.parse_args(); tmp=tempfile.mkdtemp()

    img1=nib.load(a.run1); tr=float(img1.header.get_zooms()[3]); tr=tr if 0.2<=tr<=6 else 1.5
    mean1=nib.Nifti1Image(img1.get_fdata().mean(-1), img1.affine)
    mni=load_mni152_template(resolution=2)
    nib.save(mni,os.path.join(tmp,"mni.nii.gz")); nib.save(mean1,os.path.join(tmp,"epi.nii.gz"))
    mni_a=ants.image_read(os.path.join(tmp,"mni.nii.gz")); epi_a=ants.image_read(os.path.join(tmp,"epi.nii.gz"))
    print("registering mean EPI -> MNI (SyN)…")
    reg=ants.registration(mni_a, epi_a, type_of_transform="SyNRA")
    def warp(run,tag):
        w=ants.apply_transforms(mni_a, ants.image_read(run), transformlist=reg["fwdtransforms"], imagetype=3)
        p=os.path.join(tmp,tag+".nii.gz"); ants.image_write(w,p); return nib.load(p)
    w1=warp(a.run1,"r1"); w2=warp(a.run2,"r2")

    # anatomical ROIs from Harvard-Oxford, resampled to the warped BOLD grid
    ho=fetch_atlas_harvard_oxford("cort-maxprob-thr25-2mm"); labels=ho.labels
    atl=resample_to_img(ho.maps, nib.Nifti1Image(w1.get_fdata()[...,0],w1.affine), interpolation="nearest")
    A=np.asarray(atl.get_fdata()).astype(int)
    def idxs(names): return [i for i,l in enumerate(labels) if any(n.lower() in l.lower() for n in names)]
    aud=np.isin(A, idxs(["Heschl"]))
    lang=np.isin(A, idxs(["Inferior Frontal Gyrus","Superior Temporal Gyrus, posterior",
                          "Middle Temporal Gyrus, posterior","Angular Gyrus"]))
    print(f"atlas voxels: auditory={int(aud.sum())} language={int(lang.sum())}")
    def series(w,mask):
        Y=w.get_fdata()[mask]                                  # (V,T)
        return clean(Y.T, detrend=True, high_pass=0.01, t_r=tr, standardize="zscore_sample")
    def roi(mask):
        y1=series(w1,mask); y2=series(w2,mask); T=min(len(y1),len(y2)); y1,y2=y1[:T],y2[:T]
        a_=y1-y1.mean(0); b_=y2-y2.mean(0)
        rel=np.nan_to_num((a_*b_).sum(0)/np.sqrt((a_*a_).sum(0)*(b_*b_).sum(0)+1e-12))
        keep=rel>=np.percentile(rel,a.keep_pct)
        return y1[:,keep],y2[:,keep],float(np.mean(rel[keep])),T
    Aud=roi(aud); Lang=roi(lang); T=min(Aud[3],Lang[3])

    # features
    import pandas as pd
    df=pd.read_csv(a.words); words=df["word"].astype(str).tolist(); onsets=df["onset"].astype(float).values
    emb={}; D=0
    for ln in open(a.glove,encoding="utf-8",errors="ignore"):
        q=ln.rstrip().split(" ")
        if len(q)>=5: emb[q[0]]=np.array(q[1:],float); D=len(q)-1
    from collections import Counter; fr=Counter(words); dt=0.1; nf=int(T*tr/dt)+1
    def imp(w):
        v=np.zeros(nf)
        for ww,t in zip(w,onsets):
            j=int(t/dt)
            if 0<=j<nf: v[j]+=ww
        h=canonical_hrf(tr); c=np.convolve(v,np.interp(np.arange(0,len(h)*tr,dt),np.arange(len(h))*tr,h))
        return c[np.clip((np.arange(T)*tr/dt).astype(int),0,len(c)-1)]
    LOW=np.column_stack([imp([1.0]*len(words)),imp([len(x) for x in words]),imp([np.log(fr[x]) for x in words])])
    vecs=np.array([emb.get(x,np.zeros(D)) for x in words])
    SEMraw=np.column_stack([imp(vecs[:,d]) for d in range(D)])
    Mc=SEMraw-SEMraw.mean(0); U,S,Vt=np.linalg.svd(Mc,full_matrices=False); SEM=Mc@Vt[:12].T
    z=lambda M:(M-M.mean(0))/np.maximum(M.std(0),1e-9); LOW,SEM=z(LOW),z(SEM)

    def r2(Yt,P): return float(np.mean(1-((Yt-P)**2).sum(0)/np.maximum(((Yt-Yt.mean(0))**2).sum(0),1e-9)))
    def cross(X,y1,y2):
        Xi=np.column_stack([X[:T],np.ones(T)])
        W=np.linalg.solve(Xi.T@Xi+1e2*np.eye(Xi.shape[1]),Xi.T@y1[:T]); ra=r2(y2[:T],Xi@W)
        W=np.linalg.solve(Xi.T@Xi+1e2*np.eye(Xi.shape[1]),Xi.T@y2[:T]); rb=r2(y1[:T],Xi@W)
        return (ra+rb)/2
    res={"auditory":{"low":round(cross(LOW,Aud[0],Aud[1]),4),"sem":round(cross(SEM,Aud[0],Aud[1]),4)},
         "language":{"low":round(cross(LOW,Lang[0],Lang[1]),4),"sem":round(cross(SEM,Lang[0],Lang[1]),4)}}
    rel={"auditory":round(Aud[2],3),"language":round(Lang[2],3)}
    print(json.dumps(res,indent=2)); print("ROI reliability (reliable voxels):",rel)
    M=0.01
    ordering=(res["auditory"]["low"]>res["language"]["low"]) and (res["language"]["sem"]>res["auditory"]["sem"])
    trust=(rel["auditory"]>0.1 and res["auditory"]["low"]>0.02
           and (res["auditory"]["low"]-res["language"]["low"])>M
           and (res["language"]["sem"]-res["auditory"]["sem"])>M and res["language"]["sem"]>0)
    verdict="dissociation" if (ordering and trust) else \
        "INCONCLUSIVE — ROI reliability/margins at noise level (raw single-subject; needs fMRIPrep)"
    print("QC low→auditory:",res["auditory"]["low"],"| auditory reliability:",rel["auditory"])
    print("VERDICT:",verdict)
    json.dump({"results":res,"roi_reliability":rel,"ordering_only":bool(ordering),
               "trustworthy":bool(trust),"verdict":verdict},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"encoding_dissociation_result.json"),"w"),indent=2)

if __name__=="__main__": main()
