# -*- coding: utf-8 -*-
"""📖 Read — the primary reading surface. Pick a sūra and read it top to bottom
(original Arabic + your chosen translation), on phone or computer. The page scrolls
naturally (no nested box). Reuses the sūra engine + the shared translation/text-size
controls so a choice made here carries everywhere.

Reading basics:
  • Position lives in the URL (?s=&a=) → every spot is shareable / bookmarkable / resumable.
  • Āyah-jump → highlight + open any āyah without scrolling.
  • Bookmarks + "Continue where you left off" + per-verse copy/share → a small JS-free
    tools bar backed by the browser's localStorage (persists across sessions).
"""
import json as _json
import streamlit as st
import streamlit.components.v1 as _components

import meaning as _MEAN
import mobile as _MOB
import surah_reader as _SR
import audio_player as _AUD
import structure_scales as _SS
from analysis import COL_SURAH, COL_SURAH_NAME, COL_DIACRITIZED
from state import get_corpus, hero, log_page

st.set_page_config(page_title="Read", page_icon="📖", layout="wide")
_MOB.inject()
log_page("read")
corpus = get_corpus()
df = corpus.df

hero("📖 Read the Qur'an",
     "Pick a sūra and read it top to bottom — original Arabic with your chosen translation.")

suras = sorted(set(df[COL_SURAH].astype(int)))
names = {}
_col_name = COL_SURAH_NAME if COL_SURAH_NAME in df.columns else COL_SURAH
for s, n in zip(df[COL_SURAH].astype(int), df[_col_name]):
    names.setdefault(int(s), str(n))

# ── seed position from the URL on first load (resume / shareable links) ──
_qp = st.query_params
if "read_s" not in st.session_state:
    try:
        st.session_state["read_s"] = max(1, min(114, int(_qp.get("s", 1))))
    except Exception:
        st.session_state["read_s"] = 1
    try:
        st.session_state["read_a"] = max(0, int(_qp.get("a", 0)))
    except Exception:
        st.session_state["read_a"] = 0
    st.session_state["read_s_prev"] = st.session_state["read_s"]

# ── apply a pending jump from the structural-context panel BEFORE the nav widgets are built
#    (the read_s / read_a keys are bound to widgets below, so they must be set up here) ──
_jt = st.session_state.pop("_jump_to", None)
if _jt:
    try:
        _js, _ja = int(_jt[0]), int(_jt[1])
        st.session_state["read_s"] = max(1, min(114, _js))
        st.session_state["read_s_prev"] = st.session_state["read_s"]
        st.session_state["read_a"] = max(0, _ja)
    except Exception:
        pass

# ── STICKY TOP BAR: sūra navigation + recitation player pinned together at the top of the
#    screen while you scroll, so you can jump to any sūra/āyah AND reach the player controls
#    from any point without scrolling back. Built on a KEYED container (stable class) with
#    position:sticky — which degrades SAFELY to in-flow-visible if a browser ignores it
#    (unlike the old fixed bottom-dock, which could hide on some laptops). ──
st.markdown(
    "<style>"
    "section[data-testid='stMain'] [data-testid='stVerticalBlock']{gap:.4rem}"
    "[data-testid='stElementContainer']:has(iframe){margin:0 !important}"
    ".st-key-topbar{position:sticky;top:0;z-index:100;background:#FBFCFE;"
    "padding:6px 8px 8px;margin:-4px 0 6px;box-shadow:0 6px 14px rgba(16,36,58,.12);"
    "border-radius:0 0 14px 14px}"
    ".st-key-topbar .stButton button{min-height:40px}"
    ".st-key-topbar iframe{max-width:860px;display:block;margin:0 auto}"
    "</style>", unsafe_allow_html=True)

try:
    _topbar = st.container(key="topbar")
except TypeError:                       # older Streamlit without container keys → in-flow fallback
    _topbar = st.container()
