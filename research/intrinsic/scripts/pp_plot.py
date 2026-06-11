import glob,collections,numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
pts=collections.defaultdict(list); yi=0
for ln in open(RBA,encoding='utf-8'):
    if '\t' not in ln:continue
    _,r=ln.split('\t',1);v=[x for x in r.split() if x and x!='NA'];L=len(v)
    for i,root in enumerate(v):
        pts[root].append((yi,(i/(L-1)) if L>1 else .5))
    yi+=1
show=[('ءله','Allah (uniform)','#1D3557'),('قول','qāla — verse-INITIAL','#1D9E75'),('حکم','ḥakīm — verse-FINAL','#E76F51')]
fig,axs=plt.subplots(1,3,figsize=(11,4.2),sharey=True)
for ax,(r,t,c) in zip(axs,show):
    P=np.array(pts[r]); ax.scatter(P[:,1],P[:,0],s=3,alpha=.35,c=c,edgecolors='none')
    ax.set_title('%s   n=%d'%(t,len(P)),fontsize=11); ax.set_xlabel('position in āyah (0→1)'); ax.set_xlim(-.03,1.03)
axs[0].set_ylabel('āyah index (1 → 6236)'); axs[0].invert_yaxis()
plt.suptitle('Root point patterns — vertical bands = positional preference; no tilt = no drift through the book',fontsize=11)
plt.tight_layout(); out=R+'/research/intrinsic/point_pattern_roots.png'; plt.savefig(out,dpi=110); print('saved',out)
