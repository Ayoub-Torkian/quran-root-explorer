# PROBE B — takhsis detector (course M07). Pre-stated, run 2026-06-07, PYTHONHASHSEED=0, seed 0.
# RESULT: census إلا 661 occ / 603 verses (9.7%); ألا excluded (39); غير 147; ما لم 20.
# Typology: إلا من 46 · إلا هو 39 · إلا ما 35 · إلا قليلا 27 · إلا الذين 20 · إلا الله 19 ·
# necessity formula 5 sites (2:173, 5:3, 6:119!, 6:145, 16:115 — 6:119 is a 5th site beyond piece 6f).
# Cross-verse linkage (18 pre-stated pairs, 200 size-matched null sets): Jaccard z=+18.7, cosine z=+9.99,
# lastword z=+21.6; cross-sura subset z=+17.9/+9.9; POST-HOC robustness w/o 6 necessity pairs:
# Jaccard z=+3.52, cosine z=+2.67, seal-match ns. M07 verdict: GO (10 modules). EVIDENCE #82.
import sys, re, math, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import analysis as A
import numpy as np
from collections import Counter
rng = np.random.default_rng(0)
c = A.load_corpus(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Book6.xlsx"))
df = c.df; nl = A.normalize_letters
WA = re.compile(r"[^\W\d_]+", re.UNICODE)

V={}
order=[]
for i in range(len(df)):
    r=df.iloc[i]; key=(int(r[A.COL_SURAH]),int(r[A.COL_AYAH]))
    seg=str(r[A.COL_SEGMENTED]).split()
    words=[nl(w) for w in WA.findall(nl(str(r[A.COL_DIACRITIZED])))]
    roots=[x for x in str(r[A.COL_ROOTS]).split()]
    V[key]=dict(seg=seg, segf=[nl(t) for t in seg], words=words, roots=roots)
    order.append(key)

# ---- STEP 1: operator census ----
illa_occ=0; illa_verses=set(); ala=0; ghayr=0; ghayr_v=set(); malam=0; malam_v=set()
nxt=Counter()
for k in order:
    seg=V[k]["seg"]; segf=V[k]["segf"]; words=V[k]["words"]
    for j,t in enumerate(seg):
        if t=="إلا":
            illa_occ+=1; illa_verses.add(k)
            nxt[segf[j+1] if j+1<len(segf) else "<END>"]+=1
        if t=="ألا": ala+=1
        if segf[j]=="غير": ghayr+=1; ghayr_v.add(k)
    for j in range(len(words)-1):
        if words[j]=="ما" and words[j+1]=="لم": malam+=1; malam_v.add(k)
print(f"إلا occurrences: {illa_occ} in {len(illa_verses)} verses ({len(illa_verses)/6236*100:.1f}% of 6236); ألا (excluded): {ala}")
print(f"غير standalone: {ghayr} in {len(ghayr_v)} verses; ما لم bigram: {malam} in {len(malam_v)} verses")
print("إلا next-token top15:", nxt.most_common(15))
CLS={"الذين":"class carve-out (إلا الذين)","من":"person carve-out (إلا من)","ما":"object carve-out (إلا ما)",
     "الله":"theological restriction (إلا الله)","هو":"theological restriction (إلا هو)",
     "قليلا":"quantitative (إلا قليلا)","قليل":"quantitative (إلا قليلا)"}
ty=Counter()
for t,n in nxt.items():
    if t in CLS: ty[CLS[t]]+=n
# necessity formula
nec=[k for k in order if "اضطر" in "".join(V[k]["segf"]) and "غير" in V[k]["segf"]]
print("TYPOLOGY:", dict(ty))
print("necessity formula (اضطر…غير) verses:", len(nec), nec)
print("ما لم construction:", malam)

# ---- STEP 2: cross-verse rule<->exception linkage ----
PAIRS=[((2,219),(4,43)),((4,43),(5,90)),((2,219),(5,90)),
       ((30,39),(4,161)),((4,161),(3,130)),((3,130),(2,275)),
       ((2,173),(5,3)),((2,173),(6,145)),((2,173),(16,115)),((5,3),(6,145)),((5,3),(16,115)),((6,145),(16,115)),
       ((26,224),(26,227)),((103,2),(103,3)),
       ((2,185),(22,78)),((2,185),(4,28)),
       ((4,148),(4,75)),((4,148),(49,12))]
def metrics(a,b):
    ra,rb=set(V[a]["roots"]),set(V[b]["roots"])
    jac=len(ra&rb)/max(1,len(ra|rb))
    ca,cb=Counter(V[a]["roots"]),Counter(V[b]["roots"])
    keys=set(ca)|set(cb)
    va=np.array([ca[x] for x in keys]); vb=np.array([cb[x] for x in keys])
    cos=float(va@vb/(np.linalg.norm(va)*np.linalg.norm(vb)+1e-12))
    lw = V[a]["words"][-1]==V[b]["words"][-1]
    lr = (V[a]["roots"][-1]==V[b]["roots"][-1]) if V[a]["roots"] and V[b]["roots"] else False
    return jac,cos,lw,lr
def setmeans(pairs):
    ms=[metrics(a,b) for a,b in pairs]
    return (np.mean([m[0] for m in ms]),np.mean([m[1] for m in ms]),
            np.mean([m[2] for m in ms]),np.mean([m[3] for m in ms]))
# size buckets for matching
bylen={}
for k in order: bylen.setdefault(len(V[k]["roots"]),[]).append(k)
def matched(k):
    n=len(V[k]["roots"]); cand=[]
    for d in range(0,3):
        for m in (n-d,n+d):
            cand+=bylen.get(m,[])
        if len(cand)>=5: break
    return cand
def run(pairs,label):
    real=setmeans(pairs)
    nulls=[]
    for _ in range(200):
        ps=[]
        for a,b in pairs:
            ca=matched(a); cb=matched(b)
            x=ca[rng.integers(len(ca))]; y=cb[rng.integers(len(cb))]
            while y==x: y=cb[rng.integers(len(cb))]
            ps.append((x,y))
        nulls.append(setmeans(ps))
    nulls=np.array(nulls)
    names=["Jaccard","cosine","lastword-match","lastroot-match"]
    print(f"--- {label} (n={len(pairs)} pairs, 200 null sets) ---")
    for i,nm in enumerate(names):
        mu,sd=nulls[:,i].mean(),nulls[:,i].std()
        z=(real[i]-mu)/(sd+1e-12)
        print(f"  {nm:16s} real={real[i]:.4f}  null={mu:.4f}±{sd:.4f}  z={z:+.2f}")
    return real,nulls
run(PAIRS,"ALL 18 pre-stated pairs")
xs=[p for p in PAIRS if p[0][0]!=p[1][0]]
run(xs,"CROSS-SURA subset")
# per-pair detail
print("--- per-pair ---")
for a,b in PAIRS:
    j,co,lw,lr=metrics(a,b)
    print(f"  {a}<->{b}: jac={j:.3f} cos={co:.3f} lastword={lw} lastroot={lr}")

print("\n=== POST-HOC ROBUSTNESS (flagged): excluding the 6 necessity-recurrence pairs ===")
NEC={(2,173),(5,3),(6,145),(16,115)}
rest=[p for p in PAIRS if not (p[0] in NEC and p[1] in NEC)]
run(rest,"12 pairs w/o necessity cells")
