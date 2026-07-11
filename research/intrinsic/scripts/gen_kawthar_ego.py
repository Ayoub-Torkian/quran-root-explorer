# -*- coding: utf-8 -*-
"""al-Kawthar EGO-network: the surah's 7 content roots + the roots that DISTINCTIVELY interpret each.
Distinct from the corpus-wide Concept Atlas (39) and the inner-self page (42). Writes the same JSON schema the
page reads. MEASURED on rasm (PPMI). Hapax (نحر/بتر) come out isolated -> the severance, structurally."""
import openpyxl, math, json, itertools
from collections import defaultdict, Counter
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
wb=openpyxl.load_workbook(R+"/Book6.xlsx", read_only=True, data_only=True); ws=wb.active
ayah=[]
for r in ws.iter_rows(min_row=9, values_only=True):
    try: int(r[5])
    except (TypeError,ValueError): continue
    ayah.append(set(str(r[8] or "").split()))
Nv=len(ayah)
df=Counter()
for a in ayah:
    for x in a: df[x]+=1
ANCH=[("عطو",["عطو"],"عطو give"),("کثر",["کثر"],"کوثر"),("صلو",["صلو"],"صلو pray"),("ربب",["ربب"],"ربب Lord"),
      ("نحر",["نحر"],"نحر sacrifice"),("شنء",["شنء"],"شنء hater"),("بتر",["بتر"],"أبتر")]
anchids=[a[0] for a in ANCH]; anchroots={a[0]:a[1] for a in ANCH}
STOP={'ال','من','ما','لا','ان','الذ','هو','کل','علی','الی','فی','ب','ل','و','قول','کون','ذلک','هذا','کان','الله','ءله'}
pres={i:[any(rt in a for rt in anchroots[i]) for a in ayah] for i in anchids}
dfc={i:sum(pres[i]) for i in anchids}
def interp(cid, topn=5):
    out=[]; cnt=Counter()
    for k in range(Nv):
        if pres[cid][k]:
            for x in ayah[k]: cnt[x]+=1
    for a,c in cnt.items():
        if a in anchroots[cid] or a in STOP or c<2: continue
        pab=c/Nv; pa=df[a]/Nv; pb=dfc[cid]/Nv
        ppmi=math.log2(pab/(pa*pb)) if pa*pb>0 else 0
        if ppmi<0.6: continue
        out.append((a,c,round(ppmi,2),round(c/dfc[cid],2),ppmi*math.log(1+c)))
    out.sort(key=lambda t:-t[4]); return out[:topn]
# build node set
interp_of={i:interp(i) for i in anchids}
extra=[]
for i in anchids:
    for a,c,p,pc,_ in interp_of[i]:
        if a not in extra and a not in anchids: extra.append(a)
nodes_ids=anchids+extra
# presence for ALL nodes (anchors + extras are single roots)
allpres={}
for i in anchids: allpres[i]=pres[i]
for e in extra: allpres[e]=[(e in a) for a in ayah]
alldf={i:sum(allpres[i]) for i in nodes_ids}
def co(i,j): return sum(1 for k in range(Nv) if allpres[i][k] and allpres[j][k])
# bonds among the node set (PPMI>=0.6 & co>=2 since al-Kawthar words are rare)
bonds=[]
ni={x:k for k,x in enumerate(nodes_ids)}
for i,j in itertools.combinations(nodes_ids,2):
    c=co(i,j)
    if c<2: continue
    pab=c/Nv; pa=alldf[i]/Nv; pb=alldf[j]/Nv
    ppmi=math.log2(pab/(pa*pb)) if pa*pb>0 else 0
    if ppmi<0.6: continue
    bonds.append([ni[i],ni[j],round(ppmi,2),c])
bonds.sort(key=lambda b:-b[2])
# co-occurrence vectors for layout + sem neighbors
M={i:[co(i,j) for j in nodes_ids] for i in nodes_ids}
def cos(u,v):
    num=sum(u[k]*v[k] for k in range(len(u))); nu=math.sqrt(sum(x*x for x in u)); nv=math.sqrt(sum(x*x for x in v))
    return num/(nu*nv) if nu and nv else 0.0
n=len(nodes_ids)
SEM=[[cos(M[nodes_ids[i]],M[nodes_ids[j]]) for j in range(n)] for i in range(n)]
Dsem=[[1-SEM[i][j] for j in range(n)] for i in range(n)]
def lev(a,b):
    m,k=len(a),len(b); d=[[0]*(k+1) for _ in range(m+1)]
    for x in range(m+1): d[x][0]=x
    for y in range(k+1): d[0][y]=y
    for x in range(1,m+1):
        for y in range(1,k+1):
            d[x][y]=min(d[x-1][y]+1,d[x][y-1]+1,d[x-1][y-1]+(a[x-1]!=b[y-1]))
    return d[m][k]
