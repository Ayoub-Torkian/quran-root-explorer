"""Close-up · Code 19 (Rashad Khalifa), reviewed — REFUTED-ARTIFACT. Comprehensive claim-by-claim critical review."""
import os
import streamlit as st

try:
    import state as S
except Exception:
    S = None
import closeup as C

st.set_page_config(page_title="Close-up · Code 19", page_icon="🔢", layout="wide")
if S:
    try:
        S.log_page("closeup_code19")
    except Exception:
        pass
    for fn in ("inject_css", "render_grouped_nav"):
        try:
            getattr(S, fn)()
        except Exception:
            pass
C.inject()
Y, P, N = "✔ holds", "~ partial", "✗ fails"

# ── 1 · PROBLEM ──
C.hero("Code 19 (Rashad Khalifa), reviewed",
       "Does a mathematical code based on 19 govern the Qur'ān — or is it selected from countless possible counts?",
       "REFUTED-ARTIFACT", 22, "rasm counts (Basmalas included)", "DIVINE-DEFAULT · RANDOM null")
C.story(
    "Anchored on Q 74:30 (<i>“over it is nineteen”</i>), the claim is a pervasive 19-code in letters, words and "
    "sūras. Every major claim is tested here on the text itself, Basmalas included. The result is honest and split: "
    "<b>the code reproduces EXACTLY where the spelling is fixed, and FAILS wherever spelling can vary.</b>",
    "Written to be مقبول for the general reader (a clear scorecard) and مطلوب for the specialist (every count, its "
    "tolerance, and the χ² in a table). A methodological verdict, not a theological one.", accent=C.CORAL)
C.kpis([
    ("9", "exact ÷19 facts", "Claims that reproduce exactly and are divisible by 19 (see tables)", C.TEAL),
    ("ق = 57 ✔", "stable letter", "Qāf in sūra 50 and 42 = 57 = 19×3 — reproduces exactly", C.TEAL),
    ("ي+س ≠ 285", "variable letter", "Yā-Sīn in sūra 36 = 248, not 285 — fails under a neutral count", C.CORAL),
    ("الله ÷ 7,11", "not 19", "Allah = 2695, exactly divisible by 7 and 11 — not 19 (claim: 2698)", C.CORAL),
    ("2.9%", "÷19 rate", "Share of 1,084 natural counts divisible by 19 — vs 5.3% chance; the lowest", C.CORAL),
    ("0", "above chance", "No candidate number beats chance; 19 is the rarest of all", C.CORAL),
    ("22", "grade", "REFUTED-ARTIFACT — the pervasive code, not the genuine anchors", C.CORAL),
])

# ── 2 · HYPOTHESIS ──
C.section("Hypothesis")
C.callout("If 19 truly governs the text, it must show privilege, robustness, and need no discarding",
          "A real numerical law would show three things: multiples of 19 appearing <b>above chance</b> and 19 "
          "<b>out-performing rival numbers</b> (7, 11, 13, 17, 23…); the key counts <b>robust</b> to spelling and to "
          "the choice of what to count; and <b>no text rejected</b> to make totals balance. A small genuine cluster "
          "of 19-facts can exist without these — but the <i>pervasive code</i> needs all three.", accent=C.SLATE)

# ── 3 · METHOD & INSTRUMENTS ──
C.section("Method & instruments")
C.callout("The apparatus",
          "<b>Substrate</b> — Book6 rasm; words as whole tokens, letters counted directly. <b>Basmala</b> — the 112 "
          "unnumbered chapter-opening Basmalas are added where the theory requires. <b>Tests</b> — (a) verify each "
          "structural, word, and initial-letter claim against the text; (b) the privilege test: divisibility of "
          "1,084 natural counts by 19 vs 7/11/13/17/23/29 vs chance; (c) the robustness test: re-count under a "
          "neutral spelling and see whether the totals still land on 19. <b>Note</b> — my normalised rasm differs "
          "from the exact Uthmānī orthography, which is the very point: counts that need a fixed spelling are fragile.",
          accent=C.SLATE)

