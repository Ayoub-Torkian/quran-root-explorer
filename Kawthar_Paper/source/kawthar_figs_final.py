# -*- coding: utf-8 -*-
"""Final dense figures 1-6 (chart/diagram). Readouts removed. Full-width, no overlap, >=12px, locked palette."""
import json, os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
D=json.load(open(f"{R}/research/intrinsic/scripts/kawthar_data.json",encoding='utf-8'))
OUT=f"{R}/research/intrinsic/kawthar_figs"
INK='#10243A'; NAVY='#1D3557'; GREEN='#1D9E75'; GREEN_DK='#0F6E56'; GTINT='#F4F9F7'; BTINT='#EAF2FB'
BORD='#E2E8F1'; BORDEM='#C9D6E8'; RED='#E63946'; BLUE='#378ADD'; AMBER='#EF9F27'
plt.rcParams.update({'font.size':13,'text.color':INK,'axes.labelcolor':INK,'xtick.color':INK,'ytick.color':INK,
 'axes.edgecolor':BORDEM,'font.family':'DejaVu Sans','axes.titlecolor':NAVY,'figure.facecolor':'white',
 'axes.facecolor':'white','savefig.facecolor':'white','axes.titlesize':14,'axes.titleweight':'bold','svg.fonttype':'none'})
import arabic_reshaper
from bidi.algorithm import get_display
_resh=arabic_reshaper.ArabicReshaper(configuration={'delete_harakat':True,'support_ligatures':False})
def ar(s): return get_display(_resh.reshape(s.replace('ک','ك').replace('ی','ي')))
def save(fig,name):
    fig.tight_layout(); fig.savefig(f"{OUT}/{name}.png",dpi=150,bbox_inches='tight'); fig.savefig(f"{OUT}/{name}.svg",bbox_inches='tight'); plt.close(fig); print("saved",name)
ROM={'عطو':'ʿ-ṭ-w','کثر':'k-th-r','صلو':'ṣ-l-w','ربب':'r-b-b','نحر':'n-ḥ-r','شنء':'sh-n-ʾ','بتر':'b-t-r',
 'قطع':'q-ṭ-ʿ','دبر':'d-b-r','هلک':'h-l-k','نسک':'n-s-k','ذبح':'dh-b-ḥ','هدی':'h-d-y','قرب':'q-r-b','بدن':'b-d-n'}
GL={'عطو':'give','کثر':'abundance','صلو':'prayer','ربب':'Lord','نحر':'sacrifice','شنء':'hate','بتر':'cut off',
 'نسک':'rite','ذبح':'slaughter','هدی':'offering','قرب':'draw near','بدن':'sacrificial camel'}

# ===== Figure 1: rarity =====
inv=D['inventory']
fig,ax=plt.subplots(figsize=(9.6,5))
occ=[max(i['occ'],0.7) for i in inv]; y=np.arange(len(inv))[::-1]
cols=[RED if i['hapax'] else (GREEN if i['root']=='کثر' else NAVY) for i in inv]
ax.barh(y,occ,color=cols,edgecolor='white',height=0.62,zorder=3)
ax.set_yticks(y); ax.set_yticklabels([f"{ar(i['root'])}  ·  {GL[i['root']]}" for i in inv],fontsize=13)
ax.set_xscale('log'); ax.set_xlim(0.6,1600)
med=D['corpus_root_stats']['median_occ']; ax.axvline(med,color=BLUE,ls='--',lw=1.8,zorder=2)
ax.text(1100,5.55,f"blue dash = corpus median ({med})",color=BLUE,fontsize=12,fontweight='bold',ha='right',va='center')
for yi,i in zip(y,inv):
    t=f"{i['occ']}×"+("  HAPAX (only here)" if i['hapax'] else f"  ·  {i['n_surahs']} sūras")
    ax.text(max(i['occ'],0.7)*1.13,yi,t,va='center',fontsize=12,color=RED if i['hapax'] else INK,fontweight='bold' if i['hapax'] else 'normal')
ax.set_xlabel("Times the root occurs in the whole Qurʾān (log scale)",fontsize=13)
ax.set_title("Figure 1.  The lexical fingerprint of al-Kawthar:\ntwo words used only once in the entire Qurʾān",loc='left')
for s in ['top','right']: ax.spines[s].set_visible(False)
ax.grid(axis='x',color=BORD,lw=0.8,zorder=0); save(fig,'f1_rarity')

