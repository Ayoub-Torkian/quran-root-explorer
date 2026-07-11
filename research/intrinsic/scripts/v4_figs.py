# -*- coding: utf-8 -*-
"""V4 dense figures 19-23 (real, information-rich). Locked palette/typography; Arabic reshaped in place.
No embedded 'Figure N' title (markdown caption supplies it)."""
import collections, itertools, math, random
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import re as _re, arabic_reshaper
from bidi.algorithm import get_display
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"; OUT=f"{R}/research/intrinsic/kawthar_figs"
_resh=arabic_reshaper.ArabicReshaper(configuration={'delete_harakat':True,'support_ligatures':False})
_AR=_re.compile(r'[؀-ۿݐ-ݿ]+')
def A(s): return _AR.sub(lambda m:get_display(_resh.reshape(m.group().replace('ک','ك').replace('ی','ي'))),s)
INK='#10243A'; NAVY='#1D3557'; GREEN='#1D9E75'; GREEN_DK='#0F6E56'; RED='#E63946'; AMBER='#EF9F27'; BLUE='#378ADD'
BORD='#E2E8F1'; BORDEM='#C9D6E8'; GTINT='#F4F9F7'; BTINT='#EAF2FB'
plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','text.color':INK,
    'axes.edgecolor':BORDEM,'axes.labelcolor':INK,'xtick.color':INK,'ytick.color':INK,
    'font.size':13,'axes.titlesize':14})
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا')

# ---------- load corpus ----------
sura_ay=collections.defaultdict(list); ayahs=[]; spread=collections.defaultdict(set)
for line in open(f"{R}/research/two_books_genome/roots_by_ayah.tsv",encoding='utf-8'):
    line=line.rstrip('\n')
    if '\t' not in line: continue
    ref,rs=line.split('\t',1); su=int(ref.split(':')[0]); rl=[fa(x) for x in rs.split()]
    ayahs.append(set(rl)); sura_ay[su].append(rl)
    for r in rl: spread[r].add(su)
N=len(ayahs); cnt=collections.Counter(); co=collections.Counter(); deg=collections.Counter()
for s in ayahs:
    for r in s: cnt[r]+=1
    for a,b in itertools.combinations(sorted(s),2): co[(a,b)]+=1
for (a,b),c in co.items(): deg[a]+=1; deg[b]+=1
def pair(a,b): return co[(a,b)] if (a,b) in co else co[(b,a)]
idf=lambda r: math.log(114/len(spread[r]))
NAMES={108:'الكوثر',112:'الإخلاص',103:'العصر',110:'النصر',102:'التكاثر',106:'قريش',111:'المسد',113:'الفلق',93:'الضحى',114:'الناس',107:'الماعون',105:'الفيل',109:'الكافرون',1:'الفاتحة'}

# ===== FIG 19: bond demotion + encoder reproduction =====
fig,(axA,axB)=plt.subplots(1,2,figsize=(13.6,5.6),gridspec_kw={'width_ratios':[1,1.12]})
# A: percentile of batr-shani under three measures
meas=['PPMI','G²\n(Dunning)','t-score']; pcts=[99.8,97.2,79.0]; cols=[RED,AMBER,GREEN_DK]
bars=axA.bar(meas,pcts,color=cols,edgecolor='white',width=0.62,zorder=3)
axA.axhline(95,color=BORDEM,lw=1.4,ls='--',zorder=2); axA.text(2.46,95,' 95th',va='center',ha='left',fontsize=12,color=INK)
for b,p in zip(bars,pcts): axA.text(b.get_x()+b.get_width()/2,p+1.5,f"{p:.0f}",ha='center',fontsize=14,fontweight='bold',color=INK)
axA.set_ylim(0,108); axA.set_ylabel("percentile of the بتر–شنء bond\namong all 78,111 co-occurring pairs",fontsize=12.5)
axA.set_title(A("A · the bond collapses under count-sensitive measures"),loc='left',fontsize=13,fontweight='bold',color=NAVY)
for sp in ['top','right']: axA.spines[sp].set_visible(False)
axA.text(0.02,0.03,A("co-count = 1 (only verse 108:3) · split-half: present 48%\nنحر, بتر (count=1) have NO embedding → bond unreproducible"),
         transform=axA.transAxes,fontsize=11.5,color=INK,va='bottom',
         bbox=dict(boxstyle='round,pad=0.4',fc=GTINT,ec='#cfe4dc'))
