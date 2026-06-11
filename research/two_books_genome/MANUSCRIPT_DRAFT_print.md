# Does a text encode the genome? A controlled framework for cross-domain sequence-mapping claims — with a Qur'ān–genome case study and a cautionary false positive

**A. Torkian** (torkian@sharif.edu) · *draft v2 (methods/perspective), 2026-06-09*

---

## Abstract

Claims that one symbolic sequence "encodes" another across domains — a text hiding a genome,
music in DNA, scripture in the proteome — are recurrent and seductive, and they share a single
fatal failure mode: a transformation searched over a long sequence will always extract apparent
signal from noise. This is what discredited the "Bible Code," whose method later produced equally
striking "messages" in *Moby-Dick*. We present a general, reusable framework for testing such
cross-domain mapping claims *without* fooling oneself, organized around six controls — a
composition floor, out-of-sample transfer, **convergence** of the discovered mapping, replication,
multiplicity correction, and a **planted positive control** that proves the instrument can recover
a true mapping — plus a mapping-invariant structural pre-check. We demonstrate the
framework on a concrete instance: whether a character→codon/amino-acid mapping links the Qur'ān to
the human genome/proteome. The framework returns a robust null — but its most instructive product
is a **cautionary false positive**: a convergence signal that survived single-instance shuffle,
other-language, and random-target controls, yet dissolved under replication (real 0.22 ± 0.13 =
shuffled 0.22 ± 0.16, z = 0.00). A planted positive control confirms the instrument is not merely
blind — it recovers a known cipher (recovery 1.00, convergence 1.00 on text; 0.87/0.57 on roots) —
so the nulls reflect a genuine, *target-side* limit: the genome is statistically flat at the orders
where mappings would be identifiable. The lesson generalizes beyond the case study: in cross-domain
mapping searches, raw similarity is never evidence, and controls applied to a single instance are
not enough — replication is decisive. (No Qur'ānic text was altered; controls are
frequency-matched random sequences.)

## 1. The problem

A large, informal literature attempts to show that some text "contains" or "maps onto" a
biological sequence. The appeal is real — both texts and genomes are discrete linear symbol
strings — but the methodology is almost always the same trap: choose a mapping (often by searching
many) that maximizes a similarity score against a large database, then present the resulting match
as discovery. Because the search space is astronomical and the target database vast, *some* mapping
will always produce a striking-looking match for *any* input, including random noise. The Bible
Code is the canonical cautionary case (Witztum–Rips–Rosenberg 1994; refuted by McKay et al. 1999).
What has been missing is not enthusiasm but a disciplined framework that can return an honest
verdict — positive *or* null — for this entire class of claims. We provide one and exercise it.

## 2. A framework for cross-domain mapping claims

We treat any proposed alignment as a **tested output, never an assumed input**, and require that
each of the following be satisfied. The principles are general; the case study (§3) shows each in
action.

**(0) Mapping-invariant structural pre-check.** Before searching for any mapping, compare the two
domains on relabeling-invariant structural signatures (e.g., long-range correlation / mutual-
information decay). A one-to-one mapping only relabels symbols and cannot change such statistics,
so a gross structural mismatch rules out *all* mappings at once — no search needed.

**(1) A floor, because raw similarity saturates.** Score is meaningless without a baseline: run
the identical search/pipeline on shuffled and composition-matched-random inputs. With enough
mapping freedom, a search drives similarity to a *ceiling* for any input, so the floor sits at the
ceiling and signal-over-floor ≈ 0. Only the margin over this floor can be evidence.

**(2) Out-of-sample transfer.** A mapping fitted on one portion must be tested on unseen data; an
in-sample fit is not a result.

**(3) Convergence — the operational test of "a correct mapping exists."** Independently optimize
the mapping on disjoint portions and measure agreement, *within* a portion (self-consistency) and
*across* portions, against chance. A real, universal mapping makes independent optimizations
converge to the *same* table; per-portion overfitting does not.

**(4) Replication and significance.** Every candidate is re-evaluated over many disjoint
portion-pairs and seeds, with a significance test. A single instance can pass controls (1)–(3) and
still be a fluke (see §3.3).

**(5) Multiplicity.** Correct across every objective, granularity, and scenario examined; report
the whole search, not the best cherry.

