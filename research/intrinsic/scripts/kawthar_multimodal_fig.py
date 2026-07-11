# -*- coding: utf-8 -*-
"""Figure 18: multimodal distinctiveness — two INDEPENDENT, length-validated channels (lexical rare-root density
x graphemic rare-bigram density). al-Kawthar at the joint extreme. Phonological/info-density rejected (length artifacts)."""
import json,re,math,collections,statistics as st
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
import numpy as np, arabic_reshaper
from bidi.algorithm import get_display
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"; OUT=f"{R}/research/intrinsic/kawthar_figs"
_resh=arabic_reshaper.ArabicReshaper(configuration={'delete_harakat':True,'support_ligatures':False})
_AR=re.compile('[؀-ۿݐ-ݿ]+')
def A(s): return _AR.sub(lambda m: get_display(_resh.reshape(m.group().replace('ک','ك').replace('ی','ي'))), s)
fa2=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا')
INK='#10243A';NAVY='#1D3557';GREEN='#1D9E75';GREEN_DK='#0F6E56';RED='#E63946';BORD='#E2E8F1';GREY='#9fb0c4'
plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','text.color':INK})
ar=json.load(open(f"{R}/arabic.json",encoding='utf-8'))
DIAC=re.compile(r'[ً-ْٰـ]')
def rasm(s): return fa2(DIAC.sub('',s))
sur_txt=collections.defaultdict(str); sur_nv=collections.Counter()
for k,t in ar.items():
    s,a=map(int,k.split(':')); w=t.split()
    if a==1 and s not in(1,9): w=w[4:]
    sur_txt[s]+=''.join(ch for ch in rasm(''.join(w)) if '؀'<=ch<='ۿ'); sur_nv[s]+=1
suras=sorted(sur_txt)
bg=collections.defaultdict(set)
for s,t in sur_txt.items():
    for i in range(len(t)-1): bg[t[i:i+2]].add(s)
rare={b for b,ss in bg.items() if len(ss)<=2}
gra={s:sum(1 for i in range(len(sur_txt[s])-1) if sur_txt[s][i:i+2] in rare)/max(1,len(sur_txt[s])-1) for s in suras}
vroots={}
for line in open(f"{R}/research/two_books_genome/roots_by_ayah.tsv",encoding='utf-8'):
    if '\t' in line: kk,rs=line.split('\t',1); vroots[kk]=[fa2(x) for x in rs.split()]
rc=collections.Counter(r for rs in vroots.values() for r in rs); rhap={r for r,c in rc.items() if c==1}
lex={s:sum(1 for k,rs in vroots.items() if int(k.split(':')[0])==s for r in rs if r in rhap)/sur_nv[s] for s in suras}
fig,ax=plt.subplots(figsize=(9.4,6.4))
xs=[lex[s] for s in suras]; ys=[gra[s] for s in suras]
ax.scatter(xs,ys,s=26,color=GREY,alpha=0.6,zorder=2,edgecolors='none')
ax.scatter([lex[108]],[gra[108]],s=200,color=RED,zorder=5,edgecolors='white',linewidths=1.5)
ax.annotate(A("الکوثر (108)\n97th pct lexical · 98th pct graphemic\n(length-matched nulls)"),(lex[108],gra[108]),
            xytext=(lex[108]-0.42,gra[108]-0.004),fontsize=12,color=RED,fontweight='bold',ha='left',
            arrowprops=dict(arrowstyle='->',color=RED,lw=1.4))
# label a few runners-up
for s in [112,106,94]:
    ax.annotate(f"{s}",(lex[s],gra[s]),xytext=(lex[s]+0.01,gra[s]),fontsize=11,color=NAVY)
ax.set_xlabel("LEXICAL channel  →  rare-root (hapax) density per verse",fontsize=12,color=GREEN_DK)
ax.set_ylabel("GRAPHEMIC channel  →  rare letter-bigram density",fontsize=12,color=NAVY)
ax.set_title("Figure 18.  Distinctiveness is two-dimensional and convergent. al-Kawthar sits at the joint extreme of\n"
             "two INDEPENDENT channels (r=0.38) - rare words and rare letter-pairs - each surviving its own\n"
             "length-matched null. (Phonological entropy & compressibility were rejected as length artifacts.)",
             loc='left',fontsize=11.5,color=NAVY,fontweight='bold')
for sp in ['top','right']: ax.spines[sp].set_visible(False)
ax.grid(color=BORD,lw=0.8,zorder=0)
fig.tight_layout(); fig.savefig(f"{OUT}/fig_multimodal.png",dpi=150,bbox_inches='tight'); fig.savefig(f"{OUT}/fig_multimodal.svg",bbox_inches='tight'); plt.close(fig)
print("saved fig_multimodal (F18)")
