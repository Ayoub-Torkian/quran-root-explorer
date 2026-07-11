# -*- coding: utf-8 -*-
"""Fig 7 (PPMI attraction ego-network) + Fig 8 (validation: hapax bonds vs the whole hapax distribution).
All Arabic runs reshaped in place via A() so nothing renders backwards/disconnected."""
import json, collections, itertools, math
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np, networkx as nx
import re as _re
import arabic_reshaper
from bidi.algorithm import get_display
from matplotlib.lines import Line2D
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"; OUT=f"{R}/research/intrinsic/kawthar_figs"
_resh=arabic_reshaper.ArabicReshaper(configuration={'delete_harakat':True,'support_ligatures':False})
_AR=_re.compile(r'[؀-ۿݐ-ݿ]+')
def A(s):  # reshape ONLY Arabic runs, leave Latin/numbers/punctuation in place -> no backwards artifacts
    return _AR.sub(lambda m: get_display(_resh.reshape(m.group().replace('ک','ك').replace('ی','ي'))), s)
def ar(r): return A(r)
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا')
ayahs=[]
for line in open(f"{R}/research/two_books_genome/roots_by_ayah.tsv",encoding='utf-8'):
    line=line.rstrip('\n')
    if '\t' in line:
        _,rs=line.split('\t',1); ayahs.append(set(fa(x) for x in rs.split()))
N=len(ayahs)
cnt=collections.Counter(); co=collections.Counter()
for s in ayahs:
    for r in s: cnt[r]+=1
    for a,b in itertools.combinations(sorted(s),2): co[(a,b)]+=1
def pair(a,b): return co[(a,b)] if (a,b) in co else co[(b,a)]
def ppmi(a,b):
    c=pair(a,b)
    return max(0.0, math.log2(c*N/(cnt[a]*cnt[b]))) if c>0 else 0.0
INK='#10243A'; NAVY='#1D3557'; GREEN='#1D9E75'; GREEN_DK='#0F6E56'; RED='#E63946'; AMBER='#EF9F27'; BORD='#E2E8F1'; BTINT='#D7E6F7'; BORDEM='#C9D6E8'; GREY='#9fb0c4'
S=['عطو','کثر','صلو','ربب','نحر','شنء','بتر']; HAPAX={'نحر','بتر'}
topassoc={}
for r in S:
    minc = 1 if r in HAPAX else 3
    cand=[(ppmi(r,o), pair(r,o), o) for o in cnt if o!=r and pair(r,o)>=minc]
    cand.sort(reverse=True); topassoc[r]=cand[:6]
plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','text.color':INK})

# ===== FIG 7: PPMI attraction ego-network (recaptioned honestly) =====
ego=nx.Graph()
for r in S: ego.add_node(r, kind=('hapax' if r in HAPAX else 'surah'))
for r in S:
    for p,c,o in topassoc[r]:
        if o not in ego: ego.add_node(o, kind='assoc')
        ego.add_edge(r,o,ppmi=p)
for a,b in itertools.combinations(S,2):
    if pair(a,b)>0: ego.add_edge(a,b,ppmi=ppmi(a,b))
fig,ax=plt.subplots(figsize=(9.8,7.4)); ax.axis('off')
pos=nx.spring_layout(ego,k=1.35,seed=5,weight='ppmi',iterations=400)
_xs=[q[0] for q in pos.values()]; _ys=[q[1] for q in pos.values()]
ax.set_xlim(min(_xs)-0.18,max(_xs)+0.18); ax.set_ylim(min(_ys)-0.14,max(_ys)+0.16)
sizes=[(1100 if ego.nodes[n]['kind']=='surah' else 820 if ego.nodes[n]['kind']=='hapax' else 460) for n in ego.nodes()]
colors=[RED if ego.nodes[n]['kind']=='hapax' else NAVY if ego.nodes[n]['kind']=='surah' else BTINT for n in ego.nodes()]
ews=[ego[u][v]['ppmi'] for u,v in ego.edges()]
nx.draw_networkx_edges(ego,pos,width=[1.0+0.9*w for w in ews],edge_color=[GREEN_DK if w>=4 else BORDEM for w in ews],alpha=0.8,ax=ax)
nx.draw_networkx_nodes(ego,pos,node_size=sizes,node_color=colors,edgecolors='white',linewidths=1.3,ax=ax)
for n,(x,y) in pos.items():
    k=ego.nodes[n]['kind']
    if k=='surah': ax.text(x,y-0.10,ar(n),ha='center',va='top',fontsize=16,color=NAVY,fontweight='bold',zorder=6)
    elif k=='hapax': ax.text(x,y-0.10,ar(n),ha='center',va='top',fontsize=16,color=RED,fontweight='bold',zorder=6)
    else: ax.text(x,y+0.06,ar(n),ha='center',va='bottom',fontsize=13,color=INK,zorder=6)
