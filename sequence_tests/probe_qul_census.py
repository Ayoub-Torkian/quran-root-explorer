# PROBE A — the qul census (P8 / course M06). Pre-stated, run 2026-06-07, PYTHONHASHSEED=0.
# RESULT: 308 qul-verses / 334 occ / 58 suras; buckets: other 247, creed 21, question-response 14,
# gheyb-redirect 10, supplication 9, challenge-retort 7; sanity 14/14 protocol cells in
# question-response; RESPONSE same-verse 48 (15.6%) vs corpus base 6.8% -> z=+6.07;
# same+prev-verse 78 (25.3%); PROCLAMATION (same-verse criterion) 260 (84.4%). EVIDENCE #81.
import sys, re, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import analysis as A
from collections import Counter
c = A.load_corpus(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Book6.xlsx"))
df = c.df
WA = re.compile(r"[^\W\d_]+", re.UNICODE)
nl = A.normalize_letters
INC = {"قل","فقل","وقل"}
ASK = ("يسالونك","يستفتونك")  # substring match catches و- proclitic
SPEECH = {"يسالونك","ويسالونك","يستفتونك","قالوا","وقالوا","فقالوا","يقولون","ويقولون","سيقولون","فسيقولون","قيل"}
GHEYB = {"العلم","علمها","الغيب","يعلم","اعلم"}
SUPP = {"رب","اللهم"}
CREED = {"هو","الله","امنا"}
CHAL = {"فاتوا","هاتوا"}

rows=[]
for i in range(len(df)):
    r=df.iloc[i]
    ws=[nl(w) for w in WA.findall(nl(str(r[A.COL_DIACRITIZED])))]
    rows.append((int(r[A.COL_SURAH]),int(r[A.COL_AYAH]),ws))

def classify_verse(ws):
    has_ask = any(any(a in w for a in ASK) for w in ws)
    occ=[j for j,w in enumerate(ws) if w in INC]
    if not occ: return None
    if has_ask: return "question-response", len(occ)
    # occurrence-level, verse takes highest-priority bucket among its quls
    best=None; order=["gheyb-redirect","supplication","creed-declaration","challenge-retort","other"]
    for j in occ:
        nxt = ws[j+1] if j+1<len(ws) else ""
        win = ws[j+1:j+5]
        if any(w in GHEYB for w in win): b="gheyb-redirect"
        elif nxt in SUPP: b="supplication"
        elif nxt in CREED: b="creed-declaration"
        elif nxt in CHAL: b="challenge-retort"
        else: b="other"
        if best is None or order.index(b)<order.index(best): best=b
    return best, len(occ)

buck=Counter(); occ_total=0; qul_verses=[]; suras=Counter()
resp_same=0; resp_prev=0
prev_ws=None; prev_key=None
for k,(s,a,ws) in enumerate(rows):
    res=classify_verse(ws)
    if res:
        b,n=res; buck[b]+=1; occ_total+=n; qul_verses.append((s,a,b)); suras[s]+=1
        same = any(w in SPEECH for w in ws) or any(any(x in w for x in ASK) for w in ws)
        if same: resp_same+=1
        else:
            # secondary: previous verse trigger
            if k>0 and rows[k-1][0]==s:
                pws=rows[k-1][2]
                if any(w in SPEECH for w in pws): resp_prev+=1
print("TOTAL qul-verses:", len(qul_verses), " occurrences:", occ_total)
print("suras with >=1 qul-verse:", len(suras), "/114; top:", suras.most_common(8))
print("buckets:", dict(buck))
prot=[(2,189),(2,215),(2,217),(2,219),(2,220),(2,222),(5,4),(7,187),(8,1),(17,85),(18,83),(20,105),(4,127),(4,176)]
qmap={(s,a):b for s,a,b in qul_verses}
ok=sum(1 for p in prot if qmap.get(p)=="question-response")
print("SANITY protocol cells in question-response:", ok, "/14 (79:42 qul-less, outside census)")
print("RESPONSE same-verse:", resp_same, f"({resp_same/len(qul_verses)*100:.1f}%)")
print("RESPONSE prev-verse extra:", resp_prev, " => same+prev:", resp_same+resp_prev,
      f"({(resp_same+resp_prev)/len(qul_verses)*100:.1f}%)")
print("PROCLAMATION (no same-verse trigger):", len(qul_verses)-resp_same,
      f"({(len(qul_verses)-resp_same)/len(qul_verses)*100:.1f}%)")
# baseline: among ALL verses, speech-trigger rate (for context)
allspeech=sum(1 for s,a,ws in rows if any(w in SPEECH for w in ws))
print("context: verses with speech-trigger corpus-wide:", allspeech, f"({allspeech/6236*100:.1f}%)")
# binomial: are qul verses enriched for speech triggers?
import math
p0=allspeech/6236; n=len(qul_verses); k=resp_same
mu=n*p0; sd=math.sqrt(n*p0*(1-p0)); print(f"enrichment z=({k}-{mu:.1f})/{sd:.2f} = {(k-mu)/sd:+.2f}")
# bucket examples
ex=Counter()
for s,a,b in qul_verses:
    if ex[b]<3: print("  ex",b,s,a); ex[b]+=1
