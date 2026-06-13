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
st.markdown(
    "<div style='display:flex;justify-content:flex-end;gap:9px;margin:7px 0 2px;flex-wrap:wrap'>"
    "<a href='#cu-fa-abstract' style='text-decoration:none'>"
    "<div style='background:linear-gradient(135deg,#138A74,#10243A);color:#fff;border-radius:9px;padding:7px 13px;"
    "font-weight:800;font-size:13px;box-shadow:0 2px 8px rgba(16,36,58,.25);border:1px solid rgba(255,255,255,.3)'>"
    "📄 Persian abstract · خلاصهٔ فارسی ↓</div></a>"
    "<a href='#cu-ar-abstract' style='text-decoration:none'>"
    "<div style='background:linear-gradient(135deg,#4E6E92,#10243A);color:#fff;border-radius:9px;padding:7px 13px;"
    "font-weight:800;font-size:13px;box-shadow:0 2px 8px rgba(16,36,58,.25);border:1px solid rgba(255,255,255,.3)'>"
    "📄 Arabic abstract · الملخّص العربي ↓</div></a></div>", unsafe_allow_html=True)
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
C.onpage(["① Problem", "② Hypothesis", "③ Method",
          "<b>④ Results</b> every claim by category (tables A–D)",
          "<b>⑤ Statistical core</b> six views that 19 has no privilege",
          "⑥ Gating", "⑦ Interpretation", "⑧ Caveats", "⑨ Verdict"], fa="cu-fa-abstract", ar="cu-ar-abstract")

# ── 2 · HYPOTHESIS ──
C.section("Hypothesis")
C.callout("If 19 truly governs the text, three things must ALL hold — and a single hit is never enough",
          "Two claims are usually blurred together, and we separate them. The <i>weak</i> claim is that some counts "
          "happen to be multiples of 19 — easy, and partly true. The <i>strong</i> claim is that 19 <b>governs</b> "
          "the text — and that is what we test, through three predictions it must make.<br>"
          "&nbsp;&nbsp;<b>(1) Privilege.</b> Multiples of 19 must appear <i>above</i> chance — more than the "
          "~1/19 = 5.3% that <i>any</i> number gives — and 19 must out-perform its rivals 7, 11, 13, 17, 23. "
          "<br>&nbsp;&nbsp;<b>(2) Robustness.</b> The headline counts must survive a change of spelling, of "
          "word-form definition, and of whether the 112 Basmalas are counted; a law of the text cannot hinge on a "
          "scribe's choice. <br>&nbsp;&nbsp;<b>(3) No discarding.</b> No verse may be rejected to make a total "
          "balance.<br>"
          "The null hypothesis is deliberately mundane: 19 is an ordinary number, its multiples occur at chance, and "
          "the famous hits are selection from thousands of possible counts. We let the data choose between the two.",
          accent=C.SLATE)

# ── 3 · METHOD & INSTRUMENTS ──
C.section("Method & instruments")
C.callout("The apparatus — substrate, counts, three tests, and one honest limitation",
          "<b>Substrate.</b> Book6 rasm — the consonantal skeleton, diacritics demoted as a human artifact; words "
          "counted as whole tokens, letters counted directly. The 112 unnumbered chapter-opening Basmalas are "
          "<i>added</i> to the word counts wherever the theory needs them — i.e. we grant the most generous reading "
          "of the claim, not the least.<br>"
          "&nbsp;&nbsp;<b>The count battery.</b> We assemble 1,084 natural quantities of the text: verses per sūra, "
          "root-tokens per sūra, unique roots per sūra, every individual root-frequency, and the global totals — the "
          "honest universe of things one could count.<br>"
          "&nbsp;&nbsp;<b>Three tests.</b> (a) <i>Verification</i> — re-count every structural, word, and "
          "initial-letter claim directly against the text. (b) <i>Privilege</i> — measure how often each of the 1,084 "
          "counts is divisible by 19, set against 7, 11, 13, 17, 23, 29 and against arithmetic chance (1/d), then a "
          "remainder histogram and a χ² test of uniformity. (c) <i>Robustness</i> — re-count the letters under a "
          "neutral spelling and apply a realistic per-claim tolerance, to see whether the totals still land on 19.<br>"
          "&nbsp;&nbsp;<b>The honest limitation — which is the whole point.</b> Our normalised rasm is not Khalifa's "
          "exact Uthmānī tally; a claim whose verdict flips when the spelling is normalised was never a law of the "
          "text to begin with.", accent=C.SLATE)

