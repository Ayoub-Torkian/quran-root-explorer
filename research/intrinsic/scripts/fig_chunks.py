# -*- coding: utf-8 -*-
"""#2 Sūra-chunks as graph NODES: each long sūra is a SUBGRAPH spanning the timeline. Chunk = node at its
anchored time; dotted = same-sūra membership; node colour = which developmental thread it joins. Locked UI."""
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
INK='#10243A';NAVY='#1D3557';GREEN_DK='#0F6E56';RED='#E63946';AMBER='#EF9F27';BLUE='#378ADD';PURP='#7A5AA6';BORD='#E2E8F1';GTINT='#F4F9F7';BTINT='#EAF2FB'
TH={'event':NAVY,'khamr':GREEN_DK,'qitāl':AMBER,'ribā':GREEN_DK,'referent':BLUE,'ritual':PURP}
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':INK})
fig,ax=plt.subplots(figsize=(13.8,6.6))
# sura -> list of (chunk-label, time AH, thread)
SUR={
 'Baqara (2)\nnuzūl 87':[('2:142-150 qibla',2,'ritual'),('2:219 khamr',2,'khamr'),('2:216 qitāl',2.3,'qitāl'),
                         ('2:275 ribā',2.6,'ribā'),('2:196 ḥajj',6,'ritual')],
 'Āl ʿImrān (3)\nnuzūl 89':[('3:130 ribā',3,'ribā'),('3:121-175 Uhud',3,'event'),('3:33-63 Mubāhala',9.5,'event')],
 'Tawba (9)\nnuzūl 114':[('9:100 muhājirūn',1,'referent'),('9:5 qitāl',9,'qitāl'),('9:38 Tabūk',9,'event'),('9:107 Ḍirār',9,'event')],
 'Nisāʾ (4)\nnuzūl 92':[('4:2-28 family law',4,'ritual'),('4:71-104 jihād/munāfiq',4.5,'qitāl'),('4:153 PoB',5,'referent')],
}
ys=list(range(len(SUR)-1,-1,-1))
ax.axvspan(0,10.6,color=BTINT,zorder=0)
for xw in (2,6,9): ax.axvline(xw,color=BORD,lw=9,alpha=0.45,zorder=0)
for (name,chunks),y in zip(SUR.items(),ys):
    xs=[c[1] for c in chunks]
    ax.plot([min(xs),max(xs)],[y,y],ls=':',color='#9DB2CC',lw=1.8,zorder=1)  # same-sūra membership
    ax.text(-0.4,y,name,ha='right',va='center',fontsize=12,color=NAVY,fontweight='bold')
    seen={}
    for lab,x,th in chunks:
        yy=y+(0.16 if seen.get(round(x),0)%2 else -0.0); seen[round(x)]=seen.get(round(x),0)+1
        ax.scatter([x],[yy],s=150,color=TH[th],zorder=4,edgecolors='white',linewidths=1.3)
        ax.text(x,yy+0.13,lab,ha='center',va='bottom',fontsize=9.3,color=TH[th],fontweight='bold',rotation=16,zorder=5)
    if max(xs)-min(xs)>3:
        ax.annotate('',(max(xs),y),(min(xs),y),arrowprops=dict(arrowstyle='<->',color=RED,lw=0.8,alpha=0.5))
        ax.text((min(xs)+max(xs))/2,y-0.22,f"spans {min(xs):g}→{max(xs):g} AH",ha='center',fontsize=9.5,color=RED,fontweight='bold')
ax.set_xlim(-2.2,11.2); ax.set_ylim(-0.7,len(SUR)-0.3); ax.set_yticks([])
ax.set_xticks([0,2,3,4,5,6,9,10]); ax.set_xticklabels(['Hijra','2','3','4','5','6','9','10'],fontsize=11,color=INK)
for s in ['top','right','left']: ax.spines[s].set_visible(False)
ax.spines['bottom'].set_color(BORD)
# legend
from matplotlib.lines import Line2D
leg=[Line2D([0],[0],marker='o',color='w',markerfacecolor=c,markersize=10,label=k) for k,c in TH.items()]
ax.legend(handles=leg,fontsize=10.5,loc='lower right',frameon=False,ncol=3,title='thread joined by chunk')
ax.set_xlabel('revealed time (AH) →   ·   dotted line = same-sūra membership (one sūra, chunks at different times)',fontsize=12.5,color=INK)
ax.set_title('Sūra-chunks as graph nodes: a long sūra is a SUBGRAPH spanning the timeline',loc='left',fontsize=16,fontweight='bold',color=NAVY,pad=12)
fig.tight_layout(); fig.savefig('research/intrinsic/chrono_figs/chunks_subgraph.png',dpi=150,bbox_inches='tight'); print('saved chunks_subgraph.png')
