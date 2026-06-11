import numpy as np, csv, unicodedata
from collections import Counter
rows=list(csv.DictReader(open('/sessions/gifted-tender-cori/mnt/Quran_Root_Explorer_Web_v1.2/research/intrinsic/sura_features_big.tsv'),delimiter='\t'))
feats=[k for k in rows[0] if k!='sura']
X=np.array([[float(r[f]) for f in feats] for r in rows]); sura=np.array([int(r['sura']) for r in rows])
X=np.nan_to_num(X); 
keep=[i for i in range(X.shape[1]) if X[:,i].std()>0]; X=X[:,keep]; feats=[feats[i] for i in keep]
Xs=(X-X.mean(0))/X.std(0)
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
p=PCA(15).fit(Xs); Z=p.transform(Xs)
ev=p.explained_variance_ratio_
print("FEATURES used:",len(feats))
print("var PC1-6:",np.round(ev[:6],3),"  cum6=",round(ev[:6].sum(),3))
for pc in range(3):
    L=sorted(zip(feats,p.components_[pc]),key=lambda t:-abs(t[1]))[:7]
    print(f"PC{pc+1} ({ev[pc]*100:.0f}%):"," ".join(f"{n}{'+' if v>0 else '-'}{abs(v):.2f}" for n,v in L))
print("corr(PC1,sura#)=",round(np.corrcoef(Z[:,0],sura)[0,1],3))
# how many PCs to capture 90%
c=np.cumsum(ev); print("PCs for 90% var:",int(np.argmax(c>=0.90)+1))
# UNIVERSE MATCH 1: Zipf law on word frequencies (universal across nature/language)
def skel(t):
    t=unicodedata.normalize('NFD',t); t=''.join(ch for ch in t if not unicodedata.combining(ch))
    return [w for w in (''.join(ch for ch in tok if 'ء'<=ch<='ي' and ch!='ـ') for tok in t.split()) if w]
toks=[]
for ln in open('/sessions/gifted-tender-cori/mnt/Quran_Root_Explorer_Web_v1.2/research/two_books_genome/data/quran/quran_arabic_verses.tsv',encoding='utf-8'):
    if '\t' in ln: toks+=skel(ln.split('\t',1)[1])
fr=np.array(sorted(Counter(toks).values(),reverse=True),float)
rank=np.arange(1,len(fr)+1)
# fit log f = a - b log rank over the body (ranks 10..2000)
mask=(rank>=10)&(rank<=2000)
b,a=np.polyfit(np.log(rank[mask]),np.log(fr[mask]),1)
print(f"ZIPF: slope={b:.2f} (universe/language law ~ -1.0)  vocab={len(fr)} tokens={int(fr.sum())}")
# UNIVERSE MATCH 2: Heaps law (vocab growth V ~ N^beta), universal
import random
N=len(toks); seen=set(); V=[]; Ns=[]
for i,w in enumerate(toks):
    seen.add(w)
    if i%500==0: Ns.append(i+1); V.append(len(seen))
Ns=np.array(Ns[1:]); V=np.array(V[1:])
beta,_=np.polyfit(np.log(Ns),np.log(V),1)
print(f"HEAPS: beta={beta:.2f} (universal vocab-growth exponent, ~0.4-0.6)")
