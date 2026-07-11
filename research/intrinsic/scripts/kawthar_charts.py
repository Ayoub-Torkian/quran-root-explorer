# -*- coding: utf-8 -*-
"""Publication charts for the al-Kawthar study. Locked palette, >=12px ink, no grey text."""
import json, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
D=json.load(open(f"{R}/research/intrinsic/scripts/kawthar_data.json",encoding='utf-8'))
OUT=f"{R}/research/intrinsic/kawthar_figs"; os.makedirs(OUT,exist_ok=True)

INK='#10243A'; NAVY='#1D3557'; GREEN='#1D9E75'; GREEN_DK='#0F6E56'
GTINT='#F4F9F7'; BTINT='#EAF2FB'; BORD='#E2E8F1'; BORDEM='#C9D6E8'
RED='#E63946'; BLUE='#378ADD'; AMBER='#EF9F27'

plt.rcParams.update({'font.size':13,'text.color':INK,'axes.labelcolor':INK,
 'xtick.color':INK,'ytick.color':INK,'axes.edgecolor':BORDEM,'font.family':'DejaVu Sans',
 'axes.titlecolor':NAVY,'figure.facecolor':'white','axes.facecolor':'white',
 'savefig.facecolor':'white','axes.titlesize':14,'axes.titleweight':'bold','svg.fonttype':'none'})

def save(fig,name):
    fig.tight_layout()
    fig.savefig(f"{OUT}/{name}.png",dpi=150,bbox_inches='tight')
    fig.savefig(f"{OUT}/{name}.svg",bbox_inches='tight')
    plt.close(fig)
    print("saved",name)

# romanization
ROM={'عطو':'ʿ-ṭ-w','کثر':'k-th-r','صلو':'ṣ-l-w','ربب':'r-b-b','نحر':'n-ḥ-r',
 'شنء':'sh-n-ʾ','بتر':'b-t-r','قطع':'q-ṭ-ʿ','دبر':'d-b-r','هلک':'h-l-k','صرم':'ṣ-r-m',
 'جذذ':'j-dh-dh','نسک':'n-s-k','ذبح':'dh-b-ḥ','هدی':'h-d-y','قرب':'q-r-b','بدن':'b-d-n',
 'زکو':'z-k-w','قوم':'q-w-m','ءله':'ʾ-l-h(Allah)','اتی':'ʾ-t-y','ءمن':'ʾ-m-n','کون':'k-w-n',
 'ذکر':'dh-k-r','ءخر':'ʾ-kh-r','رسل':'r-s-l','قول':'q-w-l','علم':'ʿ-l-m','صبر':'ṣ-b-r',
 'رکع':'r-k-ʿ','سجد':'s-j-d'}
GLOSS={'عطو':'give','کثر':'abundance','صلو':'prayer','ربب':'Lord','نحر':'sacrifice',
 'شنء':'hate','بتر':'cut off','قطع':'sever','دبر':'rear/remnant','هلک':'perish',
 'نسک':'rite','ذبح':'slaughter','هدی':'offering/guide','قرب':'draw near','بدن':'sacrificial camel','زکو':'almsgiving'}

# ---------- C1 rarity profile ----------
inv=D['inventory']
fig,ax=plt.subplots(figsize=(8.6,5))
roots=[i['root'] for i in inv]; occ=[max(i['occ'],0.7) for i in inv]
labels=[f"{ROM[r]}  ·  {GLOSS[r]}" for r in roots]
colors=[RED if i['hapax'] else (GREEN if i['root']=='کثر' else NAVY) for i in inv]
y=np.arange(len(inv))[::-1]
ax.barh(y,occ,color=colors,edgecolor='white',height=0.62,zorder=3)
ax.set_yticks(y); ax.set_yticklabels(labels,fontsize=13)
ax.set_xscale('log'); ax.set_xlim(0.6,1400)
med=D['corpus_root_stats']['median_occ']
ax.axvline(med,color=BLUE,ls='--',lw=1.8,zorder=2)
ax.text(950,5.55,f"blue dash = corpus median ({med})",color=BLUE,fontsize=12,fontweight='bold',ha='right',va='center')
for yi,i in zip(y,inv):
    t=f"{i['occ']}×" + ("  HAPAX (only here)" if i['hapax'] else f"  ·  {i['n_surahs']} sūras")
    ax.text(max(i['occ'],0.7)*1.12,yi,t,va='center',fontsize=12,
            color=RED if i['hapax'] else INK,fontweight='bold' if i['hapax'] else 'normal')