**(6) Instrument validation (positive control).** A null is only interpretable if the search could
have found a real mapping. Before trusting any negative, plant a *known* mapping into structured
data and confirm the identical pipeline recovers it (recovery and convergence >> chance). Without
this, "no mapping found" is indistinguishable from "the optimizer is too weak" — a confound that
sinks most framework claims. The positive control also reveals *target-side* limits: if recovery
fails specifically when the target is statistically flat, that flatness — not the search — bounds
what any mapping could achieve (see §3.2b).

A claim is credible only if it clears the floor, transfers out-of-sample, yields a convergent map,
replicates with significance, survives multiplicity, **and uses an instrument that demonstrably
recovers a planted positive control**. A clean failure at any stage is a valid, reportable null.

## 3. Worked example: the Qur'ān and the human genome

**Setup.** Qur'ān text (parsquran.com; 6,236 verses → 31-letter consonantal skeleton); human
Consensus CDS (NCBI CCDS; 35,624 sequences, ~62 Mb); eight control languages (Project Gutenberg).
Mappings (char→codon/64 or →amino-acid/20) are searched by simulated annealing; objectives include
dipeptide-distribution distance, a protein-Markov likelihood, a BLAST-seed k-mer match, and the
faithful `tblastx` bit-score against a local CCDS database. Folding via ESMFold. Qur'ān files are
read-only; composition controls are frequency-matched random sequences.

**3.1 Structural pre-check (control 0).** Across eight languages in five families, all cluster at
short-range statistical memory (MI-decay γ ≈ 1.4–2.5); the genome alone has long-range memory
(γ ≈ 0.92), with non-overlapping CIs. The Qur'ān (γ ≈ 2.29) sits inside the language cluster — no
closer to the genome than Homer or Cervantes. Because relabeling cannot change this, the mismatch
holds for every possible mapping. The genome's separation is significant (outlier z = −3.43,
one-sided p ≈ 3×10⁻⁴ against the 8-language distribution) and is **not** an alphabet-size artifact:
at a matched 4-symbol alphabet the genome (γ = 0.89) still sits far below English-recoded-to-4
(γ = 1.75), and recoding the genome *up* to 64 codon symbols pushes γ *down* to 0.27 — the opposite
of what a symbol-count effect would produce.

**3.2 Saturation and the floor (control 1).** Under a free mapping, annealing drives the
proteome-match of *any* text — real, shuffled, English — to ~100% (k = 5–6). The floor sits at the
ceiling; similarity-over-floor ≈ 0 for every objective. Maximizing similarity is trivially
achievable and cannot, alone, identify a mapping.

