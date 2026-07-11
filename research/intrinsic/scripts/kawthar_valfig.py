# -*- coding: utf-8 -*-
"""Figure 13 (NEW, headline validation): pre-registered rarity-matched null.
al-Kawthar's web-binding F sits at the 44th pct of its null -> statistically ordinary. Panel: short suras."""
import collections, itertools, math, random, statistics as st, re as _re
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
import numpy as np
import arabic_reshaper
from bidi.algorithm import get_display
random.seed(11)
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"; OUT=f"{R}/research/intrinsic/kawthar_figs"
_resh=arabic_reshaper.ArabicReshaper(configuration={'delete_harakat':True,'support_ligatures':False})
_AR=_re.compile('[؀-ۿݐ-ݿ]+')
def A(s): return _AR.sub(lambda m: get_display(_resh.reshape(m.group().replace('ک','ك').replace('ی','ي'))), s)
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا')
INK='#10243A'; NAVY='#1D3557'; GREEN='#1D9E75'; GREEN_DK='#0F6E56'; RED='#E63946'; AMBER='#EF9F27'; BORD='#E2E8F1'; BTINT='#EAF2FB'; GREY='#9fb0c4'
plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','text.color':INK})
ay={}
for line in open(f"{R}/research/two_books_genome/roots_by_ayah.tsv",encoding='utf-8'):
    line=line.rstrip('\n')
    if '\t' in line: k,rs=line.split('\t',1); ay[k]=set(fa(x) for x in rs.split())
ayahs=list(ay.values()); N=len(ayahs)
cnt=collections.Counter(); co=collections.Counter()
for s in ayahs:
    for r in s: cnt[r]+=1
    for a,b in itertools.combinations(sorted(s),2): co[(a,b)]+=1
def pair(a,b): return co.get((a,b),0)+co.get((b,a),0)
def ppmi(a,b):
    c=pair(a,b); return max(0.0,math.log2(c*N/(cnt[a]*cnt[b]))) if c>0 else 0.0
MB={}
def mb(r):
    if r not in MB: MB[r]=max((ppmi(r,o) for o in cnt if o!=r and pair(r,o)>0),default=0.0)
    return MB[r]
def F(rs): rs=[r for r in rs if r in cnt]; return sum(mb(r) for r in rs)/len(rs) if rs else 0.0
def fbin(c): return 0 if c==1 else 1 if c<=5 else 2 if c<=20 else 3 if c<=100 else 4 if c<=500 else 5
binroots=collections.defaultdict(list)
for r,c in cnt.items(): binroots[fbin(c)].append(r)
def bootF(roots,n=10000):
    tb=[fbin(cnt[r]) for r in roots if r in cnt]
    return [F([random.choice(binroots[b]) for b in tb]) for _ in range(n)]
def sroots(s): 
    rs=set()
    for k,v in ay.items():
        if int(k.split(':')[0])==s: rs|=v
    return sorted(rs)
KW=[fa(x) for x in ['عطو','کثر','صلو','ربب','نحر','شنء','بتر']]
fkw=F(KW); dist=bootF(KW,10000)
pct=100.0*sum(1 for x in dist if x<fkw)/len(dist)
z=(fkw-st.mean(dist))/(st.pstdev(dist) or 1e-9)
panel=[(108,'الکوثر'),(103,'العصر'),(110,'النصر'),(112,'الإخلاص'),(113,'الفلق'),(114,'الناس')]
pcts={}
for s,nm in panel:
    rs=KW if s==108 else sroots(s); pcts[s]=100.0*sum(1 for x in bootF(rs,4000) if x<F(rs))/4000

fig,(axL,axR)=plt.subplots(1,2,figsize=(13,5.3),gridspec_kw={'width_ratios':[1.5,1]})
# left: null histogram with al-Kawthar marked
axL.hist(dist,bins=40,color=BTINT,edgecolor='white',zorder=2)
axL.axvline(st.mean(dist),color=GREY,ls='--',lw=1.5); axL.text(st.mean(dist),axL.get_ylim()[1]*0.96,' null mean',color=INK,fontsize=10,va='top')
axL.axvline(fkw,color=RED,lw=2.6,zorder=4)
axL.annotate(A(f"الکوثر  F={fkw:.2f}\n{pct:.0f}th pct  (z={z:+.2f})"),xy=(fkw,axL.get_ylim()[1]*0.55),
             xytext=(fkw+0.5,axL.get_ylim()[1]*0.72),color=RED,fontsize=12.5,fontweight='bold',
             arrowprops=dict(arrowstyle='->',color=RED,lw=1.5))
axL.set_xlabel("web-binding F of a rarity-matched random word-set",fontsize=12,color=INK)
axL.set_ylabel("count (of 10,000 null draws)",fontsize=12,color=INK)
axL.set_title(A("Figure 13.  Pre-registered rarity-matched null.\n"
              "al-Kawthar sits at the 44th pct (z=-0.09): once rarity is\n"
              "controlled it is statistically ORDINARY — the 'designed\n"
              "coherence' reading is not supported."),
              loc='left',fontsize=12.5,color=NAVY,fontweight='bold')
for sp in ['top','right']: axL.spines[sp].set_visible(False)
axL.grid(axis='y',color=BORD,lw=0.8,zorder=0)
# right: panel percentiles
ys=np.arange(len(panel))[::-1]
vals=[pcts[s] for s,_ in panel]
cols=[RED if s==108 else NAVY for s,_ in panel]
axR.barh(ys,vals,color=cols,zorder=3,height=0.6)
axR.axvline(95,color=GREEN_DK,ls=':',lw=1.5); axR.text(95,len(panel)-0.3,'95th\n(outlier line)',color=GREEN_DK,fontsize=9.5,ha='center')
axR.axvline(50,color=GREY,ls='--',lw=1)
axR.set_yticks(ys); axR.set_yticklabels([A(f"{nm} ({s})") for s,nm in panel],fontsize=12,color=INK)
for yi,(s,nm) in zip(ys,panel): axR.text(pcts[s]+2,yi,f"{pcts[s]:.0f}",va='center',fontsize=11,color=INK,fontweight='bold')
axR.set_xlim(0,108); axR.set_xlabel("percentile in its own null",fontsize=11,color=INK)
axR.set_title("Short-sūra panel:\nnone exceeds the 95th pct",fontsize=11.5,color=NAVY,fontweight='bold',loc='left')
for sp in ['top','right']: axR.spines[sp].set_visible(False)
axR.grid(axis='x',color=BORD,lw=0.8,zorder=0)
fig.tight_layout(); fig.savefig(f"{OUT}/fig_null_validation.png",dpi=150,bbox_inches='tight'); fig.savefig(f"{OUT}/fig_null_validation.svg",bbox_inches='tight'); plt.close(fig)
print(f"saved fig_null_validation (Fig 13). al-Kawthar pct={pct:.1f} z={z:+.2f}; panel={ {s:round(pcts[s],1) for s,_ in panel} }")
