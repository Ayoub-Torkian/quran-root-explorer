"""PRELIM — wavelet LOCALITY of the verse-length signal (FFT-distinct). EQUAL-N + spectrum null.

RUN DISCIPLINE (mount-truncation fix): this file is authored as ONE fresh write. Do NOT
edit-in-place on the host mount and re-run from the mount — the VM sees a stale/truncated
byte-length (documented gotcha). If you must change it, rewrite the WHOLE file fresh, or copy
to /tmp and run there.  Run:  python3 -u sequence_tests/wavelet_prelim.py

Signal formulation (one of many; formulation is the open problem the user flagged):
  x = per-unit LENGTH series  (Qur'an: letters per AYAH = the 'sign' unit;
                               comparators: letters per sentence).
Why wavelet not FFT: FFT is GLOBAL (which rhythms exist); wavelets are LOCALIZED (WHERE).
The Qur'an's only surviving repetition signal is LOCAL (refrains #33, varied recurrence #42),
so we test LOCALITY — the thing FFT cannot see.

Statistic: CWT (Morlet) -> power(scale,time). INTERMITTENCY = mean_scale[ var_t(power)/mean_t(power)^2 ].
Null: PHASE-RANDOMIZED surrogate (keeps the global spectrum, destroys locality) -> excess
      intermittency = genuine non-stationarity BEYOND the spectrum. z vs 150 surrogates.
Equal-N: every series truncated to the shortest unit-count. Comparator-relative (G10 spirit).

CAVEAT (record in any write-up): verse-length partly encodes saj'/rhyme already found (#33),
so this may re-detect known locality, not a fully new axis — must be shown independent of #33/#42.
"""
import re, os, sys
import numpy as np
import pywt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import analysis as A
rng = np.random.default_rng(11)
ARLET = re.compile(r'[ء-ي]')
letters = lambda s: len(ARLET.findall(str(s)))
SCALES = np.arange(2, 33, 2)

def phase_randomize(x):
    X = np.fft.rfft(x - x.mean())
    ph = np.exp(1j * rng.uniform(0, 2 * np.pi, len(X))); ph[0] = 1
    return np.fft.irfft(np.abs(X) * ph, n=len(x)) + x.mean()

def intermittency(x):
    x = np.asarray(x, float)
    if x.std() == 0 or len(x) < 64: return np.nan
    coef, _ = pywt.cwt(x - x.mean(), SCALES, 'morl')
    p = np.abs(coef) ** 2
    return np.mean(p.var(1) / (p.mean(1) ** 2 + 1e-12))

def locality_z(x, B=150):
    obs = intermittency(x)
    null = np.array([intermittency(phase_randomize(x)) for _ in range(B)])
    return (obs - np.nanmean(null)) / (np.nanstd(null) + 1e-9)

def main():
    c = A.load_corpus(os.path.join(ROOT, "Book6.xlsx"))
    q_len = np.array([letters(t) for t in c.df[A.COL_SURFACE].dropna().astype(str)], float)
    SENT = re.compile(r'[.!?؟।\n،؛]+')
    def sent_lengths(path):
        fp = os.path.join(ROOT, 'sequence_tests', 'corpus', path)
        if not os.path.exists(fp): return np.array([])
        return np.array([letters(s) for s in SENT.split(open(fp, encoding='utf-8').read())
                         if letters(s) > 0], float)
    series = {'QURAN': q_len}
    for n in ['ar_news', 'ar_novel', 'ar_classical2', 'ar_tabari', 'ar_poetry', 'ar_sajprose']:
        s = sent_lengths(n + '.txt')
        if len(s) >= 110: series[n] = s
    print("series unit-counts:", {k: len(v) for k, v in series.items()})
    N = min(len(s) for s in series.values())
    print(f"EQUAL-N units = {N} (per-unit letter-count series)")
    print(f"{'text':14s}{'locality-z':>12s}  (>2 = real locality beyond the spectrum)")
    for name, s in series.items():
        if name == 'QURAN':
            zs = [locality_z(s[(st := rng.integers(0, len(s) - N + 1)):st + N]) for _ in range(7)]
            print(f"{name:14s}{np.nanmedian(zs):12.2f}  (median of 7 equal-N slices)")
        else:
            print(f"{name:14s}{locality_z(s[:N]):12.2f}")

if __name__ == "__main__":
    main()
