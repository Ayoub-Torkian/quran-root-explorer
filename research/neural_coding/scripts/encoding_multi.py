#!/usr/bin/env python3
"""Stability check (step 1): run the acoustic-envelope encoding across SEVERAL Narratives 'Pieman'
subjects and test whether envelope > floor replicates. Downloads each subject's two runs if missing
(public OpenNeuro S3, unsigned), reuses the validated pipeline in encoding_acoustic.py.

    python encoding_multi.py --subs sub-001 sub-002 sub-003 sub-004 sub-005 --fwhm 8

Prints a per-subject table + an across-subject paired test (envelope test-R2 vs phase-shuffled floor)
and saves encoding_multi_result.json. Audio (pieman_audio.wav) is downloaded once.
"""
import os, sys, json, argparse, shutil
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
DATA=os.path.join(HERE, "..", "..", "two_books_genome")  # not used; data dir below
OUTDATA=os.path.join(os.getcwd(), "narratives_data")

from botocore import UNSIGNED
from botocore.config import Config
import botocore.session
S3=botocore.session.get_session().create_client("s3", config=Config(signature_version=UNSIGNED))
BUCKET="openneuro.org"; DS="ds002345"

import encoding_acoustic as E   # validated pipeline (load_runs, audio_bands, reliability, ...)

def fetch(key, outdir):
    dst=os.path.join(outdir, os.path.basename(key))
    if os.path.exists(dst) and os.path.getsize(dst)>1000: return dst
    try:
        body=S3.get_object(Bucket=BUCKET, Key=key)["Body"]
        with open(dst,"wb") as f: shutil.copyfileobj(body,f,length=1024*1024)
        return dst
    except Exception as e:
        print(f"  [skip] {key}: {e}"); return None

def run_subject(sub, audio, outdir, fwhm, rel_pct, maxlag):
    r1=fetch(f"{DS}/{sub}/func/{sub}_task-pieman_run-1_bold.nii.gz", outdir)
    r2=fetch(f"{DS}/{sub}/func/{sub}_task-pieman_run-2_bold.nii.gz", outdir)
    if not (r1 and r2): return None
    Y1,Y2,tr=E.load_runs(r1,r2,fwhm); T=min(len(Y1),len(Y2)); Y1,Y2=Y1[:T],Y2[:T]
    X=E.audio_bands(audio,T,tr)
    rel=E.reliability(Y1,Y2); keep=rel>=np.percentile(rel,rel_pct); ceil=float(np.mean(rel[keep]))
    env=X.mean(1); meanY=0.5*(Y1[:,keep].mean(1)+Y2[:,keep].mean(1))
    best=max(range(0,maxlag+1), key=lambda L: abs(E.corr(np.roll(env,L)[L:], meanY[L:])))
    Xa=np.roll(X,best,axis=0); Xi=np.column_stack([Xa,np.ones(len(Xa))])
    def cross(Xd):
        W=E.ridge_fit(Xd,Y1[:,keep]); ra=E.r2_vox(Y2[:,keep],Xd@W)
        W=E.ridge_fit(Xd,Y2[:,keep]); rb=E.r2_vox(Y1[:,keep],Xd@W)
        return float(np.mean((ra+rb)/2))
    real=cross(Xi); floor=cross(np.column_stack([np.roll(Xa,len(Xa)//2,0),np.ones(len(Xa))]))
    return {"sub":sub,"ceiling_r":round(ceil,3),"lag":int(best),"test_r2":round(real,4),
            "floor_r2":round(floor,4),"frac_ceiling":round(real/max(ceil**2,1e-6),3)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--subs", nargs="+", default=["sub-001","sub-002","sub-003","sub-004","sub-005"])
    ap.add_argument("--fwhm", type=float, default=8.0)
    ap.add_argument("--rel_pct", type=float, default=98)
    ap.add_argument("--maxlag", type=int, default=20)
    ap.add_argument("--out", default=OUTDATA)
    a=ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    audio=fetch(f"{DS}/stimuli/pieman_audio.wav", a.out)
    rows=[]
    for s in a.subs:
        print("subject",s,"…")
        r=run_subject(s, audio, a.out, a.fwhm, a.rel_pct, a.maxlag)
        if r: rows.append(r); print("  ",json.dumps(r))
    if not rows: raise SystemExit("no subjects completed.")
    test=np.array([r["test_r2"] for r in rows]); floor=np.array([r["floor_r2"] for r in rows])
    delta=test-floor
    from scipy import stats
    try: w,wp = stats.wilcoxon(test, floor)
    except Exception: w,wp=float("nan"),float("nan")
    tt=stats.ttest_rel(test,floor)
    dz=float(delta.mean()/ (delta.std(ddof=1)+1e-12))           # Cohen's dz (paired effect size)
    summ={"fwhm":a.fwhm,"n_subjects":len(rows),"n_above_floor":int((delta>0).sum()),
          "test_r2_mean":round(float(test.mean()),4),"test_r2_sd":round(float(test.std()),4),
          "floor_r2_mean":round(float(floor.mean()),4),
          "delta_mean":round(float(delta.mean()),4),"delta_sd":round(float(delta.std(ddof=1)),4),
          "frac_ceiling_mean":round(float(np.mean([r["frac_ceiling"] for r in rows])),3),
          "ceiling_r_mean":round(float(np.mean([r["ceiling_r"] for r in rows])),3),
          "wilcoxon_p":round(float(wp),5),"ttest_p":round(float(tt.pvalue),6),
          "cohen_dz":round(dz,3),"per_subject":rows}
    print("\n=== ACROSS-SUBJECT SUMMARY ===\n"+json.dumps(summ,indent=2))
    print("\nREAD: test_r2_mean >> floor_r2_mean with small p => the envelope effect REPLICATES.")
    json.dump(summ, open(os.path.join(HERE,"encoding_multi_result.json"),"w"), indent=2)

if __name__=="__main__": main()
