# -*- coding: utf-8 -*-
"""V3 figures: F14 frequency spectrum vs Fisher neutral null; F15 rarity ladder (spread vs #roots & mean idf);
F16 burstiness obs vs Poisson null. Arabic via in-place reshaper. Locked palette."""
import collections, math, random, statistics as st, re as _re
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
import numpy as np, arabic_reshaper
from bidi.algorithm import get_display
random.seed(11)
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"; OUT=f"{R}/research/intrinsic/kawthar_figs"
_resh=arabic_reshaper.ArabicReshaper(configuration={'delete_harakat':True,'support_ligatures':False})
_AR=_re.compile('[؀-ۿݐ-ݿ]+')
def A(s): return _AR.sub(lambda m: get_display(_resh.reshape(m.group().replace('ک','ك').replace('ی','ي'))), s)
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا')
INK='#10243A';NAVY='#1D3557';GREEN='#1D9E75';GREEN_DK='#0F6E56';RED='#E63946';AMBER='#EF9F27';BORD='#E2E8F1';BTINT='#EAF2FB';GREY='#9fb0c4'
plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','text.color':INK})
rows=[]
for line in open(f"{R}/research/two_books_genome/roots_by_ayah.tsv",encoding='utf-8'):
    line=line.rstrip('\n')
    if '\t' in line: k,rs=line.split('\t',1); rows.append((k,[fa(x) for x in rs.split()]))
rows.sort(key=lambda kv:(int(kv[0].split(':')[0]),int(kv[0].split(':')[1])))
cnt=collections.Counter(r for _,rsr in rows for r in rsr)
rootsuras=collections.defaultdict(set)
for k,rsr in rows:
    s=int(k.split(':')[0])
    for r in rsr: rootsuras[r].add(s)
spread={r:len(rootsuras[r]) for r in rootsuras}
Nv=len(rows); N=sum(cnt.values()); S=len(cnt)
df=collections.Counter()
for k,rsr in rows:
    for r in set(rsr): df[r]+=1
idf=lambda r: math.log(Nv/df[r])

# ===== F14: frequency spectrum vs Fisher =====
phi=collections.Counter(cnt.values())
def fish_alpha():
    lo,hi=1e-3,1e7
    for _ in range(200):
        m=(lo+hi)/2
        if m*math.log(1+N/m)-S>0: hi=m
        else: lo=m
    return (lo+hi)/2
a=fish_alpha(); x=N/(N+a); pred=lambda k:a*x**k/k
ks=list(range(1,16)); obs=[phi[k] for k in ks]; pr=[pred(k) for k in ks]
fig,ax=plt.subplots(figsize=(9.4,5.2))
w=0.42; xi=np.arange(len(ks))
ax.bar(xi-w/2,obs,w,color=NAVY,zorder=3,label='observed')
ax.bar(xi+w/2,pr,w,color=GREY,zorder=3,label='Fisher log-series (neutral null)')
ax.set_xticks(xi); ax.set_xticklabels(ks); ax.set_yscale('log')
ax.set_xlabel("k = number of times a root occurs in the corpus",fontsize=12,color=INK)
ax.set_ylabel("number of roots (log)",fontsize=12,color=INK)
ax.annotate(f"hapax: {phi[1]} obs vs {pred(1):.0f} null\n(1.21× — a modest excess on a near-neutral spectrum)",
            xy=(0-w/2,phi[1]),xytext=(2.3,235),fontsize=11,color=RED,fontweight='bold',
            arrowprops=dict(arrowstyle='->',color=RED,lw=1.4))
ax.legend(fontsize=11,frameon=True,edgecolor=BORD)
ax.set_title("Figure 14.  The rarity spectrum is near-neutral: 24% of roots are hapax, but Fisher's neutral\nnull already predicts ~80% of them — so hapax abundance is generic, not a special feature.",loc='left',fontsize=12.5,color=NAVY,fontweight='bold')
for sp in ['top','right']: ax.spines[sp].set_visible(False)
ax.grid(axis='y',color=BORD,lw=0.8,zorder=0)
fig.tight_layout(); fig.savefig(f"{OUT}/fig_freqspectrum.png",dpi=150,bbox_inches='tight'); fig.savefig(f"{OUT}/fig_freqspectrum.svg",bbox_inches='tight'); plt.close(fig); print("saved fig_freqspectrum (F14)")

