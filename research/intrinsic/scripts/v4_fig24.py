# -*- coding: utf-8 -*-
"""F24 — the concept-coining typology of the short suras (distinct vs shared hapax)."""
import collections, itertools
import numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import re as _re, arabic_reshaper
from bidi.algorithm import get_display
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"; OUT=f"{R}/research/intrinsic/kawthar_figs"
_resh=arabic_reshaper.ArabicReshaper(configuration={'delete_harakat':True,'support_ligatures':False})
_AR=_re.compile(r'[؀-ۿݐ-ݿ]+')
def A(s): return _AR.sub(lambda m:get_display(_resh.reshape(m.group().replace('ک','ك').replace('ی','ي'))),s)
INK='#10243A';NAVY='#1D3557';GREEN_DK='#0F6E56';RED='#E63946';AMBER='#EF9F27';BORDEM='#C9D6E8';GREY='#9fb0c4'
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':INK,'axes.edgecolor':BORDEM,'font.size':13})
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا')
sura_ay=collections.defaultdict(list); ayahs=[]; spread=collections.defaultdict(set)
for line in open(f"{R}/research/two_books_genome/roots_by_ayah.tsv",encoding='utf-8'):
    line=line.rstrip('\n')
    if '\t' not in line: continue
    ref,rs=line.split('\t',1); su=int(ref.split(':')[0]); rl=[fa(x) for x in rs.split()]
    ayahs.append(set(rl)); sura_ay[su].append(rl)
    for r in rl: spread[r].add(su)
cnt=collections.Counter(); co=collections.Counter()
for s in ayahs:
    for r in s: cnt[r]+=1
    for a,b in itertools.combinations(sorted(s),2): co[(a,b)]+=1
hapax=[r for r in cnt if cnt[r]==1]
def rare_ctx(r):
    ctx=set()
    for (a,b),c in co.items():
        o=b if a==r else (a if b==r else None)
        if o and len(spread[o])<=20: ctx.add(o)
    return ctx
hctx={r:rare_ctx(r) for r in hapax}; owners=collections.defaultdict(set)
for r,cx in hctx.items():
    for o in cx: owners[o].add(r)
def distinct(r): return all(len(owners[o])<=1 for o in hctx[r])
NM={108:'الكوثر',112:'الإخلاص',113:'الفلق',105:'الفيل',106:'قريش',111:'المسد',97:'القدر',103:'العصر',110:'النصر',109:'الكافرون',114:'الناس'}
shorts=[su for su in range(1,115) if len(sura_ay[su])<=6 and any(sura_ay[su])]
rows=[]
for su in shorts:
    uniq=sorted(set(r for rl in sura_ay[su] for r in rl)); hpx=[r for r in uniq if cnt[r]==1]
    dist=[r for r in hpx if distinct(r)]
    rows.append((su,len(dist),len(hpx)-len(dist),hpx,dist))
rows.sort(key=lambda r:(r[1],r[2]))
fig,ax=plt.subplots(figsize=(11,6.2))
yy=np.arange(len(rows))
for i,(su,nd,no,hpx,dist) in enumerate(rows):
    ax.barh(i,nd,color=(RED if su in(108,112) else GREEN_DK),edgecolor='white',height=0.6,zorder=3)
    if no: ax.barh(i,no,left=nd,color=AMBER,edgecolor='white',height=0.6,zorder=3)
    lbl=" ".join(A(r) for r in (hpx or ['—']))
    ax.text(max(nd+no,0)+0.06,i,lbl,va='center',fontsize=13,color=INK)
ax.set_yticks(yy); ax.set_yticklabels([A(NM.get(su,str(su))+f' ({su})') for su,*_ in rows],fontsize=13)
ax.set_xlim(0,3.2); ax.set_xlabel("number of hapax in the sūra  (green/red = referentially DISTINCT · amber = shared-context)",fontsize=12.5)
ax.set_title("A concept-coining typology of the short sūras: al-Kawthar & al-Ikhlāṣ alone carry TWO distinct hapax",loc='left',fontsize=12.6,fontweight='bold',color=NAVY)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(fc=RED,label=A('doubly concept-coining (الكوثر، الإخلاص)')),Patch(fc=GREEN_DK,label='one distinct hapax'),Patch(fc=AMBER,label='object-hapax (shared context)')],loc='lower right',fontsize=11.5,frameon=True,edgecolor=BORDEM)
for sp in ['top','right']: ax.spines[sp].set_visible(False)
ax.set_xticks([0,1,2,3])
fig.tight_layout(); fig.savefig(f"{OUT}/fig_v4_coining.png",dpi=150,bbox_inches='tight'); plt.close(fig)
print("saved fig_v4_coining (F24); rows:",[(su,nd,no) for su,nd,no,_,_ in rows])
