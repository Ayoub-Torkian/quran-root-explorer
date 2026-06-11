import unicodedata, numpy as np
from collections import Counter
def skel(t):
    t=unicodedata.normalize('NFD',t); t=''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
S=[]  # per verse: (sura, final_letter, nwords, contentset)
ALL=[]
for ln in open('/sessions/gifted-tender-cori/mnt/Quran_Root_Explorer_Web_v1.2/research/two_books_genome/data/quran/quran_arabic_verses.tsv',encoding='utf-8'):
    if '\t' not in ln: continue
    sa,tx=ln.split('\t',1); su=int(sa.split(':')[0]); w=skel(tx); ALL+=w
    S.append([su, (w[-1][-1] if w and w[-1] else ''), len(w), w])
stop=set(w for w,_ in Counter(ALL).most_common(40))
for r in S: r[3]=set(x for x in r[3] if x not in stop)
N=len(S); K=4
fin=[r[1] for r in S]; ln_=np.array([r[2] for r in S],float); cs=[r[3] for r in S]
def modal(a):
    c=Counter(a); return c.most_common(1)[0][0] if c else ''
Drh=np.zeros(N-1); Dln=np.zeros(N-1); Dlx=np.zeros(N-1)
for i in range(N-1):
    p=slice(max(0,i-K+1),i+1); q=slice(i+1,min(N,i+1+K))
    Drh[i]=0.0 if modal(fin[p])==modal(fin[q]) else 1.0
    Dln[i]=abs(ln_[q].mean()-ln_[p].mean())
    a=set().union(*cs[p]) if cs[p] else set(); b=set().union(*cs[q]) if cs[q] else set()
    Dlx[i]=1-(len(a&b)/len(a|b) if (a|b) else 0)
z=lambda x:(x-x.mean())/x.std()
D=z(Drh)+z(Dln)+z(Dlx)
truth=np.array([S[i+1][0]!=S[i][0] for i in range(N-1)])  # boundary transitions
# AUC = P(D_boundary > D_internal)
db=D[truth]; di=D[~truth]
auc=np.mean([np.mean(x>di) for x in db]) if len(db) else 0
# precision@#boundaries
nb=truth.sum(); top=np.argsort(-D)[:nb]; prec=truth[top].mean()
d=(db.mean()-di.mean())/np.sqrt((db.var()+di.var())/2)
print(f"transitions={N-1}  true sura-boundaries={nb}")
print(f"AUC(boundary>internal) = {auc:.3f}   Cohen d = {d:.2f}")
print(f"precision@{nb} (top-D transitions that are real boundaries) = {prec:.2f}")
# recall at threshold = mean+2sd
thr=D.mean()+2*D.std(); rec=D[truth]>thr
print(f"recall at (mean+2sd) threshold = {rec.mean():.2f}")
# scale-invariance: detection of the END boundary by sura length
import collections
sura_len=collections.Counter([r[0] for r in S])
# boundary i corresponds to end of sura S[i][0]
det={}
for i in np.where(truth)[0]:
    det.setdefault(S[i][0], D[i])
short=[v for k,v in det.items() if sura_len[k]<15]; long=[v for k,v in det.items() if sura_len[k]>=60]
print(f"boundary-D: short suras(<15v) mean={np.mean(short):.2f}  long(>=60v) mean={np.mean(long):.2f}  (scale-invariant if similar & both>0)")
# what it is NOT: internal max-D within real suras vs boundary-D
import numpy as np
print(f"median boundary-D={np.median(db):.2f}  vs median internal-D={np.median(di):.2f}")
