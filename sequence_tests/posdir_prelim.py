"""PRELIM — positional + directional SUB-UNIT lens within the ayah. EQUAL-N + within-unit-shuffle null.

PRINCIPLE (user): the ayah is an inviolate divine unit — we do NOT divide it arbitrarily — but we
MAY study sub-units along a spectrum (character -> root -> morphological token). This lens is
positional & spatial. Default scan is RIGHT-TO-LEFT (natural/semantic reading); reverse/other
scans are allowed for pattern discovery. Positional AND directional views (and combinations) of
the ayah are a real methodology to give due attention.

VERIFICATION RESULT (this session): the lens is VIABLE (produces real, null-significant,
comparator-able signal) but the FIRST feature (word-length end-cadence) is NOT Qur'an-distinctive.
  - positional slope (sub-unit length vs position) is positive & significant in ALL corpora
    (z 3.3-6.4): words lengthen toward the unit end (universal heavy-final cadence). Qur'an 0.132
    sits LOW; poetry leads 0.344. => no coverage claim.
  - directionality: the linear slope flips sign under reversal trivially (it's antisymmetric in
    position), so it only proves direction-SENSITIVITY, not hidden directional structure. A real
    directional probe needs a NON-antisymmetric statistic (forward vs backward predictive entropy,
    triplet up/down asymmetry) — NEXT.
NO coverage credit. Method recorded as operational; sub-unit spectrum (char/root/morph) + genuine
directional statistics remain to explore (telescope rule).

RUN DISCIPLINE: author/run in /tmp via heredoc (mount read lags); this host copy is for the user.
"""
import re, os, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); import analysis as A
rng = np.random.default_rng(3)
ARLET = re.compile(r'[ء-ي]')
nlet = lambda s: len(ARLET.findall(str(s)))
words = lambda u: [w for w in re.split(r'\s+', str(u)) if nlet(w) > 0]

def unit_lengths(units, kmin=4):
    out = []
    for u in units:
        L = [nlet(w) for w in words(u)]
        if len(L) >= kmin: out.append(np.array(L, float))
    return out

def pos_slope(seqs):
    cs = []
    for L in seqs:
        k = len(L); p = np.arange(k) / (k - 1)
        if L.std() == 0: continue
        cs.append(np.corrcoef(p, L)[0, 1])
    return np.nanmean(cs) if cs else np.nan

def slope_z(seqs, B=300):
    obs = pos_slope(seqs)
    null = np.array([pos_slope([rng.permutation(L) for L in seqs]) for _ in range(B)])
    return obs, (obs - null.mean()) / (null.std() + 1e-9)

def argmax_pos(seqs):
    return np.mean([np.argmax(L) / (len(L) - 1) for L in seqs])

def main():
    c = A.load_corpus(os.path.join(ROOT, "Book6.xlsx"))
    q = [str(t) for t in c.df[A.COL_SURFACE].dropna().astype(str)]
    SENT = re.compile(r'[.!?؟।\n،؛]+')
    def comp(p):
        fp = os.path.join(ROOT, 'sequence_tests', 'corpus', p)
        return [s for s in SENT.split(open(fp, encoding='utf-8').read()) if nlet(s) > 0] if os.path.exists(fp) else []
    corp = {'QURAN': q}
    for n in ['ar_news','ar_novel','ar_classical2','ar_tabari','ar_poetry','ar_sajprose']:
        u = comp(n + '.txt')
        if len(unit_lengths(u)) >= 80: corp[n] = u
    seqs = {k: unit_lengths(v) for k, v in corp.items()}
    N = min(len(s) for s in seqs.values())
    print("usable units (k>=4):", {k: len(v) for k, v in seqs.items()}, "| EQUAL-N =", N)
    print(f"{'corpus':14s}{'slope':>8s}{'slope-z':>9s}{'argmaxPos':>11s}")
    for name, s in seqs.items():
        sub = [s[i] for i in rng.choice(len(s), N, replace=False)]
        obs, z = slope_z(sub)
        print(f"{name:14s}{obs:8.3f}{z:9.2f}{argmax_pos(sub):11.3f}")
    qs = seqs['QURAN'][:N]
    print(f"\nDIRECTIONALITY (Qur'an): slope R->L = {pos_slope(qs):+.3f} ; reversed = {pos_slope([L[::-1] for L in qs]):+.3f}  (trivial antisymmetric flip — use a non-antisymmetric statistic next)")

if __name__ == "__main__":
    main()
