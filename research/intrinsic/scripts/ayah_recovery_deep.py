# -*- coding: utf-8 -*-
import re, statistics
from collections import Counter
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import GroupKFold
from sklearn.metrics import roc_auc_score
np.random.seed(0)
VTSV="/sessions/determined-exciting-carson/mnt/Quran_Root_Explorer_Web_v1.2/research/two_books_genome/data/quran/quran_arabic_verses.tsv"
HARAKAT=''.join(map(chr,list(range(0x64B,0x659))+[0x670,0x653,0x654,0x655]+list(range(0x6D6,0x6EE))))
TBL={ord(c):None for c in HARAKAT}; TBL[0x640]=None
def rasm(s):
    s=s.translate(TBL)
    for a,b in [('آ','ا'),('أ','ا'),('إ','ا'),('ٱ','ا'),('ؤ','و'),('ئ','ي'),('ى','ي')]: s=s.replace(a,b)
    return re.sub('[^ء-ي ]','',s).strip()
suras={}
for line in open(VTSV,encoding='utf-8'):
    line=line.rstrip('\r\n')
    if '\t' not in line: continue
    ref,txt=line.split('\t',1); s,a=map(int,ref.split(':'))
    suras.setdefault(s,[]).append(rasm(txt))
LETTERS=list('ابتثجحخدذرزسشصضطظعغفقكلمنهوي ءة'.replace(' ',''))
SUF=['ون','ين','ات','ها','هم','نا','كم','ان','ية','وا']
OPEN=set(['و','ف','ال','قل','يا','ان','اذ','ثم','لا','ما','من','الذين','ولا','وان','يايها'])
LI={c:i for i,c in enumerate(LETTERS)}
X=[];y=[];grp=[]
for s in sorted(suras):
    words=[];ends=set()
    for t in suras[s]:
        w=[x for x in t.split() if x]
        if not w: continue
        words+=w; ends.add(len(words)-1)
    if len(words)<4: continue
    n=len(words)
    f1=Counter(w[-1] for w in words if w); m1=set(k for k,_ in f1.most_common(2))
    f2=Counter(w[-2:] for w in words if len(w)>=2); m2=f2.most_common(1)[0][0] if f2 else ''
    f3=Counter(w[-3:] for w in words if len(w)>=3); m3=f3.most_common(1)[0][0] if f3 else ''
    last_modal=-1
    for i,w in enumerate(words):
        e1=w[-1] if w else ''; e2=w[-2:] if len(w)>=2 else w; e3=w[-3:] if len(w)>=3 else w
        nx=words[i+1] if i+1<n else ''
        feat=[len(w), i/n, 1.0 if i==n-1 else 0,
              1.0 if e1 in m1 else 0, 1.0 if e2==m2 else 0, 1.0 if e3==m3 else 0,
              len(nx), 1.0 if nx in OPEN else 0, 1.0 if (nx[:1] in ('و','ف') ) else 0,
              len(words[i-1]) if i>0 else 0,
              (i-last_modal) if last_modal>=0 else i+1]
        # last-1 letter one-hot (compact: index)
        feat.append(LI.get(e1,-1))
        feat.append(LI.get(nx[:1],-1) if nx else -1)
        # suffix flags
        feat += [1.0 if w.endswith(sf) else 0.0 for sf in SUF]
        X.append(feat); y.append(1 if i in ends else 0); grp.append(s)
        if e1 in m1: last_modal=i
X=np.array(X,float); y=np.array(y); grp=np.array(grp)
print("samples=%d  ayah-ends=%d  base-rate=%.3f  features=%d"%(len(y),y.sum(),y.mean(),X.shape[1]))
gkf=GroupKFold(5); oof=np.zeros(len(y))
for tr,te in gkf.split(X,y,grp):
    clf=HistGradientBoostingClassifier(max_iter=300,learning_rate=0.08,max_depth=None,l2_regularization=1.0,
                                       class_weight='balanced',random_state=0)
    clf.fit(X[tr],y[tr]); oof[te]=clf.predict_proba(X[te])[:,1]
print("AUC (group5CV) = %.3f"%roc_auc_score(y,oof))
P=int(y.sum()); order=np.argsort(-oof)
def ev(ps):
    ps=set(ps); tp=len(ps&set(np.where(y==1)[0].tolist())); rec=tp/P; prec=tp/len(ps) if ps else 0
    return rec,prec,(2*rec*prec/(rec+prec) if rec+prec else 0)
rec,prec,f1=ev(order[:P].tolist()); print("top-%d: recall=%.3f precision=%.3f F1=%.3f"%(P,rec,prec,f1))
best=0;bt=0
for t in np.linspace(oof.min(),oof.max(),100):
    m=np.where(oof>=t)[0]
    if len(m)==0:continue
    f=ev(m.tolist())[2]
    if f>best:best=f;bt=t
m=np.where(oof>=bt)[0]; rec,prec,f1=ev(m.tolist())
print("best-threshold: recall=%.3f precision=%.3f F1=%.3f (preds=%d)"%(rec,prec,f1,len(m)))
print("  vs prior logistic: AUC 0.81 / best-F1 0.39")
