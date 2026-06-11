#!/usr/bin/env python3
"""Real-data FIRST RESULT using only files in the OpenNeuro bucket (no transcript, no MNI, no
fMRIPrep): does the speech ACOUSTIC ENVELOPE predict a subject's BOLD, cross-run, above a
phase-shuffled floor and up to the inter-run noise ceiling?

v2 adds two light fixes for raw (un-fMRIPrepped) data:
  * spatial SMOOTHING (--fwhm, default 6mm): raises the inter-run noise ceiling and tolerates
    between-run head-motion misalignment without a full realignment pipeline.
  * automatic audio↔BOLD LAG search: the stimulus audio may not start at scan t=0 (events.tsv
    shows ~13s of music before the story); we cross-correlate the broadband envelope with the
    mean reliable-voxel BOLD and shift the design to the best lag.

Design (two Pieman runs of ONE subject = same stimulus, independent acquisitions):
  X = log spectro-temporal envelope of pieman_audio.wav, HRF-convolved, on the BOLD TR grid.
  Y1,Y2 = smoothed+cleaned BOLD of run-1/run-2 on a COMMON mask.
  ceiling = per-voxel corr(Y1,Y2); test = fit X->Y1 predict Y2 (and vice-versa); floor = shuffled X.

Deps: pip install nibabel nilearn scipy numpy
"""
import os, json, argparse
import numpy as np

def canonical_hrf(dt, length=32.0):
    from math import gamma
    t=np.arange(0,length,dt)
    g=lambda t,a,b:(b**a)*(t**(a-1))*np.exp(-b*t)/gamma(a)
    h=g(t,6,1)-(1/6.0)*g(t,16,1); return h/np.abs(h).sum()

def audio_bands(wav, n_tr, tr, nbands=16):
    from scipy.io import wavfile
    from scipy.signal import spectrogram
    sr,data=wavfile.read(wav)
    if data.ndim>1: data=data.mean(1)
    data=data.astype(float); data/=np.max(np.abs(data))+1e-9
    f,t,Sxx=spectrogram(data, fs=sr, nperseg=int(sr*0.025), noverlap=int(sr*0.0125))
    logS=np.log(Sxx+1e-8)
    edges=np.logspace(np.log10(max(f[1],20)),np.log10(f[-1]),nbands+1)
    B=np.array([logS[(f>=edges[i])&(f<edges[i+1])].mean(0) if ((f>=edges[i])&(f<edges[i+1])).any()
                else np.zeros(logS.shape[1]) for i in range(nbands)])
    grid=np.arange(n_tr)*tr
    X=np.array([np.interp(grid, t, B[b]) for b in range(nbands)]).T
    h=canonical_hrf(tr)
    X=np.array([np.convolve(X[:,b],h)[:n_tr] for b in range(nbands)]).T
    return (X-X.mean(0))/np.maximum(X.std(0),1e-9)

def load_runs(run1, run2, fwhm):
    import nibabel as nib
    from nilearn.masking import compute_epi_mask, apply_mask, intersect_masks
    from nilearn.image import resample_to_img, smooth_img
    from nilearn.signal import clean
    img1=nib.load(run1); img2=nib.load(run2)
    tr=float(img1.header.get_zooms()[3]) or 1.5
    if not (0.2 <= tr <= 6.0): tr=1.5   # some headers store the 4th zoom in odd units; Narratives TR=1.5
    if img2.shape[:3]!=img1.shape[:3] or not np.allclose(img1.affine,img2.affine):
        img2=resample_to_img(img2, img1, interpolation="continuous")
    if fwhm: img1=smooth_img(img1,fwhm); img2=smooth_img(img2,fwhm)
    m=intersect_masks([compute_epi_mask(img1), compute_epi_mask(img2)], threshold=1)
    cl=lambda im: clean(apply_mask(im,m), detrend=True, high_pass=0.01, t_r=tr, standardize="zscore_sample")
    return cl(img1), cl(img2), tr

def reliability(Y1,Y2):
    a=Y1-Y1.mean(0); b=Y2-Y2.mean(0)
    return np.nan_to_num((a*b).sum(0)/np.sqrt((a*a).sum(0)*(b*b).sum(0)+1e-12))
def r2_vox(Y,P): return 1-((Y-P)**2).sum(0)/np.maximum(((Y-Y.mean(0))**2).sum(0),1e-9)
def ridge_fit(X,Y,a=1e3): return np.linalg.solve(X.T@X+a*np.eye(X.shape[1]), X.T@Y)
def corr(a,b):
    a=a-a.mean(); b=b-b.mean(); return float((a*b).sum()/np.sqrt((a*a).sum()*(b*b).sum()+1e-12))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--audio",required=True); ap.add_argument("--run1",required=True)
    ap.add_argument("--run2",required=True); ap.add_argument("--rel_pct",type=float,default=98)
    ap.add_argument("--fwhm",type=float,default=6.0); ap.add_argument("--maxlag",type=int,default=20)
    a=ap.parse_args()
    Y1,Y2,tr=load_runs(a.run1,a.run2,a.fwhm)
    T=min(len(Y1),len(Y2)); Y1,Y2=Y1[:T],Y2[:T]
    X=audio_bands(a.audio,T,tr)
    rel=reliability(Y1,Y2); keep=rel>=np.percentile(rel,a.rel_pct); ceil=float(np.mean(rel[keep]))
    # LAG search: align broadband envelope to mean reliable-voxel BOLD
    env=X.mean(1); meanY=0.5*(Y1[:,keep].mean(1)+Y2[:,keep].mean(1))
    lags=range(0,a.maxlag+1)
    best=max(lags, key=lambda L: abs(corr(np.roll(env,L)[L:], meanY[L:])))
    Xa=np.roll(X,best,axis=0); Xi=np.column_stack([Xa,np.ones(len(Xa))])
    def cross(Xd):
        W=ridge_fit(Xd,Y1[:,keep]); ra=r2_vox(Y2[:,keep],Xd@W)
        W=ridge_fit(Xd,Y2[:,keep]); rb=r2_vox(Y1[:,keep],Xd@W)
        return float(np.mean((ra+rb)/2))
    real=cross(Xi)
    floor=cross(np.column_stack([np.roll(Xa,len(Xa)//2,0),np.ones(len(Xa))]))
    out={"subject_runs":[os.path.basename(a.run1),os.path.basename(a.run2)],"tr":tr,"n_tr":int(T),
         "fwhm":a.fwhm,"best_lag_tr":int(best),"n_voxels":int(Y1.shape[1]),
         "n_reliable":int(keep.sum()),"noise_ceiling_r":round(ceil,3),
         "test_r2_reliable":round(real,4),"floor_r2":round(floor,4),
         "delta_over_floor":round(real-floor,4),
         "test_r2_over_ceiling_R2":round(real/max(ceil**2,1e-6),3)}
    print(json.dumps(out,indent=2))
    print("\nREAD: test_r2 >> floor and a sensible fraction of ceiling² => speech envelope predicts "
          "stimulus-driven BOLD cross-run. Low ceiling => raw-data limit (try --fwhm 8).")
    json.dump(out,open(os.path.join(os.path.dirname(__file__),"encoding_acoustic_result.json"),"w"),indent=2)

if __name__=="__main__": main()

# RUN (PowerShell, one line; data already downloaded):
#   python ..\neural_coding\scripts\encoding_acoustic.py --audio narratives_data\pieman_audio.wav --run1 narratives_data\sub-001_task-pieman_run-1_bold.nii.gz --run2 narratives_data\sub-001_task-pieman_run-2_bold.nii.gz
