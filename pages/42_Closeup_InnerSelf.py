"""Close-up · Anatomy of the inner self — qalb · nafs · ṣadr · fuʾād, reviewed (CANDIDATE).
The MEASURED core (co-occurrence dissociations + Fisher tests + the زاد amplifier, all on Book6 rasm) is held
sharply apart from the INFERRED synthesis (the dynamical / "processor" reading). The qalb-state gradation NULL
is reported honestly. Arabic concept-labels carry no definite article (ال) — bare terms per the locked convention."""
import os
import streamlit as st

try:
    import state as S
except Exception:
    S = None
import closeup as C

st.set_page_config(page_title="Close-up · Anatomy of the inner self", page_icon="🧠", layout="wide")
if S:
    try:
        S.log_page("closeup_inner_self")
    except Exception:
        pass
    for fn in ("inject_css", "render_grouped_nav"):
        try:
            getattr(S, fn)()
        except Exception:
            pass
C.inject()

# ── 1 · PROBLEM ──
C.hero("Anatomy of the inner self — qalb · nafs · ṣadr · fuʾād",
       "Does the Qur'ān name the inner faculties as ONE undifferentiated 'heart', or as distinct parts with "
       "distinct jobs — and do they form a measurable web rather than a list?",
       "CANDIDATE", 68, "rasm-WORD (Book6, co-occurrence on roots)", "DIVINE-DEFAULT · muṣḥaf order")
st.markdown(
    "<div style='display:flex;justify-content:flex-end;gap:9px;margin:7px 0 2px;flex-wrap:wrap'>"
    "<a href='#is-fa' style='text-decoration:none'>"
    "<div style='background:linear-gradient(135deg,#138A74,#10243A);color:#fff;border-radius:9px;padding:7px 13px;"
    "font-weight:800;font-size:13px;box-shadow:0 2px 8px rgba(16,36,58,.25);border:1px solid rgba(255,255,255,.3)'>"
    "📄 Persian abstract · خلاصهٔ فارسی ↓</div></a>"
    "<a href='#is-ar' style='text-decoration:none'>"
    "<div style='background:linear-gradient(135deg,#4E6E92,#10243A);color:#fff;border-radius:9px;padding:7px 13px;"
    "font-weight:800;font-size:13px;box-shadow:0 2px 8px rgba(16,36,58,.25);border:1px solid rgba(255,255,255,.3)'>"
    "📄 Arabic abstract · الملخّص العربي ↓</div></a></div>", unsafe_allow_html=True)
C.story(
    "The Qur'ān's inner-self vocabulary is <b>not one word repeated</b>. قلب (heart), نفس (self), صدر (breast) "
    "and فؤاد (sensing-core) occur in <b>measurably different company</b>: فؤاد binds to sight and hearing; قلب "
    "carries reasoning, turning and sealing; نفس is the one that <i>earns</i>, is <i>judged</i>, and is purified. "
    "On top of these parts sits one repeated dynamical motif — زاد, the amplifier: whatever the inner state is, "
    "God <i>increases it</i> (faith↑faith, disease↑disease). The faculties form a <b>web</b>, not a glossary.",
    "If the parts truly dissociate in the text's own usage, then the inner self is a designed, articulated system "
    "— the same WEB lens that orders the rest of the corpus. The measured part is solid; the dynamical 'processor' "
    "reading on top of it is an interpretation, and is tagged as such throughout. مقبول for the reader, مطلوب for "
    "the specialist.", accent=C.TEAL)
C.kpis([
    ("OR 8.8", "فؤاد ↔ sight/hearing", "Fisher exact: فؤاد co-occurs with sight/hearing roots far above chance "
     "(odds-ratio 8.8, p = 5.5e-4) — فؤاد is the perceptual sensor, not a generic 'heart'. MEASURED on Book6.", C.TEAL),
    ("155 : 4", "قلب-turn vs نفس", "The turning/overturning sense (root قلب) attaches to the heart 155× but to "
     "نفس only 4× — the faculties take different verbs. MEASURED.", C.TEAL),
    ("11 : 0", "sealing طبع · قلب vs نفس", "Sealing (طبع/ختم) is predicated of the heart 11× and of نفس 0× — "
     "closure is a heart-state, never a self-state. MEASURED.", C.TEAL),
    ("OR 16.2", "زاد ↔ disease", "The amplifier: where heart-disease مرض is present, زاد (increase) co-occurs at "
     "odds-ratio 16.2 (p = 1.3e-3); for faith OR 2.6 (p = 3.4e-3). Same operator, both poles. MEASURED.", C.GOLD),
    ("42", "علم ∩ عمل", "Knowledge-roots and deed-roots co-occur in 42 verses — the cognition↔action core loop is "
     "a real edge, not a metaphor. MEASURED.", C.TEAL),
    ("z = −7.31", "qalb-state gradation", "A context-similarity network of the heart's state-words did NOT separate "
     "'closed' from 'open' (modularity z = −7.31; they intermix). Reported as a NULL — the gradation is not "
     "structurally validated. MEASURED.", C.CORAL),
    ("68", "grade", "CANDIDATE — the part-dissociations and the amplifier are measured and strong; the integrated "
     "dynamical model is an INFERRED synthesis on top of them.", C.GOLD),
])
C.onpage(["① Problem", "② Hypothesis", "③ Method",
          "<b>④ Results Part 1</b> the parts dissociate (paired tables + 3 charts)",
          "<b>⑤ Results Part 2</b> the core loop & the amplifier (2 charts)",
          "<b>⑥ The network</b> (interactive)", "⑦ Gating", "⑧ Interpretation",
          "⑨ The gradation NULL", "⑩ Caveats", "⑪ Verdict", "⑫ Tie to al-Kawthar"],
         fa="is-fa", ar="is-ar",
         closers="<b>Reflection · Summary · Lessons · Takeaway</b>")

# ── 2 · HYPOTHESIS ──
C.section("Hypothesis")
C.callout("If the inner self is an articulated system, three things must hold in the text's own usage",
          "The naive reading treats قلب · نفس · صدر · فؤاد as near-synonyms for 'heart/soul'. The structural claim "
          "is stronger and testable.<br>"
          "&nbsp;&nbsp;<b>(1) Dissociation.</b> The four parts must take <i>different</i> predicates — if فؤاد binds "
          "perception, قلب binds cognition/closure, and نفس binds moral earning, they are distinct organs, not "
          "synonyms.<br>"
          "&nbsp;&nbsp;<b>(2) A coupling loop.</b> Cognition (علم) and action (عمل) must be <i>linked</i> in both "
          "directions — sound knowledge → sound deed, and (the dark mirror) corrupt deed → darkened knowledge.<br>"
          "&nbsp;&nbsp;<b>(3) A dynamical operator.</b> There must be a measurable mechanism that makes the system "
          "<i>run away</i> toward either pole — the repeated زاد (God increases what is there).<br>"
          "Predictions 1–3 are MEASURABLE on co-occurrence. What they do NOT license — a single ranked 'ladder' of "
          "heart-states — is prediction (4), and it is the one that FAILS (§⑨).", accent=C.SLATE)

# ── 3 · METHOD ──
C.section("Method & instruments")
C.callout("The apparatus — substrate, arrangement, and the tests",
          "<b>Substrate.</b> rasm-WORD (Book6): every occurrence of each faculty-root and its verse-neighbours, on "
          "the consonantal skeleton; diacritics demoted. <b>Arrangement.</b> DIVINE-DEFAULT (canonical muṣḥaf "
          "order) — we read meaning from the WHOLE dataset of each root, never one verse.<br>"
          "&nbsp;&nbsp;<b>Tests.</b> (a) <i>Dissociation</i> — for each faculty, which predicate-roots (turn, seal, "
          "purify, perceive) attach, and at what rate vs the other faculties. (b) <i>Fisher exact</i> — is the "
          "فؤاد↔perception / زاد↔state association above chance? (c) <i>Co-occurrence loop</i> — do علم and عمل "
          "share verses, and in both valences? (d) <i>Gradation test</i> — can a context-similarity network of the "
          "heart's state-words separate 'closed' from 'open' clusters? (the honest NULL).<br>"
          "&nbsp;&nbsp;<b>MEASURED vs INFERRED.</b> Every count and odds-ratio below is MEASURED on Book6. The "
          "reading of the whole as a coupled 'processor + agent' with a feedback amplifier is an INFERRED synthesis "
          "— labelled wherever it appears, and never given a measured tone. القرآن يفسر بعضه بعضا is the method: "
          "the state-word interprets the faculty's condition.", accent=C.SLATE)

# ── 4 · RESULTS PART 1 — THE PARTS DISSOCIATE ──
C.section("Results · Part 1 — the four parts dissociate (the heart is not one word)")
C.note("MEASURED. Each faculty takes a different predicate-profile. Read the two tables together: فؤاد is bound to "
       "the senses; نفس is the moral agent that earns and is purified; قلب is the processor that reasons, turns and "
       "can be sealed; صدر is the chamber the whisper lands in. Different jobs, different verbs.")
L, R = st.columns(2, gap="medium")
with L:
    C.table(["Faculty", "Binds to (MEASURED)", "Signature"], [
        ["فؤاد", "sight + hearing (Fisher OR 8.8)", "sensor"],
        ["قلب", "reason عقل · understand فقه · turn · seal", "processor"],
        ["نفس", "earn كسب · purify زكو · judged · أمّارة→لوّامة→مطمئنة", "agent"],
        ["صدر", "constrict ضيق ↔ expand شرح · whisper lands", "chamber"],
    ])
with R:
    C.table(["Predicate", "قلب", "نفس", "Reading"], [
        ["turn / overturn (قلب)", "155", "4", "turning is a heart-event"],
        ["seal (طبع / ختم)", "11", "0", "closure is heart-only"],
        ["purify (زكو)", "1", "7", "purification is self-only"],
        ["whisper lands (وسوسة)", "via صدر", "50:16", "chamber, then self"],
    ])

C.section("Statistical core — three measured views of the dissociation")

C.note("① The perceptual binding — how strongly each faculty co-occurs with the sense-roots (sight بصر, hearing "
       "سمع). فؤاد towers over the others: it is the Qur'ān's word for the perceiving core, answerable for what it "
       "took in (17:36). [MEASURED — Fisher OR 8.8, p = 5.5e-4 for فؤاد.]")
C.vbars([("فؤاد", 8.8, C.TEAL, "Fisher odds-ratio 8.8 with sight/hearing roots — the sensor"),
         ("قلب", 1.6, C.SLATE, "weakly bound — the heart reasons more than it perceives"),
         ("نفس", 0.7, C.SLATE, "below chance — the self is not a perceptual organ"),
         ("صدر", 1.1, C.SLATE, "near chance — chamber, not sensor")],
        ymax=10, fmt="{:.1f}")

C.note("② The verb dissociation — sealing/closure (طبع · ختم · قسو) attaches to the HEART, purification (زكو · "
       "طهر) to the SELF. The two faculties do not share their defining verbs: the heart is the thing that is "
       "sealed; the self is the thing that is purified. [MEASURED counts on Book6.]")
C.vbars([("seal · قلب", 11, C.TEAL, "طبع/ختم predicated of the heart 11×"),
         ("seal · نفس", 0, C.CORAL, "never of the self"),
         ("purify · نفس", 7, C.TEAL, "زكو predicated of the self 7×"),
         ("purify · قلب", 1, C.SLATE, "rarely of the heart")],
        ymax=13, fmt="{:.0f}")

C.note("③ The whisper's address — who whispers, and where it lands. The external Whisperer (وسواس / شيطان) "
       "whispers into the breast (صدر, 114:5); but the self too can whisper from within (نفس, 50:16), and the "
       "self's 'fair-seeming' enticement (تسويل) is overwhelmingly internal (3/4 نفس, 12:18·47:25). The injection "
       "is external; the relay can be internal. [MEASURED occurrence split.]")
C.vbars([("waswasa — شيطان (external)", 4, C.SLATE, "4 of 5 whisper-occurrences are Satan into the breast"),
         ("waswasa — نفس (internal)", 1, C.GOLD, "50:16 — the self too whispers"),
         ("taswīl — نفس (internal)", 3, C.TEAL, "3 of 4 'fair-seeming' are the self (12:18, etc.)"),
         ("taswīl — شيطان (external)", 1, C.SLATE, "47:25 — Satan also entices")],
        ymax=6, fmt="{:.0f}")

# ── 5 · RESULTS PART 2 — THE CORE LOOP & THE AMPLIFIER ──
C.section("Results · Part 2 — the cognition↔action loop and the زاد amplifier")
C.note("④ The core loop is bidirectional and runs in BOTH valences. Knowledge-roots (علم) and deed-roots (عمل) "
       "co-occur in 42 verses. The good direction is stated two ways — «الذين آمنوا وعملوا الصالحات» (faith→deed, "
       "50×) and «من عمل صالحاً وهو مؤمن» (deed-while-believing, 5×) — i.e. faith and deed reinforce each other. "
       "The dark mirror: evil deed → RUST on the heart (83:14), corrupting cognition. [MEASURED.]")
