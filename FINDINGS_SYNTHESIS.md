# FINDINGS SYNTHESIS — the coherent, consistent digest to draw from

Single source of truth for *what we have learned*, organized by verdict class. Stays in lockstep with
`EVIDENCE.md` (raw numbers), `SIX_LENSES_PAPER.md` (narrative, 17 lenses), `COVERAGE_MAP.html` (coverage),
`DESIGN_STANCE.md` (controls). Update this whenever a finding lands or is revised. Data-driven, no overclaim:
every entry = measurement + boundary.

State: 18 LENSES (Lens 18 = temporal deployment, added at consolidation) + rearrangement experiments
(E1–E4) + cross-impact closures D8–D12 + arcs #67–#77 (incl. corrections: #63→0.18 surface; abjadī =
human frame); coverage ~74%. Paper retitled "Eighteen Computational Lenses". MASTERY_REPORT Addendum 4.

---

## 0. Thesis (one paragraph)
The Qur'an's measurable distinctiveness is **structured RETURN at multiple scales** — not ornament,
sound-iconicity, syntactic depth, or local flow. Long-range *varied passage-recurrence* is the central axis;
at the verse-end this concentrates as a *fāṣila system* (repeated, content-fitted attribute-endings) with
*rhyme persistence*; the style isolates only as a *conjunction* (sustained rhyme + no meter + recurrence);
and one *sui-generis, divinely-rooted* layer — the muqaṭṭaʿāt *positional* pointer + *half-alphabet* — sits
outside the stylistic axes. Falsifiable summary: **locally the Qur'an is *less* continuous than ordinary
prose (self-contained āyāt); at long range it *returns* to itself more.** Architecture of return.

---

