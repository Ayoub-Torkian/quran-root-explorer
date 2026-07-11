# -*- coding: utf-8 -*-
"""#2 Community-formation timeline: when each REFERENT enters revealed time + prophet deployment.
Locked UI: >=12px, ink #10243A, navy #1D3557, green #1D9E75, tints; no grey text."""
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np, re, openpyxl, arabic_reshaper
from bidi.algorithm import get_display
from collections import defaultdict
OUT="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2/research/intrinsic/chrono_figs"
_resh=arabic_reshaper.ArabicReshaper(configuration={'delete_harakat':False,'support_ligatures':False})
_AR=re.compile(r'[؀-ۿݐ-ݿ]+')
def A(s): return _AR.sub(lambda m:get_display(_resh.reshape(m.group().replace('ک','ك').replace('ی','ي'))),s)
INK='#10243A';NAVY='#1D3557';GREEN='#1D9E75';GREEN_DK='#0F6E56';RED='#E63946';AMBER='#EF9F27';BLUE='#378ADD'
BORD='#E2E8F1';GTINT='#F4F9F7';BTINT='#EAF2FB'
def norm(s): return (s or '').replace('ي','ی').replace('ك','ک').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ة','ه')
wb=openpyxl.load_workbook("Book6.xlsx",read_only=True); ws=wb['Sheet1']
A_=[]
for row in ws.iter_rows(min_row=9,values_only=True):
    try: su,ay=int(row[5]),int(row[6])
    except: continue
    A_.append(dict(su=su,nuzul=int(row[12]),toks=[norm(t) for t in (row[9]or'').split()],surf=[norm(t) for t in (row[10]or'').split()]))
def hs(s,seq):
    L=len(seq); return any(s[i:i+L]==seq for i in range(len(s)-L+1))
def lem(tk,*p): return any(any(t.startswith(x) for x in p) for t in tk)
GROUPS=[
 ('Meccan deniers',   'المکذّبون',  lambda d: hs(d['surf'],['الذین','کذب']) or lem(d['toks'],'مکذب','مستکبر')),
 ('Polytheists',      'المشرکون',   lambda d: lem(d['toks'],'مشرک')),
 ('Disbelievers',     'الذین کفروا',lambda d: hs(d['surf'],['الذین','کفر']) or lem(d['toks'],'کافر') or 'کفار' in d['toks']),
 ('Believers',        'الذین آمنوا',lambda d: hs(d['surf'],['الذین','امن']) or lem(d['toks'],'مؤمن','مومن','مسلم')),
 ('People of Book',   'أهل الکتاب', lambda d: hs(d['surf'],['اهل','ال','کتاب']) or hs(d['surf'],['الذین','هاد']) or lem(d['toks'],'یهود','نصار')),
 ('Hypocrites',       'المنافقون',  lambda d: lem(d['toks'],'منافق') or hs(d['surf'],['قلوب','هم','مرض'])),
]
data={}
for en,ar,fn in GROUPS:
    nz=sorted(d['nuzul'] for d in A_ if fn(d)); data[en]=(ar,nz)
order=sorted(GROUPS,key=lambda g:np.median(data[g[0]][1]))  # by median emergence

fig,(ax,ax2)=plt.subplots(2,1,figsize=(13.2,8.6),gridspec_kw={'height_ratios':[1.25,1]})
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':INK})
# era bands
for x0,x1,c,lab in [(1,38,GTINT,'EARLY Meccan'),(38,77,BTINT,'MID Meccan'),(77,114,'#FBEEDD','LATE / Medinan')]:
    ax.axvspan(x0,x1,color=c,zorder=0); ax.text((x0+x1)/2,len(order)+0.35,lab,ha='center',fontsize=12.5,color=NAVY,fontweight='bold')
