#!/usr/bin/env python3
import unicodedata, collections, math
import numpy as np
rng=np.random.default_rng(1)
def norm(s):
    s=''.join(c for c in unicodedata.normalize('NFD',s) if not(0x64B<=ord(c)<=0x65F) and ord(c)!=0x670)
    return s.replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا').replace('ئ','ي').replace('ؤ','و')
AR=set(chr(c) for c in range(0x621,0x64B))
def rasm(s): return ''.join(c for c in unicodedata.normalize('NFD',s) if c in AR)
TX="research/two_books_genome/data/quran/quran_arabic_verses.tsv"; RBA="research/two_books_genome/roots_by_ayah.tsv"
roots={};
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln: k,r=ln.rstrip('\n').split('\t',1); roots[k]=[x for x in r.split() if x and x!='NA']
text={}; order=[]
for ln in open(TX,encoding='utf-8'):
    if '\t' in ln:
        sa,tx=ln.rstrip('\n').split('\t',1); text[sa]=[norm(w) for w in tx.split()]; order.append(sa)
bys=collections.defaultdict(list)
for sa in order:
    s=int(sa.split(':')[0])
    if 1<=s<=114: bys[s].append(sa)
suras=sorted(bys)

# C1 NECESSITY (functional) — is each sura irreplaceable in a FUNCTION space (incl register)? does it catch Fatiha?
SUPP={'نعبد','نستعين','اهدنا','اياك','ربنا','سبحانك','اغفر','اهدنا'}
def feats(s):
    ks=bys[s]; n=len(ks)
    L=np.mean([len([w for w in text[k] if w]) for k in ks])
    addr=np.mean([1 if any(t=='يا' or 'ايها' in t or t.endswith('كم') for t in text[k]) else 0 for k in ks])
    qul=np.mean([1 if any(t=='قل' for t in text[k]) else 0 for k in ks])
    supp=np.mean([1 if any(t in SUPP for t in text[k]) else 0 for k in ks])
    fin=[ (rasm(' '.join(text[k]))[-1] if rasm(' '.join(text[k])) else '') for k in ks]
    rh=collections.Counter(fin).most_common(1)[0][1]/n
    return [math.log(L+1),addr,qul,supp,rh]
F=np.array([feats(s) for s in suras]); F=(F-F.mean(0))/(F.std(0)+1e-9)
D=np.linalg.norm(F[:,None,:]-F[None,:,:],axis=2); np.fill_diagonal(D,np.inf)
nn=D.min(1)
fi=suras.index(1)
print(f"C1 NECESSITY (functional space): median nearest-neighbour dist {np.median(nn):.2f}; FĀTIḤA(1) dist {nn[fi]:.2f} (rank {1+sum(nn>nn[fi])}/{len(suras)} most-isolated)")
print(f"   -> {'✅ Fatiha now seen as irreplaceable (functional outlier)' if nn[fi]>np.percentile(nn,80) else 'still not captured'}")

# C2 DIGESTIVE — intake = root س ء ل (ask) ; output = قل nearby
ASK='سءل'
intake=[k for k in order if ASK in roots.get(k,[])]
def has_qul(k):
    return any(t=='قل' for t in text.get(k,[]))
keyidx={k:i for i,k in enumerate(order)}
hit=0
for k in intake:
    i=keyidx[k]; win=order[i:i+3]; hit+= 1 if any(has_qul(w) for w in win) else 0
base=np.mean([1 if has_qul(k) else 0 for k in order])
print(f"\nC2 DIGESTIVE (root 'ask'→'say'): {len(intake)} 'ask' verses; {hit/max(len(intake),1):.0%} followed by 'qul' within 0-2 vs base {base:.0%} -> {'✅ ingest→process→output' if hit/max(len(intake),1)>3*base else '◑'}")

# C4 INTEGRATION — WEIGHTED small-world
sur=collections.defaultdict(collections.Counter)
for k,rs in roots.items():
    s=int(k.split(':')[0])
    if 1<=s<=114:
        for r in rs: sur[s][r]+=1
S=len(suras); idx={s:i for i,s in enumerate(suras)}; df=collections.Counter()
for s in suras:
    for r in sur[s]: df[r]+=1
rare=[r for r in df if 2<=df[r]<=60]; M=np.zeros((S,S))
for r in rare:
    h=[idx[s] for s in suras if r in sur[s]]
    for a in range(len(h)):
        for b in range(a+1,len(h)): M[h[a],h[b]]+=1; M[h[b],h[a]]+=1
dg=M.sum(1)+1e-9; A=M/np.sqrt(np.outer(dg,dg)); np.fill_diagonal(A,0)
def wclust(W):
    s=W.sum(1); c=0
    for i in range(len(W)):
        nb=np.where(W[i]>0)[0]
        if len(nb)<2: continue
        tri=sum(W[i,j]*W[i,k]*W[j,k] for a,j in enumerate(nb) for k in nb[a+1:])
        c+= tri/(s[i]*(len(nb)-1)+1e-9)
    return c/len(W)
wc=wclust(A)
nul=[]
for _ in range(20):
    p=A[np.triu_indices(S,1)].copy(); rng.shuffle(p); R=np.zeros((S,S)); R[np.triu_indices(S,1)]=p; R=R+R.T
    nul.append(wclust(R))
z=(wc-np.mean(nul))/np.std(nul)
print(f"\nC4 INTEGRATION (WEIGHTED clustering vs weight-shuffle): {wc:.3f} vs {np.mean(nul):.3f} z={z:+.1f} -> {'✅ weighted small-world (real integration)' if z>3 else 'not beyond random weights'}")
