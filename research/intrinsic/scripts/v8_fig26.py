# -*- coding: utf-8 -*-
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import re as _re, arabic_reshaper
from bidi.algorithm import get_display
OUT="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2/research/intrinsic/kawthar_figs"
_resh=arabic_reshaper.ArabicReshaper(configuration={'delete_harakat':False,'support_ligatures':False})
_AR=_re.compile(r'[؀-ۿݐ-ݿ]+')
def A(s): return _AR.sub(lambda m:get_display(_resh.reshape(m.group().replace('ک','ك').replace('ی','ي'))),s)
INK='#10243A';NAVY='#1D3557';GREEN_DK='#0F6E56';RED='#E63946';AMBER='#EF9F27';BLUE='#378ADD';BORDEM='#C9D6E8';GTINT='#F4F9F7';BTINT='#EAF2FB';GREY='#9fb0c4'
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':INK,'font.size':13})
fig,ax=plt.subplots(figsize=(13.4,6.4)); ax.axis('off'); ax.set_xlim(0,16); ax.set_ylim(0,11)
ax.text(0.2,10.5,"Divine future-promises to the Prophet — which are declared fulfilled (perfect, matching verb)?",fontsize=13.2,fontweight='bold',color=NAVY)
ax.text(2.6,9.6,"PROMISE  (future)",ha='center',fontsize=12.5,fontweight='bold',color=BLUE)
ax.text(11.0,9.6,"FULFILMENT  (perfect)",ha='center',fontsize=12.5,fontweight='bold',color=GREEN_DK)
rows=[("عطو","give","وَلَسَوْفَ یُعْطِیكَ","۹۳:۵","أَعْطَیْنَاكَ الْكَوْثَرَ","۱۰۸:۱",True,True),
      ("کفی","suffice","فَسَیَكْفِیكَهُمُ اللهُ","۲:۱۳۷","كَفَیْنَاكَ الْمُسْتَهْزِئِینَ","۱۵:۹۵",True,False),
      ("قرأ","recite","سَنُقْرِئُكَ","۸۷:۶","— (هیچ ماضیِ متناظر)","",False,False),
      ("لقی","cast word","سَنُلْقِی عَلَیْكَ قَوْلًا","۷۳:۵","— (هیچ ماضیِ متناظر)","",False,False)]
y=8.4
for rt,gl,prom,pref,fulf,fref,discharged,star in rows:
    fc = '#FBEAEC' if star else (GTINT if discharged else '#F4F6F9')
    # promise box
    ax.add_patch(FancyBboxPatch((0.3,y-0.7),5.0,1.5,boxstyle='round,pad=0.08,rounding_size=0.18',fc=BTINT,ec='#CFE0F2',lw=1.4))
    ax.text(2.8,y+0.32,A(prom),ha='center',fontsize=15.5,color=NAVY,fontweight='bold')
    ax.text(2.8,y-0.42,A(pref),ha='center',fontsize=12,color=BLUE)
    # verb chip
    ax.text(6.05,y,A("%s"%rt),ha='center',va='center',fontsize=15,color=(RED if star else INK),fontweight='bold')
    ax.text(6.05,y-0.62,gl,ha='center',va='center',fontsize=10.5,color=INK)
    # arrow
    col = GREEN_DK if discharged else GREY
    ax.add_patch(FancyArrowPatch((7.0,y),(8.8,y),arrowstyle='-|>',mutation_scale=22,lw=2.4,color=col,
                 linestyle='-' if discharged else (0,(4,3)),zorder=4))
    ax.text(7.9,y+0.45,("کِشت" if False else ("discharged" if discharged else "open")),ha='center',fontsize=10.5,color=col,fontweight='bold')
    # fulfilment box
    ax.add_patch(FancyBboxPatch((9.0,y-0.7),6.7,1.5,boxstyle='round,pad=0.08,rounding_size=0.18',fc=fc,
                 ec=('#f3c9ce' if star else ('#cfe4dc' if discharged else BORDEM)),lw=1.4))
    ax.text(12.35,y+0.32,A(fulf),ha='center',fontsize=14.5 if discharged else 12,color=(NAVY if discharged else GREY),fontweight='bold')
    if fref: ax.text(12.35,y-0.42,A(fref),ha='center',fontsize=12,color=GREEN_DK)
    y-=2.05
ax.text(0.2,0.35,A("الگو: عطیه و کفایت «انجام‌یافته» (ماضی) اعلام می‌شوند؛ وعده‌های وحی (قرأ، لقی) هرگز در ماضیِ متناظر بسته نمی‌شوند — وحی پایان‌ناپذیر است.   ★ الكوثر = یکی از دو «وعدهٔ برآورده»."),
        fontsize=11.8,color=INK,bbox=dict(boxstyle='round,pad=0.4',fc=GTINT,ec='#cfe4dc'))
fig.savefig(f"{OUT}/fig_promise.png",dpi=150,bbox_inches='tight'); plt.close(fig); print("saved fig_promise (F26)")
