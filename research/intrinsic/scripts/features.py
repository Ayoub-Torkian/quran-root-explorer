import unicodedata, numpy as np, csv
from collections import Counter, defaultdict
def skel(t):
    t=unicodedata.normalize('NFD',t); t=''.join(c for c in t if not unicodedata.combining(c))
    out=[]
    for tok in t.split():
        w=''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ')
        if w: out.append(w)
    return out
# load verses grouped by sura, in order
suras=defaultdict(list)
for ln in open('/sessions/gifted-tender-cori/mnt/Quran_Root_Explorer_Web_v1.2/research/two_books_genome/data/quran/quran_arabic_verses.tsv',encoding='utf-8'):
    if '\t' not in ln: continue
    sa,tx=ln.split('\t',1); s=int(sa.split(':')[0]); a=int(sa.split(':')[1].split('\t')[0]) if ':' in sa else 0
    suras[s].append(skel(tx))
# corpus stop words
alltok=[w for s in suras.values() for v in s for w in v]
stop=set(w for w,_ in Counter(alltok).most_common(40))
def H(counts):
    c=np.array([x for x in counts if x>0],float); p=c/c.sum(); return float(-(p*np.log2(p)).sum())
rng=np.random.default_rng(0)
rows=[]
for s in sorted(suras):
    verses=suras[s]
    toks=[w for v in verses for w in v]
    letters=[c for w in toks for c in w]
    vl=[len(v) for v in verses]               # verse length in words
    finals=[v[-1][-1] if v and v[-1] else '' for v in verses]
    finals2=[v[-1][-2:] if v and len(v[-1])>=2 else '' for v in verses]
    content=[w for w in toks if w not in stop]
    # form
    f={}
    f['sura']=s; f['n_verses']=len(verses); f['n_tokens']=len(toks); f['n_letters']=len(letters)
    f['mean_vlen']=np.mean(vl); f['sd_vlen']=np.std(vl); f['cv_vlen']=np.std(vl)/max(np.mean(vl),1e-9)
    f['mean_wordlen']=np.mean([len(w) for w in toks]) if toks else 0
    f['vlen_ac1']=float(np.corrcoef(vl[:-1],vl[1:])[0,1]) if len(vl)>3 and np.std(vl)>0 else 0.0
    fc=Counter(finals); f['dom_final_frac']=fc.most_common(1)[0][1]/len(finals) if finals else 0
    f['final_entropy']=H(fc.values())
    f2c=Counter([x for x in finals2 if x]); f['dom_final2_frac']=(f2c.most_common(1)[0][1]/len(finals)) if f2c else 0
    # longest rhyme run + change rate
    run=best=1; chg=0
    for i in range(1,len(finals)):
        if finals[i]==finals[i-1]: run+=1; best=max(best,run)
        else: run=1; chg+=1
    f['longest_rhyme_run']=best if len(finals)>1 else len(finals)
    f['rhyme_change_rate']=chg/max(len(finals)-1,1)
    f['letter_entropy']=H(Counter(letters).values())
    # content
    f['vocab']=len(set(toks)); f['ttr']=len(set(toks))/max(len(toks),1)
    f['hapax_frac']=sum(1 for _,c in Counter(toks).items() if c==1)/max(len(set(toks)),1)
    cc=Counter(content)
    f['top1_content_frac']=cc.most_common(1)[0][1]/max(len(content),1) if content else 0
    f['repeat_rate']=1-len(set(toks))/max(len(toks),1)
    f['lex_entropy']=H(Counter(toks).values())
    bg=Counter(zip(toks,toks[1:])); f['bigram_repeat']=sum(1 for _,c in bg.items() if c>1)/max(len(bg),1)
    rows.append(f)
keys=list(rows[0].keys())
with open('/sessions/gifted-tender-cori/mnt/Quran_Root_Explorer_Web_v1.2/research/intrinsic/sura_features.tsv','w',newline='',encoding='utf-8') as fo:
    w=csv.DictWriter(fo,fieldnames=keys,delimiter='\t'); w.writeheader()
    for r in rows: w.writerow({k:(round(v,4) if isinstance(v,float) else v) for k,v in r.items()})
print(f"{len(rows)} suras x {len(keys)-1} features -> research/intrinsic/sura_features.tsv")
print("features:", ", ".join(k for k in keys if k!='sura'))
