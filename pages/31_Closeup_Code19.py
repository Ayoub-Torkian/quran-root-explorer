"""Close-up · Code 19 (Rashad Khalifa), reviewed — REFUTED-ARTIFACT. Claim-by-claim critical review."""
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

OK, MAYBE, NO = "✔ holds", "~ method-dependent", "✗ fails neutral"

# ── 1 · PROBLEM ──
C.hero("Code 19 (Rashad Khalifa), reviewed",
       "Does a mathematical code based on 19 govern the Qur'ān — or is it selected from countless possible counts?",
       "REFUTED-ARTIFACT", 22, "rasm counts (Basmalas included)", "DIVINE-DEFAULT · RANDOM null")
C.story(
    "Anchored on Q 74:30 (<i>“over it is nineteen”</i>), the claim is a pervasive 19-code in letters, words and "
    "sūras. We test <b>every</b> major claim on the text itself — Basmalas included — and the result is honest and "
    "split: <b>a real cluster of 19-facts around the Basmala, inside a wider claim that does not survive.</b>",
    "Written to be مقبول for the general reader (a clear scorecard) and مطلوب for the specialist (every count in a "
    "table, every divisor controlled). A methodological verdict, not a theological one.", accent=C.CORAL)
C.kpis([
    ("6", "exact ÷19 facts", "Counts exactly divisible by 19 under a neutral count (see scorecard)", C.TEAL),
    ("57 = 19×3", "الرحمن ✔", "Ar-Raḥmān occurs 57 times in this corpus — matches the claim exactly", C.TEAL),
    ("÷ 7 and 11", "الله, not 19", "Allah: measured 2695 = exactly divisible by 7 and 11, not 19 (claim: 2698)", C.CORAL),
    ("18 ≠ 19", "96:1 letters", "Sūra 96 verse 1 has 18 rasm letters here, not the claimed 19", C.CORAL),
    ("2.9%", "÷19 rate", "Share of 1,084 natural counts divisible by 19 — vs 5.3% chance (2nd-rarest remainder)", C.CORAL),
    ("0.55×", "19 vs chance", "Observed ÷ chance for 19 — lowest of all candidate numbers", C.CORAL),
    ("22", "grade", "REFUTED-ARTIFACT — the pervasive code, not the genuine anchors", C.CORAL),
])

# ── 2 · HYPOTHESIS ──
C.section("Hypothesis")
C.callout("If 19 truly governs the text, it must show privilege, robustness, and need no discarding",
          "A real numerical law would show three things: multiples of 19 appearing <b>above chance</b> and 19 "
          "<b>out-performing rival numbers</b> (7, 11, 13, 17, 23…); the key counts <b>robust</b> to spelling and to "
          "the choice of what to count; and <b>no text rejected</b> to make the totals balance. A genuine cluster of "
          "19-facts can exist without these — but the <i>pervasive code</i> needs all three.", accent=C.SLATE)

# ── 3 · METHOD & INSTRUMENTS ──
C.section("Method & instruments")
C.callout("The apparatus",
          "<b>Substrate</b> — Book6 rasm; word-forms counted as whole tokens. <b>Basmala</b> — the 112 unnumbered "
          "chapter-opening Basmalas are added to the word counts, as the theory requires. <b>Tests</b> — (a) verify "
          "each structural and word claim against the text; (b) the privilege test: divisibility of 1,202 natural "
          "counts by 19 vs by 7/11/13/17/23/29 vs chance (1/d); (c) the robustness test: re-count letters under a "
          "neutral spelling and see whether the totals still land on 19.", accent=C.SLATE)

# ── 4 · RESULTS ──
C.section("Results — every claim, stated and tested")

C.note("A · Structural claims — counts of sūras and verses. These are exact and they HOLD.")
C.table(["Claim (Khalifa)", "This study", "÷19", "Status"], [
    ["The Basmala has 19 letters", "19 letters", "19×1", OK],
    ["The Qur'ān has 114 sūras = 19×6", "114 sūras", "19×6", OK],
    ["Sūra 96 (first revealed) is 19th from the end", "114−96+1 = 19", "19×1", OK],
    ["Sūra 96 has 19 verses", "19 verses", "19×1", OK],
    ["Q 74:30 names the number nineteen", "textual anchor", "—", OK],
])

C.note("B · Basmala word-frequencies (numbered text + 112 opening Basmalas). The famous cluster — partly real, "
       "partly count-dependent.")
C.table(["Word", "Khalifa", "This study", "÷19?", "Status"], [
    [C.ar("الرحمن") + " Ar-Raḥmān", "57 = 19×3", "57", "✔ 19×3", OK],
    [C.ar("الرحيم") + " Ar-Raḥīm", "114 = 19×6", "95", "✔ 19×5 — different count", MAYBE],
    [C.ar("الله") + " Allah", "2698 = 19×142", "2695", "✗ 2695 not ÷19", NO],
    [C.ar("اسم") + " Ism", "19", "convention-dependent", "—", MAYBE],
])