C.vbars([("علم ∩ عمل (co-occur verses)", 42, C.TEAL, "knowledge and deed share 42 verses — the coupling edge"),
         ("«آمنوا وعملوا الصالحات»", 50, C.TEAL, "faith→deed, stated 50×"),
         ("«وهو مؤمن» (deed-while-believing)", 5, C.SLATE, "deed→faith direction, 5× (16:97 etc.)"),
         ("evil-deed → rust (ران) on heart", 1, C.CORAL, "83:14 — the dark mirror, deed corrupts cognition")],
        ymax=55, fmt="{:.0f}")

C.note("⑤ The amplifier — ONE operator, both poles. زاد (increase) is the runaway mechanism: wherever a state is "
       "present, it is increased. Validated against four states by Fisher exact — faith (OR 2.6), guidance (OR "
       "3.5), disbelief (OR 3.2), and most sharply disease of the heart (OR 16.2). This is why the system is "
       "<b>bistable</b>: small initial states self-reinforce toward either kawthar or abtar. [MEASURED odds-ratios.]")
C.vbars([("زاد ↔ disease مرض", 16.2, C.CORAL, "OR 16.2, p = 1.3e-3 — disease amplifies fastest (2:10, 9:125)"),
         ("زاد ↔ guidance هدى", 3.5, C.TEAL, "OR 3.5 — the guided are increased in guidance (47:17)"),
         ("زاد ↔ disbelief كفر", 3.2, C.SLATE, "OR 3.2 — disbelief compounds"),
         ("زاد ↔ faith إيمان", 2.6, C.TEAL, "OR 2.6, p = 3.4e-3 — faith increases faith (8:2, 9:124)")],
        ymax=18, fmt="{:.1f}")

# ── 6 · THE NETWORK ──
C.section("The inner-self network — one reality, two co-present orientations")
C.story(
    "All of the above as a single web: نفس (agent) and قلب (processor) coupled by the علم↔عمل loop; صدر the "
    "chamber and فؤاد the sensor feeding in; up-drivers (ذكر · تقوى · إيمان · هدى) versus down-drivers (ظنّ · هوى "
    "· لهو · وسواس · تسویل · مرض · طبع); زاد amplifying either pole. دنیا (the near) and آخرة (the lasting/real) "
    "are TWO CO-PRESENT orientations — by what it knows and does the self becomes دنیوی or اخروی; the غطاء veil "
    "is over perception (present in life, lifted when sight sharpens). Outcome — کوثر (joined to the lasting → "
    "crosses) or أبتر (clinging to the near → cut off). Hover any node or edge for its anchor; use the chart "
    "toolbar (zoom · pan · autoscale/home · fullscreen) like every other chart.",
    "NODES and EDGES are drawn from the MEASURED dissociations and co-occurrences (green = toward the lasting / "
    "openness · red = toward the near / severance · gold = the زاد feedback · grey = structure). The layout and "
    "the orientation reading are INFERRED from those measured links, not a separate measurement.", accent=C.TEAL)
C.callout("دنیا and آخرة — two orientations, not two times (correcting a near-universal misreading)",
          "Almost everyone reads <b>دنیا</b> as ‘this world, now’ and <b>آخرة</b> as ‘the next world, after death’, "
          "with death (or the barzakh) as the wall between them. The text points elsewhere. <b>دنیا</b> is from the "
          "root دنو, ‘to draw near’ — الحیاة الدنیا is ‘the <i>nearer</i> life’, the immediate, which 29:64 calls "
          "لهو ولعب (distraction and play). <b>آخرة</b> (from أخر, ‘the last/other’) 29:64 calls الحیوان — the real "
          "life — in the <i>present</i> tense («لو کانوا یعلمون», if only they knew). The two are weighed as a "
          "<b>present choice</b> in 57 verses («منکم من یرید الدنیا ومنکم من یرید الآخرة», 3:152). The <b>غطاء</b> "
          "(veil) is over perception and present in life (18:101), lifting when sight sharpens (50:22). And "
          "<b>برزخ</b> is a partition — 2 of its 3 uses are the barrier between the two seas, one is the dead until "
          "resurrection — <b>not</b> the wall between worlds. So <b>kawthar</b> = اخروی (joined to the lasting → "
          "crosses); <b>abtar</b> = دنیوی (clinging to the near → cut off). The choice is made now, in the heart "
          "and the deed; death only lifts the veil on the life the self was already living.", accent=C.GOLD)
# -- 6c THE MEASURED GRAPH (corpus co-occurrence) + GRAPH METRICS --
import json as _json, plotly.graph_objects as _g2
_gp = os.path.join(os.path.dirname(__file__), "..", "assets", "inner_self_graph_metrics.json")
try:
    _GM = _json.load(open(_gp, encoding="utf-8"))
except Exception:
    _GM = None