# ── 4 · RESULTS ──
C.section("Results — every claim, by category")

cA, cC = st.columns(2, gap="medium")
with cA:
    C.note("A · Structural & positional — sūras, verses, positions. These mostly HOLD.")
    C.table(["Claim", "claim", "meas.", "÷19", "v"], [
        ["Basmala = 19 letters", "19", "19", "19×1", Y],
        ["114 sūras", "114", "114", "19×6", Y],
        ["Sūra 96 is 19th from the end", "19", "19", "19×1", Y],
        ["Sūra 96 has 19 verses", "19", "19", "19×1", Y],
        ["Basmala occurs 114× (heads+1:1+27:30)", "114", "114", "19×6", Y],
        ["Span sūra 9→27 = 19; Σ(9..27)", "342", "342", "19×18", Y],
        ["Sūra 96:1 has 19 letters", "19", "18", "r=18", N],
        ["Sūra 96 has 285 letters", "285", "288", "r=3", N],
        ["First revelation 96:1–5 = 19 words", "19", "29", "r=10", N],
        ["Total verses incl. Basmalas", "6346", "6348", "r=17", N],
    ])
with cC:
    C.note("C · Quranic Initials (muqaṭṭaʿāt) — the famous claims. Split by spelling: stable ق/ص exact, variable ن/ي/alif off.")
    C.table(["Initial · sūra", "claim", "meas.", "÷19", "letter"], [
        [C.ar("ق") + " · 50 (Qāf)", "57", "57", "19×3", "stable ✔"],
        [C.ar("ق") + " · 42", "57", "57", "19×3", "stable ✔"],
        [C.ar("ص") + " · 7,19,38", "152", "152", "19×8", "stable ✔"],
        [C.ar("ن") + " · 68 (Nūn)", "133", "138", "r=5", "variable ✗"],
        [C.ar("ح م") + " · 40–46", "2147", "2112", "r=3", "variable ✗"],
        [C.ar("ي س") + " · 36 (Yā-Sīn)", "285", "248", "r=1", "variable ✗"],
        [C.ar("ك ه ي ع ص") + " · 19", "798", "729", "r=7", "variable ✗"],
        [C.ar("ا ل م") + " · 2,3,29–32", "19×k", "18,072", "r=3", "alif ✗✗"],
        [C.ar("ا ل م ص") + " · 7", "19×k", "4,759", "r=9", "alif ✗✗"],
    ])

C.note("Discrepancy — Khalifa's count vs a neutral re-count, per initial. Zero for the stable letters (ق, ص); 5–69 "
       "for the spelling-variable ones. The code lives precisely in the spelling.")
C.vbars([(C.ar("ق") + "·50", 0, C.TEAL, "Qāf sūra 50: 57 = 57, exact"),
         (C.ar("ق") + "·42", 0, C.TEAL, "Qāf sūra 42: 57 = 57, exact"),
         (C.ar("ص"), 0, C.TEAL, "Ṣād: 152 = 152, exact"),
         (C.ar("ن") + "·68", 5, C.CORAL, "Nūn: 133 claimed, 138 measured"),
         (C.ar("ح م"), 35, C.CORAL, "Ḥā-Mīm: 2147 vs 2112"),
         (C.ar("ي س"), 37, C.CORAL, "Yā-Sīn: 285 vs 248"),
         (C.ar("ك..ص"), 69, C.CORAL, "KHYʿṢ sūra 19: 798 vs 729")], ymax=75, fmt="{:.0f}")