C.note("C · Letter & total claims — re-counted under a neutral spelling, they do NOT replicate. The counts are "
       "spelling-dependent.")
C.table(["Claim (Khalifa)", "Khalifa", "This study", "Match?"], [
    ["Sūra 96, verse 1 — letters", "19", "18", NO],
    ["Sūra 96 — total letters", "285 = 19×15", "288", NO],
    ["Total verses incl. Basmalas", "6346 = 19×334", "6348", NO],
    ["Muqaṭṭaʿāt (initials) letter tallies", "various = 19×k", "spelling-dependent, disputed", NO],
])

C.note("D · Tolerance done right. A flat ±5% is itself bad method — for الله it would admit 14 multiples of 19, "
       "for the verse-total 33, so 'near a multiple' becomes automatic. Instead each claim gets a REALISTIC band "
       "from its true variance source — spelling for letters, form-inclusion for words, numbering-scheme spread for "
       "verse totals — and we ask whether that band still pins a SINGLE multiple of 19, and whether the count is "
       "specific to 19 rather than equally near 7, 11, 13…")
C.table(["Claim · count", "realistic ±τ", "÷19 in band", "specific to 19?", "exactly divisible by"], [
    ["Basmala = 19 letters", "±1 spelling", "✔ exact · 1", "yes", "19"],
    ["114 sūras", "±0 fixed", "✔ exact · 1", "—", "19 (also 2,3,6)"],
    ["Sūra 96 · 19 verses, 19th from end", "±0–1", "✔ exact · 1", "yes", "19"],
    [C.ar("الرحمن") + " = 57", "±1 form", "✔ exact · 1", "yes", "19×3"],
    [C.ar("الرحيم") + " = 95", "±3 form", "✔ exact · 1", "yes", "19×5 (claim: 114)"],
    [C.ar("الله") + " = 2695", "±20 (1% forms)", "~ gap 3 · 2 mults", "✗ vacuous", "7 and 11, NOT 19"],
    ["Sūra 96 = 288 letters", "±5 (1.5%)", "~ gap 3 · 1", "✗ near 7,11,13,17", "—"],
    ["Verses + Basmala = 6348", "±35 (schemes)", "~ gap 2 · 3 mults", "✗ vacuous", "23, NOT 19"],
])
C.note("The split is clean. Where a count is intrinsically PRECISE — structure, clean words — the 19-facts are "
       "EXACT and real (basmala, 114 sūras, sūra 96, الرحمن = 57, الرحيم = 95 = 19×5). Where a count is intrinsically "
       "VARIABLE — الله's forms, verse totals — even a realistic band spans 2–3 multiples of 19 and the count is "
       "exactly divisible by OTHER numbers (الله by 7 and 11; the verse-total by 23). The genuine 19-cluster is the "
       "precise small counts; the 'pervasive' part is the variable large ones, where 19 is not specific.")
C.note("E · No statistical privilege — every candidate number, side by side. Across 1,084 natural counts of the "
       "text, the exact-multiple rate of each number tracks pure chance (1/d); 19's rate is the LOWEST relative to "
       "chance, not the highest.")
C.table(["divisor d", "exact multiples", "observed rate", "chance 1/d", "obs ÷ chance"], [
    ["7", "149", "13.7%", "14.3%", "0.96"],
    ["11", "92", "8.5%", "9.1%", "0.93"],
    ["13", "78", "7.2%", "7.7%", "0.94"],
    ["17", "48", "4.4%", "5.9%", "0.74"],
    ["19   ← claimed special", "31", "2.9%", "5.3%", "0.55"],
    ["23", "25", "2.3%", "4.3%", "0.53"],
    ["29", "27", "2.5%", "3.4%", "0.74"],
])
C.note("F · The decisive picture — the remainder when each of the 1,084 counts is divided by 19. If 19 governed "
       "the text, remainder 0 (an exact multiple of 19) would tower above the rest. Instead it is the 2nd-rarest of "
       "the 19 possible remainders — 31 counts, below the chance line. The bulge at small remainders is the ordinary "
       "small-number effect, unrelated to 19; the χ² test rejects uniformity, but in the WRONG direction for the "
       "claim — remainder 0 is suppressed, not favoured.")
C.hist([31, 40, 40, 37, 31, 131, 93, 72, 66, 64, 66, 64, 73, 60, 46, 40, 50, 34, 46],
       [str(i) for i in range(19)], highlight=0, ref=57, reflabel="chance (uniform)")

# ── 5 · GATING CHAIN ──
C.section("Gating chain — striking, then ordinary")
C.para("<b>Naive look</b> — basmala 19 letters, 114 = 6×19 sūras, sūra 96's 19 verses and 19th-from-end, "
       "الرحمن = 57: arresting, and genuinely real. <b>Control 1 · rival numbers</b> — 7, 11, 13, 17, 23 each hit "
       "their own multiples just as often; 19 is not special. <b>Control 2 · chance</b> — across 1,202 counts 19's "
       "hit-rate (3.2%) is <i>below</i> its arithmetic chance (5.3%). <b>Control 3 · spelling</b> — re-counted "
       "neutrally, the letter totals shift off 19 (96:1 → 18; sūra 96 → 288; total → 6348). <b>Control 4 · degrees "
       "of freedom</b> — choosing which forms to count, whether to add the 112 Basmalas, and (historically) "
       "rejecting 9:128–129, supplies all the freedom needed. The <i>pervasive</i> code collapses; the Basmala "
       "cluster remains a real curiosity.")

