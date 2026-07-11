# -*- coding: utf-8 -*-
"""F25 — the grammar of the gift: (A) al-Duha future-promise -> al-Kawthar perfect-fulfilment on the
shared root عطو; (B) the three-verse mood ladder (perfect -> imperative -> equational) = agency ladder."""
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import re as _re, arabic_reshaper
from bidi.algorithm import get_display
OUT="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2/research/intrinsic/kawthar_figs"
_resh=arabic_reshaper.ArabicReshaper(configuration={'delete_harakat':False,'support_ligatures':False})
_AR=_re.compile(r'[؀-ۿݐ-ݿ]+')
def A(s): return _AR.sub(lambda m:get_display(_resh.reshape(m.group().replace('ک','ك').replace('ی','ي'))),s)
INK='#10243A';NAVY='#1D3557';GREEN='#1D9E75';GREEN_DK='#0F6E56';RED='#E63946';AMBER='#EF9F27';BLUE='#378ADD';BORDEM='#C9D6E8';GTINT='#F4F9F7';BTINT='#EAF2FB'
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':INK,'font.size':13})
fig,(axA,axB)=plt.subplots(1,2,figsize=(13.8,5.8),gridspec_kw={'width_ratios':[1,1.05]})

# ---- Panel A: promise -> fulfilment (same root عطو) ----
axA.axis('off'); axA.set_xlim(0,10); axA.set_ylim(0,11)
def box(ax,x,y,w,h,fc,ec):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.12,rounding_size=0.25',fc=fc,ec=ec,lw=1.6,zorder=2))
box(axA,0.4,5.6,9.2,3.2,BTINT,'#CFE0F2')
axA.text(5.0,8.25,A("الضحیٰ ۹۳:۵"),ha='center',fontsize=14,color=BLUE,fontweight='bold')
axA.text(5.0,7.25,A("وَلَسَوْفَ یُعْطِیكَ رَبُّكَ"),ha='center',fontsize=20,color=NAVY,fontweight='bold')
axA.text(5.0,6.25,"FUTURE — a promise ('your Lord shall give you')",ha='center',fontsize=12.5,color=INK)
box(axA,0.4,1.0,9.2,3.2,GTINT,'#cfe4dc')
axA.text(5.0,3.65,A("الكوثر ۱۰۸:۱"),ha='center',fontsize=14,color=GREEN_DK,fontweight='bold')
axA.text(5.0,2.65,A("إِنَّا أَعْطَیْنَاكَ الْكَوْثَرَ"),ha='center',fontsize=20,color=NAVY,fontweight='bold')
axA.text(5.0,1.65,"PERFECT — fulfilled ('We have given you')",ha='center',fontsize=12.5,color=INK)
axA.add_patch(FancyArrowPatch((5.0,5.5),(5.0,4.3),arrowstyle='-|>',mutation_scale=26,lw=2.6,color=RED,zorder=4))
axA.text(6.35,4.9,A("همان ریشهٔ عطو\nوعده ← انجام"),ha='left',va='center',fontsize=12.5,color=RED,fontweight='bold')
axA.set_title(A("A · promise → fulfilment: same root عطو, future → perfect"),loc='left',fontsize=12.6,fontweight='bold',color=NAVY,pad=12)

# ---- Panel B: mood ladder = agency ladder ----
axB.axis('off'); axB.set_xlim(0,10); axB.set_ylim(0,11)
rows=[(8.0,"إِنَّا أَعْطَیْنَاكَ","آیهٔ ۱ · ماضٍ (perfect)","God acts — done",GREEN_DK,GTINT,'#cfe4dc'),
      (5.0,"فَصَلِّ لِرَبِّكَ وَانْحَرْ","آیهٔ ۲ · أمر (imperative)","the Prophet is commanded",BLUE,BTINT,'#CFE0F2'),
      (2.0,"إِنَّ شَانِئَكَ هُوَ الْأَبْتَرُ","آیهٔ ۳ · جملة اسمیّة (equational)","a settled verdict — a state",RED,'#FBEAEC','#f3c9ce')]
for y,ar,mood,gloss,col,fc,ec in rows:
    axB.add_patch(FancyBboxPatch((0.5,y-1.05),9.0,2.0,boxstyle='round,pad=0.1,rounding_size=0.2',fc=fc,ec=ec,lw=1.5,zorder=2))
    axB.text(9.2,y+0.45,A(ar),ha='right',fontsize=18,color=NAVY,fontweight='bold')
    axB.text(0.8,y+0.45,A(mood),ha='left',fontsize=12.5,color=col,fontweight='bold')
    axB.text(0.8,y-0.55,gloss,ha='left',fontsize=12,color=INK)
for y0 in (6.95,3.95):
    axB.add_patch(FancyArrowPatch((5.0,y0),(5.0,y0-0.95),arrowstyle='-|>',mutation_scale=20,lw=2.2,color=INK,zorder=4))
# highlight damir al-fasl
axB.text(5.0,0.35,A("ضمیرِ فصل «هو» + «الأبتر» معرفه ← حصرِ بریدگی بر دشمن"),ha='center',fontsize=12.5,color=RED,fontweight='bold')
axB.set_title(A("B · mood ladder = agency ladder"),loc='left',fontsize=12.6,fontweight='bold',color=NAVY,pad=12)
fig.tight_layout(); fig.savefig(f"{OUT}/fig_grammar.png",dpi=150,bbox_inches='tight'); plt.close(fig)
print("saved fig_grammar (F25)")
