#!/usr/bin/env python3
# ANISOTROPY of the field F[verse][pos]. Horizontal corr ρx(k)=corr(F[v][i],F[v][i+k]) (within verse);
# Vertical corr ρy(k)=corr(F[v][i],F[v+k][i]) (across verses, same position). Anisotropy = ρx != ρy.
# Root level: F = token root-surprisal. Char level: F = long-vowel indicator.
import glob,unicodedata,collections,math,numpy as np
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
AR=set(chr(c) for c in range(0x621,0x64B)); skel=lambda s:''.join(c for c in unicodedata.normalize('NFD',s) if c in AR)
def corr(a,b):
    a=np.array(a);b=np.array(b)
    if len(a)<10 or a.std()==0 or b.std()==0:return float('nan')
    return np.corrcoef(a,b)[0,1]
def aniso(verses,name,K=4):
    print(name)
    for k in range(1,K+1):
        ax,bx=[],[]
        for v in verses:
            for i in range(len(v)-k): ax.append(v[i]);bx.append(v[i+k])
        ay,by=[],[]
        for vi in range(len(verses)-k):
            v,w=verses[vi],verses[vi+k];m=min(len(v),len(w))
            for i in range(m): ay.append(v[i]);by.append(w[i])
        print("  lag %d : ρx(within-verse)=%+.3f   ρy(across-verse)=%+.3f   anisotropy Δ=%+.3f"%(k,corr(ax,bx),corr(ay,by),corr(ax,bx)-corr(ay,by)))
# root surprisal field
ordroots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:k,r=ln.rstrip('\n').split('\t',1);ordroots[k]=[x for x in r.split() if x and x!='NA']
freq=collections.Counter(x for v in ordroots.values() for x in v);tot=sum(freq.values())
sur=lambda r:-math.log2(freq[r]/tot)
vR=[[sur(x) for x in v] for v in ordroots.values() if len(v)>=3]
aniso(vR,"ROOT level (token surprisal field):")
# char long-vowel field
vC=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' in ln:
        sk=skel(ln.split('\t',1)[1].strip())
        if len(sk)>=4: vC.append([1.0 if c in('ا','و','ي') else 0.0 for c in sk])
aniso(vC,"CHAR level (long-vowel field):")
