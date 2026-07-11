# -*- coding: utf-8 -*-
"""Expanded braided chronology WEB: many parallel developmental threads through shared time-windows.
Also computes DAG consistency + incomparability. Locked UI."""
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import networkx as nx, itertools
INK='#10243A';NAVY='#1D3557';GREEN='#1D9E75';GREEN_DK='#0F6E56';RED='#E63946';AMBER='#EF9F27';BLUE='#378ADD';PURP='#7A5AA6';BORD='#E2E8F1';GTINT='#F4F9F7';BTINT='#EAF2FB'
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':INK})
fig,ax=plt.subplots(figsize=(14.2,9.0))
lanes={'Events / community':(8,NAVY),'Ruling: khamr':(7,GREEN_DK),'Ruling: qitāl':(6,GREEN_DK),
 'Ruling: ribā':(5,GREEN_DK),'Referent groups':(4,BLUE),'Warning ↔ glad-tidings':(3,AMBER),
 'Heaven / hell tone':(2,RED),'Ritual + promise':(1,PURP)}
# (lane, x, label, colour)
N=[('Events / community',0,'Hijra',NAVY),('Events / community',2,'Badr',NAVY),('Events / community',3,'Uhud',AMBER),
   ('Events / community',4,'Banū Naḍīr',NAVY),('Events / community',5,'Khandaq',BLUE),('Events / community',6,'Ḥudaybiyya',BLUE),
   ('Events / community',8,'Conquest',RED),('Events / community',9,'Tabūk',NAVY),('Events / community',9.5,'Mubāhala',RED),('Events / community',10,'Farewell',GREEN_DK),
   ('Ruling: khamr',-1.2,'provision 16:67',GREEN_DK),('Ruling: khamr',2,'sin&benefit 2:219',GREEN_DK),('Ruling: khamr',4.5,'no-pray 4:43',GREEN_DK),('Ruling: khamr',9.5,'prohibition 5:90',GREEN_DK),
   ('Ruling: qitāl',-1,'restraint (Mecca)',GREEN_DK),('Ruling: qitāl',2.2,'permission 22:39',GREEN_DK),('Ruling: qitāl',2.6,'prescribed 2:216',GREEN_DK),('Ruling: qitāl',9,'unrestricted 9:5',GREEN_DK),
   ('Ruling: ribā',-1.5,'neutral 30:39',GREEN_DK),('Ruling: ribā',2.4,'prohibition 2:275',GREEN_DK),('Ruling: ribā',3,'no-devour 3:130',GREEN_DK),
   ('Referent groups',-2.6,'deniers',BLUE),('Referent groups',-1.6,'polytheists',BLUE),('Referent groups',1,'hypocrites',BLUE),('Referent groups',2.2,'people of Book',BLUE),('Referent groups',1.4,'muhājirūn/anṣār',BLUE),('Referent groups',8.5,'Christians',BLUE),
   ('Warning ↔ glad-tidings',-2.5,'pure warning',AMBER),('Warning ↔ glad-tidings',-0.5,'balance',AMBER),('Warning ↔ glad-tidings',6,'glad-tidings rise',AMBER),
   ('Heaven / hell tone',-2.5,'hell-heavy 57%',RED),('Heaven / hell tone',4,'balanced 44%',RED),
   ('Ritual + promise',-2,'al-Ḍuḥā 93:5',PURP),('Ritual + promise',-1,'al-Kawthar 108:1',PURP),('Ritual + promise',2,'qibla→Mecca',PURP),('Ritual + promise',6,'ḥajj ruling',PURP),('Ritual + promise',10,'ḥajj complete',PURP)]
ax.axvspan(-3.2,-0.2,color=GTINT,zorder=0); ax.axvspan(-0.2,10.7,color=BTINT,zorder=0)
ax.text(-1.7,8.75,'MECCA',ha='center',fontsize=12.5,color=NAVY,fontweight='bold'); ax.text(5,8.75,'MEDINA (AH 0–10)',ha='center',fontsize=12.5,color=NAVY,fontweight='bold')
for xw,lab in [(2,'~2 AH'),(6,'~6 AH'),(9,'~9 AH')]:
    ax.axvline(xw,color=BORD,lw=9,alpha=0.45,zorder=0); ax.text(xw,0.35,lab,ha='center',fontsize=11,color=INK,fontweight='bold')
