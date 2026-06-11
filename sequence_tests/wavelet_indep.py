"""Wavelet locality — INDEPENDENCE (vs #33 rhyme/refrain) + 2nd-formulation gate. EQUAL-N + null.

RESULT (this session): NO coverage credit. Wavelet-on-length is largely #33 seen through the
length channel. (1) masking the rhyme-ending class collapses Qur'an 2.35->1.37 (sub-2sd, saj'
2.04 exceeds it); (2) a non-length content signal (lexical novelty) is null for the Qur'an
(0.37, below ordinary prose/poetry). The METHOD stays open for other formulations (root-grain,
masked subspaces, 2D, semantic-field). Telescope rule: this null indicts the formulation, not the idea.

RUN DISCIPLINE: author/run in /tmp via heredoc (mount read lags); this host copy is for the user.
Three signals x {QURAN(ayah), ar_novel/ar_poetry/ar_sajprose(sentence)}, equal-N, phase-randomized null.
"""
import re, os, sys, collections
import numpy as np
import pywt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); import analysis as A
rng = np.random.default_rng(11)
ARLET = re.compile(r'[ء-ي]')
norm = lambda s: ''.join(ARLET.findall(str(s)))
nlet = lambda s: len(ARLET.findall(str(s)))
SCALES = np.arange(2, 33, 2)

def phase_randomize(x):
    X = np.fft.rfft(x - x.mean()); ph = np.exp(1j*rng.uniform(0,2*np.pi,len(X))); ph[0]=1
    return np.fft.irfft(np.abs(X)*ph, n=len(x)) + x.mean()
def intermit(x):
    x = np.asarray(x, float)
    if x.std()==0 or len(x)<64: return np.nan
    coef,_ = pywt.cwt(x - x.mean(), SCALES, 'morl'); p = np.abs(coef)**2
    return np.mean(p.var(1)/(p.mean(1)**2 + 1e-12))
def zloc(x, B=150):
    o = intermit(x); n = np.array([intermit(phase_randomize(x)) for _ in range(B)])
    return (o - np.nanmean(n))/(np.nanstd(n)+1e-9)

def rhyme_resid(units):
    L = np.array([nlet(u) for u in units], float)
    ends = [(norm(u)[-2:] if len(norm(u))>=2 else norm(u)) for u in units]
    out = L.copy(); g = collections.defaultdict(list)
    for i,e in enumerate(ends): g[e].append(i)
    for e,idx in g.items(): out[idx] = L[idx] - L[idx].mean()
    return out
def novelty(units):
    seen=set(); out=[]
    for u in units:
        toks=[t for t in re.split(r'\s+', str(u)) if norm(t)]
        if not toks: out.append(0.0); continue
        out.append(sum(1 for t in toks if norm(t) not in seen)/len(toks))
        seen.update(norm(t) for t in toks)
    return np.array(out, float)

def main():
    c = A.load_corpus(os.path.join(ROOT, "Book6.xlsx"))
    q = [str(t) for t in c.df[A.COL_SURFACE].dropna().astype(str)]
    SENT = re.compile(r'[.!?؟।\n،؛]+')
    def comp(p):
        fp = os.path.join(ROOT,'sequence_tests','corpus',p)
        return [s for s in SENT.split(open(fp,encoding='utf-8').read()) if nlet(s)>0] if os.path.exists(fp) else []
    units = {'QURAN': q}
    for n in ['ar_news','ar_novel','ar_classical2','ar_tabari','ar_poetry','ar_sajprose']:
        u = comp(n+'.txt')
        if len(u) >= 110: units[n] = u
    N = min(len(v) for v in units.values())
    print("units:", {k:len(v) for k,v in units.items()}, "| EQUAL-N =", N)
    def run(label, sig):
        print(f"\n=== {label} ===")
        for name,u in units.items():
            if name=='QURAN':
                zs=[zloc(sig(u[(st:=rng.integers(0,len(u)-N+1)):st+N])) for _ in range(7)]
                print(f"{name:14s}{np.nanmedian(zs):7.2f}  (median/7)")
            else:
                print(f"{name:14s}{zloc(sig(u[:N])):7.2f}")
    run("BASELINE raw length",        lambda u: np.array([nlet(x) for x in u], float))
    run("INDEPENDENCE rhyme-residual (project out #33)", rhyme_resid)
    run("2nd FORMULATION lexical-novelty (content)",     novelty)

if __name__ == "__main__":
    main()
