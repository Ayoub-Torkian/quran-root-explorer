#!/usr/bin/env python3
"""Route-B pilot: mapping-free structural comparison across modalities.

Does NOT invent any letter->codon cipher. Compares dimensionless structural
signatures of language vs real CDS vs shuffled CDS vs random, and asks the
ONE decisive question: does language resemble the REAL genome's structure more
than a structure-matched SHUFFLED genome?  Pilot = plumbing + calibration only,
NOT a claim.

Inputs (edit paths as needed):
  - CDS FASTA file(s)            (biology modality)
  - a plain-text language sample (language modality)
Metrics (all dimensionless / label-invariant where possible):
  - unigram redundancy  1 - H1/log2(A)
  - gzip compression ratio        (lower = more structured)
  - Zipf slope of 3-grams
  - mutual information MI(d), bits, Miller-Madow bias-corrected, for several d
The decisive contrast is real-vs-shuffled within each modality, then language
vs the REAL (not shuffled) genome.
"""
import re, json, zlib, math, random, sys
from collections import Counter
import numpy as np

random.seed(7); np.random.seed(7)

def load_fasta(path):
    seq=[]
    for line in open(path,encoding='utf-8',errors='ignore'):
        if line.startswith('>'): continue
        seq.append(line.strip().upper())
    return re.sub('[^ACGT]','',''.join(seq))

def load_text_letters(path, keep=r'[^a-z]'):
    t=open(path,encoding='utf-8',errors='ignore').read().lower()
    return re.sub(keep,'',t)

def codes(s):
    alpha=sorted(set(s)); idx={c:i for i,c in enumerate(alpha)}
    return np.array([idx[c] for c in s],dtype=np.int32), len(alpha)

def h1_redundancy(s,A):
    c=Counter(s); n=len(s)
    H=-sum((v/n)*math.log2(v/n) for v in c.values())
    return 1-H/math.log2(A), H

def gzip_ratio(s):
    b=s.encode('utf-8'); return len(zlib.compress(b,9))/len(b)

def zipf_slope(s,k=3):
    grams=Counter(s[i:i+k] for i in range(len(s)-k+1))
    freqs=sorted(grams.values(),reverse=True)
    if len(freqs)<10: return float('nan')
    r=np.log10(np.arange(1,len(freqs)+1)); f=np.log10(np.array(freqs))
    lo=int(0.02*len(freqs)); hi=int(0.6*len(freqs))
    return float(np.polyfit(r[lo:hi],f[lo:hi],1)[0])

def mutual_information(cd,A,d):
    x=cd[:-d]; y=cd[d:]; n=len(x)
    joint=np.zeros((A,A)); np.add.at(joint,(x,y),1.0); joint/=n
    px=joint.sum(1); py=joint.sum(0); nz=joint>0
    mi=float(np.sum(joint[nz]*np.log2(joint[nz]/np.outer(px,py)[nz])))
    bias=((np.sum(px>0)-1)*(np.sum(py>0)-1))/(2*n*math.log(2))  # Miller-Madow
    return mi-bias

def signature(name,s):
    cd,A=codes(s); red,_=h1_redundancy(s,A)
    sig={'name':name,'N':len(s),'alphabet':A,
         'redundancy_unigram':round(red,4),
         'gzip_ratio':round(gzip_ratio(s),4),
         'zipf_slope_3gram':round(zipf_slope(s),3)}
    for d in [1,2,5,10,20,50]:
        sig[f'MI_d{d}']=round(mutual_information(cd,A,d),5)
    return sig

def shuffled(s):
    l=list(s); random.shuffle(l); return ''.join(l)

def iid_match(s):
    c=Counter(s); a=list(c); p=np.array([c[x] for x in a],float); p/=p.sum()
    return ''.join(np.random.choice(a,size=len(s),p=p))

if __name__=='__main__':
    CDS = sys.argv[1] if len(sys.argv)>1 else 'data/examples/human_cds_set.fasta'
    TXT = sys.argv[2] if len(sys.argv)>2 else 'english_raw.txt'
    cds=load_fasta(CDS); txt=load_text_letters(TXT)
    seqs=[('CDS_real',cds),('CDS_shuffled',shuffled(cds)),('CDS_random_iid',iid_match(cds)),
          ('Lang_full',txt),('Lang_shuffled',shuffled(txt)),('Lang_CDSlen',txt[:len(cds)])]
    results=[signature(n,s) for n,s in seqs]
    cols=['name','N','alphabet','redundancy_unigram','gzip_ratio','zipf_slope_3gram',
          'MI_d1','MI_d5','MI_d20','MI_d50']; w=[16,8,5,11,10,9,9,9,9,9]
    print(''.join(str(c)[:w[i]].ljust(w[i]+1) for i,c in enumerate(cols)))
    for r in results:
        print(''.join(str(r.get(c,'')).ljust(w[i]+1) for i,c in enumerate(cols)))
    json.dump({'note':'Route-B pilot, plumbing/calibration only, not a claim',
               'seed':7,'sequences':results}, open('results.json','w'), indent=2)
