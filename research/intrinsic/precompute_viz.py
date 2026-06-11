#!/usr/bin/env python3
# Precompute CONTENT visuals from the actual text -> viz_data.json (sūra landscape,
# verse-length wave, Arabic onset words, top roots). Rerun when features change.
import glob,unicodedata,json,csv,numpy as np
from collections import Counter
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
BIG=R+'/research/intrinsic/sura_features_big.tsv'; DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
rows=list(csv.DictReader(open(BIG),delimiter='\t'))
feats=[k for k in rows[0] if k!='sura']
X=np.array([[float(r[k]) for k in feats] for r in rows]); suras=[int(r['sura']) for r in rows]
nv=[int(float(r['n_verses'])) for r in rows]
cm=np.nanmean(X,0); ii=np.where(np.isnan(X)); X[ii]=np.take(cm,ii[1])
Xs=np.nan_to_num((X-X.mean(0))/(X.std(0)+1e-9))
from sklearn.decomposition import PCA
Z=PCA(2).fit_transform(Xs)
r=np.corrcoef(Z[:,0],suras)[0,1]
if r<0: Z[:,0]=-Z[:,0]; r=-r
land=[[int(suras[i]),round(float(Z[i,0]),3),round(float(Z[i,1]),3),int(nv[i])] for i in range(len(suras))]
def skel(t):
    t=unicodedata.normalize('NFD',t);t=''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
wl=[]; firstword=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1); su,ay=map(int,sa.split(':')); w=skel(tx); wl.append(len(w))
    if ay==1 and w: firstword.append(w[0])
wl=np.array(wl); step=max(1,len(wl)//700)
wave=[int(x) for x in wl[::step]]
onset=Counter(firstword).most_common(14)
allr=[]
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln: allr+=[x for x in ln.split('\t',1)[1].split() if x and x!='NA']
toproots=Counter(allr).most_common(20)
out={'landscape':land,'pc1_order_r':round(float(r),2),'wave':wave,
     'onset_words':[[w,c] for w,c in onset],'top_roots':[[w,c] for w,c in toproots]}
json.dump(out,open(R+'/research/intrinsic/viz_data.json','w',encoding='utf-8'),ensure_ascii=False)
print('wrote viz_data.json: landscape',len(land),'suras; PC1~order r=',out['pc1_order_r'])
print('onset:',[w for w,_ in onset][:8]); print('roots:',[w for w,_ in toproots][:8])
