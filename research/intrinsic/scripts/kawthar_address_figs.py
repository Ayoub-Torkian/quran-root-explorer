# -*- coding: utf-8 -*-
"""Fig 10 (address map), Fig 11 (two registers), Fig 12 (directed self-interpretation). Arabic labels, decluttered."""
import json, re, collections, itertools
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np, networkx as nx
from matplotlib.lines import Line2D
import arabic_reshaper
from bidi.algorithm import get_display
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"; OUT=f"{R}/research/intrinsic/kawthar_figs"
_resh=arabic_reshaper.ArabicReshaper(configuration={'delete_harakat':True,'support_ligatures':False})
_AR=re.compile('[؀-ۿݐ-ݿ]+')
def ar(s): return _AR.sub(lambda m: get_display(_resh.reshape(m.group().replace('ک','ك').replace('ی','ي'))), s)
INK='#10243A'; NAVY='#1D3557'; GREEN='#1D9E75'; GREEN_DK='#0F6E56'; RED='#E63946'; AMBER='#EF9F27'; BORD='#E2E8F1'; BTINT='#EAF2FB'; BORDEM='#C9D6E8'; GREY='#9fb0c4'
plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','text.color':INK})
ara=json.load(open(f"{R}/arabic.json",encoding='utf-8'))
DIAC=re.compile(r'[ً-ْٰـ]')
def strip(s): return DIAC.sub('',s).replace('ک','ك').replace('ی','ي')
SNAME={1:'الفاتحة',93:'الضحى',94:'الشرح',108:'الكوثر',82:'الانفطار',20:'طه',75:'القيامة',
       110:'النصر',101:'القارعة',79:'النازعات',89:'الفجر',17:'الإسراء',13:'الرعد',
       112:'الإخلاص',109:'الكافرون',113:'الفلق',114:'الناس',27:'النمل',6:'الأنعام',73:'المزمل'}
sur=collections.defaultdict(list)
for k,t in ara.items():
    s,a=map(int,k.split(':')); sur[s].append((a,t))
def toks(t,s,a):
    w=strip(t).split()
    if a==1 and s not in (1,9): w=w[4:]
    return w
def ka(s,ays): return sum(1 for a,t in ays for w in toks(t,s,a) if w.endswith('ك') and len(w)>1)
def qul(s,ays): return sum(1 for a,t in ays for w in toks(t,s,a) if w=='قل')
rows=[]
for s,ays in sur.items():
    nt=sum(len(toks(t,s,a)) for a,t in ays)
    if nt>=10 and len(ays)>=3: rows.append((s,nt,ka(s,ays),round(100*ka(s,ays)/nt,1),qul(s,ays)))
rows.sort(key=lambda r:-r[3])

# ===== FIGURE 10 =====
fig,(axA,axB)=plt.subplots(1,2,figsize=(13.0,5.8),gridspec_kw={'width_ratios':[1.1,1]})
top=rows[:12]; y=np.arange(len(top))[::-1]
dens=[d for *_,d,q in top]
bar_c=[GREEN if s in (108,94,93) else NAVY for s,*_ in top]
axA.barh(y,dens,color=bar_c,zorder=3,height=0.62)
for yi,(s,nt,k,d,q) in zip(y,top):
    axA.text(d+0.4,yi,f"{d:.1f}%",va='center',fontsize=12,color=INK)
    axA.text(0.5,yi,ar(SNAME.get(s,str(s)))+f"  ({s})",va='center',ha='left',fontsize=13,color='white',fontweight='bold',zorder=5)
    if q>0: axA.text(d+3.0,yi,f"qul×{q}",va='center',fontsize=11,color=RED)
axA.set_yticks([]); axA.set_xlim(0,34); axA.set_xlabel("second-person -ك per 100 (non-basmala) tokens",fontsize=12,color=INK)
axA.set_title("A.  Density of address to the Prophet",fontsize=12.5,color=NAVY,fontweight='bold',loc='left',pad=8)
for sp in ['top','right']: axA.spines[sp].set_visible(False)
axA.grid(axis='x',color=BORD,lw=0.8,zorder=0)
axA.text(0.985,0.04,"green = gift-and-defence cluster (qul = 0)",transform=axA.transAxes,ha='right',fontsize=10.5,color=GREEN_DK)
axB.axis('off')
axB.text(0,1.0,"B.  Which 'giving' verb reaches the Prophet (2nd-person)?",fontsize=12.5,color=NAVY,fontweight='bold',va='top',transform=axB.transAxes)
verbs=[('عطو','aʿṭā','12 occ.','only الضحى + الكوثر','93:5,  108:1',True),
       ('شرح','sharaḥa','5 occ.','only الشرح','94:1',True),
       ('وهب','wahaba','22 occ.','NEVER to the Prophet','only progeny → Ibrāhīm, Zakariyyā, Dāwūd…',False)]
