# -*- coding: utf-8 -*-
"""The ORGAN CORE — qalb · nafs · sadr · fuad: who connects to whom. Focused, hand-laid view so the four organs'
relations read clearly. Internal ties = solid lines between organs (weight labelled); each organ's outward
attachments = spokes (top 4 by PPMI weight, coloured by the neighbour's role). MEASURED edges/weights; layout for legibility."""
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
from matplotlib.lines import Line2D
import json, re, math, arabic_reshaper
from bidi.algorithm import get_display
_resh=arabic_reshaper.ArabicReshaper(configuration={'delete_harakat':False,'support_ligatures':False})
_AR=re.compile(r'[؀-ۿ]+(?:\s+[؀-ۿ]+)*')
def A(s): return _AR.sub(lambda m:get_display(_resh.reshape(m.group().replace('ک','ك').replace('ی','ي'))),s) if s else s
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2/research/intrinsic"
GM=json.load(open(R+"/anatomy_figs/inner_self_graph_metrics.json",encoding='utf-8'))
ROLEC={"self":"#1D3557","cog":"#378ADD","act":"#0F6E56","up":"#1D9E75","down":"#E63946","amp":"#EF9F27","bound":"#7A5AA6","dom":"#94A3B8","out_g":"#0F6E56","out_r":"#C1121F","root":"#B5651D"}
roles=GM['roles']; edges=GM['edges']
ORG={"قلب":(0.0,0.0),"فؤاد":(0.0,2.45),"صدر":(2.65,0.0),"نفس":(-2.65,0.0)}
ORGSET=set(ORG); DIR={"قلب":270,"فؤاد":90,"صدر":0,"نفس":180}
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':'#10243A'})
fig,ax=plt.subplots(figsize=(14.5,9.0)); ax.axis('off'); ax.set_aspect('equal')
ax.set_xlim(-6.2,6.2); ax.set_ylim(-3.4,5.2)
ax.set_title("The organ core — qalb · nafs · ṣadr · fuʾād : who connects to whom (MEASURED PPMI). "
             "Internal ties solid; each organ's strongest outward links are spokes (coloured by role).",
             fontsize=13.5, fontweight='bold', color='#1D3557', pad=12)
# internal organ-organ edges
for a,b,w in edges:
    if a in ORGSET and b in ORGSET:
        if {a,b}=={"صدر","نفس"}:
            # faint curved arc below qalb (avoid crossing the hub)
            ax.add_patch(FancyArrowPatch(ORG[a],ORG[b],connectionstyle="arc3,rad=0.42",arrowstyle='-',
                         lw=1.1,ls=(0,(2,2)),color='#AEBED0',zorder=1))
            ax.text(0.0,-1.45,"%.1f"%w,ha='center',va='center',fontsize=11.5,color='#566B82',
                    bbox=dict(boxstyle='round,pad=0.12',fc='white',ec='none',alpha=.85),zorder=5)
        else:
            ax.plot([ORG[a][0],ORG[b][0]],[ORG[a][1],ORG[b][1]],color='#1D3557',lw=1.4+1.8*w,zorder=1,solid_capstyle='round')
            ax.text((ORG[a][0]+ORG[b][0])/2,(ORG[a][1]+ORG[b][1])/2,"%.1f"%w,ha='center',va='center',
                    fontsize=12,fontweight='bold',color='#1D3557',bbox=dict(boxstyle='round,pad=0.14',fc='white',ec='none',alpha=.92),zorder=5)
# external spokes
for org in ORG:
    nb=sorted([(b if a==org else a,w) for a,b,w in edges if (a==org)!=(b==org) and not(a in ORGSET and b in ORGSET)],key=lambda t:-t[1])[:4]
    k=len(nb); base=DIR[org]; spread=54
    for i,(n,w) in enumerate(nb):
        ang=math.radians(base-spread+(2*spread*i/(k-1) if k>1 else spread))
        ex=ORG[org][0]+2.0*math.cos(ang); ey=ORG[org][1]+2.0*math.sin(ang)
        ax.plot([ORG[org][0],ex],[ORG[org][1],ey],color='#CBD6E2',lw=1.0,zorder=1)
        c=ROLEC.get(roles.get(n,""),"#888")
        ax.add_patch(Circle((ex,ey),0.13,fc=c,ec='#fff',lw=1.1,zorder=3))
        ha='left' if math.cos(ang)>=0 else 'right'
        dx=0.2 if math.cos(ang)>=0 else -0.2
        ax.text(ex+dx,ey,A("%s·%.1f"%(n,w)),ha=ha,va='center',fontsize=11.5,color='#10243A',zorder=4)
# organ nodes
for o,(x,y) in ORG.items():
    r=0.42 if o=="قلب" else 0.34
    ax.add_patch(Circle((x,y),r,fc='#1D3557',ec='#fff',lw=2.5,zorder=4))
    ax.text(x,y,A(o),ha='center',va='center',fontsize=13.5,color='#fff',fontweight='bold',zorder=5)
leg=[('self / organ','#1D3557'),('cognition','#378ADD'),('action','#0F6E56'),('up-driver','#1D9E75'),
     ('down-driver','#E63946'),('feedback (zād)','#EF9F27'),('orientation','#94A3B8')]
ax.legend(handles=[Line2D([0],[0],marker='o',color='w',markerfacecolor=c,markersize=10,label=l) for l,c in leg],
          loc='lower center',ncol=4,fontsize=11,frameon=False,bbox_to_anchor=(0.5,-0.06))
out=R+"/kawthar_figs/fig_inner_self_organ_core.png"
plt.savefig(out,dpi=150,bbox_inches='tight',facecolor='white'); print("wrote",out)
