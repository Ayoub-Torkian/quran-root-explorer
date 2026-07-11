# -*- coding: utf-8 -*-
"""Add a NON-LEXICAL (rhyme/fāṣila, rasm-only) bond to the sūra attraction field; test gap-closing;
locate al-Kawthar in the landscape (pinnedness + bonds), lexical-only vs lexical+rhyme. MEASURED."""
import openpyxl, math, numpy as np
from collections import defaultdict, Counter
rng=np.random.default_rng(17)
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
wb=openpyxl.load_workbook(R+"/Book6.xlsx", read_only=True, data_only=True); ws=wb.active
roots=defaultdict(Counter); ends=defaultdict(Counter)
for r in ws.iter_rows(min_row=9, values_only=True):
    try: s=int(r[5])
    except (TypeError,ValueError): continue
    roots[s].update(str(r[8] or "").split())
    toks=str(r[10] or "").split()
    if toks:
        w=toks[-1]
        key=w[-2:] if len(w)>=2 else w          # rasm rhyme proxy = last 2 consonantal letters
        ends[s][key]+=1
S=sorted(roots); n=len(S); idx={s:i for i,s in enumerate(S)}
# idf over suras
df=Counter()
for s in S:
    for rt in roots[s]: df[rt]+=1
idf={rt: math.log((n+1)/(df[rt]+1))+1 for rt in df}
# vocab for lexical vectors
allroots=sorted(df); ri={rt:i for i,rt in enumerate(allroots)}
L=np.zeros((n,len(allroots)))
for s in S:
    for rt,c in roots[s].items(): L[idx[s],ri[rt]]=c*idf[rt]
# rhyme vectors
allend=sorted({k for s in S for k in ends[s]}); ei={k:i for i,k in enumerate(allend)}
Rm=np.zeros((n,len(allend)))
for s in S:
    tot=sum(ends[s].values()) or 1
    for k,c in ends[s].items(): Rm[idx[s],ei[k]]=c/tot
def signed_cos(M):
    Mn=M/ (np.linalg.norm(M,axis=1,keepdims=True)+1e-12)
    C=Mn@Mn.T; np.fill_diagonal(C,0)
    return C - C[~np.eye(n,dtype=bool)].mean()
Slex=signed_cos(L); Srhy=signed_cos(Rm)
def energy(Sm, order):
    pos=np.empty(n); pos[[idx[s] for s in order]]=np.arange(n)
    D=np.abs(pos[:,None]-pos[None,:])
    return 0.5*float((Sm*D).sum())
canon=S[:]
def Erand(Sm,k=400):
    return np.mean([energy(Sm,list(rng.permutation(S))) for _ in range(k)])
def spectral_anneal(Sm,steps=24000):
    # spectral init via Fiedler of attraction (use -Sm as 'distance')
    A=np.maximum(Sm,0); Dg=np.diag(A.sum(1)); Lap=Dg-A
    w,v=np.linalg.eigh(Lap); order=[S[i] for i in np.argsort(v[:,1])]
    E=energy(Sm,order); best=order[:]; bestE=E; cur=order[:]
    for t in range(steps):
        T=0.5*(1-t/steps)+1e-3
        i,j=rng.integers(n),rng.integers(n)
        if i==j: continue
        nb=cur[:]; nb[i],nb[j]=nb[j],nb[i]; nE=energy(Sm,nb)
        if nE<E or rng.random()<math.exp(-(nE-E)/T):
            cur=nb; E=nE
            if E<bestE: bestE=E; best=cur[:]
    return bestE
def gap(Sm):
    e0=energy(Sm,canon); estar=spectral_anneal(Sm); er=Erand(Sm)
    return e0,estar,er,(e0-estar)/(er-estar+1e-9)
# rhyme-term validity: canonical rhyme-E vs rhyme-shuffle null
e0r=energy(Srhy,canon); nullr=np.array([energy(Srhy,list(rng.permutation(S))) for _ in range(2000)])
zr=(e0r-nullr.mean())/nullr.std()
print("=== rhyme bond validity (does fāṣila carry ORDER signal?) ===")
print(f"canonical rhyme-E {e0r:.1f} vs shuffle {nullr.mean():.1f}±{nullr.std():.1f} -> z={zr:+.2f}")
# gaps
e0L,esL,erL,gL=gap(Slex)
Scomb=Slex+Srhy
e0C,esC,erC,gC=gap(Scomb)
print("=== relaxation gap (lower g = closer to ground state) ===")
print(f"LEXICAL    : E0 {e0L:.0f}  E* {esL:.0f}  Erand {erL:.0f}  -> g={gL:.3f}")
print(f"LEX+RHYME  : E0 {e0C:.0f}  E* {esC:.0f}  Erand {erC:.0f}  -> g={gC:.3f}  (Δg={gC-gL:+.3f})")
# al-Kawthar focal readout: pinnedness = best single-relocation energy GAIN (E0 - min relocated)
def reloc_gain(Sm,s):
    base=energy(Sm,canon); o=[x for x in canon if x!=s]; best=base
    for p in range(len(o)+1):
        cand=o[:p]+[s]+o[p:]; e=energy(Sm,cand)
        if e<best: best=e
    return base-best
def pin_rank(Sm):
    gains={s:reloc_gain(Sm,s) for s in S}
    order=sorted(S,key=lambda s:-gains[s])   # most movable first
    return gains, {s:order.index(s)+1 for s in S}
gL_,rkL=pin_rank(Slex); gC_,rkC=pin_rank(Scomb)
K=108
print("=== al-Kawthar (108) position in the landscape ===")
print(f"LEXICAL   : relocation gain {gL_[K]:.1f}  movability rank {rkL[K]}/{n} (1=most movable)")
print(f"LEX+RHYME : relocation gain {gC_[K]:.1f}  movability rank {rkC[K]}/{n}")
# strongest field bonds for 108 under combined
row=Scomb[idx[K]]
att=sorted(S,key=lambda s:-row[idx[s]])[:6]; rep=sorted(S,key=lambda s:row[idx[s]])[:4]
print("  top attractors:", [(s,round(float(row[idx[s]]),2)) for s in att if s!=K][:5])
print("  top repellers :", [(s,round(float(row[idx[s]]),2)) for s in rep])
print(f"  108 canonical neighbours 107,109 bond: {row[idx[107]]:+.2f}, {row[idx[109]]:+.2f}")
