#!/usr/bin/env python3
"""Step 2, hardened — replicate the SEMANTIC variance-partitioning across subjects (our own
'n=1 isn't enough' lesson). For each subject with two Pieman runs: does semantic structure predict
BOLD BEYOND low-level features (unique_semantic) above its phase-shuffled floor? Aggregate across
subjects with a paired test.

Reuses the validated pieces: encoding_acoustic.load_runs/reliability and encoding_semantic.design/
cross_r2. Word timings from pieman_words.csv (same stimulus for all subjects); GloVe for embeddings.

    python encoding_semantic_multi.py --subs sub-001 ... --words narratives_data\\pieman_words.csv --glove glove.6B.300d.txt

Uses already-downloaded runs in narratives_data\\ (skips subjects whose files aren't present).
"""
import os, sys, json, argparse
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import encoding_acoustic as E
import encoding_semantic as ES

def run_subject(r1,r2,words,onsets,glove,fwhm,rel_pct,maxlag):
    Y1,Y2,tr=E.load_runs(r1,r2,fwhm); T=min(len(Y1),len(Y2)); Y1,Y2=Y1[:T],Y2[:T]
    LOW,SEM=ES.design(words,onsets,tr,T,glove)
    rel=E.reliability(Y1,Y2); keep=rel>=np.percentile(rel,rel_pct)
    meanY=0.5*(Y1[:,keep].mean(1)+Y2[:,keep].mean(1)); env=LOW[:,0]
    best=max(range(0,maxlag+1), key=lambda L: abs(E.corr(np.roll(env,L)[L:],meanY[L:])))
    LOW=np.roll(LOW,best,0); SEM=np.roll(SEM,best,0)
    r_low=ES.cross_r2(LOW,Y1,Y2,keep)
    r_both=ES.cross_r2(np.column_stack([LOW,SEM]),Y1,Y2,keep)
    SEMsh=np.roll(SEM,len(SEM)//2,0)
    r_floor=ES.cross_r2(np.column_stack([LOW,SEMsh]),Y1,Y2,keep)
    return {"R2_low":round(r_low,4),"R2_both":round(r_both,4),
            "unique_sem":round(r_both-r_low,4),"unique_sem_floor":round(r_floor-r_low,4),
            "ceiling_r":round(float(np.mean(rel[keep])),3)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--subs",nargs="+",required=True)
    ap.add_argument("--words",required=True); ap.add_argument("--glove",required=True)
    ap.add_argument("--out",default="narratives_data"); ap.add_argument("--fwhm",type=float,default=8.0)
    ap.add_argument("--rel_pct",type=float,default=98); ap.add_argument("--maxlag",type=int,default=20)
    a=ap.parse_args()
    words,onsets=ES.words_from_csv(a.words); glove=ES.load_glove(a.glove)
    rows=[]
    for s in a.subs:
        r1=os.path.join(a.out,f"{s}_task-pieman_run-1_bold.nii.gz")
        r2=os.path.join(a.out,f"{s}_task-pieman_run-2_bold.nii.gz")
        if not (os.path.exists(r1) and os.path.exists(r2)): print(f"  [skip] {s} (files not present)"); continue
        print(f"subject {s} …"); r=run_subject(r1,r2,words,onsets,glove,a.fwhm,a.rel_pct,a.maxlag)
        r["sub"]=s; rows.append(r); print("  ",json.dumps(r))
    if not rows: raise SystemExit("no subjects completed.")
    uniq=np.array([r["unique_sem"] for r in rows]); fl=np.array([r["unique_sem_floor"] for r in rows])
    d=uniq-fl
    from scipy import stats
    tt=stats.ttest_rel(uniq,fl); dz=float(d.mean()/(d.std(ddof=1)+1e-12))
    summ={"n_subjects":len(rows),"n_unique_above_floor":int((d>0).sum()),
          "unique_sem_mean":round(float(uniq.mean()),4),"unique_sem_floor_mean":round(float(fl.mean()),4),
          "delta_mean":round(float(d.mean()),4),"ttest_p":round(float(tt.pvalue),4),"cohen_dz":round(dz,3),
          "R2_low_mean":round(float(np.mean([r["R2_low"] for r in rows])),4),"per_subject":rows}
    print("\n=== SEMANTIC ACROSS-SUBJECT SUMMARY ===\n"+json.dumps(summ,indent=2))
    print("\nREAD: unique_sem_mean >> floor with small p => meaning predicts BOLD beyond low-level "
          "(semantic signal replicates). unique_sem ≈ floor => robust semantic null (needs ROIs/preproc).")
    json.dump(summ,open(os.path.join(HERE,"encoding_semantic_multi_result.json"),"w"),indent=2)

if __name__=="__main__": main()
