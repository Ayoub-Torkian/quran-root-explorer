# Two Books · Genome ↔ Qur'an correspondence study

_Study workspace. Created 2026-06-08. Status: **DESIGN / pre-pilot.** No results yet._

## The vision (end goal)

Three parallel corpora, and a *tested* alignment between them:

1. **Corpus of language** — Qur'anic units (sūrah · āyah, and multi-āyah blocks).
2. **Corpus of genes** — expressed coding sequences (RefSeq CDS).
3. **Corpus of proteins** — the translated proteome.

The question is whether units of (1), under a letter→codon (or letter→amino-acid)
mapping, correspond to units of (2)/(3) **beyond what chance and language structure
alone produce**.

> **Scope (Amendment A1, 2026-06-08):** the claim is **language-general, not
> Qur'an-specific.** Establishing that *language as a modality* corresponds to
> genomic/protein sequence is the goal; the Qur'an is one sample, Shakespeare another
> (replication, not refutation). This is framed as **multimodal fusion** across text,
> genome, and protein. The new make-or-break control is the **shuffled-genome
> surrogate** — see CHALLENGES.md §2.5 and METHODOLOGY.md Amendment A1.

## The one rule that governs everything here

> The alignment is a **tested output, never an assumed input.**

We are NOT "finding which gene matches which āyah" (that phrasing assumes the answer
and is exactly how the Bible Code fooled itself). We are **testing whether any āyah
matches any gene beyond chance**, with a method whose verdict is trustworthy whether
it comes out positive or null. **A null is a successful result.** See `CHALLENGES.md`.

## Files

| File | What it is |
|---|---|
| `METHODOLOGY.md` | The full experimental design / pre-registration. |
| `CHALLENGES.md` | Robust critical review: every Bible-Code failure mode → the guardrail that neutralizes it. Read this first. |
| `IDEATION_LOG.md` | How the idea evolved through the design dialogue; decisions locked. |
| `data/README.md` | What data to download and how to build the BLAST database. |
| `data/examples/` | Real seed sequences (e.g. human insulin CDS) for pipeline bring-up. |
| `data/arabic_letters.md` | The 28-letter inventory and normalization rules. |

## Status / next step

Design is written and critically reviewed. Next is an **offline pilot** (not app
code): build the BLAST DB from a small CDS subset, implement the symmetric
search + baseline battery on a handful of āyāt, confirm the pipeline runs and the
null calibrates. Pilot output is for de-bugging the method, **not** for any claim.
