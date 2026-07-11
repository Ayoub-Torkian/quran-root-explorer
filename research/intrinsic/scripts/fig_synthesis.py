# -*- coding: utf-8 -*-
"""How it all fits: al-Kawthar as the seed of one self-interpreting-web program. Locked UI."""
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import re, arabic_reshaper
from bidi.algorithm import get_display
_resh=arabic_reshaper.ArabicReshaper(configuration={'delete_harakat':False,'support_ligatures':False})
_AR=re.compile(r'[؀-ۿ]+(?:\s+[؀-ۿ]+)*')
def A(s): return _AR.sub(lambda m:get_display(_resh.reshape(m.group().replace('ک','ك').replace('ی','ي'))),s) if s else s
INK='#10243A';NAVY='#1D3557';GREEN='#1D9E75';GREEN_DK='#0F6E56';RED='#E63946';AMBER='#EF9F27';BLUE='#378ADD';PURP='#7A5AA6';TEAL='#2A7D8C';BORD='#E2E8F1';GTINT='#F4F9F7';BTINT='#EAF2FB'
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':INK})
fig,ax=plt.subplots(figsize=(14.5,9)); ax.set_xlim(0,14.5); ax.set_ylim(0,9); ax.axis('off')
def box(x,y,w,h,fc,ec,lw=2): ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.08,rounding_size=0.18',fc=fc,ec=ec,lw=lw,zorder=2))
def arr(p,q,c=INK): ax.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=16,lw=2,color=c,zorder=1))
ax.text(7.25,8.65,"How it all fits — al-Kawthar as the seed of one self-interpreting-web program",ha='center',fontsize=17,fontweight='bold',color=NAVY)
# 1. al-Kawthar seed
box(5.4,7.2,3.7,1.0,GTINT,GREEN_DK,2.4); ax.text(7.25,7.85,"SŪRAT AL-KAWTHAR · "+A("الکوثر"),ha='center',fontsize=14,color=GREEN_DK,fontweight='bold')
ax.text(7.25,7.42,"the validated exemplar (the keyhole)",ha='center',fontsize=12,color=INK)
# 2. method
box(4.3,5.85,5.9,0.95,BTINT,NAVY); ax.text(7.25,6.48,"THE METHOD",ha='center',fontsize=13,color=NAVY,fontweight='bold')
ax.text(7.25,6.08,"Qur'an as a self-interpreting WEB · measured corpus-internally on the rasm · "+A("القرآن یفسر بعضه بعضا"),ha='center',fontsize=12,color=INK)
arr((7.25,7.2),(7.25,6.8),GREEN_DK)
# 3. two threads
box(0.5,3.5,6.0,1.9,'#EAF2FB',BLUE); ax.text(3.5,5.05,"CHRONOLOGY WEB · "+A("الشبکة الزمنیة"),ha='center',fontsize=13,color=BLUE,fontweight='bold')
ax.text(3.5,4.65,"the web in TIME",ha='center',fontsize=12,color=INK,fontstyle='italic')
ax.text(3.5,4.25,"partial-order DAG · 10 parallel threads ·\nevent anchors · multi-temporal sūras",ha='center',fontsize=11.5,color=INK)
ax.text(3.5,3.7,"seed edge: al-Ḍuḥā→al-Kawthar (promise→fulfilment)",ha='center',fontsize=11,color=GREEN_DK)
box(8.0,3.5,6.0,1.9,'#F3F0F8',PURP); ax.text(11.0,5.05,"INNER SELF · "+A("النفس"),ha='center',fontsize=13,color=PURP,fontweight='bold')
ax.text(11.0,4.65,"the web in the PERSON",ha='center',fontsize=12,color=INK,fontstyle='italic')
ax.text(11.0,4.18,A("النفس")+" (agent: "+A("أمّارة·مسوّلة→لوّامة→مطمئنة")+")\n⊃ "+A("الصدر")+" ⊃ "+A("القلب")+" (processor) · "+A("الفؤاد")+" (sensors)\nzād-feedback · "+A("ذکر")+" input · sealing=offline",ha='center',fontsize=11,color=INK)
arr((6.2,5.85),(3.5,5.4),NAVY); arr((8.3,5.85),(11.0,5.4),NAVY)
# 4. the spine: kawthar <-> abtar
box(1.0,1.0,12.5,1.5,'#FFFDF5',AMBER,2.2)
ax.text(7.25,2.18,"THE ONE AXIS THROUGH EVERY THREAD",ha='center',fontsize=12.5,color=AMBER,fontweight='bold')
ax.text(2.3,1.55,"KAWTHAR · "+A("الکوثر"),ha='center',fontsize=13,color=GREEN_DK,fontweight='bold')
ax.text(2.3,1.18,"abundance · continuity · increase",ha='center',fontsize=11,color=GREEN_DK)
ax.text(12.2,1.55,A("الأبتر")+" · ABTAR",ha='center',fontsize=13,color=RED,fontweight='bold')
ax.text(12.2,1.18,"severance · cut-off",ha='center',fontsize=11,color=RED)
ax.add_patch(FancyArrowPatch((3.9,1.45),(10.6,1.45),arrowstyle='<|-|>',mutation_scale=18,lw=2,color=INK,alpha=.6))
ax.text(7.25,1.62,"chronology: fulfilled promise / continuity   ·   inner self: open, faith-increasing (muṭmaʾinna) ↔ sealed, severed (لا یفقهون)",ha='center',fontsize=10.8,color=INK)
arr((3.5,3.5),(3.0,2.5),BLUE); arr((11.0,3.5),(11.5,2.5),PURP)
fig.savefig('anatomy_figs/synthesis_fit.png',dpi=140,bbox_inches='tight'); print("saved anatomy_figs/synthesis_fit.png")