with _topbar:
    # icon-only Prev/Next (sūra) keep the bar slim; the picker shows the current sūra
    top = st.columns([0.8, 3, 1.6, 0.8])
    if top[0].button("◀", use_container_width=True, help="previous sūra"):
        st.session_state["read_s"] = max(1, int(st.session_state["read_s"]) - 1)
    if top[3].button("▶", use_container_width=True, help="next sūra"):
        st.session_state["read_s"] = min(114, int(st.session_state["read_s"]) + 1)
    sel = top[1].selectbox("Sūra", suras, index=suras.index(int(st.session_state["read_s"])),
                           format_func=lambda s: f"{s} · {names.get(s, '')}")

    # switching sūra clears any āyah-jump (it belonged to the old sūra) — set BEFORE the widget
    if sel != st.session_state.get("read_s_prev"):
        st.session_state["read_a"] = 0
        st.session_state["read_s_prev"] = sel
    st.session_state["read_s"] = sel

    _n_ayat = int((df[COL_SURAH].astype(int) == sel).sum())
    cur_a = int(top[2].number_input("Jump to āyah (0 = top)", min_value=0, max_value=_n_ayat,
                                    step=1, key="read_a"))

    # recitation player — slim strip with a ⋯ options sheet; sticks at the top, always reachable.
    # autoplay (one-shot) when arriving from a Search "▶ Play in Reader" hand-off.
    _AUD.render(corpus, int(sel), start_ayah=(cur_a or 1), jumped=bool(cur_a),
                autoplay=bool(st.session_state.pop("read_autoplay", False)))

# ── reflect the current position in the URL (only when it changed → no rerun loop) ──
if st.query_params.get("s") != str(sel) or st.query_params.get("a", "") != (str(cur_a) if cur_a else ""):
    st.query_params["s"] = str(sel)
    if cur_a:
        st.query_params["a"] = str(cur_a)
    elif "a" in st.query_params:
        del st.query_params["a"]

# ── compact controls: translation + reading settings side by side ──
_cc = st.columns(2)
with _cc[0]:
    _MP = _MEAN.translation_control(st)
with _cc[1]:
    _MOB.settings_controls(st)


