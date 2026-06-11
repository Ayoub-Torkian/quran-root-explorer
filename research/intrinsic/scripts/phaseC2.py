#!/usr/bin/env python3
# Phase C2 — vowel-aware fāṣila āyah detector. The consonantal skeleton strips the
# rhyme vowels (L17 recall 5%). Here the terminal model keys on the DIACRITIZED
# rhyme: last 2 consonants + final harakat (captures -ūn/-īn fatha, tanwīn, etc.).
# Cross-validated by sūra parity (internal split). Compare to skeleton + shuffle.
import glob,unicodedata,numpy as np
from collections import Counter
DATA=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2/research/two_books_genome/data/quran/quran_arabic_verses.tsv')[0]
def base_letters(w):
    return ''.join(c for c in unicodedata.normalize('NFC',w) if 'ء'<=c<='ي' and c!='ـ')
def rhyme_key(w):
    w=unicodedata.normalize('NFC',w); b=base_letters(w)
    if not b: return 'NA'
    sk=b[-2:]
    marks=[c for c in w if unicodedata.combining(c)]
    fm=unicodedata.name(marks[-1],'X') if marks else 'SUKUN'
    fm=fm.replace('ARABIC ','')
    return sk+'|'+fm
def skel_key(w):
    b=base_letters(w); return b[-1] if b else 'NA'
# build word stream
W=[];end=[];su=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    s,tx=ln.split('\t',1); s=int(s.split(':')[0]); toks=tx.split()
    for k,t in enumerate(toks):
        W.append(t); end.append(k==len(toks)-1); su.append(s)
M=len(W); end=np.array(end); su=np.array(su)
def make_ids(keyfn,V):
    keys=[keyfn(w) for w in W]
    top=[k for k,_ in Counter(keys).most_common(V)]; d={k:i for i,k in enumerate(top)}
    return np.array([d.get(k,V) for k in keys]),V+1
def detect(ids,A,wl,train,test):
    pt=np.bincount(ids[train&end],minlength=A)+0.5; pt/=pt.sum()
    pa=np.bincount(ids[train],minlength=A)+0.5; pa/=pa.sum()
    bonus_tab=np.log(pt)-np.log(pa)
    mean_len=train.sum()/max(1,(train&end).sum()); g=1.0/mean_len; logg=np.log(g); log1g=np.log(1-g)
    idx=np.where(test)[0]; fl=ids[idx]; te=end[idx]; n=len(idx); bonus=bonus_tab[fl]
    MAXSEG=60; NEG=-1e18; best=np.full(n+1,NEG); best[0]=0.0; back=np.full(n+1,-1,np.int64)
    for j in range(1,n+1):
        lo=max(0,j-MAXSEG); starts=np.arange(lo,j); Ln=j-starts
        seglp=bonus[j-1]+(Ln-1)*log1g+logg
        cand=best[lo:j]+seglp; k=np.argmax(cand)
        if cand[k]>best[j]: best[j]=cand[k]; back[j]=lo+k
    b=[]; j=n
    while j>0:
        i=back[j]
        if i>0: b.append(i-1)
        j=i
    pred=set(b); true=set(np.where(te[:-1])[0])
    tp=len(pred&true); P=tp/len(pred) if pred else 0; R=tp/len(true) if true else 0
    return P,R,(2*P*R/(P+R) if P+R else 0)
wl=np.array([len(base_letters(w)) for w in W])
odd=(su%2==1); even=(su%2==0)
def twofold(ids,A,label):
    r1=detect(ids,A,wl,even,odd); r2=detect(ids,A,wl,odd,even)
    P=(r1[0]+r2[0])/2;R=(r1[1]+r2[1])/2;F=(r1[2]+r2[2])/2
    print(f"{label:28s} P={P:.3f} R={R:.3f} F={F:.3f}")
    return P,R,F
print(f"words={M}  āyāt={end.sum()}")
ids_v,Av=make_ids(rhyme_key,400)
ids_s,As=make_ids(skel_key,40)
twofold(ids_s,As,"skeleton (last consonant)")
res=twofold(ids_v,Av,"VOWEL-AWARE fāṣila key")
# shuffle floor on vowel-aware key
rng=np.random.default_rng(0); ids_sh=ids_v[rng.permutation(M)]
twofold(ids_sh,Av,"  shuffle floor (vowel-aware)")