ax.set_xlabel("Times the root occurs in the whole Qurʾān (log scale)",fontsize=13)
ax.set_title("Figure 1.  The lexical fingerprint of al-Kawthar:\ntwo words used only once in the entire Qurʾān",loc='left')
for s in ['top','right']: ax.spines[s].set_visible(False)
ax.grid(axis='x',color=BORD,lw=0.8,zorder=0)
save(fig,'fig1_rarity')

# ---------- C2 kthr valence ----------
v=D['kthr_field']['valence']; tot=D['kthr_field']['total_ayahs']
caut=v['most_negated']+v['rivalry_takathur']; other=v['other']
fig,ax=plt.subplots(figsize=(8.6,3.6))
ax.barh([0],[caut],color=AMBER,edgecolor='white',zorder=3,height=0.6,label='cautionary pole')
ax.barh([0],[other],left=[caut],color=GREEN,edgecolor='white',zorder=3,height=0.6,label='neutral / good pole')
ax.text(caut/2,0,f"cautionary 'muchness'\n≈ {caut} verses\n(most people do not…; takāthur)",
        ha='center',va='center',color=INK,fontsize=12,fontweight='bold')
ax.text(caut+other/2,0,f"neutral / good abundance\n≈ {other} verses\n(incl. 108:1 al-Kawthar — the gift)",ha='center',va='center',color='white',fontsize=12,fontweight='bold')
ax.set_xlim(0,tot); ax.set_ylim(-0.6,0.6); ax.set_yticks([])
ax.set_xlabel(f"All {tot} verses containing the root k-th-r (abundance)",fontsize=13)
ax.set_title("Figure 2.  The root behind 'Kawthar' has two faces in the Qurʾān —\nthe gift in 108:1 is the good pole of 'muchness'",loc='left')
for s in ['top','right','left']: ax.spines[s].set_visible(False)
save(fig,'fig2_kthr_valence')

# ---------- C3 antithesis spine ----------
fig,ax=plt.subplots(figsize=(9,5.4)); ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,10)
# left pole abundance
def box(x,y,w,h,fc,ec,txt,tc=INK,fs=12,bold=True):
    p=FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.08,rounding_size=0.12",
        fc=fc,ec=ec,lw=1.6); ax.add_patch(p)
    ax.text(x+w/2,y+h/2,txt,ha='center',va='center',color=tc,fontsize=fs,
        fontweight='bold' if bold else 'normal')
box(0.3,6.2,3.6,2.6,GTINT,GREEN,"ABUNDANCE · CONTINUATION\n\nkawthar (108:1)\nʿaṭā 'give' — 14×\nk-th-r field — 167×",GREEN_DK,12.5)
box(6.1,6.2,3.6,2.6,'#FBEAEC',RED,"SEVERANCE · NO ISSUE\n\nabtar (108:3, hapax)\nq-ṭ-ʿ 'sever' — 36×\nd-b-r 'remnant' — 44×\nh-l-k 'perish' — 68×",RED,12.5)
box(3.0,2.4,4.0,2.0,BTINT,NAVY,"SŪRAT AL-KAWTHAR\nGod gives → you worship →\nthe hater is the one cut off",NAVY,12.5)
a1=FancyArrowPatch((2.1,6.2),(4.2,4.4),arrowstyle='-|>',mutation_scale=18,color=GREEN_DK,lw=2);ax.add_patch(a1)
a2=FancyArrowPatch((7.9,6.2),(5.8,4.4),arrowstyle='-|>',mutation_scale=18,color=RED,lw=2);ax.add_patch(a2)
ax.text(5,1.3,"The taunt is reversed: the one who calls the Prophet 'cut off' is himself al-abtar.",
        ha='center',fontsize=12,color=INK,style='italic')