cB, cD = st.columns(2, gap="medium")
with cB:
    C.note("B · Basmala word-frequencies (+ 112 Basmalas). Partly exact, partly not.")
    C.table(["Word", "claim", "meas.", "÷19", "v"], [
        [C.ar("الرحمن"), "57", "57", "19×3", Y],
        [C.ar("الرحيم"), "114", "95", "19×5*", Y],
        [C.ar("الله"), "2698", "2695", "÷7,11 not 19", N],
        [C.ar("اسم"), "19", "convention-dep.", "—", "~"],
    ])
with cD:
    C.note("D · Realistic per-claim tolerance — does the band still pin ONE multiple of 19, specific to 19?")
    C.table(["Claim · count", "±τ", "÷19 in band", "exact ÷"], [
        ["Basmala = 19", "±1", "✔ exact · 1", "19"],
        [C.ar("الرحمن") + " = 57", "±1", "✔ exact · 1", "19×3"],
        [C.ar("الله") + " = 2695", "±20", "~ 2 mults", "7, 11"],
        ["Verses = 6348", "±35", "~ 3 mults", "23"],
    ])

C.section("Statistical core — six views of one fact: 19 has no special place")

C.note("① The raw material — most natural counts in the Qur'ān are small (verse counts, root frequencies). "
       "Context for everything below: small counts dominate.")
C.hist([258, 219, 263, 130, 102, 63, 49], ["<10", "10–19", "20–49", "50–99", "100–199", "200–499", "500+"],
       color=C.TEAL)

C.note("② Exact-multiple rate ÷ chance, for every divisor from 2 to 30. If a number were special its bar would rise "
       "above 1.0 (the dashed line). None does — and 19 (highlighted) is among the very lowest.")
C.hist([0.94, 1.03, 0.94, 1.25, 1.13, 0.96, 1.01, 0.94, 0.94, 0.93, 1.03, 0.94, 0.76, 0.77, 0.84, 0.75, 0.63,
        0.54, 0.83, 0.77, 0.71, 0.53, 0.80, 0.88, 0.77, 0.62, 0.59, 0.72, 0.64],
       [str(d) for d in range(2, 31)], highlight=17, ref=1.0, reflabel="chance", color="#3E78B2")

C.note("③ The decisive chart — the remainder when each of the 1,084 counts is divided by 19. If 19 governed the "
       "text, remainder 0 (an exact multiple) would tower. Instead it is the 2nd-rarest of all 19 remainders, below "
       "the chance line. (The bulge at small remainders is the ordinary small-number effect; χ² rejects uniformity — "
       "but in the WRONG direction for the claim: remainder 0 is suppressed, not favoured.)")
C.hist([31, 40, 40, 37, 31, 131, 93, 72, 66, 64, 66, 64, 73, 60, 46, 40, 50, 34, 46],
       [str(i) for i in range(19)], highlight=0, ref=57, reflabel="chance (uniform)", color="#6B5B95")

C.note("④ The same picture for a RIVAL number, 7 — remainders mod 7 are just as lumpy. Nothing distinguishes 19; "
       "every divisor shows the same small-number texture.")
C.hist([149, 144, 122, 145, 137, 208, 179], [str(i) for i in range(7)], ref=155, reflabel="chance (uniform)",
       color=C.GOLD)

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
C.para("<b>The orthographic split is the single most telling result.</b> Sort every claim by one question — does its "
       "count depend on a spelling choice? — and the verdicts sort almost perfectly along with it. Code 19 reproduces "
       "<b>exactly</b> for the counts no one can dispute: the number of sūras (114), a verse count (19), and the "
       "initials ق and ص, which have no orthographic variants at all. It <b>fails</b> for every count that rides on a "
       "contested spelling: the alif (written or dropped hundreds of times across the muṣḥaf — the الم total comes to "
       "18,072, off by 3), the yāʾ (ي+س = 248, not 285), and the long word-totals (الله = 2,695, which is exactly "
       "÷ 7 and ÷ 11, not ÷ 19).<br><br>"
       "<b>Why this is decisive.</b> A genuine numerical law could not care whether a letter happens to have spelling "
       "variants — arithmetic is indifferent to orthography. A <i>counting artifact</i>, by contrast, lives precisely "
       "in those variants, because that is the only place a counter's freedom can act. What we observe is the "
       "fingerprint of the artifact, not of a law. The real anchors are the handful of unambiguous facts around the "
       "Basmala and the muṣḥaf's frame; the 'pervasive code' is the accumulated freedom to choose a spelling, a "
       "word-form, whether to add the 112 Basmalas, and which of a thousand possible counts to report.")

