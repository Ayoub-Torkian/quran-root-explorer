#!/usr/bin/env python3
# Phase C — positional instruments (the channels the Phase B nulls demanded).
# (A) ĀYAH positional instrument: a terminal-emission segmentation of the word stream.
#     An āyah end is detected by the running RHYME register, not by marginal stats.
#     Non-circular: model trained on EVEN sūras, tested on ODD (and vice-versa) — an
#     internal split, still the text's own statistics, no external data.
# (B) SEMANTIC channel for L16: add a content-word channel and re-test boundary-load
#     share (3 modalities) to see if it clears the 90 bar.
import glob,unicodedata,numpy as np
from collections import Counter
from scipy.special import gammaln
LN2=np.log(2.0)
DATA=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2/research/two_books_genome/data/quran/quran_arabic_verses.tsv')[0]
def skel(t):
    t=unicodedata.normalize('NFD',t);t=''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
W=[];end=[];wsura=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1);su=int(sa.split(':')[0]);ws=skel(tx)
    for k,w in enumerate(ws):
        W.append(w);end.append(k==len(ws)-1);wsura.append(su)
M=len(W);end=np.array(end);wsura=np.array(wsura)
fin=[w[-1] for w in W]; fa=sorted(set(fin)); fid={c:i for i,c in enumerate(fa)}
FL=np.array([fid[c] for c in fin]); A=len(fa)

# ---------- (A) terminal-emission āyah instrument, 2-fold by sūra parity ----------
def fit_eval(train_mask, test_mask):
    # models from TRAIN
    term=FL[train_mask & end]; anyl=FL[train_mask]
    pt=np.bincount(term,minlength=A)+0.5; pt=pt/pt.sum()
    pa=np.bincount(anyl,minlength=A)+0.5; pa=pa/pa.sum()
    bonus_tab=np.log(pt)-np.log(pa)            # +ve where a letter is rhyme-preferred as a terminal
    mean_len=(train_mask).sum()/max(1,(train_mask&end).sum())
    g=1.0/mean_len                              # geometric length hazard
    logg=np.log(g); log1g=np.log(1-g)
    # test stream (contiguous words of test sūras, in order)
    idx=np.where(test_mask)[0]
    fl=FL[idx]; te=end[idx]; n=len(idx)
    bonus=bonus_tab[fl]
    MAXSEG=60
    # DP: maximise sum over segments of [bonus at terminal + length logprob]
    # cost = -score ; segment (a..j-1], terminal=j-1
    NEG=-1e18; best=np.full(n+1,NEG); best[0]=0.0; back=np.full(n+1,-1,np.int64)
    for j in range(1,n+1):
        lo=max(0,j-MAXSEG); starts=np.arange(lo,j); L=j-starts
        seglp=bonus[j-1] + (L-1)*log1g + logg         # geometric length + terminal rhyme bonus
        cand=best[lo:j]+seglp; k=np.argmax(cand)
        if cand[k]>best[j]: best[j]=cand[k]; back[j]=lo+k
    # backtrace -> predicted ends (transition indices within test stream)
    bnds=[]; j=n
    while j>0:
        i=back[j];
        if i>0: bnds.append(i-1)   # word i-1 is a predicted āyah end (0-based within test)
        j=i
    pred=set(bnds); true=set(np.where(te[:-1])[0])
    tp=len(pred&true); P=tp/len(pred) if pred else 0; R=tp/len(true) if true else 0
    F=2*P*R/(P+R) if P+R else 0
    return P,R,F,len(pred),len(true)
odd=(wsura%2==1); even=(wsura%2==0)
P1,R1,F1,np1,nt1=fit_eval(even,odd)
P2,R2,F2,np2,nt2=fit_eval(odd,even)
P=(P1+P2)/2;R=(R1+R2)/2;F=(F1+F2)/2
print("=== (A) Āyah positional instrument (2-fold, cross-validated, internal split) ===")
print(f" fold1 test=odd  P={P1:.3f} R={R1:.3f} F={F1:.3f}")
print(f" fold2 test=even P={P2:.3f} R={R2:.3f} F={F2:.3f}")
print(f" MEAN            P={P:.3f} R={R:.3f} F={F:.3f}   (marginal-MDL null was P0 0.08, F 0.03)")
# shuffle floor: shuffle final letters, redo
rng=np.random.default_rng(0); FLs=FL.copy(); FLs=FLs[rng.permutation(M)]
FLbak=FL.copy();
def fit_eval_shuf():
    global FL
    FL=FLs; r=fit_eval(even,odd); FL=FLbak; return r
