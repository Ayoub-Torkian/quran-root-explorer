#!/usr/bin/env python3
# Real content visuals -> append to viz_data.json: twin pair (Arabic), rhyme strip (Arabic
# final letters), fāṣila endings (Arabic), Zipf curve + top words, recurrence decay, L13 matrix.
import glob,unicodedata,json,numpy as np
from collections import Counter,defaultdict
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
def skel(t):
    t=unicodedata.normalize('NFD',t);t=''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln: k,r=ln.rstrip('\n').split('\t',1); roots[k]=set(x for x in r.split() if x and x!='NA')
ref=[];raw=[];sk=[];su=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1); ref.append(sa.strip()); raw.append(tx.strip()); sk.append(skel(tx)); su.append(int(sa.split(':')[0]))
N=len(ref)
# ---- L21 twin pair (cross-sūra, distinct, high Jaccard, substantial) ----
inv=defaultdict(list)
for i in range(N):
    for r in roots.get(ref[i],set()): inv[r].append(i)
best=None
for i in range(N):
    ri=roots.get(ref[i],set())
    if len(ri)<5: continue
    cand=set()
    for r in ri:
        if len(inv[r])<200: cand.update(inv[r])
    for j in cand:
        if j<=i or su[i]==su[j] or sk[i]==sk[j]: continue
        rj=roots.get(ref[j],set()); u=len(ri|rj)
        if not u: continue
        jac=len(ri&rj)/u
        if jac>=0.6 and 6<=len(sk[i])<=14 and abs(len(sk[i])-len(sk[j]))<=2:
            sc=jac*len(ri&rj)
            if not best or sc>best[0]: best=(sc,i,j,sorted(ri&rj))
_,ai,bj,shared=best
twin_pair={'a':{'ref':ref[ai],'text':raw[ai]},'b':{'ref':ref[bj],'text':raw[bj]},'shared_roots':shared}
# ---- L06 rhyme strip: final letters of a passage (Sūra 19, first 30) ----
strip=[(ref[i], sk[i][-1][-1] if sk[i] and sk[i][-1] else '') for i in range(N) if su[i]==19][:30]
rhyme_strip=[[r,c] for r,c in strip]
# ---- L17 fāṣila endings: last 2 letters of final word WITH diacritics ----
def fasila(tx):
    toks=tx.split();
    if not toks: return ''
    w=unicodedata.normalize('NFC',toks[-1]); return w[-3:]
fas=Counter(fasila(t) for t in raw).most_common(14)
# ---- L01 Zipf: word rank-freq + top words ----
allw=[w for s in sk for w in s]; wc=Counter(allw); freqs=sorted(wc.values(),reverse=True)
zipf=[[round(float(np.log10(rk+1)),3),round(float(np.log10(f)),3)] for rk,f in enumerate(freqs) if rk<3000 and (rk<50 or rk%3==0)]
top_words=[[w,c] for w,c in wc.most_common(14)]
# ---- L08 recurrence decay: P(same token at distance d) vs shuffle baseline ----
ids=np.array([hash(w)%100000 for w in allw]); M=len(ids)
dec=[]
for d in [1,2,4,8,16,32,64,128,256,512]:
    same=np.mean(ids[:-d]==ids[d:]); dec.append([d,round(float(same),5)])
base=round(float(np.mean(ids[:5000]==ids[np.random.permutation(5000)])),5)
# ---- L13 perturbation matrix (from the battery) ----
pert={'invariants':['Hurst','1/f','rhyme','network'],
      'rows':[['intact',0.95,0.76,0.72,1.0],['MOVE',0.51,0.00,0.30,0.2],['REPLACE',0.93,0.74,0.51,0.4],['ADD',0.80,0.55,0.62,0.7]]}
P=R+'/research/intrinsic/viz_data.json'; v=json.load(open(P,encoding='utf-8'))
v.update({'twin_pair':twin_pair,'rhyme_strip':rhyme_strip,'fasila':[[w,c] for w,c in fas],
          'zipf':zipf,'zipf_top':top_words,'recurrence':dec,'recurrence_base':base,'perturb':pert})
json.dump(v,open(P,'w',encoding='utf-8'),ensure_ascii=False)
print('twin pair:',twin_pair['a']['ref'],'<->',twin_pair['b']['ref'],'shared',shared)
print('rhyme strip n=',len(rhyme_strip),'| fasila top:',[w for w,_ in fas][:6])
print('zipf pts',len(zipf),'| recurrence d1=',dec[0],'base',base)