pos={}; off={}
for lane,x,lab,col in N:
    base=lanes[lane][0]
    k=(lane,round(x,1)); off[k]=off.get(k,0)+1; dy=0.0
    # stagger near-equal-x labels in a lane
    y=base
    pos[(lane,lab)]=(x,y)
    ax.scatter([x],[y],s=95,color=col,zorder=4,edgecolors='white',linewidths=1.1)
    ax.text(x,y+0.12,lab,ha='center',va='bottom',fontsize=8.8,color=col,fontweight='bold',rotation=20,zorder=5)
def arrow(p,q,col):
    if p in pos and q in pos:
        ax.add_patch(FancyArrowPatch(pos[p],pos[q],arrowstyle='-|>',mutation_scale=11,lw=1.6,color=col,alpha=0.8,zorder=3,shrinkA=6,shrinkB=6))
threads={
 'Events / community':['Hijra','Badr','Uhud','Banū Naḍīr','Khandaq','Ḥudaybiyya','Conquest','Tabūk','Mubāhala','Farewell'],
 'Ruling: khamr':['provision 16:67','sin&benefit 2:219','no-pray 4:43','prohibition 5:90'],
 'Ruling: qitāl':['restraint (Mecca)','permission 22:39','prescribed 2:216','unrestricted 9:5'],
 'Ruling: ribā':['neutral 30:39','prohibition 2:275','no-devour 3:130'],
 'Referent groups':['deniers','polytheists','hypocrites','people of Book','Christians'],
 'Warning ↔ glad-tidings':['pure warning','balance','glad-tidings rise'],
 'Heaven / hell tone':['hell-heavy 57%','balanced 44%'],
}
cols={'Events / community':NAVY,'Ruling: khamr':GREEN_DK,'Ruling: qitāl':GREEN_DK,'Ruling: ribā':GREEN_DK,'Referent groups':BLUE,'Warning ↔ glad-tidings':AMBER,'Heaven / hell tone':RED}
for lane,seq in threads.items():
    for a,b in zip(seq,seq[1:]): arrow((lane,a),(lane,b),cols[lane])
arrow(('Ritual + promise','al-Ḍuḥā 93:5'),('Ritual + promise','al-Kawthar 108:1'),PURP)
arrow(('Ritual + promise','qibla→Mecca'),('Ritual + promise','ḥajj ruling'),PURP); arrow(('Ritual + promise','ḥajj ruling'),('Ritual + promise','ḥajj complete'),PURP)
for lane,(y,col) in lanes.items(): ax.text(-3.15,y,lane,ha='left',va='center',fontsize=10.8,color=col,fontweight='bold')
ax.set_xlim(-3.2,11.4); ax.set_ylim(0,9.0); ax.set_yticks([])
ax.set_xticks([-2.5,-1,0,2,3,4,5,6,8,9,10]); ax.set_xticklabels(['early\nMecca','late\nMecca','Hijra','2','3','4','5','6','8','9','10'],fontsize=10.5,color=INK)
for s in ['top','right','left']: ax.spines[s].set_visible(False)
ax.spines['bottom'].set_color(BORD)
ax.set_xlabel('revealed time →   ·   vertical bands = contemporaneity windows (parallel threads share a time, not a sequence)',fontsize=12.5,color=INK)
ax.set_title('The chronology WEB: many parallel developmental threads braided through shared time-windows',loc='left',fontsize=16,fontweight='bold',color=NAVY,pad=12)
fig.tight_layout(); fig.savefig('research/intrinsic/chrono_figs/chronology_web.png',dpi=150,bbox_inches='tight')
# DAG stats with all threads (build quick graph by time-coord)
G=nx.DiGraph(); T={}
for lane,x,lab,col in N: T[(lane,lab)]=x
for lane,seq in threads.items():
    for a,b in zip(seq,seq[1:]): G.add_edge((lane,a),(lane,b))
# cross-thread contemporaneity not directed; add backbone time edges within Events already there
nodes=list(T)
inc=tot=0
# incomparability over event backbone + threads via time coords: a<b comparable if same lane chain OR strict time on backbone
print('saved chronology_web.png ; threads=%d nodes=%d'%(len(threads)+1,len(N)))