if _GM:
    C.section("The measured graph — corpus co-occurrence, with metrics")
    C.note("This is the primary network — the directed reading follows below as a labelled schematic. The SAME nodes "
           "as a <b>real graph built from the corpus</b>: an edge where two roots co-occur in a verse, weighted by "
           "<b>PPMI</b> (frequency-controlled). The layout is <b>clustered by community</b> (each group a blob); "
           "intra-community edges are faint, the strongest <b>bridges</b> between communities are gold; node size = "
           "association strength. Node selection and colours are interpretive; edges, weights and metrics are MEASURED.")
    _S = _GM["stats"]
    C.kpis([
        (str(_S["density"]), "density", "Edge density of the 25-node PPMI graph.", C.TEAL),
        (str(_S["avg_degree"]), "avg degree", "Mean PPMI links per node.", C.TEAL),
        (str(_S["cycles"]), "cycles", "Cycle-basis size — a web, not a tree.", C.TEAL),
        ("+%s" % _S["modularity_z"], "modularity z", "Community structure vs a degree-preserving null (z>2 = real).", C.GOLD),
        (str(_S["n_communities"]), "communities", "Greedy-modularity communities (PPMI).", C.SLATE),
        (str(_S["transitivity"]), "transitivity", "Global clustering — fraction of closed triangles.", C.TEAL),
        (str(_S["assortativity"]), "assortativity", "Degree correlation; negative = hubs link to low-degree nodes.", C.SLATE),
        ("قلب", "top hub", "Strongest PPMI association (strength %.1f) — the heart, frequency controlled." % _GM["strength"]["قلب"], C.TEAL),
        ("ذکر", "top bridge", "Highest betweenness (%.3f) — remembrance connects the communities." % _GM["betweenness"]["ذکر"], C.GOLD),
    ])
    _ROLEC = {"self": "#1D3557", "cog": "#378ADD", "act": "#0F6E56", "up": "#1D9E75", "down": "#E63946",
              "amp": "#EF9F27", "bound": "#7A5AA6", "dom": "#94A3B8", "out_g": "#0F6E56", "out_r": "#C1121F", "root": "#B5651D"}
    _pos = _GM["pos"]; _roles = _GM["roles"]; _strg = _GM["strength"]; _btw = _GM["betweenness"]; _deg = _GM["deg"]; _comms = _GM["communities"]
    _rof = _GM["region_of"]
    _cross = sorted([(a, b, w) for a, b, w in _GM["edges"] if _rof.get(a) != _rof.get(b)], key=lambda e: -e[2])[:12]
    _crs = set((a, b) for a, b, _ in _cross)
    _ix = []; _iy = []; _gx = []; _gy = []
    for a, b, w in _GM["edges"]:
        sx = [_pos[a][0], _pos[b][0], None]; sy = [_pos[a][1], _pos[b][1], None]
        if _rof.get(a) == _rof.get(b): _ix += sx; _iy += sy
        elif (a, b) in _crs: _gx += sx; _gy += sy
    _eti = _g2.Scatter(x=_ix, y=_iy, mode="lines", line=dict(color="#D7E0EA", width=1), hoverinfo="none", showlegend=False)
    _etg = _g2.Scatter(x=_gx, y=_gy, mode="lines", line=dict(color="#EF9F27", width=2.4), hoverinfo="none", showlegend=False)
    _nlab = list(_pos); _nx = [_pos[n][0] for n in _nlab]; _ny = [_pos[n][1] for n in _nlab]
    _ncol = [_ROLEC.get(_roles[n], "#888") for n in _nlab]; _nsz = [12 + 2.2 * (_strg[n] ** 0.5) for n in _nlab]
    _nhov = ["<b>%s</b><br>PPMI strength %.1f · degree %d<br>betweenness %.3f · closeness %.3f · PageRank %.3f" % (n, _strg[n], _deg[n], _btw[n], _GM["closeness"][n], _GM["pagerank"][n]) for n in _nlab]
    _nt = _g2.Scatter(x=_nx, y=_ny, mode="markers+text", marker=dict(size=_nsz, color=_ncol, line=dict(width=1.5, color="#fff")),
                      text=_nlab, textposition="top center", textfont=dict(size=11, color="#10243A"), hovertext=_nhov, hoverinfo="text", showlegend=False)
    _fg = _g2.Figure([_eti, _etg, _nt])
    _RTINT = {"apparatus": ("#EAF2FB", "#CFE0F2"), "drivers": ("#FBF1E6", "#EAD3B6"), "orientation": ("#EFF6F2", "#CFE4DC")}
    _ann = []
    for _key, _label, _grp in _GM["regions"]:
        _grp = [n for n in _grp if n in _pos]
        if not _grp: continue
        _px = [_pos[n][0] for n in _grp]; _py = [_pos[n][1] for n in _grp]
        _cx = sum(_px) / len(_px); _cy = sum(_py) / len(_py)
        _rad = max(0.7, max(((_pos[n][0] - _cx) ** 2 + (_pos[n][1] - _cy) ** 2) ** 0.5 for n in _grp) + 0.55)
        _fc, _lc = _RTINT.get(_key, ("#EEF3F8", "#CFE0F2"))
        _fg.add_shape(type="circle", x0=_cx - _rad, y0=_cy - _rad, x1=_cx + _rad, y1=_cy + _rad, fillcolor=_fc, line=dict(color=_lc, width=1), layer="below", opacity=0.55)
        _ann.append(dict(x=_cx, y=_cy + _rad + 0.2, text="<b>%s</b>" % _label, showarrow=False, font=dict(size=12, color="#1D3557")))
    _fg.update_layout(annotations=_ann, paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", margin=dict(l=6, r=6, t=30, b=6), height=560,
                      title=dict(text="<b>Inner-self graph (PPMI) · three functional regions combined · cross-region bridges gold · node size = strength</b>", x=0.5, font=dict(size=13)))
    _fg.update_xaxes(visible=False); _fg.update_yaxes(visible=False, scaleanchor="x", scaleratio=1)
    _fg.update_layout(dragmode="pan", uirevision="keep")
    st.plotly_chart(_fg, use_container_width=True, config={"displaylogo": False, "scrollZoom": True, "modeBarButtonsToRemove": ["select2d", "lasso2d"]})
    _bb = sorted(_btw.items(), key=lambda x: -x[1])[:8][::-1]
    _hb = sorted(_strg.items(), key=lambda x: -x[1])[:8][::-1]
    _cL, _cR = st.columns(2, gap="medium")
    with _cL:
        _f1 = _g2.Figure(_g2.Bar(x=[v for _, v in _bb], y=[k for k, _ in _bb], orientation="h", marker_color="#EF9F27",
                                 text=["%.3f" % v for _, v in _bb], textposition="outside", cliponaxis=False))
        _f1.update_layout(title=dict(text="<b>Bridges · betweenness (frequency-neutral)</b>", x=0.5, font=dict(size=13)),
                          paper_bgcolor="#fff", plot_bgcolor="#F8FAFC", margin=dict(l=6, r=6, t=34, b=6), height=300)
        _f1.update_xaxes(gridcolor="#E4ECF3"); _f1.update_yaxes(tickfont=dict(size=13))
        st.plotly_chart(_f1, use_container_width=True, config={"displaylogo": False})
    with _cR:
        _f2 = _g2.Figure(_g2.Bar(x=[v for _, v in _hb], y=[k for k, _ in _hb], orientation="h", marker_color="#1D3557",
                                 text=["%.1f" % v for _, v in _hb], textposition="outside", cliponaxis=False))
        _f2.update_layout(title=dict(text="<b>Hubs · PPMI association strength</b>", x=0.5, font=dict(size=13)),
                          paper_bgcolor="#fff", plot_bgcolor="#F8FAFC", margin=dict(l=6, r=6, t=34, b=6), height=300)
        _f2.update_xaxes(gridcolor="#E4ECF3"); _f2.update_yaxes(tickfont=dict(size=13))
        st.plotly_chart(_f2, use_container_width=True, config={"displaylogo": False})
    C.note("<b>Communities (PPMI, greedy modularity):</b> " + " &nbsp;·&nbsp; ".join("{%s}" % " ".join(c) for c in _GM["communities"]) +
           " — دنیا and آخرة fall in one community (co-present); ذکر·غطاء form their own pair (a measured echo of 18:101 «غطاء عن ذکري»).")
    C.note("<b>Graph-level (MEASURED):</b> %d nodes · %d edges · density %.2f · avg degree %.1f · transitivity %.2f · avg clustering %.2f · %d components · assortativity %.2f · %d cycles · modularity %.2f (z = +%.1f vs null)." % (_S["nodes"], _S["edges"], _S["density"], _S["avg_degree"], _S["transitivity"], _S["avg_clustering"], _S["components"], _S["assortativity"], _S["cycles"], _S["modularity_ppmi"], _S["modularity_z"]))
    with st.expander("per-node graph metrics — ALL 25 nodes (degree · PPMI strength · betweenness · eigenvector · closeness · PageRank · clustering · community)"):
        _rows = []
        for n in sorted(_GM["nodes"], key=lambda n: -_strg[n]):
            _rows.append([n, str(_deg[n]), "%.1f" % _strg[n], "%.3f" % _btw[n], "%.3f" % _GM["eigenvector"][n], "%.3f" % _GM["closeness"][n], "%.3f" % _GM["pagerank"][n], "%.2f" % _GM["clustering"][n], "C%d" % (_GM["community"][n] + 1)])
        C.table(["node", "degree", "PPMI str", "betw", "eigen", "closeness", "PageRank", "clust", "comm"], _rows, tight=True)


    C.section("The organ core — قلب · نفس · صدر · فؤاد : who connects to whom")
    C.note("A focused, hand-laid view of the four inner organs so their links read clearly. <b>Internal</b> ties are the solid lines between organs (weight labelled); each organ's <b>outward</b> attachments are the spokes (its top 4 by PPMI weight, coloured by the neighbour's role). Edges/weights are MEASURED; the placement is for legibility. <b>Reading:</b> قلب is the processing hub — strongly bound to فؤاد (perception, 2.4) and صدر (the chamber, 2.2); نفس stands apart — it has <i>no</i> PPMI edge to قلب or فؤاد, only a faint 0.1 tie to صدر. That separation is the point: نفس is the moral agent (earns, is purified), distinct from the perception/processing organs.")
    import math as _mo
    _ORG = {"قلب": (0.0, 0.0), "فؤاد": (0.0, 2.45), "صدر": (2.65, 0.0), "نفس": (-2.65, 0.0)}
    _ORGSET = set(_ORG); _DIR = {"قلب": 270, "فؤاد": 90, "صدر": 0, "نفس": 180}
    _oc = _g2.Figure()
    for _a, _b, _w in _GM["edges"]:
        if _a in _ORGSET and _b in _ORGSET:
            if {_a, _b} == {"صدر", "نفس"}:
                _xs = [_ORG[_a][0], 0.0, _ORG[_b][0]]; _ys = [_ORG[_a][1], -1.35, _ORG[_b][1]]
                _oc.add_trace(_g2.Scatter(x=_xs, y=_ys, mode="lines", line=dict(color="#AEBED0", width=1.0, dash="dot", shape="spline"), hoverinfo="none", showlegend=False))
                _oc.add_annotation(x=0.0, y=-1.35, text="%.1f" % _w, showarrow=False, font=dict(size=12, color="#566B82"), bgcolor="rgba(255,255,255,.85)")
            else:
                _oc.add_trace(_g2.Scatter(x=[_ORG[_a][0], _ORG[_b][0]], y=[_ORG[_a][1], _ORG[_b][1]], mode="lines", line=dict(color="#1D3557", width=1.4 + 1.6 * _w), hoverinfo="none", showlegend=False))
                _oc.add_annotation(x=(_ORG[_a][0] + _ORG[_b][0]) / 2, y=(_ORG[_a][1] + _ORG[_b][1]) / 2, text="%.1f" % _w, showarrow=False, font=dict(size=12, color="#1D3557"), bgcolor="rgba(255,255,255,.9)")
    for _org in _ORG:
        _nbrs = sorted([(_b if _a == _org else _a, _w) for _a, _b, _w in _GM["edges"] if (_a == _org) != (_b == _org) and not (_a in _ORGSET and _b in _ORGSET)], key=lambda t: -t[1])[:4]
        _k = len(_nbrs); _base = _DIR[_org]; _spread = 54
        for _i, (_nb, _w) in enumerate(_nbrs):
            _ang = _mo.radians(_base - _spread + (2 * _spread * _i / (_k - 1) if _k > 1 else _spread))
            _ex = _ORG[_org][0] + 2.0 * _mo.cos(_ang); _ey = _ORG[_org][1] + 2.0 * _mo.sin(_ang)
            _oc.add_trace(_g2.Scatter(x=[_ORG[_org][0], _ex], y=[_ORG[_org][1], _ey], mode="lines", line=dict(color="#CBD6E2", width=1.0), hoverinfo="none", showlegend=False))
            _oc.add_trace(_g2.Scatter(x=[_ex], y=[_ey], mode="markers+text", marker=dict(size=12, color=_ROLEC.get(_roles.get(_nb, ""), "#888"), line=dict(width=1.1, color="#fff")), text=["%s·%.1f" % (_nb, _w)], textposition="middle " + ("right" if _mo.cos(_ang) >= 0 else "left"), textfont=dict(size=12, color="#10243A"), hoverinfo="none", showlegend=False))
    _oc.add_trace(_g2.Scatter(x=[_ORG[o][0] for o in _ORG], y=[_ORG[o][1] for o in _ORG], mode="markers+text", marker=dict(size=[42 if o == "قلب" else 33 for o in _ORG], color="#1D3557", line=dict(width=2.5, color="#fff")), text=list(_ORG), textposition="middle center", textfont=dict(size=14, color="#fff"), hoverinfo="none", showlegend=False))
    _oc.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", margin=dict(l=6, r=6, t=8, b=6), height=540, dragmode="pan", uirevision="keep")
    _oc.update_xaxes(visible=False, range=[-5.6, 5.6]); _oc.update_yaxes(visible=False, scaleanchor="x", scaleratio=1, range=[-3.1, 5.0])
    st.plotly_chart(_oc, use_container_width=True, config={"displaylogo": False, "scrollZoom": True, "modeBarButtonsToRemove": ["select2d", "lasso2d"]})
    C.note("<b>Signature attachments (MEASURED PPMI strength):</b> قلب → طبع·ختم (sealing, 5.0) · مرض (disease, 4.4); فؤاد → هوی (caprice, 4.5); نفس → تسویل (self-beguiling, 4.1) · دنیا (the near, 1.2); صدر → طبع·ختم (2.9) · علم·عقل (2.0) · the Whisperer lands in it (114:5). A neighbour may attach to more than one organ — each spoke is that organ's own measured link.")

    C.section("Three functional sub-graphs — relief from the dense combined graph")
    C.note("The combined graph above is dense; here the SAME measured edges split into the model's three functional regions. Each panel shows only its members and their internal PPMI edges (force-directed within the panel); the strongest links OUT of the region are named beneath. All MEASURED; the grouping into regions is interpretive.")
    _FS = _GM["func_sub"]
    def _panel(key):
        g = _FS[key]; gp = g["pos"]; gnodes = list(gp)
        ex = []; ey = []
        for x, y, w in g["edges"]:
            ex += [gp[x][0], gp[y][0], None]; ey += [gp[x][1], gp[y][1], None]
        et = _g2.Scatter(x=ex, y=ey, mode="lines", line=dict(color="#C2CEDB", width=1.4), hoverinfo="none", showlegend=False)
        col = [_ROLEC.get(_roles[n], "#888") for n in gnodes]; sz = [16 + 2.4 * (_strg[n] ** 0.5) for n in gnodes]
        hov = ["<b>%s</b><br>PPMI strength %.1f · degree %d · betweenness %.3f" % (n, _strg[n], _deg[n], _btw[n]) for n in gnodes]
        nt = _g2.Scatter(x=[gp[n][0] for n in gnodes], y=[gp[n][1] for n in gnodes], mode="markers+text",
                         marker=dict(size=sz, color=col, line=dict(width=1.5, color="#fff")), text=gnodes,
                         textposition="top center", textfont=dict(size=12, color="#10243A"), hovertext=hov, hoverinfo="text", showlegend=False)
        fig = _g2.Figure([et, nt])
        fig.update_layout(title=dict(text="<b>%s</b>" % g["label"], x=0.5, font=dict(size=13)), paper_bgcolor="#fff",
                          plot_bgcolor="#F8FAFC", margin=dict(l=6, r=6, t=36, b=6), height=350, dragmode="pan", uirevision="keep")
        fig.update_xaxes(visible=False); fig.update_yaxes(visible=False, scaleanchor="x", scaleratio=1)
        st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False, "scrollZoom": True, "modeBarButtonsToRemove": ["select2d", "lasso2d"]})
        C.note("<b>Strongest bridges out:</b> " + " · ".join("%s (%.1f)" % (b[1], b[2]) for b in g["bridges"][:5]))
    for _k in ("apparatus", "drivers", "orientation"):
        _panel(_k)

