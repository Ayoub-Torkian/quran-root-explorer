## 5.23 Normalized lenses: the attraction grammar (why raw counts mislead)

One graph is one lens, and the raw co-occurrence lens of §5.22 has a fatal confound: **degree is essentially a function of frequency** — a frequent root co-occurs with many others *by chance alone*, a rare one cannot. Raw counts therefore "bear no fruit" on their own. The remedy, standard in corpus linguistics and in this project's prior work, is to **normalize** — to measure how much more two roots co-occur than their individual frequencies would predict. We apply two normalized lenses (PPMI association and directed conditional probability) alongside the raw one, and they **invert** the §5.22 picture.

**Lens B — PPMI (attraction, frequency-controlled).** Pointwise Mutual Information scores a pair by log₂(observed / expected-by-chance); the positive part (PPMI) keeps the genuine attractions. Ranking the surah's seven roots by **mean PPMI per edge** exactly reverses their raw-degree ranking (Figure 14):

| Root | Raw-degree percentile | Mean PPMI (binding) |
|---|--:|--:|
| *r-b-b* (Lord) | 100 | **0.7** |
| *k-th-r* | 97 | 1.3 |
| *ṣ-l-w* | 94 | 1.7 |
| *ʿ-ṭ-w* | 55 | 2.9 |
| *sh-n-ʾ* | 48 | 5.0 |
| *n-ḥ-r* (hapax) | 4 | 4.5 |
| *b-t-r* (hapax) | 0 | **11.0** |

The lesson is stark. The "giant hub" *r-b-b*, top of the raw ranking, has the **weakest** normalized binding (0.7): the Lord co-occurs with nearly everything *because* He is everywhere, so almost none of those links is distinctive. Conversely the hapax, "peripheral" by raw degree, are the **most specifically bound** roots in the surah. *b-t-r* sits at the very top: it occurs **only** with *sh-n-ʾ*, an exclusive pairing that, tested properly, is the one statistically notable bond (p≈0.0005; §5.26). *n-ḥ-r* is locked to the worship cluster (PPMI 6.1 to *ṣ-l-w*, 2.8 to *r-b-b*). So the corpus does not treat the hapax as lonely outliers; it treats them as words **pinned to a single context** — which is exactly what makes a once-used word interpretable at all.

The normalized lens also cleans up an earlier result. *ṣ-l-w*'s frequency-controlled top associates are *z-k-w* (almsgiving, PPMI 5.1), *b-y-ʿ* (transaction, 4.7), *r-k-ʿ* (bowing, 4.4) and *ṭ-h-r* (purity, 3.4) — the worship cluster, now robust to the frequency confound that clouded §5.8. Table 7 lists each surah root's distinctive associates.

**Lens C — directed implication, *P(B | A)*.** A third lens drops symmetry. Given a root, how often does another appear *with* it? For the hapax the answer is **deterministic**: *P(prayer | sacrifice) = 1.0*, *P(Lord | sacrifice) = 1.0*, *P(hater | cut-off) = 1.0* — wherever *naḥr* occurs, prayer and the Lord are *certainly* present; wherever *abtar* occurs, the hater is *certainly* present. The reverse is tiny (*P(sacrifice | prayer) = 0.01*). The asymmetry is the point: the rare word **implies its context**, not the other way round. The hapax do not float free; each is *determined by* a single, certain setting.

| Root | Distinctive associates (PPMI, frequency-controlled) |
|---|---|
| *b-t-r* (cut off) | *sh-n-ʾ* hate (11.0) — exclusive |
| *n-ḥ-r* (sacrifice) | *ṣ-l-w* prayer (6.1), *r-b-b* Lord (2.8) |
| *ṣ-l-w* (prayer) | *z-k-w* alms (5.1), *b-y-ʿ* transaction (4.7), *r-k-ʿ* bowing (4.4), *ṭ-h-r* purity (3.4) |
| *k-th-r* (abundance) | *f-k-h* fruit (3.0), *gh-n-m* flock/spoils (3.7), *n-j-l*, *f-s-q* transgression (3.0) |
| *ʿ-ṭ-w* (give) | *r-b-b* Lord (1.6) |
| *r-b-b* (Lord) | (diffuse — no strong distinctive partner; mean 0.7) |

*Table 7. Frequency-controlled (PPMI) attraction grammar of the surah's roots. [MEASURED]*

**Honest caveat on the magnitudes.** PPMI is famously **unstable at low counts** — it *over-rewards rare pairs*, so *b-t-r*'s headline 11.0 is high partly *because* both roots are rare and co-occur once. The robust claim is therefore not the exact PPMI number but the **structure** it and the directed lens agree on: the hapax are bound **exclusively and deterministically** to one context (best stated as *P(context | hapax) = 1.0*), while the frequent *r-b-b* is bound **diffusely** to none in particular. Read across all three lenses, the result is consistent and is the genuine fruit of normalization: **raw counts call the hapax peripheral and *r-b-b* central; normalized association reverses both** — the rare words are the tightly, specifically bound ones, and the ubiquitous Lord-root is the diffusely connected one. [MEASURED: the degree/PPMI/conditional figures; INFERRED: that exclusive binding is what makes a hapax interpretable; CONCEDED: PPMI magnitudes are inflated at low counts, so we lean on the directed *P=1.0* and the rank-inversion, not the absolute PPMI value.]

**Validation note (§5.26).** A pre-registered test qualifies this paragraph. Measured against *all* 430 once-occurring roots in the corpus, *b-t-r*'s strongest bond is above median (66th percentile) but *n-ḥ-r*'s is **below** median (10th) — so "the hapax are maximally bound" does **not** hold against hapax in general; what is true is only that, *relative to this surah's own seven roots*, the hapax are the most specifically (not diffusely) tied. The single robust, significant pairing is *b-t-r*↔*sh-n-ʾ* (hypergeometric p≈0.0005); the directed *P=1.0* values rest on single co-occurrences and are reported as suggestive, not significant. The honest residue of this section is therefore the rank-*inversion* (rare words are not the *diffuse* hubs) plus the one *b-t-r*↔*sh-n-ʾ* bond — not a general "maximal binding." **A later robustness audit (§5.29.1) demotes even that bond:** it rests on a single verse (108:3 itself), falls to the 79th percentile under a count-sensitive measure, and has no representation in an independent encoder — so what survives is the *community* structure of the web for attested roots (reproduced ≈14× above chance by that encoder), not this individual edge.