ax.text(5,9.5,"Figure 3.  The surah's spine is a single antithesis read off the roots",
        ha='center',fontsize=14,color=NAVY,fontweight='bold')
save(fig,'fig3_antithesis')

# ---------- C4 sacrifice field ----------
sf=D['sacrifice_field']; order=['نحر','بدن','نسک','ذبح','قرب','صلو','هدی']
fig,ax=plt.subplots(figsize=(8.6,4.6))
xs=[ROM[r] for r in order]; ys=[sf[r]['occ'] for r in order]
cols=[RED if sf[r]['hapax'] else (GREEN if r=='صلو' else NAVY) for r in order]
b=ax.bar(xs,ys,color=cols,edgecolor='white',zorder=3,width=0.66)
for r,rect in zip(order,b):
    g=GLOSS.get(r,'');
    ax.text(rect.get_x()+rect.get_width()/2,rect.get_height()+6,
        f"{sf[r]['occ']}×\n{g}",ha='center',va='bottom',fontsize=12,color=INK)
ax.set_ylim(0,350)
ax.set_title("Figure 4.  Defining a word used once: the hapax 'naḥr' (sacrifice)\nis interpreted by the Qurʾān's wider sacrifice vocabulary",loc='left')
ax.set_ylabel("Occurrences in the Qurʾān",fontsize=13)
for s in ['top','right']: ax.spines[s].set_visible(False)
ax.grid(axis='y',color=BORD,lw=0.8,zorder=0)
ax.text(0.0,330,"n-ḥ-r occurs only in 108:2; 6:162 ('my prayer and my rites…') and 22:37 ('not the flesh… but your piety')\nsupply its sense",
        fontsize=12,color=INK,transform=ax.get_yaxis_transform() if False else ax.transData)
save(fig,'fig4_sacrifice')

# ---------- C5 structural verse map ----------
fig,ax=plt.subplots(figsize=(9,5.2)); ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,10)
ax.text(5,9.5,"Figure 5.  The architecture of three verses",ha='center',fontsize=14,color=NAVY,fontweight='bold')
rows=[("V1","innā aʿṭaynā-ka l-kawthar","'Indeed WE gave YOU the abundance'","God → Prophet : the gift",GREEN),
      ("V2","fa-ṣalli li-rabbi-ka wa-nḥar","'so pray to your Lord and sacrifice'","Prophet's response : worship",NAVY),
      ("V3","inna shāniʾa-ka huwa l-abtar","'indeed YOUR hater is the cut-off one'","verdict on the adversary",RED)]
yy=[6.8,4.5,2.2]
for (tag,tr,gl,role,col),y in zip(rows,yy):
    box=FancyBboxPatch((1.0,y),7.0,1.7,boxstyle="round,pad=0.06,rounding_size=0.1",
        fc='white',ec=col,lw=1.8); ax.add_patch(box)
    ax.text(1.3,y+1.15,f"{tag}.  {tr}",fontsize=12.5,color=INK,fontweight='bold')
    ax.text(1.3,y+0.55,gl,fontsize=12,color=INK,style='italic')
    ax.text(7.8,y+0.85,role,fontsize=12,color=col,ha='right',fontweight='bold')