def mds(D):
    D2=[[D[i][j]**2 for j in range(n)] for i in range(n)]
    rm=[sum(D2[i])/n for i in range(n)]; tot=sum(rm)/n
    B=[[-0.5*(D2[i][j]-rm[i]-rm[j]+tot) for j in range(n)] for i in range(n)]
    import random; random.seed(1)
    def mul(B,v): return [sum(B[i][k]*v[k] for k in range(n)) for i in range(n)]
    def nrm(v):
        s=math.sqrt(sum(x*x for x in v)); return [x/s for x in v] if s else v
    def eig(B):
        v=nrm([random.random() for _ in range(n)])
        for _ in range(300): v=nrm(mul(B,v))
        return math.sqrt(sum(x*x for x in mul(B,v))),v
    val1,v1=eig(B); B2=[[B[i][j]-val1*v1[i]*v1[j] for j in range(n)] for i in range(n)]; _,v2=eig(B2)
    return v1,v2
def deov(P,min_d=0.165,it=400):
    P=[list(p) for p in P]
    for _ in range(it):
        mv=False
        for i in range(n):
            for j in range(i+1,n):
                dx=P[i][0]-P[j][0];dy=P[i][1]-P[j][1];d=math.hypot(dx,dy) or 1e-6
                if d<min_d:
                    pu=(min_d-d)/2;ux,uy=dx/d,dy/d
                    P[i][0]+=ux*pu;P[i][1]+=uy*pu;P[j][0]-=ux*pu;P[j][1]-=uy*pu;mv=True
        if not mv: break
    return P
def rn(P):
    xs=[p[0] for p in P]; ys=[p[1] for p in P]
    def sc(a):
        mn,mx=min(a),max(a); return [0.06+(x-mn)/(mx-mn)*0.88 if mx>mn else 0.5 for x in a]
    X=sc(xs);Y=sc(ys); return [[round(X[i],4),round(Y[i],4)] for i in range(n)]
v1,v2=mds(Dsem); Lmean=rn(deov([[v1[i],v2[i]] for i in range(n)]))
of=sorted(range(n),key=lambda i:nodes_ids[i]); Lform=[None]*n
for r_,i in enumerate(of):
    ang=2*math.pi*r_/n+math.pi/2; Lform[i]=[round(0.5+0.42*math.cos(ang),4),round(0.5+0.42*math.sin(ang),4)]
orr=sorted(range(n),key=lambda i:alldf[nodes_ids[i]]); rows=4; ncol=math.ceil(n/rows); Lrar=[None]*n
for r_,i in enumerate(orr):
    Lrar[i]=[round(0.06+0.88*(r_//rows)/(ncol-1),4),round(0.12+0.76*(r_%rows)/(rows-1),4)]
GOLD="#CC8A3C"; NAVY="#1D3557"
out_nodes=[]
for k,i in enumerate(nodes_ids):
    isanch=i in anchids
    lab=next((a[2] for a in ANCH if a[0]==i), i)
    ints=[{"r":a,"co":c,"ppmi":p,"P":pc} for a,c,p,pc,_ in (interp_of[i] if isanch else interp(i) if False else [])]
    sem=sorted([(next((a[2] for a in ANCH if a[0]==nodes_ids[j]),nodes_ids[j]),round(SEM[k][j],2)) for j in range(n) if j!=k and SEM[k][j]>0],key=lambda t:-t[1])[:4]
    out_nodes.append({"id":i,"label":lab,"role":("kawthar" if isanch else "interp"),"color":(GOLD if isanch else NAVY),
                      "df":alldf[i],"pos":{"meaning":Lmean[k],"form":Lform[k],"rarity":Lrar[k]},"interp":ints,"sem":sem})
# form-meaning corr
fe=[];se=[]
for i in range(n):
    for j in range(i+1,n): fe.append(lev(nodes_ids[i],nodes_ids[j])); se.append(SEM[i][j])
mm=len(fe); mf=sum(fe)/mm; ms=sum(se)/mm
cov=sum((fe[t]-mf)*(se[t]-ms) for t in range(mm))/mm
sf=(sum((x-mf)**2 for x in fe)/mm)**.5; ss=(sum((x-ms)**2 for x in se)/mm)**.5
rho=cov/(sf*ss) if sf and ss else 0
iso=[i for i in anchids if not any(i in (nodes_ids[b[0]],nodes_ids[b[1]]) for b in bonds)]
D={"nodes":out_nodes,"edges":{"meaning":[],"form":[]},"bonds":bonds,"corr_form_meaning":round(rho,2),"N":Nv,
   "anchors":anchids,"isolated":iso}
json.dump(D,open(R+"/assets/concept_rearrange_data.json","w",encoding='utf-8'),ensure_ascii=False)
print("ego nodes:",n,"(7 anchors +",len(extra),"interpreters) | bonds:",len(bonds),"| isolated anchors:",iso,"| r=%.2f"%rho)
