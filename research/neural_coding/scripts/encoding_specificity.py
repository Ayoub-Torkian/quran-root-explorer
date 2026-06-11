#!/usr/bin/env python3
"""Stimulus-SPECIFICITY control for the acoustic-envelope positive (referee-grade). For each subject,
predict Pieman BOLD (cross-run) from THREE feature sets and compare:
  REAL      = the Pieman speech envelope (the true stimulus),
  MISMATCH  = a DIFFERENT story's envelope (real, structured speech, but wrong content) — given its
              OWN best lag, i.e. its best shot,
  FLOOR     = phase-shuffled Pieman envelope (autocorrelation/spectrum matched, timing destroyed).
If REAL >> MISMATCH ≈ FLOOR, the encoding is specific to the actual stimulus, not to any speech
envelope — the analog of the genome programme's real-vs-English-vs-random-target controls.

Uses cached Pieman BOLD; needs the mismatch story's audio (e.g. tunnel_audio.wav).
    python encoding_specificity.py --audio narratives_data\\pieman_audio.wav --mismatch narratives_data\\tunnel_audio.wav --subs sub-001 ...
"""
import os, sys, json, argparse
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import encoding_acoustic as E

def best_cross(X, Y1, Y2, keep, meanY, maxlag):
    """give X its best lag, return cross-run R2 over reliable voxels."""
    env=X.mean(1)
    best=max(range(0,maxlag+1), key=lambda L: abs(E.corr(np.roll(env,L)[L:], meanY[L:])))
    Xa=np.roll(X,best,0); Xi=np.column_stack([Xa,np.ones(len(Xa))]); T=len(Xi)
    W=E.ridge_fit(Xi,Y1[:T,keep]); ra=E.r2_vox(Y2[:T,keep],Xi@W)
    W=E.ridge_fit(Xi,Y2[:T,keep]); rb=E.r2_vox(Y1[:T,keep],Xi@W)
    return float(np.mean((ra+rb)/2)), best

def run_subject(r1,r2,audio,mismatch,fwhm,rel_pct,maxlag):
    Y1,Y2,tr=E.load_runs(r1,r2,fwhm); T=min(len(Y1),len(Y2)); Y1,Y2=Y1[:T],Y2[:T]
    Xr=E.audio_bands(audio,T,tr); Xm=E.audio_bands(mismatch,T,tr)
    rel=E.reliability(Y1,Y2); keep=rel>=np.percentile(rel,rel_pct)
    meanY=0.5*(Y1[:,keep].mean(1)+Y2[:,keep].mean(1))
    real,_=best_cross(Xr,Y1,Y2,keep,meanY,maxlag)
    mism,_=best_cross(Xm,Y1,Y2,keep,meanY,maxlag)
    floor,_=best_cross(np.roll(Xr,T//2,0),Y1,Y2,keep,meanY,0)
    return {"real":round(real,4),"mismatch":round(mism,4),"floor":round(floor,4),
            "ceiling_r":round(float(np.mean(rel[keep])),3)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--audio",required=True); ap.add_argument("--mismatch",required=True)
    ap.add_argument("--subs",nargs="+",required=True); ap.add_argument("--out",default="narratives_data")
    ap.add_argument("--fwhm",type=float,default=8.0); ap.add_argument("--rel_pct",type=float,default=98)
    ap.add_argument("--maxlag",type=int,default=20)
    a=ap.parse_args(); rows=[]
    for s in a.subs:
        r1=os.path.join(a.out,f"{s}_task-pieman_run-1_bold.nii.gz")
        r2=os.path.join(a.out,f"{s}_task-pieman_run-2_bold.nii.gz")
        if not (os.path.exists(r1) and os.path.exists(r2)): print(f"  [skip] {s}"); continue
        print(f"subject {s} …"); r=run_subject(r1,r2,a.audio,a.mismatch,a.fwhm,a.rel_pct,a.maxlag)
        r["sub"]=s; rows.append(r); print("  ",json.dumps(r))
    if not rows: raise SystemExit("no subjects.")
    real=np.array([r["real"] for r in rows]); mism=np.array([r["mismatch"] for r in rows]); fl=np.array([r["floor"] for r in rows])
    from scipy import stats
    def pair(a,b):
        d=a-b; return round(float(stats.ttest_rel(a,b).pvalue),5), round(float(d.mean()/(d.std(ddof=1)+1e-12)),3)
    p_rm,dz_rm=pair(real,mism); p_rf,dz_rf=pair(real,fl)
    summ={"n_subjects":len(rows),"real_mean":round(float(real.mean()),4),
          "mismatch_mean":round(float(mism.mean()),4),"floor_mean":round(float(fl.mean()),4),
          "real_gt_mismatch_n":int((real>mism).sum()),"real_vs_mismatch_p":p_rm,"real_vs_mismatch_dz":dz_rm,
          "real_vs_floor_p":p_rf,"real_vs_floor_dz":dz_rf,"per_subject":rows}
    print("\n=== SPECIFICITY SUMMARY ===\n"+json.dumps(summ,indent=2))
    print("\nREAD: real >> mismatch ≈ floor => the encoding is SPECIFIC to the actual stimulus, "
          "not to any speech envelope.")
    json.dump(summ,open(os.path.join(HERE,"encoding_specificity_result.json"),"w"),indent=2)

if __name__=="__main__": main()
