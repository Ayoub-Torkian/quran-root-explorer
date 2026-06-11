import re, sys, time
import numpy as np
from collections import Counter
sys.path.insert(0,"/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2")
import analysis as A
from analysis import normalize_letters
t0=time.time(); WL=re.compile(r"[a-zA-Z]+"); WA=re.compile(r"[^\W\d_]+",re.UNICODE)
def yuleK(words):
    c=Counter(words); N=len(words); vi=Counter(c.values())
    return 1e4*(sum(v*(i*i) for i,v in vi.items())-N)/(N*N+1e-9)
def measures(win_words, sent_lens):
    types=set(win_words); N=len(win_words); wl=np.array([len(w) for w in win_words])
    fc=Counter(win_words); wp=np.array(list(fc.values()),float)/N; went=-np.sum(wp*np.log2(wp))
    sl=np.array(sent_lens) if len(sent_lens)>=3 else np.array([1,1,1])
    return dict(yuleK=yuleK(win_words), word_ent=went, std_wl=wl.std(),
                frac_long=np.mean(wl>=8 if win_words and len(win_words[0])>0 else [0]),
                unit_cv=sl.std()/(sl.mean()+1e-9), ttr=len(types)/N)
def win_from_sents(sents, N=1200, step=600, maxw=60):
    flat=[(w,si) for si,s in enumerate(sents) for w in s]; rows=[]
    for c in range(0,max(1,len(flat)-N+1),step):
        seg=flat[c:c+N]
        if len(seg)<N*0.8: break
        ww=[w for w,_ in seg]; sids=sorted(set(si for _,si in seg))
        rows.append(measures(ww,[len(sents[i]) for i in sids]))
        if len(rows)>=maxw: break
    ks=rows[0].keys(); return {k:np.array([r[k] for r in rows]) for k in ks}, len(rows)
def load_ar_sents(p):
    sents=[]
    for ln in open(p,encoding="utf-8",errors="ignore"):
        s=ln.strip()
        if not s or s.startswith(("صحيح","أرض السافلين","نص إخباري")): continue
        for se in re.split(r"[.!؟]+",s):
            w=[normalize_letters(x) for x in WA.findall(se) if normalize_letters(x)]
            if len(w)>=2: sents.append(w)
    return sents
# Quran: units = ayahs (whitespace words)
corp=A.load_corpus("/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2/Book6.xlsx")
col='متن آیه با حرکت'
q_sents=[]
for i in range(len(corp.df)):
    w=[normalize_letters(x) for x in str(corp.df.iloc[i][col]).split() if normalize_letters(x)]
    if len(w)>=2: q_sents.append(w)
reg={"QURAN":q_sents,"Tabari":load_ar_sents("corpus/ar_tabari.txt"),
     "Novel":load_ar_sents("corpus/ar_novel.txt"),"News":load_ar_sents("corpus/ar_news.txt")}
D={k:win_from_sents(v)[0] for k,v in reg.items()}
ks=["unit_cv","std_wl","yuleK","word_ent","frac_long","ttr"]
print(f"[{time.time()-t0:.1f}s] MASTERY DETECTORS (validated on Shakespeare) applied to QURAN vs ordinary Arabic")
for k in reg: print(f"   {k:8s} sents={len(reg[k]):5d} windows={len(D[k]['ttr'])}")
print(f"\n  {'measure':10s}{'QURAN':>10}{'Tabari':>9}{'Novel':>9}{'News':>9}   Q vs nearest-ORD")
# direction validated on Shakespeare: unit_cv LOWER, std_wl LOWER, yuleK LOWER, word_ent HIGHER, frac_long LOWER
shdir={"unit_cv":-1,"std_wl":-1,"yuleK":-1,"word_ent":+1,"frac_long":-1,"ttr":+1}
for k in ks:
    q=D["QURAN"][k]
    ordmeans={o:D[o][k].mean() for o in ["Tabari","Novel","News"]}
    # nearest ordinary = the one closest to Quran (hardest); report gap & whether Quran is in Shakespeare-direction vs pooled
    pool=np.concatenate([D[o][k] for o in ["Tabari","Novel","News"]])
    g=(q.mean()-pool.mean())/(np.sqrt((q.var()+pool.var())/2)+1e-9)
    shakes_like = "Shakespeare-dir" if np.sign(g)==shdir[k] else "OPPOSITE"
    print(f"  {k:10s}{q.mean():10.3f}{ordmeans['Tabari']:9.3f}{ordmeans['Novel']:9.3f}{ordmeans['News']:9.3f}   {g:+.1f}sd {shakes_like}")
print(f"\n[total {time.time()-t0:.1f}s]")