# B: shani's real independent-encoder neighbourhood
nb=[('قلد',0.93),('عون',0.79),('صید',0.75),('جرم',0.58),('برر',0.53),('صدد',0.52)]
yy=np.arange(len(nb))[::-1]
axB.barh(yy,[v for _,v in nb],color=NAVY,edgecolor='white',height=0.6,zorder=3)
axB.set_yticks(yy); axB.set_yticklabels([A(w) for w,_ in nb],fontsize=15)
for y,(w,v) in zip(yy,nb): axB.text(v+0.012,y,f"{v:.2f}",va='center',fontsize=12.5,color=INK,fontweight='bold')
axB.set_xlim(0,1.05); axB.set_xlabel("cosine similarity to شنء in the independent SVD encoder".replace('شنء',''),fontsize=12.5)
axB.set_xlabel(A("cosine similarity to شنء in the independent encoder"),fontsize=12.5)
axB.set_title(A("B · شنء's real neighbourhood = al-Māʾida (5) legal/ritual vocab — not بتر"),loc='left',fontsize=13,fontweight='bold',color=NAVY)
for sp in ['top','right']: axB.spines[sp].set_visible(False)
axB.text(0.97,0.06,A("قلد=garlands · عون=help · صید=game\n(all 5:1–2 pilgrimage law)"),transform=axB.transAxes,
         ha='right',va='bottom',fontsize=11.5,color=INK,bbox=dict(boxstyle='round,pad=0.4',fc=BTINT,ec='#CFE0F2'))
fig.tight_layout(); fig.savefig(f"{OUT}/fig_v4_bond.png",dpi=150,bbox_inches='tight'); plt.close(fig); print("saved fig_v4_bond (F19)")

# ===== precompute per-sura features for F20/F21/F22 =====
feat={}
for su in range(1,115):
    uniq=sorted(set(r for rl in sura_ay[su] for r in rl)); nv=len(sura_ay[su])
    if not uniq: continue
    hd=sum(1 for r in uniq if cnt[r]==1)/nv
    mi=float(np.mean([idf(r) for r in uniq]))
    sup=float(np.mean([deg[r] for r in uniq]))
    feat[su]=dict(hd=hd,idf=mi,sup=sup,n=len(uniq),nv=nv)
sus=list(feat)
def zc(key):
    v=np.array([feat[s][key] for s in sus]); return dict(zip(sus,(v-v.mean())/v.std()))
zidf,zhd,zsup=zc('idf'),zc('hd'),zc('sup')
openness={s:zidf[s]+zhd[s]-zsup[s] for s in sus}

# fittingness z (reuse swap-test, only <=40 roots; fast set)
def assoc(a,b):
    c=pair(a,b); return max(0.0,math.log2(c*N/(cnt[a]*cnt[b]))) if c>0 and a!=b else 0.0
import bisect; byc=collections.defaultdict(list)
for r,c in cnt.items(): byc[c].append(r)
csort=sorted(byc); _pc={}
def matched(r,rng):
    c=cnt[r]
    if c not in _pc:
        lo=bisect.bisect_left(csort,max(1,int(c*0.5))); hi=bisect.bisect_right(csort,int(c*2)+1)
        _pc[c]=[x for k in csort[lo:hi] for x in byc[k]] or [r]
    return rng.choice(_pc[c])
def coh(rs):
    rs=[r for r in rs if r in cnt]
    return float(np.mean([assoc(a,b) for a,b in itertools.combinations(rs,2)])) if len(rs)>1 else 0.0
rng=random.Random(13); fitz={}
for su in sus:
    uniq=sorted(set(r for rl in sura_ay[su] for r in rl))
    if not(3<=len(uniq)<=40): continue
    Ca=coh(uniq); nl=[coh([matched(r,rng) for r in uniq]) for _ in range(150)]
    mu,sd=np.mean(nl),np.std(nl); fitz[su]=(Ca-mu)/sd if sd>0 else 0.0

