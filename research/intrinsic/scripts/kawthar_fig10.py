# -*- coding: utf-8 -*-
"""Figure 10: the divine 'We' (majesty/bounty) vs 'I' (oneness/worship) register."""
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
OUT=f"{R}/research/intrinsic/kawthar_figs"
INK='#10243A'; NAVY='#1D3557'; GREEN='#1D9E75'; GREEN_DK='#0F6E56'
GTINT='#F4F9F7'; BTINT='#EAF2FB'; AMBER='#EF9F27'
plt.rcParams.update({'text.color':INK,'font.family':'DejaVu Sans','svg.fonttype':'none'})

fig,ax=plt.subplots(figsize=(9.4,5.6)); ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,10)
ax.text(5,9.6,"Figure 10.  Why “We gave” (innā) and not “I gave” (innī): two registers",
        ha='center',fontsize=14,color=NAVY,fontweight='bold')

def panel(x,w,head,sub,items,ec,fc,tc):
    p=FancyBboxPatch((x,1.4),w,7.2,boxstyle="round,pad=0.08,rounding_size=0.12",fc=fc,ec=ec,lw=1.8)
    ax.add_patch(p)
    ax.text(x+w/2,8.15,head,ha='center',fontsize=13.5,color=ec,fontweight='bold')
    ax.text(x+w/2,7.6,sub,ha='center',fontsize=12,color=tc,style='italic')
    yy=6.9
    for it in items:
        ax.text(x+0.25,yy,it,ha='left',fontsize=12,color=tc); yy-=0.62

panel(0.3,4.45,"“WE”  ·  innā / naḥnu","majesty — power & bounty  (208×)",
 ["108:1  “WE gave you” the abundance","48:1   “WE opened for you” a victory",
  "15:87  “WE gave you” the seven oft-repeated","94:1   “Did WE not expand your breast?”",
  "97:1   “WE sent it down” on the Night","76:23  “WE sent down to you the Qurʾān”",
  "54:49  “WE created everything in measure”"],NAVY,BTINT,INK)
panel(5.25,4.45,"“I”  ·  innī / innanī","oneness, nearness, worship-Me  (158×)",
 ["20:14  “I am Allah… so worship ME”","21:25  “no god but I, so worship ME”",
  "2:186  “I am near” (to My servants)","16:51  “One God… so be in awe of ME”",
  "51:56  “I created… that they worship ME”","",
  "→ singular goes with tawḥīd & worship"],GREEN_DK,GTINT,INK)

ax.text(5,0.75,"Inside al-Kawthar the two registers sit side by side: the GIFT is from “We” (108:1),"
        "\nbut worship in 108:2 is to “your Lord” (rabb, singular) — never “to Us.”",
        ha='center',fontsize=12,color=INK,fontweight='bold')
fig.savefig(f"{OUT}/fig10_register.png",dpi=150,bbox_inches='tight')
fig.savefig(f"{OUT}/fig10_register.svg",bbox_inches='tight')
print("saved fig10_register")