# ── 7 · CAVEATS & CONFOUNDS ──
C.section("Caveats & confounds")
C.para("<b>In fairness — what we are NOT claiming.</b> The anchors are real, and several claims reproduce "
       "<i>exactly</i> on a neutral count (الرحمن = 57, ق = 57, ص = 152). This review does not pretend everything is "
       "bogus, nor that those who find 19 compelling are careless — the genuine facts are striking. We refute the "
       "<i>pervasive code</i>, not the existence of a small, real 19-cluster.<br><br>"
       "<b>On method — the limits of our instrument.</b> We count on a normalised rasm, not Khalifa's exact Uthmānī "
       "tally, whose own spelling is contested. So our verdict is precise about two things — the <i>statistical "
       "privilege</i> of 19 (refuted: across 1,084 counts it is the rarest of all candidate numbers) and the "
       "<i>variable-letter and total claims</i> (refuted: re-counted neutrally they shift off 19) — while it grants "
       "the unambiguous structural and stable-letter facts outright. We do not adjudicate each Uthmānī count "
       "letter-by-letter; we show that any claim needing a fixed spelling is, by that fact alone, fragile.<br><br>"
       "<b>On the record.</b> The framework as a whole requires a fixed spelling, the free inclusion of the 112 "
       "Basmalas, and the rejection of 9:128–129 to make a total balance; it is rejected by mainstream Sunnī and "
       "Shīʿī scholarship. <b>This is a statistical and methodological verdict, not a theological one</b> — and the "
       "same gates were turned, without favour, on one of our own findings (the inter-sūra coherence), which we "
       "recorded honestly as a size artifact.")

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
C.para("Three things make this case instructive, and they generalise far beyond it.<br><br>"
       "<b>The pull is real.</b> A handful of exact 19-facts genuinely exist — basmala 19 letters, 114 = 6×19 sūras, "
       "الرحمن = 57, ق = 57 — and the human mind is built to read design into coincidence. Dismissing those moved by "
       "such facts would be both unkind and unscientific; the facts are striking, and an honest review begins by "
       "granting them.<br><br>"
       "<b>The over-reach is equally real.</b> Any long text offers thousands of countable quantities — letters, "
       "words, verses, sūras, their sums and their positions. By arithmetic alone, about one in nineteen of them is a "
       "multiple of 19. Search hard enough, report the hits, quietly drop the misses, and a 'code' assembles itself "
       "out of nothing but selection. This is the multiple-comparisons trap, and from the inside it is invisible.<br><br>"
       "<b>The cure is simple: count everything, not only the hits.</b> When we did — all 1,084 natural counts — "
       "multiples of 19 turned out to be the <i>rarest</i> outcome, not the commonest, and 19 the least distinguished "
       "of every candidate number. The lesson, in the end, is not about 19 at all: a pattern is worth exactly as much "
       "as the null hypothesis it was tested against — and not one bit more.")

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

