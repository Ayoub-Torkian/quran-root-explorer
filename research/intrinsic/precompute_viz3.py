#!/usr/bin/env python3
import glob,unicodedata,json,csv,numpy as np
from collections import Counter,defaultdict
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'; BIG=R+'/research/intrinsic/sura_features_big.tsv'
def skel(t):
    t=unicodedata.normalize('NFD',t);t=''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln: k,r=ln.rstrip('\n').split('\t',1); roots[k]=set(x for x in r.split() if x and x!='NA')
sura=[];fin=[];nw=[];vr=[];allw=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1); su=int(sa.split(':')[0]); w=skel(tx)
    sura.append(su);fin.append(w[-1][-1] if w and w[-1] else '');nw.append(len(w));vr.append(roots.get(sa.strip(),set()));allw+=w
N=len(sura);sura=np.array(sura);nw=np.array(nw,float)
truth=np.array([sura[i+1]!=sura[i] for i in range(N-1)]);tset=set(np.where(truth)[0])
# L02 heaps curve
seen=set();hc=[]
for i,w in enumerate(allw):
    seen.add(w)
    if i%400==0: hc.append([i+1,len(seen)])
hc.append([len(allw),len(seen)])
# L08 recurrence ratio vs shuffle, cumulative within window
ids=np.array([hash(w)%200000 for w in allw]);M=len(ids);rng=np.random.default_rng(0)
def recur(seq,W,samp=4000):
    idx=rng.integers(0,len(seq)-W-1,samp); hit=0
    for i in idx: hit+= seq[i] in seq[i+1:i+1+W]
    return hit/samp
rec=[]
sh=ids[rng.permutation(M)]
for W in [2,4,8,16,32,64,128,256,512]:
    r=recur(ids,W); b=recur(sh,W); rec.append([W,round(r/max(b,1e-9),2)])
# L10 clusters on landscape (recompute PCA+KMeans, align to existing landscape order)
rows=list(csv.DictReader(open(BIG),delimiter='\t'));feats=[k for k in rows[0] if k!='sura']
X=np.array([[float(r[k]) for k in feats] for r in rows]);cm=np.nanmean(X,0);ii=np.where(np.isnan(X));X[ii]=np.take(cm,ii[1])
Xs=np.nan_to_num((X-X.mean(0))/(X.std(0)+1e-9))
from sklearn.cluster import KMeans
lab=KMeans(2,n_init=10,random_state=0).fit_predict(Xs)
nvv=np.array([float(r['n_verses']) for r in rows])
short_lab=0 if nvv[lab==0].mean()<nvv[lab==1].mean() else 1
clust={int(rows[i]['sura']):int(0 if lab[i]==short_lab else 1) for i in range(len(rows))}
# L11/L12 discontinuity signal D per transition (rhyme + length + root-distance)
fa=sorted(set(fin));fid={c:i for i,c in enumerate(fa)};FL=np.array([fid[c] for c in fin])
K=4
def modal(a):
    c=Counter(a);return c.most_common(1)[0][0] if c else -1
Drh=np.zeros(N-1);Dln=np.zeros(N-1);Drt=np.zeros(N-1)
for i in range(N-1):
    p=slice(max(0,i-K+1),i+1);q=slice(i+1,min(N,i+1+K))
    Drh[i]=0.0 if modal(FL[p])==modal(FL[q]) else 1.0
    Dln[i]=abs(nw[q].mean()-nw[p].mean())
    a=set().union(*vr[p]) if vr[p] else set();b=set().union(*vr[q]) if vr[q] else set()
    Drt[i]=1-(len(a&b)/len(a|b) if (a|b) else 0)
z=lambda x:(x-x.mean())/(x.std()+1e-9)
D=z(Drh)+z(Dln)+z(Drt)
# L11 hist: D at boundaries vs internal (binned density)
bnd=D[truth];intr=D[~truth]
edges=np.linspace(min(D.min(),-3),min(D.max(),9),22)
hb=np.histogram(bnd,edges,density=True)[0];hi=np.histogram(intr,edges,density=True)[0]
cen=[round(float((edges[i]+edges[i+1])/2),2) for i in range(len(edges)-1)]
disc_hist={'centers':cen,'boundary':[round(float(x),3) for x in hb],'internal':[round(float(x),3) for x in hi]}
# L12 offset curve: mean D at offset from true boundary
offs=range(-5,6);oc=[]
bpos=np.where(truth)[0]
for o in offs:
    idx=[b+o for b in bpos if 0<=b+o<N-1]; oc.append([o,round(float(D[idx].mean()),2)])
# L16 seams hard/soft: top ~35% of boundary D = hard
bd=D[truth];thr=np.quantile(bd,0.65);seams=[1 if v>=thr else 0 for v in bd]
# L07 rhyme->theme: adjacent pairs sharing final letter vs not -> mean root jaccard
def jac(a,b): u=len(a|b); return len(a&b)/u if u else 0
sh_j=[];no_j=[]
for i in range(N-1):
    j=jac(vr[i],vr[i+1])
    (sh_j if fin[i]==fin[i+1] else no_j).append(j)
P=R+'/research/intrinsic/viz_data.json';v=json.load(open(P,encoding='utf-8'))
# attach cluster to landscape entries
for e in v['landscape']: e.append(clust.get(e[0],0))
v.update({'heaps':hc,'recurrence2':rec,'disc_hist':disc_hist,'disc_offset':oc,'seams':seams,
          'rhyme_theme':{'share':round(float(np.mean(sh_j)),3),'noshare':round(float(np.mean(no_j)),3)}})
json.dump(v,open(P,'w',encoding='utf-8'),ensure_ascii=False)
print('heaps pts',len(hc),'| recurrence',rec[:3],'| clusters short=%d long=%d'%(sum(1 for x in clust.values() if x==0),sum(1 for x in clust.values() if x==1)))
print('disc_offset peak@0:',oc[5],'| seams hard=%d/%d'%(sum(seams),len(seams)),'| rhyme-theme',v['rhyme_theme'])
