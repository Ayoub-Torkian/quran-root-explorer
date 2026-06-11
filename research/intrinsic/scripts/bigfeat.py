import unicodedata, numpy as np, csv
from collections import Counter, defaultdict
def skel(t):
    t=unicodedata.normalize('NFD',t); t=''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
suras=defaultdict(list)
for ln in open('/sessions/gifted-tender-cori/mnt/Quran_Root_Explorer_Web_v1.2/research/two_books_genome/data/quran/quran_arabic_verses.tsv',encoding='utf-8'):
    if '\t' not in ln: continue
    sa,tx=ln.split('\t',1); s=int(sa.split(':')[0]); suras[s].append(skel(tx))
ALL=[w for v in suras.values() for vv in v for w in vv]
alpha=sorted(set(c for w in ALL for c in w))
stop=set(w for w,_ in Counter(ALL).most_common(40))
def mom(a):
    a=np.array(a,float)
    if len(a)<2 or a.std()==0: return a.mean() if len(a) else 0,0.0,0.0,0.0
    m,s=a.mean(),a.std(); sk=((a-m)**3).mean()/s**3; ku=((a-m)**4).mean()/s**4-3
    return m,s,sk,ku
def H(c):
    v=np.array([x for x in c if x>0],float); p=v/v.sum(); return float(-(p*np.log2(p)).sum())
def ac(x,lag):
    x=np.array(x,float)
    if len(x)<=lag+2 or x.std()==0: return 0.0
    return float(np.corrcoef(x[:-lag],x[lag:])[0,1])
rows=[]
for s in sorted(suras):
    verses=suras[s]; toks=[w for v in verses for w in v]; letters=[c for w in toks for c in w]
    vl=[len(v) for v in verses]; wl=[len(w) for w in toks]
    finals=[v[-1][-1] if v and v[-1] else '' for v in verses]
    content=[w for w in toks if w not in stop]
    f={'sura':s}
    # A size/shape
    f['n_verses']=len(verses); f['n_tokens']=len(toks); f['n_letters']=len(letters)
    m,sd,sk,ku=mom(vl); f['vl_mean'],f['vl_sd'],f['vl_skew'],f['vl_kurt']=m,sd,sk,ku
    f['vl_med']=np.median(vl); f['vl_min']=min(vl); f['vl_max']=max(vl); f['vl_cv']=sd/max(m,1e-9)
    f['vl_ac1']=ac(vl,1); f['vl_ac2']=ac(vl,2); f['vl_ac3']=ac(vl,3)
    m,sd,sk,ku=mom(wl); f['wl_mean'],f['wl_sd'],f['wl_skew'],f['wl_kurt']=m,sd,sk,ku
    for k in (1,2,3,4,5): f[f'wl_frac{k}']=np.mean([1 if x==k else 0 for x in wl]) if k<5 else np.mean([1 if x>=5 else 0 for x in wl])
    # B letter unigram freq
    lc=Counter(letters); tot=max(len(letters),1)
    for L in alpha: f[f'let_{L}']=lc.get(L,0)/tot
    f['letter_entropy']=H(lc.values())
    # C rhyme / final-letter
    fc=Counter(finals); nv=max(len(finals),1)
    for L in alpha: f[f'fin_{L}']=fc.get(L,0)/nv
    f['dom_final_frac']=fc.most_common(1)[0][1]/nv if fc else 0
    f['final_entropy']=H(fc.values())
    fin2=Counter([v[-1][-2:] if v and len(v[-1])>=2 else '' for v in verses])
    f['dom_final2_frac']=(fin2.most_common(1)[0][1]/nv) if fin2 else 0
    run=best=1; chg=0
    for i in range(1,len(finals)):
        if finals[i]==finals[i-1]: run+=1; best=max(best,run)
        else: run=1; chg+=1
    f['longest_rhyme_run']=best if len(finals)>1 else len(finals); f['rhyme_change_rate']=chg/max(len(finals)-1,1)
    # D lexical/content
    f['vocab']=len(set(toks)); f['ttr']=len(set(toks))/max(len(toks),1)
    tc=Counter(toks); f['hapax_frac']=sum(1 for _,c in tc.items() if c==1)/max(len(set(toks)),1)
    f['lex_entropy']=H(tc.values()); f['repeat_rate']=1-len(set(toks))/max(len(toks),1)
    cc=Counter(content); cl=sorted(cc.values(),reverse=True); ct=max(sum(cl),1)
    f['top1_frac']=cl[0]/ct if cl else 0; f['top5_frac']=sum(cl[:5])/ct; f['top10_frac']=sum(cl[:10])/ct
    bg=Counter(zip(toks,toks[1:])); f['bigram_repeat']=sum(1 for _,c in bg.items() if c>1)/max(len(bg),1)
    tg=Counter(zip(toks,toks[1:],toks[2:])); f['trigram_repeat']=sum(1 for _,c in tg.items() if c>1)/max(len(tg),1)
    # burstiness of content recurrence (gaps)
    pos=defaultdict(list)
    for i,w in enumerate(content): pos[w].append(i)
    gaps=[b-a for ps in pos.values() if len(ps)>1 for a,b in zip(ps,ps[1:])]
    gm,gsd,_,_=mom(gaps) if gaps else (0,0,0,0); f['burst']=(gsd-gm)/(gsd+gm) if (gsd+gm)>0 else 0
    # E position
    f['rel_pos']=s/114
    rows.append(f)
keys=list(rows[0].keys())
with open('/sessions/gifted-tender-cori/mnt/Quran_Root_Explorer_Web_v1.2/research/intrinsic/sura_features_big.tsv','w',newline='',encoding='utf-8') as fo:
    w=csv.DictWriter(fo,fieldnames=keys,delimiter='\t'); w.writeheader()
    for r in rows: w.writerow({k:(round(v,5) if isinstance(v,float) else v) for k,v in r.items()})
print(f"{len(rows)} suras x {len(keys)-1} features")
print("alphabet size:",len(alpha))
print("families: size/shape, letter-freq(28+), rhyme-final(28+), lexical, position")