# ===== FIG 20: cross-text fingerprint heatmap =====
quad=[108,112,103,110]; feats=['hapax / verse','mean idf\n(specificity)','fittingness z','openness\n(percentile)']
def opct(s): vals=list(openness.values()); return 100*sum(1 for x in vals if x<openness[s])/len(vals)
Mtx=np.array([[feat[s]['hd'],feat[s]['idf'],fitz.get(s,0),opct(s)] for s in quad])
# normalise each column 0..1 for colour
Mn=(Mtx-Mtx.min(0))/(np.ptp(Mtx,0)+1e-9)
fig,ax=plt.subplots(figsize=(9.2,4.5))
im=ax.imshow(Mn,cmap='YlGnBu',aspect='auto',vmin=0,vmax=1)
ax.set_xticks(range(4)); ax.set_xticklabels(feats,fontsize=12.5)
ax.set_yticks(range(4)); ax.set_yticklabels([A(NAMES[s]+f' ({s})') for s in quad],fontsize=14)
raw=[['%.2f'%feat[s]['hd'],'%.2f'%feat[s]['idf'],'%.1f'%fitz.get(s,0),'%.0f'%opct(s)] for s in quad]
for i in range(4):
    for j in range(4):
        ax.text(j,i,raw[i][j],ha='center',va='center',fontsize=13,fontweight='bold',
                color='white' if Mn[i,j]>0.55 else INK)
ax.set_title(A("Singularity is PARTICULAR: الكوثر & الإخلاص carry it; العصر & النصر do not — and only الكوثر is also OPEN"),
             loc='left',fontsize=12.5,fontweight='bold',color=NAVY)
for sp in ax.spines.values(): sp.set_visible(False)
ax.set_xticks(np.arange(-.5,4,1),minor=True); ax.set_yticks(np.arange(-.5,4,1),minor=True)
ax.grid(which='minor',color='white',lw=2); ax.tick_params(which='minor',length=0)
fig.tight_layout(); fig.savefig(f"{OUT}/fig_v4_crosstext.png",dpi=150,bbox_inches='tight'); plt.close(fig); print("saved fig_v4_crosstext (F20)")

# ===== FIG 21: singularity vs openness 2D map (flagship) =====
fig,ax=plt.subplots(figsize=(10.6,7.2))
xs=[feat[s]['idf'] for s in sus]; ys=[openness[s] for s in sus]
ax.scatter(xs,ys,s=26,color='#9fb0c4',alpha=0.55,zorder=2,edgecolors='none')
hi={108:(RED,15),112:(GREEN_DK,12),103:(BLUE,12),110:(AMBER,12),102:(NAVY,11),1:(NAVY,10)}
for s,(c,ms) in hi.items():
    if s in feat:
        ax.scatter([feat[s]['idf']],[openness[s]],s=ms*ms*1.7,color=c,zorder=4,edgecolors='white',linewidths=1.4)
        dy=0.5 if s not in(112,) else -0.9
        ax.annotate(A(NAMES[s]+f' ({s})'),(feat[s]['idf'],openness[s]),textcoords='offset points',
                    xytext=(8,8 if s!=112 else -16),fontsize=13.5,fontweight='bold',color=c)
ax.axhline(np.median(ys),color=BORDEM,lw=1,ls=':',zorder=1); ax.axvline(np.median(xs),color=BORDEM,lw=1,ls=':',zorder=1)
ax.set_xlabel("specificity →  mean idf of the sūra's content roots (rarer vocabulary)",fontsize=13)
ax.set_ylabel("openness →  internal under-determination score",fontsize=13)
ax.text(0.985,0.97,A("الكوثر: singular AND open (unique #1)"),transform=ax.transAxes,ha='right',va='top',
        fontsize=12.5,color=RED,fontweight='bold')
ax.text(0.985,0.06,A("الإخلاص: singular but ANCHORED (صمد is fixed)"),transform=ax.transAxes,ha='right',va='bottom',
        fontsize=12.5,color=GREEN_DK,fontweight='bold')
ax.set_title("Singularity ≠ openness: rare vocabulary need not be referentially open",loc='left',fontsize=13.5,fontweight='bold',color=NAVY)
for sp in ['top','right']: ax.spines[sp].set_visible(False)
fig.tight_layout(); fig.savefig(f"{OUT}/fig_v4_openmap.png",dpi=150,bbox_inches='tight'); plt.close(fig); print("saved fig_v4_openmap (F21)")

