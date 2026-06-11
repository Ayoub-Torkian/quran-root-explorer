# Ideation log — how this study took shape

_Captures the design dialogue (2026-06-08) so the reasoning is recoverable. The
prompts were the user's; the critical pushback and structure are recorded as-is._

## Relationship to the EXISTING Biology module (important)

The app already ships `pages/16_Biology.py` + `pages/17_Two_Books_Summary.py`. That
module is the **metaphor/lens** version of "two books": it borrows sequence-biology
tools (base composition, codon-usage Zipf, di-codon bias, sequence complexity) and
applies them to the corpus under the explicit mapping `letters≈bases, roots≈codons,
words≈proteins`, with permutation nulls and an honest "this is a lens, not a literal
claim" caption. It is about **sequence latent features, not semantics** — which is
exactly the original two-books/biology intent.

**None of the genome-correspondence study below is in the app yet.** This is a NEW,
much stronger direction: instead of borrowing biology's *tools*, it tests an actual
letter→codon mapping against **real genomic data** (RefSeq CDS via BLAST). Per
`METHODOLOGY.md §9`, if it ships at all it should be a **separate self-contained
lens** with precomputed results — not bolted onto the live Biology page. This
directory is its design home until then.

## How the idea evolved (and where pushback changed it)

1. **Opening idea:** map Arabic characters to codons (64) and amino acids (20) —
   upscale and downscale — and validate via BLAST against genome/proteome banks,
   optimizing the mapping by Monte Carlo to maximize match. "Better match = better
   mapping."
   - *Pushback:* optimizing a mapping to maximize match is data-dredging; any long
     sequence BLASTs to *something*. Without a null and pre-registration this is a
     guaranteed false positive (the Bible-Code trap).

2. **Refinement:** use length-matched units (root / āyah / multi-āyah) and ask, under
   a given mapping, the *probability* of matching a known gene/protein.
   - *Reframe:* that probability IS essentially a BLAST e-value. Made testable, but
     three things decide it: length scale (roots too short), the null must isolate
     ORDER from composition, and genome vs proteome are different math.

3. **Reverse direction proposed:** start from a real protein/gene and find a mapping
   that reproduces Qur'anic sequences ("larger volume of matched data").
   - *Pushback:* reversing direction does not change the fit; a one-to-many mapping
     is a cipher with wildcards that can encode anything. Same Bible-Code failure.

4. **"Works for other books too — no problem."**
   - *Pushback:* under the two-books-one-Author thesis, other books matching equally
     is a *refutation*, not a convenience. The thesis requires Qur'an-specificity.

5. **Theological frame stated:** Word of God (Qur'an) and Act of God (genome/proteome
   — hardware with built-in software).
   - *Note:* the theology motivates *looking* for correspondence; it does NOT specify
     that correspondence is a character-level cipher. That extra assumption is the
     fragile part.

6. **Decisions locked (via structured Q&A):** mapping searched by Monte Carlo;
   one-to-one rigid; match = significant BLAST; baseline = random matched. Resolved a
   collision (one-to-one is impossible letters→amino-acids since 28>20) ⇒ route =
   **letters→codons→genome**, database = **known genes / coding sequences**.

7. **"Use expressed/translated codons; AA can differ from codon; works in all
   spectrums; simplify then refine."**
   - *Incorporated:* RefSeq CDS already = expressed coding sequence. AA track kept as
     a *separate* experiment (can't be one-to-one). "All spectrums" flagged as the
     main look-elsewhere risk ⇒ family-wise correction + pilot-vs-confirmation split.

8. **"End objective: which gene/protein corresponds to which Qur'an unit; eventually
   corpora of genes, proteins, language." + "Failure is not an option."**
   - *Critical reframe (the spine of CHALLENGES.md):* the alignment must be a TESTED
     output, never an assumed input. "Failure is not an option" = *methodological*
     failure is not an option; a calibrated **null is a success**. Building the system
     to only accept "found correspondences" would manufacture them — the exact
     Bible-Code machine.

9. **Scope set to language-general + multimodal (Amendment A1).** "We do not want to be
   specific to Qur'an. If correspondence between genome/amino-acid sequence and the text
   of *language* is established, that is the accomplishment; nuances come after."
   Shakespeare analogy: language uses "the same raw gradient as anybody" — all literature
   from ~28 letters, all biology from 4 bases. Framed explicitly as **multimodal fusion**:
   explore text, genome, and protein as modalities, not text alone.
   - *Critical consequence:* other books become replication, not refutation. New dominant
     risk = structure-to-structure generic resemblance ⇒ mandatory **shuffled-genome**
     control. And a method fork opens: searched-mapping+BLAST (A) vs mapping-free
     structural/embedding comparison (B). B is the stronger "establishment" route and is
     what "multimodal fusion" actually denotes. Awaiting A / B / B-then-A.

## Decisions still open (see METHODOLOGY.md §2, §8)

- Final letter inventory (28 vs 36) and the frozen hamza / tāʾ-marbūṭa rules.
- Primary unit set and minimum length floor.
- Aggregate statistic (default: count of units with e < 1e-3).
- M (mappings sampled) and K (surrogate sets) given compute budget.
- Human-only vs multi-species headline.