# ── 4 · RESULTS ──
C.section("Results — every claim, by category")

C.note("A · Structural & positional claims. The counts of sūras, verses and positions — exact, and they mostly HOLD.")
C.table(["Claim (Khalifa)", "claimed", "measured", "÷19", "verdict"], [
    ["Basmala has 19 letters", "19", "19", "19×1", Y],
    ["114 sūras", "114 = 19×6", "114", "19×6", Y],
    ["Sūra 96 (first revealed) is 19th from the end", "19", "19", "19×1", Y],
    ["Sūra 96 has 19 verses", "19", "19", "19×1", Y],
    ["Basmala occurs 114 times (heads + 1:1 + 27:30)", "114 = 19×6", "114", "19×6", Y],
    ["Span sūra 9 → 27 = 19 sūras; Σ(9..27)", "342 = 19×18", "342", "19×18", Y],
    ["Sūra 96 verse 1 has 19 letters", "19", "18", "r = 18", N],
    ["Sūra 96 has 285 letters", "285 = 19×15", "288", "r = 3", N],
    ["First revelation 96:1–5 has 19 words", "19", "29", "r = 10", N],
    ["Total verses incl. Basmalas", "6346 = 19×334", "6348", "r = 17", N],
])

C.note("B · Basmala word-frequencies (numbered text + 112 Basmalas). The famous cluster — partly exact, partly not.")
C.table(["Word", "claimed", "measured", "÷19", "verdict"], [
    [C.ar("الرحمن") + " Ar-Raḥmān", "57 = 19×3", "57", "19×3", Y],
    [C.ar("الرحيم") + " Ar-Raḥīm", "114 = 19×6", "95", "19×5 (value differs)", Y],
    [C.ar("الله") + " Allah", "2698 = 19×142", "2695", "÷7 and ÷11, not 19", N],
    [C.ar("اسم") + " Ism", "19", "convention-dependent", "—", "~"],
])

C.note("C · Quranic Initials (muqaṭṭaʿāt) — the most famous claims. Re-counted neutrally, the split is the whole "
       "story: the orthographically STABLE letters (ق, ص) reproduce EXACTLY; the spelling-VARIABLE ones (ن, ي, ع, alif) shift off 19.")
C.table(["Initial · sūra(s)", "claimed", "measured", "÷19", "letter is"], [
    [C.ar("ق") + " · Sūra 50 (Qāf)", "57 = 19×3", "57", "19×3", "stable ✔"],
    [C.ar("ق") + " · Sūra 42", "57 = 19×3", "57", "19×3", "stable ✔"],
    [C.ar("ص") + " · Sūras 7, 19, 38", "152 = 19×8", "152", "19×8", "stable ✔"],
    [C.ar("ن") + " · Sūra 68 (Nūn)", "133 = 19×7", "138", "r = 5", "variable ✗"],
    [C.ar("ح م") + " · Sūras 40–46", "2147 = 19×113", "2112", "r = 3", "variable ✗"],
    [C.ar("ي س") + " · Sūra 36 (Yā-Sīn)", "285 = 19×15", "248", "r = 1*", "variable ✗"],
    [C.ar("ك ه ي ع ص") + " · Sūra 19", "798 = 19×42", "729", "r = 7", "variable ✗"],
    [C.ar("ا ل م") + " · Sūras 2,3,29–32", "= 19×k", "18,072", "r = 3", "alif — very variable ✗"],
    [C.ar("ا ل م ص") + " · Sūra 7", "= 19×k", "4,759", "r = 9", "alif — very variable ✗"],
])
C.note("Discrepancy between Khalifa's count and a neutral re-count, per initial-letter claim. Zero for the stable "
       "letters (ق, ص); 5–69 for the spelling-variable ones. The code lives precisely in the spelling.")