# ===== FIG 22: fittingness landscape (short suras) + regulative null =====
shortz=sorted(((s,fitz[s]) for s in fitz if feat[s]['n']<=15),key=lambda kv:kv[1])
fig,ax=plt.subplots(figsize=(10.4,5.8))
yy=np.arange(len(shortz)); vals=[v for _,v in shortz]
cols=[RED if s==108 else NAVY for s,_ in shortz]
ax.barh(yy,vals,color=cols,edgecolor='white',height=0.66,zorder=3)
ax.set_yticks(yy); ax.set_yticklabels([A(NAMES.get(s,str(s))+f' ({s})') for s,_ in shortz],fontsize=12.5)
for y,(s,v) in zip(yy,shortz): ax.text(v+0.1,y,f"{v:.1f}",va='center',fontsize=12,fontweight='bold',color=INK)
ax.axvline(0,color=INK,lw=1); ax.set_xlabel("word-by-word fittingness  z  (cohesion vs count-matched substitutes)",fontsize=13)
ax.set_title("Fittingness is real but a GENERAL short-sūra property — al-Kawthar is high, not uniquely so",loc='left',fontsize=12.8,fontweight='bold',color=NAVY)
for sp in ['top','right']: ax.spines[sp].set_visible(False)
ax.text(0.98,0.04,A("regulative-voice null: easing verbs do NOT\nconcentrate in Prophet-office sūras (p=0.99)"),
        transform=ax.transAxes,ha='right',va='bottom',fontsize=11.5,color=INK,
        bbox=dict(boxstyle='round,pad=0.4',fc=GTINT,ec='#cfe4dc'))
fig.tight_layout(); fig.savefig(f"{OUT}/fig_v4_fitting.png",dpi=150,bbox_inches='tight'); plt.close(fig); print("saved fig_v4_fitting (F22)")

# ===== FIG 23: elaboration refutation =====
nroots={s:feat[s]['n'] for s in feat}
def elab(t,s):
    sh=set(r for rl in sura_ay[t] for r in rl)&set(r for rl in sura_ay[s] for r in rl)
    return sum(idf(r) for r in sh)/nroots[t] if nroots.get(t) else 0
shorts=[s for s in range(1,115) if 3<=nroots.get(s,0)<=15]
toplen=[]; pairs=[]
for s in shorts:
    rk=sorted((t for t in range(1,115) if t!=s and nroots.get(t,0)>0),key=lambda t:-elab(t,s))
    toplen.append(nroots[rk[0]]); pairs.append((s,rk[0]))
fig,ax=plt.subplots(figsize=(10.4,5.8))
yy=np.arange(len(shorts))
ax.barh(yy,toplen,color=[RED if s==108 else NAVY for s in shorts],edgecolor='white',height=0.66,zorder=3)
ax.set_yticks(yy); ax.set_yticklabels([A(NAMES.get(s,str(s))+f' ({s})') for s in shorts],fontsize=12.5)
allmean=np.mean([nroots[t] for t in range(1,115) if nroots.get(t,0)>0])
ax.axvline(allmean,color=AMBER,lw=2.2,ls='--',zorder=4); ax.text(allmean+2,len(shorts)-0.5,f" random sūra mean = {allmean:.0f} roots",color=INK,fontsize=12,va='top')
for y,(s,t) in zip(yy,pairs): ax.text(toplen[shorts.index(s)]+1,y,A(NAMES.get(t,str(t))),va='center',fontsize=11.5,color=INK)
ax.set_xlabel("size (#roots) of each short sūra's TOP length-normalised elaborator",fontsize=13)
ax.set_title("'Long elaborates short' is NOT systematic: every top elaborator is itself short (p=1.0); al-Kawthar↔al-Ḍuḥā",loc='left',fontsize=12.3,fontweight='bold',color=NAVY)
for sp in ['top','right']: ax.spines[sp].set_visible(False)
fig.tight_layout(); fig.savefig(f"{OUT}/fig_v4_elab.png",dpi=150,bbox_inches='tight'); plt.close(fig); print("saved fig_v4_elab (F23)")
print("ALL V4 FIGS DONE")