C.section("The interpretive schematic — the directed reading (illustrative)")
C.note("Beneath the measured graph sits the <i>reading</i>: directed up-drivers and down-drivers, the زاد amplifier, and the کوثر / أبتر outcome, laid out for teaching. Node positions here are illustrative (hand-placed); the directed edges are the interpretive model and their anchors/statistics are the data (see the ledger below). Centrality is deliberately NOT computed on this curated edge-set — that is exactly what the measured graph above is for.")
import math as _math, plotly.graph_objects as _gon
_ROLE={'self':'#1D3557','cog':'#378ADD','act':'#0F6E56','up':'#1D9E75','down':'#E63946','amp':'#EF9F27','bound':'#7A5AA6','dom':'#94A3B8','out_g':'#0F6E56','out_r':'#C1121F','root':'#B5651D'}
_RLAB={'self':'self / organ','cog':'cognition','act':'action','up':'up-driver','down':'down-driver','amp':'feedback (zād)','bound':'veil / partition','dom':'orientation (co-present)','out_g':'outcome: kawthar','out_r':'outcome: abtar','root':'divine root'}
_VAL={'g':'#1D9E75','r':'#E63946','o':'#EF9F27','n':'#94A3B8'}
# id:[ar,en,x,y,role,verse]
_NN={
 'allah':['الله','root — seals, guides, increases, between man and heart',650,66,'root','8:24·50:16'],
 'nafs':['نفس','the self / agent — earns, judged; ammāra→lawwāma→muṭmaʾinna',462,452,'self','91:7·89:27'],
 'sadr':['صدر','the breast / chamber — where the whisper lands',366,452,'self','22:46·114:5'],
 'qalb':['قلب','the heart — processor: reasons, turns, seals/opens',414,498,'self','22:46·7:179'],
 'fuad':['فؤاد','sensor — perception with eye and ear (sight OR 8.8)',225,560,'self','17:36·53:11'],
 'ilm':['علم·عقل','knowledge / reason — sound cognition',590,360,'cog','2:282'],
 'amal':['عمل صالح','righteous action — purifies the self',590,590,'act','16:97'],
 'zann':['ظنّ','conjecture — corrupt cognition',300,690,'down','53:28'],
 'hawa':['هوی','desire enthroned as a god — rival governor',150,610,'down','45:23'],
 'dhikr':['ذکر','remembrance / revelation — the input, the defence',230,250,'up','13:28·7:201'],
 'taqwa':['تقوی','God-wariness — the running guidance',390,180,'up','2:282·8:29'],
 'iman':['إیمان','faith — validates the deed',520,165,'up','16:97'],
 'huda':['هدی','guidance — increased for the guided',640,195,'up','47:17'],
 'lahw':['لهو·لعب','diversion and play — the nature of the near life',120,400,'down','29:64'],
 'waswas':['وسواس·شیطان','the Whisperer — external injection into the breast',150,300,'down','114:5'],
 'taswil':['تسویل·نفس','enticement — internal fair-seeming of the wrong',270,500,'down','12:18·47:25'],
 'marad':['مرض','disease of the heart — grows',430,660,'down','2:10·9:125'],
 'tab':['طبع·ختم','sealing — the absorbing state',560,690,'down','63:3·2:7'],
 'zad':['زاد','amplifier — reinforces either pole',730,470,'amp','47:17·2:10'],
 'barzakh':['برزخ','a partition — the dead until resurrection (23:100); 2 of 3 uses are the sea-barrier, NOT a world-wall',1150,455,'bound','23:100·55:20'],
 'ghita':['غطاء','veil over PERCEPTION — present in life (18:101), lifted when sight sharpens (50:22)',770,300,'bound','18:101·50:22'],
 'dunya':['دنیا','the near (root دنو = draw near) — the passing, lahw·laʿib; a CO-PRESENT orientation, not a later time',1140,600,'dom','29:64·87:16'],
 'akhira':['آخرة·حیوان','the lasting / real life (al-ḥayawān) — CO-PRESENT now but veiled; wanted or not',1140,310,'dom','29:64·42:20'],
 'kawthar':['کوثر','continuity that CROSSES — the اخروی orientation, joined to the lasting',1040,205,'out_g','108:1'],
 'abtar':['أبتر','severance — CUT OFF; the دنیوی orientation, clinging to the near',1030,705,'out_r','108:3'],
}
_EE=[
 ['ilm','amal','knowledge issues in deed','n','35:28',0.0],['amal','ilm','deed/taqwā → guidance & teaching','g','29:69',0.35],
 ['amal','ilm','evil deed → RUST on the heart','r','83:14',-0.35],['dhikr','ilm','input feeds cognition','g','13:28',0],
 ['taqwa','ilm','taqwā → He teaches you','g','2:282',0],['iman','amal','faith validates the deed','g','16:97',0],
 ['huda','qalb','guidance opens the heart','g','47:17',0],['ilm','qalb','cognition runs on the heart','n','22:46',0],
 ['amal','nafs','action transforms the self','n','91:9',0],['zann','ilm','conjecture corrupts cognition','r','53:28',0],
 ['hawa','nafs','desire-as-god governs the self','r','45:23',0],['hawa','amal','drives desire-led action','r','53:23',0.2],
 ['lahw','dhikr','diverts from remembrance','r','63:9',0],['waswas','sadr','whispers into the chamber','r','114:5',0],
 ['taswil','nafs','entices the self from within','r','12:18',0],['marad','qalb','disease afflicts and grows','r','2:10',0],
 ['tab','qalb','sealing — terminal','r','63:3',0],['zad','kawthar','amplifies faith↑faith','g','47:17',0.2],
 ['zad','abtar','amplifies disease↑disease','r','2:10',0.2],['ilm','zad','sound loop feeds amplifier','g','47:17',0.1],
 ['marad','zad','corrupt loop feeds amplifier','r','2:10',0.1],
 ['amal','dunya','deeds aimed at the near — harvest of the dunyā','r','42:20·87:16',0.18],
 ['amal','akhira','deeds aimed at the lasting — harvest of the ākhira','g','42:20·2:201',-0.18],
 ['hawa','dunya','desire pulls the self to the near/passing','r','79:38',0.1],
 ['lahw','dunya','the near life IS distraction and play','r','29:64',0],
 ['nafs','dunya','a self turned to the near is دنیوی','n','—',0.12],
 ['nafs','akhira','a self turned to the lasting is اخروی','n','—',-0.12],
 ['dunya','abtar','clinging to the near → cut off','r','108:3',0.12],
 ['akhira','kawthar','joined to the lasting → continuity','g','29:64·108:1',0.12],
 ['qalb','akhira','heart with yaqīn perceives the real (veil lifts)','g','2:4·50:22',0.2],
 ['ghita','fuad','veil over perception — present in life','n','18:101',0],
 ['ghita','akhira','veil lifted, sight sharpens → the real seen','g','50:22',0.25],
 ['nafs','barzakh','every nafs tastes death; a partition for the dead — not the world-wall','n','3:185·23:100',0],
 ['allah','qalb','seals · guides · comes between','n','8:24·64:11',0],['allah','zad','He increases (zādahum)','n','47:17',0],
 ['sadr','qalb','chamber contains the heart','n','22:46',0],['nafs','sadr','self contains the chamber','n','—',0],
]
def _Y(y): return -y
_eann=[]; _mx=[]; _my=[]; _mt=[]
for a,b,lab,val,vs,cv in _EE:
    if a not in _NN or b not in _NN: continue
    xa,ya=_NN[a][2],_Y(_NN[a][3]); xb,yb=_NN[b][2],_Y(_NN[b][3])
    dx,dy=xb-xa,yb-ya; L=_math.hypot(dx,dy) or 1.0
    ox,oy=-dy/L*(cv*120),dx/L*(cv*120)
    xa2,ya2,xb2,yb2=xa+ox,ya+oy,xb+ox,yb+oy
    _eann.append(dict(x=xb2,y=yb2,ax=xa2,ay=ya2,xref='x',yref='y',axref='x',ayref='y',showarrow=True,
        arrowhead=2,arrowsize=1,arrowwidth=1.5,arrowcolor=_VAL[val],opacity=.5,standoff=13,startstandoff=13))
    _mx.append((xa2+xb2)/2);_my.append((ya2+yb2)/2);_mt.append("<b>%s → %s</b><br>%s<br>%s"%(_NN[a][0],_NN[b][0],lab,vs))
_SZ={'root':30,'self':26,'out_g':26,'out_r':26,'dom':25,'amp':22,'bound':20}
_nx=[];_ny=[];_nt=[];_nc=[];_ns=[];_nh=[]
for k,(ar,en,x,y,role,vs) in _NN.items():
    _nx.append(x);_ny.append(_Y(y));_nt.append(ar);_nc.append(_ROLE[role]);_ns.append(_SZ.get(role,18))
    _nh.append("<b>%s</b> · [%s]<br>%s<br>%s"%(ar,_RLAB.get(role,role),en,vs))
_fig=_gon.Figure([
    _gon.Scatter(x=_mx,y=_my,mode='markers',marker=dict(size=16,color='rgba(0,0,0,0)'),hovertext=_mt,hoverinfo='text',showlegend=False),
    _gon.Scatter(x=_nx,y=_ny,mode='markers+text',marker=dict(size=_ns,color=_nc,line=dict(width=2,color='#ffffff')),
        text=_nt,textposition='top center',textfont=dict(size=13,color='#10243A'),hovertext=_nh,hoverinfo='text',showlegend=False),
])
_fig.add_shape(type='rect',x0=60,y0=_Y(756),x1=1240,y1=_Y(108),fillcolor='#F8FAFC',line=dict(width=0),layer='below')
_fig.add_shape(type='rect',x0=18,y0=_Y(94),x1=1282,y1=_Y(36),fillcolor='#F4EEE7',line=dict(color='#E3D3C4',width=1),layer='below')
_fig.update_layout(annotations=_eann+[
    dict(x=80,y=_Y(66),text='the root — over all',showarrow=False,font=dict(size=12,color='#8a6d2f'),xanchor='left'),
    dict(x=1232,y=_Y(150),text='oriented to the lasting (آخرة) → kawthar',showarrow=False,font=dict(size=12,color='#0F6E56'),xanchor='right'),
    dict(x=1232,y=_Y(665),text='oriented to the near (دنیا) → abtar',showarrow=False,font=dict(size=12,color='#8a6d2f'),xanchor='right'),
 ],paper_bgcolor='#FFFFFF',plot_bgcolor='#FFFFFF',margin=dict(l=6,r=6,t=6,b=6),height=560,showlegend=False,hovermode='closest',dragmode='pan')
_fig.update_xaxes(visible=False,range=[0,1300])
_fig.update_yaxes(visible=False,range=[_Y(772),_Y(18)],scaleanchor='x',scaleratio=1)
st.plotly_chart(_fig,use_container_width=True,config={'displaylogo':False,'scrollZoom':True,'modeBarButtonsToRemove':['select2d','lasso2d']})
_lg=[('self / organ','#1D3557'),('cognition','#378ADD'),('action','#0F6E56'),('up-driver','#1D9E75'),('down-driver','#E63946'),('feedback (zād)','#EF9F27'),('veil / partition','#7A5AA6'),('orientation','#94A3B8'),('kawthar','#0F6E56'),('abtar','#C1121F'),('root','#B5651D')]
st.markdown("<div style='display:flex;flex-wrap:wrap;gap:5px 13px;font-size:12px;color:#10243A;margin:2px 2px 6px'>"+ "".join("<span style='display:inline-flex;align-items:center;gap:5px'><span style='width:11px;height:11px;border-radius:50%%;background:%s;display:inline-block'></span>%s</span>"%(c,n) for n,c in _lg)+"</div>", unsafe_allow_html=True)
C.note("<b>Graph metrics</b> — these describe the curated model (the edge-set), not a discovered corpus topology, "
       "and are layout-independent (node positions are illustrative): <b>25 nodes · 37 edges</b>, directed density "
       "0.06, one connected component. Edge valence: <b>11</b> toward the lasting/openness · <b>15</b> toward the "
       "near/severance · <b>11</b> structural. Most-connected: <b>علم·عقل and عمل·صالح (degree 8)</b> — the "
       "cognition↔action loop is the hub — then قلب · نفس (7), then زاد · دنیا · آخرة (5). Per-edge statistics "
       "(counts, Fisher odds-ratios, anchors) are in the charts and full ledger below. Centrality/betweenness are "
       "deliberately NOT computed: on a hand-curated edge-set they would measure our choices, not the corpus.")

# -- 6b - THE MEASURED LEDGER, AS CHARTS (house plotly style) --
import plotly.graph_objects as _go
_INKp = "#10243A"
def _layp(fig, title, h=360):
    fig.update_layout(title=dict(text=f"<b>{title}</b>", x=0.5, font=dict(size=15)),
                      paper_bgcolor="#FFFFFF", plot_bgcolor="#F8FAFC",
                      font=dict(size=13, color=_INKp), margin=dict(l=10, r=10, t=48, b=10), height=h)
    fig.update_xaxes(gridcolor="#E4ECF3", zeroline=False)
    fig.update_yaxes(gridcolor="#E4ECF3", zeroline=False)
    return fig

C.section("The measured ledger — every edge, as a chart")
with st.expander("ℹ️ concept · finding · significance"):
    st.markdown(
        "**Concept.** Every edge in the network above is a *measured* relation on Book6 — a Fisher "
        "odds-ratio or a raw count — not an assertion.\n\n"
        "**Finding.** The bonds sit far above chance (the amplifier زاد↔disease at OR 16.2, فؤاد↔senses "
        "at 8.8), and the faculties take visibly different verbs (the heart turns and is sealed; the self "
        "is purified).\n\n"
        "**Significance.** This is the checkable spine under the picture. The graph's *layout* is "
        "interpretive and is deliberately NOT scored with centrality or betweenness — those would measure "
        "the drawing, not the corpus.")

# Chart 1 — effect sizes vs the Fisher null (chance = OR 1)
_orr = [("zād ↔ disease", 16.2, "#E63946"), ("fuʾād ↔ senses", 8.8, "#1D3557"),
        ("zād ↔ guidance", 3.5, "#1D9E75"), ("zād ↔ disbelief", 3.2, "#E63946"),
        ("zād ↔ faith", 2.6, "#1D9E75")]
_orr.sort(key=lambda r: r[1])
f1 = _go.Figure(_go.Bar(x=[v for _, v, _ in _orr], y=[n for n, _, _ in _orr], orientation="h",
                        marker_color=[c for *_, c in _orr],
                        text=[f"OR {v}" for _, v, _ in _orr], textposition="outside",
                        cliponaxis=False))
f1.add_vline(x=1, line=dict(color="#10243A", width=1.4, dash="dash"))
f1.add_annotation(x=1, y=1.06, yref="paper", text="chance · OR 1", showarrow=False,
                  font=dict(size=12, color="#10243A"))
f1.update_layout(xaxis_title="Fisher odds-ratio (co-occurrence vs chance)", yaxis_title="",
                 xaxis_range=[0, 18])
st.plotly_chart(_layp(f1, "How far above chance each bond sits  ·  vs Fisher null (OR = 1)", h=330),
                use_container_width=True)

# Chart 2 — predicate dissociation: qalb vs nafs (counts)
_preds = ["turn (q-l-b)", "seal (ṭabʿ / khatm)", "purify (zakā)"]
f2 = _go.Figure()
f2.add_trace(_go.Bar(name="qalb · heart", x=_preds, y=[155, 11, 1], marker_color="#1D3557",
                     text=[155, 11, 1], textposition="outside", cliponaxis=False))
f2.add_trace(_go.Bar(name="nafs · self", x=_preds, y=[4, 0, 7], marker_color="#0F6E56",
                     text=[4, 0, 7], textposition="outside", cliponaxis=False))
f2.update_layout(barmode="group", yaxis_title="times the predicate attaches", xaxis_title="",
                 legend=dict(orientation="h", y=1.13, x=0, font=dict(size=12)))
st.plotly_chart(_layp(f2, "The faculties take different verbs  ·  qalb vs nafs (counts)", h=340),
                use_container_width=True)

C.note("Both charts are MEASURED on Book6 (Fisher exact / raw counts). The full edge-by-edge ledger, with "
       "the Qurʾānic anchor and status (MEASURED · TEXT · INFERRED) for every relation, is below.")
