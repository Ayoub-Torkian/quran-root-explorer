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
    "<div style='display:flex;justify-content:flex-end;margin:7px 0 2px'>"
    "<div style='background:linear-gradient(135deg,#138A74,#10243A);color:#fff;border-radius:10px;"
    "padding:9px 15px;font-weight:800;font-size:13.5px;box-shadow:0 3px 10px rgba(16,36,58,.25);"
    "border:1px solid rgba(255,255,255,.25)'>"
    "📄 خلاصهٔ کامل به فارسی و العربية در پایان صفحه ↓ &nbsp;·&nbsp; "
    "Full plain-language abstract — Persian &amp; Arabic — at the end ↓</div></div>", unsafe_allow_html=True)
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

# ── PERSIAN ABSTRACT ──
C.section("خلاصهٔ کامل — Persian abstract")
st.markdown(
    "<div dir='rtl' style='font-family:Vazirmatn,Tahoma,\"Segoe UI\",sans-serif;font-size:15.5px;line-height:2.0;"
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
    "<b>نتیجه.</b> خوشه‌ای کوچک و واقعی از حقایقِ ۱۹ پیرامونِ بسمله هست و آن را به‌انصاف می‌پذیریم؛ اما «رمزی فراگیر» "
    "در کار نیست. این داوری <b>آماری</b> است، نه کلامی.<br><br>"
    "<b>درس.</b> هر ادعا دربارهٔ قرآن — از جمله ادعاهای خودِ ما — باید داده‌محور، دارای آزمونِ پوچِ درست، روش‌مند، "
    "آماری‌معتبر و تکرارپذیر باشد؛ نه عوام‌گرایانه و عوام‌پسند.</div>", unsafe_allow_html=True)

# ── ARABIC ABSTRACT ──
C.section("الملخّص الكامل — Arabic abstract")
st.markdown(
    "<div dir='rtl' style='font-family:Amiri,\"Scheherazade New\",Tahoma,serif;font-size:16px;line-height:2.0;"
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
    "<b>الخلاصة.</b> يوجد عنقودٌ صغيرٌ حقيقيّ من حقائق ۱۹ حول البسملة، ونعترف به بإنصاف؛ لكن لا «رمزَ شاملاً». وهذا "
    "حُكمٌ <b>إحصائيّ</b> لا لاهوتيّ.<br><br>"
    "<b>الدرس.</b> كلُّ دعوى عن القرآن — بما فيها دعاوانا — يجب أن تكون قائمةً على البيانات، ذاتَ اختبارٍ عدميٍّ سليم، "
    "منهجيّةً، وصحيحةً إحصائياً وقابلةً للتكرار؛ لا تملّقاً للعامّة (عوام‌گرایی / عوام‌پسند).</div>", unsafe_allow_html=True)

st.page_link("pages/27_Closeup_Index.py", label="← Back to the Close-up map", icon="🔎")
