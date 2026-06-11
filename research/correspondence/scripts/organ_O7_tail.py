#!/usr/bin/env python3
# O7 tail — settle the CLOSING cadence with a better instrument than 'common vocab' (which read 0.54).
import unicodedata, collections, math
import numpy as np
AR=set(chr(c) for c in range(0x621,0x64B))
def rasm(s): return ''.join(c for c in unicodedata.normalize('NFD',s) if c in AR)
RBA="research/two_books_genome/roots_by_ayah.tsv"; TX="research/two_books_genome/data/quran/quran_arabic_verses.tsv"
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln: k,r=ln.rstrip('\n').split('\t',1); roots[k]=[x for x in r.split() if x and x!='NA']
wc={}; 
for ln in open(TX,encoding='utf-8'):
    if '\t' in ln:
        sa,tx=ln.split('\t',1); wc[sa]=len([w for w in (rasm(x) for x in tx.split()) if w])
# order
keys=[]; bys=collections.defaultdict(list)
for ln in open(TX,encoding='utf-8'):
    if '\t' in ln:
        sa=ln.split('\t',1)[0]; s=int(sa.split(':')[0]); keys.append(sa); bys[s].append(sa)
df=collections.Counter()
for k,rs in roots.items():
    for r in set(rs): df[r]+=1
N=len(keys)
DIV={'ءله','ربب'}; ATTR={'غفر','رحم','علم','حكم','عزز','قدر','سمع','بصر','رحب','ودد','حمد','عظم','کبر','تبب','غنی'}
rows=[]
for s,ks in bys.items():
    n=len(ks)
    for pos,k in enumerate(ks):
        rs=roots.get(k,[]); 
        comm=np.mean([math.log(df[r]) for r in rs]) if rs else 0
        ndiv=sum(1 for r in rs if r in DIV); nattr=sum(1 for r in rs if r in ATTR)
        rows.append((1 if pos==n-1 else 0, comm, wc.get(k,len(rs)), ndiv, nattr))
rows=np.array(rows,float); y=rows[:,0]
def auc(score):
    o=np.argsort(score); r=np.empty(len(score)); r[o]=np.arange(1,len(score)+1)
    n1=y.sum(); n0=len(y)-n1; return (r[y==1].sum()-n1*(n1+1)/2)/(n1*n0)
print("O7 TAIL — last-verse detection (closing cadence), by indicator:")
print(f"   root-commonness (L26 'settle')   AUC={auc(rows[:,1]):.3f}")
print(f"   contains divine name (ءله/ربب)   AUC={auc(rows[:,3]):.3f}")
print(f"   divine-ATTRIBUTE count (غفور رحيم…) AUC={auc(rows[:,4]):.3f}")
# fused logistic
X=rows[:,[1,3,4]]; Xm=X.mean(0);Xs=X.std(0)+1e-9; Xn=(X-Xm)/Xs; Xa=np.c_[np.ones(len(Xn)),Xn]; w=np.zeros(4)
for _ in range(500):
    p=1/(1+np.exp(-Xa@w)); w-=0.3*Xa.T@(p-y)/len(y)
print(f"   FUSED (commonness+divine+attribute) AUC={auc(Xa@w):.3f}")
# fraction of suras ending in a divine-attribute formula
endform=np.mean([ (sum(1 for r in roots.get(ks[-1],[]) if r in ATTR)>=1) for s,ks in bys.items()])
print(f"   {endform:.0%} of suras' LAST verse carries a divine-attribute root (closing-formula cadence)")
