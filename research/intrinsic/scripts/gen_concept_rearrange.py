# -*- coding: utf-8 -*-
"""Generate assets/concept_rearrange_data.json — concept-rearrangement explorer (Streamlit/Plotly reads this).
Lenses: Meaning (co-occurrence MDS)[divine] · Form (edit-distance ring)[HUMAN] · Rarity (frequency grid). MEASURED on rasm."""
import openpyxl, math, json
from collections import defaultdict, Counter
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
wb=openpyxl.load_workbook(R+"/Book6.xlsx", read_only=True, data_only=True); ws=wb.active
ayah=[]
for r in ws.iter_rows(min_row=9, values_only=True):
    try: int(r[5])
    except (TypeError,ValueError): continue
    ayah.append(set(str(r[8] or "").split()))
Nv=len(ayah)
C=[
 ("عطو",["عطو"],"عطو give","act"),("کثر",["کثر"],"کوثر","out_g"),("صلو",["صلو"],"صلو pray","up"),
 ("ربب",["ربب"],"ربب Lord","root"),("نحر",["نحر"],"نحر sacrifice","act"),("شنء",["شنء"],"شنء hater","down"),
 ("بتر",["بتر"],"أبتر","out_r"),
 ("قلب",["قلب"],"قلب heart","self"),("نفس",["نفس"],"نفس self","self"),("صدر",["صدر"],"صدر breast","self"),
 ("فؤاد",["فءد"],"فؤاد","self"),("علم",["علم","عقل"],"علم·عقل","cog"),("عمل",["عمل","صلح"],"عمل صالح","act"),
 ("ذکر",["ذکر"],"ذکر","up"),("وقی",["وقی"],"تقوی","up"),("ءمن",["ءمن"],"إیمان","up"),("هدی",["هدی"],"هدی","up"),
 ("دنو",["دنو"],"دنیا","dom"),("ءخر",["ءخر","حیی"],"آخرة","dom"),("زید",["زید"],"زاد","amp"),
 ("هوی",["هوی"],"هوی","down"),("مرض",["مرض"],"مرض","down"),
]
ids=[c[0] for c in C]; lab={c[0]:c[2] for c in C}; role={c[0]:c[3] for c in C}; rootsof={c[0]:c[1] for c in C}
pres={cid:[any(rt in a for rt in rootsof[cid]) for a in ayah] for cid in ids}
dfc={cid:sum(pres[cid]) for cid in ids}
dfr=Counter()
for a in ayah:
    for x in a: dfr[x]+=1
def co_ids(i,j): return sum(1 for k in range(Nv) if pres[ids[i]][k] and pres[ids[j]][k])
n=len(ids)
M=[[co_ids(i,j) for j in range(n)] for i in range(n)]
def cos(u,v):
    num=sum(u[k]*v[k] for k in range(len(u))); nu=math.sqrt(sum(x*x for x in u)); nv=math.sqrt(sum(x*x for x in v))
    return num/(nu*nv) if nu and nv else 0.0
SEM=[[cos(M[i],M[j]) for j in range(n)] for i in range(n)]
Dsem=[[1-SEM[i][j] for j in range(n)] for i in range(n)]
def lev(a,b):
    m,k=len(a),len(b); d=[[0]*(k+1) for _ in range(m+1)]
    for i in range(m+1):d[i][0]=i
    for j in range(k+1):d[0][j]=j
    for i in range(1,m+1):
        for j in range(1,k+1):
            d[i][j]=min(d[i-1][j]+1,d[i][j-1]+1,d[i-1][j-1]+(a[i-1]!=b[j-1]))
    return d[m][k]
Dform=[[lev(rootsof[ids[i]][0],rootsof[ids[j]][0]) for j in range(n)] for i in range(n)]
def mds(D):
    D2=[[D[i][j]**2 for j in range(n)] for i in range(n)]
    rm=[sum(D2[i])/n for i in range(n)]; tot=sum(rm)/n
    B=[[-0.5*(D2[i][j]-rm[i]-rm[j]+tot) for j in range(n)] for i in range(n)]
    import random; random.seed(1)
    def mul(Bm,v):return [sum(Bm[i][k]*v[k] for k in range(n)) for i in range(n)]
    def norm(v):
        s=math.sqrt(sum(x*x for x in v));return [x/s for x in v] if s else v
    def eig(Bm):
        v=norm([random.random() for _ in range(n)])
        for _ in range(300): w=mul(Bm,v); v=norm(w)
        val=math.sqrt(sum(x*x for x in mul(Bm,v))); return val,v
    v1=eig(B)[1]; val1=eig(B)[0]
    B2=[[B[i][j]-val1*v1[i]*v1[j] for j in range(n)] for i in range(n)]
    v2=eig(B2)[1]
    return [v1[i] for i in range(n)],[v2[i] for i in range(n)]
def deoverlap(P,min_d=0.165,it=400):
    P=[list(p) for p in P]
    for _ in range(it):
        moved=False
        for i in range(n):
            for j in range(i+1,n):
                dx=P[i][0]-P[j][0];dy=P[i][1]-P[j][1];dist=math.hypot(dx,dy) or 1e-6
                if dist<min_d:
                    pu=(min_d-dist)/2;ux,uy=dx/dist,dy/dist
                    P[i][0]+=ux*pu;P[i][1]+=uy*pu;P[j][0]-=ux*pu;P[j][1]-=uy*pu;moved=True
        if not moved:break
    return P