# ── bookmarks · resume · per-verse copy/share (localStorage, JS-free for the user) ──
def _read_tools(s: int, a: int, sname: str):
    eff = a if a else 1
    ar_text = ""
    # pull the effective āyah's Arabic for "copy verse"
    try:
        from analysis import COL_AYAH
        row = df[(df[COL_SURAH].astype(int) == s) & (df[COL_AYAH].astype(float).astype(int) == eff)]
        if len(row):
            ar_text = str(row[COL_DIACRITIZED].iloc[0])
    except Exception:
        ar_text = ""
    en_text = _MEAN.gloss(f"{s}:{eff}", "en")
    payload = _json.dumps({"s": int(s), "a": int(eff), "name": sname,
                           "ar": ar_text, "en": en_text}, ensure_ascii=False)
    html = """
<style>
 *{box-sizing:border-box;font-family:'Inter',system-ui,sans-serif}
 body{margin:0;color:#10243A}
 .bar{display:flex;flex-wrap:wrap;gap:6px;align-items:center;padding:0 0 5px}
 .btn{font-size:13px;font-weight:700;border:1px solid #cfe4dc;background:#F4F9F7;color:#0F6E56;
   border-radius:999px;padding:5px 12px;cursor:pointer}
 .btn:active{background:#E4F0EB}
 .lbl{font-size:13px;font-weight:800;color:#0F6E56}
 .empty{font-size:12.5px;color:#10243A}
 .chip{display:inline-block;font-size:12.5px;font-weight:700;text-decoration:none;color:#10243A;
   background:#EEF4F1;border:1px solid #d7e8e0;border-radius:999px;padding:3px 9px;margin:2px}
 .chip .x{color:#B23A3A;margin-left:5px;font-weight:800}
 .cont{display:inline-block;font-size:13px;font-weight:800;text-decoration:none;color:#1D3557;
   background:#FFF6DA;border:1px solid #EAD9A0;border-radius:10px;padding:5px 12px;margin:2px 0}
 .row{margin:2px 0}
 .ok{color:#0F6E56;font-weight:700;font-size:12.5px;margin-left:6px}
</style>
<div id=app>
  <div class=bar>
    <button class=btn id=save>★ Save this verse</button>
    <button class=btn id=cpv>⧉ Copy verse</button>
    <button class=btn id=cpl>🔗 Copy link</button>
    <span class=ok id=ok></span>
  </div>
  <div class=row id=cont></div>
  <div class=row><span class=lbl>★ Bookmarks</span> <span id=list></span></div>
</div>
<script>
const cur = __PAYLOAD__;
const BM='qre_bm', LAST='qre_last';
function ld(k){try{return JSON.parse(localStorage.getItem(k)||'null')}catch(e){return null}}
function sv(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
function flash(m){var o=document.getElementById('ok');o.textContent=m;setTimeout(function(){o.textContent=''},1800);}
function url(s,a){var u='?s='+s;if(a)u+='&a='+a;return u;}
// Continue uses the PREVIOUS last-read, then we update it (never clobber a real spot with the bare default)
var prev = ld(LAST);
var ca = cur.a||1;
var contEl=document.getElementById('cont');
if(prev && (prev.s!=cur.s || (prev.a||1)!=ca)){
  contEl.innerHTML = "<a class=cont target=_top href='"+url(prev.s,prev.a)+"'>▶ Continue where you left off — "+prev.s+":"+prev.a+(prev.name?(" · "+prev.name):"")+"</a>";
}
var isDefault=(cur.s==1 && !cur.a);
if(!isDefault) sv(LAST,{s:cur.s,a:ca,name:cur.name});
function render(){
  var bm=ld(BM)||[],h='';
  if(!bm.length){h="<span class=empty>none yet — tap “★ Save this verse”.</span>";}
  else bm.forEach(function(b,i){
    h+="<span class=chip><a class=chip style='border:none;background:none;padding:0;margin:0' target=_top href='"+url(b.s,b.a)+"'>"+b.s+":"+b.a+"</a><span class=x data-i='"+i+"'>×</span></span>";
  });
  document.getElementById('list').innerHTML=h;
  document.querySelectorAll('.x').forEach(function(e){e.onclick=function(){
    var bm=ld(BM)||[];bm.splice(+e.getAttribute('data-i'),1);sv(BM,bm);render();};});
}
document.getElementById('save').onclick=function(){
  var bm=ld(BM)||[];
  if(!bm.some(function(b){return b.s==cur.s&&b.a==ca})){bm.unshift({s:cur.s,a:ca,name:cur.name});sv(BM,bm);render();flash('saved ✓');}
  else flash('already saved');
};
document.getElementById('cpv').onclick=function(){
  var t=cur.s+":"+ca+(cur.name?(" · "+cur.name):"")+"\\n"+(cur.ar||"")+(cur.en?("\\n\\n"+cur.en):"");
  navigator.clipboard.writeText(t).then(function(){flash('verse copied ✓')},function(){flash('copy blocked')});
};
document.getElementById('cpl').onclick=function(){
  var base=(window.top&&window.top.location&&window.top.location.href||'').split('?')[0];
  navigator.clipboard.writeText(base+url(cur.s,ca)).then(function(){flash('link copied ✓')},function(){flash('copy blocked')});
};
render();
</script>
""".replace("__PAYLOAD__", payload)
    _components.html(html, height=84, scrolling=True)


_read_tools(int(sel), cur_a, names.get(int(sel), ""))


# ── per-āyah STRUCTURAL CONTEXT (lazy + cached; reuses the structure engines) ──
@st.cache_data(show_spinner="Reading this āyah's structure…")
def _struct_ctx(_cid):
    return _SS.read_context(corpus)


def _jump_btns(verses, keyp, cur=None, limit=8):
    """Compact row of '{s}:{a}' buttons that jump the reader to that verse (rerun-free of the
    nav widgets — they stash a target the top-of-page handler applies before the widgets build)."""
    seen = []
    for sa in verses:
        s, a = int(sa[0]), int(sa[1])
        if cur is not None and (s, a) == cur:
            continue
        if (s, a) not in seen:
            seen.append((s, a))
        if len(seen) >= limit:
            break
    if not seen:
        return
    cols = st.columns(min(len(seen), 4))
    for j, (s, a) in enumerate(seen):
        if cols[j % len(cols)].button(f"{s}:{a}", key=f"{keyp}_{s}_{a}",
                                      help=f"open {s}:{a} in the reader", use_container_width=True):
            st.session_state["_jump_to"] = (s, a)
            st.rerun()


