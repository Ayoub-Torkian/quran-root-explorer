# -*- coding: utf-8 -*-
"""Validated integrated model of the inner self, on the unifying kawthar↔abtar axis. Locked UI."""
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import re, arabic_reshaper
from bidi.algorithm import get_display
_resh=arabic_reshaper.ArabicReshaper(configuration={'delete_harakat':False,'support_ligatures':False})
_AR=re.compile(r'[؀-ۿ]+(?:\s+[؀-ۿ]+)*')
def A(s): return _AR.sub(lambda m:get_display(_resh.reshape(m.group().replace('ک','ك').replace('ی','ي'))),s) if s else s
INK='#10243A';NAVY='#1D3557';GREEN='#1D9E75';GREEN_DK='#0F6E56';RED='#E63946';AMBER='#EF9F27';BLUE='#378ADD';PURP='#7A5AA6';TEAL='#2A7D8C';BORD='#E2E8F1';GTINT='#F4F9F7';BTINT='#EAF2FB';RTINT='#FBEAEC'
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':INK})
fig,ax=plt.subplots(figsize=(15.5,9.4)); ax.set_xlim(0,15.5); ax.set_ylim(0,9.4); ax.axis('off')
ax.text(0.3,9.05,"The inner self — a validated, bistable model on the kawthar↔abtar axis",fontsize=17,fontweight='bold',color=NAVY)
ax.text(0.3,8.62,"MEASURED: co-occurrences + Fisher tests.  INFERRED (tagged): the OS / processor / control-system framing.",fontsize=12,color=INK)
# poles backdrop
ax.add_patch(FancyBboxPatch((0.5,1.7),7.0,6.4,boxstyle='round,pad=0.05',fc=RTINT,ec=RED,lw=1.4,alpha=0.5))
ax.add_patch(FancyBboxPatch((8.0,1.7),7.0,6.4,boxstyle='round,pad=0.05',fc=GTINT,ec=GREEN_DK,lw=1.4,alpha=0.5))
ax.text(2.0,7.7,A("الأبتر")+" · ABTAR — severed / sealed",fontsize=14,color=RED,fontweight='bold')
ax.text(13.0,7.7,"KAWTHAR · "+A("الکوثر")+" — open / increasing",ha='right',fontsize=14,color=GREEN_DK,fontweight='bold')
# lanes
def lane(y,label,ar,left,right,col):
    ax.text(0.7,y+0.28,label,fontsize=12.5,color=col,fontweight='bold'); ax.text(0.7,y-0.12,A(ar),fontsize=12,color=col)
    ax.text(3.9,y+0.07,left,ha='center',fontsize=11.5,color=RED); ax.text(11.6,y+0.07,right,ha='center',fontsize=11.5,color=GREEN_DK)
    ax.add_patch(FancyArrowPatch((5.6,y),(9.9,y),arrowstyle='-|>',mutation_scale=12,lw=1.4,color=INK,alpha=.35))
lane(6.6,"NAFS (agent)","النفس",A("أمّارة")+" commands · "+A("مسوّلة")+" entices",A("مطمئنة")+" serene",PURP)
ax.text(7.75,6.67,A("لوّامة")+"\nself-reproach\n(PIVOT)",ha='center',fontsize=10.8,color=AMBER,fontweight='bold')
lane(5.2,"QALB (processor)","القلب",A("طبع")+" sealed · "+A("لا یفقهون")+" offline",A("شرح")+" open · understands",BLUE)
lane(3.9,"ṢADR (chamber)","الصدر",A("ضیق · حرج")+" constricted",A("شرح")+" expanded",TEAL)
ax.text(0.7,2.75,"FUʾĀD (sensors) · "+A("الفؤاد"),fontsize=12.5,color=GREEN_DK,fontweight='bold')
ax.text(4.0,2.4,"perception with "+A("سمع · بصر")+" (eye & ear) — bound to sight OR 8.8, p<0.001 — accountable 17:36",fontsize=11.5,color=INK)
# forcing inputs (below axis)
ax.add_patch(FancyArrowPatch((3.4,1.3),(1.6,1.3),arrowstyle='-|>',mutation_scale=14,lw=2,color=RED))
ax.text(3.6,1.22,A("سوّل")+" entice (nafs & Satan, 47:25) — pushes to severance",ha='left',fontsize=11.5,color=RED,fontweight='bold')
ax.add_patch(FancyArrowPatch((12.0,0.75),(13.9,0.75),arrowstyle='-|>',mutation_scale=14,lw=2,color=GREEN_DK))
ax.text(11.8,0.67,A("ذکر")+" remembrance / revelation (input) → trembles, humbles, tranquil",ha='right',fontsize=11.5,color=GREEN_DK,fontweight='bold')
# feedback loops (zaid) on each pole
ax.add_patch(FancyArrowPatch((1.4,5.0),(1.4,6.0),connectionstyle="arc3,rad=-1.1",arrowstyle='-|>',mutation_scale=13,lw=2,color=RED))
ax.text(1.5,5.5,A("زاد")+"\ndisease↑disease\nOR 16, p<.01",ha='left',fontsize=10.5,color=RED,fontweight='bold')
ax.add_patch(FancyArrowPatch((14.1,5.0),(14.1,6.0),connectionstyle="arc3,rad=1.1",arrowstyle='-|>',mutation_scale=13,lw=2,color=GREEN_DK))
ax.text(13.9,5.5,A("زاد")+"\nfaith↑faith\nOR 2.6, p<.01",ha='right',fontsize=10.5,color=GREEN_DK,fontweight='bold')
# nesting note
ax.text(7.75,8.15,"nesting: "+A("النفس")+" (agent) ⊃ "+A("الصدر")+" (chamber, 22:46 "+A("القلوب التی فی الصدور")+") ⊃ "+A("القلب")+" (processor) · "+A("الفؤاد")+" (sensors)",ha='center',fontsize=11.5,color=NAVY)
fig.savefig('anatomy_figs/inner_self_model.png',dpi=140,bbox_inches='tight'); print("saved anatomy_figs/inner_self_model.png")
