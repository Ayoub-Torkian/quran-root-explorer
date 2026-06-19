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

# ── STICKY sūra navigation: stays pinned at the top of the screen while you scroll, so
#    you can jump to ANY sūra (or āyah) from ANY point without scrolling back to the top ──
st.markdown(
    "<style>"
    "[data-testid='stLayoutWrapper']:has(.rdnav),"
    "[data-testid='stVerticalBlock'] > [data-testid='stElementContainer']:has(.rdnav){"
    "position:sticky;top:0;z-index:60;background:#FBFCFE;padding:6px 6px 2px;margin:-4px 0 6px;"
    "box-shadow:0 5px 12px rgba(16,36,58,.10);border-radius:0 0 12px 12px}"
    ":has(>.rdnav),.rdnav{margin:0}"
    "[data-testid='stLayoutWrapper']:has(.rdnav) .stButton button{min-height:40px}"
    "</style>", unsafe_allow_html=True)

top = st.columns([1, 3, 1.5, 1])
top[1].markdown("<div class='rdnav'></div>", unsafe_allow_html=True)
if top[0].button("◀ Prev", use_container_width=True):
    st.session_state["read_s"] = max(1, int(st.session_state["read_s"]) - 1)
if top[3].button("Next ▶", use_container_width=True):
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

# ── reflect the current position in the URL (only when it changed → no rerun loop) ──
if st.query_params.get("s") != str(sel) or st.query_params.get("a", "") != (str(cur_a) if cur_a else ""):
    st.query_params["s"] = str(sel)
    if cur_a:
        st.query_params["a"] = str(cur_a)
    elif "a" in st.query_params:
        del st.query_params["a"]

# ── translation choice + text size (shared across the app) ──
_MP = _MEAN.translation_control(st)
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
 .bar{display:flex;flex-wrap:wrap;gap:6px;align-items:center;padding:2px 0 8px}
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
 .row{margin:4px 0}
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
    _components.html(html, height=150, scrolling=True)


_read_tools(int(sel), cur_a, names.get(int(sel), ""))

# ── the whole sūra, inline (page scrolls), highlighting the jumped-to āyah ──
st.markdown(_SR.inline_html(corpus, sel, _MP, cur=(cur_a or None)), unsafe_allow_html=True)

# best-effort: scroll the page to the jumped-to āyah (graceful no-op if the browser blocks it)
if cur_a:
    _components.html(
        "<script>try{var d=window.parent.document;var el=d.getElementById('a%d');"
        "if(el)el.scrollIntoView({block:'center'});}catch(e){}</script>" % int(cur_a),
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