C.vbars([(C.ar("ق") + "·50", 0, C.TEAL, "Qāf sūra 50: 57 = 57, exact"),
         (C.ar("ق") + "·42", 0, C.TEAL, "Qāf sūra 42: 57 = 57, exact"),
         (C.ar("ص"), 0, C.TEAL, "Ṣād: 152 = 152, exact"),
         (C.ar("ن") + "·68", 5, C.CORAL, "Nūn: 133 claimed, 138 measured"),
         (C.ar("ح م"), 35, C.CORAL, "Ḥā-Mīm: 2147 vs 2112"),
         (C.ar("ي س"), 37, C.CORAL, "Yā-Sīn: 285 vs 248"),
         (C.ar("ك..ص"), 69, C.CORAL, "KHYʿṢ sūra 19: 798 vs 729")], ymax=75, fmt="{:.0f}")

C.note("D · Tolerance done right. A flat ±5% is bad method (for الله it admits 14 multiples of 19). Each claim gets "
       "a REALISTIC band from its true variance — and we ask if it still pins a SINGLE multiple of 19, specific to 19.")
C.table(["Claim · count", "realistic ±τ", "÷19 in band", "specific to 19?", "exactly ÷"], [
    ["Basmala = 19 letters", "±1 spelling", "✔ exact · 1", "yes", "19"],
    [C.ar("الرحمن") + " = 57", "±1 form", "✔ exact · 1", "yes", "19×3"],
    [C.ar("الله") + " = 2695", "±20 (1%)", "~ gap 3 · 2 mults", "✗ vacuous", "7 and 11"],
    ["Verses + Basmala = 6348", "±35 (schemes)", "~ gap 2 · 3 mults", "✗ vacuous", "23"],
])

C.section("Statistical core — six views of one fact: 19 has no special place")

C.note("① The raw material — most natural counts in the Qur'ān are small (verse counts, root frequencies). "
       "Context for everything below: small counts dominate.")
C.hist([258, 219, 263, 130, 102, 63, 49], ["<10", "10–19", "20–49", "50–99", "100–199", "200–499", "500+"],
       color=C.SLATE)

C.note("② Exact-multiple rate ÷ chance, for every divisor from 2 to 30. If a number were special its bar would rise "
       "above 1.0 (the dashed line). None does — and 19 (highlighted) is among the very lowest.")
C.hist([0.94, 1.03, 0.94, 1.25, 1.13, 0.96, 1.01, 0.94, 0.94, 0.93, 1.03, 0.94, 0.76, 0.77, 0.84, 0.75, 0.63,
        0.54, 0.83, 0.77, 0.71, 0.53, 0.80, 0.88, 0.77, 0.62, 0.59, 0.72, 0.64],
       [str(d) for d in range(2, 31)], highlight=17, ref=1.0, reflabel="chance")

C.note("③ The decisive chart — the remainder when each of the 1,084 counts is divided by 19. If 19 governed the "
       "text, remainder 0 (an exact multiple) would tower. Instead it is the 2nd-rarest of all 19 remainders, below "
       "the chance line. (The bulge at small remainders is the ordinary small-number effect; χ² rejects uniformity — "
       "but in the WRONG direction for the claim: remainder 0 is suppressed, not favoured.)")
C.hist([31, 40, 40, 37, 31, 131, 93, 72, 66, 64, 66, 64, 73, 60, 46, 40, 50, 34, 46],
       [str(i) for i in range(19)], highlight=0, ref=57, reflabel="chance (uniform)")

C.note("④ The same picture for a RIVAL number, 7 — remainders mod 7 are just as lumpy. Nothing distinguishes 19; "
       "every divisor shows the same small-number texture.")
C.hist([149, 144, 122, 145, 137, 208, 179], [str(i) for i in range(7)], ref=155, reflabel="chance (uniform)")

C.note("⑤ The distance from each count to its NEAREST multiple of 19 (0–9). If 19 pulled, gap 0 would spike. It is "
       "instead the rarest gap of all — exact divisibility by 19 is the least common outcome, not the most.")