# ── 6 · INTERPRETATION ──
C.section("Interpretation")
C.para("Two truths sit together. First, a genuine knot of 19-facts surrounds the Basmala and the muṣḥaf's frame "
       "(19 letters; 114 = 6×19 sūras; sūra 96; الرحمن = 57) — real, and the honest source of the theory's pull. "
       "Second, the move from that knot to a <b>governing code</b> is where it fails: any rich text offers thousands "
       "of countable quantities, about one in nineteen is a multiple of 19 by arithmetic, and reporting the hits "
       "while dropping the misses (the <b>multiple-comparisons</b> / 'Texas sharpshooter' problem) manufactures a "
       "pattern the data do not privilege. The letter-level claims, re-counted neutrally, simply do not hold.")

# ── 7 · CAVEATS & CONFOUNDS ──
C.section("Caveats & confounds")
C.para("<b>In fairness:</b> the anchors are real and some word-counts (الرحمن = 57) replicate exactly — this review "
       "does not pretend everything is bogus. <b>On method:</b> we count on a normalised rasm, not Khalifa's exact "
       "letter-by-letter Uthmānī tally (whose spelling is itself contested) — so we refute the <i>statistical "
       "privilege</i> and the <i>letter totals</i>, while granting the genuine word/structure facts. <b>On record:</b> "
       "the framework needs a fixed spelling, free inclusion of the Basmalas, and the rejection of two verses to "
       "balance; it is rejected by mainstream Sunnī and Shīʿī scholarship. <b>This is a statistical verdict, not a "
       "theological one.</b>")

# ── 8 · VERDICT ──
C.section("Verdict")
C.verdict("REFUTED-ARTIFACT",
          "A genuine cluster of 19-facts exists around the Basmala and the muṣḥaf's structure — and is fairly "
          "credited. But the <b>pervasive code</b> fails: under a proper null 19 holds no privilege (rate ≤ chance, "
          "below rival numbers), the letter totals do not replicate under a neutral spelling, and the system needs "
          "selectable conventions and discarded text. Not established as a governing code.",
          "~85% the pervasive code is a multiple-comparisons artifact; the Basmala anchors are real",
          "a pre-registered, spelling-fixed count scheme (no choices) showing 19-multiples far above chance and rivals",
          "such a scheme would reopen it — none has survived independent replication to date")

# ── REFLECTION ──
C.section("Reflection")
C.para("Three things make this case instructive. <b>The pull is real:</b> a handful of exact 19-facts genuinely "
       "exist — the Basmala's 19 letters, 114 = 6×19 sūras, الرحمن = 57 — and the mind naturally reads design into "
       "them. <b>The over-reach is equally real:</b> any long text offers thousands of countable quantities, so "
       "roughly one in nineteen is a multiple of 19 by arithmetic alone — collect the hits, forget the misses, and "
       "a 'code' appears. <b>The cure is to count everything, not just the hits:</b> across 1,084 natural counts, "
       "multiples of 19 turned out to be the <i>rarest</i>, not the commonest. The real lesson is not about 19 at "
       "all — it is that a pattern is only as strong as the null it was tested against.")

# ── SUMMARY ──
C.section("Summary — what held, what failed")
C.note("Side by side, in the plainest terms — the genuine 19-facts on the left, the claims that do not survive a "
       "neutral count on the right.")
C.table(["✔ Holds — exactly divisible by 19", "✗ Fails — under a neutral count"], [
    ["Basmala = 19 letters", C.ar("الله") + " = 2695 — exactly ÷ 7 and ÷ 11, not 19"],
    ["114 sūras = 19 × 6", "Sūra 96 = 288 letters, not the claimed 285"],
    ["Sūra 96 — 19 verses, and 19th from the end", "Verses + Basmalas = 6348, not the claimed 6346"],
    [C.ar("الرحمن") + " = 57 = 19 × 3", "19's exact-multiple rate 2.9% — lowest of any number"],
    [C.ar("الرحيم") + " = 95 = 19 × 5", "remainder 0 is the 2nd-rarest of the 19 remainders"],
])

# ── TAKEAWAY ──
C.section("Takeaway")
C.callout("In one line — for every reader",
          "A small, genuine cluster of 19-facts surrounds the Basmala — but there is <b>no governing 19-code</b>. "
          "Under a proper null, 19 holds no special place in the Qur'ān's counts; it is the <i>least</i> common "
          "multiple, not the most. The Qur'ān's structure is real and measurable — see the Āyah and Sūra close-ups — "
          "but this particular numerical claim is not where it lives.", accent=C.CORAL)

st.page_link("pages/27_Closeup_Index.py", label="← Back to the Close-up map", icon="🔎")
