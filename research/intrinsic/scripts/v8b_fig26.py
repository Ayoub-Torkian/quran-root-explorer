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
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':INK,'font.size':12.5})
fig,ax=plt.subplots(figsize=(14.2,8.2)); ax.axis('off'); ax.set_xlim(0,17); ax.set_ylim(0,15.6)
ax.text(0.2,15.0,"The complete ledger of God's prospective promises to the Prophet — and how each is grammatically closed",fontsize=13.2,fontweight='bold',color=NAVY)
ax.text(3.0,14.1,"PROMISE  (prospective)",ha='center',fontsize=12,fontweight='bold',color=BLUE)
ax.text(12.0,14.1,"FULFILMENT",ha='center',fontsize=12,fontweight='bold',color=GREEN_DK)
# rows: (promise, pref, root, gloss, fulfil, fref, discharged, star_ridha, note)
rows=[
 ("یُعْطِیكَ رَبُّكَ فَتَرْضَىٰ","۹۳:۵","عطو","gift","أَعْطَیْنَاكَ الْكَوْثَرَ","۱۰۸:۱",True,True,"★ ال‌كوثر"),
 ("فَسَیَكْفِیكَهُمُ اللهُ","۲:۱۳۷","کفی","protection","كَفَیْنَاكَ الْمُسْتَهْزِئِینَ","۱۵:۹۵",True,False,""),
 ("لَنُوَلِّیَنَّكَ قِبْلَةً تَرْضَاهَا","۲:۱۴۴","ولی","qibla","فَوَلِّ وَجْهَكَ (همان آیه)","۲:۱۴۴",True,True,""),
 ("عَسَىٰ أَن یَبْعَثَكَ … مَقَامًا مَّحْمُودًا","۱۷:۷۹","بعث","praised station","— (آخرت: روزِ قیامت)","",False,False,""),
 ("سَنُقْرِئُكَ فَلَا تَنسَىٰ","۸۷:۶","قرأ","recite","— (وحیِ جاری)","",False,False,""),
 ("سَنُلْقِی عَلَیْكَ قَوْلًا ثَقِیلًا","۷۳:۵","لقی","the weighty word","— (وحیِ جاری)","",False,False,""),
]
# group bands
ax.add_patch(FancyBboxPatch((0.15,8.5),16.7,5.1,boxstyle='round,pad=0.05,rounding_size=0.1',fc='#F3F9F6',ec='#cfe4dc',lw=1.2,zorder=0))
ax.text(0.35,13.35,A("سامانهٔ «انجام‌یافته» — عطایای دنیویِ مهرشده در ماضی"),fontsize=11.5,color=GREEN_DK,fontweight='bold')
ax.add_patch(FancyBboxPatch((0.15,1.0),16.7,6.6,boxstyle='round,pad=0.05,rounding_size=0.1',fc='#F6F7FA',ec=BORDEM,lw=1.2,zorder=0))
ax.text(0.35,7.35,A("سامانهٔ «گشوده» — وحی و آخرت، که طبعاً در ماضی بسته نمی‌شوند"),fontsize=11.5,color=GREY,fontweight='bold')
y=12.3
for prom,pref,rt,gl,fulf,fref,disch,star,note in rows:
    fc='#FBEAEC' if star and rt=='عطو' else (GTINT if disch else '#FAFBFD')
    ax.add_patch(FancyBboxPatch((0.4,y-0.78),6.0,1.55,boxstyle='round,pad=0.06,rounding_size=0.14',fc=BTINT,ec='#CFE0F2',lw=1.2))
    ax.text(3.4,y+0.28,A(prom),ha='center',fontsize=13.5,color=NAVY,fontweight='bold')
    ax.text(3.4,y-0.42,A(pref)+("   ★ ترضیٰ" if star else ""),ha='center',fontsize=11,color=(RED if star else BLUE))
    ax.text(6.95,y,A(rt),ha='center',va='center',fontsize=14,color=(RED if rt=='عطو' else INK),fontweight='bold')
    ax.text(6.95,y-0.6,gl,ha='center',va='center',fontsize=9.5,color=INK)
    col=GREEN_DK if disch else GREY
    ax.add_patch(FancyArrowPatch((7.8,y),(9.4,y),arrowstyle='-|>',mutation_scale=20,lw=2.3,color=col,
                 linestyle='-' if disch else (0,(4,3)),zorder=4))
    ax.text(8.6,y+0.4,("discharged" if disch else "open"),ha='center',fontsize=9.5,color=col,fontweight='bold')
    ax.add_patch(FancyBboxPatch((9.6,y-0.78),6.9,1.55,boxstyle='round,pad=0.06,rounding_size=0.14',fc=fc,
                 ec=('#f3c9ce' if (star and rt=='عطو') else ('#cfe4dc' if disch else BORDEM)),lw=1.2))
    ax.text(13.05,y+0.28,A(fulf),ha='center',fontsize=13 if disch else 11.5,color=(NAVY if disch else GREY),fontweight='bold')
    if fref: ax.text(13.05,y-0.42,A(fref),ha='center',fontsize=11,color=GREEN_DK)
    y-=1.93
ax.text(0.2,0.4,A("نکته: «رِضیٰ» (ترضیٰ/ترضاها) تنها دو وعده را نشان می‌کند — عطیه (۹۳:۵) و قبله (۲:۱۴۴): دو وعدهٔ «خشنودیِ پیامبر». ★ الكوثر یکی از سه عطای دنیویِ مهرشده است."),
        fontsize=11.3,color=INK,bbox=dict(boxstyle='round,pad=0.4',fc=GTINT,ec='#cfe4dc'))
fig.savefig(f"{OUT}/fig_promise.png",dpi=150,bbox_inches='tight'); plt.close(fig); print("saved fig_promise (F26 v2, 6-row ledger)")