# inna inclusio bracket (spans V1 ... V3 — opens at V1, closes at V3)
ax.annotate("",xy=(0.72,8.5),xytext=(0.72,2.2),arrowprops=dict(arrowstyle='-',color=AMBER,lw=3))
ax.plot([0.72,0.95],[8.5,8.5],color=AMBER,lw=3); ax.plot([0.72,0.95],[2.2,2.2],color=AMBER,lw=3)
ax.text(0.42,5.35,"inna … inna\n(emphatic ring:\nopens V1, closes V3)",rotation=90,va='center',ha='center',fontsize=12,color='#7a5200',fontweight='bold')
# kaf thread (all three verses)
ax.text(8.72,5.35,"-ka thread:\n'you / your'\nin ALL three\nverses",fontsize=12,color=GREEN_DK,fontweight='bold',va='center')
ax.annotate("",xy=(8.45,8.5),xytext=(8.45,2.2),arrowprops=dict(arrowstyle='-',color=GREEN,lw=2.4,ls=(0,(3,2))))
save(fig,'fig5_structure')

# ---------- C6 rhyme & shape ----------
st=D['structure']
fig,(ax1,ax2)=plt.subplots(1,2,figsize=(9.2,4.2),gridspec_kw={'width_ratios':[1.1,1]})
v=[s['k'].split(':')[1] for s in st]; nl=[s['n_letters'] for s in st]; nw=[s['n_words'] for s in st]
x=np.arange(3)
ax1.bar(x-0.18,nl,width=0.36,color=NAVY,zorder=3,label='letters (rasm)')
ax1.bar(x+0.18,nw,width=0.36,color=GREEN,zorder=3,label='words')
for i in range(3):
    ax1.text(x[i]-0.18,nl[i]+0.4,str(nl[i]),ha='center',fontsize=12,color=INK,fontweight='bold')
    ax1.text(x[i]+0.18,nw[i]+0.4,str(nw[i]),ha='center',fontsize=12,color=INK,fontweight='bold')
ax1.set_xticks(x); ax1.set_xticklabels([f"verse {n}" for n in v],fontsize=12)
ax1.set_ylim(0,20); ax1.legend(fontsize=12,frameon=False,loc='upper right')
ax1.set_title("Size of each verse",fontsize=13,color=NAVY)
for s in ['top','right']: ax1.spines[s].set_visible(False)
ax1.grid(axis='y',color=BORD,lw=0.8,zorder=0)
# rhyme panel
ax2.axis('off'); ax2.set_xlim(0,10); ax2.set_ylim(0,10)
ax2.text(5,9.3,"One rhyme, three times",ha='center',fontsize=13,color=NAVY,fontweight='bold')
ends=[("-kaw-THAR","ث + ر"),("-wan-ḤAR","ح + ر"),("-ab-TAR","ت + ر")]
for i,(e,ar) in enumerate(ends):
    y=7-2.4*i
    ax2.text(2.2,y,e,fontsize=14,color=INK,fontweight='bold',ha='left')
    ax2.text(7.0,y,ar,fontsize=13,color=GREEN_DK,ha='center')
ax2.text(5,0.4,"every verse ends in –ar (rāʾ),\npreceded by a soft voiceless sound (th / ḥ / t)",
         ha='center',fontsize=12,color=INK,style='italic')
fig.suptitle("Figure 6.  Shape and sound: the shortest sūra, sealed by a single rhyme",
             x=0.02,ha='left',fontsize=14,color=NAVY,fontweight='bold')
save(fig,'fig6_rhyme')

# ---------- C7 shortest surah ----------
SL=D['surah_lengths']; vals=sorted(SL.values())
fig,ax=plt.subplots(figsize=(8.6,4.6))
ax.hist(vals,bins=40,color=NAVY,edgecolor='white',zorder=3)
s108=D['s108_letters']; s102=D['s102_letters']
ax.axvline(s108,color=GREEN,lw=2.4,zorder=4)
ax.axvline(s102,color=AMBER,lw=2.0,zorder=4)
ax.annotate(f"al-Kawthar (108)\n{s108} letters — the shortest sūra",xy=(s108,8),xytext=(s108+260,30),
    fontsize=12,color=GREEN_DK,fontweight='bold',arrowprops=dict(arrowstyle='->',color=GREEN_DK,lw=1.6))
