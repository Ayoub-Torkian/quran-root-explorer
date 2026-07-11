# -*- coding: utf-8 -*-
"""#2 Navigable chronology MAP: (A) multi-temporal suras along the AH timeline (chunk dates, cross-referenced);
(B) gradation clocks. Locked UI: >=12px, ink, navy, green, tints; no grey text."""
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np, re, arabic_reshaper
from bidi.algorithm import get_display
OUT="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2/research/intrinsic/chrono_figs"
_resh=arabic_reshaper.ArabicReshaper(configuration={'delete_harakat':False,'support_ligatures':False})
_AR=re.compile(r'[؀-ۿݐ-ݿ]+')
def A(s): return _AR.sub(lambda m:get_display(_resh.reshape(m.group().replace('ک','ك').replace('ی','ي'))),s)
INK='#10243A';NAVY='#1D3557';GREEN='#1D9E75';GREEN_DK='#0F6E56';RED='#E63946';AMBER='#EF9F27';BLUE='#378ADD';BORD='#E2E8F1';GTINT='#F4F9F7';BTINT='#EAF2FB'
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':INK})
fig=plt.figure(figsize=(13.4,8.8))
gs=fig.add_gridspec(2,1,height_ratios=[1.15,1],hspace=0.34)
axA=fig.add_subplot(gs[0]); axB=fig.add_subplot(gs[1])

# ---- Panel A: multi-temporal suras on Hijra timeline (chunk dates) ----
# (sura, [(label, ayah-range, AH, color)])
ROWS=[
 ("Baqara (2)",[("Qibla 2:142-150",2.0,GREEN_DK),("Ḥajj/ʿUmra 2:196-203",6.0,BLUE)]),
 ("Āl ʿImrān (3)",[("Uhud 3:121-175",3.0,AMBER),("Najrān/Mubāhala 3:33-63",9.5,RED)]),
 ("Aḥzāb (33)",[("Khandaq 33:9-27",5.0,BLUE)]),
 ("Ḥashr (59)",[("Banū Naḍīr 59:1-14",4.0,BLUE)]),
 ("Anfāl (8)",[("Badr 8:41-44",2.0,GREEN_DK)]),
 ("Fatḥ (48)",[("Ḥudaybiyya 48:1-29",6.0,BLUE)]),
 ("Naṣr (110)",[("Conquest 110:1-3",8.0,RED)]),
 ("Tawba (9)",[("Muhājirūn/Anṣār 9:100",1.0,GREEN_DK),("Tabūk/Ḍirār 9:38-110",9.0,RED)]),
]
axA.set_xlim(0,11); axA.set_ylim(-0.6,len(ROWS)+0.2)
for x in range(1,11): axA.axvline(x,color=BORD,lw=0.8,zorder=0)
for i,(name,chunks) in enumerate(ROWS):
    y=len(ROWS)-1-i
    axA.text(-0.15,y,name,ha='right',va='center',fontsize=13,color=NAVY,fontweight='bold')
    xs=[ah for _,ah,_ in chunks]
    if len(xs)>1: axA.plot([min(xs),max(xs)],[y,y],color=BORD,lw=2,zorder=1)
    for lab,ah,col in chunks:
        axA.scatter([ah],[y],s=150,color=col,zorder=3,edgecolors='white',linewidths=1.4)
        axA.text(ah,y+0.26,lab,ha='center',va='bottom',fontsize=10.5,color=col,fontweight='bold',rotation=0)
# highlight the multi-temporal spreads
for name,yy in [("Baqara",7),("Āl ʿImrān",6),("Tawba",0)]:
    pass
axA.text(2.6,len(ROWS)-1+0.0,"",fontsize=11)
axA.set_xticks(range(1,11)); axA.set_xticklabels([f"{n}" for n in range(1,11)],fontsize=12,color=INK)
axA.set_yticks([]); 
for s in ['top','right','left']: axA.spines[s].set_visible(False)
axA.spines['bottom'].set_color(BORD)
axA.set_xlabel("Hijri year (AH) — chunk dates from cross-referenced event anchors [REPORT]",fontsize=12.5,color=INK)
axA.set_title("Chronology map: long sūras are multi-temporal — chunks dated by anchor cross-reference",loc='left',fontsize=17,fontweight='bold',color=NAVY,pad=14)
axA.text(0,-0.5,"Āl ʿImrān spans 3→10 AH · Baqara 2→6 AH · Tawba Hijra→9 AH — one nuzūl number cannot hold them",fontsize=11.5,color=GREEN_DK,fontweight='bold')

# ---- Panel B: gradation clocks ----
eras=['EARLY','MID','LATE']; x=[0,1,2]
warn=[100,75,53]; hell=[57,43,44]; christ=[0,0,100]; jews=[0,33,67]
axB.plot(x,warn,'-o',color=AMBER,lw=2.6,markersize=8,label=A("nadhīr→bashīr warning-share %"))
axB.plot(x,hell,'-o',color=RED,lw=2.6,markersize=8,label="hell-share % (vs paradise)")
axB.plot(x,christ,'-o',color=BLUE,lw=2.6,markersize=8,label="Christians (نصاری) share of PoB %")
for xi,w,h,c in zip(x,warn,hell,christ):
    axB.text(xi,w+3,f"{w}%",ha='center',fontsize=11,color=AMBER,fontweight='bold')
    axB.text(xi,h-7,f"{h}%",ha='center',fontsize=11,color=RED,fontweight='bold')
axB.set_xticks(x); axB.set_xticklabels(eras,fontsize=12.5,color=INK,fontweight='bold')
axB.set_ylim(-8,112); axB.set_yticks([0,25,50,75,100]); axB.tick_params(labelsize=11,colors=INK)
for s in ['top','right']: axB.spines[s].set_visible(False)
for s in ['left','bottom']: axB.spines[s].set_color(BORD)
axB.legend(fontsize=11.5,loc='center right',frameon=False)
axB.set_title("Gradation clocks (validated, resolution-adding): warning→glad-tidings, terror→paradise, Christians late",loc='left',fontsize=14,fontweight='bold',color=NAVY,pad=10)
axB.set_xlabel("revealed time (early → mid → late Meccan / Medinan)",fontsize=12.5,color=INK)
fig.savefig(f"{OUT}/chronology_map.png",dpi=150,bbox_inches='tight'); print("saved",f"{OUT}/chronology_map.png")
