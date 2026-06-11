#!/usr/bin/env python3
# C12 control: do LONG-RANGE fixed offsets (modal gap >=3) survive — beyond local Arabic
# phrase grammar (which only fixes adjacent gap=1/2)? Test concentration vs within-verse shuffle
# restricted to long-range pairs. Also report tightest long-range templates.
import glob,numpy as np,collections
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
verses=[]
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:
        _,r=ln.split('\t',1);v=[x for x in r.split() if x and x!='NA']
        if 5<=len(v)<=40:verses.append(v)
def gaps(vs):
    g=collections.defaultdict(list)
    for v in vs:
        for i in range(len(v)):
            for j in range(i+1,len(v)):
                if v[i]!=v[j]:g[(v[i],v[j])].append(j-i)
    return g
G=gaps(verses)
def modal(gl):
    c=collections.Counter(gl);mg,mc=c.most_common(1)[0];return mg,mc/len(gl)
pairs=[(k,v) for k,v in G.items() if len(v)>=25]
# split by modal gap
longp=[(k,v) for k,v in pairs if modal(v)[0]>=3]
adjp =[(k,v) for k,v in pairs if modal(v)[0]<=2]
print('pairs >=25: %d  | adjacent-modal(<=2): %d  | LONG-RANGE-modal(>=3): %d'%(len(pairs),len(adjp),len(longp)))
rng=np.random.default_rng(1)
def conc(plist,vs):
    Gs=gaps(vs);out=[]
    for k,v in plist:
        if k in Gs and len(Gs[k])>=25:out.append(modal(Gs[k])[1])
    return np.mean(out) if out else np.nan
realL=np.mean([modal(v)[1] for k,v in longp])
fl=[conc(longp,[list(rng.permutation(v)) for v in verses]) for _ in range(40)]
fl=np.array(fl);print('LONG-RANGE modal-fraction: real %.3f vs within-verse shuffle %.3f±%.3f  z=%+.1f'%(realL,fl.mean(),fl.std(),(realL-fl.mean())/fl.std()))
tight=sorted(longp,key=lambda kv:-modal(kv[1])[1])[:8]
print('tightest LONG-RANGE fixed-offset templates:')
for (a,b),gl in tight:
    mg,mf=modal(gl);print('   %s ... %s  gap=%d  %.0f%%  (n=%d)'%(a,b,mg,100*mf,len(gl)))