**3.2b Instrument validation and the flat-target ceiling (control 6).** We planted a known
substitution cipher into structured text and ran the identical convergence pipeline. On the Arabic
letter sequence (scored against the text's own trigram model) the instrument recovers the planted
key perfectly — recovery 1.00, cross-portion convergence 1.00 (chance 0.032) — and on the Qur'ān's
1,702-root vocabulary it still fires decisively (recovery 0.87, convergence 0.57; chance 0.033).
So the machinery *does* return a positive when a true mapping exists. But the same instrument, when
the target is the **real genome**, collapses to chance — because protein/genome sequence is
statistically flat at the low n-gram orders that make ciphers crackable. This flatness is a
property of the *target*, not the source: it bounds every forward text→genome substitution map
regardless of the Word-side unit, and it means our nulls are genuine signal-absence, not weak
search.

**3.3 A cautionary false positive (the centerpiece; controls 3–4).** One disjoint-portion pair
produced a cross-set convergence of 0.58 (chance 0.056) that **survived** shuffle, other-language
(English), *and* random-target controls — a genuine-looking candidate. Replication killed it: over
five disjoint pairs, real Qur'ān convergence was 0.22 ± 0.13, statistically identical to shuffled
Qur'ān (0.22 ± 0.16, z = 0.00). The residual is a composition effect carried by the most frequent
letters (0.31 vs 0.14 rare) — not order, not meaning, not Qur'ān-specific. **A signal can pass
single-instance controls and still be a fluke; n = 1 is never enough.** This is the framework's most
transferable lesson.

**3.4 Folding (orthogonal check).** Proteins generated from Qur'ānic characters do not fold:
Al-Ikhlas (47 aa) pLDDT 49.6, pTM 0.30; An-Nas (80 aa) pLDDT 34, pTM 0.15 — the disordered/random
band (real proteins: pLDDT 70–90, pTM > 0.5).

**3.5 Faithful BLAST (control 1, paper's own objective).** A local `tblastx`-vs-CCDS run (20
mappings × six short sūras) scored real against control: best bit-scores indistinguishable — real
mean 32.9 (max 50.6) vs control mean 32.2 (max 43.2), Δmean = 0.74, in the low/chance band. Same
null.

**3.6 Granularity (control 5, multiplicity).** Because the target-side flatness (§3.2b) is
unit-independent, the null should hold across Word-side granularities. We confirm at three: the
single letter, the codon-aligned letter, and the **triliteral root** — the largest motivated unit
that still escapes parameter explosion (1,702 roots over 51,044 tokens, ratio 30, vs 11,260
arbitrary trigraphs with ~10 tokens each, which we exclude as unidentifiable by construction). With
the validated instrument, root→codon convergence to the genome is 0.015 ± 0.004, identical to the
shuffled floor (0.016) and chance (0.017). Coarser closed-vocabulary units (root→gene) escape
flatness only if paired with a pre-registered biological prior; without one they become a
multiplicity trap and are out of scope here.

## 4. Discussion — lessons that generalize

The case study yields a robust null, but the reusable findings are methodological. (i) **Raw
similarity is not evidence:** sufficient mapping freedom saturates any score, so only a calibrated
margin over a matched floor can count. (ii) **Convergence is the right operational definition** of
"a correct mapping exists," and it cleanly separates a universal code from per-portion overfitting.
(iii) **Replication is decisive:** the only thing standing between us and a published phantom was
re-running the candidate across many pairs — single-instance controls had passed. (iv) A
**mapping-invariant structural pre-check** can refute an entire claim before any search.
(v) **A planted positive control is non-negotiable:** our first "null" instrument was simply too
weak to recover even a known cipher; only after validating that it recovers a planted mapping
(recovery 1.00 on text, 0.87 on roots) could we attribute the genome nulls to the *target's*
statistical flatness rather than to search failure. We recommend these as a default protocol for
cross-domain sequence-mapping claims.

**On scope and what we deliberately do not do.** A natural temptation is to escalate to whole-unit
correspondences (sūra/root/ayah → gene). We scope this explicitly and decline it: the
unit↔gene space is 10⁶–10⁸ pairings, so a credible test needs the candidate pairs fixed *a priori*
by an independent, mechanistic prior — and none exists. Every prior we could construct (semantic,
rank, positional) is a researcher-chosen mapping in disguise, reintroducing exactly the degrees of
freedom this framework exists to remove; and the flat-target ceiling still caps any sequence-level
test of the chosen pairs. Chasing it would manufacture the artifact, not test a hypothesis. All
conclusions here concern the specific sequence-cipher hypothesis only and say nothing about the
Qur'ān as scripture or meaning, which no similarity statistic can address.

## 5. Conclusion

Tempting cross-domain "encoding" claims can be tested rigorously rather than asserted or dismissed.
Applied to the Qur'ān and the human genome, the framework returns a clean null across structural,
search, convergence, folding, and faithful-BLAST analyses, and the forward text→genome substitution
program is now closed across all three sensible Word-side granularities — letter, codon, and root —
each judged with an instrument validated to recover a planted positive control. Its most valuable
output is a worked demonstration — a false positive caught only by replication, and a null shown to
be a *target-side* limit rather than a weak search — of how to pursue such ideas without
self-deception.

## Figures

![Fig. 1](figures/F1_structural_gamma.png)

**Fig. 1 — Structural pre-check (control 0).** MI-decay exponent γ for eight languages (five
families), the Qur'ān, and the human genome, with 95% CIs. Languages cluster (γ ≈ 1.4–2.5); the
genome alone is long-memory (γ ≈ 0.92, non-overlapping CI); the Qur'ān (γ ≈ 2.29) sits inside the
language cluster. *Takeaway: relabeling-invariant, so the mismatch holds for every mapping.*

![Fig. 2](figures/F2_pipeline.png)

**Fig. 2 — The pipeline.** Text → char→codon/AA mapping (searched by simulated annealing) →
sequence → objective (dipeptide / Markov / k-mer / `tblastx`), run in parallel on real input and on
the shuffled + composition-matched-random floor.

![Fig. 3](figures/F3_saturation.png)

**Fig. 3 — Saturation and the floor (control 1).** Best proteome k-mer match vs annealing
iterations for real, shuffled, and English inputs — all converge to ~100% at k = 5–6. *Takeaway:
the floor sits at the ceiling; similarity-over-floor ≈ 0.*

![Fig. 4](figures/F4_false_positive.png)

**Fig. 4 — The cautionary false positive (centerpiece; controls 3–4).** (a) Single pair:
convergence 0.58 (chance 0.056), surviving shuffle/English/random-target controls. (b) Replication
over five disjoint pairs: real 0.22 ± 0.13 vs shuffled 0.22 ± 0.16 (z = 0.00). (c) Letter
dissection: frequent letters 0.31 vs rare 0.14 (composition, not order). *Takeaway: n = 1 passes
controls and still dies under replication.*

![Fig. 5](figures/F5_folding.png)

**Fig. 5 — Folding null (orthogonal check).** pLDDT/pTM for Qur'ān-derived proteins (Al-Ikhlas
49.6/0.30; An-Nas 34/0.15) against the disordered band and the real-protein band (70–90 / > 0.5).