# ===== F15: rarity ladder =====
byk=collections.Counter(spread.values())
ks2=list(range(1,21)); nr=[byk[k] for k in ks2]
mi=[ (sum(idf(r) for r in spread if spread[r]==k)/byk[k]) if byk[k] else 0 for k in ks2]
fig,ax=plt.subplots(figsize=(9.8,5.4)); ax2=ax.twinx()
ax.bar(ks2,nr,color=BTINT,edgecolor='white',zorder=2,label='# roots at this spread')
ax2.plot(ks2,mi,color=GREEN_DK,lw=2.4,marker='o',ms=4,zorder=4,label='mean idf (specificity)')
ax.set_xlabel("spread k = number of sūras a root appears in",fontsize=12,color=INK)
ax.set_ylabel("# roots",fontsize=12,color=NAVY); ax2.set_ylabel("mean idf  (higher = more specific)",fontsize=12,color=GREEN_DK)
ax.set_xticks(ks2)
# al-Kawthar roots placed on the ladder
KW={'نحر':1,'بتر':1,'شنء':2,'عطو':11}; 
for r,k in KW.items():
    ax.annotate(A(r),(k,byk[k]),xytext=(k,byk[k]+30),fontsize=12,color=RED if k<=2 else NAVY,fontweight='bold',ha='center',
                arrowprops=dict(arrowstyle='->',color=RED if k<=2 else NAVY,lw=1))
ax.text(0.97,0.55,A("al-Kawthar spans the ladder:\nنحر، بتر at k=1 (islands), شنء at k=2,\nعطو k=11, صلو k=37, کثر k=51, ربب k=94"),
        transform=ax.transAxes,ha='right',va='top',fontsize=10.5,color=INK,bbox=dict(boxstyle='round',fc='#F4F9F7',ec='#cfe4dc'))
ax.text(0.97,0.78,"k=1: concrete once-named objects (بصل، عدس، قثء)\n→ k≥5: abstractions (جوع، حرص)",transform=ax.transAxes,ha='right',va='top',fontsize=10,color=GREEN_DK)
ax.set_title("Figure 15.  The rarity ladder: as roots touch more sūras, specificity falls smoothly (mean idf,\ngreen) — a concrete→abstract gradient. al-Kawthar's roots sample every rung.",loc='left',fontsize=12.5,color=NAVY,fontweight='bold')
for sp in ['top']: ax.spines[sp].set_visible(False); ax2.spines[sp].set_visible(False)
fig.tight_layout(); fig.savefig(f"{OUT}/fig_rarityladder.png",dpi=150,bbox_inches='tight'); fig.savefig(f"{OUT}/fig_rarityladder.svg",bbox_inches='tight'); plt.close(fig); print("saved fig_rarityladder (F15)")

# ===== F16: burstiness STRATIFIED by frequency (rare end is NOT the bursty part) =====
order={k:i for i,(k,_) in enumerate(rows)}
occ=collections.defaultdict(list)
for i,(k,rsr) in enumerate(rows):
    for r in set(rsr): occ[r].append(i)
def burst(p):
    g=[p[i+1]-p[i] for i in range(len(p)-1)]
    if len(g)<2: return None
    m=st.mean(g); s=st.pstdev(g); return (s-m)/(s+m) if (s+m)>0 else 0.0
bands=[("rare\n5-15",5,15),("mid\n16-60",16,60),("common\n61-300",61,300),("ubiq\n>300",301,10**9)]
labs=[]; obsB=[]; nulB=[]
for nm,lo,hi in bands:
    rs=[r for r in occ if lo<=cnt[r]<=hi]
    Bo=[b for r in rs if (b:=burst(occ[r])) is not None]
    Bn=[b for r in rs for b in [burst(sorted(random.sample(range(Nv),cnt[r])))] if b is not None]
    labs.append(nm); obsB.append(st.median(Bo)); nulB.append(st.median(Bn))
fig,ax=plt.subplots(figsize=(9.2,5.2))
xi=np.arange(len(labs)); w=0.4
ax.bar(xi-w/2,obsB,w,color=NAVY,zorder=3,label='observed median B')
ax.bar(xi+w/2,nulB,w,color=GREY,zorder=3,label='Poisson-null median B')
ax.axhline(0,color=INK,lw=1)
ax.set_xticks(xi); ax.set_xticklabels(labs,fontsize=11)
ax.set_xlabel("frequency band (corpus occurrences)",fontsize=12,color=INK)
ax.set_ylabel("median burstiness B  (>0 = clustered)",fontsize=12,color=INK)
ax.set_title("Figure 16.  Burstiness rises with frequency — the rare end is NOT self-exciting.\n"
             "Rare roots (5-15) are near-Poisson (B≈-0.04); only common/ubiquitous roots cluster strongly.\n"
             "So 'self-exciting lexicon' is a common-word property, not a rarity feature.",loc='left',fontsize=12,color=NAVY,fontweight='bold')
ax.legend(fontsize=11,frameon=True,edgecolor=BORD)
for sp in ['top','right']: ax.spines[sp].set_visible(False)
ax.grid(axis='y',color=BORD,lw=0.8,zorder=0)
fig.tight_layout(); fig.savefig(f"{OUT}/fig_burstiness.png",dpi=150,bbox_inches='tight'); fig.savefig(f"{OUT}/fig_burstiness.svg",bbox_inches='tight'); plt.close(fig); print("saved fig_burstiness (F16 stratified)")