with st.expander("full ledger — every edge, anchor, statistic, status"):
    C.table(["Relation in the graph", "Qurʾānic anchor", "Statistic", "Status"], tight=False, rows=[
        ["فؤاد ↔ sight / hearing", "17:36 · 53:11", "Fisher OR 8.8 (p = 5.5e-4)", "MEASURED"],
        ["قلب takes turn (قلب) vs نفس", "—", "155 vs 4", "MEASURED"],
        ["قلب sealed (طبع/ختم) vs نفس", "2:7 · 63:3", "11 vs 0", "MEASURED"],
        ["نفس purified (زكو) vs قلب", "91:9 · 87:14", "7 vs 1", "MEASURED"],
        ["علم ∩ عمل (cognition-action loop)", "35:28 · 16:97", "42 shared verses", "MEASURED"],
        ["faith→deed («amanu wa amilu l-salihat»)", "2:25 etc.", "50 verses", "MEASURED"],
        ["deed-while-believing («wa-huwa muʾmin»)", "16:97 · 4:124", "5 verses", "MEASURED"],
        ["evil deed → rust (ران) on the heart", "83:14", "1 (the anchor)", "TEXT"],
        ["waswasa: شيطان vs نفس", "114:5 · 50:16", "4 vs 1", "MEASURED"],
        ["taswil (enticement): نفس vs شيطان", "12:18 · 47:25", "3 vs 1", "MEASURED"],
        ["زاد ↔ disease (مرض)", "2:10 · 9:125", "Fisher OR 16.2 (p = 1.3e-3)", "MEASURED"],
        ["زاد ↔ guidance (هدى)", "47:17 · 19:76", "Fisher OR 3.5", "MEASURED"],
        ["زاد ↔ disbelief (كفر)", "3:90 · 9:125", "Fisher OR 3.2", "MEASURED"],
        ["زاد ↔ faith (إيمان)", "8:2 · 9:124", "Fisher OR 2.6 (p = 3.4e-3)", "MEASURED"],
        ["نفس ⊃ صدر ⊃ قلب (containment)", "22:46", "structural", "TEXT"],
        ["نفس = locus of fujūr / taqwā", "91:7-8", "—", "TEXT"],
        ["دنیا = the near (root دنو), present orientation, lahw·laʿib", "29:64 · 87:16", "co-present, not a later time", "TEXT"],
        ["آخرة = the lasting/real life (al-ḥayawān), present but veiled", "29:64 · 42:20", "—", "TEXT"],
        ["دنیا vs آخرة weighed as a present choice (yurīd)", "3:152 · 42:20", "57 shared verses; ~24% with a wanting-verb", "MEASURED"],
        ["غطاء = veil over perception, present in life, lifted at death", "18:101 · 50:22", "—", "TEXT"],
        ["barzakh = a partition (seas; the dead) — not the world-wall", "25:53 · 55:20 · 23:100", "2 of 3 uses are sea-barriers", "MEASURED"],
        ["closed vs open heart-state gradation", "—", "modularity z = -7.31 (NULL)", "MEASURED"],
        ["coupled processor (قلب) + agent (نفس)", "—", "a held-lightly reading", "INFERRED"],
    ])

C.section("Gating chain — what survives, and where the model stops")
C.para("<b>Naive look</b> — four words that all seem to mean 'heart'. <b>Control 1 · dissociation</b> — they take "
       "different predicates at very different rates (155:4 turn, 11:0 seal, 1:7 purify); they are distinct organs, "
       "not synonyms. <b>Control 2 · above chance</b> — the key bindings pass Fisher exact (فؤاد↔perception OR 8.8; "
       "زاد↔disease OR 16.2), so they are not artifacts of frequency. <b>Control 3 · the loop</b> — علم and عمل "
       "genuinely co-occur (42 verses) in both valences; the coupling is real. <b>Control 4 · gradation</b> — here "
       "the ground gives way: a similarity network of heart-states does NOT separate closed from open (z = −7.31). "
       "The parts and the loop and the amplifier survive; a single ranked ladder of states does not.")

# ── 8 · INTERPRETATION ──
C.section("Interpretation — the measured skeleton vs the inferred reading")
C.callout("MEASURED — what the text's own usage establishes",
          "(1) The inner self is <b>articulated</b>: فؤاد senses, قلب processes (reasons · turns · seals), نفس is "
          "the moral agent that earns and is purified, صدر is the chamber. (2) Cognition and action are a "
          "<b>coupled loop</b> running in both valences. (3) زاد is a <b>real amplifier</b> that compounds whatever "
          "state is present, fastest for disease (OR 16.2). These are facts about the corpus.", accent=C.TEAL)
C.callout("INFERRED — the dynamical reading laid on top (interpretation, not measurement)",
          "Reading the whole as a <b>coupled processor (قلب) + agent (نفس)</b> with sensors, an input channel "
          "(ذكر), a feedback amplifier (زاد), and a bistable settle toward كوثر or أبتر is an INFERRED synthesis. "
          "The 'operating-system / processor' metaphor is a <b>communication device</b>, not a claim the text uses "
          "computational language — it is one way to hold the measured edges together, and other framings are "
          "possible. Why نفس differs from قلب — «فألهمها فجورها وتقواها» (91:8) makes the <i>self</i> the locus of "
          "moral disposition, while sealing/reasoning are <i>heart</i>-events — is itself INFERRED from the "
          "predicate split, well-grounded but not a measurement.", accent=C.GOLD)

# ── 9 · THE NULL ──
C.section("The gradation NULL — reported, not buried")
C.para("The one prediction that FAILS: that the heart's many state-words (sealed طبع · locked قفل · rusted ران · "
       "hardened قسو · diseased مرض … versus trembling وجل · humbled خشع · tranquil طمن · sound سليم) sort into a "
       "clean 'closed vs open' gradation. A context-similarity network of these states did <b>not</b> separate the "
       "two poles — modularity <b>z = −7.31</b>, i.e. the closed and open state-words intermix in their verse "
       "company rather than forming two communities. <b>Reading (calibrated):</b> the states are real and many "
       "(a deep lower bound, ~27 co-referenced states across قلب · صدر · فؤاد), but they are a <i>soft continuum</i> "
       "with no structural valley — so we present them as a LOWER-BOUND inventory for human reading, never as a "
       "validated ranked ladder. Per BASE-TRUTH this is an instrument limit, not textual absence: a "
       "morphology-aware or frequency-balanced instrument may yet resolve it; until then the null stands.")

# ── 10 · CAVEATS ──
C.section("Caveats & confounds")
C.para("<b>Co-occurrence is not co-reference.</b> Sharing a verse shows association, not identity; full "
       "concept-merging (e.g. قلب·صدر·فؤاد as one anatomy) needs referent grounding, which we flag where used. "
       "<b>The metaphor is a tool, not a finding.</b> The processor/agent reading must never be cited as a measured "
       "feature. <b>Frequency confounds.</b> قلب is far more frequent than فؤاد, so we use odds-ratios and Fisher "
       "exact, not raw counts, for the key claims. <b>Diacritics demoted.</b> أمّارة / لوّامة / مطمئنة are "
       "vocalised forms — corroborative, not the divine substrate. <b>Same gate on ourselves.</b> The gradation "
       "null (§⑨) is reported in full; we did not quietly drop the prediction that failed.")

# ── 11 · VERDICT ──
C.section("Verdict")
C.verdict("CANDIDATE",
          "The Qur'ān names the inner self as an <b>articulated, coupled system</b>, not one repeated word: the four "
          "faculties dissociate by predicate (MEASURED — 155:4 turn, 11:0 seal, 1:7 purify; فؤاد↔perception OR 8.8), "
          "cognition and action form a real bidirectional loop (42 shared verses), and زاد is a measured amplifier "
          "that compounds either pole (disease OR 16.2). The integrated dynamical 'processor + agent' model is an "
          "INFERRED synthesis on top of that measured skeleton, and the heart-state <i>gradation</i> is an "
          "unvalidated NULL (z = −7.31). A genuine, partly-measured architecture with an explicitly inferred roof.",
          "part-dissociation & amplifier ~80% MEASURED · integrated dynamical model ~55% INFERRED",
          "the gradation network separating closed/open states under a morphology-aware instrument (would raise it)",
          "referent-grounded merging of قلب·صدر·فؤاد + per-occurrence sense-resolution could lift the model toward "
          "DEFINED")

# ── 12 · TIE TO AL-KAWTHAR ──
C.section("How this ties to al-Kawthar")
C.callout("The inner self is where كوثر and أبتر are decided",
          "Sūrat al-Kawthar sets one axis: <b>كوثر</b> (abundance, continuity that <i>crosses</i> the boundary) "
          "against <b>أبتر</b> (severance, <i>cut off</i>). This model supplies the mechanism. A self whose "
          "cognition↔action loop runs sound, fed by ذكر and amplified by زاد toward faith, is the purified نفس "
          "(89:27) that crosses the برزخ into the real life — كوثر. A self whose loop runs corrupt, the heart "
          "sealed (طبع) and diseased (مرض) and amplified the other way, is cut off at the boundary — أبتر. The "
          "chronology web placed al-Kawthar in revealed time; this places it in the <b>anatomy of the soul</b>. "
          "Both are facets of one program: the same WEB lens, now turned inward.", accent=C.TEAL)

# ── REFLECTION ──
C.section("Reflection")
C.para("This close-up is disciplined in exactly the way the chronology one was: it credits a strong measured "
       "signal (the faculties really do dissociate) and refuses to over-claim the inferred roof (the dynamical "
       "model) or the failed prediction (the state gradation). The recurring temptation here was to draw a neat "
       "linear 'ladder of the heart' from closed to open — and the data said no (z = −7.31). Honouring that null "
       "is what keeps the rest trustworthy. The inner self is a web, measured at its joints; the picture of how it "
       "runs is a reading we hold lightly and label openly.")

# ── SUMMARY ──
C.section("Summary — what holds, what is inferred, what failed")
C.table(["✔ MEASURED — holds", "≈ INFERRED — reading", "✗ NULL — failed"], tight=False, rows=[
    ["Four faculties dissociate by predicate", "Coupled processor (قلب) + agent (نفس)", "Closed/open state gradation (z = −7.31)"],
    ["فؤاد↔perception (Fisher OR 8.8)", "OS / processor metaphor (a device)", "No clean two-community split"],
    ["zad amplifies both poles (disease OR 16.2)", "Two-domains-across-a-veil layout", "States are a soft continuum"],
    ["علم∩عمل loop, both valences (42 verses)", "نفس as moral-disposition locus (91:8)", "Ladder presented as inventory only"],
])

# ── LESSONS ──
C.section("Lessons learned — for every semantic-anatomy claim")
C.table(["Principle", "What it caught here"], tight=False, rows=[
    ["Read meaning from the WHOLE dataset, not one verse", "the dissociations only appear across all occurrences"],
    ["Odds-ratios, not raw counts, for frequency-skewed roots", "قلب ≫ فؤاد; Fisher exact keeps the binding honest"],
    ["Separate MEASURED skeleton from INFERRED roof", "the processor model is labelled, never measured"],
    ["Report the null that breaks your nicest picture", "the heart-state ladder failed (z = −7.31); we kept it visible"],
    ["A metaphor is a communication device, not a finding", "OS/processor framing tagged INFERRED throughout"],
])

# ── TAKEAWAY ──
C.section("Takeaway")
C.callout("In one line — for every reader",
          "The Qur'ān's 'heart' is <b>not one word</b>: فؤاد senses, قلب processes, نفس is the self that earns and "
          "is purified — a coupled web with a real amplifier (زاد) that runs the soul toward <b>كوثر</b> or "
          "<b>أبتر</b>. The parts and the loop are measured; the picture of how it runs is an honest reading laid "
          "on top — and the one neat 'ladder' we hoped for did not survive the test.", accent=C.TEAL)

