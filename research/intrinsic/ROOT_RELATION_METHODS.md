# Three lenses on root relations — co-occurrence · dependency graph · motifs

*Grounded in the actual Qur'ān corpus (Book6), the root as the anchor. All numbers below are
**[MEASURED]** in-sandbox on the rasm ROOT substrate, muṣḥaf (DIVINE‑DEFAULT) arrangement.
No external model, no GPU — the owned space. Date: 2026‑06‑19. Script: `/tmp/methods.py`.*

**Corpus shape:** 6,236 verses · 1,702 unique roots · 666 roots occur ≥8× (the analysable core).
Co‑occurrence graph (co ≥ 3): **17,046 edges, density 0.077, mean degree 51, max degree 592 (ءله)**.

The same fact — *which roots relate to which* — looks completely different through three lenses.
The point of this note is to show, with data, **what each lens sees and what it is blind to**, so we
invest in the one that adds real understanding rather than re‑describing frequency.

---

## 1 · Co‑occurrence (symmetric, undirected)

**What it is:** two roots are linked if they share a verse; weight = how many verses. This is what the
app's Network/Motif pages were built on.

**Advantages**
- Directly observable and verifiable — you can read the shared verses.
- Cheap, complete, and intuitive.

**Disadvantages — shown in the data**
- **Frequency‑dominated.** Ranked by raw shared‑verse count, the "top relations" are pure ubiquity:

  | pair | raw co | freq A / freq B |
  |---|---|---|
  | ءله · قول | 512 | 1877 / 1383 |
  | ءله · كون | 441 | 1877 / 1176 |
  | ءله · علم | 408 | 1877 / 728 |

  These tell you nothing — ءله is in 1,877 verses, so it co‑occurs with everything.
- **One super‑hub distorts the whole graph.** ءله has degree **592** (links to ~89% of all roots).
  Any structure is drowned by it.
- **Symmetric — no direction.** It cannot say *عنب implies نخل but not the reverse.*
- **Within‑verse only** — blind to relations that span verses.

**The fix that rescues it — frequency‑controlled association (NPMI).** Divide by what frequency predicts
and the lens suddenly recovers **genuine Qur'ānic concept‑bonds**:

| pair (top NPMI) | NPMI | meaning |
|---|---|---|
| جري · تحت | 0.86 | rivers **flowing beneath** (تجري من تحتها الأنهار) |
| نخل · عنب | 0.85 | date‑palm & grape (the paired garden fruits) |
| شمس · قمر | 0.84 | sun & moon |
| شرق · غرب | 0.84 | east & west |
| نفخ · صور | 0.83 | the **blowing of the Trumpet** |
| مريم · عيسى | 0.81 | Mary & Jesus |
| شري · ثمن | 0.80 | buy & price (the "selling the hereafter" trope) |

> **Lesson:** raw co‑occurrence measures *frequency*; NPMI measures *bond*. The app must rank by the
> latter (now done — Motif "honesty map", 2026‑06‑19).

---

## 2 · Dependency graph (directed, asymmetric) — the underused lens

**What it is:** make the edge **directed** — `conf(A→B) = P(B present | A present)` — and weight by **lift**
(`P(B|A) / P(B)`, frequency‑controlled). Now the graph carries *direction* and *hierarchy*.

**Advantages — shown in the data**
- **Recovers idioms and one‑way implications** invisible to symmetric co‑occurrence:

  | A ⇒ B | P(B\|A) | lift | reading |
  |---|---|---|---|
  | طبع ⇒ قلب | **1.00** | 40 | "**sealing** of the **heart**" (طبع على قلوبهم) |
  | لبب ⇒ ءول | **1.00** | 39 | "**أولو الألباب**" — people of understanding |
  | عنب ⇒ نخل | 0.82 | **255** | grape almost never occurs without date‑palm |
  | خبث ⇒ طيب | 0.80 | 109 | the impure / pure contrast pair |
  | علن ⇒ سرر | 0.75 | 109 | the open / secret contrast pair |

- **Asymmetry reveals satellite → hub structure.** حبط⇒عمل (deeds *rendered vain*, P=1.00 vs reverse 0.05),
  عدن⇒جنن (Gardens of **Eden**, P=1.00), and a whole family that one‑way invoke God — حلف⇒ءله (oath),
  خون⇒ءله (treachery), عصم⇒ءله (protection): the *act* implies *God*, not vice‑versa.
- **Names the gravitational centres.** Roots most *depended upon* (count of lift≥2 incoming implications):
  **ءله (98) · قول (41) · كون (17) · ءرض (10) · قوم (7) · خلق · علم · ءمن (6).** ءله is the hub 98 roots
  point toward — a real, directed theological centre, not just a frequent word.
