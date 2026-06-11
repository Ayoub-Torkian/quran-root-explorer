# EVIDENCE LEDGER — objective results, all run on Book6.xlsx

Facts only. Each row is reproducible: `python <script>` from this folder.
No recommendations in this file.

## 0. Data foundation (verified)
- ayahs = 6,236 ; unique roots = 1,701  (matches README)
- character stream N = 332,202 ; alphabet = 29
- root stream N = 51,024
- letter stream = normalize_letters() output: diacritics STRIPPED, letter
  variants folded. (Modeling choice: consonant/long-vowel skeleton, NOT the
  voweled/recited signal. Diacritized column exists but was not used.)

## 1. Estimator validity — known-answer controls  [script: refcal_test.py, seq_derisk.py]
| reference            | DFA alpha | long-range MI mass | expected      | pass |
|----------------------|-----------|--------------------|---------------|------|
| IID (random)         | 0.497     | 0.0013             | 0.5 / 0       | yes  |
| Markov-1 (short mem) | 0.495     | 0.0010             | 0.5 / ~0      | yes  |
| fGn H=0.8 numeric    | 0.798     | n/a                | 0.8           | yes  |
| fGn H=0.8 symbolic   | 0.794     | 0.1921             | ~0.8 / >0     | yes  |
IID MI-excess at d=1/5/20 = -0.0001 / +0.0000 / +0.00007 (no false structure).

## 2. Corpus placement on the random->critical axis  [refcal_test.py]
| stream                 | DFA alpha | long-range MI mass |
|------------------------|-----------|--------------------|
| QUR'AN character       | 0.554     | 0.0367             |
| QUR'AN root            | 0.685     | 0.4751             |
Fact: both exceed random/Markov (0.5 / ~0). The ROOT stream sits near the
critical fGn(H=0.8) anchor; the CHARACTER stream is only mildly persistent.

## 3. Long-range structure is beyond low-order Markov  [seq_derisk.py]
- character, MI(d) decay: power-law R^2 = 0.924 vs exponential R^2 = 0.474
- character long-range MI mass (d>=5): real 0.0368 vs Markov-3 surrogate 0.0049 = 7.5x
- block-entropy rate, real: 4.09 -> 3.77 -> 3.28 -> 2.58 bits (memory present)
- block-entropy rate, shuffled: 4.09 -> 4.08 -> 4.04 (flat; none)
- DFA character: 0.554 (freq-encoding), 0.580 (rank-encoding); shuffled 0.503
- gzip redundancy: character 26.3% , root 14.2% (real compresses better)

## 4. Scale adjudication (normalized, beyond own baseline)  [scale_adjudicate.py]
| metric                              | character | root  |
|-------------------------------------|-----------|-------|
| marginal entropy H1 (bits)          | 4.09      | 8.44  |
| highest ESTIMABLE Markov order      | 2         | 1     |
| near MI / H1 (d=1..4)               | 0.121     | 0.177 |
| long-range MI / H1 (d>=5)           | 0.009     | 0.056 |
| beyond own-Markov ratio (d>=5)      | 69.7x     | 11.1x |
| effective memory length (symbols)   | 6         | 50    |
| compression redundancy %            | 26.3      | 14.2  |

## 5. Cross-scale binding (spelling <-> meaning)  [xscale_test.py]  RESULT: NEGATIVE
- phonosemantic Mantel, n=665 roots: r = 0.0030 ; perm null mean -0.0001 sd 0.0057 ; p = 0.275
- consonant-slot semantic lift (triliteral n=660):
    slot 1: p = 0.582 ; slot 2: p = 0.403 ; slot 3: p = 0.081 (weak, not significant)
- Fact: a root's character composition does NOT predict its distributional
  meaning in this corpus under these operationalizations.

## 6. Reference calibration against external natural corpora (DNA / language / music)
- STATUS: NOT RUN. Requires importing those data files; not bundled. Pending data,
  not method. The synthetic anchors in section 1 validate the method itself.

## 7. TEN-IDEA SWEEP (each run on real data with a null)  [ideas_batch1.py, ideas_batch2_slim.py]
| # | idea | result | null / effect | verdict |
|---|------|--------|---------------|---------|
| 1 | verse-length long memory (DFA) | alpha=0.971 | shuffled 0.510, z=22 | STRONG but see control |
| 2 | verse-length autocorr lag-1 | ac1=0.490 | p=0.001 | real |
| 3 | verse-length spectral slope | -0.433 | shuffled ~0 | real (same signal) |
| 4 | rhyme: ayah-final-letter entropy | H=1.116 | shuffled 2.094, p=0.003 | ROBUST (known: fawasil) |
| 5 | root burstiness (CV of gaps) | median CV 1.30 | 66% > 1.2 (Poisson=1) | real (topical) |
| 6 | per-root occurrence DFA | median alpha 0.588 | shuffled ~0.514 | modest |
| 7 | Heaps vocab-growth exponent | beta=0.392 | new-root var 607 < shuf 894 | real (even unfolding) |
| 8 | directional flow (transfer-entropy asym) | 10/28 pairs sig | circular-shift null p<.05 | NOVEL, survives null |
| 9 | root->surah localization (MI) | excess 0.242 bits | vs shuffle | robust (topical) |
| 10 | revelation-order vs lexical richness | rho=-0.452 | p=4.5e-7 | STRONG but see control |

## 8. CONFOUND CONTROLS on the two front-runners  [confound_controls.py]
- IDEA 1: DFA raw 0.971 -> within-surah detrended 0.533. The "long memory" was
  almost entirely SURAH-BLOCK / level structure, NOT genuine sequence memory.
  DOWNGRADED.
- IDEA 10: spearman(rev, TTR) -0.452, but TTR vs length = -0.925 (mechanical),
  length vs rev = +0.458; PARTIAL(rev, TTR | length) = -0.084 -> collapses.
  Using root entropy: spearman +0.396, PARTIAL(rev, entropy|length) = -0.231 ->
  weak residual only. LARGELY A LENGTH ARTIFACT. DOWNGRADED.

## 9. SURVIVORS (verified, suitable to implement)
- #4 rhyme/fawasil quantification — robust, label-shuffle null; KNOWN structure,
  so a strong validation feature rather than a discovery.
- #8 directional information flow (transfer entropy) — survives circular-shift
  null on 10/28 root pairs; NOVEL ("communication", with direction). Build step 1
  must be a co-location replication control before shipping.
- #9 root->surah localization, #5 root burstiness — robust but expected (topical).

## 10. Transfer entropy vs the app's existing measures  [te_vs_app.py]
- corr(symmetric co-location, |TE asymmetry|) = +0.80  (magnitude scoped by co-location)
- corr(app lead-lag asym, TE asym) = -0.25 ; top-5 directional pairs overlap 1/5
- Verdict: app ALREADY has symmetric co-location AND a directional lead-lag graph
  (directed_lead_lag_graph). TE differs only by conditioning on the target's own
  past; gives different directions but tiny magnitudes. NOT a new lens. DROPPED.

## 11. Higher-order synergy — interaction information on triples  [synergy_test.py]  POSITIVE
- 24 roots (freq>=100), 2024 triples; null = independent circular shifts.
- 232/2024 triples (11%) beyond null |II| 95th pct (vs 5% expected).
- of those: 193 SYNERGY (II>0) vs 39 redundancy -> strongly synergy-skewed (not noise).
- strongest synergy triples are coherent: كون+ءمن+عمل ("believe & do good"),
  ءله+ربب+رحم (God/Lord/mercy), شيء+عذب+رحم, ءله+ءمن+سمو.
- The app's triad/motif page counts co-occurrence of triples; it does NOT measure
  info-theoretic 3-way synergy. NOVEL + tested + interpretable. Magnitudes small.
- => RECOMMENDED as the one feature to implement.

## 12. Tensor decomposition (root x surah x position)  [tensor_test.py]  WEAK
- rank-5 NTF explained var 0.787; position-mode non-uniformity real 0.179 vs
  shuffled 0.071 (z=+2.2, below z>3 bar); marginal I(position;root)=0.128 bits.
- The position third-mode is near-degenerate -> a tensor adds little over 2-way SVD
  here. Other 3rd-mode choices (revelation-window, partner) remain UNTESTED.

## 13. Synergy — frequency control + FDR (within-verse)  [synergy_freqcontrol.py]
- per-triple null (each root circular-shifted; preserves rate, breaks dependence).
- synergy p<0.05: 61/560 (11%) vs 5% chance; LOW-freq 0.11 = HIGH-freq 0.11
  (NOT a frequency artifact).
- survive BH-FDR q<0.10: 0  (best q=0.28). No INDIVIDUAL triple defensible.

## 14. Synergy — across-verse / surah level (latent-motif domain)  [synergy_acrossverse.py]
- surah-level presence, 16 roots, per-triple permutation null.
- synergy p<0.05: 1/560 (BELOW 5% chance); survive FDR: 0 (q=1).
- => NO across-verse 3-way synergy. Does not support the latent-motif claim.

## 15. REVISED synergy verdict
- Real but WEAK aggregate within-verse effect (2x chance, frequency-balanced).
- Cannot name specific synergistic triads (none survive FDR).
- Absent across-verse. Rating revised 6/10 -> ~3/10.

