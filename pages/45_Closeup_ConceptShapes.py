"""Close-up · Shapes of a concept — the structural typology (axis · field · partition · ladder · pair).
A SYNTHESIS page: it assembles five worked concept-readings and shows that concepts do NOT share one
structure — each has its own measured geometry. All counts are rasm-WORD form-level counts on Book6,
tagged MEASURED vs INFERRED. This is the 'elephant' the per-concept studies were touches of."""
import streamlit as st
try:
    import state as S
except Exception:
    S = None
import closeup as C

st.set_page_config(page_title="Close-up · Shapes of a concept", page_icon="🔷", layout="wide")
if S:
    try: S.log_page("closeup_concept_shapes")
    except Exception: pass
    for fn in ("inject_css", "render_grouped_nav"):
        try: getattr(S, fn)()
        except Exception: pass
C.inject()

TYPE_COLORS = {"axis": "#EF9F27", "field": "#1D9E75", "partition": "#378ADD", "ladder": "#7209B7", "pair": "#4E6E92"}

# ── 1 · PROBLEM ──
C.hero("Shapes of a concept — the structural typology",
       "Do the Qur'ān's concepts all share one structure, or does each concept have its OWN shape — and can that "
       "shape be read off the text's own form (order, number, morphology, co-occurrence)?",
       "SYNTHESIS", "method", "rasm-WORD (Book6) — form-level counts", "DIVINE-DEFAULT · muṣḥaf order")
st.markdown(
    "<div style='display:flex;justify-content:flex-end;gap:9px;margin:7px 0 2px;flex-wrap:wrap'>"
    "<a href='#cs-fa' style='text-decoration:none'><div style='background:linear-gradient(135deg,#138A74,#10243A);"
    "color:#fff;border-radius:9px;padding:7px 13px;font-weight:800;font-size:13px;border:1px solid rgba(255,255,255,.3)'>"
    "📄 Persian abstract · خلاصهٔ فارسی ↓</div></a>"
    "<a href='#cs-ar' style='text-decoration:none'><div style='background:linear-gradient(135deg,#4E6E92,#10243A);"
    "color:#fff;border-radius:9px;padding:7px 13px;font-weight:800;font-size:13px;border:1px solid rgba(255,255,255,.3)'>"
    "📄 Arabic abstract · الملخّص العربي ↓</div></a></div>", unsafe_allow_html=True)
C.story(
    "Five concepts were read from their <b>whole datasets</b>, and each turned out to have a <b>different geometry</b> — "
    "not a shared template. <b>Light/darkness</b> is an <b>axis</b> (one light, many darknesses; a fixed dark→light "
    "motion). <b>Mercy</b> is a <b>field</b> (encompasses all things; graded, God at the apex). <b>Lawful/forbidden</b> "
    "is a <b>partition</b> (a small enumerated ḥarām carved from a default ḥalāl; the root itself means 'to bound'). "
    "<b>The heart</b> is a <b>ladder</b> (~27 graded states). <b>Heaven/earth</b> is a <b>frozen pair</b> (order- and "
    "number-fixed; the two poles name the whole).",
    "The mission is to understand concepts by cross-referencing their layers — and the first thing that emerges is "
    "that <b>“what shape is this?” is itself a finding</b>. Recognising structural diversity (and then integrating the "
    "parts onto one web) is the method; a single template would have hidden the concepts, not revealed them.", accent=C.SLATE)
C.kpis([
    ("axis", "light / darkness", "نور always singular (43×, plural 0×) · ظلمات always plural (23×, singular 0×) · "
     "motion مِنَ الظُّلُمَاتِ إِلَى النُّورِ 7× vs reverse 1× (marked). MEASURED.", TYPE_COLORS["axis"]),
    ("field", "mercy", "رحمة encompasses ALL things (7:156, 40:7) · graded scale, God the أرحم الراحمين (6×) · "
     "113 āyāt close on رحيم. MEASURED.", TYPE_COLORS["field"]),
    ("partition", "lawful / forbidden", "ḥurrima ʿalaykum 9× (closed lists) vs default ḥalāl · 6:145 'nothing "
     "forbidden except…' · root ح-ر-م = forbidden AND sacred. MEASURED.", TYPE_COLORS["partition"]),
    ("ladder", "the heart", "قلب·صدر·فؤاد carry ~27 graded states (sound→sealed) · co-reference-merged organ. "
     "MEASURED (states); gradation-null honest.", TYPE_COLORS["ladder"]),
    ("pair", "heaven / earth", "السماوات والأرض fixed order 147 : 2 · heavens plural/7, earth never plural · "
     "merism for the whole (وما بينهما 21×). MEASURED.", TYPE_COLORS["pair"]),
])
C.onpage(["① Problem", "② The five shapes", "③ Geometry", "④ Contrast", "⑤ Method",
          "⑥ Integration", "⑦ Caveats", "⑧ Verdict"], fa="cs-fa", ar="cs-ar")

