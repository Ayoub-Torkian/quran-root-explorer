import re, sys, time, gzip
import numpy as np
from collections import Counter
sys.path.insert(0,"/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2")
import analysis as A
from analysis import normalize_letters
t0=time.time(); W=re.compile(r"[^\W\d_]+",re.UNICODE)
def enc(seq,cap):
    top=[w for w,_ in Counter(seq).most_common(cap)]; vm={w:i for i,w in enumerate(top)}
    return np.array([vm.get(w,cap) for w in seq]),cap+1
def MI(a,d,K):
    if a.size<=d: return 0.0
    x=a[:-d];y=a[d:]; j=np.bincount(x*K+y,minlength=K*K).astype(float)/x.size; pj=j.reshape(K,K)
    px=pj.sum(1);py=pj.sum(0);nz=pj>0; return float(np.sum(pj[nz]*np.log2(pj[nz]/np.outer(px,py)[nz])))
def rep(a,n):
    if len(a)<=n: return 0.0
    g=Counter(tuple(a[i:i+n].tolist()) for i in range(len(a)-n)); return 1-len(g)/max(sum(g.values()),1)
def gz(a): return len(gzip.compress(a.astype(np.int16).tobytes()))/(2*max(len(a),1))
# word-stream metrics on a window of words
def word_metrics(words):
    a,K=enc(words,400)
    return dict(mi3_w=MI(a,3,K), mi5_w=MI(a,5,K), rep4_w=rep(a,4), gz_w=gz(a))
def char_metrics(s):
    al=sorted(set(s)); vm={c:i for i,c in enumerate(al)}; a=np.array([vm[c] for c in s]); K=len(al)
    return dict(mi5_c=MI(a,5,K), rep4_c=rep(a,4), gz_c=gz(a))
def win_words(words,N=1500,step=750,maxw=20):
    rows=[]
    for c in range(0,max(1,len(words)-N+1),step):
        w=words[c:c+N]
        if len(w)<N*0.6: break
        rows.append(word_metrics(w))
        if len(rows)>=maxw: break
    ks=rows[0].keys(); return {k:np.array([r[k] for r in rows]) for k in ks}
def win_chars(s,N=4000,step=2000,maxw=20):
    rows=[]
    for c in range(0,max(1,len(s)-N+1),step):
        sub=s[c:c+N]
        if len(sub)<N*0.6: break
        rows.append(char_metrics(sub))
        if len(rows)>=maxw: break
    ks=rows[0].keys(); return {k:np.array([r[k] for r in rows]) for k in ks}

corp=A.load_corpus("/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2/Book6.xlsx")
col='متن آیه با حرکت'
q_ws=[normalize_letters(w) for i in range(len(corp.df)) for w in str(corp.df.iloc[i][col]).split() if normalize_letters(w)]
q_seg=[normalize_letters(x) for i in range(len(corp.df)) for x in corp.seg_tokens[i] if normalize_letters(x)]
tab_w=[]
for ln in open("corpus/ar_tabari.txt",encoding="utf-8",errors="ignore"):
    ss=ln.strip()
    if not ss or ss.startswith("صحيح"): continue
    tab_w+=[normalize_letters(w) for w in W.findall(ss) if normalize_letters(w)]
qs_rasm=" ".join(q_ws); ts_rasm=" ".join(tab_w)

# word metrics: Quran(ws), Quran(seg), Tabari
Wq=win_words(q_ws); Wqs=win_words(q_seg); Wt=win_words(tab_w)
# char metrics: Quran rasm, Tabari rasm
Cq=win_chars(qs_rasm); Ct=win_chars(ts_rasm)

def verdict(qws_arr, qseg_arr, t_arr):
    # gap of each Quran tokenization vs Tabari, in Quran-window sd units
    def g(q): return (q.mean()-t_arr.mean())/(q.std()+1e-9)
    gws=g(qws_arr); gseg=g(qseg_arr)
    same_dir = np.sign(gws)==np.sign(gseg)
    both_sep = abs(gws)>2 and abs(gseg)>2
    if both_sep and same_dir and gws>0: return "PASS(Quran>ORD both tok)", gws, gseg
    if both_sep and same_dir and gws<0: return "n/a (Quran<ORD)", gws, gseg
    return "FAIL/DEMOTE (tok-dependent or ~ORD)", gws, gseg

print(f"[{time.time()-t0:.1f}s] G10 RE-AUDIT of KEEP registry vs ordinary Arabic (Tabari), equal-N")
print(f"  word windows: Q(ws)={len(Wq['mi3_w'])} Q(seg)={len(Wqs['mi3_w'])} Tabari={len(Wt['mi3_w'])}")
print(f"  char windows: Q={len(Cq['mi5_c'])} Tabari={len(Ct['mi5_c'])}")
print(f"\n  {'metric':8s}{'Q(ws)':>9}{'Q(seg)':>9}{'Tabari':>9}  {'ws_sd':>6}{'seg_sd':>7}   G10 verdict")
for k in ["mi3_w","mi5_w","rep4_w","gz_w"]:
    v,gws,gseg=verdict(Wq[k],Wqs[k],Wt[k])
    print(f"  {k:8s}{Wq[k].mean():9.4f}{Wqs[k].mean():9.4f}{Wt[k].mean():9.4f}  {gws:+6.1f}{gseg:+7.1f}   {v}")
for k in ["mi5_c","rep4_c","gz_c"]:
    gws=(Cq[k].mean()-Ct[k].mean())/(Cq[k].std()+1e-9)
    v = "PASS(Quran>ORD)" if gws>2 else ("n/a(Quran<ORD)" if gws<-2 else "FAIL/DEMOTE (~ORD)")
    print(f"  {k:8s}{Cq[k].mean():9.4f}{'(char)':>9}{Ct[k].mean():9.4f}  {gws:+6.1f}{'':>7}   {v}")
print(f"\n[total {time.time()-t0:.1f}s]")