# ===== Figure 2: antithesis spine =====
fig,ax=plt.subplots(figsize=(9.6,5.2)); ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,10)
def box(x,y,w,h,fc,ec,txt,tc,fs=12.5):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.08,rounding_size=0.12",fc=fc,ec=ec,lw=1.6))
    ax.text(x+w/2,y+h/2,txt,ha='center',va='center',color=tc,fontsize=fs,fontweight='bold')
box(0.3,6.0,4.2,2.7,GTINT,GREEN,"ABUNDANCE · CONTINUATION\n\nkawthar (108:1)\nʿaṭā 'give' — 14×\nk-th-r field — 167×",GREEN_DK)
box(5.5,6.0,4.2,2.7,'#FBEAEC',RED,"SEVERANCE · NO ISSUE\n\nabtar (108:3, hapax)\nq-ṭ-ʿ 'sever' — 36× · d-b-r 'remnant' — 44×\nh-l-k 'perish' — 68×",RED)
box(3.0,2.3,4.0,2.0,BTINT,NAVY,"SŪRAT AL-KAWTHAR\nGod gives → you worship →\nthe hater is the one cut off",NAVY)
ax.add_patch(FancyArrowPatch((2.4,6.0),(4.3,4.3),arrowstyle='-|>',mutation_scale=18,color=GREEN_DK,lw=2))
ax.add_patch(FancyArrowPatch((7.6,6.0),(5.7,4.3),arrowstyle='-|>',mutation_scale=18,color=RED,lw=2))
ax.text(5,1.2,"The taunt is reversed: the one who calls the Prophet 'cut off' is himself al-abtar.",ha='center',fontsize=12,color=INK,style='italic')
ax.text(5,9.5,"Figure 2.  The surah's spine is a single antithesis read off the roots",ha='center',fontsize=14,color=NAVY,fontweight='bold')
save(fig,'f2_antithesis')

# ===== Figure 3: sacrifice field (decluttered, full width; note moved to caption) =====
sf=D['sacrifice_field']; order=['نحر','بدن','نسک','ذبح','قرب','صلو','هدی']
fig,ax=plt.subplots(figsize=(9.8,4.8))
ys=[sf[r]['occ'] for r in order]
cols=[RED if sf[r]['hapax'] else (GREEN if r=='صلو' else NAVY) for r in order]
b=ax.bar([ar(r) for r in order],ys,color=cols,edgecolor='white',zorder=3,width=0.7)
for r,rect in zip(order,b):
    ax.text(rect.get_x()+rect.get_width()/2,rect.get_height()+7,f"{sf[r]['occ']}×\n{GL[r]}",ha='center',va='bottom',fontsize=12,color=INK)
ax.set_ylim(0,360); ax.set_ylabel("Occurrences in the Qurʾān",fontsize=13)
ax.set_title("Figure 3.  Defining a word used once: the hapax 'naḥr' (sacrifice)\nis interpreted by the Qurʾān's wider sacrifice vocabulary",loc='left')
for s in ['top','right']: ax.spines[s].set_visible(False)
ax.grid(axis='y',color=BORD,lw=0.8,zorder=0); ax.margins(x=0.02); save(fig,'f3_sacrifice')

# ===== Figure 4: verse architecture =====
fig,ax=plt.subplots(figsize=(9.8,5.2)); ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,10)
ax.text(5,9.5,"Figure 4.  The architecture of three verses",ha='center',fontsize=14,color=NAVY,fontweight='bold')
rows=[("V1",ar("إنا أعطيناك الكوثر"),"'Indeed WE gave YOU the abundance'","God → Prophet : the gift",GREEN),
      ("V2",ar("فصل لربك وانحر"),"'so pray to your Lord and sacrifice'","Prophet's response : worship",NAVY),
      ("V3",ar("إن شانئك هو الأبتر"),"'indeed YOUR hater is the cut-off one'","verdict on the adversary",RED)]