C.hist([31, 86, 74, 87, 71, 177, 153, 145, 130, 130], [str(i) for i in range(10)], highlight=0, color=C.SLATE)

# ── 5 · GATING CHAIN ──
C.section("Gating chain — striking, then ordinary")
C.para("<b>Naive look</b> — basmala 19 letters, 114 = 6×19 sūras, sūra 96's 19 verses, الرحمن = 57, ق = 57: "
       "arresting, and genuinely real. <b>Control 1 · rival numbers</b> — 7, 11, 13, 17, 23 each hit their own "
       "multiples just as often; 19 is not special. <b>Control 2 · chance</b> — across 1,084 counts 19's hit-rate "
       "(2.9%) is below its arithmetic chance (5.3%). <b>Control 3 · spelling</b> — re-counted neutrally, the "
       "variable-letter and total claims shift off 19 (ن → 138, ي+س → 248, الم → 18,072). <b>Control 4 · degrees of "
       "freedom</b> — choosing which forms to count, whether to add the 112 Basmalas, which spelling to use, and "
       "(historically) rejecting 9:128–129, supplies all the freedom needed. The <i>pervasive</i> code collapses; "
       "the stable-letter cluster remains a real curiosity.")

# ── 6 · INTERPRETATION ──
C.section("Interpretation")
C.para("The single most telling result is the orthographic split. Code 19 reproduces <b>exactly</b> for counts that "
       "no one can dispute — the number of sūras, a verse count, the letters ق and ص (which have no spelling "
       "variants) — and it <b>fails</b> for every count that depends on a contested spelling: the letter alif "
       "(written or omitted hundreds of times), the yāʾ, the long word-totals. A genuine numerical law would not "
       "care whether a letter has orthographic variants. A counting artifact would live <i>precisely</i> in those "
       "variants — which is exactly what we see. The real anchors are the handful of unambiguous facts; the "
       "'pervasive code' is the freedom to pick a spelling, a word-form, and which counts to report.")

# ── 7 · CAVEATS & CONFOUNDS ──
C.section("Caveats & confounds")
C.para("<b>In fairness:</b> the anchors are real, and some claims reproduce <i>exactly</i> (الرحمن = 57, ق = 57, "
       "ص = 152) — this review does not pretend everything is bogus. <b>On method:</b> we count on a normalised "
       "rasm, not Khalifa's exact Uthmānī tally (whose spelling is itself contested) — so we refute the statistical "
       "privilege and the variable-letter totals, while granting the unambiguous facts. <b>On record:</b> the "
       "framework needs a fixed spelling, free inclusion of the Basmalas, and the rejection of two verses to "
       "balance, and is rejected by mainstream Sunnī and Shīʿī scholarship. <b>This is a statistical verdict, not a "
       "theological one.</b>")

# ── 8 · VERDICT ──
C.section("Verdict")
C.verdict("REFUTED-ARTIFACT",
          "A genuine cluster of 19-facts exists around the Basmala, the muṣḥaf's structure, and the stable initial "
          "letters — fairly credited. But the <b>pervasive code</b> fails: under a proper null 19 holds no privilege "
          "(rate ≤ chance, the rarest number), the variable-letter and total claims do not replicate under a neutral "
          "spelling, and the system needs selectable conventions and discarded text. Not a governing code.",
          "~85% the pervasive code is a counting artifact; the stable anchors are real",
          "a pre-registered, spelling-fixed scheme (no choices) showing 19-multiples far above chance and rivals",
          "such a scheme would reopen it — none has survived independent replication to date")

# ── REFLECTION ──
C.section("Reflection")
C.para("Three things make this case instructive. <b>The pull is real:</b> a handful of exact 19-facts genuinely "
       "exist — basmala 19 letters, 114 = 6×19 sūras, الرحمن = 57, ق = 57 — and the mind reads design into them. "
       "<b>The over-reach is equally real:</b> any long text offers thousands of countable quantities, so roughly "
       "one in nineteen is a multiple of 19 by arithmetic; collect the hits, forget the misses, and a 'code' "
       "appears. <b>The cure is to count everything, not just the hits:</b> across 1,084 counts, multiples of 19 are "
       "the rarest, not the commonest. The lesson is not about 19 — a pattern is only as strong as the null it is "
       "tested against.")