leg=[Line2D([0],[0],marker='o',color='w',markerfacecolor=RED,markersize=12,label=A('hapax root (نحر, بتر)')),
     Line2D([0],[0],marker='o',color='w',markerfacecolor=NAVY,markersize=12,label='surah content root'),
     Line2D([0],[0],marker='o',color='w',markerfacecolor=BTINT,markersize=10,label='associate root'),
     Line2D([0],[0],color=GREEN_DK,lw=3,label=A('strong specific bond (بتر–شنء, PPMI≥4)'))]
ax.legend(handles=leg,loc='lower left',fontsize=11,frameon=True,framealpha=0.9,edgecolor=BORD)
ax.set_title(A("Figure 7.  Attraction lens (PPMI, frequency-controlled): rare roots sit on FEW edges.\n"
             "Only the بتر–شنء bond is both strong and statistically notable (p≈0.0005, §5.26); the hapax are\n"
             "neither peripheral by raw degree nor uniformly 'maximally bound' (see Figure 8)."),
             loc='left',fontsize=13,color=NAVY,fontweight='bold')
fig.tight_layout(); fig.savefig(f"{OUT}/fig13_ppmi_network.png",dpi=150,bbox_inches='tight'); fig.savefig(f"{OUT}/fig13_ppmi_network.svg",bbox_inches='tight'); plt.close(fig)
print("saved fig13_ppmi_network (Fig 7)")

# ===== FIG 8: VALIDATION — are the hapax 'maximally bound'? max-PPMI vs ALL hapax =====
def maxbond(r):
    return max((ppmi(r,o) for o in cnt if o!=r and pair(r,o)>0), default=0.0)
hapax_all=[r for r,c in cnt.items() if c==1]
hb=sorted(maxbond(r) for r in hapax_all)
import statistics as st
med=st.median(hb)
fig,ax=plt.subplots(figsize=(9.6,5.2))
ax.hist(hb,bins=30,color=BTINT,edgecolor='white',zorder=2)
ax.axvline(med,color=GREY,lw=1.5,ls='--',zorder=3); ax.text(med,ax.get_ylim()[1]*0.92,f" median of all {len(hapax_all)} hapax = {med:.1f}",color=INK,fontsize=11,va='top')
for r,col in [('نحر',RED),('بتر',GREEN_DK)]:
    v=maxbond(r); p=100.0*sum(1 for x in hb if x<v)/len(hb)
    ax.axvline(v,color=col,lw=2.4,zorder=4)
    ax.annotate(A(f"{r}  ({p:.0f}th pct)"),xy=(v,ax.get_ylim()[1]*0.6),xytext=(v+0.5,ax.get_ylim()[1]*0.72),
                color=col,fontsize=13,fontweight='bold',arrowprops=dict(arrowstyle='->',color=col,lw=1.4))
ax.set_xlabel("strongest single PPMI bond of a hapax root",fontsize=12,color=INK)
ax.set_ylabel("number of hapax roots",fontsize=12,color=INK)
ax.set_title(A("Figure 8.  Validation: are al-Kawthar's hapax 'maximally bound'? No.  Against the corpus's\n"
             f"{len(hapax_all)} once-occurring roots, نحر binds BELOW median (10th pct) and بتر is only moderate (66th).\n"
             "The earlier 'maximally specific' reading is not supported; what survives is the single بتر–شنء tie."),
             loc='left',fontsize=12.5,color=NAVY,fontweight='bold')
for sp in ['top','right']: ax.spines[sp].set_visible(False)
ax.grid(axis='y',color=BORD,lw=0.8,zorder=0)
fig.tight_layout(); fig.savefig(f"{OUT}/fig14_normalization.png",dpi=150,bbox_inches='tight'); fig.savefig(f"{OUT}/fig14_normalization.svg",bbox_inches='tight'); plt.close(fig)
print("saved fig14_normalization (Fig 8, repurposed to validation)")