ax.annotate(f"at-Takāthur (102)\nits root-twin — {s102} letters",xy=(s102,5),xytext=(s102+300,18),
    fontsize=12,color='#7a5200',fontweight='bold',arrowprops=dict(arrowstyle='->',color=AMBER,lw=1.5))
ax.set_xlabel("Length of each sūra (rasm letters, basmala excluded)",fontsize=13)
ax.set_ylabel("Number of sūras",fontsize=13)
ax.set_title("Figure 7.  Among all 114 sūras, al-Kawthar is the shortest —\nyet it carries a complete argument",loc='left')
for s in ['top','right']: ax.spines[s].set_visible(False)
ax.grid(axis='y',color=BORD,lw=0.8,zorder=0); ax.set_xlim(0,2500)
save(fig,'fig7_shortest')

# ---------- C8 salat partners ----------
co=D['salat_cooc_top'][:10]
fig,ax=plt.subplots(figsize=(8.6,4.8))
names=[ROM.get(r,r) for r,_ in co]; vals=[c for _,c in co]
cols=[GREEN if r in ('زکو','رکع','سجد') else NAVY for r,_ in co]
y=np.arange(len(co))[::-1]
ax.barh(y,vals,color=cols,edgecolor='white',height=0.62,zorder=3)
ax.set_yticks(y); ax.set_yticklabels(names,fontsize=12.5)
for yi,(r,c) in zip(y,co):
    extra='  ← almsgiving (zakāt): prayer\'s usual partner' if r=='زکو' else ''
    ax.text(c+0.6,yi,f"{c}{extra}",va='center',fontsize=12,color=GREEN_DK if r=='زکو' else INK,
            fontweight='bold' if r=='زکو' else 'normal')
ax.set_xlabel("Verses where the root shares a verse with 'prayer' (ṣ-l-w)",fontsize=13)
ax.set_title("Figure 8.  Prayer rarely travels alone: in 108:2 its companion is\nsacrifice — elsewhere it is almsgiving",loc='left')
for s in ['top','right']: ax.spines[s].set_visible(False)
ax.grid(axis='x',color=BORD,lw=0.8,zorder=0); ax.set_xlim(0,60)
save(fig,'fig8_salat')

# ---------- C9 hapax density ----------
dist=D['ayah_hapax_dist']
fig,ax=plt.subplots(figsize=(8.6,4.4))
ks=sorted(int(k) for k in dist); vs=[dist[str(k)] if str(k) in dist else dist[k] for k in ks]
# dist keys may be ints
vs=[dist.get(str(k),dist.get(k,0)) for k in ks]
b=ax.bar([str(k) for k in ks],vs,color=[NAVY if k<2 else RED for k in ks],edgecolor='white',zorder=3)
for k,rect in zip(ks,b):
    val=rect.get_height()
    ax.text(rect.get_x()+rect.get_width()/2,val+40,str(val),ha='center',fontsize=12,color=INK)
ax.set_yscale('symlog')
ax.set_xlabel("Number of 'used-only-once' roots in a single verse",fontsize=13)
ax.set_ylabel("Number of verses (log)",fontsize=13)
n2=D['n_ayahs_2plus_hapax']
ax.set_title("Figure 9.  Lexical singularity: only %d of 6,236 verses reach 2+ rare words —\nal-Kawthar packs 2 into a 3-verse sūra"%n2,loc='left')
for s in ['top','right']: ax.spines[s].set_visible(False)
ax.grid(axis='y',color=BORD,lw=0.8,zorder=0)
save(fig,'fig9_hapax')

print("ALL FIGURES DONE ->",OUT)
print(sorted(os.listdir(OUT)))
