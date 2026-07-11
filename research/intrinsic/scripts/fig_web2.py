# -*- coding: utf-8 -*-
"""Chronology WEB v2: 9 parallel threads, Arabic on every thread, overlaps eliminated (>=12px labels,
2-tier staggering, lane labels in a left margin). Adds the Prophet's-household thread."""
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import re, arabic_reshaper
from bidi.algorithm import get_display
_resh=arabic_reshaper.ArabicReshaper(configuration={'delete_harakat':False,'support_ligatures':False})
_AR=re.compile(r'[؀-ۿ]+')
def A(s): return _AR.sub(lambda m:get_display(_resh.reshape(m.group().replace('ک','ك').replace('ی','ي'))),s)
INK='#10243A';NAVY='#1D3557';GREEN_DK='#0F6E56';RED='#E63946';AMBER='#EF9F27';BLUE='#378ADD';PURP='#7A5AA6';TEAL='#2A7D8C';BORD='#E2E8F1';GTINT='#F4F9F7';BTINT='#EAF2FB'
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':INK})
fig,ax=plt.subplots(figsize=(17,12))
# lanes: (y, colour, english, arabic)
LAN=[('Events / community',13.5,NAVY,'الأحداث والجماعة'),
     ('Prophet household',12.0,PURP,'أزواج النبي وأهل البيت'),
     ('Ruling: khamr',10.5,GREEN_DK,'حكم الخمر'),
     ('Ruling: qitāl',9.0,GREEN_DK,'حكم القتال'),
     ('Ruling: ribā',7.5,GREEN_DK,'حكم الربا'),
     ('Referent groups',6.0,BLUE,'الفئات المخاطَبة'),
     ('Warning ↔ tidings',4.5,AMBER,'النذير والبشير'),
     ('Heaven ↔ hell',3.0,RED,'الجنة والنار'),
     ('Ritual + promise',1.5,TEAL,'الشعائر والوعد')]
LY={n:(y,c) for n,y,c,a in LAN}
# nodes: (lane, x, label-en, label-ar)
N=[('Events / community',0,'Hijra','الهجرة'),('Events / community',2,'Badr','بدر'),('Events / community',3,'Uhud','أحد'),
   ('Events / community',4,'Banū Naḍīr','بنو النضير'),('Events / community',5,'Khandaq','الخندق'),('Events / community',6,'Ḥudaybiyya','الحديبية'),
   ('Events / community',8,'Conquest','الفتح'),('Events / community',9,'Tabūk','تبوك'),('Events / community',10,'Farewell','الوداع'),
   ('Prophet household',5,'Zayd 33:37','زيد'),('Prophet household',5.4,'ḥijāb 33:53','الحجاب'),('Prophet household',6,'ifk 24:11','الإفك'),('Prophet household',7.2,'taḥrīm 66:1','التحريم'),
   ('Ruling: khamr',-1.5,'provision 16:67','إباحة'),('Ruling: khamr',2,'sin&benefit 2:219','إثم ومنافع'),('Ruling: khamr',4.5,'no-pray 4:43','لا تقربوا'),('Ruling: khamr',9.5,'prohibition 5:90','تحريم'),
   ('Ruling: qitāl',-1.5,'restraint','كفّ'),('Ruling: qitāl',2.5,'permission 22:39','أُذن'),('Ruling: qitāl',3.5,'prescribed 2:216','كُتب'),('Ruling: qitāl',9,'unrestricted 9:5','قاتلوا'),
   ('Ruling: ribā',-1.5,'neutral 30:39','محايد'),('Ruling: ribā',2.5,'prohibition 2:275','حُرّم'),('Ruling: ribā',3.5,'no-devour 3:130','لا تأكلوا'),
   ('Referent groups',-2.5,'deniers','المكذّبون'),('Referent groups',-1.5,'polytheists','المشركون'),('Referent groups',1,'hypocrites','المنافقون'),('Referent groups',2.5,'people of Book','أهل الكتاب'),('Referent groups',8.5,'Christians','النصارى'),
   ('Warning ↔ tidings',-2.5,'pure warning','إنذار'),('Warning ↔ tidings',-0.5,'balance','توازن'),('Warning ↔ tidings',6,'tidings rise','بشارة'),
   ('Heaven ↔ hell',-2.5,'hell-heavy 57%','نار'),('Heaven ↔ hell',4,'balanced 44%','توازن'),
   ('Ritual + promise',-2,'al-Ḍuḥā 93:5','الضحى'),('Ritual + promise',-1,'al-Kawthar 108:1','الكوثر'),('Ritual + promise',2,'qibla→Mecca','القبلة'),('Ritual + promise',6,'ḥajj 2:196','الحج'),('Ritual + promise',10,'ḥajj complete','إتمام')]