# ── 2 · FOUNDATION ──
C.foundation(
    "In the atlas typology each concept is profiled with a <b>structural type</b>. This page is where the types are "
    "read <i>against each other</i>. The claim is deliberately modest and measurable: the <b>form</b> of a concept — "
    "the number of a noun, the order of a pair, the morphology of a root, the shape of its co-occurrence — already "
    "encodes what <b>kind of thing</b> the concept is. القرآن يفسر بعضه بعضا: the text's own form interprets its own "
    "meaning. What follows is one row per shape, each grounded in counts you can re-run on the rasm.")

# ── 3 · THE FIVE SHAPES ──
C.section("The five shapes — one row each, read from the form")
C.table(["Concept", "Type", "The form-level signature (MEASURED)", "What the shape means (INFERRED)"], tight=False, rows=[
    ["نور · light / darkness", "AXIS", "light singular 43× (plural 0×); darkness plural 23× (singular 0×); "
     "motion dark→light 7× vs 1× reverse (ṭāghūt)", "one truth, many falsehoods; guidance is a directed crossing you are <i>brought</i> across"],
    ["رحمة · mercy", "FIELD", "encompasses all things (7:156, 40:7); graded scale, God the أرحم (6×); 113 āyāt "
     "close on رحيم", "an unbounded ambient degree with no clean zero; you are <i>within</i> it and may partake"],
    ["حرام · lawful / forbidden", "PARTITION", "ḥurrima 9× closed lists vs default ḥalāl; 6:145 'nothing forbidden "
     "except'; root = forbidden AND sacred", "a small marked exception fenced out of a default ground; God alone draws the line"],
    ["قلب · the heart", "LADDER", "قلب·صدر·فؤاد (co-ref) carry ~27 graded states, sound سليم → sealed مطبوع", "a single "
     "faculty read by <i>which graded state</i> it is in — a dimmer of many discrete rungs"],
    ["سماء · heaven / earth", "FROZEN PAIR", "order fixed 147 : 2; heavens plural/7, earth never plural; merism "
     "(وما بينهما 21×)", "the meaning is the invariant <i>pairing</i> — two poles named to mean the whole (a merism)"],
])