# ── STRUCTURE FINGERPRINT chip — a one-glance summary shown WITHOUT expanding, so the reader
#    sees there's structure worth opening. Costs nothing until the panel has been opened once
#    (then it reuses the already-cached read_context — never a fresh compute). ──
if st.session_state.get("_struct_ready"):
    try:
        _CXf = _struct_ctx(id(corpus))
        _ayf = int(cur_a) if cur_a else 1
        _if = _CXf["refs"].get((int(sel), _ayf))
        if _if is not None:
            _vrf = _CXf["vroots"][_if]; _drf = _CXf["drop"]; _npf = _CXf["npmi"]
            _crf = sorted(r for r in _vrf if r not in _drf)
            _nb = sum(1 for _a in range(len(_crf)) for _b in range(_a + 1, len(_crf))
                      if frozenset((_crf[_a], _crf[_b])) in _npf)
            _nt = len(_CXf["vt"].get(_if, []))
            _dst = _CXf.get("dist", {})
            _nc = sum(1 for r in _crf if _dst.get(r, {}).get("arch") == "Distributed core")
            _npk = sum(1 for r in _crf if _dst.get(r, {}).get("arch") == "Concentrated pocket")
            _lean = ("core-leaning" if _nc > _npk else "pocket-leaning" if _npk > _nc else "balanced")
            _thf = _CXf.get("sura_theme", {}).get(int(sel))
            _tht = f" · theme ‹{_thf['roots'][0]}›" if _thf else ""
            st.markdown(
                "<div style='display:inline-block;background:#EAF2FB;border:1px solid #CFE0F2;"
                "border-radius:999px;padding:4px 13px;font-size:13px;color:#10243A;font-weight:600;'>"
                f"📐 {_nb} concept-bond{'s' if _nb != 1 else ''} · in {_nt} "
                f"template{'s' if _nt != 1 else ''} · {_lean}{_tht}</div>",
                unsafe_allow_html=True)
    except Exception:
        pass

with st.expander("📐 What this āyah is part of — its place in the Qur'ān's structure"):
    st.caption("A reading lens (optional): how this single āyah sits in the larger pattern — the "
               "idea-pairs it links, and any repeated formula (mathānī) it shares with verses elsewhere. "
               "All from the original roots, measured against the text's own shuffle.")
    _CX = _struct_ctx(id(corpus))
    st.session_state["_struct_ready"] = True
    _aysel = int(cur_a) if cur_a else 1
    _i = _CX["refs"].get((int(sel), _aysel))
    if _i is None:
        st.caption("Use “Jump to āyah” above to pick a verse.")
    else:
        st.markdown(f"**Āyah {sel}:{_aysel}** · {names.get(int(sel), '')}")
        _vr = _CX["vroots"][_i]; _np = _CX["npmi"]; _drop = _CX["drop"]
        _cr = sorted(r for r in _vr if r not in _drop)
        _bonds = []
        for _x in range(len(_cr)):
            for _y in range(_x + 1, len(_cr)):
                _k = frozenset((_cr[_x], _cr[_y]))
                if _k in _np:
                    _bonds.append((_cr[_x], _cr[_y], _np[_k]))
        _bonds.sort(key=lambda z: -z[2])
        if _bonds:
            st.markdown("**Concept-bonds it activates** — pairs of ideas the Qur'ān links far more than "
                        "chance, like two notes that keep sounding together as a chord:")
            st.markdown(" · ".join(f"`{a}·{b}` **{v}**" for a, b, v in _bonds[:10]))
            _ba, _bb, _bv0 = _bonds[0]
            _inv = {i: sa for sa, i in _CX["refs"].items()}
            _bverses = [_inv[i] for i in range(len(_CX["vroots"]))
                        if _ba in _CX["vroots"][i] and _bb in _CX["vroots"][i]]
            st.caption(f"Read other verses where ‹{_ba}› and ‹{_bb}› meet:")
            _jump_btns(_bverses, "bond", cur=(int(sel), _aysel))
        else:
            st.caption("· No strong concept-bonds (beyond plain word frequency) in this āyah.")
        _fams = _CX["vt"].get(_i, [])
        if _fams:
            st.markdown("**Recurring template (mathānī) it belongs to** — a formula echoed across the "
                        "book, like a chorus that returns through a song. Tap a verse to read it:")
            for _fi, _f in enumerate(_fams[:4]):
                st.markdown(f"- `{' · '.join(_f['roots'])}` — recurs in **{_f['n_suras']} chapters** "
                            f"({_f['support']} verses)")
                _jump_btns(_f.get("verses", []), f"tmpl{_fi}", cur=(int(sel), _aysel))
        else:
            st.caption("· Not part of a book-wide recurring template — a mostly unique combination of ideas.")
        _th = _CX.get("sura_theme", {}).get(int(sel))
        if _th:
            st.markdown("**The theme this chapter centers on** — its dominant thread across the whole book "
                        "(the Qur'ān's global topic-model), like which section of a library a book sits in:")
            st.markdown("`" + " · ".join(_th["roots"]) + "`"
                        + f"  — most concentrated in chapters **{_th['lo']}–{_th['hi']}**")
        _dist = _CX.get("dist", {})
        _core = [(r, _dist[r]) for r in _cr if r in _dist and _dist[r]["arch"] == "Distributed core"]
        _pocket = [(r, _dist[r]) for r in _cr if r in _dist and _dist[r]["arch"] == "Concentrated pocket"]
        if _core or _pocket:
            st.markdown("**How its ideas are laid out in the book** — *core* ideas are load-bearing columns "
                        "present throughout; *pocket* ideas are furniture specific to one room:")
            if _core:
                st.markdown("- 🏛️ **Distributed core** (woven through most of the book): "
                            + " · ".join(f"`{r}` — {d['n_suras']} chapters" for r, d in _core[:6]))
            if _pocket:
                st.markdown("- 📍 **Concentrated pocket** (situational, a few chapters): "
                            + " · ".join(f"`{r}` — {d['n_suras']} chapters" for r, d in _pocket[:6]))