def renorm(P):
    xs=[p[0] for p in P];ys=[p[1] for p in P]
    def sc(a,lo=0.06,hi=0.94):
        mn,mx=min(a),max(a);return [lo+(x-mn)/(mx-mn)*(hi-lo) if mx>mn else 0.5 for x in a]
    X=sc(xs);Y=sc(ys);return [[round(X[i],4),round(Y[i],4)] for i in range(n)]
xs,ys=mds(Dsem); Lmean=renorm(deoverlap([[xs[i],ys[i]] for i in range(n)]))
# FORM: ring sorted by primary root spelling (form has no real 2-D structure -> show as a neutral ring)
order_f=sorted(range(n), key=lambda i: rootsof[ids[i]][0])
Lform=[None]*n
for rank,i in enumerate(order_f):
    ang=2*math.pi*rank/n+math.pi/2
    Lform[i]=[round(0.5+0.42*math.cos(ang),4), round(0.5+0.42*math.sin(ang),4)]
# RARITY: grid by df, 4 rows
order_r=sorted(range(n), key=lambda i: dfc[ids[i]]); rows=4; ncol=math.ceil(n/rows)
Lrar=[None]*n
for rank,i in enumerate(order_r):
    col=rank//rows; rw=rank%rows
    Lrar[i]=[round(0.06+0.88*col/(ncol-1),4), round(0.12+0.76*rw/(rows-1),4)]
STOP={'ال','من','ما','لا','ان','الذ','هو','کل','علی','الی','فی','ب','ل','و','قول','کون','ذلک','هذا','کان'}
def interp(cid):
    out=[];dfb=dfc[cid]
    if dfb==0:return []
    cnt=Counter()
    for k in range(Nv):
        if pres[cid][k]:
            for x in ayah[k]:cnt[x]+=1
    for a,c in cnt.items():
        if a in rootsof[cid] or a in STOP or c<2:continue
        pab=c/Nv;pa=dfr[a]/Nv;pb=dfb/Nv
        ppmi=math.log2(pab/(pa*pb)) if pa*pb>0 else 0
        out.append((a,c,round(ppmi,2),round(c/dfb,2),ppmi*math.log(1+c)))
    out.sort(key=lambda t:-t[4])
    return [{"r":a,"co":c,"ppmi":p,"P":pc} for a,c,p,pc,_ in out[:6]]
INTERP={cid:interp(cid) for cid in ids}
sem_edges=[]
for i in range(n):
    for j in range(i+1,n):
        if SEM[i][j]>=0.30: sem_edges.append([i,j,round(SEM[i][j],3)])
sem_edges.sort(key=lambda e:-e[2]); sem_edges=sem_edges[:26]
form_edges=[[i,j] for i in range(n) for j in range(i+1,n) if Dform[i][j]<=1]
fe=[];se=[]
for i in range(n):
    for j in range(i+1,n): fe.append(Dform[i][j]); se.append(SEM[i][j])
m=len(fe);mf=sum(fe)/m;ms=sum(se)/m
cov=sum((fe[k]-mf)*(se[k]-ms) for k in range(m))/m
sf=(sum((x-mf)**2 for x in fe)/m)**.5;ss=(sum((x-ms)**2 for x in se)/m)**.5
rho=cov/(sf*ss) if sf and ss else 0
ROLEC={"self":"#1D3557","cog":"#378ADD","act":"#0F6E56","up":"#1D9E75","down":"#E63946","amp":"#EF9F27","bound":"#7A5AA6","dom":"#94A3B8","out_g":"#0F6E56","out_r":"#C1121F","root":"#B5651D"}
nodes=[{"id":ids[i],"label":lab[ids[i]],"role":role[ids[i]],"color":ROLEC[role[ids[i]]],"df":dfc[ids[i]],
        "pos":{"meaning":Lmean[i],"form":Lform[i],"rarity":Lrar[i]},"interp":INTERP[ids[i]],
        "sem":sorted([(lab[ids[j]],round(SEM[i][j],2)) for j in range(n) if j!=i and SEM[i][j]>0],key=lambda t:-t[1])[:4]} for i in range(n)]
D={"nodes":nodes,"edges":{"meaning":sem_edges,"form":form_edges},"corr_form_meaning":round(rho,2),"N":Nv}
def mind(key):
    c=[nd["pos"][key] for nd in nodes]
    return min(math.hypot(c[i][0]-c[j][0],c[i][1]-c[j][1]) for i in range(n) for j in range(i+1,n))
json.dump(D,open(R+"/assets/concept_rearrange_data.json","w",encoding='utf-8'),ensure_ascii=False)
print("min dist  meaning %.3f  form %.3f  rarity %.3f  | sem_edges %d form_edges %d r=%.2f"%(mind("meaning"),mind("form"),mind("rarity"),len(sem_edges),len(form_edges),rho))