# ── 4 · GEOMETRY ICONS ──
C.section("The geometry at a glance — five shapes, five pictures")
_ax, _fi, _pa, _la, _pr = (TYPE_COLORS[k] for k in ("axis","field","partition","ladder","pair"))
_svg = f'''<svg viewBox="0 0 1000 210" width="100%" style="max-width:1000px;font-family:system-ui,sans-serif">
<!-- AXIS -->
<text x="100" y="24" text-anchor="middle" font-size="14" font-weight="800" fill="{_ax}">AXIS</text>
<circle cx="55" cy="110" r="9" fill="#10243A"/><circle cx="66" cy="96" r="9" fill="#10243A"/><circle cx="44" cy="96" r="9" fill="#10243A"/>
<line x1="80" y1="105" x2="140" y2="105" stroke="{_ax}" stroke-width="3" marker-end="url(#a)"/>
<circle cx="158" cy="105" r="12" fill="#EFC047" stroke="{_ax}" stroke-width="2"/>
<text x="55" y="150" text-anchor="middle" font-size="12" fill="#10243A">darknesses</text>
<text x="158" y="150" text-anchor="middle" font-size="12" fill="#10243A">light</text>
<defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="{_ax}"/></marker></defs>
<!-- FIELD -->
<text x="300" y="24" text-anchor="middle" font-size="14" font-weight="800" fill="{_fi}">FIELD</text>
<circle cx="300" cy="108" r="60" fill="{_fi}" opacity="0.10"/><circle cx="300" cy="108" r="42" fill="{_fi}" opacity="0.16"/>
<circle cx="300" cy="108" r="24" fill="{_fi}" opacity="0.28"/><circle cx="300" cy="108" r="9" fill="{_fi}"/>
<text x="300" y="190" text-anchor="middle" font-size="12" fill="#10243A">encompasses all · graded</text>
<!-- PARTITION -->
<text x="500" y="24" text-anchor="middle" font-size="14" font-weight="800" fill="{_pa}">PARTITION</text>
<rect x="440" y="60" width="120" height="96" rx="6" fill="{_pa}" opacity="0.10" stroke="{_pa}" stroke-width="1.5"/>
<rect x="512" y="112" width="44" height="40" rx="4" fill="{_pa}" opacity="0.45" stroke="{_pa}" stroke-width="2"/>
<text x="474" y="96" text-anchor="middle" font-size="12" fill="#10243A">ḥalāl</text>
<text x="534" y="137" text-anchor="middle" font-size="11" fill="#fff" font-weight="700">ḥarām</text>
<text x="500" y="185" text-anchor="middle" font-size="12" fill="#10243A">default + marked exception</text>
<!-- LADDER -->
<text x="700" y="24" text-anchor="middle" font-size="14" font-weight="800" fill="{_la}">LADDER</text>
<line x1="700" y1="55" x2="700" y2="160" stroke="{_la}" stroke-width="2"/>
<line x1="672" y1="68" x2="728" y2="68" stroke="{_la}" stroke-width="4"/><line x1="672" y1="90" x2="728" y2="90" stroke="{_la}" stroke-width="4"/>
<line x1="672" y1="112" x2="728" y2="112" stroke="{_la}" stroke-width="4"/><line x1="672" y1="134" x2="728" y2="134" stroke="{_la}" stroke-width="4"/>
<text x="700" y="185" text-anchor="middle" font-size="12" fill="#10243A">~27 graded states</text>
<!-- PAIR -->
<text x="900" y="24" text-anchor="middle" font-size="14" font-weight="800" fill="{_pr}">FROZEN PAIR</text>
<circle cx="865" cy="108" r="13" fill="{_pr}"/><circle cx="935" cy="108" r="10" fill="{_pr}"/>
<path d="M845,70 q-10,38 0,76" fill="none" stroke="{_pr}" stroke-width="2.5"/><path d="M955,70 q10,38 0,76" fill="none" stroke="{_pr}" stroke-width="2.5"/>
<text x="865" y="150" text-anchor="middle" font-size="12" fill="#10243A">heaven</text><text x="935" y="150" text-anchor="middle" font-size="12" fill="#10243A">earth</text>
<text x="900" y="185" text-anchor="middle" font-size="12" fill="#10243A">the pair = the whole</text>
</svg>'''
st.markdown(f"<div class='cu-card' style='padding:10px 14px'>{_svg}</div>", unsafe_allow_html=True)
C.note("Each picture is the concept's <b>measured</b> shape, not decoration: the axis has a direction (§KPIs), the "
       "field has no boundary, the partition is a small box inside a big one, the ladder has discrete rungs, the pair "
       "is bracketed. The map on the Concept Atlas can be coloured by these same five types.")

# ── 5 · CONTRAST ──
C.section("The contrast — why one template would have failed")
C.table(["", "AXIS", "FIELD", "PARTITION", "LADDER", "PAIR"], tight=True, rows=[
    ["boundary", "clean switch", "none (all)", "a drawn line", "rung thresholds", "n/a"],
    ["internal shape", "binary + direction", "continuous degree", "default + exception", "discrete states", "fixed 2-pole"],
    ["symmetry", "asym. (1 vs many)", "graded, God apex", "asym. (small ḥarām)", "ordered rungs", "order-fixed 147:2"],
    ["the person", "brought across", "within, partakes", "inside default", "in some state", "invokes both"],
    ["meaning lives in", "the direction", "the degree", "the line", "which state", "the pairing"],
])
C.para("Read down any column and the shapes refuse to collapse into one another. A <b>field</b> has no line to draw; "
       "a <b>partition</b> has no degree to grade; a <b>pair</b> is not traversed. This is the mission's structural-"
       "diversity mandate made concrete: <b>concepts need not behave the same or share one structure</b> — and "
       "'no clean zero' (mercy) or 'no middle' (light/dark) is a <i>finding</i> about the type, not a failure.")

# ── 6 · METHOD ──
C.section("Method — how each shape was read")
C.callout("The same four-step apparatus for every concept",
          "① <b>Sense-resolve first</b> — split the root by surface form (نور=light≠نار=fire; ظلم=darkness≠injustice; "
          "حرم=forbidden/sacred≠deprived; سمو=heaven≠name) so the reading is of one sense, from every occurrence. "
          "② <b>Read the form</b> — count number, order, morphology, clause-position, co-occurrence on the rasm. "
          "③ <b>Cross-reference layers</b> — form↔meaning, grammar↔semantics, structure↔function. "
          "④ <b>Name the type</b> and tag every claim MEASURED (a count) vs INFERRED (a reading).", accent=C.SLATE)