![Fig. 6](figures/F6_positive_control.png)

**Fig. 6 — Instrument validation (control 6).** The identical pipeline recovers a *planted* cipher
on structured text (letters: recovery/convergence 1.00; roots: 0.87/0.57; chance ≈ 0.03), but
collapses to chance against the real genome (root→codon convergence 0.015 ≈ chance 0.017). The
nulls are a target-side flatness ceiling, not a weak search.

## Data, code & reproducibility
Pre-registration and guardrails (METHODOLOGY.md, CHALLENGES.md), structural results and the
alphabet-size control (RESULTS.md), pipeline (PIPELINE.md), scenario design (SCENARIOS.md), the
exhaustive scenario triage (SCENARIO_MATRIX.md), the internal referee report (REFEREE_NOTES.md),
the whole-unit→gene scoping (GENE_PRIOR_SCOPING.md), the full per-step ledger with seeds and
timestamps (METHOD_LEDGER.md, ledger.json), and all scripts are in `research/two_books_genome/`.
Key scripts: `positive_control_cipher.py` (instrument validation), `root_map_test.py` (root-level
test), `matched_alphabet.py` (M4 control), `run_blast.py` (faithful tblastx), `build_figures.py`.
Corpora: parsquran.com (Qur'ān), Book6.xlsx (root segmentation), NCBI CCDS, Project Gutenberg.

## Limitations
The mapping space is sampled, not exhausted — but the positive control (§3.2b) shows the instrument
recovers a planted mapping, so the nulls reflect target-side flatness, not search failure. The
cross-alphabet γ comparison is controlled (matched 4-symbol and 64-codon recodings, §3.1) but
remains one structural lens; conclusions rest on the convergence of independent analyses (structure,
search, convergence, folding, BLAST, positive control), not any single metric. Folding used one
fixed mapping and n = 2 proteins (a supporting, not primary, check).

## References
1. Witztum, D., Rips, E. & Rosenberg, Y. (1994). Equidistant letter sequences in the Book of
   Genesis. *Statistical Science* 9(3): 429–438.
2. McKay, B. D., Bar-Natan, D., Bar-Hillel, M. & Kalai, G. (1999). Solving the Bible Code puzzle.
   *Statistical Science* 14(2): 150–173.
3. Drosnin, M. (1997). *The Bible Code.* Simon & Schuster.
4. Peng, C.-K. et al. (1994). Mosaic organization of DNA nucleotides. *Physical Review E* 49(2):
   1685–1689. (DNA long-range correlation / DFA.)
5. Lin, Z. et al. (2023). Evolutionary-scale prediction of atomic-level protein structure with a
   language model (ESMFold). *Science* 379(6637): 1123–1130.
6. Jumper, J. et al. (2021). Highly accurate protein structure prediction with AlphaFold. *Nature*
   596: 583–589.
7. Altschul, S. F. et al. (1990). Basic Local Alignment Search Tool (BLAST). *Journal of Molecular
   Biology* 215(3): 403–410.
8. Pruitt, K. D. et al. (2009). The consensus coding sequence (CCDS) project. *Genome Research*
   19(7): 1316–1323.