for (tag,tr,gl,role,col),yv in zip(rows,[6.8,4.5,2.2]):
    ax.add_patch(FancyBboxPatch((1.0,yv),7.0,1.7,boxstyle="round,pad=0.06,rounding_size=0.1",fc='white',ec=col,lw=1.8))
    ax.text(1.3,yv+1.15,f"{tag}.  {tr}",fontsize=12.5,color=INK,fontweight='bold')
    ax.text(1.3,yv+0.55,gl,fontsize=12,color=INK,style='italic')
    ax.text(7.8,yv+0.85,role,fontsize=12,color=col,ha='right',fontweight='bold')
ax.annotate("",xy=(0.72,8.5),xytext=(0.72,2.2),arrowprops=dict(arrowstyle='-',color=AMBER,lw=3))
ax.plot([0.72,0.95],[8.5,8.5],color=AMBER,lw=3); ax.plot([0.72,0.95],[2.2,2.2],color=AMBER,lw=3)
ax.text(0.42,5.35,"inna … inna\n(ring: opens V1, closes V3)",rotation=90,va='center',ha='center',fontsize=12,color='#7a5200',fontweight='bold')
ax.text(8.72,5.35,"-ka thread:\n'you / your'\nin ALL three",fontsize=12,color=GREEN_DK,fontweight='bold',va='center')
ax.annotate("",xy=(8.45,8.5),xytext=(8.45,2.2),arrowprops=dict(arrowstyle='-',color=GREEN,lw=2.4,ls=(0,(3,2))))
save(fig,'f4_structure')

# ===== Figure 5: shortest surah =====
SL=D['surah_lengths']; vals=sorted(SL.values())
fig,ax=plt.subplots(figsize=(9.6,4.8))
ax.hist(vals,bins=40,color=NAVY,edgecolor='white',zorder=3)
s108=D['s108_letters']; s102=D['s102_letters']
ax.axvline(s108,color=GREEN,lw=2.4,zorder=4); ax.axvline(s102,color=AMBER,lw=2.0,zorder=4)
ax.annotate(f"al-Kawthar (108)\n{s108} letters — the shortest sūra",xy=(s108,8),xytext=(s108+300,30),fontsize=12,color=GREEN_DK,fontweight='bold',arrowprops=dict(arrowstyle='->',color=GREEN_DK,lw=1.6))
ax.annotate(f"at-Takāthur (102)\nits root-twin — {s102} letters",xy=(s102,5),xytext=(s102+340,18),fontsize=12,color='#7a5200',fontweight='bold',arrowprops=dict(arrowstyle='->',color=AMBER,lw=1.5))
ax.set_xlabel("Length of each sūra (rasm letters, basmala excluded)",fontsize=13); ax.set_ylabel("Number of sūras",fontsize=13)
ax.set_title("Figure 5.  Among all 114 sūras, al-Kawthar is the shortest —\nyet it carries a complete argument",loc='left')
for s in ['top','right']: ax.spines[s].set_visible(False)
ax.grid(axis='y',color=BORD,lw=0.8,zorder=0); ax.set_xlim(0,2500); save(fig,'f5_shortest')

# ===== Figure 6: hapax density =====
dist=D['ayah_hapax_dist']; ks=sorted(int(k) for k in dist); vs=[dist.get(str(k),dist.get(k,0)) for k in ks]
fig,ax=plt.subplots(figsize=(9.6,4.6))
b=ax.bar([str(k) for k in ks],vs,color=[NAVY if k<2 else RED for k in ks],edgecolor='white',zorder=3,width=0.7)
for k,rect in zip(ks,b): ax.text(rect.get_x()+rect.get_width()/2,rect.get_height()+40,str(int(rect.get_height())),ha='center',fontsize=12,color=INK)
ax.set_yscale('symlog'); ax.set_xlabel("Number of 'used-only-once' roots in a single verse",fontsize=13); ax.set_ylabel("Number of verses (log)",fontsize=13)
n2=D['n_ayahs_2plus_hapax']
ax.set_title("Figure 6.  Lexical singularity: only %d of 6,236 verses reach 2+ rare words —\nal-Kawthar packs 2 into a 3-verse sūra"%n2,loc='left')
for s in ['top','right']: ax.spines[s].set_visible(False)
ax.grid(axis='y',color=BORD,lw=0.8,zorder=0); save(fig,'f6_hapax')
print("DONE figs 1-6")
