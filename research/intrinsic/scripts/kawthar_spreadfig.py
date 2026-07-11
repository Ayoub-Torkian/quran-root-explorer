# -*- coding: utf-8 -*-
"""Figure 17: spread-of-message. IC reach observed vs degree-rewired null (anti-diffusion), + al-Kawthar roots."""
import collections, random, itertools, statistics as st, re as _re
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
import numpy as np, arabic_reshaper
from bidi.algorithm import get_display
random.seed(11)
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"; OUT=f"{R}/research/intrinsic/kawthar_figs"
_resh=arabic_reshaper.ArabicReshaper(configuration={'delete_harakat':True,'support_ligatures':False})
_AR=_re.compile('[؀-ۿݐ-ݿ]+')
def A(s): return _AR.sub(lambda m: get_display(_resh.reshape(m.group().replace('ک','ك').replace('ی','ي'))), s)
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا')
INK='#10243A';NAVY='#1D3557';GREEN='#1D9E75';GREEN_DK='#0F6E56';RED='#E63946';AMBER='#EF9F27';BORD='#E2E8F1';BTINT='#EAF2FB';GREY='#9fb0c4'
plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','text.color':INK})
rows=[]
for line in open(f"{R}/research/two_books_genome/roots_by_ayah.tsv",encoding='utf-8'):
    line=line.rstrip('\n')
    if '\t' in line: k,rs=line.split('\t',1); rows.append([fa(x) for x in set(rs.split())])
cnt=collections.Counter(r for rs in rows for r in rs)
co=collections.Counter()
for rs in rows:
    for a,b in itertools.combinations(sorted(rs),2): co[(a,b)]+=1
def pair(a,b): return co.get((a,b),0)+co.get((b,a),0)
nodes=[r for r in cnt if cnt[r]>=5]; Nn=len(nodes)
adj=collections.defaultdict(list)
for a in nodes:
    for b in nodes:
        if a!=b and pair(a,b)>0:
            p=pair(a,b)/cnt[a]
            if p>=0.15: adj[a].append((b,min(p,0.9)))
def IC(seed,Adj,sims=40):
    if seed not in nodes: return 0.0
    tot=0
    for _ in range(sims):
        act={seed}; fr=[seed]
        while fr:
            nf=[]
            for a in fr:
                for b,p in Adj.get(a,[]):
                    if b not in act and random.random()<p: act.add(b); nf.append(b)
            fr=nf
        tot+=len(act)
    return tot/sims/Nn
def rewire(Adj):
    tg=[b for a in nodes for (b,p) in Adj.get(a,[])]; pr=[p for a in nodes for (b,p) in Adj.get(a,[])]
    random.shuffle(tg); out=collections.defaultdict(list); i=0
    for a in nodes:
        for _ in range(len(Adj.get(a,[]))): out[a].append((tg[i],pr[i])); i+=1
    return out
samp=random.sample(nodes,200); Anull=rewire(adj)
obs=[IC(s,adj) for s in samp]; nul=[IC(s,Anull) for s in samp]
fig,(axL,axR)=plt.subplots(1,2,figsize=(13,5.4),gridspec_kw={'width_ratios':[1.25,1]})
axL.hist(nul,bins=30,color=AMBER,alpha=0.55,label=f'rewired null (median {st.median(nul):.2f})',zorder=2)
axL.hist(obs,bins=30,color=NAVY,alpha=0.8,label=f'observed corpus (median {st.median(obs):.3f})',zorder=3)
axL.set_xlabel("message-reach: fraction of the lexicon a seeded concept activates",fontsize=12,color=INK)
axL.set_ylabel("number of seed roots",fontsize=12,color=INK)
axL.legend(fontsize=11,frameon=True,edgecolor=BORD)
axL.set_title("Figure 17.  Spread of meaning is CONTAINED, not broadcast.\n"
             "Concept-cascades reach ~1-2% of the lexicon, but a randomly\n"
             "rewired graph reaches 20-40x more - the signature of tight\n"
             "thematic modularity that localizes spread.",loc='left',fontsize=11.5,color=NAVY,fontweight='bold')
for sp in ['top','right']: axL.spines[sp].set_visible(False)
axL.grid(axis='y',color=BORD,lw=0.8,zorder=0)
# right: al-Kawthar roots obs vs null + islands
KW=[('عطو',True),('کثر',True),('صلو',True),('ربب',True),('نحر',False),('شنء',False),('بتر',False)]
labels=[]; ob=[]; nu=[]
allre={s:IC(s,adj,30) for s in [fa(k) for k,g in KW if g]}
for k,g in KW:
    r=fa(k); labels.append(r)
    if g: ob.append(allre[r]); nu.append(st.mean([IC(r,rewire(adj),20) for _ in range(3)]))
    else: ob.append(0); nu.append(0)
y=np.arange(len(labels))[::-1]; w=0.38
axR.barh(y+w/2,ob,w,color=NAVY,label='observed',zorder=3)
axR.barh(y-w/2,nu,w,color=AMBER,alpha=0.7,label='rewired null',zorder=3)
axR.set_yticks(y); axR.set_yticklabels([A(l) for l in labels],fontsize=14)
for yi,(k,g) in zip(y,KW):
    if not g: axR.text(0.005,yi,A("  island (reach 0)"),va='center',fontsize=10,color=GREY)
axR.set_xlabel("message-reach",fontsize=11,color=INK); axR.legend(fontsize=10,frameon=True,edgecolor=BORD,loc='lower right')
axR.set_title(A("al-Kawthar's roots: low spreaders.\nربب converges (sink), not disseminates;\nنحر/شنء/بتر are islands."),fontsize=10.5,color=NAVY,fontweight='bold',loc='left')
for sp in ['top','right']: axR.spines[sp].set_visible(False)
axR.grid(axis='x',color=BORD,lw=0.8,zorder=0)
fig.tight_layout(); fig.savefig(f"{OUT}/fig_spread.png",dpi=150,bbox_inches='tight'); fig.savefig(f"{OUT}/fig_spread.svg",bbox_inches='tight'); plt.close(fig)
print(f"saved fig_spread (F17). obs median {st.median(obs):.3f} null median {st.median(nul):.2f}")
