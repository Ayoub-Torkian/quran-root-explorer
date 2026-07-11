# -*- coding: utf-8 -*-
"""Anatomy of the inner self: nafs ⊃ ṣadr ⊃ qalb (containment 22:46), qalb=the turner (انقلب), fuʾād=perception.
All relations MEASURED on Book6. Locked UI: >=12px, ink, palette, Arabic reshaped."""
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse, Circle, Wedge, FancyArrowPatch
import re, arabic_reshaper
from bidi.algorithm import get_display
_resh=arabic_reshaper.ArabicReshaper(configuration={'delete_harakat':False,'support_ligatures':False})
_AR=re.compile(r'[؀-ۿ]+(?:\s+[؀-ۿ]+)*')
def A(s):
    return _AR.sub(lambda m:get_display(_resh.reshape(m.group().replace('ک','ك').replace('ی','ي'))),s) if s else s
INK='#10243A';NAVY='#1D3557';GREEN='#1D9E75';GREEN_DK='#0F6E56';RED='#E63946';AMBER='#EF9F27';BLUE='#378ADD';PURP='#7A5AA6';TEAL='#2A7D8C';BORD='#E2E8F1';GTINT='#F4F9F7';BTINT='#EAF2FB';RTINT='#FBEAEC'
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':INK})
fig,ax=plt.subplots(figsize=(15,9.2)); ax.set_xlim(0,15); ax.set_ylim(0,9.2); ax.axis('off')
ax.text(0.3,8.9,"Anatomy of the inner self — a differentiated system, not heart-synonyms",fontsize=18,fontweight='bold',color=NAVY)
ax.text(0.3,8.5,A("النفس")+"  ⊃  "+A("الصدر")+"  ⊃  "+A("القلب")+"   ·   "+A("الفؤاد")+" = perception   ·   all relations MEASURED on the rasm",fontsize=13,color=INK)
# nafs outer
ax.add_patch(FancyBboxPatch((0.4,0.7),9.2,7.2,boxstyle='round,pad=0.1,rounding_size=0.3',fc=GTINT,ec=NAVY,lw=2.2))
ax.text(0.8,7.5,"NAFS · "+A("النفس")+" — the fashioned moral self",fontsize=14,color=NAVY,fontweight='bold')
ax.text(0.8,7.05,A("و نفس و ما سواها · فألهمها فجورها وتقواها")+"  (91:7-8): capacity for fujūr & taqwā",fontsize=12.5,color=INK)
# sadr chamber (ellipse) contains qalb
ax.add_patch(Ellipse((4.0,3.9),6.4,5.2,fc=BTINT,ec=BLUE,lw=2))
ax.text(4.0,6.05,"ṢADR · "+A("الصدر")+" — the breast / chamber (the space)",ha='center',fontsize=13.5,color=BLUE,fontweight='bold')
ax.text(1.05,5.4,"constricted\n"+A("ضیق · حرج")+"\n(صدر only, 0× qalb)",ha='center',fontsize=12,color=RED,fontweight='bold')
ax.text(7.0,5.4,"expanded\n"+A("شرح")+"\n(صدر 5×)",ha='center',fontsize=12,color=GREEN_DK,fontweight='bold')
ax.add_patch(FancyArrowPatch((1.9,5.3),(6.1,5.3),arrowstyle='<|-|>',mutation_scale=16,lw=1.6,color=INK,alpha=.5))
ax.text(4.0,2.0,A("القلوب التی فی الصدور")+" (22:46): the heart is IN the breast",ha='center',fontsize=12.5,color=BLUE,fontstyle='italic')
# qalb seat (circle) with closed/open halves
cx,cy,r=4.0,4.0,1.55
ax.add_patch(Wedge((cx,cy),r,90,270,fc=RTINT,ec=RED,lw=1.6))   # left = closed
ax.add_patch(Wedge((cx,cy),r,270,450,fc=GTINT,ec=GREEN_DK,lw=1.6))# right = open
ax.text(cx,cy+0.15,"QALB · "+A("القلب"),ha='center',fontsize=13,color=NAVY,fontweight='bold')
ax.text(cx,cy-0.35,"the seat — & the turner",ha='center',fontsize=11.5,color=INK)
ax.text(cx-0.95,cy-1.15,"CLOSED",ha='center',fontsize=11.5,color=RED,fontweight='bold')
ax.text(cx+0.95,cy-1.15,"OPEN",ha='center',fontsize=11.5,color=GREEN_DK,fontweight='bold')
ax.text(cx-1.85,cy+0.3,A("طبع·ختم")+" sealed\n"+A("مرض")+" diseased\n"+A("قسو")+" hardened\n"+A("رین")+" rusted",ha='right',fontsize=11.5,color=RED)
ax.text(cx+1.85,cy+0.3,"humbled "+A("خشع")+"\nsoftened "+A("لین")+"\ntranquil "+A("طمن")+"\nsound "+A("سلیم"),ha='left',fontsize=11.5,color=GREEN_DK)
# turning arrow around qalb
ax.add_patch(FancyArrowPatch((cx-0.5,cy+1.75),(cx+0.5,cy+1.75),connectionstyle="arc3,rad=-0.9",arrowstyle='-|>',mutation_scale=15,lw=2,color=AMBER))
ax.text(cx,cy+2.05,A("انقلب · تقلّب")+" — turns between states (35 tokens)",ha='center',fontsize=11.5,color=AMBER,fontweight='bold')
ax.text(cx,cy-1.95,"belief "+A("آمن")+" 49 · disbelief "+A("کفر")+" 21 attach here",ha='center',fontsize=11.5,color=NAVY)
# fuʾād perception cluster (right panel)
ax.add_patch(FancyBboxPatch((10.1,2.3),4.5,4.6,boxstyle='round,pad=0.1,rounding_size=0.3',fc='#F3F0F8',ec=PURP,lw=2))
ax.text(12.35,6.5,"FUʾĀD · "+A("الفؤاد"),ha='center',fontsize=14,color=PURP,fontweight='bold')
ax.text(12.35,6.05,"the perceiving / witnessing heart",ha='center',fontsize=12,color=INK)
ax.add_patch(Circle((11.2,4.9),0.45,fc='#fff',ec=BLUE,lw=1.6)); ax.text(11.2,4.9,A("السمع"),ha='center',va='center',fontsize=11.5,color=BLUE)
ax.add_patch(Circle((13.5,4.9),0.45,fc='#fff',ec=BLUE,lw=1.6)); ax.text(13.5,4.9,A("البصر"),ha='center',va='center',fontsize=11.5,color=BLUE)
ax.add_patch(Circle((12.35,3.6),0.5,fc='#fff',ec=PURP,lw=1.8)); ax.text(12.35,3.6,A("فؤاد"),ha='center',va='center',fontsize=12,color=PURP,fontweight='bold')
ax.add_patch(FancyArrowPatch((11.4,4.55),(12.1,3.9),arrowstyle='-|>',mutation_scale=11,lw=1.5,color=BLUE))
ax.add_patch(FancyArrowPatch((13.3,4.55),(12.6,3.9),arrowstyle='-|>',mutation_scale=11,lw=1.5,color=BLUE))
ax.text(12.35,2.75,"bound to sight: OR 8.8, p<0.001\nthe triad "+A("سمع·بصر·فؤاد")+" (6 verses)\n«did not lie about what it saw» 53:11\naccountable 17:36",ha='center',fontsize=11.5,color=INK)
# fuad != qalb divider note
ax.text(9.85,1.05,"fuʾād ≠ qalb : perception (eye/ear) vs belief/morality — never interchanged",fontsize=12.5,color=PURP,fontweight='bold')
fig.savefig('anatomy_figs/inner_self_map.png',dpi=140,bbox_inches='tight'); print("saved anatomy_figs/inner_self_map.png")
