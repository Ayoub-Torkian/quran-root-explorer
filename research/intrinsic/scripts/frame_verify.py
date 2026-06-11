#!/usr/bin/env python3
# Verify the period-3 in root-length: is it a real WITHIN-VERSE 3-beat, or an artifact of
# verse boundaries / global structure? Compare real lag-3,6,9 autocorr to (a) within-verse
# shuffle (keeps verse lengths, scrambles internal order) and (b) per-verse periodicity.
import glob,numpy as np,collections
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
verses=[]
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln: verses.append([len(x) for x in ln.split('\t',1)[1].split() if x and x!='NA'])
stream=[x for v in verses for x in v]; stream=np.array(stream,float)
def acf(x,maxlag):
    x=np.asarray(x,float);x=x-x.mean();d=np.dot(x,x)
    return np.array([np.dot(x[:len(x)-k],x[k:])/d for k in range(1,maxlag+1)]) if d>0 else np.zeros(maxlag)
rng=np.random.default_rng(0)
real=acf(stream,9)
# null A: shuffle WITHIN each verse (keeps verse boundaries + lengths, breaks internal order)
def within_shuffle():
    out=[]
    for v in verses: out+= list(rng.permutation(v))
    return out
flA=np.array([acf(within_shuffle(),9) for _ in range(120)])
zA=(real-flA.mean(0))/(flA.std(0)+1e-9)
# null B: global shuffle
flB=np.array([acf(rng.permutation(stream),9) for _ in range(120)])
zB=(real-flB.mean(0))/(flB.std(0)+1e-9)
print("root-length autocorrelation z at lags 1..9:")
print("  vs GLOBAL shuffle:      "+" ".join("L%d:%+.0f"%(k+1,zB[k]) for k in range(9)))
print("  vs WITHIN-VERSE shuffle:"+" ".join("L%d:%+.0f"%(k+1,zA[k]) for k in range(9)))
print("  (if 3/6/9 stay high vs WITHIN-VERSE shuffle -> real sequential 3-beat; if they vanish -> verse-length artifact)")