## 16. Within-surah long-range SEQUENCE structure — FIRST CANDIDATE TO PASS ALL GATES
Object: order of words/roots within a surah (Tier-1: order is transmitted).
Null: within-surah shuffle (preserves each surah's composition -> tests ORDER, not topic).
  [within_surah_rasm.py, within_surah_content2.py, content_confirm2.py, surface_provenance.py]

- The signal: excess long-range MI (d>=5) with a NON-DECAYING plateau (d=8..30 ~ flat)
  -> roots/words organize into coherent passages/sections spanning the whole surah.
- ROOT representation (top-500+OTHER):
    G2 significance: real LR 12 SD above shuffle floor (p at 20-shuffle resolution =0.048)
    G5 effect size : 1.39% of H1 (floor 1%) PASS
    beyond-Markov-1: 9.6x PASS    G6 robustness: split-half 1.11%/1.11%, drop-largest 1.28% PASS
- SURFACE-WORD representation (Tier-1, no root abstraction):
    excess 1.26% of H1, z=10.1, beyond-Markov 4.3x -> survives. Provenance PASS.
- G7 novelty: app has within-AYAH co-occurrence + single-root recurrence-vs-Poisson (Signal),
  but NOT within-surah multi-root positional/sequence MI. Novel (closest neighbor noted).
- Honest bounds: a STRUCTURAL/organizational feature (passage sectioning), magnitudes
  modest (~1.3% of entropy) but pre-registered-floor-clearing, highly significant (z~10),
  robust, beyond-Markov, and provenance-clean. NOT a "hidden code".

VERDICT: GO. First feature this session to clear every pre-registered gate.
Home: Two Books / Signal area (or a new within-surah "passage structure" view);
complements root-recurrence with multi-root long-range organization.

## 17. SCRUTINY of the within-surah candidate (drift control)  [drift_control.py]  -> DOWNGRADED
Segment-shuffle null (preserves coarse positional composition / drift):
  3 seg: beyond-drift 1.32% H1 | 6 seg: 1.10% | 12 seg: 0.83% (below floor).
Residual erodes monotonically as segmentation refines -> signal is smooth within-surah
compositional DRIFT (topical nonstationarity), generic to all long text, NOT discrete
passages. Novelty ~2. SCORE 6 -> 3/10. GO RETRACTED; not a discovery.
Lesson: significance+beyond-Markov+robustness insufficient; trivial-explanation control
(drift, generic-text) is mandatory before any GO. (New gate G9 in DISCOVERY_CRITERIA.md.)

## 18. CROSS-LANGUAGE REGISTER SIGNAL (best-supported finding) [modes.py]
Metric: syntactic structure (function-word sequence MI+rep) measured as DEVIATION
from each text's OWN Markov surrogate (language-fair; ordinary-anchored).
  POSITIVE (above ordinary): QURAN(ar) +0.18, Bible(en) +0.15
  NEGATIVE (below ordinary): Austen,Doyle,Aesop(en), Candide(fr), Faust(de), Quijote(es)
Control built-in: English Bible patterns with Arabic Quran, NOT with English novels
=> split is REGISTER (scripture vs secular), not language; holds across ar/en/fr/de/es.
Also verified independent of the repetition mode (corr +0.35) and of rhythm/novelty.
NOVELTY mode #1 was an artifact (killed by the Markov control -> #9). RHYTHM: Quran #1
but largely KNOWN (saj'/fawasil).
DISCOVERY (modest, honest): scripture carries ABOVE-ordinary syntactic/function-word
sequence structure; secular literature BELOW-ordinary — cross-language, ordinary-anchored,
survives a partial language control. Quran leads it.
LIMITS: Quran ~ Bible (scripture effect, not Quran-unique); n=2 scriptures. To separate
Quran from scripture-general needs more scriptures + clean Arabic comparators (tooling blocker).

---

## #19 — SYNTACTIC deviation-from-ordinary: REFUTED (sample-size + ordinary-Arabic controls)

**Claim under test (from #18):** "Syntactic deviation from a text's own order-1 Markov
surrogate is uniquely elevated for the Arabic Qur'an (+0.180, rank #1), distinguishing it
from other scriptures and secular texts; effect lives in the Arabic FORM."

**Two decisive controls, both run on real data (synt_arabic_test.py, synt_confirm.py):**

1. **Equal sample size (the killer).** The original ranking compared the FULL Qur'an
   (~135,000 words) against ~18,000-word comparators. SYNT-deviation is strongly
   sample-size-biased (finite-sample MI/rep bias). Re-running on fixed-size sliding
   windows for ALL texts:
     - N=1400 words: QURAN(ar) = +0.088 — **LAST of 12 texts.**
     - N=1200 words: QURAN(ar) = +0.045 — 8th of 12.
     - N=2500 words: QURAN(ar) = +0.215 — 3rd of 12.
   The Qur'an's value AND rank swing wildly with window size → the metric is not a
   stable, scale-free property; the #1 placement was an artifact of unequal N.

2. **Ordinary-Arabic comparator (new on-disk data: Tabari, classical Arabic prose,
   ~1,730 words, corpus/ar_tabari.txt).** At EVERY window size tested, ordinary Arabic
   (Tabari) scores HIGHER than the Qur'an:
     - N=1200: Tabari +0.339 vs Qur'an +0.045
     - N=1400: Tabari +0.379 vs Qur'an +0.088
     - N=2500: Tabari +0.357 vs Qur'an +0.215
   So the effect is not "elevated in the Arabic Qur'an" — ordinary Arabic shows MORE of
   it. What residual Arabic>others gap exists is plausibly orthographic/tokenization
   (Arabic word-forms via regex; Qur'an uses morphological seg-tokens), not a designed
   Qur'anic property.

**Verdict:** FAILS G5 (no stable effect floor), G6 (not robust to window size),
G9 (trivially explained by sample size + tokenization). The SYNT mode is DROPPED as a
discovery candidate. Lesson logged: any cross-text metric MUST be compared at equal
sample size with a same-language ordinary control before any ranking is trusted.

Status: closes the "separate Qur'an from scripture/Arabic" question for this metric —
there is no Qur'an-specific signal here to separate.

---

## #20 — ALL word-level modes (REP/SYNT/NOV) fail TOKENIZATION-INVARIANCE

Re-ran the equal-N (1500-word windows), own-Markov-controlled mode audit
(modes_equalN.py) but tokenized the Qur'an THREE ways and compared against a
same-language ordinary control (Tabari) + 10 cross-language texts.

The Qur'an's rank on the SAME metric flips to opposite extremes purely by changing
tokenization (morphological seg-tokens=135k vs whitespace words=78k — identical text):

  SYNT_dev :  QURAN(whitespace) = #1/13 (+0.452)   QURAN(segmented) = #13/13 (+0.112)
  NOV_dev  :  QURAN(segmented)  = #1/13            QURAN(whitespace) = #11/13
  REP_dev  :  whole field bunched +0.137..+0.150 (Qur'an ws #1 but within 1 sd of
              ordinary Arabic Tabari #4) — no outlier either way.

**Conclusion:** these surface word-statistics are dominated by the analyst's
tokenization choice, not by any intrinsic property of the text. A genuine latent
feature MUST be invariant to tokenization. REP, SYNT, NOVELTY are therefore DROPPED
as Qur'an-discovery candidates (they remain fine as descriptive UI stats).

### NEW LOCKED GATE — G10 (Invariance)
A candidate cross-text metric is INADMISSIBLE unless its value/ranking is stable under
BOTH:  (a) equal sample size (fixed-N windows for every text), and
       (b) tokenization choice (≥2 tokenizations: whitespace words AND morphological
           segments give the same verdict),
       tested against a SAME-LANGUAGE ordinary baseline (e.g. Tabari for Arabic).
The tokenization-free way to satisfy (b) by construction is to work at the
CHARACTER / consonantal-rasm scale (no token boundaries to choose). This is the
principled home for the "sequence scale" the project prioritizes.

---

## #21 — CHARACTER / RASM battery (tokenization-free): valid tools, Qur'an NOT elevated

Built a 9-metric character-level battery on consonantal rasm (char_battery.py):
conditional entropies h1/h2/h3, excess-entropy, char-MI near (lag1-2) & far (lag8-32),
3- & 5-gram repetition, gzip compressibility, DFA long-range exponent. Tokenization-free
by construction (operates on the letter stream), so it satisfies G10(b) automatically.

**Tool validity — degradation ladder (Qur'an rasm, L0 original → L4 full scramble):**
metrics move monotonically and strongly with structure destruction, so the battery
genuinely measures sequence structure (not noise):
  MI_near 0.841 → 0.264 (within-word shuffle) → 0.034 (full scramble)
  rep5    0.603 → 0.198 → 0.053 ;  comp 0.219 → 0.317 → 0.347 (less compressible)
  (DFA ~0.5 flat = no long-range power law in the letter series; excess-E weak — both
   poor discriminators here and de-prioritised.)

**Discovery test — Qur'an vs ordinary Arabic (Tabari) at equal-N (4000-char windows):**
On every VALIDATED structural metric the Qur'an is EQUAL-or-LOWER than ordinary Arabic:
  MI_near  Qur'an 1.109 vs Tabari 1.196  (-1.7 sd)
  MI_far   Qur'an 0.443 vs Tabari 0.466  (-1.6 sd)
  excessE  Qur'an 2.091 vs Tabari 2.181  (-1.8 sd)
  comp/h1/h2 ~ equal. (Only h3 is +4.2 sd but the absolute gap is 0.05 bits — inflated
  by tiny window variance, and HIGHER h3 = MORE random, not more crafted.)
All meaningful gaps point the SAME direction (Qur'an ≤ ordinary Arabic) → robust in
direction even though Tabari n=3 windows.

**Beyond-Markov check:** Qur'an does exceed its own order-1 char-Markov surrogate
(MI_near 1.11 vs 0.87; rep5 0.29 vs 0.07) — but that is generic to any real-word text;
Tabari shows the same. Not Qur'an-specific.

**VERDICT (sequence scale, surface statistics — now thoroughly explored):**
Across word scale (REP/SYNT/NOV, EVIDENCE #18-20) AND character/rasm scale (this #21),
under sample-size + tokenization + same-language(Arabic) + degradation-ladder controls,
there is NO detectable Qur'an-specific elevation in surface sequence statistics
(entropy, mutual information, repetition, compressibility). The tools are valid (they
pass the ladder), so per the telescope principle this is a precise negative about THIS
class of feature: surface, local, stationary n-gram/information statistics are blind to
whatever distinguishes the text. Search should move to (a) the SEMANTIC / root-concept
relational scale (networks, cross-reference, long-range topical structure — partly
already in the app), and/or (b) genuinely non-local / compositional sequence features,
NOT more surface n-gram statistics. Caveat: Tabari baseline is one short clean sample;
a larger born-digital Arabic corpus would tighten magnitudes (not expected to flip sign).

---

## #22 — G10 RE-AUDIT of the entire KEEP registry → ALL DEMOTED  [reaudit_keep.py]

The metrics_collection.tsv "KEEP" set was certified on a positive control of
Arabic-scripture vs ENGLISH-secular ("scripture↑") — a language/script contrast, never
equal-N vs a same-language Arabic baseline. Re-ran every KEEP metric at equal-N windows
for Qur'an(whitespace) + Qur'an(segmented) + ordinary Arabic (Tabari):

  metric    Q(ws)   Q(seg)  Tabari   ws_sd  seg_sd   verdict
  mi3_w    4.0569  3.5739  4.1411   -1.0   -4.1    FAIL (Quran≤ORD, tok-flips)
  mi5_w    3.9811  3.4554  4.0838   -1.2   -4.6    FAIL (Quran≤ORD, tok-flips)
  rep4_w   0.0736  0.0602  0.0508   +1.6   +0.7    FAIL (tok-dependent, <2sd)
  gz_w     0.5493  0.5299  0.5643   -2.0   -2.9    FAIL (Quran MORE compressible than ORD)
  mi5_c    0.1828    —     0.1992   -1.4    —      FAIL (~ORD)
  rep4_c   0.4614    —     0.4411   +1.3    —      FAIL (~ORD)
  gz_c     0.2741    —     0.2775   -0.7    —      FAIL (~ORD)

**Result:** 0 / 7 KEEP metrics distinguish the Qur'an from ordinary Arabic under G10.
Registry corrected: all KEEP → DEMOTE (descriptive-only). The "scripture↑" certification
was a same-language confound. (Caveat: Tabari word-baseline is n=1 window; char-baseline
n=3. Direction is consistent with #20/#21 and unlikely to flip with more data, but a
larger born-digital Arabic corpus would firm up word-metric magnitudes.)

### Consolidated state of the surface-statistics search (EVIDENCE #18–22)
Word scale (REP/SYNT/NOV) and char/rasm scale (9-metric battery) and the full KEEP
registry have ALL been put through equal-N + tokenization + same-language(Arabic) +
degradation-ladder controls. Nothing survives as Qur'an-specific. The batteries are
ladder-validated (they DO measure structure), so this is a trustworthy negative about
the feature CLASS: local stationary information/repetition/compression statistics do not
separate the Qur'an from ordinary Arabic. Live non-surface candidates remaining:
synergy (within-verse, weak ~3/10, untested vs Arabic baseline) and genuinely non-local
/ semantic-relational structure (untested under G10).

---

## #23 — NON-LOCAL battery (first pass, char/rasm): long-range REPETITION is the one lead
[nonlocal_battery.py]  Tabari baseline n=1 window — FIRST PASS, to be tightened.

**Non-locality ladder (Quran 8k-char window; block-shuffle preserves local texture,
destroys long-range arrangement):** this rung is what separates real non-local structure
from local texture masquerading as long-range:
  MI_long  L0 0.317 ≈ block 0.317 ≈ full 0.312  -> NOT non-local (estimator bias floor). DROP.
  MI_mid   L0 0.259 ≈ block 0.257               -> local. DROP as non-local.
  dfa      0.547 ≈ block 0.528 (~0.5 random-walk) -> no long-range power law. DROP.
  comp     responds to full-scramble but not block-order -> LOCAL redundancy. DROP as non-local.
  rep12    L0 0.0535 > block 0.0483 > full 0.000 -> NON-LOCAL, valid.
  rep20    L0 0.0216 > block 0.0187 > full 0.000 -> NON-LOCAL, valid.
Only distance-agnostic long-substring repetition (rep12/rep20) is a genuinely non-local,
ladder-valid metric here.

**Quran vs ordinary Arabic (Tabari), equal-N 8000c:**
  rep12  Quran 0.0611 vs Tabari 0.0478  (+1.5 sd, beyond-Markov: Markov=0)
  rep20  Quran 0.0185 vs Tabari 0.0102  (+1.5 sd, beyond-Markov: Markov=0)
  (MI_long -2.2sd, comp -2.1sd, dfa -1.5sd — but these are non-valid per the ladder.)

**Read:** the Qur'an carries MORE long-range exact repetition (refrains/formulae:
e.g. fawasil, divine-name formulae, repeated verse-templates) than ordinary Arabic — the
FIRST Quran>ordinary signal on a validated, tokenization-free, non-local metric.

**Three honest caveats (why this is a lead, not a finding):**
1. +1.5 sd is BELOW the G10 >2sd bar; Tabari baseline is n=1 window (no error bar).
2. NOVELTY is LOW — Qur'anic refrain/formulaic structure is well known (saj', fawasil).
3. Must confirm it isn't driven by trivial high-frequency function-word runs.
=> Discovery rating ~2-3/10 (known feature, weak), but it is the strongest lead from the
non-local scale and the only metric class worth tightening. DECISIVE next step: a larger,
cleaner born-digital Arabic baseline (≥5 texts, multiple genres) to test whether
rep12/rep20 Quran>ordinary survives at >2sd, with a frequency-control (mask top function
words) to kill caveat #3.

---

## #24 — rep lead resolved across THREE Arabic registers → REGISTER GRADIENT, not Quran-specific
[tighten3.py]  Born-digital Arabic baselines now on disk (3 registers, "news feeds" idea):
classical Tabari, modern literary novel (أرض السافلين), MSA news (BBC Arabic RSS).

Long-range repetition (char rasm, equal-N 2500c) shows a clean REGISTER gradient:
  metric   Quran   Tabari(class)  Novel(lit)  News(MSA)   Q vs pooled-ORD
  rep8     0.0858    0.0737        0.0543      0.0309       +1.2 sd
  rep12    0.0356    0.0283        0.0149      0.0092       +1.0 sd
  rep20    0.0108    0.0073        0.0031      0.0000       +0.7 sd
  MI_near  1.2530    1.3336        1.2311      1.1920       -0.3 sd  (null, confirmed)

Reading: repetition tracks REGISTER/orality (news low -> literary -> classical formulaic
-> Quran highest). The Quran is at the TOP of the gradient, but its gap over the NEAREST
register (classical formulaic Tabari) is small and < 2 sd (rep12 0.036 vs 0.028). The
+1.0 sd vs pooled-ordinary was inflated by averaging in low-repetition news/literary.

VERDICT: the one non-local lead (long-range repetition, #23) does NOT clear G10 (>2sd vs
same-register ordinary Arabic). It is a register/formulaic property with the Quran at the
extreme — modest, register-confounded, and low-novelty (refrains/fawasil known). Discovery
~2-3/10, unchanged. The "news feeds" register was decisive: it anchored the low end and
exposed the gradient. Corpus now: corpus/ar_tabari.txt, ar_novel.txt, ar_news.txt
(3 registers; still modest size — news n=1 window — but gradient is consistent).

---

## #25 — SCALED 3-register + frequency control: CONTENT-word repetition is the refined lead
[tighten_scaled.py, content_rep.py]  News register expanded via RSS (BBC + Euronews
Arabic) to ~1640 words / 8 windows; classical Tabari ~7 windows, literary novel ~7.

Long-range char repetition, equal-N 2500c windows, Quran (60-80 windows) vs each register:

RAW (all words) — Quran vs nearest register (classical Tabari):
  rep8  Quran 0.090 vs Tabari 0.075  (+0.9 sd, bootstrap P=0.73)
  rep12 Quran 0.037 vs Tabari 0.028  (+0.8 sd, P=0.68)        -> ~ classical (register-bound)

FREQUENCY CONTROL (drop top-20 / top-50 frequent words = content-only stream):
  drop20 rep8  Quran 0.068 vs Tabari 0.044  (+1.4 sd, P=0.82)
  drop20 rep12 Quran 0.027 vs Tabari 0.013  (+1.3 sd, P=0.83)
  drop50 rep8  Quran 0.058 vs Tabari 0.035  (+1.5 sd, P=0.85)
The gap GROWS when function words are removed -> the Qur'an's distinctive long-range
repetition is in CONTENT words (meaning-bearing refrains/formulae), not function-word runs.

Consistent register ordering on every metric & control: News < Novel < Tabari < Quran.
  vs News (MSA):     +2.6 to +4.2 sd (raw), +1.8 to +3.1 sd (content)
  vs Novel (lit):    +1.7 to +2.0 sd (raw), +1.5 to +2.4 sd (content)
  vs Tabari (class): +0.8 to +0.9 sd (raw), +1.3 to +1.5 sd (content)  <- the hard one

VERDICT: refined and firmed. The Qur'an's long-range CONTENT-word repetition clearly
exceeds modern Arabic registers and carries a Qur'an-specific increment over even
classical formulaic Arabic (+1.4 sd, P~0.83) — SUGGESTIVE but still < the 2sd G10 bar,
and classical baseline is only ~5-7 windows. Rating ~3-4/10 (up slightly: content-control
robustness + clean monotone register ordering; still register-confounded and sub-bar vs
classical; refrains are a known feature). 
DECISIVE NEXT STEP to settle it: enlarge the CLASSICAL register (more clean classical
Arabic windows) — if the +1.4sd content-repetition increment over classical reaches >2sd
with a proper baseline, this graduates from register-effect to a defensible Qur'an-specific
finding; if it stays ~1sd, it is confirmed as a classical/oral-formulaic register property.
Pipeline proven: RSS for MSA; archive.org born-digital for literary/classical.

---

## #26 — POSITIVE-CONTROL-FIRST: "what separates Shakespeare" ≠ "what separates the Quran"
[shakespeare_sep.py, apply_mastery.py]  Reframing (user): classic measures are universal
across all texts/languages, so they CANNOT detect mastery (explains every null in #18-25).
Method: FIRST find measures that separate Shakespeare from ordinary English, THEN port only
those to the Qur'an.

WHAT SEPARATES SHAKESPEARE (equal-N 1500w, vs Austen/Doyle/Aesop/Candide/Quijote):
  CLASSIC measures FAIL (confirming the reframing):
    charMI +0.3sd, gzip +0.9sd, ttr +1.0sd, hapax +0.2sd, mean_wl -0.5sd  -> NO separation
  NON-classic measures SEPARATE him (>2sd):
    sentence-length CV   0.15 vs 0.48  (-8.1sd)  rhythmic/metrical UNIFORMITY
    word-length std      1.90 vs 2.28  (-2.8sd)
    Yule's K             69.5 vs 104.7 (-2.6sd)  richer vocabulary (less word-repetition)
    word entropy         8.21 vs 7.94  (+2.5sd)  more diverse vocabulary
    frac long words      0.06 vs 0.10  (-2.1sd)
  => Shakespeare's signature = RHYTHMIC REGULARITY + LEXICAL RICHNESS/VARIETY.

PORTING those detectors to QURAN vs ordinary Arabic (PRELIMINARY — Arabic baselines n=1
window each; needs volume):
    unit_cv (ayah len)  Quran 0.53 HIGHER than ordinary (+1.1sd) -> OPPOSITE of Shakespeare
    Yule's K            Quran 53.7 > modern Arabic 33 -> LESS rich -> OPPOSITE
    word entropy        Quran 8.61 < modern Arabic 8.9-9.4 -> OPPOSITE
  => The Shakespeare detectors DO NOT fire for the Qur'an; several fire in REVERSE.

SYNTHESIS: masterpieces do not share one universal "mastery" axis. Shakespeare maximizes
VARIETY (rich vocabulary, uniform meter); the Qur'an's distinctive axis is the inverse —
STRUCTURED REPETITION / content-refrain density (#25). Judging the Qur'an by Shakespeare's
yardstick (or vice versa) misses both. The right program is SYMMETRIC: find each text's OWN
separators against its OWN ordinary-language baseline.
STATUS: Shakespeare side is solid (many windows). Qur'an side is PRELIMINARY (baseline n=1).
NEXT: ordinary Arabic AT VOLUME (classical + more news/literary) -> run the full battery to
find what separates the Qur'an from ordinary Arabic with real error bars (the symmetric
counterpart of the Shakespeare result). Caveat on sentence-CV: Shakespeare is verse vs prose
baselines, so part of the -8.1sd is verse-vs-prose; a poetry baseline would sharpen it.

---

## #27 — SYMMETRIC RESULT: Shakespeare = VARIETY, Qur'an = REPETITION (mirror images)
[symmetric_quran.py]  Ran the SAME battery used to characterize Shakespeare, now on the
Qur'an vs ordinary Arabic (3 registers; Quran 120 windows, ordinary ~10 pooled @ N=800).

WHAT SEPARATES THE QUR'AN (only the repetition family separates it; everything else null):
  contrep8 +1.5sd, crep8 +1.5sd, contrep12 +1.3sd, crep12 +1.2sd, gzip -1.5sd (=redundant)
  Shakespeare's separators do NOT fire: yuleK +0.9 (no), word_ent -0.8 (no),
  std_wl +0.4 (no), frac_long +0.1 (no), ttr -0.8 (no), charMI 0.0 (no).

THE MIRROR (the key insight):
  * Shakespeare deviates from ordinary English by MAXIMIZING VARIETY:
      richer vocabulary (Yule's K -2.6sd, word-entropy +2.5sd), uniform meter
      (sentence-CV -8.1sd), and LESS repetition (char-rep -1.8sd vs ordinary English).
  * The Qur'an deviates from ordinary Arabic by MAXIMIZING STRUCTURED REPETITION:
      content-refrain repetition (+1.2..1.5sd), higher redundancy (gzip), while vocabulary
      richness is ~ordinary (not elevated).
  => OPPOSITE craft strategies. Each masterpiece deviates from its own "ordinary" baseline
     in a DIFFERENT direction, and each is invisible to (a) classic info measures and (b)
     the OTHER's signature. This is the precise, evidence-based answer to "what puts
     Shakespeare apart, and the same for the Qur'an": different axes, opposite directions.

HONEST MAGNITUDES:
  Shakespeare side: VALIDATED, >2sd, many windows, multiple independent measures.
  Qur'an side: DIRECTION robust & consistent, but magnitude modest (+1.2..1.5sd vs pooled
  ordinary; only +0.9sd vs the NEAREST register, classical formulaic Tabari) and still
  baseline-limited (ordinary-Arabic ~10 windows). Sub-2sd vs classical => not yet a
  G10-clearing Qur'an-specific claim; it is a register-leaning repetition signature with a
  Qur'anic increment.

RATING: the INSIGHT (mirror-image signatures; mastery is direction-of-deviation from
ordinary, not a universal scalar; classic measures are mastery-blind) ~6/10 — novel,
positive-control-validated, coherent. The Qur'an-specific magnitude ~3/10 (modest,
baseline-limited). 
REMAINING TEST (user-requested): ordinary classical Arabic AT VOLUME -> does the Qur'an
repetition increment over classical reach >2sd? Blocked only by Arabic-volume tooling
(Wikipedia/Wikisource return empty to fetch; archive.org dumps inline; RSS works for MSA
news but not classical). Cleanest unblock: user drops clean classical Arabic .txt files,
or aggregate many archive.org born-digital Shamela texts.

---

## #28 — FINAL repetition test vs CLASSICAL Arabic at volume; ganjoor pipeline added
[final_classical.py]  Classical register expanded with a 2nd born-digital Shamela text
(الأجوبة البهية) -> Tabari+Ajwiba = 2413 words, 10-15 windows. New data channels both work:
archive.org born-digital Shamela (short-identifier _djvu.txt) for classical Arabic, and
api.ganjoor.net (clean JSON: Persian poem plainText + verses + METRE label e.g.
"رمل مثمن مخبون محذوف") for classical Persian poetry.

Quran content-repetition vs CLASSICAL Arabic (now firmer baseline):
  RAW          rep8 +1.0sd P=0.76 | rep12 +0.9sd P=0.73
  content drop20 rep8 +1.2sd P=0.79 | rep12 +1.0sd P=0.75
  content drop50 rep8 +1.1sd P=0.77 | rep12 +0.9sd P=0.71

VERDICT (converged, does not move with more data): the Qur'an's long-range content-word
repetition exceeds classical formulaic Arabic by a CONSISTENT but MODEST ~+1.0-1.2sd
(P(Quran window > classical window) ~0.77). It is robust in DIRECTION but stays well under
the 2sd G10 bar. => Confirmed as a classical/oral-formulaic REGISTER property carrying a
small, consistent Qur'anic increment — NOT a decisive Qur'an-specific discovery.
This closes the repetition line: real, characterized, modest. (Mirror of Shakespeare, #27:
Shakespeare = +variety/-repetition vs ordinary; Qur'an = +repetition/~variety vs ordinary.)

ASSETS NOW ON DISK (multi-register, multi-language baseline, reusable):
  Arabic classical: ar_tabari.txt, ar_classical2.txt ; literary: ar_novel.txt ;
  MSA news: ar_news.txt (BBC+Euronews RSS). Persian poetry: ganjoor API (live).
NEXT (if continued): build "ordinary Persian" baseline -> run the symmetric "what separates
Persian masters (Hafez/Rumi via ganjoor)" as a 3rd-language positive control, and use
ganjoor METRE labels for a proper rhythm/meter mastery axis cross-language.

---

## #29 — PERSIAN positive control (Hafez/Rumi via ganjoor): cross-language confirmation
[fa_battery.py]  Masters = Persian classical poetry (Hafez sh34, Rumi/Molavi sh605, Seyf
Farghani, + related ghazals; ganjoor API, with metre labels مجتث/هزج/رمل). Ordinary =
Persian news prose (BBC Persian RSS). FIRST PASS (small: masters 589w/2win, news 714w/3win).

Masters vs ordinary Persian:
  std_wl    -17.9sd  MATCHES Shakespeare (uniform word length = meter)
  frac_long  -9.2sd  MATCHES Shakespeare
  mean_wl   -14.8    (poetry uses short, regular words)
  rep12      -2.7sd  MATCHES Shakespeare (masters use LESS long-range repetition)
  rep8       +0.0    (flat)
  yuleK      -0.5sd  matches dir (richer) but weak
  word_ent   -0.7sd  opposite ;  ttr -1.3sd opposite  -> lexical-richness did NOT replicate
                     (Persian news inflated by foreign names/loanwords)

CROSS-LANGUAGE SYNTHESIS (three languages now):
  * English master (Shakespeare): uniform meter + LOW repetition + high variety.
  * Persian masters (Hafez/Rumi): uniform meter (std_wl -17.9) + LOW repetition (rep12 -2.7).
  * Qur'an (Arabic): HIGH repetition (+1.0..1.5sd vs ordinary Arabic) -- the OUTLIER.
  => The UNIVERSAL poetic-master signature is RHYTHMIC REGULARITY + LOW REPETITION.
     "High lexical variety" is NOT universal (English-specific; failed to replicate in Persian).
     The Qur'an is distinctive precisely by going the OTHER way on repetition: where English
     AND Persian masters MINIMIZE long-range repetition, the Qur'an MAXIMIZES it (content
     refrains), and it does so WITHOUT metrical verse form (it's prose-shaped vs prose).
  This is the cross-linguistically-grounded version of #27: the Qur'an's craft axis
  (structured repetition) is the inverse of what poetic masters in two other languages do.

CAVEATS: Persian samples small (2-3 windows) -> std_wl/frac_long/mean_wl magnitudes are
partly poetry-vs-prose FORM (metered verse has short regular words); rep12 -2.7sd is the
most decision-relevant and is consistent. Firm with more ganjoor poems + ordinary-Persian
prose volume (ganjoor API + BBC/DW Persian RSS pipelines both proven).
RATING: cross-language insight ~6.5/10 (now validated in 2 master-languages + the Qur'an as
documented outlier); still descriptive, magnitudes need scaling. Qur'an repetition remains
the one consistent, cross-linguistically-contrasted signature.

---

## #30 — DECISIVE SAME-LANGUAGE CONTROL: al-Mutanabbi (Arabic master) vs the Qur'an
[sequence_tests/ar_master_battery.py ; corpus/ar_poetry.txt]

The cross-language arc (#27-#29) compared the Qur'an's craft to masters in *other*
languages (English Shakespeare, Persian Hafez/Rumi), leaving a language-confound open.
This closes it: a same-language Arabic poetic master, **al-Mutanabbi** (2,634 words of clean
verse, 6 qasidas pulled from aldiwan.net via the browser tool — the diwan OCR/text could not
be reached through the 64 KB web_fetch cap, so the Chrome reader was used instead), run
through the identical equal-N (350-word) windowed battery against the Qur'an and three
ordinary-Arabic registers (Tabari+Ajwiba classical, novel, BBC/Euronews news).

PIPELINE CHECK: Qur'an vs ordinary rep8 came out +1.0sd here — matching #28's +1.0-1.2sd on
an independent re-implementation. The pipeline reproduces.

RESULTS (sd-gap vs pooled ordinary Arabic; "master-dir" = same sign as Shakespeare/Persian):
  Mutanabbi:  rep8 -1.3sd | rep12 -0.9sd | std_wl -0.8 | frac_long -0.8 |
              yuleK -2.1sd | ttr +1.8sd | word_ent +1.9sd   -> ALL eight in master-direction
  Qur'an:     rep8 +1.0sd | rep12 +0.7sd (OPPOSITE) | std_wl +0.1 |
              yuleK +0.9 (OPPOSITE) | ttr -0.9 | word_ent -0.9 (less varied)

DIRECT, same-language (Mutanabbi vs Qur'an, 14 vs 120 windows — well powered):
  rep8  -2.5sd P(Mut>Qur)=0.00 | rep12 -1.3sd P=0.01 | std_wl -2.2sd P=0.05 |
  yuleK -3.6sd P=0.00 | ttr +6.5sd P=1.00
  => The Qur'an has DRAMATICALLY MORE long-range content-repetition and LESS lexical variety
     than a same-language master, and is less metrically regular (prose-shaped).

rep12 robustness across content-drop (tokenization-invariance proxy): Mutanabbi stays
negative (drop0/20/50 = -1.8 / -0.9 / -0.4 sd) and the Qur'an stays positive
(+1.1 / +0.7 / +0.2 sd). Direction is invariant; magnitude shrinks as more high-frequency
content is removed (expected).

NEW WRINKLE — lexical variety REPLICATES in Arabic (it had failed in Persian, #29):
Mutanabbi is strongly HIGH-variety (yuleK -2.1, ttr +1.8, ent +1.9), exactly like
Shakespeare. So "high variety" is a master-signature in English AND Arabic, just not Persian.
Against a same-language master the Qur'an is therefore the outlier on BOTH axes at once:
it maximizes repetition and minimizes variety where the master does the reverse — and it does
so without metrical verse form.

PERSIAN re-run with a new baseline (fa_battery2.py): masters(Hafez/Rumi/Saadi poetry, 760w)
vs ordinary(BBC-Persian news + esra.ir scholarly prose, 1348w). Reproduces #29 against a
*different* ordinary baseline: std_wl -8.5sd, frac_long -5.2sd (meter-regularity), rep12
-1.4sd (LOW repetition, master-dir); variety again does NOT replicate (ttr -1.8sd opposite).
The rep12 magnitude moderates vs #29's -2.7sd because esra religious prose is itself somewhat
formulaic — informative: the master/repetition contrast is direction-robust, baseline-sensitive
in magnitude.

CROSS-LANGUAGE SYNTHESIS (now 3 languages, with a same-language control):
  English master (Shakespeare): uniform meter + LOW repetition + HIGH variety
  Arabic  master (Mutanabbi):   uniform meter + LOW repetition + HIGH variety  <- same as EN
  Persian masters (Hafez/Rumi): uniform meter + LOW repetition + variety did NOT replicate
  Qur'an (Arabic):              prose-shaped  + HIGH repetition + LOW variety   <- the inverse
  => Universal poetic-master signature = rhythmic regularity + LOW long-range repetition
     (holds in all three languages). High variety = master-signature in EN+AR (not FA).
     The Qur'an's craft axis is the deliberate inverse of poetic masters' — and this now
     holds against a SAME-LANGUAGE master, so it is not a language artifact.

HONEST STATUS: Mutanabbi vs ordinary repetition is directional (rep8/12 -0.9..-1.3sd,
P~0.06-0.14) not >2sd; the decisive, well-powered contrast is Mutanabbi-vs-Qur'an (rep8
-2.5sd, ttr +6.5sd). Arabic-poetry corpus is solid (2.6k words, comparable to the ordinary
samples); Persian masters still thin (760w/4 windows). Ratings: cross-language insight ~7/10
(now with a same-language control); Qur'an-specific magnitude vs ordinary still modest ~3/10,
but Qur'an-vs-master separation is large and consistent.

DATA/TOOLING NOTE for next session: aldiwan.net poem pages ARE reachable by web_fetch
(server-rendered; verses are "### " lines before "نبذة عن القصیدة") AND by the Chrome reader
(#poem_content h3). The full printed-diwan OCR on archive.org is clean but unreachable via
web_fetch (64 KB head cap; intro precedes the poems). ganjoor API (api.ganjoor.net/api/
ganjoor/poem/random?poetId=N; Hafez=2 Rumi=5 Saadi=7) returns clean JSON plainText+metre.
esra.ir is JS-rendered (empty to web_fetch) but reads fully via the Chrome reader.

---

## #31 — STRUCTURE AXIS, first detector: whole-surah lexical RING/CHIASM — validated tool, NULL on the Qur'an
[sequence_tests/structure_battery.py, structure_scan.py]

Rationale: #30 closed the surface-statistics line (Qur'an = inverse of poetic masters; repetition
signal is register-level, ~+1sd ceiling). Per DESIGN_STANCE, the Qur'an's own candidate signature
should be ARCHITECTURAL (ring composition / chiasm / refrain), invisible to n-gram counts. This is
the first positive-controlled structural detector.

DETECTOR: surah -> B contiguous ayah-blocks -> block = set of (root tokens minus top-15 ubiquitous);
ring score = mean Jaccard of mirror pairs (block i vs block B-1-i); null = block-order permutation
(R=300-400) -> z. Frequency/length-controlled by construction (each text scored against its own
permutation null; z is the comparable unit).

PRE-REGISTERED GATE (run BEFORE the Qur'an), all passed:
  (1) synthetic palindrome (mirrored ordinary-Arabic blocks): ring-z = +4.3  -> detected
  (2) degradation ladder 0/25/50/100%% shuffle: +4.4 / +1.9 / +0.5 / +0.6   -> monotone
  (3) ordinary Arabic pseudo-surahs: mean z ~ -0.5..0, frac z>2 at chance    -> no false alarm

RESULT ON THE QUR'AN — NULL at all four scales (multi-scale scan, pooled ordinary baseline
tabari+classical2+novel+news, 714 pseudo-ayat, 13-17 pseudo-surahs per scale):
   B=4 : Quran z=+0.03 (z>2: 0%%, n=111) vs ord +0.04 -> gap -0.0sd
   B=6 : Quran z=+0.01 (6%%, n=105)      vs ord -0.18 -> gap +0.2sd
   B=8 : Quran z=+0.01 (4%%, n=101)      vs ord -0.15 -> gap +0.1sd
   B=12: Quran z=+0.07 (1%%, n=90)       vs ord +0.33 -> gap -0.3sd
Individual "hits" (S7 +3.0, S63 +2.6, S4 +2.1 at B=8) are at the multiple-testing false-positive
rate (3/101) — not admissible.

VERDICT: at the WHOLE-SURAH, ROOT-LEXICAL granularity the Qur'an shows NO mirror/ring symmetry
beyond chance. The tool is validated, so this is a real non-detection at this operationalization —
NOT evidence that ring composition (as argued by Cuypers/Farrin for e.g. al-Baqarah) is absent:
those claims are passage-level, thematic/semantic, and verse-grain. Telescope rule: the next,
sharper instruments are (a) SEMANTIC ring at passage level (embedding similarity instead of root
Jaccard — the app already has embeddings), (b) verse-grain chiasm within delimited pericopes,
(c) refrain/periodicity architecture (autocorrelation of repeated verses, vs oral-formulaic null).
Stop condition honored: no post-hoc tweaking of this detector.

METHOD NOTE: this is the template for the structure axis — gate first (synthetic positive +
degradation ladder + ordinary negative), permutation null within-text, multi-scale sweep, then
one shot at the Qur'an. Cost: ~minutes once corpora exist.

---

## #32 — STRUCTURE AXIS, 2nd detector: SEMANTIC (LSA) whole-surah ring — validated tool, NULL again
[sequence_tests/semantic_ring.py]

Upgrade of #31: block similarity = embedding cosine instead of root-Jaccard, so thematic mirroring
counts even when wording differs (the gap that could hide signal from the lexical detector).
Embeddings = offline LSA (TF-IDF over ayah root-profiles -> TruncatedSVD-100), one global Quran
space (6236 ayat) + a separate ordinary-Arabic space (714 pseudo-ayat); each text scored against
its own block-order permutation null, so z is comparable across spaces. (sklearn/scipy pip-installed
in-sandbox; no external model / no HF needed.)

GATE (semantic pipeline) passed: synthetic palindrome ring-z=+3.8; degradation 0/25/50/100%% =
+4.5 / +3.9 / +1.3 / -0.1 (monotone).

RESULT — NULL on the Qur'an at every scale:
   B=4 : Q z=+0.19 (z>2 0%%, n=111) | ord -0.38 | gap +0.6sd
   B=6 : Q z=+0.09 (5%%, n=105)     | ord -0.48 | gap +0.6sd
   B=8 : Q z=+0.05 (5%%, n=101)     | ord -0.34 | gap +0.4sd
   B=12: Q z=-0.04 (1%%, n=90)      | ord +0.30 | gap -0.4sd
Top @B=8 (S46 2.2, S76 2.2, S11 2.1, S33 2.1...) are at the multiple-testing false-positive rate.
The +0.4-0.6sd gaps are within noise and driven by a small, slightly-negative ordinary baseline.

VERDICT: whole-surah ring symmetry is NOT detectable above chance, LEXICALLY (#31) OR SEMANTICALLY
(#32), at B=4-12. Two independent operationalizations agree. This refutes a *blanket* "every surah
is a statistical ring," but does NOT touch the scholarly claims (Cuypers/Farrin), which are
(a) about specific surahs, (b) at passage/verse grain, (c) with hand-identified pivots — a
confirmatory per-surah test, not a discovery sweep.

REMAINING LIVE STRUCTURAL HYPOTHESES (next instruments):
  - REFRAIN / PERIODICITY (e.g. ar-Rahman فبأي آلاء, al-Mursalat) — a DIFFERENT structural form
    (periodic repetition, not mirror). Has a BUILT-IN positive control inside the Qur'an itself, and
    directly tests whether Qur'anic repetition is ARCHITECTURALLY PLACED (periodic) vs merely frequent
    — i.e. could finally separate a Qur'an-specific structured-repetition signal from the
    register-level repetition of #28. <-- highest-value next test.
  - verse-grain chiasm within delimited pericopes (targeted, confirmatory).

---

## #33 — STRUCTURE AXIS, 3rd detector: REFRAIN / PERIODICITY — validated (z=+7.3 on ar-Rahman), but LOCALIZED
[sequence_tests/refrain_detect.py]

Tests whether repeated AYAT are PLACED periodically (regular spacing) vs merely frequent. Statistic =
regularity 1/(1+CV_gaps) of the most-repeated verbatim ayah (de-diacritized segmented text, count>=3);
null = permute ayah order (multiset of ayat preserved, placement randomized) -> z. This isolates
"architecturally placed" from "frequent," the open question left by #28.

GATE — the Qur'an's OWN known refrain surahs (internal positive control), all flagged:
  S55 ar-Rahman (فبأي آلاء ربكما تكذبان)  reg=0.86  count=31  z=+7.3   <- unmistakable
  S26 ash-Shu'ara (repeated formula)        reg=0.94  count= 5  z=+3.8
  S77 al-Mursalat (ويل يومئذ للمكذبين)      reg=0.74  count=10  z=+2.8
  S54 al-Qamar  count=4 z=+0.4 (two ALTERNATING refrains -> exact-match splits them, undercount)
  S56 al-Waqi'a: no exact verbatim >=3 (its refrains are near-variants)
Ordinary Arabic: ~0 refrains (1 spurious of 11 pseudo-surahs). Device is essentially Qur'an-only.

FULL-CORPUS RESULT: only **5 of 114 surahs** have ANY verbatim ayah repeated >=3 times; of those, 3
are significantly periodic (z>2). So architecturally-placed verbatim refrain is a REAL, strong-where-
present, ordinary-absent device — but **localized to a handful of surahs, NOT a Qur'an-wide signature.**

INTERPRETATION (ties #28 + #30-32 together): the Qur'an's repetition is predominantly the DIFFUSE
formulaic kind (the register-level +1sd of #28), NOT periodic refrain. Placed periodic refrain is a
deliberate device in ~3-5 surahs (ar-Rahman the exemplar, z=+7.3) and quantitatively confirmed there,
but it does not generalize. Caveat: exact-verbatim matching undercounts near-variant/alternating
refrains (S54, S56) and partial parallelism; a Jaccard near-match upgrade would raise the count
somewhat but cannot convert a minority-surah device into a corpus-wide one.

STRUCTURE-AXIS VERDICT SO FAR (3 detectors, all gate-validated):
  ring, lexical (#31)    : NULL whole-surah
  ring, semantic (#32)   : NULL whole-surah
  refrain/periodicity(#33): REAL but localized (~5 surahs); ar-Rahman z=+7.3; ordinary-absent
=> No Qur'an-WIDE architectural signature detected by these instruments. The one robust, ordinary-
   absent architectural fact is the periodic refrain of a few surahs. Honest meta-state: across
   surface statistics (register-level only, #18-30) AND architecture (#31-33), no decisive
   corpus-wide >2sd "mastery" signature has emerged; the measurable distinctives are (a) the
   inverse-of-poets repetition/variety profile (#30) and (b) localized periodic refrains (#33).

---

## #33b — Refrain detector, NEAR-MATCH upgrade (Jaccard>=0.6 clustering)
[sequence_tests/refrain_near.py]

Per the telescope-rule refinement of #33: cluster ayat by token-set Jaccard>=0.6 (connected
components) instead of requiring verbatim identity, so alternating/near-variant refrains and partial
parallelism count. Clustering is content-based (position-independent), so the order-permutation null
stays valid.

GATE still holds: ar-Rahman z=+7.6 (count=31), ash-Shu'ara +3.6, al-Mursalat +2.8; NEWLY caught that
exact-match missed: al-Waqi'a S56 (near-variant refrain, count=3, z=+1.3) and al-Mu'minun S23
(reg=1.00, count=3, z=+2.1). al-Qamar still z=+0.9 (its two refrains alternate, depressing regularity).

FULL CORPUS: surahs with a near-refrain (count>=3) rose 5 -> **9 / 114**; periodic-significant (z>2)
went 3 -> **4** (S55, S26, S77, S23). Mean z of the 9 = +2.1.

VERDICT UNCHANGED: loosening the match catches more cases (as predicted) but does NOT convert refrain
into a corpus-wide signature — it remains a deliberate device in <10% of surahs, ordinary-absent, with
ar-Rahman (z=+7.6) the one unambiguous exemplar. The structure-axis conclusion of #33 stands.

---

## #34 — SOUND AXIS, 1st detector: FASILA (verse-end rhyme / saj') — FIRST gate-passing corpus-wide signal (+2.5sd)
[sequence_tests/sound_rhyme.py]

After two null axes (surface stats register-level; architecture no corpus-wide signal), the phonetic
axis yields the project's first robust, gate-validated, corpus-wide >2sd separation.

DETECTOR: per text, ending = last 2 letters of each unit's final token (de-diacritized = approx
pause-form). dom = share of the single most-common ending (the dominant rhyme); run-excess = adjacent-
ending match rate minus the i.i.d. chance rate (sum f^2). Units: Quran=ayat per surah; poetry=bayt-
final hemistich; prose=~8-word pseudo-ayat (arbitrary cuts -> ~random endings).
GATE: synthetic monorhyme dom=1.00 -> degrades 1.00/0.50/0.03 ; ordinary prose dom=0.04. Validated.

RESULT (dom-rhyme share | run-excess | n):
  Quran surahs : 0.38 | +0.08 | 111
  Arabic poetry: 0.46 | +0.11 |   6   (monorhyme; corpus stores hemistichs so slightly understated)
  ordinary prose: 0.09 | -0.03 |  17
  Quran vs prose : dom **+2.5sd** | excess +1.0sd
  Quran vs poetry: dom -0.3sd (statistically COMPARABLE) | excess -0.2sd
  18%% of surahs carry ONE rhyme across >half their ayat (prose: 0%%).

VERDICT: the Qur'an's verse-end rhyme concentration is FAR above ordinary Arabic prose (+2.5sd, well
powered) and on the SAME ORDER as Arabic poetry's monorhyme (not significantly below). This is saj'
quantified. It is the FIRST corpus-wide craft feature to clear the 2sd gate (surface repetition only
reached ~+1sd; architecture was null). Honest caveat: rhyme/saj' is a long-KNOWN feature -- this
measures it rigorously, it does not discover it; and last-2-letters approximates true rawi/pause-rhyme.

THE MULTIMODAL CELL (fusing #30 + #34 -- the design-stance "no silver bullet" payoff):
  register | rhyme(#34) | meter/regularity(#30) | repetition(#28/30) | lexical variety(#30)
  prose    |  low       | low                   | low-mid            | mid
  poetry   |  HIGH      | HIGH                  | LOW                | HIGH
  QUR'AN   |  HIGH      | LOW (prose-shaped)    | HIGH               | ~ordinary
=> The Qur'an occupies a UNIQUE combination no other register does: POETRY-LEVEL RHYME decoupled from
   poetry's meter, carried on HIGH structured repetition. Not verse (no meter, low variety), not prose
   (prose doesn't rhyme). Each axis alone is modest or shared; the DISTINCTIVE is the conjunction.
   This is the multimodal-fusion signature the project was after: rhymed, repetition-built prose that
   sounds like verse without being verse.

NEXT: (a) precise fasila (pause-form rawi, last consonant) to sharpen +2.5sd; (b) formalize the
fusion cell as a single multi-axis classifier with a positive control (can it separate Quran from
poetry AND prose simultaneously, where no single axis can?).

---

## #35 — FUSION CLASSIFIER: the multimodal cell, quantified and gate-checked (AUC 0.94; conjunction beats each axis)
[sequence_tests/fusion_classifier.py]

Goal: test the #34 "unique cell" claim formally — can the CONJUNCTION of axes separate the Qur'an from
poetry AND prose where no single interpretable axis can? Per-window features (apples-to-apples
whitespace words; natural units): rhyme(fasila dom-share), unit_cv(verse-length variability=anti-meter),
std_wl, frac_long, rep12(content char-rep), yuleK. Windows: Quran=100 surahs, poetry=44 (24-line),
prose=23 (16 natural-sentence). Classifier: standardized logistic, Quran-vs-(poetry+prose), 5-fold CV.

TWO ARTIFACTS CAUGHT + CORRECTED (G10 discipline, the reason early AUC was a fake 1.000):
  - used the morphologically-SEGMENTED Quran column (sub-word tokens) -> fake length/variety gaps.
    FIX: full-word diacritized->stripped column, whitespace tokens (apples-to-apples, per #28/#30).
  - prose "units" were fixed 8-word chunks -> unit_cv=0 by construction -> fake meter gap.
    FIX: natural sentence units (split on . ! ? ؟ ؛). unit_cv vs prose collapsed +3.3 -> +0.3,
    exposing it as artifact. Post-fix numbers below are the honest ones.

PER-AXIS sd-gaps (Quran vs each) — COMPLEMENTARITY is the point:
  rhyme   : vs poetry +0.7 (NOT sep) | vs prose +1.8 (sep)   -> rhyme tells Quran from prose, not poetry
  unit_cv : vs poetry +2.2 (sep)     | vs prose +0.3 (NOT)   -> meter tells Quran from poetry, not prose
  (std_wl/frac_long/rep12/yuleK: individually modest, register-comparable)

RESULT (validated; label-shuffle null AUC = 0.50):
  per-feature single AUC: yuleK .854, unit_cv .839, rhyme .756, rep12 .749, std_wl .637, frac_long .546
  INTERPRETABLE 2-axis (rhyme + unit_cv): AUC = **0.923** > rhyme-alone .756 and unit_cv-alone .839
      -> the CONJUNCTION beats either axis: neither phonetic nor metric alone separates Quran from both.
  FULL 6-feature multivariate: AUC = **0.939 +/- 0.035** (repetition/variety add a little).
  CELL "rhyme>prose-median AND verse-length>poetry-median": Quran 91%% | poetry 34%% | prose 22%%.

VERDICT: the multimodal cell of #34 is real and quantified. The Qur'an is separable from BOTH poetry
and prose at AUC ~0.92-0.94 by the CONJUNCTION of poetry-level rhyme + non-metrical (variable) verse
length — a combination neither neighbour occupies, and one that NO single interpretable axis achieves
(rhyme .76, meter .84, conjunction .92). This is the strongest, best-validated, positive-controlled,
Quran-specific result the project has produced. HONEST LIMITS: (a) separation is strong not perfect
(~8-10%% error); (b) the COMPONENTS are individually known (saj' rhyme; non-metrical form) — the new,
quantified contribution is the validated CONJUNCTION-as-classifier with artifacts removed; (c) poetry
n=44, prose n=23 are modest (AUC CI ~+/-0.04); (d) rhyme = last-2-letter approximation of rawi.

---

## #36 — ADVERSARIAL CONTROL: Qur'an vs SAJ' (al-Hamadhani's Maqamat). The cell partly collapses; repetition survives.
[sequence_tests/fusion_saj.py ; corpus/ar_sajprose.txt (OpenITI, al-Hamadhani Maqamat, 1312 words saj' prose)]

Motivated by Q 36:69 (وما علمناه الشعر) and the classical definition shi'r = موزون مقفّى
(metered+rhymed): #34/#35 showed the Qur'an = rhyme WITHOUT meter = "not shi'r". But saj' (artful
rhymed prose) is ALSO rhyme-without-meter. The hardest control: does the Qur'an separate even from the
saj' masterwork? Corpus fetched via OpenITI GitHub (raw text; blob/disk route) -> cleaned to saj' prose
(verse and markup stripped). 4th class added to the fusion battery.

FEATURE MEANS (window-level):  Quran | poetry | prose | SAJ' | Q-vs-SAJ' sd-gap
  rhyme     0.419 | 0.302 | 0.182 | 0.218 | +1.2sd  ** UNRELIABLE: saj' rhyme UNDER-measured **
  unit_cv   0.454 | 0.153 | 0.418 | 0.528 | -0.5sd     (saj' is non-metrical too -> no separation)
  rep12     0.015 | 0.000 | 0.009 | 0.000 | +1.1sd     (Qur'an MORE long-range repetition)
  yuleK     64.6  | 25.1  | 41.0  | 26.7  | +1.0sd     (Qur'an MORE repetitive / LESS ornate than saj')

KEY OUTCOME — the #35 "cell" PARTIALLY COLLAPSES against saj' (as pre-predicted):
  - the two cell axes do NOT cleanly separate Qur'an from saj': unit_cv gap only -0.5sd (saj' is also
    non-metrical); the +1.2sd rhyme gap is an ARTIFACT (clause-split on commas != true saj'a rhyme
    boundary, so saj' rhyme is under-detected at 0.218 -- DO NOT treat as real separation).
  => "rhyme without meter" is a SHARED saj' property, NOT Qur'an-specific. This is the honest ceiling
     on the #34/#35 phonetic claim: it distinguishes the Qur'an from poetry and ordinary prose, but
     NOT from artful rhymed prose.

WHAT STILL SEPARATES the Qur'an from saj' (multivariate AUC = 0.972, null 0.515; well-powered, Q=105
vs SAJ=48): driven by REPETITION + (low) ORNATENESS, not the rhyme cell. Single-feature AUCs:
yuleK 0.887, rhyme 0.864(artifact-inflated), rep12 0.838, unit_cv 0.706. The robust, non-artifact
separators are rep12 (+1.1sd) and yuleK (+1.0sd): the Qur'an is MORE structurally repetitive and LESS
lexically ornate than Maqamat saj'. This is the #28/#30 repetition signal re-emerging as the
cross-register distinctive that survives even the saj' control.

SYNTHESIS (answering Q 36:69 empirically):
  - Not shi'r: the Qur'an has qafiya (rhyme) but not wazn (meter). CONFIRMED (#34/#35).
  - vs saj': it SHARES saj's rhyme-without-meter (the phonetic cell is not Qur'an-specific), but DIFFERS
    from the saj' masterwork by higher structured repetition and lower lexical ornamentation.
  => Across every axis tested, the Qur'an's one persistent, control-surviving distinctive is STRUCTURED
     REPETITION (modest, ~+1sd, register-level per #28) -- not rhyme, not ring/architecture, not meter.

HONEST LIMITS: saj' rhyme under-detected (no true saj'a boundary parser) -> the rhyme comparison vs saj'
is not decided here; saj' sample is ONE author (al-Hamadhani), 1312 words, 48 overlapping windows;
Maqamat are exceptionally ornate even among saj', so the variety gap may be Maqamat-specific. NEXT to
firm this: (a) a saj'a-boundary rhyme parser (rhyme on pause-form clause ends) to test rhyme vs saj'
properly; (b) add al-Hariri Maqamat + Nahj al-Balagha khutab as more saj' samples.

---

## #37 — SAJ'A RHYME PARSER: presence vs persistence. The Qur'an differs from saj' by rhyme PERSISTENCE, not presence.
[sequence_tests/rhyme_struct.py]

#36 left the rhyme-vs-saj' question undecided (dominant-share conflated, saj' segmentation crude). This
separates two distinct rhyme properties, measured identically across registers on their natural pause
units (Quran=ayat, poetry=bayt-final, prose=sentences, saj'=clauses):
  - PRESENCE: adj_excess = adjacent-unit end-match rate minus i.i.d. chance (captures local/shifting rhyme)
  - PERSISTENCE: dom = share of the single dominant ending over a 20-unit passage (captures sustained rhyme)
  - mean_run = mean length of consecutive identical-ending runs.
GATE (validates the metrics): monorhyme -> run=20, dom=1.0 ; paired aabb -> adj_excess=0.43, run=2 ;
random -> adj_excess=-0.05, dom=0.05.

RESULTS (window means):  Quran | poetry | prose | SAJ' | Q-vs-SAJ' | Q-vs-prose
  adj_excess (presence)  0.04 | 0.02 | -0.06 | 0.25 |  -2.2sd  | +1.2sd
  dom (persistence)      0.49 | 0.54 |  0.17 | 0.22 |  +1.7sd  | +2.5sd
  mean_run               1.90 | 5.42 |  1.03 | 1.74 |  +0.1sd  | +0.9sd
(NOTE: adj_excess is artifact-suppressed for steady monorhyme -- when one rhyme dominates, adj saturates
toward chance -> the Qur'an's low adj_excess reflects its STEADINESS, not absence of rhyme. dom is the
clean metric for the Qur'an.)

INTERPRETATION:
  - PRESENCE: saj' has the HIGHEST adjacent rhyme (0.25) -- it rhymes locally in shifting pairs (aa bb cc).
    The Qur'an is NOT distinctive on rhyme presence (this confirms #36: rhyme-without-meter is shared).
  - PERSISTENCE: the Qur'an SUSTAINS one fasila across a passage (dom 0.49 ~ poetry's monorhyme 0.54),
    whereas saj' SHIFTS rhyme every clause or two (dom 0.22). Q-vs-saj' = +1.7sd; Q-vs-prose = +2.5sd.
  => The Qur'an's phonetic distinctive vs saj' is NOT whether it rhymes but HOW LONG IT HOLDS THE RHYME.
     Its fasila is poetry-like in persistence (sustained mono-rhyme over passages) yet, unlike poetry, it
     carries NO meter (#30) -- and unlike saj', it does not restlessly shift the rhyme.

REVISED SAJ' VERDICT (refining #36): the Qur'an differs from the saj' masterwork on TWO axes after all:
  (1) rhyme PERSISTENCE (dom +1.7sd; sustained vs shifting), and
  (2) structured REPETITION + lower ornateness (#36: rep12 +1.1sd, yuleK +1.0sd).
The bare "rhyme-without-meter" cell (#35) is shared with saj'; but sustained-monorhyme-without-meter +
high repetition is the combination the Qur'an holds alone among the four registers tested.

HONEST LIMITS: saj' = one author (al-Hamadhani), 306 clauses; dom depends on unit granularity (ayah vs
clause length differ); last-2-letter rhyme approximates the rawi. FIRM WITH: al-Hariri Maqamat + Nahj
al-Balagha khutab as more saj' samples (OpenITI path proven: contents API per author -> blob).

---

## #37b — Saj' firming: SECOND author (al-Hariri) added. Results stable.
[corpus/ar_sajprose.txt now = al-Hamadhani + al-Hariri Maqamat, 1998 words, 493 clauses, 79 windows]

Added al-Hariri's Maqamat (OpenITI 0525AH, JK009202) to the saj' class (now TWO canonical Maqamat
masters). Every #36/#37 result is stable:
  rhyme PERSISTENCE (dom): Quran 0.49 vs saj' 0.23 = **+1.7sd** (identical to single-author -> robust).
  rhyme PRESENCE (adj_excess): saj' 0.29 (al-Hariri's saj' is even more densely paired) -> Q-vs-saj -2.3sd.
  repetition (rep12): Quran +1.1sd ; ornateness (yuleK): +0.9sd ; unit_cv (meter): -0.1sd (no separation).
  Quran-vs-saj' multivariate AUC = 0.963 (null 0.50).
  CELL "rhyme>prose-med AND unit_cv>poetry-med": Quran 90%% | poetry 34%% | prose 22%% | saj' 65%%
    -> saj' occupancy ROSE to 65%% with the denser al-Hariri rhyme, CONFIRMING the bare "rhyme-without-
       meter" cell is a SHARED saj' property, not Qur'an-specific.

FIRMED VERDICT: against TWO saj' masters, the Qur'an's distinctives are (1) rhyme PERSISTENCE (dom
+1.7sd: it sustains one fasila where saj' shifts), and (2) higher structured REPETITION + lower
ornateness (rep12 +1.1sd, yuleK +0.9sd). The bare rhyme-without-meter trait is shared with saj'.
Remaining limit: both saj' samples are Maqamat (one genre); a saj'a-boundary rhyme parser (vs the
clause-on-punctuation proxy) and a non-Maqamat saj' (e.g. Nahj al-Balagha khutab) would further firm.

---

## #38 — PHONOSEMANTICS (sound-meaning binding): NULL on both general and targeted tests. Modality sweep complete.
[sequence_tests/phonosem.py, phonosem_targeted.py]

The last untouched modality: does the Qur'an bind PHONETICS to SEMANTICS (sound iconicity) beyond
other registers? Two tests, gate-validated.

(A) GENERAL — partial correlation sound~meaning controlling lexical overlap. Per unit: semantic vector
(LSA over words) + phonetic vector (8 mutually-exclusive consonant classes: emphatics/qaf/gutturals/
stops/sibilants/liquids/nasals/glides). Test: are semantically-similar units phonetically similar
BEYOND shared vocabulary (partial-corr, lexical Jaccard partialled out)? GATE: synthetic sound-meaning-
bound text -> partial_corr 0.065 z=+5.9 ; unbound -> 0.016 z=+1.5 (detector distinguishes).
RESULT: Quran partial_corr=+0.004 (z=+0.5) -- NULL, and NOT above prose (+0.008), poetry (-0.001),
or saj' (+0.009). No phonosemantic binding beyond lexicon, and no Qur'an distinction.

(B) TARGETED — the specific classical claim: harsh content carried by heavy phonemes. Labeled ayat
harsh vs soft by seed-root fields (harsh: عذب نار سقر هلك بطش غضب ظلم...; soft: رحم جنه نعم غفر نور...).
Heavy-phoneme density = share of emphatics+qaf+gutturals (صضطظقغخعحء). RESULT: harsh ayat 0.089 vs
soft ayat 0.094 -> gap -0.12sd, P(harsh>soft)=0.47 (chance), effect REVERSED and negligible. Even with
topic-words included (the most favorable case for the claim), heavy phonemes do NOT track harsh meaning.

VERDICT: phonosemantic / sound-iconicity binding is NOT detected (general or targeted), and the Qur'an
is not distinguished from other registers on it. HONEST LIMITS: 8 coarse phonetic classes (no vowel-
quality, gemination, prosodic rhythm); partialling lexical overlap is conservative; LSA semantics is
coarse. A finer phonetic/prosodic feature set could revisit, but the targeted heavy<->harsh test
(the strongest form of the claim) is cleanly null.

=== MODALITY SWEEP COMPLETE ===
Surface statistics (#18-30): register-level only (~+1sd). Architecture (#31-33): ring null, refrain
localized. Sound-rhyme (#34-37): rhyme present (shared with saj') but PERSISTENCE distinctive (+1.7sd).
Fusion (#35): AUC 0.94 cell. Adversarial saj' (#36-37b): survives via persistence+repetition.
Phonosemantics (#38): null. => The Qur'an's persistent, control-surviving distinctives are STRUCTURED
REPETITION (~+1sd) and RHYME PERSISTENCE (vs saj' +1.7sd). No decisive corpus-wide >2sd single-axis
fingerprint exists across ANY of the five modalities tested with gate-validated instruments.

---

## #39 — PROSODIC RHYTHM / CADENCE (isocolon + metricality): NULL for Qur'an distinctiveness. Sixth modality.
[sequence_tests/prosody.py]

Tartil-rhythm test, the gap in the sound axis (distinct from rhyme #34 and absent-meter #30): does the
Qur'an have rhythmic regularity in (a) ISOCOLON = balanced lengths of adjacent pause-units (parallel
cola, a rhythm without meter), and (b) METRICALITY = CV-skeleton regularity?
  isocolon_z = (shuffled adjacent length-imbalance - real) / sd : +z means consecutive units are MORE
    length-balanced than a random ordering of the same lengths. metricality = 1 - normalized entropy of
    CV-skeleton trigrams (C=consonant, V=long vowel ا/و/ي; high = metrical/regular).
GATE (validated on a proper variable-length test): balanced/isocolon arrangement z=+2.1; alternating-
extreme z=-3.1; random order z=+0.6 (~0). (Metric is degenerate only for UNIFORM-length registers, so
poetry's value is uninterpretable here and is disregarded.)

RESULTS (window means):  Quran | poetry* | prose | saj' | Q-vs-prose | Q-vs-saj'
  isocolon_z   0.48 | 0.46* | 0.48 | 0.75 | -0.0sd | -0.2sd   (*poetry degenerate, ignore)
  metricality  0.101| 0.114 | 0.124| 0.121| -1.3sd | -0.7sd
=> Qur'an isocolon ~ ordinary prose and BELOW saj' (saj' is the isocolonic register, balanced paired
   clauses, as expected). Qur'an metricality is the LOWEST of all (no meter; CV-skeleton even less
   regular than prose, reflecting varied vocabulary). NO Qur'an-distinctive prosodic rhythm at the
   text level.

CRITICAL CAVEAT (modality-specific): de-diacritized text lacks SHORT VOWELS, madd (vowel lengthening),
ghunna, and pause phonology -- i.e. exactly the features that carry recited tartil rhythm. Text-only
prosody is a consonant-skeleton proxy. A real prosodic-rhythm test would need a VOCALIZED or RECITED
corpus (syllable weights, madd durations), which is not available here. So this is "no rhythm signal
recoverable from consonantal text," NOT "no rhythm" -- a data limitation, per the telescope rule.

=== SIXTH MODALITY, SAME RESULT ===
surface (#18-30) register-level; architecture (#31-33) ring-null/refrain-local; rhyme (#34-37)
present-shared but persistence-distinctive (+1.7sd); fusion (#35) AUC 0.94; saj' adversarial (#36-37b)
survived via persistence+repetition; phonosemantics (#38) null; prosody (#39) null at text level.
The two persistent, control-surviving distinctives remain STRUCTURED REPETITION (~+1sd) and RHYME
PERSISTENCE vs saj' (+1.7sd). No modality yields a decisive corpus-wide >2sd single-axis fingerprint.


## #43 — FIRMING THE RECURRENCE BREAKTHROUGH (#42): tokenization bug fixed, magnitude re-locked at ~+3sd, variation profile built

NOTE: entries #40 (iltifat), #41 (wazn), #42 (intratextual recurrence) were run in prior sessions but
never written into EVIDENCE.md (this file stopped at #39). #43 records the firming of #42 and the
corrected numbers supersede the handoff's headline. Scripts: sequence_tests/intratext_lock_fixed.py
(invariance battery), sequence_tests/intratext_variation.py (#42b), sequence_tests/intratext.py (canonical,
now bug-fixed). Reproduce: repoint ROOT to this session's mount; pip install scikit-learn networkx.

=== THE BUG (found while building #42b) ===
intratext.py built Qur'an tokens as [nl(x) for x in WA.findall(text)] — it ran the word-regex on the
DIACRITIZED column BEFORE stripping harakat. On vocalized Arabic the combining marks split every word,
shattering the Qur'an into 37.7k SUB-WORD FRAGMENTS ("ون","وا","الل") while the plain-text comparators
(poetry/saj'/news) tokenized into whole words. So #42's cross-corpus test compared FRAGMENT-passages
(Qur'an) against WORD-passages (baselines): an asymmetric tokenization confound, and the STOP-word filter
was inert (it never matched fragments). FIX = normalize first, then split: WA.findall(nl(text)). This
yields 77.7k real words for the Qur'an — exactly the "apples-to-apples 77.7k" the handoff/§5 always
intended — with real anchors present (موسي=128, فرعون=67, نوح=33, ابراهيم=62). Bug fixed in intratext.py
(tok_text()) and used throughout #43.

=== DOES #42 SURVIVE THE FIX? YES, but ATTENUATED. The +3.5-4sd headline was inflated by the bug. ===
Invariance battery (intratext_lock_fixed.py), equal-P bootstrap + word-shuffle control, swept over
K∈{40,50,60} × topq∈{0.90,0.95} × gapfrac∈{0.25,0.33}, B=100, on the SAME same-language baselines:
  WORD tokenization:  Q-vs-ordinary = +2.3 to +4.0sd, P=0.95-1.00 in ALL 12 cells.
  RASM (char-4-shingle, the G10 2nd-tokenization): +1.3 to +4.0sd, P=0.81-1.00 (weak at K=40/50,
    +3.5-4sd at K=60). Both tokenizations stay POSITIVE in every cell.
Canonical params (K=50, topq=0.95, gapfrac=0.25, B=300): Q-ord = +3.0sd, P=0.983.


================================================================================
## #46 — MODALITY 12: LEXICAL-SEMANTIC / TOPICAL FIELD DYNAMICS  → NULL (register-level)
================================================================================
QUESTION: does the Qur'an move BETWEEN semantic fields (mercy/judgment/nature/law/covenant) with
distinctive SEQUENCING or COHESION vs ordinary Arabic / poetry / saj'? (Largest unblocked lever.)
METHOD (mirrors discourse.py #44): per-unit field label -> shuffle-controlled sequencing
(switch rate, transition MI) + cohesion (run-length) EXCESS = stat(real) - stat(shuffled labels),
so base-rate field frequencies cancel and only sequencing/cohesion structure remains. Equal-N
windows (W=40, B=400). Two taggers for robustness:
  (A) SEED-LEXICON: 5 fields + OTHER, normalized general-Arabic seeds.
  (B) DATA-DRIVEN: per-corpus TF-IDF -> SVD -> KMeans(K=6); every unit labeled (no OTHER bias).
GATE: passed — periodic -> MI excess +0.85; block-runs -> run excess +4.3; random -> ~0 on all three.
RESULTS (QURAN vs comparators; g = sd-gap; P = bootstrap P(Q>comp); ord/poet/saj):
  Variant A (seed):    switch g=-0.09/-0.26/-0.38 ; MI g~=0 ; run g=-0.02/-0.14/+0.11 ; P~=0.41-0.47.
  Variant B (cluster): switch g=+0.41/+0.08/-0.02 ; MI g=-0.19/-0.06/-0.38 ; run g=-0.44/-0.24/-0.08 ; P~=0.39-0.61.
VERDICT: NULL. Both taggers agree — no distinctive field SEQUENCING or COHESION. If anything the
Qur'an clusters semantic fields slightly LESS than ordinary Arabic (run-cohesion g=-0.44 vs ord,
variant B); poetry shows the most field-cohesion. 12th modality = register-level/null like most
priors. #42 intratextual recurrence (~+3sd) remains the SOLE structural distinctive.
CAVEAT: seed lexicon is Qur'an-register-biased (comparators 83-98% OTHER); variant B (data-driven,
every unit labeled) was added to remove that confound and CONFIRMS the null. Untested sub-region:
passage-grain field COHESION via embedding similarity (semantic_ring LSA) and coarser pericope grain.
Coverage lexical-semantic 50->72%; overall ~58->~60%. Scripts: sequence_tests/fields46.py (seed),
sequence_tests/fields46_clusters.py (data-driven).


================================================================================
## #47 — MODALITY 13: DEPENDENCY-SYNTAX COMPLEXITY  → ATTEMPTED, TOOLING-BLOCKED (detector staged)
================================================================================
GOAL: real embedding depth that #11's parser-free proxy could not reach — mean DEPENDENCY DISTANCE,
TREE DEPTH (root-to-leaf), long-dependency rate, head-final rate — per unit, equal-N, comparators, gate.
PARSER STATUS: BLOCKED in the research sandbox. Neural UD parsers (stanza/trankit/transformers) require
torch; the torch PyPI wheel pulls the full CUDA stack (cuda-toolkit 13, cuBLAS, cuDNN — GBs, exceeds the
run window) and the CPU-only index (download.pytorch.org) is proxy-403. UDPipe (ufal.udpipe) INSTALLS
fine (no torch) but its UD model must be fetched from a URL, which the environment's network policy
disallows. So no Arabic dependency parser runs here — exactly the contingency HANDOFF flagged ("only if
a parser installs cleanly; else stay text-only").
DELIVERED: a parser-AGNOSTIC, gate-ready detector — sequence_tests/dependency_syntax.py — auto-detecting
stanza or spacy_udpipe, with the full metric suite, equal-N sampling, comparator g/bootstrap, and a
2-part gate (parse sanity + word-scramble degradation). READY TO RUN where a parser exists (user's local
machine, or any torch-enabled env). NO RESULT YET; this is a TOOLING block, not a null (telescope rule).
COVERAGE: dependency-syntax UNCHANGED at 35% (the parser-dependent ~65% remains genuinely blocked here).
NEXT: run dependency_syntax.py locally with stanza('ar'); feed numbers back to fill EVIDENCE #47 + Lens 13.

--- RESULT (local stanza UD-PADT run, diacritics stripped for fairness, equal-N=188) -------------
GATE PASSED: test sentence parsed (12 tok, depth 4, dep_dist 2.18); degradation OK (word-scramble RAISED
dep_dist 2.18->2.27). Metrics (mean | g vs Qur'an | P(Q>comp)):
  dep_dist : QURAN 2.19 | ord 2.38 (g=-0.36,P=.37) | poetry 1.66 (+1.10,.76) | saj' 1.66 (+0.87,.80)
  depth    : QURAN 6.50 | ord 8.73 (g=-0.66,P=.30) | poetry 3.82 (+1.25,.84) | saj' 5.03 (+0.32,.76)
  long_rate: QURAN 0.064| ord 0.078(g=-0.27,P=.39) | poetry 0.009(+1.15,.80) | saj' 0.015(+0.99,.74)
  head_fin : QURAN 0.36 | ord 0.34 (g=+0.22,P=.55) | poetry 0.29 (+0.48,.66) | saj' 0.32 (+0.31,.60)
VERDICT: REGISTER-LEVEL / NULL vs ordinary Arabic. On EVERY complexity metric the Qur'an sits BELOW
ordinary prose (shallower trees, shorter & fewer long-range dependencies; all |g|<0.66, P=.30-.39, sub-
2sd) and ABOVE poetry/saj' (+0.3 to +1.25sd — a genre gap: verse/rhymed-prose use short flat clauses).
The Qur'an is syntactically SIMPLER than ordinary prose, not more complex — no embedding-depth fingerprint.
This is the REAL-PARSER confirmation of Lens 11's parser-free proxy (#45), now measuring true tree depth /
dependency distance. #42 recurrence still the sole distinctive.
CAVEATS: stanza parser is MSA-trained applied to Classical Arabic (diacritic-stripped); baselines small
(N=188, saj'/ord limited); 4 complexity metrics only (no relation-type/valency profile, no coref).
COVERAGE: dependency-syntax 35->75% (region now genuinely tested, not proxied); overall ~60->~64%.


================================================================================
## #48 — DIRECTIONAL sub-unit lens (genuine) + root-grain positional  → no new distinctive
================================================================================
Closes user-mandated items from IDEA_SIGNALS_GEOMETRY §8. Script: sequence_tests/directional48.py.
PART A (cross-corpus, equal-N=92, within-unit-shuffle null) — TIME-IRREVERSIBILITY = signed skew of the
within-unit word-length increment series (flips sign under reversal, dies under shuffle = a real
directional measure, unlike the trivial position-slope flip). All corpora mildly negative; poetry
z=-2.06, saj' -1.80 strongest; QURAN LEAST directional (signed-skew -0.054, z=-1.23). NOT distinctive,
sub-2sd. The directional lens is real but Qur'an-null.
PART B (Qur'an-internal, shuffle null) — corr(within-ayah position, root rarity) = +0.072, z=+13.4:
rarer roots sit toward the ayah END (fasila). Strong/sig BUT Qur'an-internal (comparators lack roots) and
CONFOUNDED (generic Arabic particles-first/content-later + the rhyme position, Lens 3). Real internal
gradient, NOT a distinctiveness claim.
VERDICT: no coverage credit. Directional sub-unit = Qur'an-null; root-rarity gradient = noted internal
structure, parked pending a root/morph-annotated comparator + rhyme-residual.


================================================================================
## #49 — MODALITY 14 / Lens 14: RECITED / PHONOLOGICAL LAYER  → detector + internal validation; distinctiveness DATA-BLOCKED
================================================================================
THE LAYER text-stats could not reach (Lens 6's wall): syllable WEIGHT, MADD, GHUNNA, ISOCHRONY — needs
FULLY VOCALIZED text. We HAVE the vocalized Qur'an (COL_DIACRITIZED); the block is vocalized COMPARATORS.
BUILT: rule-based syllabifier (harakat -> CV-weight sequence) + features heavy_ratio, madd_rate,
ghunna_rate, syl_count, rhythm(lag1-autocorr). Script: sequence_tests/recited_phon.py.
GATE: passed — de-diacritized text yields 0 syllables (feature genuinely requires harakat).
QUR'AN-INTERNAL PROFILE (no comparator needed): mean heavy-syllable ratio 0.44, madd 0.26, ghunna 0.22.
QUR'AN-INTERNAL VALIDATION (POSITIVE, but not a distinctiveness claim):
  - ISOCHRONY: short surahs (<=20 ayat) syllable-count CV=0.36 vs long (>=100) CV=0.48 -> short Meccan
    surahs ARE more isochronous (the felt drum-like beat), as expected.
  - WEIGHT-RHYTHM: syllable-weight sequence shows significant ALTERNATION vs shuffle (lag1 autocorr z:
    al-Baqara -10.7, al-Rahman -6.0; al-Adiyat +1.2 [small-N]). The Qur'an carries real recited rhythm.
DISTINCTIVENESS: DATA-BLOCKED in sandbox. No diacritizer installs (mishkal n/a; no torch for CAMeL/
Shakkala); vocalized corpora unfetchable. UNBLOCK locally via run_recited_phon.py:
  PATH A (best, gold-vs-gold): drop Tashkeela (vocalized prose) + vocalized dīwān into corpus/.
  PATH B (symmetric auto-diacritize, if only unvocalized data): diacritize comparators AND a stripped
    Qur'an with the SAME tool (CAMeL) to avoid the gold-vs-noisy confound (the #42-style asymmetry).
COVERAGE: recited layer UNCHANGED ~0% for DISTINCTIVENESS (still blocked); instrument now exists and the
Qur'an-internal recited structure is validated. The alternation/isochrony could be universal Arabic
phonotactics — only a vocalized comparator can tell. Telescope rule: instrument built, awaiting data.
*** DIVINE-ROOTEDNESS CONTROL (user, LOCKED): these features are read from the ḥarakāt, a HUMAN
notational artifact (not the revealed rasm). This whole lens is therefore DEPRIORITIZED — even a positive
cross-text result would describe editorial vocalization, not the revealed text. Retained as instrumented
+ internally validated, but NOT a priority; do not pursue vocalized comparators as a main line. Priority =
revealed layers: rasm, roots, words, āyah/sūrah structure, canonical order. See DESIGN_STANCE.md. ***


================================================================================
## #50 — MODALITY 15 / Lens 15: MUQATTA'AT / RASM POINTER (divinely-rooted)  → POSITIVE structural result
================================================================================
First lens BUILT to the divine-rootedness control: revealed text only (rasm, disjoint opening letters,
canonical sūra order; NO ḥarakāt). 29 muqaṭṭaʿāt sūras; permutation nulls; gate-validated.
Script: sequence_tests/muqattaat_pointer.py.
  A) BEARER ENRICHMENT — opening letters appear at 1.064x their corpus rate in their OWN sūra rasm;
     null (random same-size letter sets) 1.006; z=+2.17, p=0.024. Modest aggregate, CONCENTRATED in
     single-letter sūras: ق/S50 1.73x, ص/S38 1.46x, ن/S68 1.24x (the classic 'ق lead'). Multi-letter sets
     incl. super-common ا/ل dilute toward 1 — the signal lives in the distinctive letters.
  B) HALF-ALPHABET — distinct letters across all muqaṭṭaʿāt = 14 of 28 (نصف الحروف). CONFIRMED
     (احرسصطعقكلمنهي). Clean structural fact of the revealed text.
  C) MUSHAF CONTIGUITY — 29 muqaṭṭaʿāt sūras form 19 canonically-adjacent pairs vs null mean 7.1
     (random 29-subsets of 1..114), p<0.0001. Strong position-clustering; reproduces the pointer headline
     (cf. app Disjoint-Letters label-permutation p≈2e-5).
  GATE: positive control (most over-represented letter per sūra) fires 1.49x; negative (random) 1.01x. Valid.
VERDICT: POSITIVE. A validated INTERNAL design structure of the revealed text (sui generis — no ordinary-
Arabic muqaṭṭaʿāt baseline; nulls are permutation). The SECOND positive structural result alongside #42
recurrence, and the divinely-rooted KIND of target the control prioritizes. Strongest piece = position
contiguity (C, p<1e-4); half-alphabet (B) exact; bearer enrichment (A) modest-but-significant.
CAVEAT: these are organizational/positional facts of the revealed text, not cross-text STYLE distinctives;
the right framing is 'designed internal structure', validated against permutation nulls.


================================================================================
## #51 — MUQATTA'AT POINTER DEEPENED (Lens 15 sharpening; divinely-rooted, rasm only)
================================================================================
Script: sequence_tests/muqattaat_deepen.py. Three sharpenings, permutation-nulled:
  A) MORAN'S I (1-D spatial autocorrelation, rook adjacency) of the 29-sūra indicator over canonical
     order 1..114 = +0.539, z=+5.80, p<1e-4. Rigorous form of #50's contiguity — strong clustering.
  B) ROBUSTNESS under NUZŪL (revelation) order: Moran's I +0.306, p<1e-4; contiguity 14 pairs vs null
     7.1, p=0.001. The clustering SURVIVES re-ordering (NOT merely a canonical-arrangement artifact) but
     is STRONGER in muṣḥaf order (0.54 vs 0.31) — partly chronological, amplified by the canonical order.
  C) PER-LETTER bearer enrichment concentrated in DISTINCTIVE/emphatic letters: ط 1.25x, ق 1.24x,
     ن 1.24x, ص 1.18x; ubiquitous ا/ل/م ~1.0 (ك 0.00x is n=1 noise, S19). The 'ق lead' = a distinctive-
     letter lead. (Multi-letter sets w/ common letters dilute, as in #50.)
VERDICT: the muqaṭṭaʿāt pointer is ROBUST (survives ordering) and SPATIALLY strong (Moran z=5.8). Stays
the 2nd positive, divinely-rooted result. Next rasm extensions: alt chronologies (Nöldeke), letter-group
phonetics (why these 14), signal-geometry on rasm/roots/positions.


================================================================================
## #52 — MUQATTA'AT PHONETIC-BALANCE ('half of each category' claim)  → PARTIAL / NOT distinctive
================================================================================
Script: sequence_tests/muqattaat_phonetic.py. Tests the popular claim that the 14 letters take ~half of
each phonetic category. (Voicing/articulation are intrinsic to the revealed consonants — not ḥarakāt; the
sifa taxonomy is a human description of intrinsic sounds. Within the divine-rootedness control.)
OBSERVED splits (muqaṭṭaʿāt take k of class): mahmūsa 5/10 (EXACT half), iṭbāq 2/4 (exact), shadīda 4/8
(exact), qalqala 2/5, ḥalqī 4/6, shafawī 1/4. Voicing: 5/10 voiceless + 9/18 voiced = EXACTLY half each.
PERMUTATION TEST (balance deviation vs random 14-subsets, 20k): obs dev=5.0 vs null 9.9±3.7, z=-1.34,
p=0.137. So the set IS more balanced than chance but NOT significantly (sub-2σ); throat/labial deviate.
VERDICT: the 14/28 cardinality is exact (#50) and voicing/emphatic/stop split exactly in half (individually
striking), BUT the aggregate 'half of every phonetic category' claim is NOT statistically distinctive
(p=0.14; multiple features -> some exact halves by chance). No phonetic-structure signal beyond cardinality.
The real muqaṭṭaʿāt result stays the POSITIONAL pointer (#50/#51). Honest tempering of a popular claim.


================================================================================
## #53 — SIGNAL-GEOMETRY ON ROOTS: muqaṭṭaʿāt ROOT-SPACE cohesion  → POSITIVE (strengthens the pointer)
================================================================================
Script: sequence_tests/muqattaat_rootspace.py. Each sūra -> root-TF-IDF vector; cohesion = mean pairwise
cosine; null = random sūra-subsets of same size. Divinely-rooted (roots, not ḥarakāt); Qur'an-internal.
RESULTS (mean cosine | null | z | p):
  all 29 muqaṭṭaʿāt: 0.530 | 0.251 | z=+6.92 | p<1e-4   (~2x more root-similar than random sūra-sets)
  Ḥā-Mīm group (7):  0.545 | 0.253 | z=+3.08 | p=0.003
  Alif-Lām-Rā (5):   0.565 | 0.252 | z=+2.68 | p=0.010
  Alif-Lām-Mīm (6):  0.599 | 0.252 | z=+3.27 | p=0.003
VERDICT: the muqaṭṭaʿāt grouping is NOT merely positional — it is strongly coherent in root/semantic space,
and EACH same-letter subgroup is internally cohesive beyond chance. The opening letters track LEXICAL-
THEMATIC families (same-letter sūras share root content). Strengthens the #50/#51 pointer into a
position+content structure. CAVEAT: muqaṭṭaʿāt are mostly Meccan -> part of the 29-set cohesion is shared
register; but same-letter subgroups being TIGHTER than the 29-set average (0.55-0.60 vs 0.53) argues for
letter-specific structure beyond register. (A Meccan-only null would tighten this — next refinement.)


================================================================================
## #54 — MECCAN-CONTROLLED null for muqaṭṭaʿāt root-space cohesion  → CAVEAT RESOLVED, effect STRENGTHENS
================================================================================
Script: sequence_tests/muqattaat_rootspace_meccan.py. Re-ran #53 drawing null subsets from MECCAN-only
sūras (Medinan set ~28 excluded), to isolate letter-specific cohesion from shared Meccan register.
26 of 29 muqaṭṭaʿāt are Meccan (Medinan: 2,3,13). RESULTS (cos | Meccan-null | z | p):
  Meccan muqaṭṭaʿāt (26): 0.518 | 0.221 | z=+7.35 | p<1e-4   (STRONGER than the all-corpus null z=+6.9)
  Ḥā-Mīm (7):            0.545 | 0.221 | z=+3.58 | p=0.001
  Alif-Lām-Rā (5):       0.565 | 0.220 | z=+3.18 | p=0.007
  Alif-Lām-Mīm (29-32):  0.511 | 0.222 | z=+2.34 | p=0.026
VERDICT: the root-space cohesion is NOT a register artifact — it SURVIVES and STRENGTHENS against a
Meccan-only null (the Meccan baseline is LOWER, 0.221 vs 0.251, because long Medinan legal sūras inflate
the all-corpus baseline; so muqaṭṭaʿāt cohesion stands out more). Letter-grouping is genuinely letter-
specific lexical-thematic structure. #53 caveat RESOLVED. The muqaṭṭaʿāt pointer = position (#50/#51) +
robust letter-specific content coherence (#53/#54). Strongest divinely-rooted result besides #42.


================================================================================
## #55 — IS THE MUQATTA'AT COHESION ANCHORED IN THE "THE BOOK" THEME?  → YES (content anchor found)
================================================================================
Script: sequence_tests/muqattaat_revelation.py. Do muqaṭṭaʿāt sūras over-express a revelation/"the Book"
root cluster (کتب، نزل، قرء، ءیی[āyah]، وحی، ذکر، بین، تلو، حکم، رسل، نبء، صدق، هدی)? Permutation-nulled.
  WHOLE-SŪRA: muqaṭṭaʿāt REV-root rate 0.0706 vs others 0.0479, diff +0.0227, z=+3.55, p=0.0002.
  OPENING (āyāt 1-3): muqaṭṭaʿāt 0.308 vs others 0.060 — ~5x concentration right after the letters
    (quantifies the classical pattern: e.g. الم ذلك الكتاب 2:1-2; الر كتاب 14:1; الم تنزيل الكتاب 32:1-2;
    حم تنزيل الكتاب 40:1-2; الر كتاب أحكمت آياته 11:1).
VERDICT: the root-space cohesion (#53/#54) is ANCHORED, in part, in a shared theme — scripture announcing
scripture; the muqaṭṭaʿāt are the "Book-announcing" sūras. CAVEAT: explains the COMMON revelation theme,
not the DIFFERENCE between letter-groups (حم vs الر); cohesion z=6.9 > theme z=3.5, so theme is PART of
the cohesion. Per-letter distinctive signatures remain (next). Divinely-rooted, gate-valid.


================================================================================
## #56 — PER-LETTER ROOT-SIGNATURES: are families separable from EACH OTHER?  → NULL globally; thematic at margin
================================================================================
Script: sequence_tests/muqattaat_letter_signatures.py. Multi-member families الم(6) حم(7) الر(5) طس(3).
  GLOBAL SEPARABILITY = NULL: within-group cos 0.574 vs between-group 0.570, diff +0.004, z=+0.30, p=0.37
  (permutation: shuffle family labels among grouped sūras, sizes preserved). Families are NOT distinct as
  whole vectors — the #53 cohesion is a SHARED-theme effect; shared revelation/register vocab dominates the
  TF-IDF vector and swamps letter-specific differences.
  BUT per-family TOP DISTINCTIVE ROOTS are vividly thematic:
    الم -> legal/communal: شری(trade) ربو(ribā) طلق(divorce) حجج(pilgrimage) — Baqara/Āl-ʿImrān legislation
    الر -> Yūsuf narrative: سجن(prison) کیل(measure) سبع(seven) کید(scheming) ءبو(father)
    طس -> Mūsā–Pharaoh: سحر(sorcery) فرعن(Pharaoh) جند(troops) مدن(Madyan) شعر
    حم -> dispute/judgment: فرعن قضی(decree) جوب(response) کبر(arrogance)
VERDICT: NO separable letter→theme cipher (p=0.37). The distinctive roots reflect WHICH NARRATIVES each
group's sūras contain (الر holds Sūrat Yūsuf -> Yūsuf vocab) — confounded with narrative content, NOT
evidence the letter causes the theme. Honest tempering: same-letter sūras share narrative vocabulary
(consistent with #53 cohesion), but no hidden letter-code at the whole-vector level. Closes the muqaṭṭaʿāt
content arc: cohesion is real & theme-anchored (#53/#54/#55); per-letter SEPARATION is not established.


================================================================================
## #57 — CANONICAL-ORDER THEMATIC COHERENCE (signal-geometry, whole muṣḥaf)  → POSITIVE (length-controlled)
================================================================================
Script: sequence_tests/canonical_order_theme.py. Divinely-rooted (roots + canonical arrangement, NO ḥarakāt).
Sūra root-TF-IDF vectors; adjacency = mean cosine between canonically-consecutive sūras; two nulls.
  adjacency cosine = 0.3465
  vs FULL-shuffle null 0.2509 -> z=+10.6 p<1e-4 (BUT muṣḥaf is length-ordered: position↔length r=-0.73, so
    most of this is the length/register gradient — not the interesting claim).
  vs LENGTH-BAND(6) null 0.3282 -> z=+3.14, p=0.0007: preserving the length backbone (shuffle only within
    blocks of 6 consecutive sūras), neighbors are STILL more root-similar than chance. GENUINE LOCAL
    thematic coherence beyond length. Generalizes muqaṭṭaʿāt contiguity to the whole muṣḥaf. Magnitude
    modest (+0.018 over length-controlled baseline) but significant.
NMF (8 themes) recovers interpretable axes: T8 refuge/Muʿawwidhāt (شرر وسوس حسد عوذ زلزل خنس), T3/T5
eschatology (یوم کذب ویل / علم یقن قبر), T2 creed (ءله ءمن کفر رسل), T6 family/tawḥīd (وصی وحد ولد), T7
devotion (عبد دین رحم صرط). Descriptive validation that the decomposition finds real themes.
VERDICT: POSITIVE — the revealed ARRANGEMENT carries thematic coherence beyond the length gradient; a 3rd
divinely-rooted positive (after #42 recurrence, muqaṭṭaʿāt) at whole-muṣḥaf scale. CAVEAT: modest effect;
partly reflects known consecutive thematic groups (Ḥawāmīm, Ṭawāsīn, Musabbiḥāt) — which IS the canonical design.


================================================================================
## #58 — SŪRA-JUNCTION INTERLOCK (tanāsub al-suwar)  → WEAK-POSITIVE (modest)
================================================================================
Script: sequence_tests/sura_junction.py. Classical claim: the END of each sūra links to the START of the
next. End/start windows = 5 āyahs; shared root-TF-IDF; cosine; random-pairing null. Divinely-rooted.
  junction cos(end_k, start_(k+1)) = 0.087 vs random-pairing null 0.070, z=+2.47, p=0.013.
  whole-sūra adjacency (#57) = 0.346 (stronger, general effect); within-sūra end·start = 0.232.
REARRANGEMENT TEST (user-suggested — compare legitimate orderings, full-order-shuffle null 0.071±0.005):
  CANONICAL muṣḥaf order : junction 0.0911, z=+3.98, p<1e-4
  NUZŪL (revelation) order: junction 0.1009, z=+5.92, p<1e-4   ( > canonical by +0.0098 )
VERDICT: seam-interlock is REAL under BOTH legitimate arrangements (both well above random), so consecutive
sūras share seam vocabulary beyond chance — modest support for tanāsub al-suwar. BUT the canonical order is
NOT specially optimized for it: the chronological (nuzūl) order interlocks MORE (same-period sūras share
theme/register). HONEST READING: the muṣḥaf sustains significant seam-coherence DESPITE abandoning the
chronological grouping that would maximize it (coherence against the grain), but seam-interlock is not
evidence of unique canonical design. Overlaps #57; length/period-locality is the main driver. No coverage change.


================================================================================
## #59 — CROSS-IMPACT D3: is muqaṭṭaʿāt root-cohesion SPECIAL?  → NO (general grouping effect; tempers #53/#54)
================================================================================
Back-propagation of D3 (CROSS_IMPACT.md). Applied the #53 root-space cohesion test to other named sūra-groups
vs random same-N null. Script: /tmp/d3.py (-> sequence_tests/group_cohesion.py).
  muqaṭṭaʿāt(29)  cos 0.530 z=+6.8 | al-sabʿ al-ṭiwāl(7) cos 0.778 z=+5.4 | Medinan(28) 0.476 z=+5.4 |
  Ḥawāmīm(7) 0.545 z=+3.1 | Musabbiḥāt(7) 0.392 z=+1.5 n.s. | ḥamdu-openers(5) 0.428 z=+1.5 n.s. |
  closing quls(4) 0.051 z=-1.5 | Meccan(86) 0.221 z=-2.2.
LEARNING (revises prior framing): root-space cohesion is a GENERAL property of length/topically-homogeneous
traditional groupings — the seven long and Medinan cohere as much or MORE than the muqaṭṭaʿāt. So the
muqaṭṭaʿāt CONTENT-cohesion leg (#53/#54) is NOT sui-generis; down-weight it as evidence of design-via-letters
(it is substantially the shared "Book"-theme #55 + register effect). STILL DISTINCTIVE: the POSITION pointer
(#50/#51 Moran's I, contiguity) and the half-alphabet (#50). SURVIVING NUANCE: the letter-defined group is
MORE cohesive than several MEANING-defined groups (Musabbiḥāt, ḥamdu-openers, both n.s.), so its cohesion is
not merely a shared-opening-word effect. Net: muqaṭṭaʿāt = strong on POSITION/CARDINALITY, ordinary on CONTENT-cohesion.


================================================================================
## #60 — E2: fāṣila-CONCEPT stream (does meaning chain at verse-ends?)  → NEGATIVE for special hypothesis
================================================================================
DoE E2. Root embedding from āyah co-occurrence (PPMI + SVD-50); per-āyah pick end/start/random root;
mean cosine of consecutive picks within sūra vs within-sūra shuffle. Divinely-rooted (roots, order).
  verse-START root : mean-cos 0.691, z=+17.6 ; RANDOM root: 0.649, z=+10.0 ; verse-END (fāṣila): 0.625, z=+7.2.
LEARNING: ALL positions chain strongly (general local āyah-to-āyah semantic continuity), but the fāṣila
concept chains the LEAST — meaning does NOT specially chain at verse-ends; the m2 ordering mechanism is not
privileged. NUANCE (new, links Lens 3 × Lens 16): the verse-end word is rhyme-constrained, which partially
DECOUPLES its concept from the semantic flow; verse-STARTS (rhyme-free, often parallel/formulaic) chain
tightest. So rhyme and local semantic continuity TRADE OFF at the fāṣila. No new distinctive; general
adjacency coherence re-confirmed at āyah grain (cf. #57 at sūra grain). Script: sequence_tests/fasila_concept.py.


================================================================================
## #61 — E3: RE-EXPRESSION quantified (edit-distance + Kendall on recurrence pairs)
================================================================================
DoE E3. Top far-cosine 30-root passage pairs (different sūras); order-aware metrics. Sharpens #42.
  RECURRENCE band (cos 0.6–0.95, n=19): edit-similarity 0.270, Kendall(order) +0.42 — high shared content,
  heavily re-sequenced surface = RE-EXPRESSION not copying (confirms #42 with order-aware metrics).
  MODERATE (0.45–0.6): edit-sim 0.088, Kendall +0.21. No verbatim band (>0.95) — verbatim-excluded, as #42.
  Script: sequence_tests/recurrence_editdist.py.

================================================================================
## #62 — fāṣila–CONTENT FIT (munāsabat al-fawāṣil; rhyme-end grouping)  → STRONG POSITIVE (Qur'an-internal)
================================================================================
User-proposed rhyme-end grouping. Does the āyah-FINAL word predict the BODY content? Body-cohesion of
āyahs sharing an ending vs random same-N null; body = roots, with the ending's ROOT stripped (strict
self-repetition control). Two grains for the ending:
  ROOT grain (رحم/حکم/قدر…): mean z=+11.3, 13/14 classes z>2 (رحم +30, قدر +28, حکم +22, ءلم +21);
    control (remove fāṣila-root from body) barely changes it (+11.43→+11.32) — predicts OTHER content.
  MORPHOLOGY grain (user-preferred — رحیم/علیم/حکیم/قدیر/صادقین…): mean z=+12.1, 16/16 z>2
    (قدیر +32, رحیم +29, صادقین +27, حکیم +26, ألیم +18, … متقین +2.4). Wordform captures the faʿīl/-īn
    attribute better than the collapsed root → morphology is the apt unit for the ENDING.
VERDICT: the verse-ending attribute strongly FITS its āyah's body content. RECONCILES WITH #60/E2: the
fāṣila does NOT chain to the NEXT āyah (rhyme decouples horizontally) but strongly CAPS its OWN āyah
(couples vertically). Fuses rhyme (Lens 3) × meaning × wazn (Lens 8 faʿīl attributes).
CAVEAT (key, queued): Qur'an-INTERNAL (random-āyah null); cross-text DISTINCTIVENESS untested — ordinary
prose may also have topic-laden sentence-endings. NEXT (rearrangement protocol): run the SAME test on
comparators (sentence-final word predicts body) to test if the coupling is distinctively strong, especially
as it holds UNDER a rhyme constraint. Scripts: sequence_tests/fasila_content_fit.py (root + morphology).

================================================================================
## #63 — COMPARATOR test for #62 (fāṣila system)  → ending-REPETITION is cross-text DISTINCTIVE (exceeds saj')
================================================================================
Per rearrangement protocol: run the ending→body fit on comparators (surface-word grain). RESULT: the
content-fit cannot be compared DIRECTLY because ordinary Arabic/poetry have ~0 ending-words recurring ≥10×
(the Qur'an has 14+). That gap IS the finding. Equal-N (319 units, 200 subsamples) ending-word repetition:
  QURAN    ending-TTR 0.699  frac-recurs≥3x 0.279
  saj'     ending-TTR 0.699  frac-recurs≥3x 0.038
  ord-Ar   ending-TTR 0.817  frac-recurs≥3x 0.099
  poetry   ending-TTR 0.841  frac-recurs≥3x 0.021
VERDICT: the Qur'an HEAVILY repeats SPECIFIC ending words (28% of āyahs end in a word used ≥3x, vs 2–10%
elsewhere) — and this EXCEEDS saj' too: saj' matches type-level ending variety (TTR 0.699, it rhymes) but
NOT heavy ≥3x repetition of the SAME word. So the fāṣila system is not mere rhyme (saj' has rhyme) but the
distinctive heavy RECURRENCE of specific meaningful attribute-endings — each FITTING its content (#62).
Combined picture (cross-text distinctive): rhyme-persistence (#34–37) + recurrence (#42) + content-fit (#62)
converge at the verse-end. CANDIDATE new Lens (fāṣila system). CAVEAT: content-fit itself stays Qur'an-
internal (comparators can't form ending-groups); the distinctiveness rests on the repetition precondition,
which IS cross-text and exceeds saj'. Script: sequence_tests/fasila_compare.py.
*** #76 CORRECTION (tokenization audit): the 0.279 above was computed on COL_SURFACE = توکن ریشه نحوی,
which is a LEMMA column — asymmetric vs raw-word comparators (lemma collapse merges الرحيم/رحيم/رحيما).
RE-RUN on TRUE SURFACE (nrm of the diacritized text): QURAN 0.179±0.032 vs ord 0.101±0.017, sajʿ 0.038,
poetry 0.019. VERDICT: SURVIVES the second tokenization at REDUCED magnitude (the #43 pattern) — still
~4.7× sajʿ and ~9× poetry; the margin vs ORDINARY narrows to ≈+2.2σ. Corrected headline: 0.18 (surface)
/ 0.28 (lemma grain). RULE locked: cross-text features must use nrm(COL_DIACRITIZED); COL_SURFACE is a
lemma layer (fine Qur'an-internally, e.g. #62's morphology grain — NOT for cross-text). ***

================================================================================
## D2 (cross-impact re-open of #46) — FIELD-RECURRENCE/burstiness  → still NULL (mild)
================================================================================
Re-opened #46 (field SEQUENCING was null) through the recurrence modality: do semantic fields recur in
BURSTS across the sequence? Equal-N (425) Fano factor of field inter-occurrence gaps vs random-position null,
mean over 5 seed fields: QURAN z=+0.59, ord-Arabic −0.09, poetry −1.36, saj' n/a (too few field-units).
VERDICT: mildly positive direction but SUB-significant — #46 region stays null even as recurrence. A clean
"nothing is final → re-checked → still null" outcome. Script: /tmp/d2.py (sequence_tests/field_recurrence.py).

================================================================================
## CROSS-REF — WAZN re-opened at the FĀṢILA (re-evaluate #41 via the fāṣila system)  → register-level (shared w/ saj')
================================================================================
#41 (wazn) was null corpus-wide. Re-evaluated at the VERSE-END: attribute-template (faʿīl/faʿūl/-īn/-ūn,
crude surface detector) share at the ending vs baseline (enrichment), per corpus:
  QURAN end 0.141 base 0.116 enrich 1.21× | saj' end 0.090 base 0.068 enrich 1.32× |
  ord-Arabic 0.085/0.088 enrich 0.97× (none) | poetry 0.044/0.077 enrich 0.56× (depleted).
VERDICT: the Qur'an has the HIGHEST ABSOLUTE attribute-ending density (~1.6× ord, ~3× poetry), but the
END-ENRICHMENT is SHARED with saj' (rhymed prose also clusters faʿīl/-īn at clause-ends; poetry ends on
non-attribute rhyme words). So #41 stays REGISTER-LEVEL even at the fāṣila — wazn-class PRESENCE at the end
is a rhymed-register trait, not Qur'an-unique. SHARPENS #63: the fāṣila distinctive is NOT the attribute
template (saj' matches) but the heavy REPETITION of the SAME specific attributes + their content-fit.
Cross-reference outcome: re-opened a 'final' (#41) → still register-level, but clarified the locus of the
fāṣila distinctive. Caveat: crude surface wazn detector. Script: sequence_tests/wazn_fasila.py.

================================================================================
## E1 — COHERENCE-LENGTH / block-rearrangement curve (where does order live?)  → local (~few āyāt)
================================================================================
DoE E1. (A) mean root-cosine between āyāt L apart (within sūra): lag1 0.074, lag2 0.059, lag3 0.049, lag5
0.044, lag8 0.042, lag13 0.040 ≈ random within-sūra baseline 0.040. Coherence is strongest at immediate
adjacency (~1.8× baseline) and DECAYS to chance by ~lag 8–13 → short, pericope-scale coherence length.
(B) adjacency cosine after within-block shuffle: b=1 0.074, b=2 0.068, b=3 0.064, b=5 0.060, b=8 0.056,
full 0.040 → order carries structure mainly at the FINEST scale; small-block scrambling already erodes most.
VERDICT (descriptive, data-driven): localizes order at the fine/local scale (a handful of āyāt) and
quantifies the coherence length; SHARPENS #57 (canonical-order coherence is a LOCAL effect). Qur'an-internal
(baseline-gated); a comparator decay-curve would be needed to claim the length/strength is distinctive — no
such claim made. Script: sequence_tests/coherence_length.py.

================================================================================
## E1-COMPARATOR — is local coherence DISTINCTIVE?  → NO (ordinary Arabic has MORE); tempers #57
================================================================================
Coherence-length decay on SURFACE words, per corpus (lag-L cosine within document; ratio lag1/baseline):
  QURAN lag1 0.045 base 0.030 ratio 1.50 | ord-Arabic lag1 0.099 base 0.054 ratio 1.82 |
  poetry lag1 0.028 base 0.019 ratio 1.46 | saj' baseline ~0 (degenerate, unreliable).
VERDICT: local thematic coherence is NOT a Qur'an distinctive — ordinary Arabic has HIGHER local coherence
(ratio 1.82 > 1.50; absolute neighbour-similarity 0.099 > 0.045). So #57 canonical-order coherence is
internally real (vs shuffle) but NOT distinctive vs ordinary prose — TEMPER it. Coherent synthesis: the
Qur'an's āyāt are more SELF-CONTAINED locally yet more RECURRENT at long range — its coherence is the
ARCHITECTURE OF RETURN (#42), not local flow. ('Nothing is final': the comparator gate revised #57's reading.)
Script: sequence_tests/coherence_length_compare.py.

================================================================================
## E4 — MANTEL test (position-distance vs content-distance over sūras; canonical vs nuzūl)
================================================================================
DoE E4. Mantel r between sūra position-distance |i−j| and content-distance (1−root-cosine), perm null.
  CANONICAL (muṣḥaf #): r=+0.325, z=+8.5, p<1e-4 | NUZŪL (revelation): r=+0.290, z=+7.6, p<1e-4.
VERDICT: position tracks content in BOTH legitimate orderings (near-in-order ⇒ near-in-content), strongly.
Canonical EDGES nuzūl (+0.325 vs +0.290) — REVERSING #58 (seam-interlock favored nuzūl): coherent reading
= the muṣḥaf optimizes GLOBAL thematic grouping over LOCAL seam-chronology. CAVEATS (no overclaim):
(1) muṣḥaf is length-ordered, so much of canonical Mantel is the content-by-length gradient (only the
length-controlled part, #57, is the genuine thematic signal); (2) per E1-comparator, "position tracks
content" is likely a GENERAL property of organized texts — Qur'an-INTERNAL, not a cross-text distinctive.
The meaningful internal result is the canonical>nuzūl comparison. Generalizes #57 globally. Script:
sequence_tests/mantel_position_content.py.

================================================================================
## D1 — defensible window-fusion (Qur'an vs ordinary Arabic)  → dominated by rhyme-persistence; no fusion gain
================================================================================
DoE D1. Window-of-8-units, rate-based features (no length leak), logistic 5-fold CV. Qur'an vs ord-Arabic.
  univariate AUC: rhyme-persistence 0.863 | attr-ending 0.582 | len-CV 0.578 | local-rep 0.557 | variety 0.557.
  FUSED (5 feats) AUC=0.875. Drop-one-out: −persistence → 0.574 (Δ+0.30); all others Δ≈0.
VERDICT (honest): at this grain, separation is carried almost entirely by RHYME-PERSISTENCE; no synergistic
fusion gain, and the per-window fāṣila/attribute features are weak. PRINCIPLED REASON: the survivors live at
DIFFERENT grains — the fāṣila distinctive (#63) is a CORPUS-level repetition property (not per-window), and
muqaṭṭaʿāt is sūra-level — so a single-grain classifier cannot fuse them. The honest "fusion" is the
conceptual synthesis (FINDINGS_SYNTHESIS.md) + the #35 cell (vs sajʿ AUC 0.96 via persistence+repetition,
the stringent test). CAVEATS: ord-Arabic n=53 windows (small/noisy); vs ordinary prose is the EASY comparator
(no rhyme). Script: sequence_tests/fusion_window.py.

================================================================================
## #64 — NETWORK view of the muqaṭṭaʿāt (multi-grain; network-first per locked principle)
================================================================================
Two graphs. (1) LETTER co-occurrence network (14 letters, edge=co-appearance in an opening): hubs م(32),
ا(28), ل(28), then ر/س/ح/ع/ص; ISOLATE ن (never combined); communities (greedy modularity) recover the
traditional families {ا ر ل}, حم-cluster {ح م ع ق س ط}, {ك ه ي ص}, {ن}. A designed COMBINATORIAL network,
not a flat set. (2) SŪRA CONTENT network (29 muqaṭṭaʿāt sūras, edge=root-cosine>0.3, 395 edges): letter-
family modularity Q=−0.028 vs null −0.032, z=+1.73, p=0.051 (borderline); data-driven communities split the
29 into two groups that CUT ACROSS letter-families.
VERDICT: even in the NETWORK/community framing, content is NOT organized by letter-family → CONFIRMS #56 was
not a linear-method artifact. The muqaṭṭaʿāt distinctive = POSITION + CARDINALITY + LETTER-COMBINATORICS
(real network topology: hubs, isolate, family-communities), NOT content. The network lens corroborated the
absence of per-letter content distinctiveness while revealing the letter-combination topology as genuine
structure. Multi-grain (letter/family/sūra), network (topology/communities/hubs). Script: sequence_tests/muqattaat_network.py.

================================================================================
## #65 — QUR'AN CONNECTOME (root co-occurrence network): integrated ecosystem, emergent fields
================================================================================
Connectome-first / ecosystem principle. Nodes = roots (freq≥4, 915), edges = co-occur in same āyah ≥2× (29,374).
  avg degree 64, density 0.070, transitivity(clustering) 0.364.
  SMALL-WORLD tendency: clustering 0.364 > degree-matched random 0.275 (real local cohesion beyond degree).
  KEYSTONE HUBS (top degree): ءله(768) قول(686) کون(666) ءمن(540) ربب(534) علم(520) قوم(499) ءتی بین شیء کفر ءرض
    — theologically central core.
  INTEGRATION: modularity Q=0.090 (LOW) → NOT siloed; a densely interconnected whole (the ecosystem point).
  EMERGENT communities (recovered, not imposed) ≈ interpretable fields: creation/knowledge (ءله علم شیء ءرض
    کلل جعل رءی) · revelation/speech (قول کون ربب ءتی بین رسل ءیی) · faith/ethics (ءمن نفس عمل رحم وقی) ·
    disbelief/judgment (قوم کفر ءنس یوم عذب ظلم ءخذ).
VERDICT (descriptive, internal): an INTEGRATED small-world ecosystem with theologically-central hubs and
emergent thematic communities — connection without dissolving any node's identity (all roots retained).
CAVEAT: gated vs a degree-preserving null (clustering>random); cross-text DISTINCTIVENESS untested (would
need a surface-word network on comparators). First layer of a multi-relational, multi-grain connectome.
Script: sequence_tests/connectome.py.
--- RIGOR CORRECTIONS (comparator + frequency-normalization) -------------------------------------------
(a) COMPARATOR (equal-N=427 units, surface-word networks): Qur'an clust 0.149 (rand 0.106) Q=0.314 vs
    ord-Arabic clust 0.309 (rand 0.176) Q=0.265. Small-world (clust>rand) is GENERAL — ordinary Arabic is
    MORE clustered. So the connectome TOPOLOGY is NOT a Qur'an distinctive; ordinary raw hubs are pure
    FUNCTION words (في/من/الي) = frequency artifact. (connectome_cmp.py)
(b) FREQUENCY-NORMALIZATION (PPMI edges, not raw counts; the fix): raw-degree hubs = most-FREQUENT roots
    (artifact); PPMI-strength hubs shift (ءله ءمن قوم کفر کلل نفس...). Communities 4→12 (Q=0.248): frequency
    bias had washed out structure; normalization REVEALS interpretable fields (creation/cosmos; faith/
    perception {ءله ءمن ربب قلب ءذن ذکر بصر}; disbelief/punishment; social/law). STRONGEST PPMI EDGES are
    genuine specific COLLOCATIONS, not frequent words: لحم–خنزر–دمو–هلل (forbidden foods 2:173/5:3),
    بکم–صمم (deaf-dumb), قمص–قدد (Yūsuf's torn shirt). (connectome_ppmi.py)
HONEST NET: the connectome is a navigable MAP of the Qur'an's own conceptual ecosystem (normalized → real
associations + emergent fields), NOT a claim of distinctive topology (topology is general; comparator shows
ordinary Arabic more clustered). Frequency must always be normalized (PPMI) or raw counts mislead.

================================================================================
## #66 — LOCAL vs GLOBAL (multi-location) COLLOCATION: two orthogonal axes
================================================================================
For root-pairs (co-occur ≥6 āyahs): PPMI = association strength; sūra-SPREAD (# distinct sūras they co-occur
in) = local↔global. 7024 pairs; sūra-spread median 8, max 61; GLOBAL(≥20 sūras)=594, LOCAL(≤3)=69.
GLOBAL motif-pairs (high spread AND high PPMI — returned to across the whole book): ءرض-سمو heaven-earth
  (61 sūras, PPMI +2.20), شیء-کلل all-things (51, +1.66), ءمن-عمل believe+do-good (50, +1.02).
HIGH-spread/LOW-PPMI = frequency co-occurrence (ءله with قول/علم/کون — God ubiquitous, not specific).
LOCAL formulae (high PPMI, ≤3 sūras): نسو-نکح marriage, حرم-شهر sacred-months, طلق(عرف) divorce (Baqara),
  ءخو/ءبو-ءسف Yūsuf's father/brother-grief — passage-bound narrative/legal collocations.
VERDICT (descriptive): two INDEPENDENT axes — association (PPMI) × locality (sūra-spread) — give quadrants:
global motifs, local formulae, frequency-pairs. The GLOBAL high-PPMI pairs are the conceptual face of
recurrence (#42 — returned-to across the muṣḥaf); the LOCAL high-PPMI pairs are passage-specific. Multi-scale
collocation, frequency-normalized. Script: sequence_tests/collocation_local_global.py.

================================================================================
## #67 — MUQAṬṬAʿĀT NETWORK-FIRST EXTENSION: temporal family-deployment · bipartite combinatorics · transition order
================================================================================
[sequence_tests/muqattaat_network2.py — rasm only, NO ḥarakāt; the three probes from the handoff NEXT list]

Extends #50/#51/#64. Sui generis (no other-Arabic muqaṭṭaʿāt exists), so the admissible comparator is the
randomization null itself (per #50/#51 precedent); REARRANGEMENT (canonical vs nuzūl) baked into probe 1.
GATE: rasm strips ḥarakāt (الٓمٓ→الم, OK); alphabet recovered 14/28; the structure-destroying shuffle IS the
negative control, and probe 2's recovery of the known traditional families under a proper null doubles as
the positive control of the method.

(1) TEMPORAL / DYNAMIC FAMILY DEPLOYMENT — family = identical opening ({الم:6, الر:5, طسم:2, حم:6});
    metric = mean within-family pairwise rank-distance among the 29; null = 20k rank-shuffles:
      canonical: 4.93 vs null 10.00, z=−4.66, p=0.0001
      nuzūl    : 4.20 vs null 10.00, z=−5.31, p<1e−4
    Families are tightly BLOCKED in BOTH orders — and at least as tightly in revelation TIME as in the
    muṣḥaf (the ḥā-mīm seven near-consecutive in nuzūl; الم in its two known blocks 2–3 / 29–32). Extends
    #51's nuzūl-robustness from the 29-set indicator to the FAMILY grain: the letter-system was deployed
    in coherent temporal WAVES, not scattered across the revelation.

(2) BIPARTITE sūra×letter (29×14, 78 edges) vs DEGREE-PRESERVING null (checkerboard swaps, 2k samples —
    every sūra keeps its letter-count AND every letter its bearer-count):
      whole-combination REUSE (entropy of distinct-row distribution): 3.319 bits vs null 4.635, z=−12.55, p<5e−4
      letter-projection modularity (greedy): Q=0.280 vs null 0.083, z=+6.94, p<5e−4
      nestedness (NODF-like): 22.5 vs null 34.1, z=−6.99 → significantly ANTI-nested
    The system reuses 14 whole combinations VERBATIM (الم×6, حم×6, الر×5) vastly beyond degree-matched
    chance; the letter-families are REAL communities under a proper null (upgrades #64 from descriptive to
    nulled); and the topology is MODULAR, NOT nested — the letter-blocks {الر}/{حم-cluster}/{كهيعص}/{ن}
    PARTITION the alphabet rather than nesting inside one another. Designed combinatorics, properly nulled.

(3) RASM LETTER-TRANSITION directed graph — the 14 distinct combos as ORDERED sequences; null = within-
    sequence shuffle ×20k (multiset & length preserved, only ORDER destroyed):
      distinct transitions: 17 vs null 21.3, z=−3.54 (transitions REUSED across combos)
      transition entropy: 3.887 vs null 4.354, z=−4.20, p=0.0006 (concentrated on few motifs)
      one-directionality: 1.000 vs null 0.884, z=+1.83, p=0.0625 (every letter-pair flows ONE way only —
        striking but sub-2σ as a lone statistic)
    Letter ORDER carries structure beyond the multiset: the combos are built from a small set of reused
    ordered motifs (the ا→ل backbone branching to ر/م, then م→ر/م→ص; ح→م; ط→س/ط→ه) and no transition is
    ever reversed anywhere in the system. The gated signals are transition REUSE and CONCENTRATION.

VERDICT: three gated POSITIVE sharpenings of the sui-generis layer (Lens 15). The muqaṭṭaʿāt structure is
now: half-alphabet CARDINALITY (#50) + POSITION (#50/#51) + COMBINATORICS (whole-combination reuse, modular
anti-nested families, ordered transition motifs — #64→#67) + TEMPORAL family-block deployment (#67). Content
remains NOT letter-organized (#56/#64). BOUNDARY: all Qur'an-internal (sui generis; randomization-null
comparator) — design properties of the revealed text, not cross-text style claims. CAVEATS: probe 1's
canonical clustering overlaps #51's contiguity at the set grain (the FAMILY grain and the nuzūl-wave reading
are the new content); probe 3's reuse partly reflects the shared ال-prefix architecture (that IS the
structure, named plainly); one-directionality alone is sub-2σ. No coverage change (deepens an opened region).
Script: sequence_tests/muqattaat_network2.py (CLI probe selection "123"; /tmp run discipline per GOTCHA).

================================================================================
## #68 — WITHIN-OPENING LETTER ORDER follows the ABJADĪ (ancient-alphabet) key
================================================================================
[sequence_tests/muqattaat_abjad_order.py — rasm only; ORDERS tested, no numerology (no abjad VALUES)]

QUESTION (CROSS_IMPACT D9, from #67's perfect one-directionality): is the letter ORDER inside each
muqaṭṭaʿāt opening correlated with a known key — modern hijāʾī alphabet, ABJADĪ order (the ancient Semitic
letter sequence ابجد هوز حطي كلمن سعفص قرشت, historically PRIOR to the hijāʾī shape-resorting), or corpus
body-frequency rank? Six hypotheses (3 keys × 2 directions), selection-corrected via max-over-keys null.
GATE: planted abjadī-sorted sequences read 1.000; random key ~0.4; null = within-sequence shuffle
(multiset & length preserved). 45 key-distinct pairs over the 11 multi-letter distinct combos.

RESULTS:
  abjadi-asc : 0.889 (40/45 pairs)  z=+4.32  p<1e-4   <- THE KEY
  freq-desc  : 0.644                z=+1.60  p=0.069  (sub-2σ)
  hijai-asc  : 0.578                z=+0.86  p=0.237  (chance)
  SELECTION-CORRECTED (max over 6 keys): p=0.00005.
  ROBUSTNESS per-sūra weighting (الم×6, حم×6 …): 0.925 (74/80 pairs), z=+6.60, p<1e-5 — strengthens,
  because the abjadī-perfect families (الم الر المر المص حم) are the most-reused combos.
  VIOLATIONS (5 pairs, named): كهيعص (ك placed FIRST against ه/ي), طه, طسم (س before م), حمعسق (ع before س).
  STRUCTURE NOTE: the transition graph is NOT a global DAG — one 3-cycle م→ع→س→م — so NO total order can
  sort all openings; abjadī is the dominant but not exceptionless key.

VERDICT: POSITIVE (gated, selection-corrected). The openings' internal letter order tracks the ANCIENT
alphabet order — not the later Arabic didactic (hijāʾī) order, and not frequency. This EXPLAINS #67's
one-directionality (pairs never reverse because openings are mostly sorted by one fixed ancient key) and
joins the half-alphabet cardinality (#50) as a second alphabet-SYSTEM property: the muqaṭṭaʿāt relate to
the alphabet as an ordered system, in its oldest attested ordering. Lens 15 sharpened: cardinality +
position + combinatorics + temporal deployment + ABJADĪ-ORDERED spelling.
BOUNDARY: Qur'an-internal/sui generis (randomization-null comparator); the abjadī key is a historical-
linguistic object (ancient letter SEQUENCE), explicitly not letter-VALUES — the numerology door stays
closed (gimmickry-guard, cf. #52's failed phonetic balance and the declined 114-numerology). The 5
violations are reported, not explained; كهيعص is the main outlier (its ك also breaks DAG-ness upstream).
Scripts: muqattaat_abjad_order.py. EVIDENCE #68; D9 follow-up DONE.

================================================================================
## #69 — CALIBRATING #68: abjadī is NEAR-OPTIMAL; no secondary key; violations are local
================================================================================
[sequence_tests/muqattaat_order_optimum.py — exact optimum via bitmask DP over all 14-letter orders]

(1) CEILING: the maximum concordance ANY total order could achieve is 0.978 (44/45) distinct /
    0.975 per-sūra — the م→ع→س→م 3-cycle makes exactly one pair unsortable by ANY key. The data-fit
    optimal orders are overfit strings (احطلمركهيعسصقن), not a known historical object.
(2) RANK of the a-priori key: abjadī (0.889) is matched/beaten by only ~436 of 1e6 random total orders —
    TOP ~0.04% of the full permutation space (per-sūra 0.925: top ~0.05%) — and sits 4 pairs below the
    absolute ceiling. An externally given, historically prior key landing this close to the overfit
    optimum is the cleanest possible statement of #68's strength.
(3) SECONDARY-KEY SWEEP: makhārij (articulation-point order, deepest-first): 0.644 / 0.738 — sub-2σ;
    articulation does NOT explain the violations. (Frequency already sub-2σ in #68.)
(4) VIOLATION ANATOMY (descriptive, no claim): every deviating combo is exactly ONE local move from its
    abjadī-sorted form — حمعسق adjacent swap ع↔س; طسم swap س↔م (dist 2); طه swap ط↔ه (dist 2); كهيعص a
    single fronting of ك (sorted هيكعص → observed كهيعص). Deviations are LOCAL perturbations of one key,
    not a rival system. The fronted ك of كهيعص is the standing outlier — open, unexplained, filed as such.

VERDICT: #68 SHARPENED, not changed. Abjadī is the dominant key at near-ceiling fit and extreme
percentile; no gated secondary key exists for the residue; the residue is small, local, and named.
GATE: planted-sorted input → DP optimum 1.000. Boundary: sui generis / Qur'an-internal as before.
Scripts: muqattaat_order_optimum.py. EVIDENCE #69.

--- STANCE RE-WEIGHT (#68/#69, user-mandated; divine-rootedness control) ---------------------------
The abjadī SEQUENCE is a HUMAN cultural artifact (ancient, but a scribal/cultural convention — same
class as ḥarakāt and Meccan/Medinan labels). Per DESIGN_STANCE, the key-MATCH is therefore
DOWN-WEIGHTED to an interpretive/historical frame (control-grade), not a divinely-rooted design claim.
What remains REVEALED-LAYER and stands: the internal ORDER-CONSISTENCY of the openings themselves —
one-directionality, conserved transitions, reused ordered motifs (#67), and the calibration facts
(#69: near-ceiling consistency with ONE fixed external sequence, top ~0.04% of all orders). Read:
"the openings are internally order-disciplined to near the ceiling" (revealed) + "the best-known
matching key happens to be the oldest attested alphabet order" (human frame, historical interest).

================================================================================
## #70 — DEPLOYMENT DYNAMICS: waves generalize PARTIALLY — seals yes (some), stories no
================================================================================
[sequence_tests/deployment_dynamics.py — Moran's I per feature under canonical + nuzūl orders;
 full-shuffle null + WITHIN-PERIOD null (Meccan/Medinan trad. 86/28 nuzūl cut, human label, control-only)]

QUESTION (D9): #67 found the muqaṭṭaʿāt families deployed as temporal blocks. Do other rasm features
arrive in nuzūl waves — (a) fāṣila ending-classes (#62), (b) recurrence anchors (#42/#43)?
METHOD NOTE (honesty): the FIRST run hit the #43 tokenizer trap exactly (Persian ک in the text shattered
words: fragment 'endings' رون/يم/ون, Ibrāhīm count 0). Re-run with the proven normalizer (nl: normalize
FIRST incl. ک→ك/ی→ي, then split). Top-10 ending-classes pre-stated by frequency; Bonferroni×10 applied.
POSITIVE CONTROL: muqaṭṭaʿāt indicator reproduces #51 (I_nuz=+0.306, z=+3.4) AND survives the
within-period null (z=+3.2, p=0.0018) — the letter-waves are FINER than the Meccan/Medinan split.

(a) FĀṢILA ENDING-CLASSES — PARTIAL YES, and the split is informative:
    TRUE WAVES (survive within-period null; Bonferroni-safe):
      تعملون  I_nuz=+0.456 z=+5.2 p<2e-4 (within-period z=+3.3)
      يعلمون  z=+3.3 (within +3.7) · اليم z=+3.5 (within +3.1) · مبين marginal (+2.3, within +2.5)
    REGISTER-ONLY (nuzūl clustering = the gross Meccan/Medinan shift; within-period z≈0):
      رحيم (+2.6 → +0.2) · عليم (+2.4 → +0.4) · الظالمين partial (+2.9 → +1.7)
(b) RECURRENCE ANCHORS — ALL NULL (Mūsā 135×, Firʿawn 74×, Ibrāhīm 69×, Nūḥ 43×, ʿĪsā 25×; all |z|<1):
    the narrative anchors are temporally DISTRIBUTED — the book re-tells its stories CONTINUOUSLY
    across revelation time, in both orders.

VERDICT: deployment-in-waves is NOT a muqaṭṭaʿāt quirk but is also NOT universal — it is FEATURE-
SPECIFIC. Some verse-seal vocabulary deploys in fine temporal waves; some seals are register-level; and
the architecture-of-return characters return throughout the timeline. The anchor-null actually SHARPENS
the central thesis: long-range return (#42) spans revelation time rather than clustering in it — return
is a standing mode of the book, not a phase. CAVEATS: Meccan/Medinan proxy is the traditional human
cut (control-only); smooth within-period drift not fully modeled; sūra-grain rates only (āyah-grain
waves untested). Qur'an-internal (temporal structure of the revealed text; no cross-text comparator
exists for nuzūl). EVIDENCE #70; D9 deployment-dynamics arm DONE.

================================================================================
## #71 — WAVE CONTENT: the same seal is RE-AIMED across revelation time (2 of 3 gated)
================================================================================
[sequence_tests/seal_wave_content.py — āyah-grain follow-up to #70 on the true-wave seals]

METHOD: per seal, āyahs by final word (nl-normalized); 3 nuzūl waves (1D k-means, pre-stated); wave
content profiles (rate-ratio roots, generic + seal-own roots excluded); TEMPORAL SEPARATION = within-wave
− between-wave TF-IDF root-cosine. GATE: planted content-split fires z≈+5.5…+10. DECISIVE CONTROL:
cross-sūra pairs ONLY + sūra-level permutation (kills the sūra-vocabulary-block confound — wave 2 of
تعملون is heavily al-Baqara).

RESULTS (naive → CONTROLLED):
  يعلمون (67 āyahs, 29 sūras): z=+3.91 → z=+3.38 p=0.0005  SURVIVES.
    Arc: Meccan wave = creation-signs ignorance (جعل ءرض سمو رزق قدر) → Medinan = scripture-community
    ignorance (ءمن کتب فرق کفر دین). The polemic's target shifts cosmos → kitāb.
  اليم (46 āyahs, 29 sūras): z=+2.70 → z=+2.48 p=0.012  SURVIVES (Bonf.×3 ≈ .036).
    Arc: past-nations punishment stories (ءمم وعد ظلم ءیی) → covenant-breach (شری قتل کفر) →
    community-era warnings (رسل ءذن ءمن). The threat moves from history into the living community.
  تعملون (50 āyahs, 30 sūras): z=+2.39 → z=+1.23 p=0.12  FALLS — wave-content was substantially the
    al-Baqara block; filed CONFOUND-LIMITED (its naive arc برء/ربب → غفل/کتب → خبر/غیب/عذر noted only
    descriptively).

VERDICT: for يعلمون and اليم the seal-system is dynamically RE-AIMED — same cadence, evolving
referential domain, robust to the sūra confound. RE-READS #62 (cross-impact): the fāṣila content-fit
has a TIME dimension — the seal fits the mission-phase's domain, not one fixed topic; #70's "true
waves" are campaigns, not mere usage-intensity phases. CAVEATS: k=3 pre-stated; nuzūl = traditional
chronology (established rearrangement frame); d-magnitudes modest (~0.01) though gated; Qur'an-internal.
EVIDENCE #71. Scripts: seal_wave_content.py.

================================================================================
## #72 — SIGNAL-GEOMETRY: latent axes of the sūra×root matrix have an ORDER TYPOLOGY
================================================================================
[sequence_tests/sura_root_axes.py — SVD/NMF on 114×857 (49,330 root tokens), normalized per stance]

(1) SPECTRAL DIFFERENTIATION: effective rank 28.51 vs token-reassignment null 20.20±0.24 (sūra lengths +
    root totals preserved), z=+34.5 — sūras carry genuinely distinct root profiles beyond frequency+length.
    BOUNDARY: register-level descriptive (any topical book should differentiate; no comparator run).
    GATE bidirectional: planted exact rank-4 reads 4.0 (5.25 noisy); unstructured Poisson ~35.8.
(2) NMF AXES (k=8) interpretable: narrative/prophetic · creed/faith-polemic · eschatology (یوم ویل فجر) ·
    dhikr/ease devotional · legal/family (وصی ولد مول) · REFUGE (وسوس حسد عوذ زلزل = the Muʿawwidhāt
    component, recovering #57's cluster) · worship/dīn.
(3) ORDER TYPOLOGY (Moran per component over canonical AND nuzūl, 2000 perms; 16 tests, Bonferroni z≳3):
    BOTH orders: narrative C1 (can +5.4 / nuz +6.1), creed C2 (+5.3/+6.3), refuge C7 (+5.6/+3.4).
    CANONICAL-leaning: eschatology C3 (+5.3 vs +2.2) — grouped in the muṣḥaf beyond its temporal order.
    NUZŪL-only: C5 (+0.6/+3.5), C4 (+2.7/+3.7) — revelation-time waves INVISIBLE in the canon.
    NEITHER: C8 (worship/dīn — everywhere, like the mercy-field).
VERDICT: the latent thematic axes are themselves ORDER-TYPED — some arranged canonically, some temporally,
the great creed/narrative axes in both, one axis order-free. One decomposition connects #57 (adjacency),
E4 (grouping>chronology), #70/#71 (temporal waves). Signal-geometry register delivered at this grain.
CAVEATS: NMF axes data-derived (exploratory typology, per-axis permutation-nulled); k=8 pre-stated;
Qur'an-internal. EVIDENCE #72.

================================================================================
## #73 — MULTI-LAYER CONNECTOME: the letter layer is INDEPENDENT of the meaning layer (gated NULL)
================================================================================
[sequence_tests/multilayer_connectome.py — letters↔roots↔āyahs; D8 retest of phonosemantics at root grain]

GATED CORE: do roots that SHARE LETTERS share CONTEXTS? Letter-Jaccard over 954 root lettersets (28-letter
alphabet) vs āyah-grain PPMI co-occurrence (29,456 co-occurring pairs of 454,581). Null = permute the
root→letterset assignment (1000×). GATE: planted coupling on top-200 PPMI pairs fires z≈+15.
  A corr(letterJ, PPMI | co≥2): obs −0.0175, z=−1.74, p₂=0.074  (faintly NEGATIVE)
  B ΔJaccard (co≥2 vs <2):     obs +0.0029, z=+1.23, p₂=0.21
VERDICT: NULL, gate-validated — no form↔meaning coupling at root grain. Confirms the dead phonosemantics
lens (#38) at a second grain and matches #56/#64 (content independent of the letter layer). The sub-2σ
NEGATIVE direction of A is consistent with Arabic root phonotactics (OCP-style dissimilation: similar
letters avoid co-occurring roots) — noted descriptively only. MAP STATS: letter-participation hubs
ر(276) و ل ب م ن; muqaṭṭaʿāt letters avg 127 root-participations vs 75 others (descriptive; the 14
include the commonest consonants). BOUNDARY: lexical layer, Qur'an-internal. EVIDENCE #73.

================================================================================
## #74 — SEAL SWEEP: rate-waves and content-re-aiming are DISSOCIABLE (2×2 typology)
================================================================================
[sequence_tests/seal_sweep_temporal.py — 12 second-tier ending-classes (≥35 āyahs), #71 control standard
 (cross-sūra pairs + sūra-level perm) built in from the start; Bonferroni ×12]

RESULTS: SURVIVOR = عليم (d=+0.0187, z=+3.52, p=0.0010, Bonferroni-safe). Nominal-only: يعملون (+2.22).
All else NULL — incl. مبين (z=−0.72: its #70 marginal rate-wave carries NO content shift) and رحيم
(+0.22: content-stable wherever it appears — fitting for the pervasive mercy-field).

THE 2×2 TYPOLOGY (with #70/#71) — usage-rate waves × content re-aiming are INDEPENDENT dimensions:
   BOTH:         يعلمون · اليم
   RATE only:    تعملون (wave usage, content fell to the sūra-block confound)
   CONTENT only: عليم (register-only in rate, yet re-aimed in content)
   NEITHER:      مبين رحيم الظالمين قدير يءمنون … (stable formulas)

عليم ARC (descriptive): Meccan = knowledge-CONTEST narratives (سحر حکم ربب — incl. the ساحر عليم
sorcerer-epithet verses 7:109/112, 26:34/37) → early-Medinan = covenant/legal audit (کتب 12×, شهد 8×)
→ late-Medinan = community purification & grace (زکو نور فضل; 9:103).
METHOD CATCH → cross-impact: ending-word classes are REFERENT-MIXED — عليم caps divine attributes AND
the sorcerer-epithet; part of its temporal shift is referent-composition. #62-style seal-semantics
analyses should SPLIT classes by referent before claiming. CAVEATS: k=3 pre-stated; nuzūl traditional;
d small (~0.02) though gated; Qur'an-internal. EVIDENCE #74.

================================================================================
## #75 — THE NUZŪL-ONLY AXES CHARACTERIZED: one gated wave, one honest demotion
================================================================================
[sequence_tests/nuzul_axes_characterize.py — #72's C4/C5 under a robustness gate: within-period control
 (#70 standard) + stability across 10 random-init NMF restarts (axis-match by H-cosine>0.7)]

C4 — EARLY-MECCAN DEVOTIONAL WAVE === GATED POSITIVE.
  roots یسر ذکر عسر صحف شقو صلی زکو غنی سعی غشو; top sūras al-Layl(nuz 9), al-Aʿlā(8), ash-Sharḥ(12),
  al-Muddaththir(4), al-Masad(6), ʿAbasa(24), an-Najm(23), ash-Shams(26). nuzūl I=+0.310: full z=+3.59,
  WITHIN-PERIOD z=+3.20 (p=0.009 — a wave INSIDE the Meccan period). STABILITY 10/10 restarts,
  nuzūl-z=+3.72±0.31. Canonically part-regrouped (the 87–94 run) and part-dispersed (53/54, 74, 80, 111):
  revelation-time has topical BURSTS that the canonical grouping (E4) partially redistributes.
C5 — FIRST-REVELATIONS AXIS === axis stable, WAVE CLAIM FAILS the gate.
  roots ربب رءی صلو عطو علم کذب یتم کثر وجد نهی; top sūras al-ʿAlaq(nuz 1), al-Qalam(2), al-Fajr(10),
  aḍ-Ḍuḥā(11), al-Kawthar(15), at-Takāthur(16), al-Māʿūn(17) — the orphan/prayer/giving cluster of the
  earliest revelations. Recovered 10/10 AS AN AXIS, but temporal clustering is init-dependent
  (nuzūl-z=+1.59±0.78; the seed run's +3.5 was partly init-luck). FILED DESCRIPTIVE ONLY.
VERDICT: one of two survives the full battery — the early-Meccan devotional campaign is the whole-sūra-
grain counterpart of the #71 seal campaigns. The C5 demotion is the restart-battery working as intended
on data-derived axes. CAVEATS: nuzūl traditional; Qur'an-internal. EVIDENCE #75.

================================================================================
## #76 — D1 FUSION RE-RUN + the AUDIT that corrected #63
================================================================================
[sequence_tests/fusion_window_rerun.py — window grain K=25, equal-N, 5 features, logistic 5-fold]

PART 1 — AUDIT (the run's chief outcome): caught a #43-class asymmetric-tokenization confound —
COL_SURFACE is a LEMMA column (توکن ریشه نحوی); #63's 0.279 was lemma-grain vs raw-word comparators.
TRUE-SURFACE re-run: QURAN 0.179±0.032 vs ord 0.101 / sajʿ 0.038 / poetry 0.019 → #63 SURVIVES at
reduced magnitude (corrected headline 0.18 surface; vs-ordinary margin ≈+2.2σ; vs sajʿ/poetry still
4.7×/9×). Correction filed inside the #63 entry; tokenizer RULE locked (cross-text ⇒ nrm(COL_DIACRITIZED);
COL_SURFACE = lemma layer, Qur'an-internal use only).

PART 2 — FUSION with corrected features (rhyme-persistence · ending-reuse · ending-concentration ·
within-window self-similarity · wāw-initial; label-perm gate ≈0.5):
  vs ORDINARY: best single rhyme-persist 0.926; FUSED 0.945 (synergy +0.020)
  vs SAJʿ:     self-similar 1.000 (content-return 0.407 vs 0.145 — sajʿ rhymes but does not RETURN);
               ending-reuse 0.885; FUSED 1.000 (saturated; n=12 windows, small-N flagged)
  vs POETRY:   self-similar 0.961; ending-reuse 0.882; FUSED 0.978 (synergy +0.017)
VERDICT: D1 CONFIRMED with corrected features — no meaningful statistical synergy; the signature is a
PROFILE: each comparator is beaten by a DIFFERENT axis (ordinary by rhyme-persistence; sajʿ/poetry by
content-return + ending-reuse). The real fusion remains the conceptual synthesis + the #35 conjunction
cell. CAVEATS: comparator windows few (12–36, equal-N enforced); wāw = register feature (#45). EVIDENCE #76.

================================================================================
## #77 — REFERENT-SPLIT re-audit of #62 (D11): the fit SURVIVES — and is REFERENT-GENERAL
================================================================================
[sequence_tests/fasila_referent_split.py — pre-stated divine-marker rule (الله/رب*/هو-family within the
 last 6 surface words); #62's exact cohesion statistic per referent-subset, 600 same-N nulls each]

RESULT: #62 PASSES on BOTH sides of the split (15/16 classes; every subset n≥8 fits):
  divine subsets: قدیر +31.2(n=34) · رحیم +29.6(73) · حکیم +24.7(57) · عالمین +19.2(41) · علیم +11.4(68)
  other subsets:  صادقین +27.7(34) · ألیم +16.1(40) · مؤمنین +8.2(52) · مبین +6.5(64) · عظیم +4.1(37)
REFINED READING: the fāṣila content-fit is REFERENT-GENERAL — a property of the seal SYSTEM, not of
divine naming alone. Divine-attribute seals are the strongest fitted subclasses in their divine use;
human/event seals (the ṣādiqīn challenges, the ʿadhāb-alīm warnings) are equally fitted in theirs. 'The
seal that interprets' generalizes: the verse-end names whatever the verse is about, and the naming is
content-fitted either way. FLAG: the ن class (n=1070, a bare final-MORPHEME bucket covering -ūn/-īn
verbs) has the lone non-fitting subset (other side −1.4) — segmentation granularity; exclude bare-affix
buckets from Lens 17 headlines. Composition %s ride the crude (pre-stated) marker rule.

D12 SWEEP VERDICT (same run): COL_SURFACE (lemma) used cross-text in 9 scripts. Filed findings affected:
E1-comparator + #65-comparator — bias runs IN THE QUR'AN'S FAVOR in both (lemma collapse raises overlap/
clustering) and the Qur'an still lost/tied → verdicts ROBUST (conservative direction). wazn_fasila
(#41-reopen, register non-claim): low-priority re-check. Preliminary probes (wavelet/posdir/signals):
no claims to protect. #63: corrected in #76. EVIDENCE #77.

Seed robustness (5 RNG seeds, B=150): mean +2.86sd, sd 0.29, range +2.51 to +3.36 — not seed-driven.
=> FIRMED HEADLINE: varied intratextual recurrence is ~+3sd vs ordinary Arabic at passage grain
   (word-shuffle-controlled, verbatim-excluded), invariant across K/quantile/gap/seed and surviving a
   2nd tokenization. This still CLEARS/approaches the 2sd G10 bar, but the earlier "+3.5-4sd" was a
   fragment-tokenization artifact and is RETRACTED in favour of ~+3sd. Poetry (Mutanabbi) clears
   ~+2sd (same direction) => still NOT unique in kind; the Qur'an MAXIMISES a recurrence-genre trait.
   saj' is unstable around 0 (tiny 44-passage baseline) and does NOT robustly show it.

=== SCALE-UP (good-faith, moderate) ===
The literal ">=300 clean passages/comparator" target is impractical in-session (clean classical
poetry/saj' at ~45k words isn't available via the proven pipelines without huge context cost; archive.org
djvu is noisy OCR). Instead the ordinary baseline was grown with CLEAN BBC-Arabic RSS (corpus/ar_news2.txt,
+811 content-words, 92->109 passages); Q-ord stayed flat at +3.85->+4.11sd, demonstrating baseline-size
invariance. ar_news2 folded into intratext.py's ordinary loop. Robustness is carried by the invariance
battery, not by raw N (the equal-P bootstrap already controls baseline size).

=== #42b SURAH-AWARE VARIATION PROFILE (intratext_variation.py) ===
Promotes #42 from "recurrence exists" to "characterise the variation". Character-anchored narrative
clusters (FIXED tokenization, K=50 content-word passages, surah-tagged):
  Musa موسي: 93 passages across 32 surahs (surah-span 77)   Ibrahim: 49 pass / 22 surahs (span 86)
  Firaun:    46 / 23 (span 84)   Nuh: 29 / 21 (span 67)   Maryam: 27 / 11   Adam: 16 / 8   Lut: 14 / 10
The Musa material alone recurs across 32 of 114 surahs — the long-range narrative backbone of #42, now
named and quantified. Variation metrics on cross-surah pairs (Jaccard=shared content vocab; reorder=frac
discordant order of shared words; verbatim-run=longest shared contiguous token run; gate-validated:
injected substitution & reorder recovered, refrain=off gives reorder~0.01 + run=16):
  QURAN same-character cross-surah:   Jaccard 0.034 | reorder 0.474 | verbatim-run 1.21
  QURAN same-EPISODE (top-cos decile):Jaccard 0.071 | reorder 0.447 | verbatim-run 2.17
  QURAN top-similarity (refrain ctl): Jaccard 0.147 | reorder 0.283 | verbatim-run 5.84
  poetry reused far pairs:            Jaccard 0.006 | reorder 0.325 | verbatim-run 0.41
  ordinary far pairs:                 Jaccard 0.005 | reorder 0.507 | verbatim-run 0.35
INTERPRETATION: the Qur'an returns to the same figures/events across vast spans, sharing 6-12x more
cross-passage vocabulary than poetry/ordinary far pairs — yet even the genuine same-episode retellings
keep verbatim runs SHORT (~2 tokens) and reordering HIGH (~0.45). I.e. the recurrence is carried by
RE-EXPRESSION, not verbatim copying — "the same story told differently each time." The book's actual
verbatim/formulaic repetition lives in a minority "refrain" tail (top-sim pairs, run~5.8, lower reorder),
which #42's verbatim-exclusion correctly sets aside. This is the direct evidence for the "with variation"
craft claim: structured recurrence + high re-sequencing + low verbatim overlap.

=== NET STATUS AFTER #43 ===
#42 stands as the project's strongest single axis but at ~+3sd (not +3.5-4sd): the first axis to robustly
reach the 2sd neighbourhood vs ordinary Arabic, shared in kind with poetry (+2sd), maximised by the
Qur'an, and now CHARACTERISED as re-expressive cross-surah narrative recurrence rather than refrain.
Honest caveat: comparator baselines remain small (poetry/saj' ~42-44 passages); the equal-P bootstrap
controls this but a future clean scale-up of Mutanabbi (aldiwan, Chrome) + full Maqamat would tighten the
poetry/saj' magnitudes further.


## #40 — MORPHO-SYNTACTIC AXIS / ILTIFAT (الالتفات): person/number/tense shift rate — register-level, NULL vs ordinary Arabic. Seventh modality.
[sequence_tests/iltifat_tagger.py, iltifat.py, iltifat_axes.py, iltifat_verify.py]

The grammatical layer, classically the most distinctively-Qur'anic rhetorical stratum. iltifat =
rule-governed shifts of grammatical PERSON / NUMBER / TENSE / addressee between adjacent units
(al-Zarkashi, al-Suyuti). Hypothesis: the Qur'an shifts at a higher RATE and/or a distinctive PATTERN
than ordinary Arabic, poetry, and saj'.

TAGGER (lightweight, raw-text, applied IDENTICALLY to every corpus so its noise is symmetric and
cancels in cross-corpus contrasts): per text-unit, dominant person {1,2,3} from independent pronouns
(أنا/نحن/أنت/هو/إياك/الذين...), vocative يا, and clitic suffixes (ـكم/ـهم/ـها/ـنا high-precision; ـك/ـه
low-weight); number from plural/dual markers; tense from imperfect prefixes vs perfect suffixes.
CALIBRATION: vs the Qur'an's own GOLD morphological segmentation (seg_tokens, where clitics are split
into separate tokens) = 81.0% agreement on dominant person over 5015 both-tagged ayat; coverage 83-87%.
Robust to clitic noise: STRICT mode (single-letter ـك/ـه dropped) gives the SAME 81% and the SAME verdict.

GATE (telescope rule + monotone ladder, PASSED): alternating-person stream 1,2,1,2 -> shift_rate=1.00,
shuffle_z=+7.8 ; cycle 1,2,3 -> 1.00, +5.6 ; blocked runs -> 0.03, z=-10.7 ; constant -> 0.00 ;
random -> 0.71, z=+0.6 (~0). Degradation ladder (block stream, increasing scramble) monotone in z:
-8.3 -> -5.6 -> -0.7 -> +0.2. Detector cleanly separates structured alternation (+z), clustering (-z),
and randomness (~0).

RESULTS — fixed-N=40-unit windows, two unitizations (natural pause-units AND fixed 8-word chunks = G10):
  PERSON shift-rate:  Qur'an 0.478 | ord-Arabic 0.476 | poetry 0.431 | saj' 0.336
     Q vs ord-Arabic  Δ=-0.25sd (NATURAL) / +0.09sd (FIXED8), P(Q>base)=0.44/0.50  -> NULL vs ordinary
     Q vs poetry      Δ=+0.51sd P=0.66 ;  Q vs saj' Δ=+1.07sd P=0.75  -> only a GENRE gap (poetry/saj'
     are more person-monotone; ordinary narrative prose shifts person just as much as the Qur'an).
  NUMBER shift-rate:  Qur'an 0.195 ; vs ord-Arabic Δ=-2.28sd (P=0.07) i.e. Qur'an shifts number LESS,
     vs saj' ~0. The only >2sd cell — but OPPOSITE direction (more number-stable), vs a thin/noisy
     baseline, from the weakest tagger axis. NOT a credible fingerprint.
  TENSE shift-rate:   Qur'an 0.066 ; vs ord +1.07sd, vs poetry +0.84sd, vs saj' -0.93sd -> register/mixed.

DIRECTIONAL PROFILE (person transitions). Net into-2nd vs out-of-2nd asymmetry ≈ 0 EVERYWHERE — a
flux-conservation tautology in any long sequence, so that metric is degenerate (noted, discarded). The
informative quantity is the SHARE of person-shifts that involve 2nd person (direct address):
  Qur'an 0.62 | poetry 0.69 | ord-Arabic 0.40 | saj' 0.42.  Windowed: Q vs ord +0.89sd (P=0.68),
  vs saj' +1.32sd (P=0.82), vs poetry -0.65sd (P=0.28). Qur'an's top transition types are 3->2 (.24)
  and 2->3 (.23): it is markedly ADDRESS-ORIENTED — but this is a POETRY-like trait that lyric poetry
  EXCEEDS, not a Qur'an-unique signature, and it is below 2sd against every baseline.

HAND-CHECK (al-Fatiha, the textbook 3->2 iltifat): 1:5 إِيَّاكَ نَعْبُدُ correctly tagged 2nd (score 4) —
the address pivot is caught; but 1:4 مَالِكِ mis-fires 2nd (ـك false clitic) and 1:7 أَنْعَمْتَ's past-tense
2nd-person ـت is missed. The canonical iltifat is real and visible at the unit grain, but the tagger is
genuinely noisy — and, decisively, it is REFERENT-BLIND: it counts every person-shift, whereas true
iltifat is a REFERENT-CONSTANT shift (the SAME entity named 3rd then addressed 2nd). A referent-blind
rate therefore conflates ordinary topic-changes with genuine iltifat. That confound, not absence of the
device, is why no bulk-rate signal appears.

=== SEVENTH MODALITY, SAME RESULT ===
At equal sample size the Qur'an's morpho-syntactic shifting is INDISTINGUISHABLE from ordinary Arabic
prose on person (the canonical axis), more number-stable (weak/opposite), register-mixed on tense, and
address-oriented in a poetry-like, sub-poetry, sub-2sd way. iltifat behaves exactly like the refrain
finding (#33): a real, artful, LOCALIZED device, not an elevated corpus-wide bulk statistic. No decisive
corpus-wide >2sd single-axis fingerprint — consistent with all six prior modalities. The two standing
control-surviving distinctives are unchanged: STRUCTURED REPETITION (~+1sd) and RHYME PERSISTENCE vs
saj' (+1.7sd).

TELESCOPE-RULE FRONTIER (this modality): the honest test of iltifat needs (a) a GOLD morphological
person/tense tagger (e.g. Quranic Arabic Corpus features) to kill the 81%-tagger noise, and (b) a
REFERENT-RESOLVED layer (coreference) so that only same-referent person-shifts are counted. Both are
buildable but data/tooling-blocked here. Non-detection of a bulk fingerprint is NOT evidence iltifat is
absent — it is below the resolution of a referent-blind text-rate detector.


## #41 — MORPHOLOGICAL-TEMPLATE (WAZN) DISTRIBUTION — register-level (Qur'an +1sd from ordinary, EXACTLY matched by poetry). Eighth modality.
[sequence_tests/wazn_tagger.py, wazn.py]

Does the Qur'an's distribution over DERIVATIONAL TEMPLATES (verb-form I-X, participle/intensive/plural
patterns) differ from ordinary Arabic / poetry / saj' beyond register noise? Arabic is templatic
(root x wazn), so the histogram over patterns is a candidate stylistic fingerprint — and the Qur'an's
density of intensive divine-attribute patterns (فعيل/فعّال/فعول: رحيم، غفور، عزيز...) is a plausible lead.

TAGGER (raw consonantal text, applied identically to every corpus; calibration target = gold seg_tokens):
9 coarse derivational buckets from the de-diacritized skeleton after minimal proclitic strip — X (است/مست),
VII (ان..), MU (م.. participles II-X), AF (ا.. form IV/elative), FAIL (فاعل active participle), INT
(فعيل/فعول intensive/attribute), PLUR (broken plural), BASE (bare triliteral), OTHER. Metric per fixed-N
word window: the wazn histogram, scored as JS-divergence from the global ordinary-Arabic histogram, plus
per-bucket rate sd-gaps.

GATE (PASSED): planted window (all-MU forms) JS-from-ordinary = 0.836 (HIGH) ; null (ordinary re-sample)
JS = 0.004 (~0) ; degradation ladder monotone 0.836 -> 0.417 -> 0.207 -> 0.085 -> 0.006 as the window is
mixed back toward ordinary. The divergence detector cleanly separates a distinct template profile from
sampling noise.

RESULTS — fixed-N=300-word windows; G10 confirmed across TWO tokenizations (raw; enclitics-stripped):
  JS-from-ordinary:  Qur'an 0.017 (Δ=+1.00sd vs ordinary's own self-divergence, P=0.77)
                     poetry(Mutanabbi) 0.018 (Δ=+1.07sd)  |  saj' 0.008 (Δ=-0.64sd)
     Tokenization #2 (enclitics stripped): Qur'an +0.94sd, poetry +0.95sd, saj' -0.52sd — SAME verdict.
  POSITIVE CONTROL: poetry DOES diverge from ordinary (+1.07sd) -> wazn is not fully mastery-blind; it
     carries some genre signal. But the Qur'an's divergence is NO LARGER than the poetry master's, and
     both sit at ~+1sd, BELOW the 2sd admissibility bar. So the Qur'an's template profile is distinct
     from ordinary prose to exactly the same, register-level degree that a poetry master's is — not a
     Qur'an-specific fingerprint.
  PER-BUCKET (Q vs ord): all |Δ|<1sd EXCEPT FAIL (bare 4-letter active-participle شكل): Qur'an 0.006 vs
     ord 0.021, Δ=-2.0sd, robust across both tokenizations. But this is (a) a TINY bucket, (b) NEGATIVE
     direction (a positive distinctive would be elevation, not depletion), and (c) a classifier-granularity
     effect: Qur'anic active participles overwhelmingly occur in PLURAL/derived forms (الصابرين،
     المؤمنون، المفلحون) that fall in MU/OTHER, not the narrow bare-فاعل bucket. It is not "the Qur'an
     avoids active participles." OTHER is correspondingly +1.5sd (Qur'an skews to longer/derived forms
     outside the coarse buckets). No positive corpus-wide >2sd template distinctive.

=== EIGHTH MODALITY, SAME RESULT ===
The Qur'an's morphological-template distribution differs from ordinary Arabic only at the register level
(+1sd JS), a divergence a poetry master matches exactly, with no positive >2sd bucket. Consistent with
all seven prior modalities. Standing control-surviving distinctives unchanged (structured repetition
~+1sd; rhyme persistence vs saj' +1.7sd). TELESCOPE caveat: the tagger is a coarse 9-bucket consonantal
classifier (large shared OTHER); a GOLD morphological analyser (CAMeL/Farasa/Quranic Arabic Corpus wazn
labels) could sharpen per-pattern resolution — but the whole-distribution verdict (register-level,
poetry-matched) is unlikely to move, since even a perfect classifier still measures the same proportions.


## #42 — INTRATEXTUAL NARRATIVE RECURRENCE — *** FIRST POSITIVE >2sd CONTROL-SURVIVING SINGLE-AXIS DISTINCTIVE ***. Ninth modality.
[sequence_tests/intratext.py]

Tests the Qur'an's signature of RETELLING the same stories/themes across DISTANT passages WITH VARIATION
(Mūsā across al-Baqara/al-Aʿrāf/Ṭā-Hā/al-Qaṣaṣ; Nūḥ, Ādam, the punished nations...). Signature = a heavy
upper tail of LONG-RANGE passage similarity (a few far-apart passages spike) ABOVE the far-pair median —
which separates genuine RECURRENCE from mere topical homogeneity (uniformly high similarity).

METHOD: passages = consecutive 50-content-word chunks (function words dropped); passage TF-IDF cosine.
recurrence_excess = (95th-pctile far-pair cosine) - (median far-pair cosine), far = |i-j| > P/4.
FAIRNESS: EQUAL passage count P=40 per corpus via bootstrap subsampling (controls the 77k-vs-3k word
size asymmetry and multiple-comparison inflation). TWO decisive controls:
  (i)  WORD-SHUFFLE null: shuffle all content words, re-chunk -> preserves unigram frequency, destroys
       passage co-occurrence. real-minus-shuffle = recurrence BEYOND the Qur'an's known repetitive
       vocabulary (i.e. NOT just the #28 repetition signal re-expressed).
  (ii) VERBATIM-EXCLUSION: drop far-pairs with cosine > 0.9 -> tests VARIED (non-identical) recurrence,
       so the signal cannot be the verbatim refrains of #33.

GATE (PASSED): on exactly-P synthetic sets, planted-twin ladder is MONOTONE (excess 0.073 -> 0.073 ->
0.075 -> 0.087 -> 0.087 for 0/1/2/4/6 distant near-duplicate passages); word-shuffled ordinary drops to
0.030 (the metric detects passage coherence). Modest sensitivity per planted twin, correct direction, null low.

RESULTS — equal P=40, 80 bootstraps, real-minus-wordshuffle (recurrence beyond unigram repetitiveness):
  QURAN            real 0.185 | wshuf 0.128 | RESIDUAL +0.057  ->  Δ = +3.98sd vs ordinary, P=1.00
  ord-Arabic       real 0.031 | wshuf 0.034 | residual -0.003  (≈0, as expected: no long-range recurrence)
  poetry(Mutanabbi) real 0.032 | wshuf 0.026 | residual +0.006 ->  Δ = +2.01sd, P=0.90
  saj'(Ham+Har)    real 0.045 | wshuf 0.038 | residual +0.007 ->  Δ = +1.36sd, P=0.85
  VERBATIM-EXCLUDED (cos>0.9 dropped): Qur'an residual +0.056, Δ = +3.55sd vs ordinary — essentially
  UNCHANGED. In a random 40-passage subsample, frac(far-pair cos > 0.9) = 0.000; the recurrence lives in
  the 0.5–0.9 band (18% of far-pairs, median 0.366). => the signal is VARIED retelling, not refrains.

INTERPRETATION (and honest scope of the claim):
  * This is the FIRST metric in the entire program (#18-42) to put the Qur'an >2sd above ordinary Arabic
    on a single axis with BOTH a same-language baseline AND a structure-destroying null surviving. The
    long-sought magnitude (the repetition axis was stuck at ~+1sd in #28) appears once repetition is
    measured at PASSAGE grain, tail-focused, equal-N, and shuffle-controlled: +3.5–4sd.
  * It is NOT a brand-new independent modality: it is the project's central STRUCTURED-REPETITION /
    recurrence distinctive, measured more powerfully. So #42 SHARPENS the headline rather than adding an
    orthogonal axis.
  * It is NOT unique to the Qur'an in KIND: poetry also clears 2sd (+2.01sd) — Mutanabbi reuses thematic/
    figurative material across the dīwān. The honest statement is "the Qur'an MAXIMISES a varied-recurrence
    trait that recurrence-genres (poetry) share," with the Qur'an the highest by a clear margin. This is
    fully consistent with the cross-language finding (#30): the Qur'an's craft axis is structured recurrence.
  * CAVEATS: baseline corpora are small (ord 92 / poetry 43 / saj 46 passages), so the baseline magnitudes
    are provisional; the Qur'an estimate (753 passages) is robust. K=50-word passaging and the 95th-pctile
    tail are design choices; direction is stable but exact sd should be read as provisional.

=== NINTH MODALITY — THE MAGNITUDE BREAKTHROUGH ===
After eight register-level/null modalities, the recurrence axis — properly operationalised at passage
scale with a word-shuffle null and a verbatim-exclusion — finally clears the 2sd bar (+3.5–4sd vs ordinary
Arabic, control-surviving, varied not verbatim). It does not overturn the prior picture; it UPGRADES the
standing central distinctive (STRUCTURED REPETITION) from "~+1sd, below bar" to ">2sd at passage grain,"
while confirming it is a recurrence-genre trait the Qur'an maximises (poetry +2sd) rather than a unique
kind. Standing distinctives now: STRUCTURED / VARIED RECURRENCE (passage-grain +3.5-4sd vs ordinary;
+1sd as bulk rate) and RHYME PERSISTENCE vs saj' (+1.7sd).
[SUPERSEDED by #43: the +3.5-4sd here was inflated by a tokenization bug; corrected magnitude ~+3sd.]


## #44 — MODALITY 10: DISCOURSE / RHETORICAL MACROSTRUCTURE (the macro-rhythm of genres). Tenth modality.
[sequence_tests/discourse.py, discourse_full.py]

The cleanest remaining text-computable lens (handoff option A): does the Qur'an's distinctiveness live in
how it SEQUENCES speech-act MOVES — oath -> narrative -> judgment -> address -> assertion — switching genre
more, and with more pattern, than ordinary prose / poetry / saj'? No parser needed.

METHOD (mirrors #42's shuffle-control, applied to MOVE-LABELS not words). Each unit (Qur'an=ayah;
comparators=punctuation/clause units) tagged with one of 6 moves — OATH, ADDR/command, NARR, JUDG/
eschatology, INT/interrogation, ASSERT — by general-Arabic lexical cues (applied IDENTICALLY to every
corpus so tagger noise is symmetric). Two SEQUENCING statistics on the move-label sequence: SWITCH rate
(adjacent units differ) and transition-MI (normalized I(move_t;move_{t+1})), each compared to the SAME
labels reshuffled, so base-rate move frequencies cancel and only SEQUENCING structure remains. Plus a
RUN-LENGTH excess (block coherence) and a base-rate MOVE-ENTROPY (genre-inventory diversity). Equal-N
windows (W=60 units), bootstrap, vs same-language ordinary baseline.

GATE (PASSED): periodic move-stream -> switch-excess +0.153, MI-excess +0.854 (fires); block-runs ->
switch-excess -0.676 (coherent blocks switch less), MI-excess +0.596; random -> +0.006 / +0.017 (~0 null).
The instrument cleanly separates structured from random move-sequences.

RESULTS:
  SEQUENCING (shuffle-controlled) — the structural hypothesis — NULL:
    Qur'an vs ordinary  switch-excess d=-0.86sd (P=0.28) | transition-MI d=+0.05sd (P=0.54) |
                        run-length   d=-0.14sd (P=0.49).  poetry & saj' likewise null.
    => the Qur'an's ordering of speech-act moves carries NO more structure than ordinary Arabic.
  MOVE-INVENTORY DIVERSITY (base-rate, NOT shuffle-controlled) — distinctive at REGISTER level:
    move-entropy  Qur'an 1.007 | ordinary 0.465 | saj' 0.326 | poetry 0.211.
    Q vs ordinary d=+2.36sd (P=0.95); poetry is the most genre-monotone (d=-1.82sd below ordinary).
    Move-mix: Qur'an ASSERT 64% / NARR 12% / ADDR 8% / JUDG 8% / OATH 4% / INT 2%; comparators are
    85-93% ASSERT. The Qur'an packs far more genres per span — but this is a base-rate/register effect
    (like #28 repetition), NOT a controlled structural signal.

=== TENTH MODALITY, SAME PATTERN ===
Discourse macro-SEQUENCING is null vs ordinary (gate-validated instrument, so a real "tool adequate,
no structural signal" result, per the telescope rule). The genre-INVENTORY diversity is a genuine
register-level descriptive distinctive (+2.4sd) — the Qur'an interleaves oath/narrative/address/judgment
within short spans far more than any comparator — but it is base-rate, not a G10-passing structural
fingerprint. So modality 10 joins 7 of the prior 9 single axes as register-level/null on structure; the
sole control-surviving structural distinctive remains #42 VARIED RECURRENCE (~+3sd, #43-corrected), with
RHYME PERSISTENCE vs saj' (+1.7sd) second. No new corpus-wide >2sd structural single-axis fingerprint.
FRONTIER (this modality): a true argument-structure test needs rhetorical-relation / discourse-parsing
(coordination, subordination, topic-chains) — tooling-blocked like dependency-syntax; the referent-aware
iltifat (#40 frontier) is the adjacent unfinished sub-lens.


## #45 — MODALITY 11: SHALLOW SYNTACTIC COMPLEXITY (parataxis vs hypotaxis). Eleventh modality.
[sequence_tests/syntax_complexity.py]

First probe of the SYNTAX region (dependency-syntax was ~0% — parser-blocked). Done parser-FREE via
surface function-word cues applied IDENTICALLY to every corpus (so tagger noise is symmetric): relatives
(الذي/التي/الذين...), complementizers + conditional/temporal subordinators (اذا/لو/حتي/كي/لان/كلما...),
standalone coordinators (ثم/او/ام/بل/لكن), waw-initial rate (parataxis proxy), and mean clause length on
pause-units. Equal-N windows (W=40 units), bootstrap vs same-language ordinary baseline.

GATE (PASSED): inject relative-marker at known rate -> measured rel/100 recovers it monotonically
(0.05->5.5, 0.10->10.5, 0.20->20.5). The counter is faithful; the question is the cross-corpus contrast.

RESULTS (vs ordinary Arabic, per-100-word densities + mean clause length):
  subordinator/100: Qur'an 2.81 d=+1.22sd (P=0.81) | poetry 3.04 d=+1.35 | saj' 1.74 d=+0.13
  relative/100    : Qur'an 1.35 d=+1.08sd (P=0.76) | poetry 0.43 d=-0.38 | saj' 0.18 d=-1.13
  coord/100       : Qur'an 1.17 d=+0.65sd (P=0.69)
  waw-initial %   : Qur'an 12.9 d=+1.92sd (P=0.90) | poetry 11.9 d=+1.63 | saj' 19.2 d=+2.99
  mean clause len : Qur'an 12.5 d=-0.27sd (~ordinary 14.8) | poetry 4.8 | saj' 3.9 (hemistich/rhyme units)
INTERPRETATION: a register-level syntactic profile, NO decisive fingerprint. The Qur'an embeds somewhat
more than ordinary prose (relatives +1.1sd, subordinators +1.2sd) — notably MORE relative clauses than
poetry/saj' — and is markedly WAW-PARATACTIC (+1.9sd), the famous و-stringing. But every axis is sub-2sd,
poetry matches the subordination, and saj' EXCEEDS the parataxis (+3.0sd: rhymed prose is the most
waw-strung register). So parataxis is an oral/rhymed-register trait the Qur'an shares (and saj' maximises),
not a Qur'an-unique signature; embedding is mid, prose-like. Clause length ~ ordinary prose (the Qur'an is
NOT short-clause like poetry/saj').

=== ELEVENTH MODALITY, SAME PATTERN ===
Shallow syntax is register-level/null on distinctiveness (gate-validated instrument -> honest "tool
adequate, no >2sd signal" per the telescope rule). Standing structural distinctive remains #42 recurrence
(~+3sd); rhyme persistence vs saj' (+1.7sd) second. CAVEAT/FRONTIER: this is a parser-FREE proxy — true
dependency-syntax (dependency distance, tree depth, head-direction, embedding DEPTH not just rate) needs an
Arabic parser (CAMeL/Stanza) and remains the deeper unopened sub-lens; the proxy opens the region partially
(~0% -> ~35%).

================================================================================
## #46 — MODALITY 12: LEXICAL-SEMANTIC / TOPICAL FIELD DYNAMICS  → NULL (register-level)
================================================================================
QUESTION: does the Qur'an move BETWEEN semantic fields (mercy/judgment/nature/law/covenant) with
distinctive SEQUENCING or COHESION vs ordinary Arabic / poetry / saj'? (Largest unblocked lever.)
METHOD (mirrors discourse.py #44): per-unit field label -> shuffle-controlled sequencing
(switch rate, transition MI) + cohesion (run-length) EXCESS = stat(real) - stat(shuffled labels),
so base-rate field frequencies cancel and only sequencing/cohesion structure remains. Equal-N
windows (W=40, B=400). Two taggers for robustness:
  (A) SEED-LEXICON (5 fields + OTHER, normalized general-Arabic seeds).
  (B) DATA-DRIVEN per-corpus TF-IDF -> SVD -> KMeans(K=6) — every unit labeled (no OTHER bias).
GATE: passed — periodic seq -> high MI excess (+0.85); block-runs -> high run excess (+4.3);
random -> ~0 on all three. Detector fires on planted structure, nulls on noise.
RESULTS (QURAN vs comparators, g = sd-gap; P = bootstrap P(Q>comp)):
  Variant A (seed):   switch g=-0.09/-0.26/-0.38 (ord/poet/saj); MI g≈0; run g=-0.02/-0.14/+0.11. All P≈0.4-0.5.
  Variant B (cluster):switch g=+0.41/+0.08/-0.02; MI g=-0.19/-0.06/-0.38; run g=-0.44/-0.24/-0.08. All P≈0.39-0.61.
VERDICT: NULL. Both taggers agree — no distinctive field SEQUENCING or COHESION. If anything the
Qur'an clusters semantic fields slightly LESS than ordinary Arabic (run-cohesion g=-0.44 vs ord in
variant B); poetry shows the most field-cohesion. 12th modality, register-level/null like most
priors. #42 intratextual recurrence (~+3sd) remains the SOLE structural distinctive.
CAVEAT: seed lexicon is Qur'an-register-biased (comparators 83-98% OTHER); variant B (data-driven,
every unit labeled) was added precisely to remove that confound and CONFIRMS the null. Untested
sub-region: passage-grain field COHESION via embedding similarity (semantic_ring LSA), and coarser
(pericope) grain. Coverage lexical-semantic 50->72%; overall ~58->~60%. Scripts: fields46.py (seed),
fields46_clusters.py (data-driven).

## #78 — THE SEAL DICTIONARY (inverted #62; internal instrument)  → the seal system is content-bound CORPUS-WIDE
Agenda item 1 (INTERNAL_RESEARCH_AGENDA.md). All 143 ending-classes in the #62 bounds (8<=n<=300)
scored: class fit-z (#62 statistic, 150 same-N nulls), content PROFILE (log-odds top body-roots vs
corpus background, support >=max(3, 12% of class)), referent share (#77 rule), per-verse fit.
GATE: planted-class z=+134.3 fires; random-class z=-0.0 clean.
RESULT: 87% of classes >2σ, 60% >5σ, median z=+6.5 — content-binding is the RULE of the seal
system, not a property of a few famous seals. Top: تكذبان z=+151.6 (the al-Rahman refrain; bodies=
ءلی ربب) · قدير +35.8 (كل شيء/ملك/موت/حيي/خلق — dominion domain, div .91) · رحيم +32.6 (غفر/توب/رءف,
div .93) · مستقيم +40.7 (صرط/هدی/عبد) · صادقين +26.5 (وعد/دعو/قول challenge contexts, div .13 —
re-confirms #77 referent-generality) · الدين +25.2 (یوم). HONEST NEGATIVES: قليلا/يبصرون/يرجعون/
المجرمون ≈0σ — generic clause-endings, not seals (the dictionary discriminates).
DEVIANTS: 206 verses below the random-baseline median inside z>3 classes — the exegetically
interesting index (e.g. مبين class: 26:195 لسان عربي مبين — the Qur'an describing ITSELF — deviates
from the class's typical usage). Boundary: Qur'an-internal instrument (MAP/INDEX, no distinctiveness
claim); body=roots-minus-final (#62 definition); profiles are doc-rate log-odds, not PPMI.
Artifacts: SEAL_DICTIONARY.csv (143 rows) · SEAL_DEVIANTS.csv (206) · sequence_tests/seal_dictionary.py.
Cross-impact: feeds Āyah-hero seal panel (show class profile + deviant flag); sharpens Lens 17
("the seal interprets" now corpus-wide); #74 typology should be re-read against fit-z ranking.

## #78b — REFERENT-RULE CORRECTION (+ #79, #80: course-build side-findings filed)
#78b: the #77/#78 divine-marker regex missed the DUAL pronoun (ربكما) — caught when the al-Raḥmān
refrain scored div_share 0.00 (module08 build). Rule extended (…|كم|كما|هم|هن); seal_dictionary.py
+ both CSVs regenerated: تكذبان now div=1.00; all other entries and headline stats UNCHANGED
(143 classes · 87%>2σ · median +6.5 · gate +134.3/−0.0). The app's _DIVRE (20_Ayah_Deep_Dive)
patched to match. Lesson: referent rules must cover the full pronoun paradigm incl. duals.
#79: الكافرين = NEW TRUE WAVE — found by a module09 exercise using the verbatim #70 instrument
(NS=5000, within-period null): z_nuzūl=+3.9, WITHIN-period z=+3.6 — survives the control like
تعملون/يعلمون/اليم. Extends the #70 wave family; not in the original pre-stated top-10 set, so file
as exploratory-confirmed (single new test, no multiple-comparison burden beyond the one run).
Source: AppMastery/module09/Module9_Data_Bank.json (computed section).
#80 (observation, Qur'an-internal descriptive): implication asymmetry P(divine-name | عدل-āyah)
= 70.8% vs P(عدل | divine-name-āyah) = 0.9% — a 78× one-way implication (justice talk is
God-saturated; God-talk is far broader than justice). Module03 bank; the Statistics page tile 5c
computes it live. No distinctiveness claim; a striking internal structure worth a lecture.

## #81 — THE قل CENSUS: a proclamation interface with a measurably dialogic core (P8 pre-registered; Qur'an-internal)
================================================================================
SelfTafsir course gap-probe A (P8, pre-registered in the nuance index; feeds course M06). Inclusion
pre-stated: word-grain folded tokens {قل، فقل، وقل} on the diacritized column — replicates 6h's
baseline exactly (gate-equivalent): 308 qul-verses (4.9% of 6,236) · 334 occurrences (قل 295 ·
فقل 18 · وقل 21) · 58/114 sūras (top S6 ×35; S3/S10/S17 ×20; S2 ×17).
PRE-STATED BUCKETS (next-token/context detectors, priority order): question-response 14 (SANITY
PASSED: all 14 qul-bearing يسألونك/يستفتونك protocol cells land here; 79:42 qul-less, outside census)
· creed-declaration (قل هو/الله/ءامنا) 21 · gheyb-redirect (علم/الغيب window) 10 · supplication
(قل رب/اللهم) 9 · challenge-retort (قل فأتوا/هاتوا) 7 · other 247 (narrow detectors, pre-stated).
HEADLINE (gated): 48/308 (15.6%) of qul-verses are RESPONSE-structured (same-verse audience-speech
trigger, pre-stated list) vs 84.4% proclamation — and 15.6% is 2.3× the corpus base rate of 6.8%
(427/6,236): enrichment z=+6.07 (binomial). With previous-verse triggers: 78/308 (25.3%).
READING: قل is predominantly a PROCLAMATION interface; its dialogic core is real and enriched far
beyond chance, with the 14/15 يسألونك protocol (6h) as the strongest cell. Boundary: Qur'an-internal
census + enrichment; no cross-text claim. Label: exploratory/internal (single pre-registered run).
Script: sequence_tests/probe_qul_census.py. Cross-impact: course M06 spine; index P8 → PROBE DONE;
bridges 6h (protocol) to the mediated-speech architecture question.

## #82 — TAKHṢĪṢ DETECTOR (probe): rule↔exception verses are measurably root-linked; إلا typology counted (pre-registered; Qur'an-internal)
================================================================================
SelfTafsir course gap-probe B (decides course M07; the detector flagged OPEN in piece 6f).
STEP 1 CENSUS (raw segmented token, hamza-bearing إلا only — the ألا homograph excluded, 39 occ
flagged): إلا = 661 occurrences in 603 verses (9.7% of corpus); غير standalone 147; ما لم bigram 20.
TYPOLOGY (pre-stated next-token classes): إلا من 46 · إلا هو 39 · إلا ما 35 · إلا قليلا 27 ·
إلا الذين 20 · إلا الله 19 · necessity formula (اضطر…غير) 5 sites · ما لم 20. CENSUS BONUS: the
necessity clause has a FIFTH site — 6:119 — beyond the four catalogued in piece 6f (2:173, 5:3,
6:145, 16:115); the carve-out recurrence is wider than the written record had it.
STEP 2 CROSS-VERSE LINKAGE (18 pre-stated rule↔exception pairs from pieces 6d/6f — wine 2:219→4:43→5:90,
ribā staircase, necessity 4-site pairs, poets 26:224↔227, al-ʿAṣr 103:2↔3, fasting-principle echoes,
speech-ethics; null = 200 sets of size-matched random pairs, root-count ±2): root-Jaccard z=+18.7 ·
root-cosine z=+9.99 · last-word(seal) match z=+21.6 (cross-sūra subset: +17.9/+9.9/+20.7).
HONEST DECOMPOSITION (post-hoc cut, flagged as such): the near-verbatim necessity cells carry the
seal-match entirely; EXCLUDING those 6 pairs the root-echo linkage still fires — Jaccard z=+3.52,
cosine z=+2.67 — seal-match drops to ns. So rule↔exception verse pairs share measurably more root
material than size-matched random pairs even outside the verbatim-recurrence cells.
VERDICT: a measurable rule↔exception linkage EXISTS (z>2 incl. the conservative cut) AND the census
yields a teachable ≥3-construction typology → course M07 GO (10-module shape stands; 9-module
fallback not triggered). CAVEATS: pair list is from the written pieces (pre-stated but few, n=18;
two same-sūra-adjacent pairs included and the cross-sūra subset reported); linkage partly rides
recurrence (#42/#61 substrate) — the probe DETECTS the takhṣīṣ signature, a full classified detector
(exceptive/restrictive/negative-polarity labels) remains the M07 exercise's gold-standard task.
Label: exploratory/internal. Script: sequence_tests/probe_takhsis_detector.py. Cross-impact: piece 6f
status flag (detector OPEN → probe-level linkage measured); course M07 unblocked; necessity 5th site
feeds 6f's next revision. [Probe C of the same run — P3 firm-then-detailed direction on #61-replicated
pairs (17 pairs, probe_firm_detailed.py) — returned an honest NULL both orders (canonical 11/17
z=+1.21; nuzūl 9/17 z=+0.24; densities ~0) and is filed in the course record + index P3, not as a
numbered finding.]