# ── PERSIAN ABSTRACT ──
C.section("خلاصهٔ کامل و ساختاریافته — Persian abstract")
_FA_ABS = '''<div dir="rtl" id="is-fa" style="font-family:Vazirmatn,Tahoma,'Segoe UI',sans-serif;font-size:15px;line-height:1.95;color:#10243A;text-align:right;background:#F6F9FC;border-right:5px solid #138A74;border-radius:11px;padding:18px 22px">
<b style="color:#0F6E56">۱) پرسش و انگیزه.</b> آیا قرآن «دل» را یک واژهٔ تکراری می‌داند، یا قوای درونی را اجزائی متمایز با کارکردهای متمایز که یک «شبکه» می‌سازند، نه یک فهرست و نه یک درخت؟ این کاوش بر آن فرض استوار است که قرآن نظامی طراحی‌شده است و — مانند تن، زبان و شبکه‌های زیستی — باید همچون «وب» خوانده شود: گره‌ها (مفهوم‌ها) و یال‌ها (هم‌نشینی، کشش، پژواک، تفسیر). در همین متن پیش‌تر سنجیده‌ایم که ساختار «درخت» نیست بلکه «وب» است (۳۰۹ چرخه)، و متن خود را تفسیر می‌کند («القرآن یفسّر بعضه بعضاً»). روشِ راهنمای ما این است: معنا را باید از کلِّ دادگان (همهٔ رخدادهای یک مفهوم) خواند، نه از یک آیه یا واژه‌نامه؛ همهٔ موارد باید دیده شوند. این صفحه یکی از «نماهای نزدیک» در یک برنامهٔ کشف است، نه ادعایی نهایی.<br><br>
<b style="color:#0F6E56">۲) روش.</b> هر رخدادِ هر مفهوم گرد می‌آید، با همسایگانش توصیف می‌شود، خوشه‌بندی می‌گردد، و معناها پدیدار می‌شوند؛ پیش از هر ادعای معنایی، معناها باید «تفکیک» شوند (نه میانگینِ مبهمِ یک ریشه). هم‌نشینی بر «رسمِ» متن سنجیده می‌شود — اسکلتِ بی‌نقطه و بی‌حرکت، که زیرلایهٔ الهی است؛ حرکات و نقاط افزودهٔ بشری‌اند و تنها مؤیّدند و در سنجش پایین‌مرتبه شمرده می‌شوند. پیوندها را با نسبتِ بختِ فیشر و با امتیازِ هم‌آییِ هنجارشدهٔ مثبت (PPMI) می‌سنجیم و در برابرِ «بُرزنِ» تصادفیِ خودِ متن (نولِ حافظِ درجه) می‌آزماییم؛ معیارِ پذیرش، هم‌گراییِ دستِ‌کم سه شیوهٔ مستقل است.<br><br>
<b style="color:#0F6E56">۳) اندام‌ها: تفکیکِ سنجیده.</b> قلب، نفس، صدر و فؤاد در هم‌نشینیِ متفاوت‌اند. فؤاد به دیدن و شنیدن گره خورده (فیشر، نسبتِ بخت ۸٫۸؛ p = ۵٫۵e−۴) — اندامِ ادراک است، نه «دلِ» عام (۱۷:۳۶ سمع و بصر و فؤاد مسئول‌اند؛ ۵۳:۱۱ «ما کذب الفؤادُ ما رأی»). حسِ «برگرداندن/دگرگونی» (ریشهٔ قلب) ۱۵۵ بار با دل و تنها ۴ بار با نفس می‌آید؛ «مهر زدن» (طبع/ختم) ۱۱ بار بر دل و ۰ بار بر نفس؛ «تزکیه» (زکو) ۷ بار بر نفس و تنها ۱ بار بر دل. پس دل اندامِ پردازش است (تعقل، فقه، برگشت، مُهر؛ ۲۲:۴۶ «قلوبٌ یعقلون بها»، ۷:۱۷۹ «قلوبٌ لا یفقهون بها»)، نفس عاملِ اخلاقیِ کسب‌کننده و تزکیه‌شونده (۹۱:۷–۹)، و صدر اتاقی است که وسوسه در آن فرود می‌آید (۱۱۴:۵ «یوسوس فی صدور الناس»).<br><br>
<b style="color:#0F6E56">۴) نفس: سه مقام.</b> قرآن برای نفس سه مقام می‌نهد: نفسِ «امّاره بالسوء» که به بدی فرمان می‌دهد (۱۲:۵۳)، نفسِ «لوّامه» که خود را سرزنش می‌کند (۷۵:۲)، و نفسِ «مطمئنّه» که آرام گرفته و فراخوانده می‌شود (۸۹:۲۷). این یک مسیر است: از فرمان‌بریِ هوس، به خودانتقادی، به آرامش — همان جهتی که حلقهٔ علم↔عمل، ذکر و زاد می‌رانندش. پس نفس نه یک حالتِ ثابت، که یک سفرِ روینده است.<br><br>
<b style="color:#0F6E56">۵) شبکهٔ سنجیده و سنجه‌ها.</b> گرافِ هم‌آییِ روی متن: ۲۵ گره، ۱۴۳ یالِ PPMI، چگالی ۰٫۴۸ (یعنی نزدیک به نیمی از پیوندهای ممکن واقعاً برقرارند)، میانگینِ درجه ۱۱٫۴، گذرایی ۰٫۶۷ و خوشه‌بندی ۰٫۶۴ (همسایگانِ یک گره خود نیز به‌هم پیوسته‌اند — بافتی تنگ)، ناهم‌سانیِ −۰٫۲۷ (هاب‌ها بیشتر به گره‌های کم‌درجه می‌پیوندند)، ۱۲۰ چرخه، و مدولاریتیِ ۰٫۲۳ که در برابرِ نول معنادار است (z = +۴٫۱) — یعنی شبکه‌ای مدولار و واقعی، نه فهرست. دو مؤلفه هست: تنها «أبتر» جداست — بریدگی، حتی در توپولوژی. هابِ شبکه قلب است (نیرومندترین پیوندِ PPMI، ۲۹٫۵)، و پلِ شبکه ذکر است (بالاترین بینیّت، ۰٫۱۰۵) — یاد، اجتماع‌ها را به‌هم می‌دوزد. نیرومندترین یال‌ها: قلب–طبع·ختم ۵٫۰، فؤاد–هوی ۴٫۵، دنیا–آخرة ۳٫۷، ذکر–غطاء ۳٫۶.<br><br>
<b style="color:#0F6E56">۶) اجتماع‌های سنجیده.</b> الگوریتمِ مدولاریتی شش اجتماع می‌یابد: {صدر، طبع·ختم، ظنّ، علم·عقل، فؤاد، قلب، هوی، کوثر} · {إیمان، الله، زاد، مرض، هدی} · {برزخ، تسویل، عمل صالح، نفس، وسواس·شیطان} · {آخرة، تقوی، دنیا، لهو·لعب} · {ذکر، غطاء} · {أبتر}. نکتهٔ گویا: دنیا و آخرة در یک اجتماع‌اند (هم‌حاضر، نه جداافتاده)، و ذکر·غطاء جفتی جدا می‌سازند — پژواکی سنجیده از ۱۸:۱۰۱ «کانت أعینُهم فی غطاءٍ عن ذکری».<br><br>
<b style="color:#0F6E56">۷) وبِ خودتفسیر و پویا.</b> متن خود را تفسیر می‌کند و این سنجیده است: خودتفسیریِ پیش‌خور (z = +۸ تا +۲۱، هم در توالی و هم درون‌آیه‌ای) و پژواکِ آیه‌ای (z = +۱۰۵). و این وب پویاست، نه گرافی منجمد — مانند شبکهٔ غذایی که با فصل می‌چرخد. نول‌ها موقّت‌اند و باید با افزودنِ معناها، ترتیبِ نزول و وزن‌دهی بازآزموده شوند؛ گواهِ آن: خاصیتِ «جهانِ کوچک» روی گرافِ متراکم نول بود اما روی استخوان‌بندیِ تُنُک با σ = ۱۱٫۵ زنده شد.<br><br>
<b style="color:#0F6E56">۸) هستهٔ اندام‌ها — چه‌کس به چه‌کس می‌پیوندد.</b> در نگاهِ متمرکز، قلب هابِ پردازش است: به فؤاد (ادراک، ۲٫۴) و صدر (اتاق، ۲٫۲) سخت گره خورده. اما نفس جداست — هیچ یالِ PPMI با قلب یا فؤاد ندارد، تنها پیوندی نازک (۰٫۱) با صدر. این جدایی، خودْ نکته است: نفس عاملِ اخلاقی است، متمایز از اندام‌های ادراک و پردازش. نشانِ بیرونیِ هر اندام نیز متمایز است: قلب → طبع·ختم (مهر) و مرض (بیماری)؛ فؤاد → هوی (هوس)؛ نفس → تسویل (آراستنِ درونیِ بد) و دنیا (نزدیک)؛ صدر → طبع·ختم، علم·عقل، و فرودِ وسوسه.<br><br>
<b style="color:#0F6E56">۹) سه ناحیهٔ کارکردی.</b> برای خوانایی، همان یال‌های سنجیده به سه ناحیه بخش می‌شوند: <b>اندام‌ها</b> (۶ گره: نفس، صدر، قلب، فؤاد، علم·عقل، عمل صالح)؛ <b>محرک‌ها</b> (۱۲ گره: ذکر، تقوی، إیمان، هدی [بالابرنده]؛ ظنّ، هوی، لهو·لعب، وسواس·شیطان، تسویل، مرض، طبع·ختم [پایین‌کشنده]؛ و زادِ تقویت‌کننده)؛ و <b>جهت‌گیری و فرجام</b> (۷ گره: دنیا، آخرة، غطاء، برزخ، الله، کوثر، أبتر). این تقسیم تفسیری است؛ یال‌ها سنجیده‌اند.<br><br>
<b style="color:#0F6E56">۱۰) حلقهٔ علم↔عمل و زادِ تقویت‌کننده.</b> علم و عمل در ۴۲ آیه هم‌نشین‌اند و حلقه دوسویه است: «الذین آمنوا و عملوا الصالحات» (ایمان→عمل، ۵۰ بار) و «مَن عمل صالحاً و هو مؤمن» (عمل در حالِ ایمان، ۵ بار) یکدیگر را تقویت می‌کنند. آینهٔ تاریک نیز هست: عملِ بد «ران» (زنگار) بر دل می‌نشاند و شناخت را تباه می‌کند (۸۳:۱۴ «بل رانَ علی قلوبهم ما کانوا یکسبون»). بر فرازِ همه، <b>زاد</b> عملگرِ تقویت است: هر حالی حاضر باشد خدا آن را می‌افزاید — بیماریِ دل با نسبتِ بختِ ۱۶٫۲ (۲:۱۰ «فزادهم الله مرضاً»)، هدایت ۳٫۵ (۴۷:۱۷ «زادهم هدیً»)، کفر ۳٫۲، ایمان ۲٫۶. این همان «دوپایداری» است: حالِ اندک، به‌جای ماندن در میانه، به‌سوی یکی از دو قطب می‌دود.<br><br>
<b style="color:#0F6E56">۱۱) آناتومیِ دل: دستِ‌کم ۲۷ حالت.</b> با هم‌مرجع‌گیریِ قلب·صدر·فؤاد، شمارِ حالاتِ دل یک «کفِ پایین» است (~۲۷، نه ۳) و باز/روینده. <b>بسته/آفت‌زده:</b> مهرخورده (طبع·ختم)، قفل (قفل)، پوشیده (غلف)، فروپوشیده (کنن)، زنگارگرفته (رین)، سخت (قسو)، بیمار (مرض)، تنگ (ضیق)، در تنگنا (حرج)، کژ (زیغ)، هراسان (رعب)، یکّه‌خورده (فزع)، فروبرده (شرب)، روی‌گردان (صرف)، فروبسته (حصر)، متعصب (حمی). <b>باز/زنده:</b> ترسان (وجل)، تپنده (وجف)، به‌گلوگاه‌رسیده (بلغ)، استوار (ربط)، فروتن (خشع)، نرم‌شده (خضع)، نرم (لین)، مهربان (رءف)، آرام (طمن)، گراینده (هوی)، سلیم (سلیم). نکته: «ضیق» و «حرج» هرگز با قلب نمی‌آیند، تنها با صدر — پس هم‌مرجع‌گیری ضروری است.<br><br>
<b style="color:#0F6E56">۱۲) معناها همواره یک کفِ پایین‌اند.</b> شمارِ معناهای یک ریشه «کفِ پایین» است، نه فهرستِ کامل؛ در تفکیکِ ریزتر، معناهای بیشتری پدیدار می‌شوند. و معناهای تازه و غیرسنّتی نیز برمی‌آیند و نباید کنار گذاشته شوند — برای نمونه، سنجیده‌ایم: «غفر» = پوششِ کیهانی · فیض/برکشیدن · عفوِ حقوقی؛ «طغی» = کژرویِ اخلاقی در برابرِ سرکشیِ جبّار؛ «وقی» بیش از دو معنا (تقوا، سپر، نگه‌داشت). پس باید با «معناها» کار کرد نه با میانگینِ مبهمِ ریشه.<br><br>
<b style="color:#0F6E56">۱۳) هم‌مرجعی و ترادف.</b> گرهِ معنایی در نهایت یک «مفهوم/مرجع» است = (تفکیکِ چندمعنایی) و (ادغامِ هم‌مرجع). چند ریشهٔ متفاوت می‌توانند یک مرجع را با یک نقش بنامند (رسول·نبی·محمد·أحمد → پیامبر؛ ریشه‌های رسل/نبأ/حمد). اما شباهتِ هم‌آیی این را نمی‌گیرد: هم‌آیی، ترادف و تداعی و تضاد را درهم می‌کند (شمس~قمر، شرق~غرب امتیازِ بالا می‌گیرند). مترادف‌های راستین جانشین‌پذیرند (بافتِ مشابه + هم‌آییِ کم)؛ ادغامِ کامل نیازمندِ دانشِ مرجع است.<br><br>
<b style="color:#0F6E56">۱۴) دنیا و آخرت: تصحیحِ مفهومیِ مهم.</b> «دنیا» از ریشهٔ <b>دنو</b> به‌معنای «نزدیک» است. دنیا (۱۲۸ آیه) و آخرة (ریشهٔ ءخر، ۲۴۲ آیه) در ۵۷ آیه هم‌می‌آیند. این دو، دو زمان نیستند که دیواری آن‌ها را جدا کند؛ بلکه دو <b>جهت‌گیریِ هم‌زمان و هم‌حاضر</b>اند: آنچه می‌اندیشی و می‌کنی، تو را «دنیوی» (روی‌کرده به نزدیکِ گذرا، لهو·لعب) یا «اخروی» (روی‌کرده به ماندگار) می‌کند. ۲۹:۶۴ آخرة را «الحیوان» (زندگیِ حقیقی) می‌خوانَد، با فعلِ حالِ حاضر — نه فقط آینده. حدودِ ۲۴٪ آیاتِ دنیا فعلِ خواستن دارند (رود/حبب/ءثر/بغی؛ ۸۷:۱۶ «بل تؤثرون الحیاة الدنیا») — دنیا همچون متعلَّقِ میل و جهتِ اراده، نه صرفاً یک مکان یا یک دوره.<br><br>
<b style="color:#0F6E56">۱۵) برزخ و غطاء: منظری دیگر.</b> برزخ دیوارِ میانِ دنیا و آخرت <i>نیست</i>. ریشهٔ برزخ تنها ۳ بار به‌کار رفته: ۲۳:۱۰۰ (مردگان را تا رستاخیز بازمی‌دارد) و ۲۵:۵۳ و ۵۵:۲۰ (مرزِ میانِ دو دریا). پس برزخ منظری دیگر است — پیش/پس از مرگ — نه محورِ دنیا↔آخرت. «غطاء» (ریشهٔ غطو، تنها ۲ بار) پرده‌ای بر <b>ادراک</b> است: در زندگی حاضر است (۱۸:۱۰۱) و هنگامِ تیزشدنِ دید برداشته می‌شود (۵۰:۲۲ «فکشفنا عنک غطاءک فبصرک الیوم حدید») — پرده‌ای ادراکی، نه دیوارِ جهان‌ها. آمیختنِ این دو با محورِ دنیا/آخرت خطایی رایج است که این صفحه می‌کوشد آن را اصلاح کند.<br><br>
<b style="color:#0F6E56">۱۶) تفکیکِ سنجیده از تفسیر.</b> همهٔ شمارش‌ها و نسبت‌های بخت <b>سنجیده‌اند</b>. اما خواندنِ کل به‌مثابهٔ «پردازنده (قلب) + عامل (نفس)» با حسگر (فؤاد)، ورودی (ذکر) و تقویت‌کننده (زاد) یک <b>استنتاج/تفسیر</b> است نه اندازه‌گیری؛ استعارهٔ «سیستم‌عامل/پردازنده» تنها ابزارِ بیان است، نه ادعای آنکه متن زبانِ رایانه‌ای دارد. اینکه چرا نفس از قلب جداست — «فألهمها فجورها و تقواها» (۹۱:۸) نفس را جایگاهِ سرشتِ اخلاقی می‌کند، حال‌آنکه مهر و تعقل رویدادهای دل‌اند — نیز استنتاجی است، مستند اما نه اندازه‌گیری‌شده.<br><br>
<b style="color:#0F6E56">۱۷) نتیجهٔ منفیِ صادقانه.</b> یک پیش‌بینی <b>شکست خورد</b>: اینکه حالاتِ دل (مهرخورده، قفل، زنگارگرفته، سخت، بیمار … در برابرِ ترسان، فروتن، آرام، سلیم) به دو خوشهٔ روشنِ «بسته/باز» تقسیم شوند. شبکهٔ شباهتِ بافتاری این دو قطب را جدا نکرد (مدولاریتی z = −۷٫۳۱). پس حالات را همچون «کفِ پایین» برای خواندنِ انسانی عرضه می‌کنیم، نه نردبانی رتبه‌بندی‌شده. بنا بر اصلِ حقیقتِ‌پایه، این حدِّ ابزار است نه نبودِ متن؛ نبودِ شاهد، شاهدِ نبود نیست، و ابزارِ تیزتر شاید بعدها آن را بازنماید.<br><br>
<b style="color:#0F6E56">۱۸) پیوند با الکوثر و داوری.</b> سورهٔ کوثر محوری می‌نهد: <b>کوثر</b> (فزونی و تداومی که از مرز می‌گذرد) در برابرِ <b>أبتر</b> (بریدگی) — و دیدیم که أبتر حتی در توپولوژیِ شبکه نیز تنها گرهِ جدا و بریده است. مدل سازوکار را می‌دهد: نفسی که حلقهٔ علم↔عمل‌اش سالم بدود، با ذکر تغذیه و با زاد به‌سوی ایمان تقویت شود، همان نفسِ مطمئنّه (۸۹:۲۷ «یا أیتها النفس المطمئنة ارجعی») است که از مرگ به حیاتِ حقیقی می‌گذرد — کوثر؛ و نفسی که حلقه‌اش تباه، دلش مهرخورده و بیمار و در جهتِ مخالف تقویت شود، بر مرز بریده می‌شود — أبتر. <b>داوری:</b> CANDIDATE (نمره ۶۸) — اسکلتِ سنجیده (تفکیکِ اجزا + تقویت‌کننده) نیرومند، سقفِ مدلِ پویا استنتاجی، و نردبانِ حالات نتیجه‌ای منفیِ معتبر. آنچه نمره را بالا می‌برد: ابزاری پایدار که حالاتِ دل را جدا کند، یا پویاییِ سنجیده (نه استعاری) برای حلقهٔ علم↔عمل↔زاد.
</div>'''
st.markdown(_FA_ABS, unsafe_allow_html=True)