- **Conditional independence exposes MEDIATION — the deepest payoff.** Two roots can look unrelated
  globally yet be strongly linked *inside a third's context*:

  | triple | corr(A,C) overall | corr(A,C \| B present) | reading |
  |---|---|---|---|
  | خلق · **نفس** · وحد | 0.02 | **0.53** | creation ↔ oneness are bonded **only through the soul (نفس)** |
  | بعث · **رسل** · ضلل | 0.04 | **0.43** | resurrection ↔ misguidance bonded **through the messenger** |

  Symmetric co‑occurrence sees corr ≈ 0 and concludes "unrelated." The dependency lens shows the link is
  **real but mediated**. [MEASURED, descriptive — not yet gated vs shuffle.]

**Disadvantages**
- Small‑support pairs need a min‑count + lift floor (a rare root trivially "implies" a ubiquitous one
  unless you control with lift — which we do).
- Directionality is statistical implication, not grammar/causation; label it as such.
- Still within‑verse.

> **Lesson:** this is the **richest and most under‑exploited** lens in the owned space. It turns a flat
> "these relate" into "**what implies what, what is central, what mediates what**" — all interpretable,
> all readable back in the text.

---

## 3 · Motif analysis (higher‑order: triads, cliques)

**What it is:** recurring subgraphs — three (or more) roots all sharing verses.

**Advantages**
- In principle captures templates and constellations a pair cannot.

**Disadvantages — shown in the data**
- **The graph is already ~85% transitive.** On the top‑200 roots, triad **closure = 84.8%**
  (773k triangles vs 416k open paths). When partners‑of‑partners almost always meet, a triangle is
  *cheap* — it carries little beyond the three pairs that compose it.
- **Genuine higher‑order (3‑way beyond pairwise) is rare.** Measured rigorously (Poisson + FDR, then a
  verse‑length+frequency‑preserving curveball null), only **~0.5% of triads** (≈15 vs ~4 expected by
  chance) exceed what their pairwise rates imply; the rest is pairwise + frequency + **verse length**
  (survivor triads sit in verses of 12.8 roots vs 5.5 global). [MEASURED 2026‑06‑19, GRADED_FINDINGS.]
- **Combinatorial and artifact‑prone** — small expected counts make naïve tests (asymptotic χ²) lie.

> **Lesson:** motifs are mostly a *re‑description* of pairwise + frequency + length. Keep them as a
> descriptive/reading aid (with the honesty‑map controls), not as a source of new structure.

---

## Cross‑reference — the same structure, three resolutions

| question | co‑occurrence | dependency graph | motif |
|---|---|---|---|
| do A,B relate? | yes (but freq‑biased) | yes, **+direction & strength** | yes (but ~implied by pairs) |
| who is central? | high‑degree = high‑frequency (ءله) | **most depended‑upon** (ءله 98 incoming, by lift) | hub of many triangles (= same) |
| A⇒B vs B⇒A? | **cannot tell** | **yes** (طبع⇒قلب, عنب⇒نخل) | n/a |
| is A–C real but mediated by B? | sees corr≈0 → "unrelated" ✗ | **yes** (خلق–وحد via نفس, 0.02→0.53) ✓ | flags a weak triangle, can't explain |
| new info beyond pairs? | — | **conditional structure** | **~0.5% only** |

The three are nested: **co‑occurrence** is the raw symmetric shadow; **the dependency graph** adds the
two things that carry meaning — *direction* and *conditioning*; **motifs** mostly re‑describe the pairwise
layer. The mediation result is the clinching cross‑reference: what co‑occurrence calls "unrelated" and
motifs call "a weak triangle," the dependency lens **explains** as a context‑gated bond.

---

## Recommendation (ranked, #1 = pick)

1. **Build the dependency‑graph lens over roots — directed, lift‑ranked, with mediation.** It is the one
   lens that adds genuine, interpretable understanding from the data we own: "what implies what" (طبع⇒قلب),
   "what is central" (the 98‑in‑degree of ءله), and "what mediates what" (نفس between خلق and وحد). Dense,
   readable, root‑anchored, no external compute. A real new app surface and a real analytic instrument.
2. **De‑frequency everything, everywhere — NPMI/lift, never raw counts.** Already applied to Motifs;
   apply the same discipline to the Network page so the whole app stops surfacing ubiquity as structure.
3. **Demote motifs to a descriptive reading aid** (honesty‑map controls already in). Stop mining them for
   new structure — measured to be ~0.5% beyond pairs.

The honest headline: we kept looking outward for a richer signal; the richer signal was a **direction and
a conditioning bar** away, inside the co‑occurrence data we already had.
