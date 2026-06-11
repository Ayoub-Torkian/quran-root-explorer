#!/usr/bin/env python3
# HARDEST TEST — split-half (odd vs even suras) replication of the 8 A-core attributes.
import unicodedata, collections, math
import numpy as np
rng=np.random.default_rng(1)
AR=set(chr(c) for c in range(0x621,0x64B))
def rasm(s): return ''.join(c for c in unicodedata.normalize('NFD',s) if c in AR)
def norm(s):
    s=''.join(c for c in unicodedata.normalize('NFD',s) if not(0x64B<=ord(c)<=0x65F) and ord(c)!=0x670)
    return s.replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا')
TX="research/two_books_genome/data/quran/quran_arabic_verses.tsv"; RBA="research/two_books_genome/roots_by_ayah.tsv"
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln: k,r=ln.rstrip('\n').split('\t',1); roots[k]=set(x for x in r.split() if x and x!='NA')
V=[]
for ln in open(TX,encoding='utf-8'):
    if '\t' in ln:
        sa,tx=ln.rstrip('\n').split('\t',1); s=int(sa.split(':')[0]); T=[norm(w) for w in tx.split()]
        wl=len([w for w in (rasm(x) for x in tx.split()) if w]); fin=rasm(' '.join(tx.split()))
        V.append((s,sa,roots.get(sa,set()),wl,T,fin[-1] if fin else ''))
MUQ={2,3,7,10,11,12,13,14,15,19,20,26,27,28,29,30,31,32,36,38,40,41,42,43,44,45,46,50,68}
def outward(T): return 1 if any(t=='يا' or 'ايها' in t or t.endswith('كم') for t in T) else 0

def run(half, lab):
    Vh=[v for v in V if (v[0]%2==1)==half]
    # A1 membrane: within-sura vs across-boundary adjacent overlap
    w=[];a=[]
    for i in range(len(Vh)-1):
        ov=len(Vh[i][2]&Vh[i+1][2]); (w if Vh[i][0]==Vh[i+1][0] else a).append(ov)
    # A2 weave: per-sura real vs own-shuffle
    bys=collections.defaultdict(list)
    for v in Vh: bys[v[0]].append(v[2])
    d=[]
    for s,L in bys.items():
        if len(L)<3: continue
        real=np.mean([len(L[i]&L[i+1]) for i in range(len(L)-1)])
        nul=np.mean([ (lambda P:np.mean([len(P[i]&P[i+1]) for i in range(len(P)-1)]))([L[k] for k in rng.permutation(len(L))]) for _ in range(30)])
        d.append(real-nul)
    # A3 propagation: bigram repeat-mass vs shuffle
    stream=[r for v in Vh for r in v[2]]
    def rm(seq): c=collections.Counter(zip(seq,seq[1:])); t=sum(c.values()); return sum(x for x in c.values() if x>=2)/t
    nul=[rm(list(rng.permutation(stream))) for _ in range(15)]; z3=(rm(stream)-np.mean(nul))/np.std(nul)
    # A4 interface: outward clustering autocorr
    o=np.array([outward(v[4]) for v in Vh]); ac4=np.corrcoef(o[:-1],o[1:])[0,1]
    nul=[ (lambda p:np.corrcoef(p[:-1],p[1:])[0,1])(rng.permutation(o)) for _ in range(300)]; z4=(ac4-np.mean(nul))/np.std(nul)
    # A5 rhythm: verse-length autocorr lag10
    vl=np.array([v[3] for v in Vh],float); ac5=np.corrcoef(vl[:-10],vl[10:])[0,1]
    # A8 skeleton: muqattaat verse-length t
    ml=[v[3] for v in Vh if v[0] in MUQ]; ol=[v[3] for v in Vh if v[0] not in MUQ]
    t8=(np.mean(ml)-np.mean(ol))/math.sqrt(np.var(ml)/len(ml)+np.var(ol)/len(ol))
    print(f"[{lab}] A1 within {np.mean(w):.2f}/across {np.mean(a):.2f} | A2 weave Δ={np.mean(d):+.3f} ({(np.array(d)>0).mean():.0%}+) | A3 z={z3:+.0f} | A4 z={z4:+.1f} | A5 ac10={ac5:+.2f} | A8 t={t8:+.1f}")

run(True,"ODD ")
run(False,"EVEN")
print("Bedrock = same sign + significant in BOTH halves.")
