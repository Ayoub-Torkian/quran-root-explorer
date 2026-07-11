# -*- coding: utf-8 -*-
"""Static paper figure — bidi FIX (whole Arabic run), Qurʾanic-only Arabic, wider spacing, raised banner."""
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import re, arabic_reshaper
from bidi.algorithm import get_display
from collections import defaultdict
_resh=arabic_reshaper.ArabicReshaper(configuration={'delete_harakat':False,'support_ligatures':False})
_AR=re.compile(r'[؀-ۿ]+(?:\s+[؀-ۿ]+)*')
def A(s):
    if not s: return s
    return _AR.sub(lambda m:get_display(_resh.reshape(m.group().replace('ک','ك').replace('ی','ي'))),s)
INK='#10243A';NAVY='#1D3557';BORD='#E2E8F1';GTINT='#F4F9F7';BTINT='#EAF2FB'
TH=[('events','Events / community','الأحداث','#1D3557'),('house','Prophet household','أزواج النبي','#9B5DE5'),
 ('family','Family law','أحكام الأسرة','#B5651D'),('khamr','Ruling: khamr','الخمر','#0F6E56'),
 ('qital','Ruling: qitāl','القتال','#F3722C'),('riba','Ruling: ribā','الربا','#2A7D8C'),
 ('ref','Referent groups','الفئات','#378ADD'),('warn','Warning ↔ tidings','النذير والبشير','#EF9F27'),
 ('hh','Heaven ↔ hell','الجنة والنار','#E63946'),('ritual','Ritual + promise','الشعائر','#6D597A')]
C={t[0]:t[3] for t in TH}
N=[('events',0,'Hijra','هاجروا'),('events',1.9,'Badr','بدر'),('events',2.3,'captives','أسرى'),('events',3,'Uhud','القرح'),
   ('events',4,'Banū Naḍīr','الحشر'),('events',5,'Khandaq','الأحزاب'),('events',6,'Ḥudaybiyya','فتح'),
   ('events',8,'Conquest','نصر'),('events',9,'Tabūk','انفروا'),('events',9.4,'delegations','أفواجاً'),('events',10,'Farewell','أكملت'),
   ('house',4.9,'Zayd 33:37','زيد'),('house',5.5,'ḥijāb 33:53','حجاب'),('house',6.1,'ifk 24:11','الإفك'),('house',7.5,'taḥrīm 66:1','تحرّم'),
   ('family',3.5,'inherit 4:11','يوصيكم'),('family',5.4,'liʿān 24:6','يرمون'),('family',6.6,'dhihār 58:2','يظاهرون'),
   ('khamr',-1.5,'provision 16:67','سكراً'),('khamr',2,'sin&benefit 2:219','إثم'),('khamr',4.5,'no-pray 4:43','لا تقربوا'),('khamr',9.5,'prohibition 5:90','اجتنبوا'),
   ('qital',-1.5,'restraint 4:77','كفّوا'),('qital',2.4,'permission 22:39','أُذن'),('qital',3.6,'prescribed 2:216','كُتب'),('qital',9,'unrestricted 9:5','فاقتلوا'),
   ('riba',-1.5,'neutral 30:39','ربا'),('riba',2.5,'prohibition 2:275','حرّم'),('riba',3.7,'no-devour 3:130','لا تأكلوا'),
   ('ref',-2.5,'deniers','المكذّبون'),('ref',-1.5,'polytheists','المشركون'),('ref',1,'hypocrites','المنافقون'),('ref',2.5,'people of Book','أهل الكتاب'),('ref',8.5,'Christians','النصارى'),
   ('warn',-2.5,'pure warning','نذير'),('warn',-0.5,'balance',''),('warn',6,'tidings rise','بشير'),
   ('hh',-2.5,'hell-heavy 57%','نار'),('hh',4,'paradise rises','جنّة'),
   ('ritual',-2,'al-Ḍuḥā 93','الضحى'),('ritual',-1,'al-Kawthar 108','الكوثر'),('ritual',1.9,'fasting 2:183','الصيام'),('ritual',2.8,'qibla 2:144','قبلة'),('ritual',6,'ḥajj 2:196','الحج'),('ritual',10,'complete 5:3','أكملت')]
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':INK})
fig,ax=plt.subplots(figsize=(19,14))
step=1.7; ytop=len(TH)*step
laneY={t[0]:ytop-i*step for i,t in enumerate(TH)}
ax.axvspan(-3.0,-0.2,color=GTINT,zorder=0); ax.axvspan(-0.2,10.8,color=BTINT,zorder=0)
ax.text(-1.6,ytop+1.45,'MECCA',ha='center',fontsize=15,color=NAVY,fontweight='bold')
ax.text(5,ytop+1.45,'MEDINA (AH 0–10) · '+A('المدينة'),ha='center',fontsize=15,color=NAVY,fontweight='bold')
for xw,lab in [(2,'~2 AH'),(6,'~6 AH'),(9,'~9 AH')]:
    ax.axvline(xw,color=BORD,lw=12,alpha=0.4,zorder=0); ax.text(xw,0.4,lab,ha='center',fontsize=13,color=INK,fontweight='bold')
