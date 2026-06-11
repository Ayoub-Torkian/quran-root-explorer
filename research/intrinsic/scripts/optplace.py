import unicodedata, numpy as np
from collections import Counter
def skel(t):
    t=unicodedata.normalize('NFD',t); t=''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
S=[]; ALL=[]
for ln in open('/sessions/gifted-tender-cori/mnt/Quran_Root_Explorer_Web_v1.2/research/two_books_genome/data/quran/quran_arabic_verses.tsv',encoding='utf-8'):
    if '\t' not in ln: continue
    sa,tx=ln.split('\t',1); su=int(sa.split(':')[0]); w=skel(tx); ALL+=w
    S.append([su,(w[-1][-1] if w and w[-1] else ''),len(w),w])
stop=set(w for w,_ in Counter(ALL).most_common(40))
for r in S: r[3]=set(x for x in r[3] if x not in stop)
N=len(S); K=4; fin=[r[1] for r in S]; ln_=np.array([r[2] for r in S],float); cs=[r[3] for r in S]
def modal(a):
    c=Counter(a); return c.most_common(1)[0][0] if c else ''
Drh=np.zeros(N-1);Dln=np.zeros(N-1);Dlx=np.zeros(N-1)
for i in range(N-1):
    p=slice(max(0,i-K+1),i+1);q=slice(i+1,min(N,i+1+K))
    Drh[i]=0.0 if modal(fin[p])==modal(fin[q]) else 1.0
    Dln[i]=abs(ln_[q].mean()-ln_[p].mean())
    a=set().union(*cs[p]) if cs[p] else set(); b=set().union(*cs[q]) if cs[q] else set()
    Dlx[i]=1-(len(a&b)/len(a|b) if (a|b) else 0)
z=lambda x:(x-x.mean())/x.std(); D=z(Drh)+z(Dln)+z(Dlx)
truth=np.array([S[i+1][0]!=S[i][0] for i in range(N-1)]); B=np.where(truth)[0]
for w in (1,2,3):
    lm=[]
    for i in B:
        lo=max(0,i-w);hi=min(N-1,i+w+1); lm.append(D[i]==D[lo:hi].max())
    base=1/(2*w+1)
    print(f"local-max within +/-{w}: true boundaries {100*np.mean(lm):.0f}%   (chance {100*base:.0f}%)")
# move-by-one penalty: D at boundary vs at boundary+-1
pen=[]
for i in B:
    nb=[D[j] for j in (i-1,i+1) if 0<=j<N-1]; pen.append(D[i]-np.mean(nb))
print(f"move-by-one penalty (D_true - D_neighbor), mean={np.mean(pen):.2f}  >0 in {100*np.mean(np.array(pen)>0):.0f}% of boundaries")