for i,(en,ar,fn) in enumerate(order):
    ar_,nz=data[en]; y=len(order)-1-i
    lo,hi,med=min(nz),max(nz),int(np.median(nz))
    # span line + density dots
    ax.plot([lo,hi],[y,y],color=BORD,lw=2,zorder=1,solid_capstyle='round')
    ax.scatter(nz,[y]*len(nz),s=14,color=NAVY,alpha=0.28,zorder=2,edgecolors='none')
    late=sum(x>77 for x in nz)/len(nz)
    col=GREEN_DK if med>77 else (BLUE if med>38 else AMBER)
    ax.scatter([med],[y],s=240,color=col,zorder=4,edgecolors='white',linewidths=1.6)
    ax.text(med,y,f"{med}",ha='center',va='center',fontsize=11.5,color='white',fontweight='bold',zorder=5)
    ax.text(0,y,f"{en}",ha='right',va='center',fontsize=13,color=NAVY,fontweight='bold')
    ax.text(-0.5,y,'',ha='right')
    ax.text(116,y,A(ar_)+f"  ·  {late:.0%} late",ha='left',va='center',fontsize=12.5,color=col,fontweight='bold')
ax.set_xlim(-30,150); ax.set_ylim(-0.7,len(order)+0.9); ax.set_yticks([])
ax.set_xticks([1,20,40,60,80,100,114]); ax.tick_params(labelsize=12,colors=INK)
for s in ['top','right','left']: ax.spines[s].set_visible(False)
ax.spines['bottom'].set_color(BORD)
ax.set_xlabel("revelation order (nuzūl rank, 1 → 114)  · dot = median emergence",fontsize=12.5,color=INK)
ax.set_title("Community formation: when each referent enters revealed time",loc='left',fontsize=18,fontweight='bold',color=NAVY,pad=26)

# Panel B: prophets — historical order (y) vs revelation time (x)
PRO=[('Adam','ادم',['ادم']),('Noah','نوح',['نوح']),('Hud','هود',['هود']),('Salih','صالح',['صالح']),
 ('Abraham','ابراهیم',['ابراهیم','ابرهیم']),('Lot','لوط',['لوط']),('Joseph','یوسف',['یوسف']),
 ('Moses','موسی',['موسی','موس']),('David','داود',['داود']),('Solomon','سلیمان',['سلیمان']),
 ('Jesus','عیسی',['عیسی','عیس']),('Muhammad','محمد',['محمد','احمد'])]
for j,(en,ar,pats) in enumerate(PRO):
    y=len(PRO)-1-j
    nz=[d['nuzul'] for d in A_ if any(any(t.startswith(p) for p in pats) for t in d['toks'])]
    if not nz: continue
    med=int(np.median(nz)); n=len(nz)
    col=GREEN_DK if med>77 else (BLUE if med>38 else AMBER)
    ax2.plot([min(nz),max(nz)],[y,y],color=BORD,lw=1.6,zorder=1)
    ax2.scatter([med],[y],s=60+n*7,color=col,zorder=3,edgecolors='white',linewidths=1.3)
    ax2.text(-2,y,f"{en}",ha='right',va='center',fontsize=12.5,color=NAVY,fontweight='bold')
ax2.annotate("Moses among the earliest",(49,len(PRO)-1-7),(20,len(PRO)-1-7+0.9),fontsize=12,color=AMBER,
             fontweight='bold',arrowprops=dict(arrowstyle='->',color=AMBER,lw=1.6))
ax2.annotate("Jesus / Muhammad latest",(92,len(PRO)-1-10),(60,len(PRO)-1-10-0.9),fontsize=12,color=GREEN_DK,
             fontweight='bold',arrowprops=dict(arrowstyle='->',color=GREEN_DK,lw=1.6))
ax2.set_xlim(-28,120); ax2.set_ylim(-1,len(PRO)); ax2.set_yticks([])
ax2.set_xticks([1,20,40,60,80,100,114]); ax2.tick_params(labelsize=12,colors=INK)
for s in ['top','right','left']: ax2.spines[s].set_visible(False)
ax2.spines['bottom'].set_color(BORD)
ax2.set_xlabel("revelation order (nuzūl rank) →   ·   y-axis = fixed historical order (Adam→Muhammad)",fontsize=12.5,color=INK)
ax2.set_title("Prophets: historical order (down) is NOT the revelation order (across)",loc='left',fontsize=15,fontweight='bold',color=NAVY,pad=12)
fig.tight_layout(); fig.savefig(f"{OUT}/community_timeline.png",dpi=150,bbox_inches='tight'); print("saved",f"{OUT}/community_timeline.png")