# ── the whole sūra, inline (page scrolls), highlighting the jumped-to āyah ──
st.markdown(_SR.inline_html(corpus, sel, _MP, cur=(cur_a or None)), unsafe_allow_html=True)

# ── TAP-TO-PLAY bridge: a tap on any āyah's ▶ tells the recitation player to play from
#    there (and auto-continue). The reader is plain markdown in the MAIN doc, so this tiny
#    helper (in its own iframe) delegates the click on the parent doc and postMessages every
#    iframe — the player picks up {qre_cmd:'play'}. Best-effort: a no-op if the browser
#    blocks parent access (the ▶ then simply does nothing; tap-to-reveal still works). ──
_components.html(
    "<script>try{var pd=window.parent.document;"
    "if(pd&&!pd.__qreTap){pd.__qreTap=1;"
    "pd.addEventListener('click',function(ev){var t=ev.target;"
    "while(t&&t!==pd){if(t.classList&&t.classList.contains('vp'))break;t=t.parentNode;}"
    "if(!t||t===pd||!t.classList||!t.classList.contains('vp'))return;"
    "ev.preventDefault();ev.stopPropagation();"
    "var a=+t.getAttribute('data-a');if(!a)return;"
    "var f=pd.querySelectorAll('iframe');"
    "for(var i=0;i<f.length;i++){try{f[i].contentWindow.postMessage({qre_cmd:'play',a:a},'*');}catch(e){}}"
    "},true);}}catch(e){}</script>",
    height=0)

# best-effort: scroll the page to the jumped-to āyah (graceful no-op if the browser blocks it)
if cur_a:
    _components.html(
        "<script>try{var d=window.parent.document;var el=d.getElementById('qa%d_%d');"
        "if(el)el.scrollIntoView({block:'center'});}catch(e){}</script>" % (int(sel), int(cur_a)),
        height=0)

# ── bottom nav ──
b = st.columns(2)
if sel > 1 and b[0].button("← Previous sūra", use_container_width=True, key="prevb"):
    st.session_state["read_s"] = sel - 1
    st.session_state["read_a"] = 0
    st.rerun()
if sel < 114 and b[1].button("Next sūra →", use_container_width=True, key="nextb"):
    st.session_state["read_s"] = sel + 1
    st.session_state["read_a"] = 0
    st.rerun()