ax.axvspan(-3.0,-0.2,color=GTINT,zorder=0); ax.axvspan(-0.2,10.8,color=BTINT,zorder=0)
ax.text(-1.6,14.4,'MECCA',ha='center',fontsize=14,color=NAVY,fontweight='bold')
ax.text(5,14.4,A('المدينة')+'  ·  MEDINA (AH 0–10)',ha='center',fontsize=14,color=NAVY,fontweight='bold')
for xw,lab in [(2,'~2 AH'),(6,'~6 AH'),(9,'~9 AH')]:
    ax.axvline(xw,color=BORD,lw=11,alpha=0.4,zorder=0); ax.text(xw,0.55,lab,ha='center',fontsize=12.5,color=INK,fontweight='bold')
# lane labels in left margin (no node overlap; nodes start x=-2.5)
for n,y,c,ar in LAN:
    ax.text(-4.7,y+0.12,n,ha='left',va='center',fontsize=13,color=c,fontweight='bold')
    ax.text(-4.7,y-0.34,A(ar),ha='left',va='center',fontsize=12,color=c)
pos={}
# 2-tier staggered labels per lane to avoid horizontal-neighbour overlap
from collections import defaultdict
bylane=defaultdict(list)
for lane,x,en,ar in N: bylane[lane].append((x,en,ar))
for lane,items in bylane.items():
    y0=LY[lane][0]; col=LY[lane][1]
    for k,(x,en,ar) in enumerate(sorted(items)):
        pos[(lane,en)]=(x,y0)
        ax.scatter([x],[y0],s=130,color=col,zorder=4,edgecolors='white',linewidths=1.4)
        dy=0.30 if k%2==0 else 0.62
        ax.text(x,y0+dy,en,ha='center',va='bottom',fontsize=12,color=col,fontweight='bold',zorder=6)
        ax.text(x,y0+dy-0.0,'',fontsize=1)
        ax.text(x,y0-0.30 if k%2==0 else y0-0.55,A(ar),ha='center',va='top',fontsize=12,color=col,zorder=6)
def arrow(lane,a,b):
    if (lane,a) in pos and (lane,b) in pos:
        ax.add_patch(FancyArrowPatch(pos[(lane,a)],pos[(lane,b)],arrowstyle='-|>',mutation_scale=12,lw=1.8,color=LY[lane][1],alpha=0.75,zorder=3,shrinkA=8,shrinkB=8))
THr={'Events / community':['Hijra','Badr','Uhud','Banū Naḍīr','Khandaq','Ḥudaybiyya','Conquest','Tabūk','Farewell'],
 'Prophet household':['Zayd 33:37','ḥijāb 33:53','ifk 24:11','taḥrīm 66:1'],
 'Ruling: khamr':['provision 16:67','sin&benefit 2:219','no-pray 4:43','prohibition 5:90'],
 'Ruling: qitāl':['restraint','permission 22:39','prescribed 2:216','unrestricted 9:5'],
 'Ruling: ribā':['neutral 30:39','prohibition 2:275','no-devour 3:130'],
 'Referent groups':['deniers','polytheists','hypocrites','people of Book','Christians'],
 'Warning ↔ tidings':['pure warning','balance','tidings rise'],
 'Heaven ↔ hell':['hell-heavy 57%','balanced 44%'],
 'Ritual + promise':['al-Ḍuḥā 93:5','al-Kawthar 108:1','qibla→Mecca','ḥajj 2:196','ḥajj complete']}
for lane,seq in THr.items():
    for a,b in zip(seq,seq[1:]): arrow(lane,a,b)
ax.set_xlim(-4.8,11.4); ax.set_ylim(0,15.0); ax.set_yticks([])
ax.set_xticks([-2.5,-1,0,2,3,4,5,6,8,9,10]); ax.set_xticklabels(['early\nMecca','late\nMecca','Hijra','2','3','4','5','6','8','9','10'],fontsize=12,color=INK)
for s in ['top','right','left']: ax.spines[s].set_visible(False)
ax.spines['bottom'].set_color(BORD)
ax.set_xlabel('revealed time →   ·   vertical bands = contemporaneity windows (parallel threads share a time, not a sequence)',fontsize=13,color=INK)
ax.set_title('The chronology web (الشبكة الزمنية): parallel threads braided through shared time-windows',loc='left',fontsize=18,fontweight='bold',color=NAVY,pad=14)
fig.tight_layout(); fig.savefig('research/intrinsic/chrono_figs/chronology_web.png',dpi=145,bbox_inches='tight'); print('saved chronology_web.png (9 threads, Arabic, spaced)')