yy=0.82
for root,lat,occ,note,chips,reaches in verbs:
    axB.text(0.03,yy,ar(root),fontsize=22,color=NAVY,fontweight='bold',va='center',transform=axB.transAxes)
    axB.text(0.20,yy+0.035,lat,fontsize=12,color=INK,va='center',style='italic',transform=axB.transAxes)
    axB.text(0.20,yy-0.05,occ,fontsize=11,color=GREY,va='center',transform=axB.transAxes)
    axB.text(0.42,yy+0.035,ar("→ "+note),fontsize=11.5,color=(GREEN_DK if reaches else GREY),va='center',fontweight=('bold' if reaches else 'normal'),transform=axB.transAxes)
    axB.text(0.42,yy-0.05,ar(chips),fontsize=10.5,color=(GREEN if reaches else GREY),va='center',transform=axB.transAxes)
    yy-=0.255
axB.text(0.03,0.03,ar("The personal gift is named with the open verb عطو + genus-noun كوثر,\nnot with وهب (a specific child) — underwriting the open referent (§5.11)."),fontsize=10.5,color=INK,va='bottom',transform=axB.transAxes)
fig.suptitle("Figure 10.  The map of address: al-Kawthar leads the Qurʾān in personal address, inside the gift-to-the-Prophet cluster",x=0.01,ha='left',fontsize=13,color=NAVY,fontweight='bold')
fig.tight_layout(rect=[0,0,1,0.93]); fig.savefig(f"{OUT}/fig_addr_map.png",dpi=150,bbox_inches='tight'); fig.savefig(f"{OUT}/fig_addr_map.svg",bbox_inches='tight'); plt.close(fig)
print("saved fig_addr_map")

# ===== FIGURE 11: two registers (decluttered) =====
fig,ax=plt.subplots(figsize=(9.4,6.4))
ax.scatter([d for *_,d,q in rows],[q for *_,d,q in rows],s=24,color=GREY,alpha=0.5,zorder=2,edgecolors='none')
def mark(s,col,dx,dy,ha='left'):
    for ss,nt,k,d,q in rows:
        if ss==s:
            ax.scatter([d],[q],s=130,color=col,zorder=4,edgecolors='white',linewidths=1.3)
            ax.annotate(ar(SNAME.get(s,str(s)))+f" ({s})",(d,q),xytext=(d+dx,q+dy),fontsize=12.5,color=col,fontweight='bold',
                        ha=ha,arrowprops=dict(arrowstyle='-',color=col,lw=0.8))
            return
mark(108,GREEN,-6.5,2.2); mark(93,GREEN,-5.2,2.2); mark(94,GREEN,-2.0,4.2)
mark(6,RED,0.6,0.0); mark(17,RED,0.6,0.0); mark(13,RED,0.6,-0.3)
# group the qul-openers with one annotation
ax.annotate(ar("قل-سور (109، 112، 113، 114)"),(5,1),xytext=(7.5,6.0),fontsize=12,color=AMBER,fontweight='bold',
            arrowprops=dict(arrowstyle='->',color=AMBER,lw=1.0))
for s in (109,112,113,114):
    for ss,nt,k,d,q in rows:
        if ss==s: ax.scatter([d],[q],s=70,color=AMBER,zorder=3,edgecolors='white',linewidths=1.0)
ax.set_xlabel("PERSONAL register →  second-person -ك per 100 tokens",fontsize=12.5,color=GREEN_DK)
ax.set_ylabel(ar("OFFICE register →  count of  قل  (\"say!\")"),fontsize=12.5,color=RED)
ax.set_xlim(-1,33); ax.set_ylim(-1.5,16)
ax.set_title("Figure 11.  The two registers are near-orthogonal: al-Kawthar sits at the extreme of the personal\naxis with zero office-marker; the qul-sūras occupy the other arm.",loc='left',fontsize=12.5,color=NAVY,fontweight='bold')
for sp in ['top','right']: ax.spines[sp].set_visible(False)
ax.grid(color=BORD,lw=0.8,zorder=0)
fig.tight_layout(); fig.savefig(f"{OUT}/fig_two_registers.png",dpi=150,bbox_inches='tight'); fig.savefig(f"{OUT}/fig_two_registers.svg",bbox_inches='tight'); plt.close(fig)
print("saved fig_two_registers")