# ── 7 · INTEGRATION ──
C.section("Integration — how the shapes fold back onto the web (the elephant)")
C.para("These are not five loose cards. Each concept is a <b>profile</b> in the atlas registry carrying its "
       "structural type and a tagged three-layer reading; the profile <b>surfaces in the Concept Atlas</b> when you "
       "drill Family → concept. The Atlas map can be <b>coloured by structural type</b>, so the typology is visible "
       "across the whole web, and this page is the one place they are read side by side. The path is continuous: "
       "<b>whole</b> (map, coloured by shape) → <b>family</b> (organ) → <b>concept</b> (profile + type) → "
       "<b>facet</b> (senses) → here (the shapes named). Each part-study hangs on the graph; nothing stays a loose card.")

# ── 8 · CAVEATS ──
C.section("Caveats & confounds")
C.para("<b>Five is a sample, not a census.</b> Other types certainly exist (hub — God; bridge — high-betweenness "
       "roots; cycle) and some concepts may be mixed or shift type as senses are re-resolved. <b>Naming is "
       "interpretive.</b> The counts are measured; calling a shape an 'axis' or a 'field' is a reading, and a "
       "different reader may re-cut the boundaries. <b>Co-occurrence is not co-reference</b>, and the ladder's "
       "gradation ordering is an unvalidated null. The typology is a <b>navigation lens</b>, not a claim of "
       "exhaustive taxonomy.")

# ── 9 · VERDICT ──
C.section("Verdict")
C.verdict("SYNTHESIS",
          "Five concepts, five genuinely different measured geometries — axis, field, partition, ladder, frozen pair. "
          "The form-level signatures (number, order, morphology, position) are MEASURED and re-runnable; the shape-"
          "names and their meanings are INFERRED and tagged. The value is the lens: 'what kind of thing is this "
          "concept?' is a first-class question, and the answer is read from the text's own form.",
          "~95% on the form-level signatures (counting); ~75% on the shape-names/readings (interpretive).",
          "a concept that resists all five types, or a re-resolution that collapses two shapes into one",
          "raise as more concepts are typed and the coloured map fills in")

# ── 10 · REFLECTION / SUMMARY / LESSONS ──
C.section("Reflection")
C.para("The light study almost <i>became</i> the template — a tidy binary. Mercy broke it (no boundary, no zero), and "
       "insisting on a partition there would have been the classic error: importing one concept's shape onto another. "
       "Holding the shapes apart, and letting the form dictate the type, is what kept each reading honest.")
C.section("Summary")
C.para("<b>Measured:</b> the five form-level signatures. <b>Inferred:</b> the shape-names and their meanings, plus the "
       "unifying claim that form encodes type. <b>Failed / open:</b> the heart's gradation ordering (null); whether "
       "the partition has a graded middle; how many types there are in all.")
C.section("Lessons — for every concept reading")
C.para("① Sense-resolve before you count. ② Let the <b>form</b> speak first (number, order, morphology, position). "
       "③ Don't reuse the last concept's shape — ask the type afresh. ④ Tag MEASURED vs INFERRED at every step. "
       "⑤ Assemble onto the web; never ship a loose card.")

