# -*- coding: utf-8 -*-
"""COMBINED measured graph = the 3 functional regions laid out together (Apparatus / Drivers / Orientation) as
blobs, so all relations are legible and synthesizable. Within-region edges faint; cross-region BRIDGES gold.
Node size = PPMI strength. MEASURED edges/weights; the grouping into regions is interpretive."""
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import json, re, arabic_reshaper
from bidi.algorithm import get_display
_resh=arabic_reshaper.ArabicReshaper(configuration={'delete_harakat':False,'support_ligatures':False})
_AR=re.compile(r'[؀-ۿ]+(?:\s+[؀-ۿ]+)*')
def A(s): return _AR.sub(lambda m:get_display(_resh.reshape(m.group().replace('ک','ك').replace('ی','ي'))),s) if s else s
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2/research/intrinsic"
GM=json.load(open(R+"/anatomy_figs/inner_self_graph_metrics.json",encoding='utf-8'))
ROLEC={"self":"#1D3557","cog":"#378ADD","act":"#0F6E56","up":"#1D9E75","down":"#E63946","amp":"#EF9F27","bound":"#7A5AA6","dom":"#94A3B8","out_g":"#0F6E56","out_r":"#C1121F","root":"#B5651D"}
pos=GM['pos']; roles=GM['roles']; strg=GM['strength']; st=GM['stats']; regions=GM['regions']; rof=GM['region_of']
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':'#10243A'})
fig,ax=plt.subplots(figsize=(13.5,11)); ax.axis('off'); ax.set_aspect('equal')
xs=[p[0] for p in pos.values()]; ys=[p[1] for p in pos.values()]
ax.set_xlim(min(xs)-1.3,max(xs)+1.3); ax.set_ylim(min(ys)-1.3,max(ys)+1.3)
# region hulls + labels
for key,label,grp in regions:
    px=[pos[n][0] for n in grp]; py=[pos[n][1] for n in grp]
    cx=sum(px)/len(px); cy=sum(py)/len(py)
    rad=max(0.7,max(((pos[n][0]-cx)**2+(pos[n][1]-cy)**2)**0.5 for n in grp)+0.6)
    ax.add_patch(plt.Circle((cx,cy),rad,fc='#EEF3F8',ec='#CFE0F2',lw=1.2,alpha=.6,zorder=0))
    ax.text(cx,cy+rad+0.12,label,ha='center',va='bottom',fontsize=12,fontweight='bold',fontstyle='italic',color='#4E6E92',zorder=6)
wmax=max(w for *_ ,w in GM['edges']) or 1
cross=sorted([(a,b,w) for a,b,w in GM['edges'] if rof.get(a)!=rof.get(b)],key=lambda e:-e[2])[:12]
crosset=set((a,b) for a,b,_ in cross)
# within-region edges: ultra-faint (detail lives in the panels); cross-region: only the strongest dozen, gold
for a,b,w in GM['edges']:
    if a not in pos or b not in pos: continue
    x1,y1=pos[a]; x2,y2=pos[b]
    if rof.get(a)==rof.get(b):
        ax.plot([x1,x2],[y1,y2],'-',color='#D7E0EA',lw=0.4+1.2*(w/wmax),alpha=.35,zorder=1)
    elif (a,b) in crosset:
        ax.plot([x1,x2],[y1,y2],'-',color='#EF9F27',lw=1.0+2.4*(w/wmax),alpha=.85,zorder=2)
for n in pos:
    x,y=pos[n]; c=ROLEC.get(roles[n],'#888')
    ax.scatter([x],[y],s=120+strg[n]*22,c=c,edgecolors='#fff',linewidths=1.5,zorder=3)
    ax.text(x,y+0.14+0.001*strg[n],A(n),ha='center',va='bottom',fontsize=11.5,fontweight='bold',color=c,zorder=4)
ax.set_title("The inner-self graph — three functional regions combined · within-region edges faint · cross-region bridges gold",
             fontsize=14,fontweight='bold',color='#1D3557',pad=12)
sub=("MEASURED (corpus PPMI): %d nodes · %d edges · density %.2f · avg degree %.1f · transitivity %.2f · %d cycles · "
     "%d data-communities (modularity z = +%.1f vs null).  Top hub قلب · top bridge ذکر.  "
     "Regions are interpretive; edges/weights/metrics measured."%(
     st['nodes'],st['edges'],st['density'],st['avg_degree'],st['transitivity'],st['cycles'],st['n_communities'],st['modularity_z']))
ax.text(0.5,-0.03,sub,transform=ax.transAxes,ha='center',fontsize=10.5,color='#10243A')
leg=[('self','#1D3557'),('cognition','#378ADD'),('action','#0F6E56'),('up-driver','#1D9E75'),('down-driver','#E63946'),
     ('feedback','#EF9F27'),('veil/partition','#7A5AA6'),('orientation','#94A3B8'),('kawthar','#0F6E56'),('abtar','#C1121F'),('root','#B5651D')]
h=[Line2D([0],[0],marker='o',color='w',markerfacecolor=c,markersize=9,label=l) for l,c in leg]
h.append(Line2D([0],[0],color='#EF9F27',lw=2.5,label='cross-region bridge'))
ax.legend(handles=h,loc='lower center',bbox_to_anchor=(0.5,-0.1),ncol=6,frameon=False,fontsize=10)
out=R+"/kawthar_figs/fig_inner_self_graph.png"
plt.savefig(out,dpi=150,bbox_inches='tight',facecolor='white'); print("wrote",out)
