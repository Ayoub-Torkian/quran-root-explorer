#!/usr/bin/env python3
"""Step 2 — the SEMANTIC arm. Does semantic (word-meaning) structure explain BOLD variance BEYOND
the low-level acoustic/word features? Tested by VARIANCE PARTITIONING, cross-run, on one subject's
two Pieman runs — no preprocessed/MNI data needed.

Word onsets + transcript come from Whisper run on the audio you already have (no external transcript
file required); pass --words <csv> to override with a real alignment if you have one.

Features (all HRF-convolved, lag-aligned, on the TR grid):
  LOW  = word-rate, word-length, vowel-ratio, log-frequency      (acoustic/low-level proxy)
  SEM  = GloVe embedding per word, PCA-reduced to k comps          (meaning)
Partition (cross-run R2 over reliable voxels):
  R2_low, R2_sem, R2_both ; unique_sem = R2_both - R2_low ; floor = phase-shuffled SEM.
A positive semantic result = unique_sem > floor (semantic adds held-out predictive variance).

Deps:  pip install openai-whisper torch  (for word timings)   +  a GloVe txt (glove.6B.300d.txt)
       (already have: nibabel nilearn scipy numpy)
"""
import os, sys, json, argparse
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import encoding_acoustic as E

def words_from_whisper(audio, model="base"):
    import whisper
    from scipy.io import wavfile
    from scipy.signal import resample_poly
    from math import gcd
    print(f"  transcribing {os.path.basename(audio)} with Whisper '{model}' (CPU; a few min)…")
    sr,data=wavfile.read(audio)                      # read WAV ourselves -> no ffmpeg needed
    if data.ndim>1: data=data.mean(1)
    data=data.astype(np.float32); data/=(np.max(np.abs(data))+1e-9)
    if sr!=16000:                                    # Whisper expects 16 kHz mono float32
        g=gcd(int(sr),16000); data=resample_poly(data,16000//g,int(sr)//g).astype(np.float32)
    m=whisper.load_model(model)
    r=m.transcribe(data, word_timestamps=True, language="en")
    W=[]
    for seg in r["segments"]:
        for w in seg.get("words",[]):
            tok="".join(c for c in w["word"].lower() if c.isalpha())
            if tok: W.append((tok, float(w["start"])))
    print(f"  got {len(W)} words")
    return [w for w,_ in W], np.array([t for _,t in W])

def words_from_csv(path):
    import pandas as pd
    sep="\t" if path.endswith((".tsv",".txt")) else ","
    df=pd.read_csv(path,sep=sep); cols={c.lower():c for c in df.columns}
    wc=next(cols[c] for c in ("word","text","token") if c in cols)
    oc=next(cols[c] for c in ("onset","start","start_time","begin") if c in cols)
    w=df[wc].astype(str).str.lower().str.replace(r"[^a-z]","",regex=True)
    on=pd.to_numeric(df[oc],errors="coerce"); k=w.str.len().gt(0)&on.notna()
    return list(w[k]), np.array(on[k],float)

def load_glove(path):
    emb={}; D=0
    for ln in open(path,encoding="utf-8",errors="ignore"):
        p=ln.rstrip().split(" ")
        if len(p)<5: continue
        emb[p[0]]=np.array(p[1:],float); D=len(p)-1
    return emb,D

def impulse_to_tr(words, onsets, weights, tr, n_tr):
    dt=0.1; nf=int(n_tr*tr/dt)+1; v=np.zeros(nf)
    for w,t in zip(weights,onsets):
        j=int(t/dt)
        if 0<=j<nf: v[j]+=w
    h=E.canonical_hrf(tr); conv=np.convolve(v, np.interp(np.arange(0,len(h)*tr,dt), np.arange(len(h))*tr, h))
    idx=np.clip((np.arange(n_tr)*tr/dt).astype(int),0,len(conv)-1)
    return conv[idx]

def design(words, onsets, tr, n_tr, glove, ksem=12):
    from collections import Counter
    fr=Counter(words)
    feats={"rate":[1.0]*len(words),"len":[len(w) for w in words],
           "vowel":[sum(c in "aeiou" for c in w)/max(len(w),1) for w in words],
           "logfreq":[np.log(fr[w]) for w in words]}
    LOW=np.column_stack([impulse_to_tr(words,onsets,feats[k],tr,n_tr) for k in feats])
    emb,D=glove; vecs=np.array([emb.get(w,np.zeros(D)) for w in words])
    SEMraw=np.column_stack([impulse_to_tr(words,onsets,vecs[:,d],tr,n_tr) for d in range(D)])
    # PCA reduce semantic to ksem comps
    Mc=SEMraw-SEMraw.mean(0); U,S,Vt=np.linalg.svd(Mc,full_matrices=False); SEM=Mc@Vt[:ksem].T
    z=lambda M:(M-M.mean(0))/np.maximum(M.std(0),1e-9)
    return z(LOW), z(SEM)

def cross_r2(X,Y1,Y2,keep):
    Xi=np.column_stack([X,np.ones(len(X))])
    W=E.ridge_fit(Xi,Y1[:,keep]); ra=E.r2_vox(Y2[:,keep],Xi@W)
    W=E.ridge_fit(Xi,Y2[:,keep]); rb=E.r2_vox(Y1[:,keep],Xi@W)
    return float(np.mean((ra+rb)/2))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--audio",required=True); ap.add_argument("--run1",required=True)
    ap.add_argument("--run2",required=True); ap.add_argument("--glove",required=True)
    ap.add_argument("--words",default=""); ap.add_argument("--fwhm",type=float,default=8.0)
    ap.add_argument("--rel_pct",type=float,default=98); ap.add_argument("--maxlag",type=int,default=20)
    ap.add_argument("--whisper",default="base")
    a=ap.parse_args()
    Y1,Y2,tr=E.load_runs(a.run1,a.run2,a.fwhm); T=min(len(Y1),len(Y2)); Y1,Y2=Y1[:T],Y2[:T]
    words,onsets=words_from_csv(a.words) if a.words else words_from_whisper(a.audio,a.whisper)
    # save the alignment so step 3 (encoding_real.py --words) can reuse it without re-transcribing
    if not a.words:
        import csv; wp=os.path.join(os.path.dirname(a.run1) or ".","pieman_words.csv")
        with open(wp,"w",newline="",encoding="utf-8") as f:
            wr=csv.writer(f); wr.writerow(["word","onset"])
            for w,t in zip(words,onsets): wr.writerow([w,round(float(t),3)])
        print(f"  saved word alignment -> {wp}")
    LOW,SEM=design(words,onsets,tr,T,load_glove(a.glove))
    rel=E.reliability(Y1,Y2); keep=rel>=np.percentile(rel,a.rel_pct); ceil=float(np.mean(rel[keep]))
    # lag-align using low-level rate vs mean reliable BOLD
    meanY=0.5*(Y1[:,keep].mean(1)+Y2[:,keep].mean(1)); env=LOW[:,0]
    best=max(range(0,a.maxlag+1), key=lambda L: abs(E.corr(np.roll(env,L)[L:],meanY[L:])))
    LOW=np.roll(LOW,best,0); SEM=np.roll(SEM,best,0)
    r_low=cross_r2(LOW,Y1,Y2,keep); r_sem=cross_r2(SEM,Y1,Y2,keep)
    r_both=cross_r2(np.column_stack([LOW,SEM]),Y1,Y2,keep)
    SEMsh=np.roll(SEM,len(SEM)//2,0)
    r_floor=cross_r2(np.column_stack([LOW,SEMsh]),Y1,Y2,keep)
    out={"audio":os.path.basename(a.audio),"n_words":len(words),"tr":tr,"lag":int(best),
         "ceiling_r":round(ceil,3),"R2_low":round(r_low,4),"R2_sem":round(r_sem,4),
         "R2_both":round(r_both,4),"unique_semantic":round(r_both-r_low,4),
         "unique_sem_floor":round(r_floor-r_low,4),"unique_low":round(r_both-r_sem,4)}
    print(json.dumps(out,indent=2))
    print("\nREAD: unique_semantic > unique_sem_floor (and >0) => semantic adds held-out predictive "
          "variance BEYOND low-level features. ~0 => acoustic features already capture it.")
    json.dump(out,open(os.path.join(HERE,"encoding_semantic_result.json"),"w"),indent=2)

if __name__=="__main__": main()

# RUN (PowerShell, one line; needs glove.6B.300d.txt and: pip install openai-whisper torch):
#   python ..\neural_coding\scripts\encoding_semantic.py --audio narratives_data\pieman_audio.wav --run1 narratives_data\sub-001_task-pieman_run-1_bold.nii.gz --run2 narratives_data\sub-001_task-pieman_run-2_bold.nii.gz --glove glove.6B.300d.txt
