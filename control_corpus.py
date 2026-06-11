import json, re, math, numpy as np
import analysis as A, spatial_patterns as SP
from collections import defaultdict, Counter

c = A.load_corpus('Book6.xlsx')
N = len(c.df)
su = [int(c.df[A.COL_SURAH].iat[i]) for i in range(N)]
ay = [int(c.df[A.COL_AYAH].iat[i]) for i in range(N)]
W = SP.contiguity_W(114)

def tally(toks_by_row, K):
    ylists = defaultdict(list)
    counts = defaultdict(lambda: np.zeros(115))
    freq = Counter()
    for i in range(N):
        toks = toks_by_row[i]
        if not toks: continue
        seen=set()
        for t in toks:
            r = K(t)
            if not r: continue
            if r not in seen:
                seen.add(r); freq[r]+=1
            ylists[r].append(i)
            s=su[i]
            if 1<=s<=114: counts[r][s]+=1
    rows=[]
    for r,fr in freq.items():
        if fr<8: continue
        ys=sorted(ylists[r])
        if len(ys)<4: continue
        gaps=[ys[k+1]-ys[k] for k in range(len(ys)-1)]
        fano=SP._fano_factor(gaps)
        vec=counts[r][1:115]
        cov=int((vec>0).sum())/114
        klass=SP.morans_I_analytic(vec,W)['klass']
        rows.append((fano,cov,klass))
    m=len(rows) or 1
    def pct(p): return round(100*sum(1 for x in rows if p(x))/m,1)
    return dict(n_roots=len(rows),
        local_clustered=pct(lambda x:x[0]>1.5),
        mean_coverage=round(float(np.mean([x[1] for x in rows])),3) if rows else 0.0,
        I_clustered=pct(lambda x:x[2]=='clustered'),
        I_regular=pct(lambda x:x[2]=='regular'),
        I_random=pct(lambda x:x[2]=='random'))

def scramble(toks_by_row, seed):
    rng=np.random.default_rng(seed)
    flat=[t for toks in toks_by_row for t in toks]
    rng.shuffle(flat)
    out=[]; k=0
    for toks in toks_by_row:
        n=len(toks); out.append(flat[k:k+n]); k+=n
    return out

def run_lang(toks_by_row, K, n_seeds=3):
    real=tally(toks_by_row,K)
    keys=['local_clustered','mean_coverage','I_clustered','I_regular','I_random']
    sims={k:[] for k in keys}
    for sd in range(n_seeds):
        s=tally(scramble(toks_by_row,sd),K)
        for k in keys: sims[k].append(s[k])
    null={k:(round(float(np.mean(v)),2),round(float(np.std(v)),2)) for k,v in sims.items()}
    verdict={}
    for k in keys:
        mu,sd=null[k]; diff=real[k]-mu
        z=diff/sd if sd>0 else (float('inf') if abs(diff)>1e-6 else 0.0)
        verdict[k]=dict(real=real[k],null_mean=mu,null_sd=sd,diff=round(diff,2),
            z=round(z,1) if math.isfinite(z) else None,
            beyond_chance=bool(abs(z)>=2) if math.isfinite(z) else True)
    return dict(real=real, null={k:null[k][0] for k in keys}, verdict=verdict)

if __name__=='__main__':
    import sys
    # Arabic
    ar = run_lang(c.surface_tokens, A.normalize_letters)
    print('ARABIC', json.dumps(ar['real']))
    print('ARABIC null', json.dumps(ar['null']))
    np.save('.stage/_su.npy', np.array(su)); np.save('.stage/_ay.npy', np.array(ay))
    json.dump(ar, open('.stage/arabic_result.json','w'), ensure_ascii=False)