# ===== FIGURE 12: directed self-interpretation network (manual layout, decluttered) =====
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا')
ayahs=[]
for line in open(f"{R}/research/two_books_genome/roots_by_ayah.tsv",encoding='utf-8'):
    line=line.rstrip('\n')
    if '\t' in line: _,rs=line.split('\t',1); ayahs.append(set(fa(x) for x in rs.split()))
cnt=collections.Counter(); co=collections.Counter()
for st in ayahs:
    for r in st: cnt[r]+=1
    for a,b in itertools.combinations(sorted(st),2): co[(a,b)]+=1
def pair(a,b): return co.get((a,b),0)+co.get((b,a),0)
def P(a,b): return pair(a,b)/cnt[b] if cnt[b] else 0   # P(a | b)
pos={'صلو':(-1.45,0.45),'نحر':(-0.55,0.95),'ربب':(0.0,0.0),'عطو':(-1.05,-0.85),'شنء':(0.95,0.15),'بتر':(1.55,-0.55)}
HAP={'نحر','بتر'}
edges=[('صلو','نحر'),('ربب','نحر'),('ربب','عطو'),('ربب','شنء'),('شنء','بتر'),('بتر','شنء')]
fig,ax=plt.subplots(figsize=(9.8,6.6)); ax.axis('off')
ax.set_xlim(-2.0,2.1); ax.set_ylim(-1.5,1.5)
for u,v in edges:
    w=P(u,v); strong=w>=0.8
    ax.annotate("",xy=pos[v],xytext=pos[u],
        arrowprops=dict(arrowstyle='-|>',color=GREEN_DK if strong else BORDEM,lw=1.2+3.0*w,
                        shrinkA=26,shrinkB=26,alpha=0.95,connectionstyle='arc3,rad=0.10'))
    mx,my=(pos[u][0]+pos[v][0])/2,(pos[u][1]+pos[v][1])/2
    ax.text(mx,my+0.07,f"{w:.2f}",fontsize=11.5,color=GREEN_DK if strong else INK,ha='center',fontweight=('bold' if strong else 'normal'),
            bbox=dict(boxstyle='round,pad=0.14',fc='white',ec='none',alpha=0.85))
for n,(x,yv) in pos.items():
    ax.scatter([x],[yv],s=(1700 if n in HAP else 1300),color=(RED if n in HAP else NAVY),edgecolors='white',linewidths=1.6,zorder=4)
    ax.text(x,yv,ar(n),ha='center',va='center',fontsize=16,color='white',fontweight='bold',zorder=6)
leg=[Line2D([0],[0],marker='o',color='w',markerfacecolor=RED,markersize=13,label=ar('hapax (نحر، بتر) — fixed by context')),
     Line2D([0],[0],marker='o',color='w',markerfacecolor=NAVY,markersize=13,label='content root'),
     Line2D([0],[0],color=GREEN_DK,lw=3,label='P(interpreter | term) ≥ 0.8 (reliable)'),
     Line2D([0],[0],color=BORDEM,lw=2,label='weaker conditional link')]
ax.legend(handles=leg,loc='upper right',fontsize=10.5,frameon=True,framealpha=0.92,edgecolor=BORD)
ax.set_title(ar("Figure 12.  Self-interpretation, directed (القرآن يفسر بعضه بعضا).  Arrow a→b = \"a reliably accompanies b\" P(a|b).\n"
             "بتر co-occurs with شنء (the only بتر verse is a شنء verse); these conditionals rest on single\n"
             "co-occurrences (n=1) — suggestive, not significant except بتر–شنء (p≈0.0005). See §5.26."),loc='left',fontsize=12,color=NAVY,fontweight='bold')
fig.tight_layout(); fig.savefig(f"{OUT}/fig_selfinterp.png",dpi=150,bbox_inches='tight'); fig.savefig(f"{OUT}/fig_selfinterp.svg",bbox_inches='tight'); plt.close(fig)
print("saved fig_selfinterp (manual)")
