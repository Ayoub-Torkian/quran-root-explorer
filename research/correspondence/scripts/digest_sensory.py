#!/usr/bin/env python3
import unicodedata, collections, math
import numpy as np
rng=np.random.default_rng(1)
def norm(s):
    s=''.join(c for c in unicodedata.normalize('NFD',s) if not(0x64B<=ord(c)<=0x65F) and ord(c)!=0x670)
    return s.replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا').replace('ئ','ي').replace('ؤ','و')
TX="research/two_books_genome/data/quran/quran_arabic_verses.tsv"; RBA="research/two_books_genome/roots_by_ayah.tsv"
V=[]
for ln in open(TX,encoding='utf-8'):
    if '\t' in ln:
        sa,tx=ln.rstrip('\n').split('\t',1); s=int(sa.split(':')[0]); V.append((s,[norm(w) for w in tx.split()]))
N=len(V)
# DIGESTIVE: intake(ingest external speech) -> output(process/respond 'say')
intake=np.array([1 if any(t in('قالوا','قالو','يقولون') or 'سلونك' in t or 'سالونك' in t for t in toks) else 0 for _,toks in V])
output=np.array([1 if any(t=='قل' for t in toks) else 0 for _,toks in V])
co=np.mean([1 if output[i:i+3].any() else 0 for i in np.where(intake==1)[0]])
nul=[np.mean([1 if output[i:i+3].any() else 0 for i in rng.integers(0,N-3,int(intake.sum()))]) for _ in range(1000)]
z=(co-np.mean(nul))/np.std(nul)
print(f"DIGESTIVE (refined): intake {int(intake.sum())} verses; intake→'say' within 0-2 verses = {co:.0%} vs random {np.mean(nul):.0%} (z={z:+.1f}) -> {'✅ ingest→process→output' if z>3 else 'weak'}")

# SENSORY ORGANS: which suras are the EYE vs EAR systems?
sur=collections.defaultdict(collections.Counter)
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:
        k,r=ln.rstrip('\n').split('\t',1); s=int(k.split(':')[0])
        if 1<=s<=114:
            for x in r.split():
                if x and x!='NA': sur[s][x]+=1
suras=sorted(sur); df=collections.Counter()
for s in suras:
    for r in sur[s]: df[r]+=1
tot=sum(sum(sur[s].values()) for s in suras)
EYE={'بصر','رءی','نظر','عین','رای'}; EAR={'سمع','ءذن','صمم','نصت','وعی'}
def keyness(members):
    out={}
    for s in suras:
        n=sum(sur[s].values()); 
        got=sum(sur[s][r] for r in members); exp=n*sum(df[r] for r in members)/tot
        out[s]=(got-exp)/math.sqrt(exp+1) if exp>0 else 0
    return out
NAME={36:"YaSin",50:"Qaf",2:"Baqara",6:"An'am",7:"A'raf",10:"Yunus",16:"Nahl",17:"Isra",41:"Fussilat",46:"Ahqaf",67:"Mulk",23:"Mu'minun"}
ke=keyness(EYE); ka=keyness(EAR)
top=lambda d:[ (s,NAME.get(s,'')) for s,_ in sorted(d.items(),key=lambda x:-x[1])[:5]]
print("EYE system (vision roots بصر/رأى/نظر/عين) top suras:", top(ke))
print("EAR system (hearing roots سمع/أذن)        top suras:", top(ka))