## 1. DISTINCTIVES (cross-text, gated)
| # | Lens / finding | Measure | Result | Boundary |
|---|---|---|---|---|
| #42/#43 | **Varied long-range recurrence** (Lens 9) | passage re-similarity tail, word-shuffle-controlled, verbatim-excluded | **~+3σ vs ordinary** | shared *in kind* with poetry (+2σ); Qur'an maximises it |
| #61 | …re-expression quantified (E3) | edit-distance + Kendall on recurrence pairs | cos ~0.68 but edit-sim ~0.27 | "same matter, re-sequenced," not copying |
| #34–37 | **Rhyme persistence** (Lens 3) | dominant-fāṣila share over a window | **+1.7σ vs sajʿ** | presence (rhyme itself) is shared with sajʿ |
| #62/#63 | **Fāṣila system** (Lens 17) | ending-word repetition; ending→body content-fit | repeat ≥3× share **0.18 surface** (#76-corrected; 0.28 was lemma-grain) **> sajʿ 0.04**, ord 0.10; fit **z≈+12** | repetition cross-text (vs-ord ≈+2.2σ after correction; vs sajʿ/poetry 4.7×/9×); content-fit Qur'an-internal |
| #35 | **Fusion cell** (Lens 5) | classifier over all axes; rhyme×(non-)meter | **AUC ≈0.94**; pair 0.92 > 0.76/0.84 | only the *conjunction* separates; single axes don't |
| #50/#51 | **Muqaṭṭaʿāt POSITION + half-alphabet** (Lens 15) | 14/28 letters; canonical contiguity | exact 14/28; **Moran's I +0.54**, p<10⁻⁴, robust to nuzūl | *sui generis* (no other-Arabic baseline); POSITION/CARDINALITY only |
| #64 | …muqaṭṭaʿāt LETTER-COMBINATORICS (network) | letter co-occurrence graph | designed topology: hubs م/ا/ل, isolate ن, family-communities {الر},{حم-cluster},{كهيعص} | descriptive; content NOT letter-organized (Q≈0, z=1.73) — confirms #56 in network view |
| #67 | …muqaṭṭaʿāt NETWORK extension (3 probes) | family temporal blocks; bipartite vs degree-null; transition order | nuzūl z=−5.3 / canonical −4.7 (families = temporal waves); combo-REUSE z=−12.6, family-modularity z=+6.9, ANTI-nested z=−7.0; transition reuse z=−3.5, entropy z=−4.2 | Qur'an-internal (sui generis); upgrades #64 to properly-nulled; order carries design, content still not letter-organized |
| #68 | …muqaṭṭaʿāt spelling-order CONSISTENCY | within-opening letter order vs 6 keys (selection-corrected) | order-consistency near ceiling: 0.889/0.925, z=+4.3/+6.6, p_corr=5e-5; hijāʾī ≈ chance | REVEALED layer = the internal order-discipline (explains #67 one-directionality); the matching abjadī key is a HUMAN artifact → key-match DOWN-WEIGHTED to historical frame (stance re-weight); 5 violations named |
| #69 | …abjadī calibration (optimum + sweep) | exact DP ceiling over all orders; 1e6-permutation rank; makhārij sweep | ceiling 0.978 (one pair unsortable by ANY key); abjadī = top ~0.04% of all orders, 4 pairs from ceiling; makhārij sub-2σ | a-priori key near the overfit optimum; violations = one local move each; fronted ك of كهيعص = open outlier |
| #70 | DEPLOYMENT DYNAMICS (nuzūl waves, generalization of #67) | per-sūra Moran's I, canonical+nuzūl, within-period (Meccan/Medinan control) null | seals SPLIT: تعملون z=+5.2 / يعلمون +3.3 / اليم +3.5 are TRUE waves (survive within-period); رحيم/عليم register-only; narrative anchors (Mūsā 135× … ʿĪsā 25×) ALL NULL | feature-specific, not universal; anchor-null SHARPENS the thesis — return spans revelation time, not a phase; Meccan/Medinan = control-only human cut |
| #71 | WAVE CONTENT (āyah grain) | within−between wave cosine; cross-sūra pairs only + sūra-level perm (confound-killed) | يعلمون z=+3.38 p=.0005 (cosmos→kitāb ignorance) · اليم z=+2.48 (nations→covenant→community) SURVIVE; تعملون falls to +1.23 (al-Baqara block) | the seal is RE-AIMED over time — #62's content-fit has a TIME dimension; waves = campaigns; تعملون confound-limited |
| #72 | LATENT AXES order-typology (signal-geometry) | NMF k=8 on sūra×root; Moran per axis over canonical+nuzūl; eff-rank vs token-shuffle | axes interpretable (incl. the refuge component); BOTH-orders: narrative/creed/refuge (z +5..+6); CANONICAL-leaning: eschatology (+5.3 vs +2.2); NUZŪL-only: C4/C5 (+3.5/+3.7); eff-rank z=+34.5 | axes are ORDER-TYPED — one decomposition joins #57/E4/#70; eff-rank = register-level descriptive (no comparator); axes data-derived (exploratory, per-axis nulled) |
| #73 | Letter-layer ⊥ meaning-layer (multi-layer connectome) | letter-Jaccard × PPMI co-occurrence Mantel, root→letterset permutation null; gate z≈+15 | NULL: corr −0.018 (z=−1.74), ΔJ z=+1.23 — no form↔meaning coupling at root grain | confirms phonosemantics-dead (#38) at a 2nd grain (D8); faint negative = OCP-like phonotactics, descriptive; matches #56/#64 content⊥letters |
| #74 | SEAL SWEEP 2×2 typology | 12 second-tier ending-classes, #71 control + Bonferroni | survivor: عليم z=+3.52 (contest→covenant-audit→purification); يعملون nominal; rest null | rate-waves × content-re-aiming are INDEPENDENT axes (both/rate-only/content-only/neither); METHOD CATCH: ending-classes are referent-mixed (ساحر عليم) — split by referent before seal-semantics claims |
| #75 | Nuzūl-only axes characterized | within-period control + 10-restart stability battery | C4 = early-Meccan DEVOTIONAL WAVE (al-Aʿlā/al-Layl/ash-Sharḥ…; within-period z=+3.20; stability z=+3.72±0.31) GATED; C5 = first-revelations axis — stable as axis, wave claim FAILS gate (z=+1.59±0.78), descriptive only | revelation-time has topical bursts the canon partially redistributes; the restart battery is the standard defense for data-derived axes |
| #76 | D1 fusion re-run + #63 AUDIT | window-grain fusion (5 corrected features); lemma-confound audit | AUDIT: #63 corrected 0.28→0.18 (survives 2nd tokenization; vs-ord ≈+2.2σ); FUSION: no synergy (≤+0.02) — ordinary beaten by rhyme-persistence (0.926), sajʿ/poetry by content-return (1.00/0.96) + ending-reuse | the signature is a PROFILE, not a summed score (D1 confirmed); tokenizer rule locked: cross-text ⇒ surface (nrm of diacritized), never the lemma column |
| #77 | #62 referent-split re-audit (D11) | pre-stated divine-marker rule; #62 statistic per referent subset | PASSES both sides: divine قدیر+31/رحیم+30/حکیم+25; other صادقین+28/ألیم+16/مؤمنین+8 | the fit is REFERENT-GENERAL — the seal system fits content whatever it names; ن affix-bucket flagged; D12 sweep: E1-cmp/#65-cmp robust (conservative bias direction) |