# ── Persian abstract ──
C.section("خلاصهٔ کامل — Persian abstract")
st.markdown('''<div dir="rtl" id="cs-fa" style="font-family:Vazirmatn,Tahoma,'Segoe UI',sans-serif;font-size:15px;line-height:1.95;color:#10243A;text-align:right;background:#F6F9FC;border-right:5px solid #138A74;border-radius:11px;padding:18px 22px">
<b>شکل‌های یک مفهوم — گونه‌شناسی ساختاری.</b> پنج مفهوم قرآنی از کلّ داده‌هایشان خوانده شد و هر یک <b>هندسه‌ای متفاوت</b> نشان داد، نه یک قالب مشترک:
<b>نور/ظلمات</b> یک <b>محور</b> است (نور همیشه مفرد، ۴۳ بار؛ ظلمات همیشه جمع، ۲۳ بار؛ حرکت «مِنَ الظُّلُمَاتِ إِلَى النُّورِ» ۷ بار و تنها ۱ بار وارونه که کارِ طاغوت است).
<b>رحمت</b> یک <b>میدان</b> است (وَسِعَتْ کُلَّ شَیْءٍ؛ مقیاسِ مدرّج با خدا در قلّه، أرحم الراحمین ۶ بار؛ ۱۱۳ آیه با «رحیم» پایان می‌یابد).
<b>حلال/حرام</b> یک <b>افراز</b> است (فهرست‌های بستهٔ «حُرِّمَ عَلَیْکُم» در برابر حلالِ پیش‌فرض؛ ۶:۱۴۵ «چیزی حرام نمی‌یابم جز…»؛ ریشهٔ ح‑ر‑م هم «حرام» و هم «مقدّس/مرزکشیده»).
<b>قلب</b> یک <b>نردبان</b> است (قلب·صدر·فؤاد حاملِ ~۲۷ حالتِ مدرّج).
<b>آسمان/زمین</b> یک <b>جفتِ منجمد</b> است (ترتیب ثابت ۱۴۷ به ۲؛ آسمان‌ها جمع/هفت‌گانه، زمین هرگز جمع نمی‌شود؛ «وَمَا بَیْنَهُمَا» ۲۱ بار — نامیدنِ دو قطب یعنی نامیدنِ کلّ).
<b>روش:</b> نخست تفکیکِ معنا، سپس خواندنِ فرم (عدد، ترتیب، صرف، جایگاه)، سپس ارجاع متقابلِ لایه‌ها، سپس نام‌گذاریِ گونه؛ هر ادّعا با برچسبِ «سنجیده» یا «استنباط». همهٔ این پروفایل‌ها به اطلسِ مفاهیم بازمی‌گردند و نقشه می‌تواند برحسبِ گونهٔ ساختاری رنگ‌آمیزی شود. اطمینان: ~۹۵٪ برای امضاهای فرمی، ~۷۵٪ برای نام‌ها و خوانش‌ها.
</div>''', unsafe_allow_html=True)

# ── Arabic abstract ──
C.section("الملخّص الكامل — Arabic abstract")
st.markdown('''<div dir="rtl" id="cs-ar" style="font-family:Amiri,'Scheherazade New',Tahoma,serif;font-size:15.5px;line-height:2.0;color:#10243A;text-align:right;background:#F6F9FC;border-right:5px solid #4E6E92;border-radius:11px;padding:18px 22px">
<b>أشكال المفهوم — تصنيفٌ بنيويّ.</b> قُرِئت خمسة مفاهيم قرآنية من كامل ورودها، فتبيَّن أنّ لكلٍّ منها <b>هندسةً مختلفة</b> لا قالبًا واحدًا:
<b>النور/الظلمات</b> <b>محورٌ</b> (النور مفردٌ دائمًا ٤٣ مرّة، والظلمات جمعٌ دائمًا ٢٣ مرّة؛ الحركة «مِنَ الظُّلُمَاتِ إِلَى النُّورِ» ٧ مرّات، والعكس مرّةً واحدةً موسومةً بأنّها فعل الطاغوت).
<b>الرحمة</b> <b>حقلٌ</b> (وَسِعَتْ كُلَّ شَيْءٍ؛ سُلَّمٌ متدرّجٌ واللهُ في قمّته «أرحم الراحمين» ٦ مرّات؛ ١١٣ آيةً تُختَم بـ«رحيم»).
<b>الحلال/الحرام</b> <b>قِسمةٌ</b> (قوائمُ مغلقةٌ «حُرِّمَ عَلَيْكُم» مقابل الحلال الأصل؛ ٦:١٤٥ «لا أجد… محرَّمًا إلّا…»؛ والجذر ح‑ر‑م يعني المحرَّمَ والمقدَّسَ معًا — أي وضْعَ الحدّ).
<b>القلب</b> <b>سُلَّمٌ</b> (القلب·الصدر·الفؤاد تحمل ~٢٧ حالةً متدرّجة).
<b>السماوات/الأرض</b> <b>ثنائيٌّ جامدٌ</b> (ترتيبٌ ثابتٌ ١٤٧ إلى ٢؛ السماوات جمعٌ/سبعٌ والأرضُ لا تُجمَع قطّ؛ «وَمَا بَيْنَهُمَا» ٢١ مرّة — فتسميةُ القطبين تسميةٌ للكلّ).
<b>المنهج:</b> فضُّ المعنى أوّلًا، ثمّ قراءةُ الصورة (العددُ والترتيبُ والصرفُ والموضع)، ثمّ المقابلةُ بين الطبقات، ثمّ تسميةُ النوع؛ مع وسمِ كلِّ دعوى بـ«مقيس» أو «مستنبَط». وكلُّ هذه الملامح تعود إلى أطلس المفاهيم، وللخريطة أن تُلوَّن بحسب النوع البنيويّ. الثقة: ~٩٥٪ للملامح الصُّوَريّة، ~٧٥٪ للأسماء والقراءات.
</div>''', unsafe_allow_html=True)
