# -*- coding: utf-8 -*-
"""Braided temporal GRAPH: time on x (Meccan eras -> AH 0-10), parallel developmental THREADS as lanes,
contemporaneity = vertical alignment. Replaces the implicit 'line' with the partial-order graph. Locked UI."""
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
INK='#10243A';NAVY='#1D3557';GREEN='#1D9E75';GREEN_DK='#0F6E56';RED='#E63946';AMBER='#EF9F27';BLUE='#378ADD';BORD='#E2E8F1';GTINT='#F4F9F7';BTINT='#EAF2FB'
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':INK})
fig,ax=plt.subplots(figsize=(13.6,7.4))
# lanes (y) and their colour
lanes={'Events / community':(4,NAVY),'Rulings (khamr)':(3,GREEN_DK),'Referent groups':(2,BLUE),'Promise→fulfilment':(1,RED)}
# nodes: (lane, x_time, label, colour)
N=[('Events / community',0,'Hijra',NAVY),('Events / community',2,'Badr',NAVY),('Events / community',2,'Qibla',NAVY),
   ('Events / community',3,'Uhud',AMBER),('Events / community',4,'Banū Naḍīr',NAVY),('Events / community',5,'Khandaq',BLUE),
   ('Events / community',6,'Ḥudaybiyya',BLUE),('Events / community',6,'Ḥajj ruling',NAVY),('Events / community',8,'Conquest',RED),
   ('Events / community',9,'Tabūk',NAVY),('Events / community',9,'Masjid Ḍirār',NAVY),('Events / community',9.5,'Mubāhala',RED),('Events / community',10,'Farewell/Māʾida',GREEN_DK),
   ('Rulings (khamr)',-1.2,'provision 16:67',GREEN_DK),('Rulings (khamr)',2,'sin&benefit 2:219',GREEN_DK),('Rulings (khamr)',4.5,'no-pray-drunk 4:43',GREEN_DK),('Rulings (khamr)',9.5,'prohibition 5:90',GREEN_DK),
   ('Referent groups',-2.6,'deniers',BLUE),('Referent groups',-1.6,'polytheists',BLUE),('Referent groups',1.2,'hypocrites',BLUE),('Referent groups',2.2,'people of Book',BLUE),('Referent groups',8.5,'Christians',BLUE),
   ('Promise→fulfilment',-2,'al-Ḍuḥā 93:5',RED),('Promise→fulfilment',-1,'al-Kawthar 108:1',RED)]
# Mecca / Medina backdrop
ax.axvspan(-3.2,-0.2,color=GTINT,zorder=0); ax.axvspan(-0.2,10.6,color=BTINT,zorder=0)
ax.text(-1.7,4.75,'MECCA (pre-Hijra)',ha='center',fontsize=12.5,color=NAVY,fontweight='bold')
ax.text(5.2,4.75,'MEDINA (AH 0–10)',ha='center',fontsize=12.5,color=NAVY,fontweight='bold')
# contemporaneity windows (vertical) — simultaneity across lanes
for xw,lab in [(2,'~2 AH'),(6,'~6 AH'),(9,'~9 AH')]:
    ax.axvline(xw,color=BORD,lw=8,alpha=0.5,zorder=0)
    ax.text(xw,0.3,lab,ha='center',fontsize=11.5,color=INK,fontweight='bold')
pos={}
for lane,x,lab,col in N:
    y=lanes[lane][0]+ (0.22 if lab in('Qibla','Ḥajj ruling','Masjid Ḍirār','people of Book') else (-0.22 if lab in('Mubāhala','polytheists') else 0))
    pos[(lane,lab)]=(x,y)
    ax.scatter([x],[y],s=120,color=col,zorder=4,edgecolors='white',linewidths=1.3)
    ax.text(x,y+0.14,lab,ha='center',va='bottom',fontsize=9.6,color=col,fontweight='bold',rotation=18,zorder=5)
def arrow(p,q,col):
    ax.add_patch(FancyArrowPatch(pos[p],pos[q],arrowstyle='-|>',mutation_scale=12,lw=1.8,color=col,alpha=0.8,zorder=3,shrinkA=7,shrinkB=7))
# directed threads
ev=['Hijra','Badr','Uhud','Banū Naḍīr','Khandaq','Ḥudaybiyya','Conquest','Tabūk','Mubāhala','Farewell/Māʾida']
for a,b in zip(ev,ev[1:]): arrow(('Events / community',a),('Events / community',b),NAVY)
kh=['provision 16:67','sin&benefit 2:219','no-pray-drunk 4:43','prohibition 5:90']
for a,b in zip(kh,kh[1:]): arrow(('Rulings (khamr)',a),('Rulings (khamr)',b),GREEN_DK)
rf=['deniers','polytheists','hypocrites','people of Book','Christians']
for a,b in zip(rf,rf[1:]): arrow(('Referent groups',a),('Referent groups',b),BLUE)
arrow(('Promise→fulfilment','al-Ḍuḥā 93:5'),('Promise→fulfilment','al-Kawthar 108:1'),RED)
for lane,(y,col) in lanes.items():
    ax.text(-3.15,y,lane,ha='left',va='center',fontsize=11.5,color=col,fontweight='bold')
ax.set_xlim(-3.2,11.2); ax.set_ylim(0,5.2); ax.set_yticks([])
ax.set_xticks([-2.6,-1,0,2,3,4,5,6,8,9,10]); ax.set_xticklabels(['early\nMecca','late\nMecca','Hijra','2','3','4','5','6','8','9','10'],fontsize=11,color=INK)
for s in ['top','right','left']: ax.spines[s].set_visible(False)
ax.spines['bottom'].set_color(BORD)
ax.set_xlabel('revealed time →  (vertical bands = contemporaneity windows: parallel events share a time, not a sequence)',fontsize=12.5,color=INK)
ax.set_title('Chronology is a braided partial-order, not a line: parallel threads through shared time-windows',loc='left',fontsize=16,fontweight='bold',color=NAVY,pad=12)
fig.tight_layout(); fig.savefig('research/intrinsic/chrono_figs/chronology_braid.png',dpi=150,bbox_inches='tight'); print('saved chronology_braid.png')