## 2. INTERNAL-ONLY / DOWN-WEIGHTED (real vs shuffle, NOT cross-text distinctive)
| # | Finding | Why down-weighted |
|---|---|---|
| #53/#54 → #59 | Muqaṭṭaʿāt content-cohesion (root-space) | a GENERAL grouping effect — the seven long cohere more (cos 0.78); other traditional groups cohere too |
| #55 | Muqaṭṭaʿāt over-express the "Book" theme | internal anchor of the cohesion; not shown distinctive vs comparators |
| #57 / E1 / E4 | Canonical-order coherence (Lens 16) | internally real, but ordinary prose is MORE locally coherent (E1-cmp ratio 1.82 > 1.50); position-tracks-content is general |
| #58 | Sūra-junction interlock (tanāsub al-suwar) | real but modest; nuzūl interlocks *more* — not canonical-specific |

## 3. NULL / register-level (swept, defensible negatives)
Lens 1 repetition as a *bulk rate* (~+1σ) · Lens 2 rings (null) / refrain (local, ~9 sūras) · Lens 4
phonosemantics (null) · Lens 6 prosody at text level (null) · Lens 7 iltifāt (null vs prose; referent-blind)
· Lens 8 wazn (register; also register at the fāṣila, ≈sajʿ) · Lens 10 discourse *sequencing* (null;
move-*inventory* +2.4σ is register-level) · Lens 11 shallow syntax (register; wāw-parataxis +1.9σ, sajʿ
exceeds) · Lens 13 dependency-syntax with real parser (Qur'an *simpler* than prose) · Lens 12 lexical-semantic
field dynamics (sequencing null; field-*recurrence* D2 also null) · #48 directional sub-unit (Qur'an-null).

## 4. BLOCKED / DEPRIORITIZED
Lens 14 recited/phonological — instrument built, Qur'an-internal rhythm real (isochrony; weight-alternation),
but **DATA-BLOCKED** (no vocalized comparators) and **DEPRIORITIZED** (ḥarakāt = human artifact). Deep
dependency-syntax beyond depth, and referent-aware iltifāt, remain parser/coref-blocked.

---

## 5. The rearrangement program (how we probe order)
Ordering mechanisms: linear index · āyah-final word (fāṣila-concept) stream · rhyme-class · root
first-occurrence · frequency-rank. Methods: edit-distance/SW · LCS · Kendall/inversion · genome-rearrangement
· DTW · optimal transport · permutation entropy · Moran/Geary · Mantel · block-permutation sensitivity.
Key results: E1 coherence length ~few āyāt (order lives at the fine scale); E4 Mantel canonical r=+0.325 >
nuzūl +0.290 (global grouping > chronology); #60 the fāṣila caps its OWN verse, doesn't chain to the next.
Nulls always at the same scale + allowed-practice reorderings (nuzūl/Nöldeke) reported alongside. (DESIGN_OF_EXPERIMENTS.md)
D1 (fusion, window grain, Qur'an vs ordinary): dominated by rhyme-persistence (AUC 0.86; fused 0.875, no
synergy) — the survivors live at DIFFERENT grains, so single-grain statistical fusion can't combine them;
the real fusion is this conceptual synthesis + the #35 cell (vs sajʿ AUC 0.96).

## 6. Controls & practices (LOCKED — DESIGN_STANCE.md)
- Positive-control-first; G10 invariance gate (equal-N, ≥2 tokenizations, same-language baseline, null).
- Telescope rule: absence of evidence ≠ evidence of absence (buys *search*, never a *claim*).
- Divine-rootedness: study rasm/roots/words/structure/canonical order; deprioritize ḥarakāt + human groupings.
- Voice: data-driven only, no overclaim, no miracle-tone.
- Cross-impact propagation: nothing is final; re-evaluate every verdict as other modalities teach us.
- Rearrangement built into every experiment.
- Keep the paper (SIX_LENSES_PAPER.md) live at every finding.

## 7. Frontier (largest first)
Recited/phonological (data-blocked, largest region; deprioritized as ḥarakāt) · deep dependency-syntax &
referent-aware iltifāt (tooling-blocked) · D1 statistical FUSION of the survivors (capstone, pending) ·
muqaṭṭaʿāt/rasm thread EXTENDED (#67: temporal waves + nulled combinatorics + transition order); still open
there: numeric/positional regularities of the canonical rasm (careful re gimmickry) · SVD/NMF sūra×root
latent axes.