# ── SUMMARY ──
C.section("Summary — what held, what failed")
C.note("In the plainest terms — the genuine 19-facts on the left, the claims that do not survive a neutral count on the right.")
C.table(["✔ Holds — exactly divisible by 19", "✗ Fails — under a neutral count"], tight=False, rows=[
    ["Basmala = 19 letters · 114 sūras = 19×6", C.ar("الله") + " = 2695 — exactly ÷ 7 and ÷ 11, not 19"],
    ["Sūra 96 — 19 verses, 19th from the end", "Sūra 96 = 288 letters, not 285; 96:1–5 = 29 words, not 19"],
    [C.ar("الرحمن") + " = 57 · " + C.ar("ق") + " = 57 · " + C.ar("ص") + " = 152", C.ar("ن") + " = 138 · " + C.ar("ي س") + " = 248 · " + C.ar("الم") + " = 18,072"],
    ["Basmala occurs 114× · Σ(9..27) = 342", "Verses + Basmalas = 6348, not 6346"],
    ["— the unambiguous, stable counts —", "19's rate 2.9% (lowest); remainder 0 the 2nd-rarest"],
])

# ── LESSONS LEARNED ──
C.section("Lessons learned — for every claim about the Book")
C.para("This is a template, not a verdict on one person. Any claim about the Qur'ān — including our own — must clear "
       "the same gates, applied without favour. Each principle below earned its place by catching something here.")
C.table(["Principle", "What it caught in this review"], tight=False, rows=[
    ["Data-driven — re-count on the text, never assert", C.ar("الله", 17) + " = 2695, not the asserted 2698"],
    ["A proper null — test against chance AND rival numbers", "19's rate (2.9%) is below chance and the lowest of all numbers"],
    ["Robust — survive spelling & counting conventions", C.ar("ن", 17) + ", " + C.ar("ي", 17) + ", alif shift off 19; " + C.ar("ق", 17) + ", " + C.ar("ص", 17) + " do not"],
    ["No degrees of freedom — no discarding data to fit", "the code needed a fixed spelling and the rejection of 9:128–129"],
    ["Effect size, not a single striking hit", "multiples of 19 must beat chance — they do not"],
    ["Peer-reviewed & independently replicated", "no one has reproduced the full code under pre-registered rules"],
])
C.callout("The discipline, in plain terms",
          "A claim earns belief by surviving <b>scrutiny</b> — data, a proper null, and independent replication — "
          "not by being striking, emotionally satisfying, or popular. It must be <b>methodologically sound and "
          "statistically valid</b>, never " + C.ar("عوام گرایی", 17) + " or " + C.ar("عوام پسند", 17) + " "
          "(crowd-pleasing populism). The very same gates that refuted this claim also refuted one of <i>our own</i> "
          "findings — the inter-sūra coherence — which we recorded honestly as a size artifact. Rigour without favour, "
          "for claims we dislike and claims we would love to be true alike.", accent=C.SLATE)

# ── TAKEAWAY ──
C.section("Takeaway")
C.callout("In one line — for every reader",
          "A small, genuine cluster of 19-facts surrounds the Basmala and the stable letters — but there is <b>no "
          "governing 19-code</b>. Under a proper null, 19 holds no special place in the Qur'ān's counts; it is the "
          "<i>least</i> common multiple, not the most. The Qur'ān's structure is real and measurable — see the Āyah "
          "and Sūra close-ups — but this particular numerical claim is not where it lives.", accent=C.CORAL)

st.page_link("pages/27_Closeup_Index.py", label="← Back to the Close-up map", icon="🔎")