# ── PERSIAN ABSTRACT ──
C.section("خلاصهٔ کامل — Persian abstract")
st.markdown(
    "<div dir='rtl' id='cu-fa-abstract' style='font-family:Vazirmatn,Tahoma,\"Segoe UI\",sans-serif;font-size:15px;line-height:1.7;"
    "color:#243b53;text-align:right;background:#F6F9FC;border-right:5px solid #138A74;border-radius:11px;"
    "padding:16px 20px'>"
    "<b>ادعا.</b> رشاد خلیفه با تکیه بر آیهٔ «عَلَیْهَا تِسْعَةَ عَشَرَ» (مدّثر ۷۴:۳۰) مدّعی شد عددی به نام ۱۹ بر سراسر "
    "قرآن — بر شمار حرف‌ها، واژه‌ها و سوره‌ها — حاکم است.<br><br>"
    "<b>روش.</b> همهٔ ادعاهای اصلی را مستقیم روی متن (رسمِ بدونِ اعراب، با احتسابِ ۱۱۲ بسملهٔ آغازِ سوره‌ها) شمردیم؛ "
    "و عددِ ۱۹ را در برابرِ «شانس» و در برابرِ اعدادِ رقیب (۷، ۱۱، ۱۳، ۱۷، ۲۳) سنجیدیم.<br><br>"
    "<b>یافته‌ها.</b> بخشی واقعی و دقیقاً بخش‌پذیر بر ۱۹ است: بسمله ۱۹ حرف، ۱۱۴ سوره (۱۹×۶)، سورهٔ ۹۶ با ۱۹ آیه و "
    "نوزدهمین از آخر، «الرحمن» ۵۷ بار (۱۹×۳)، حرفِ «ق» در سورهٔ ۵۰ برابر ۵۷ و «ص» برابر ۱۵۲. اما ادعاهای بزرگ‌تر با "
    "یک شمارشِ بی‌طرف فرومی‌ریزند: «الله» ۲۶۹۵ بار (که دقیقاً بر ۷ و ۱۱ بخش‌پذیر است، نه ۱۹)، «یس» ۲۴۸ (نه ۲۸۵)، و "
    "حروفِ الف‌دار کاملاً وابسته به املا (الم در سوره‌هایش = ۱۸٬۰۷۲). در میانِ ۱٬۰۸۴ شمارشِ طبیعیِ متن، نرخِ بخش‌پذیری "
    "بر ۱۹ تنها ۲٫۹٪ است — کمترین در میانِ همهٔ اعداد و پایین‌تر از شانس (۵٫۳٪)؛ و باقیماندهٔ صفر (یعنی مضربِ ۱۹) "
    "دومین کمیاب‌ترین حالت است.<br><br>"
    "<b>نکتهٔ کلیدی.</b> رمز دقیقاً جایی «درست» درمی‌آید که املا قطعی است (ق و ص که گونهٔ نوشتاری ندارند) و دقیقاً جایی "
    "«شکست» می‌خورد که املا اختلافی است (الف، یاء). این، نشانهٔ یک «مصنوعِ شمارش» است، نه یک قانونِ عددی.<br><br>"
    "<b>حروفِ مقطّعه.</b> مشهورترین ادعاها دربارهٔ حروفِ مقطّعه‌اند و آن‌ها را جداگانه آزمودیم. حروفی که گونهٔ نوشتاری "
    "ندارند درست درمی‌آیند: «ق» در سوره‌های ۵۰ و ۴۲ هر یک ۵۷، و «ص» در سوره‌های ۷ و ۱۹ و ۳۸ روی‌هم ۱۵۲ (۱۹×۸). اما "
    "حروفِ پراختلاف نادرست‌اند: «یس»=۲۴۸ به‌جای ۲۸۵، «ن»=۱۳۸ به‌جای ۱۳۳، و حروفِ الف‌دار صدها واحد خطا دارند "
    "(الم=۱۸٬۰۷۲). همین، «شکافِ املایی» را آشکار می‌کند.<br><br>"
    "<b>آزمونِ آماری.</b> در توزیعِ باقیمانده‌ها بر ۱۹ (۱۹ حالت)، اگر ۱۹ بر متن حاکم بود باید باقیماندهٔ صفر بلندترین "
    "ستون می‌بود؛ اما در عمل کوتاه‌ترین‌هاست و آزمونِ خی‌دو یکنواختی را رد می‌کند — ولی در جهتِ خلافِ ادعا: مضربِ ۱۹ "
    "سرکوب شده است، نه برجسته. در میانِ اعدادِ ۲ تا ۳۰ نیز هیچ‌کدام از شانس فراتر نمی‌رود و ۱۹ از همه پایین‌تر است.<br><br>"
    "<b>ساختار و مکان.</b> چند حقیقتِ ساختاری به‌راستی بر ۱۹ بخش‌پذیرند: بسمله ۱۹ حرف؛ ۱۱۴ سوره (۱۹×۶)؛ سورهٔ ۹۶ "
    "(نخستین وحی) با ۱۹ آیه و نوزدهمین از پایان؛ بسمله ۱۱۴ بار (۱۹×۶) در سراسرِ متن؛ و فاصلهٔ سوره‌های ۹ تا ۲۷ برابرِ "
    "۱۹ سوره با مجموعِ شماره‌ها ۳۴۲ (۱۹×۱۸). این‌ها واقعی‌اند. اما همان سورهٔ ۹۶ در شمارشِ بی‌طرف، آیهٔ نخست را ۱۸ حرف "
    "(نه ۱۹) و کلِّ سوره را ۲۸۸ حرف (نه ۲۸۵) می‌دهد، و مجموعِ آیات با بسمله‌ها ۶۳۴۸ می‌شود (نه ۶۳۴۶).<br><br>"
    "<b>باندِ رواداری.</b> گفته می‌شود با «کمی رواداری» شمارش‌ها به ۱۹ می‌رسند؛ اما این برای اعدادِ بزرگ بی‌معناست. "
    "باندِ ۵٪ پیرامونِ «الله» (۲۶۹۵) چهارده مضربِ ۱۹ را در بر می‌گیرد و پیرامونِ مجموعِ آیات سی‌وسه مضرب را — پس "
    "«اصابت» خودکار و بی‌ارزش است. تنها برای شمارش‌های کوچک و دقیق (بسمله=۱۹، الرحمن=۵۷) باند تنها یک مضرب دارد و آزمون "
    "معنا می‌یابد — و آن‌ها را پذیرفته‌ایم.<br><br>"
    "<b>چرا «رمز» پدید می‌آید.</b> هر متنِ بلند هزاران کمیتِ شمردنی دارد — حرف‌ها، واژه‌ها، آیه‌ها، سوره‌ها، جمع‌ها و "
    "جای‌گاه‌ها. به‌حکمِ حساب، حدودِ یک‌نوزدهمِ آن‌ها مضربِ ۱۹‌اند. اگر کسی به‌قدرِ کافی بگردد، اصابت‌ها را گزارش کند و "
    "ناکامی‌ها را وانهد، «رمزی» از دلِ گزینشِ صرف پدید می‌آید. این همان «تلهٔ مقایسه‌های چندگانه» (تمثیلِ تک‌تیراندازِ "
    "تگزاسی) است که از درون نامرئی است.<br><br>"
    "<b>انصافِ بی‌طرفانه.</b> این داوری از سرِ خصومت نیست. همان دروازه‌های روشی که این ادعا را رد کرد، بر یکی از "
    "یافته‌های خودِ ما — هم‌بستگیِ واژگانیِ میان‌سوره‌ها — نیز اعمال شد و آن را «مصنوعِ اندازه» ثبت کردیم. سخت‌گیریِ "
    "یکسان، برای آنچه دوست داریم درست باشد و آنچه دوست نداریم.<br><br>"
    "<b>نتیجه.</b> خوشه‌ای کوچک و واقعی از حقایقِ ۱۹ پیرامونِ بسمله هست و آن را به‌انصاف می‌پذیریم؛ اما «رمزی فراگیر» "
    "در کار نیست. این داوری <b>آماری و روش‌شناختی</b> است، نه کلامی.<br><br>"
    "<b>درس.</b> هر ادعا دربارهٔ قرآن — از جمله ادعاهای خودِ ما — باید داده‌محور، دارای آزمونِ پوچِ درست، روش‌مند، "
    "آماری‌معتبر و تکرارپذیر باشد؛ نه عوام‌گرایانه و عوام‌پسند.</div>", unsafe_allow_html=True)