Ps,Rs,Fs,_,_=fit_eval_shuf()
print(f" shuffle floor   P={Ps:.3f} R={Rs:.3f} F={Fs:.3f}  (instrument must beat this)")

# ---------- (B) third (semantic) modality for L16 boundary-load ----------
# verse stream rebuild for boundary-load with symbol+wave+lexical
sura_v=[];fin_v=[];nw_v=[];words_v=[];ALL=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1);su=int(sa.split(':')[0]);ws=skel(tx)
    sura_v.append(su);fin_v.append(ws[-1][-1] if ws and ws[-1] else '');nw_v.append(len(ws));words_v.append(ws);ALL+=ws
Nv=len(sura_v);sura_v=np.array(sura_v)
truth=np.array([sura_v[i+1]!=sura_v[i] for i in range(Nv-1)])
fav=sorted(set(fin_v));fidv={c:i for i,c in enumerate(fav)};FLv=np.array([fidv[c] for c in fin_v]);Afl=len(fav)
edges=np.array([0,1,2,3,4,5,6,8,10,13,17,22,29,38,50,66,87,115,300,10**9]);LB=np.digitize(np.array(nw_v),edges)-1;Alb=LB.max()+1
stop=set(w for w,_ in Counter(ALL).most_common(40)); Vv=300
top=[w for w,_ in Counter([w for w in ALL if w not in stop]).most_common(Vv)]; lid={w:i for i,w in enumerate(top)}
vlx=[[lid.get(w,Vv) for w in ws if w not in stop] for ws in words_v]; Alx=Vv+1
def pref1(ids,Adim):
    P=np.zeros((Nv+1,Adim),np.int64)
    for k in range(Nv):
        P[k+1]=P[k]
        if np.isscalar(ids[k]): P[k+1,ids[k]]+=1
        else:
            for x in ids[k]: P[k+1,x]+=1
    return P
Pfl=pref1(FLv,Afl);Plb=pref1(LB,Alb);Plx=pref1(vlx,Alx);Pw=Plx.sum(1)
ALPHA=0.5; mc=max(Nv,int(Pw[-1]))+5; Gg=gammaln(np.arange(mc)+ALPHA)
Ffl=gammaln(np.arange(mc)+Afl*ALPHA);Flb=gammaln(np.arange(mc)+Alb*ALPHA);Flx=gammaln(np.arange(mc)+Alx*ALPHA)
cfl=gammaln(Afl*ALPHA)-Afl*gammaln(ALPHA);clb=gammaln(Alb*ALPHA)-Alb*gammaln(ALPHA);clx=gammaln(Alx*ALPHA)-Alx*gammaln(ALPHA)
def sc(P,a,b,Ft,k,n=None):
    n=(b-a) if n is None else n
    return float(-(Gg[P[b]-P[a]].sum()+k-Ft[n])/LN2)
lam=6.7
def seg3(a,b):
    return sc(Pfl,a,b,Ffl,cfl)+sc(Plb,a,b,Flb,clb)+sc(Plx,a,b,Flx,clx,int(Pw[b]-Pw[a]))
def share(starts):
    cuts=[0]+sorted(starts)+[Nv];s=t=0
    for m in range(1,len(cuts)-1):
        a,x,b=cuts[m-1],cuts[m],cuts[m+1]; g=(seg3(a,x)+seg3(x,b)+lam)-seg3(a,b); s+=(g<0);t+=1
    return s/t
canon=list(np.where(truth)[0]+1)
real=share(canon)
rng=np.random.default_rng(5)
null=np.array([share(sorted(rng.choice(np.arange(1,Nv),len(canon),replace=False))) for _ in range(60)])
z=(real-null.mean())/null.std()
print("\n=== (B) L16 with 3rd (semantic) modality: boundary-load share ===")
print(f" canonical share load-bearing={real:.3f}  null={null.mean():.3f}±{null.std():.3f}  z={z:.1f}  (3 modalities: symbol+wave+lexical)")