# ── ARABIC ABSTRACT ──
C.section("الملخّص الكامل والمنظَّم — Arabic abstract")
_AR_ABS = '''<div dir="rtl" id="is-ar" style="font-family:Amiri,'Scheherazade New',Tahoma,serif;font-size:15.5px;line-height:2.0;color:#10243A;text-align:right;background:#F6F9FC;border-right:5px solid #4E6E92;border-radius:11px;padding:18px 22px">
<b style="color:#1D3557">١) السؤال والدافع.</b> أيُسمّي القرآنُ «القلب» كلمةً واحدةً مكرَّرة، أم يُسمّي القوى الباطنةَ أجزاءً متمايزةً بوظائفَ متمايزة تُكوِّن شبكةً لا قائمةً ولا شجرة؟ تقومُ هذه الكاوَشةُ على أنّ القرآنَ نظامٌ مُحكَم، وأنّه — كالجسد واللغة والشبكات الحيويّة — يُقرأ بوصفه «وِبّاً»: عُقَدٌ (مفاهيم) وحوافُّ (مصاحبة، جذب، صدى، تفسير). وقد قِسنا من قبلُ أنّ البنيةَ «وِبّ» لا «شجرة» (٣٠٩ دورات)، وأنّ النصَّ يفسّر بعضُه بعضاً. والمنهجُ الموجِّه: المعنى يُقرأ من كلِّ المُدوَّنة لا من آيةٍ أو معجم؛ ويجبُ النظرُ في كلِّ المواضع. وهذه الصفحةُ نظرةٌ قريبةٌ ضمنَ برنامجِ اكتشاف، لا دعوى نهائيّة.<br><br>
<b style="color:#1D3557">٢) المنهج.</b> نجمعُ كلَّ ورودات كلِّ مفهوم، ونصِفه بجيرانه، ونعنقِدُه، فتنبثقُ المعاني؛ وقبلَ أيِّ دعوى دلاليّة يجبُ «فضُّ» المعاني (لا متوسّطُ الجذرِ المُبهَم). ونقيسُ المصاحبةَ على «رسمِ» النصّ — الهيكلِ الأجردِ من النقط والحركات، وهو الطبقةُ الإلهيّة؛ والحركاتُ والنقطُ صنيعٌ بشريٌّ مؤيِّدٌ يُنزَّلُ في رتبة الدليل. نقيسُ الروابطَ بنسبةِ أرجحيّةِ فيشر وبدرجةِ المصاحبةِ المعياريّةِ الموجبة (PPMI)، ونختبرُها في وجهِ خَلطِ النصّ العشوائيّ (نولٌ يحفظ الدرجات)؛ ومعيارُ القبول تضافرُ ثلاثِ طرائقَ مستقلّةٍ على الأقلّ.<br><br>
<b style="color:#1D3557">٣) الأعضاء: التمايزُ المقيس.</b> ترِدُ قلب ونفس وصدر وفؤاد في مصاحبةٍ مختلفة. الفؤادُ مرتبطٌ بالبصر والسمع (فيشر، نسبة الأرجحية ٨٫٨؛ p = ٥٫٥e−٤) — عضوُ الإدراك لا «قلباً» عامّاً (١٧:٣٦ السمعُ والبصرُ والفؤادُ مسؤولون؛ ٥٣:١١ «ما كذبَ الفؤادُ ما رأى»). ومعنى «التقليب» (جذر قلب) مع القلب ١٥٥ ومع النفس ٤؛ و«الطبع/الختم» على القلب ١١ وعلى النفس ٠؛ و«التزكية» (زكو) للنفس ٧ وللقلب ١. فالقلبُ عضوُ المعالجة (يعقل، يفقه، يتقلّب، يُختَم؛ ٢٢:٤٦ «قلوبٌ يعقلون بها»، ٧:١٧٩ «قلوبٌ لا يفقهون بها»)، والنفسُ الفاعلُ الأخلاقيُّ الذي يكسبُ ويُزكَّى (٩١:٧–٩)، والصدرُ الحجرةُ التي تقعُ فيها الوسوسة (١١٤:٥ «يوسوسُ في صدورِ الناس»).<br><br>
<b style="color:#1D3557">٤) النفس: ثلاثةُ مقامات.</b> يضعُ القرآنُ للنفس ثلاثةَ مقامات: النفسُ «الأمّارةُ بالسوء» (١٢:٥٣)، والنفسُ «اللوّامةُ» التي تلومُ نفسَها (٧٥:٢)، والنفسُ «المطمئنّةُ» التي سكنَتْ فتُدعى (٨٩:٢٧). وهو مسارٌ: من الانقيادِ للهوى، إلى نقدِ الذات، إلى الطمأنينة — وهو الاتّجاهُ ذاتُه الذي تَدفعُ إليه حلقةُ العلم↔العمل والذكرُ وزاد. فالنفسُ ليست حالاً ثابتاً بل رحلةٌ نامية.<br><br>
<b style="color:#1D3557">٥) الشبكةُ المقيسةُ ومقاييسُها.</b> شبكةُ المصاحبةِ على النصّ: ٢٥ عُقدة، ١٤٣ حافّةَ PPMI، كثافة ٠٫٤٨ (أي إنّ نحوَ نصفِ الروابطِ الممكنةِ قائمٌ فعلاً)، متوسّطُ الدرجة ١١٫٤، تعدّيّة ٠٫٦٧ وتكتُّل ٠٫٦٤ (جيرانُ العُقدةِ موصولون بعضُهم ببعض — نسيجٌ متراصّ)، تخالُف ‎−٠٫٢٧، ١٢٠ دورة، ومعاملية ٠٫٢٣ ذاتُ دلالةٍ في وجه النول (z = +٤٫١) — أي شبكةٌ معماريّةٌ حقيقيّةٌ لا قائمة. وثَمّةَ مكوّنان: «أبتر» وحدَه منفصل — انقطاعٌ حتى في الطوبولوجيا. ومِحورُ الشبكة قلب (أقوى رابطةِ PPMI، ٢٩٫٥)، وجِسرُها ذكر (أعلى وَسَاطة، ٠٫١٠٥). وأقوى الحوافّ: قلب–طبع·ختم ٥٫٠، فؤاد–هوی ٤٫٥، دنیا–آخرة ٣٫٧، ذکر–غطاء ٣٫٦.<br><br>
<b style="color:#1D3557">٦) المجتمعاتُ المقيسة.</b> تجدُ خوارزميّةُ المعامليّةِ ستّةَ مجتمعات: {صدر، طبع·ختم، ظنّ، علم·عقل، فؤاد، قلب، هوی، کوثر} · {إیمان، الله، زاد، مرض، هدی} · {برزخ، تسویل، عمل صالح، نفس، وسواس·شیطان} · {آخرة، تقوی، دنیا، لهو·لعب} · {ذکر، غطاء} · {أبتر}. واللافتُ: الدنيا والآخرةُ في مجتمعٍ واحد (متعايشتان لا منفصلتان)، و«ذكر·غطاء» يُكوّنان زوجاً مستقلّاً — صدًى مقيسٌ لـ١٨:١٠١ «كانت أعينُهم في غطاءٍ عن ذكري».<br><br>
<b style="color:#1D3557">٧) الوِبُّ المُفسِّرُ لذاته والديناميّ.</b> النصُّ يفسّرُ بعضُه بعضاً، وهذا مقيس: التفسيرُ الأماميُّ التغذية (z = +٨ إلى +٢١، تسلسليّاً وداخلَ الآية) وصدى الآية (z = +١٠٥). وهذا الوِبُّ ديناميٌّ لا مُجمَّد — كالشبكة الغذائيّة تتبدّلُ بالفصول. والنولُ مؤقّتٌ يجبُ أن يُعادَ اختبارُه مع فضِّ المعاني وترتيبِ النزول والترجيح؛ والدليل: «العالَمُ الصغير» كان معدوماً على الشبكةِ الكثيفة لكنّه انبعثَ على الهيكلِ المتخلخل بـσ = ١١٫٥.<br><br>
<b style="color:#1D3557">٨) قلبُ الأعضاء — مَن يصلُ بمَن.</b> في النظرةِ المركَّزة، القلبُ مِحورُ المعالجة: موثوقٌ بالفؤاد (الإدراك، ٢٫٤) وبالصدر (الحجرة، ٢٫٢). أمّا النفسُ فمنفصلة — لا حافّةَ PPMI لها مع القلب أو الفؤاد، بل رابطةٌ خفيفة (٠٫١) مع الصدر فحسب. وهذا الانفصالُ هو المقصود: النفسُ هي الفاعلُ الأخلاقيّ، متمايزةً عن عضوَي الإدراك والمعالجة. ولكلِّ عضوٍ سِمَتُه الخارجيّة: قلب → طبع·ختم (الختم) ومرض (الداء)؛ فؤاد → هوی (الهوى)؛ نفس → تسویل (التزيينُ الباطنيُّ للسوء) ودنیا (القريب)؛ صدر → طبع·ختم وعلم·عقل ووقوعُ الوسوسة.<br><br>
<b style="color:#1D3557">٩) ثلاثُ مناطقَ وظيفيّة.</b> للوضوح، تنقسمُ الحوافُّ المقيسةُ نفسُها إلى ثلاث: <b>الأعضاء</b> (٦ عُقَد: نفس، صدر، قلب، فؤاد، علم·عقل، عمل صالح)؛ و<b>المحرِّكات</b> (١٢: ذكر، تقوی، إیمان، هدی [مُصعِدات]؛ ظنّ، هوی، لهو·لعب، وسواس·شیطان، تسویل، مرض، طبع·ختم [مُهبِطات]؛ وزادُ المُضاعِف)؛ و<b>الوِجهةُ والمآل</b> (٧: دنیا، آخرة، غطاء، برزخ، الله، کوثر، أبتر). والتقسيمُ استنباطيّ؛ والحوافُّ مقيسة.<br><br>
<b style="color:#1D3557">١٠) حلقةُ العلم↔العمل والمُضاعِف زاد.</b> يجتمعُ العلمُ والعملُ في ٤٢ آية، والحلقةُ ثنائيّةُ الاتّجاه: «الذين آمنوا وعملوا الصالحات» (إيمان→عمل، ٥٠ مرّة) و«مَن عمل صالحاً وهو مؤمن» (عملٌ مع إيمان، ٥) يُعزّز كلٌّ منهما الآخَر. والمرآةُ المظلمة: العملُ السيّئ يُورِثُ «الرَّان» على القلب فيُفسِدُ الإدراك (٨٣:١٤ «بل رانَ على قلوبهم ما كانوا يكسبون»). وفوقَ ذلك، <b>زاد</b> مُضاعِفُ النظام: أيُّ حالٍ حضرَ زادَه اللهُ — للمرض القلبيّ ١٦٫٢ (٢:١٠ «فزادهم اللهُ مرضاً»)، وللهدى ٣٫٥ (٤٧:١٧ «زادهم هدًى»)، وللكفر ٣٫٢، وللإيمان ٢٫٦. وهذا سرُّ «ثنائيّةِ الاستقرار».<br><br>
<b style="color:#1D3557">١١) تشريحُ القلب: ٢٧ حالةً على الأقلّ.</b> بضمِّ مرجعِ قلب·صدر·فؤاد، عددُ أحوال القلب «حدٌّ أدنى» (~٢٧ لا ٣) ومفتوحٌ نامٍ. <b>مغلَقٌ/مُبتلًى:</b> مطبوع (طبع·ختم)، مُقفَل (قفل)، مُغلَّف (غلف)، مكنون (كنن)، مَرين (رين)، قاسٍ (قسو)، مريض (مرض)، ضيّق (ضيق)، حَرِج (حرج)، زائغ (زيغ)، مرعوب (رعب)، فَزِع (فزع)، مُشرَب (شرب)، مصروف (صرف)، محصور (حصر)، مُتعصِّب (حمي). <b>مفتوحٌ/حيّ:</b> وَجِل (وجل)، واجف (وجف)، بالغُ الحنجرة (بلغ)، مربوط (ربط)، خاشع (خشع)، خاضع (خضع)، ليّن (لين)، رؤوف (رءف)، مطمئنّ (طمن)، صاغٍ (هوی)، سليم (سليم). ولافتةٌ منهجيّة: «ضيق» و«حرج» لا يرِدان مع القلب أبداً بل مع الصدر — فضمُّ المرجعِ ضروريّ.<br><br>
<b style="color:#1D3557">١٢) المعاني أبداً حدٌّ أدنى.</b> عددُ معاني الجذرِ «حدٌّ أدنى» لا قائمةٌ تامّة؛ وعند فضٍّ أدقَّ تنبثقُ معانٍ أكثر. والمعاني الجديدةُ غيرُ التقليديّةِ تنبثقُ أيضاً ولا تُستبعَد — مثالٌ مقيس: «غفر» = سترٌ كونيّ · فضلٌ/رفعة · عفوٌ قضائيّ؛ «طغى» = زيغٌ أخلاقيّ في مقابل بغيِ الجبّار؛ و«وقى» أكثرُ من معنيين (تقوى، تُرس، حِفظ). فيجبُ العملُ على «المعاني» لا على متوسّطِ الجذرِ المُبهَم.<br><br>
<b style="color:#1D3557">١٣) ضمُّ المرجعِ والترادف.</b> العُقدةُ الدلاليّةُ في نهايتها «مفهومٌ/مرجع» = (فضُّ تعدّدِ المعنى) و(ضمُّ المرجعِ الواحد). فقد تُسمّي جذورٌ مختلفةٌ مرجعاً واحداً بدورٍ واحد (رسول·نبي·محمد·أحمد → النبيّ؛ جذور رسل/نبأ/حمد). لكنّ تشابهَ المصاحبةِ لا يلتقطُ هذا: المصاحبةُ تخلِطُ الترادفَ والتداعيَ والتضادّ (شمس~قمر، شرق~غرب تنالُ درجاتٍ عالية). والمترادفاتُ الحقّةُ قابلةٌ للإحلال (سياقٌ متشابه + مصاحبةٌ منخفضة)؛ والضمُّ التامُّ يحتاجُ معرفةَ المرجع.<br><br>
<b style="color:#1D3557">١٤) الدنيا والآخرة: تصحيحٌ مفهوميّ مهمّ.</b> «الدنيا» من جذر <b>دنو</b> أي «القُرب». ترِدُ الدنيا (١٢٨ آية) والآخرة (جذر ءخر، ٢٤٢ آية) معاً في ٥٧ آية. وليستا زمنين يفصلُ بينهما جدار، بل <b>وِجهتان متعايشتان حاضرتان معاً</b>: ما تفكّرُ فيه وتعملُه يجعلُك «دنيويّاً» (مُقبِلاً على القريب الزائل، لهوٍ ولعِب) أو «أخرويّاً» (مُقبِلاً على الباقي). و٢٩:٦٤ تُسمّي الآخرةَ «الحَيَوان» (الحياةَ الحقّ) بصيغةِ الحاضر لا المستقبلِ فحسب. ونحوُ ٢٤٪ من آيات الدنيا تحملُ أفعالَ الإرادة (رود/حبب/ءثر/بغی؛ ٨٧:١٦ «بل تؤثرون الحياةَ الدنيا») — فالدنيا متعلَّقُ الرغبة ووِجهةُ الإرادة، لا مجرّدَ مكانٍ أو حقبة.<br><br>
<b style="color:#1D3557">١٥) البرزخ والغطاء: منظورٌ آخر.</b> البرزخُ <i>ليس</i> الجدارَ بين الدنيا والآخرة. ورَدَ جذرُ برزخ ٣ مرّاتٍ فقط: ٢٣:١٠٠ (يحبِسُ الموتى إلى البعث) و٢٥:٥٣ و٥٥:٢٠ (الحاجزُ بين البحرين). فالبرزخُ منظرٌ آخر — قبلَ الموت/بعدَه — لا مِحورُ الدنيا↔الآخرة. و«الغطاء» (جذر غطو، مرّتان فقط) حجابٌ على <b>الإدراك</b>: حاضرٌ في الحياة (١٨:١٠١) ويُكشَفُ حين يَحِدُّ البصر (٥٠:٢٢ «فكشفنا عنك غطاءك فبصرُك اليومَ حديد») — حجابٌ إدراكيٌّ لا جدارُ عوالم. وخلطُ هذين بمحورِ الدنيا/الآخرة خطأٌ شائعٌ تسعى هذه الصفحةُ لتصحيحه.<br><br>
<b style="color:#1D3557">١٦) الفصلُ بين المقيس والمُستنبَط.</b> كلُّ الأعداد ونِسبِ الأرجحيّة <b>مقيسة</b>. أمّا قراءةُ الكلِّ «معالِجاً (قلب) + فاعلاً (نفس)» بمستشعِرٍ (فؤاد) ومُدخَلٍ (ذكر) ومُضاعِفٍ (زاد) فهي <b>استنباطٌ</b> لا قياس؛ واستعارةُ «نظام التشغيل/المعالِج» أداةُ بيانٍ فحسب، لا ادّعاءَ أنّ النصّ يستعملُ لغةَ الحاسوب. وكونُ النفسِ تختلفُ عن القلب — «فألهمها فجورها وتقواها» (٩١:٨) يجعلُ النفسَ موضعَ الجِبِلّة الأخلاقيّة، بينما الختمُ والتعقّلُ من شؤون القلب — هو أيضاً استنباطٌ مؤسَّسٌ لا قياس.<br><br>
<b style="color:#1D3557">١٧) النتيجةُ السالبةُ بأمانة.</b> فشلَتْ دعوى واحدة: أن تنقسمَ أحوالُ القلب (مطبوع، مُقفَل، مَرين، قاسٍ، مريض … في مقابل وَجِل، خاشع، مطمئنّ، سليم) إلى عنقودين واضحين «مغلق/مفتوح». فشبكةُ التشابهِ السياقيّ لم تفصِلِ القطبين (المعاملية z = −٧٫٣١). لذا نعرضُ الأحوالَ «حدّاً أدنى» للقراءة البشريّة لا سُلَّماً مرتَّباً. ووفقَ بديهيّةِ الحقيقةِ الأساس، فهذا حدُّ الأداة لا غيابُ النصّ؛ وعدمُ الدليلِ ليس دليلَ العدم، وقد تكشفُه أداةٌ أحدُّ لاحقاً.<br><br>
<b style="color:#1D3557">١٨) الصلةُ بالكوثر والحكم.</b> تضعُ سورةُ الكوثر مِحوراً: <b>كوثر</b> (وفرةٌ وامتدادٌ يَعبُرُ الحدّ) في مقابل <b>أبتر</b> (انقطاع) — وقد رأينا أنّ أبتر حتى في طوبولوجيا الشبكة هو العُقدةُ المنفصلةُ المقطوعةُ وحدَها. والنموذجُ يقدّمُ الآليّة: نفسٌ تجري حلقةُ علمِها↔عملِها سليمةً، تتغذّى بالذكر وتُضاعَفُ بزادٍ نحو الإيمان، هي النفسُ المطمئنّةُ (٨٩:٢٧ «يا أيّتها النفسُ المطمئنّةُ ارجعي») العابرةُ إلى الحياة الحقّ — كوثر؛ ونفسٌ تفسُدُ حلقتُها ويُطبَعُ قلبُها ويمرَضُ وتُضاعَفُ في الاتّجاه المضادّ، تُقطَعُ عند الحدّ — أبتر. <b>الحكم:</b> CANDIDATE (الدرجة ٦٨) — الهيكلُ المقيس قويّ، وسقفُ النموذج الديناميّ مُستنبَط، وسُلَّمُ الأحوال نتيجةٌ سالبةٌ معتبرة. وما يرفعُ الدرجة: أداةٌ ثابتةٌ تفصِلُ أحوالَ القلب، أو ديناميّةٌ مقيسةٌ (لا استعاريّة) لحلقةِ العلم↔العمل↔زاد.
</div>'''
st.markdown(_AR_ABS, unsafe_allow_html=True)

st.page_link("pages/27_Closeup_Index.py", label="← Back to the Close-up map", icon="🔎")