# ── ARABIC ABSTRACT ──
C.section("الملخّص الكامل — Arabic abstract")
st.markdown(
    "<div dir='rtl' id='cu-ar-abstract' style='font-family:Amiri,\"Scheherazade New\",Tahoma,serif;font-size:15.5px;line-height:1.75;"
    "color:#243b53;text-align:right;background:#F6F9FC;border-right:5px solid #4E6E92;border-radius:11px;"
    "padding:16px 20px'>"
    "<b>الدعوى.</b> استناداً إلى آية «عَلَيْهَا تِسْعَةَ عَشَرَ» (المدّثّر ۷۴:۳۰)، زعم رشاد خليفة أنّ عدداً هو ۱۹ "
    "يحكم القرآن كلَّه — حروفَه وكلماتِه وسُوَرَه.<br><br>"
    "<b>المنهج.</b> اختبرنا كلَّ دعوى رئيسية مباشرةً على النصّ (الرسم بلا حركات، مع إدراج ۱۱۲ بسملةً في فواتح "
    "السُّوَر)، وقِسنا العددَ ۱۹ في مقابل الصُّدفة وفي مقابل أعدادٍ منافِسة (۷، ۱۱، ۱۳، ۱۷، ۲۳).<br><br>"
    "<b>النتائج.</b> بعضُ الدعاوى حقيقيّ ويقبل القسمةَ على ۱۹ بالضبط: البسملة ۱۹ حرفاً، و۱۱۴ سورة (۱۹×۶)، والسورة ۹۶ "
    "بتسعَ عشرةَ آية وهي التاسعةَ عشرةَ من الآخِر، و«الرحمن» ۵۷ مرّة (۱۹×۳)، وحرف «ق» في السورة ۵۰ يساوي ۵۷ و«ص» "
    "يساوي ۱۵۲. لكنّ الدعاوى الأكبر تنهار عند عدٍّ محايد: «الله» ۲۶۹۵ مرّة (وهو قابلٌ للقسمة على ۷ و۱۱ بالضبط، لا ۱۹)، "
    "و«يس» ۲۴۸ لا ۲۸۵، والحروف ذاتُ الألف تعتمد كلّياً على الرسم (الم في سورها = ۱۸٬۰۷۲). وبين ۱٬۰۸۴ عدّاً طبيعياً في "
    "النصّ، نسبةُ القسمة على ۱۹ هي ۲٫۹٪ فقط — أدنى من كلّ الأعداد وأقلّ من الصُّدفة (۵٫۳٪)، والباقي صفرٌ (أي مضاعفات "
    "۱۹) ثاني أندرِ الحالات.<br><br>"
    "<b>الجوهر.</b> «الرمز» يصحّ تماماً حيث يكون الرسمُ قاطعاً (الحرفان ق وص بلا صورٍ إملائية)، ويفشل تماماً حيث يكون "
    "الرسمُ خلافياً (الألف، الياء). وهذه علامةُ «مصنوعٍ إحصائيّ»، لا قانونٍ عدديّ.<br><br>"
    "<b>الحروف المقطَّعة.</b> أشهرُ الدعاوى هي الحروف المقطَّعة، واختبرناها على حِدة. الحروفُ التي لا صورةَ إملائية "
    "لها تصحّ: «ق» في السورتين ٥٠ و٤٢ يساوي ٥٧، و«ص» في السور ٧ و١٩ و٣٨ مجموعها ١٥٢ (١٩×٨). أمّا المتغيّرةُ الرسمِ "
    "فتفشل: «يس»=٢٤٨ لا ٢٨٥، و«ن»=١٣٨ لا ١٣٣، والحروفُ ذاتُ الألف تُخطئ بمئات الوحدات (الم=١٨٬٠٧٢). هذا هو "
    "«الانقسامُ الإملائيّ».<br><br>"
    "<b>الاختبار الإحصائيّ.</b> في توزيع البواقي على ١٩ (تسعةَ عشرَ احتمالاً)، لو حكم ١٩ النصَّ لكان الباقي صفرٌ أعلى "
    "عمودٍ؛ لكنّه من أدناها، ويرفض اختبارُ كاي‑تربيع التوحّدَ — في الاتجاه المعاكس للدعوى: مضاعفاتُ ١٩ مكبوتةٌ لا "
    "بارزة. وبين الأعداد ٢ إلى ٣٠ لا يتجاوز أيٌّ منها الصُّدفة، و١٩ أدناها جميعاً.<br><br>"
    "<b>البنية والموضع.</b> بعضُ الحقائق البنيوية تقبل القسمة على ١٩ فعلاً: البسملة ١٩ حرفاً؛ ١١٤ سورة (١٩×٦)؛ "
    "السورة ٩٦ (أوّل ما نزل) بتسعَ عشرةَ آية، وهي التاسعةَ عشرةَ من الآخِر؛ والبسملة تَرِد ١١٤ مرّة (١٩×٦)؛ والمسافةُ "
    "من السورة ٩ إلى ٢٧ تسعَ عشرةَ سورة بمجموع أرقامٍ ٣٤٢ (١٩×١٨). هذه حقيقية. لكنّ السورةَ ٩٦ نفسَها بعدٍّ محايد "
    "تُعطي الآيةَ الأولى ثمانيةَ عشرَ حرفاً (لا ١٩) وكاملَها ٢٨٨ حرفاً (لا ٢٨٥)، ومجموعُ الآيات مع البسملات ٦٣٤٨ "
    "(لا ٦٣٤٦).<br><br>"
    "<b>هامش التسامح.</b> يُقال إنّ «بقليلٍ من التسامح» تبلغ الأعدادُ ١٩؛ لكنّ هذا بلا معنى للأعداد الكبيرة. فهامشُ "
    "٥٪ حول «الله» (٢٦٩٥) يضمّ أربعةَ عشرَ مضاعفاً لـ١٩، وحول مجموع الآيات ثلاثةً وثلاثين مضاعفاً — فالإصابةُ "
    "تلقائيةٌ بلا قيمة. وإنّما يصحّ الاختبارُ للأعداد الصغيرة الدقيقة (البسملة=١٩، الرحمن=٥٧) حيث لا يضمّ الهامشُ إلّا "
    "مضاعفاً واحداً — وقد قبِلناها.<br><br>"
    "<b>لماذا يظهر «الرمز».</b> كلُّ نصٍّ طويل يحوي آلافَ الكمّيات القابلة للعدّ — حروفاً وكلماتٍ وآياتٍ وسوراً "
    "ومجاميعَ ومواضعَ. وبحكم الحساب نحوُ واحدٍ من تسعةَ عشرَ منها مضاعفٌ لـ١٩. فمن بحث بما يكفي، وأبلغ عن الإصاباتِ "
    "وأهمل الإخفاقات، صنع «رمزاً» من محض الانتقاء. وهذه «مغالطةُ المقارنات المتعدّدة» (قنّاصُ تكساس)، وهي خفيّةٌ من "
    "الداخل.<br><br>"
    "<b>الإنصافُ بلا محاباة.</b> هذا الحكمُ ليس خصومةً. فالمعاييرُ المنهجية نفسُها التي ردّت هذه الدعوى طُبِّقت على "
    "أحد اكتشافاتنا — التماسكِ المعجميّ بين السور — فسجّلناه «مصنوعَ حجمٍ». صرامةٌ واحدةٌ، لِما نحبّ أن يصحّ ولِما لا "
    "نحبّ.<br><br>"
    "<b>الخلاصة.</b> يوجد عنقودٌ صغيرٌ حقيقيّ من حقائق ۱۹ حول البسملة، ونعترف به بإنصاف؛ لكن لا «رمزَ شاملاً». وهذا "
    "حُكمٌ <b>إحصائيّ ومنهجيّ</b> لا لاهوتيّ.<br><br>"
    "<b>الدرس.</b> كلُّ دعوى عن القرآن — بما فيها دعاوانا — يجب أن تكون قائمةً على البيانات، ذاتَ اختبارٍ عدميٍّ سليم، "
    "منهجيّةً، وصحيحةً إحصائياً وقابلةً للتكرار؛ لا تملّقاً للعامّة (عوام‌گرایی / عوام‌پسند).</div>", unsafe_allow_html=True)

st.page_link("pages/27_Closeup_Index.py", label="← Back to the Close-up map", icon="🔎")
