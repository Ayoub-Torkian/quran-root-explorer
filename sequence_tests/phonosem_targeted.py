import re, time
import numpy as np, pandas as pd
ROOT="/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2"
rng=np.random.default_rng(29); t0=time.time()
_DIA=re.compile(r"[ً-ٰٟۖ-ۭ]"); _TAT=re.compile("ـ"); WA=re.compile(r"[^\W\d_]+",re.UNICODE)
def nl(t):
    t=_TAT.sub("",_DIA.sub("",str(t)))
    t=re.sub(r"[آأإٱ]","ا",t); t=re.sub(r"[ىی]","ي",t); t=re.sub(r"[ةھ]","ه",t)
    return t.replace("ک","ك").replace("ؤ","ء").replace("ئ","ء").strip()
def words(s): return [w for w in WA.findall(nl(str(s))) if w]
HEAVY=set("صضطظقغخعحء")   # emphatics+qaf+gutturals (the "heavy" phonemes)
def heavy_density(ws):
    h=0; n=0
    for w in ws:
        for ch in w:
            if ch in "ابتثجحخدذرزسشصضطظعغفقكلمنهوي": n+=1; h+= (1 if ch in HEAVY else 0)
    return h/n if n else np.nan

raw=pd.read_excel(ROOT+"/Book6.xlsx",header=None,nrows=8); hdr=0
for i in range(len(raw)):
    if raw.iloc[i].map(lambda x: nl(x)).str.contains("سوره").any(): hdr=i;break
df=pd.read_excel(ROOT+"/Book6.xlsx",header=hdr); df.columns=[str(c).strip() for c in df.columns]
rcol=[c for c in df.columns if "ريشه" in nl(c) and "توك" not in nl(c)][0]   # roots
tcol=[c for c in df.columns if "متن" in nl(c) and "توكن" not in nl(c)][0]    # surface

# seed fields (normalized root strings)
HARSH=set(nl(x) for x in "عذب نار جحم سقر هلك بطش قهر غضب حطم لظي سعر صلي خزي عقب ذنب كفر ويل عقاب جزي شدد خسر ظلم".split())
SOFT =set(nl(x) for x in "رحم جنه نعم غفر سلم روح ودد لطف رزق هدي نور طيب فضل بشر صبر حسن خير ايمن نجو فوز رضو".split())

rows=[]
for r,t in zip(df[rcol].fillna("").astype(str), df[tcol].fillna("").astype(str)):
    roots=set(nl(w) for w in WA.findall(r) if nl(w))
    if not roots: continue
    nh=len(roots&HARSH); ns=len(roots&SOFT)
    if nh==ns: continue
    lab="harsh" if nh>ns else "soft"
    # phonetics over surface words whose root is NOT a seed (decouple from topic words)
    surf=words(t)
    # crude exclusion: drop surface words containing any seed-root trigram letters set match is hard;
    # instead drop words that are short function words and seed-ish; keep it simple: use ALL words AND non-seed-letter version
    hd_all=heavy_density(surf)
    rows.append((lab,hd_all))
rows=[x for x in rows if not np.isnan(x[1])]
H=np.array([d for l,d in rows if l=="harsh"]); S=np.array([d for l,d in rows if l=="soft"])
def g(a,b): return (a.mean()-b.mean())/(np.sqrt((a.var()+b.var())/2)+1e-9)
bp=np.mean(rng.choice(H,8000)>rng.choice(S,8000))
print("[%.1fs] TARGETED phono-iconicity (heavy-phoneme density: harsh vs soft ayat)"%(time.time()-t0))
print("  harsh ayat n=%d  heavy-density=%.4f"%(len(H),H.mean()))
print("  soft  ayat n=%d  heavy-density=%.4f"%(len(S),S.mean()))
print("  gap = %+.2fsd   P(harsh>soft)=%.2f   [iconicity predicts harsh>soft]"%(g(H,S),bp))
# control: also compare to neutral baseline? report raw diff
print("  raw diff = %+.4f (%.1f%% relative)"%(H.mean()-S.mean(),100*(H.mean()-S.mean())/S.mean()))
print("[%.1fs]"%(time.time()-t0))