for tid,en,ar,c in TH:
    y=laneY[tid]; ax.text(-4.9,y+0.16,en,ha='left',va='center',fontsize=13,color=c,fontweight='bold')
    ax.text(-4.9,y-0.34,A(ar),ha='left',va='center',fontsize=12.5,color=c)
pos={}; bylane=defaultdict(list)
for lane,x,en,ar in N: bylane[lane].append((x,en,ar))
for lane,items in bylane.items():
    y0=laneY[lane]; col=C[lane]
    for k,(x,en,ar) in enumerate(sorted(items)):
        pos[(lane,en)]=(x,y0); ax.scatter([x],[y0],s=130,color=col,zorder=4,edgecolors='white',linewidths=1.4)
        ax.text(x,y0+(0.32 if k%2==0 else 0.66),en,ha='center',va='bottom',fontsize=12,color=col,fontweight='bold',zorder=6)
        if ar: ax.text(x,y0-(0.32 if k%2==0 else 0.62),A(ar),ha='center',va='top',fontsize=12.5,color=col,zorder=6)
def arrow(lane,a,b):
    if (lane,a) in pos and (lane,b) in pos:
        ax.add_patch(FancyArrowPatch(pos[(lane,a)],pos[(lane,b)],arrowstyle='-|>',mutation_scale=11,lw=1.7,color=C[lane],alpha=0.7,zorder=3,shrinkA=8,shrinkB=8))
SEQ=defaultdict(list)
for lane,x,en,ar in N: SEQ[lane].append((x,en))
for lane,items in SEQ.items():
    s=[en for x,en in sorted(items)]
    for a,b in zip(s,s[1:]): arrow(lane,a,b)
ax.set_xlim(-5.0,11.4); ax.set_ylim(0,ytop+2.2); ax.set_yticks([])
ax.set_xticks([-2.5,-1,0,2,3,4,5,6,8,9,10]); ax.set_xticklabels(['early\nMecca','late\nMecca','Hijra','2','3','4','5','6','8','9','10'],fontsize=12,color=INK)
for s in ['top','right','left']: ax.spines[s].set_visible(False)
ax.spines['bottom'].set_color(BORD)
ax.set_xlabel('revealed time →   ·   vertical bands = contemporaneity windows (parallel threads share a time, not a sequence)',fontsize=13,color=INK)
ax.set_title('The chronology web ('+A('الشبكة الزمنية')+'): 10 parallel threads braided through shared time-windows',loc='left',fontsize=18,fontweight='bold',color=NAVY,pad=18)
fig.tight_layout(); fig.savefig('research/intrinsic/chrono_figs/chronology_web.png',dpi=140,bbox_inches='tight'); print('saved (bidi-fixed, Quranic-only Arabic)')
