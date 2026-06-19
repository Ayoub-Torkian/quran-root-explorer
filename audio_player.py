# -*- coding: utf-8 -*-
"""Audio recitation — a mobile-first player bar for the Read surface.

Source (verified live, free, no key): the Islamic Network CDN —
    https://cdn.islamic.network/quran/audio/{bitrate}/{edition}/{N}.mp3
where N is the GLOBAL āyah number 1..6236 (standard Ḥafṣ order, the same order as
Book6). We map (sūra, āyah) → N from the corpus itself, so the app's own numbering
drives the request (no external assumption).

The player is one self-contained <iframe> (st.components.v1.html): an <audio> element
+ touch-sized controls + reciter picker + continuous auto-advance through the sūra,
with a repeat mode (off / āyah / sūra) for memorisation. It best-effort highlights and
scrolls the matching āyah in the page (graceful no-op if the browser blocks cross-frame).
"""
import json as _json
import streamlit as st
import streamlit.components.v1 as _components
from analysis import COL_SURAH, COL_AYAH

# Per-āyah editions on the Islamic Network CDN (all standard, widely-used). Default first.
RECITERS = [
    ("ar.alafasy", "Mishary Alafasy"),
    ("ar.abdulbasitmurattal", "Abdul Basit (Murattal)"),
    ("ar.husary", "Mahmoud Al-Husary"),
    ("ar.minshawi", "Al-Minshawi"),
    ("ar.abdurrahmaansudais", "Abdurrahman As-Sudais"),
    ("ar.mahermuaiqly", "Maher Al-Muaiqly"),
    ("ar.ahmedajamy", "Ahmed Al-Ajamy"),
]
_BITRATE = 128
_CDN = "https://cdn.islamic.network/quran/audio"

_OFFSETS = None   # sūra -> global index of its āyah 1 (computed once from the corpus)


def _offsets(corpus):
    """global N of āyah 1 for each sūra, derived from the corpus (Book6) so the
    app's own numbering is authoritative. Verified: 1:1→1, 2:1→8, total→6236."""
    global _OFFSETS
    if _OFFSETS is None:
        df = corpus.df
        counts = (df.groupby(df[COL_SURAH].astype(int))[COL_AYAH]
                  .nunique().sort_index())
        off, run = {}, 0
        for s, c in counts.items():
            off[int(s)] = run + 1
            run += int(c)
        _OFFSETS = off
    return _OFFSETS


def global_index(corpus, surah: int, ayah: int) -> int:
    return _offsets(corpus).get(int(surah), 1) + (int(ayah) - 1)


def _player_html(surah: int, gstart: int, n_ayat: int, start_ayah: int) -> str:
    cfg = _json.dumps({
        "cdn": _CDN, "br": _BITRATE, "surah": int(surah), "gstart": int(gstart),
        "n": int(n_ayat), "start": int(start_ayah) if start_ayah else 1,
        "reciters": RECITERS,
    })
    opts = "".join(f"<option value='{e}'>{lbl}</option>" for e, lbl in RECITERS)
    return """
<style>
 *{box-sizing:border-box;font-family:'Inter',system-ui,sans-serif}
 body{margin:0;color:#10243A;background:transparent}
 .pl{display:flex;align-items:center;gap:8px;flex-wrap:wrap;
   background:#1D3557;border-radius:14px;padding:8px 10px;box-shadow:0 3px 10px rgba(16,36,58,.18)}
 .pl button{min-width:44px;min-height:44px;border:none;border-radius:10px;background:#2C4A6E;color:#fff;
   font-size:18px;font-weight:700;cursor:pointer}
 .pl button.pp{background:#1D9E75;min-width:52px;font-size:20px}
 .pl button:active{filter:brightness(.92)}
 .ref{color:#fff;font-weight:800;font-size:15px;min-width:64px;text-align:center}
 .rep{font-size:13px !important;min-width:64px !important}
 select{min-height:40px;border-radius:10px;border:1px solid #2C4A6E;background:#fff;color:#10243A;
   font-size:13px;font-weight:700;padding:2px 6px;max-width:46vw}
 .barwrap{height:4px;background:#2C4A6E;border-radius:99px;margin-top:7px;overflow:hidden}
 #bar{height:100%;width:0;background:#7FD9BD}
 .err{color:#FFD7C2;font-size:12.5px;font-weight:700}
</style>
<div class=pl>
  <button id=prev title='previous āyah'>⏮</button>
  <button id=pp class=pp title='play'>▶</button>
  <button id=next title='next āyah'>⏭</button>
  <span class=ref id=ref>—</span>
  <button id=rep class=rep title='repeat'>↻ off</button>
  <select id=rec title='reciter'>__OPTS__</select>
  <span class=err id=err></span>
</div>
<div class=barwrap><div id=bar></div></div>
<audio id=au preload=auto></audio>
<script>
const C = __CFG__;
const au=document.getElementById('au'), ref=document.getElementById('ref'),
      pp=document.getElementById('pp'), bar=document.getElementById('bar'),
      err=document.getElementById('err'), rec=document.getElementById('rec');
let a=C.start, repeat=0, playing=false;       // repeat: 0 off · 1 āyah · 2 sūra
const REP=['↻ off','↻ āyah','↻ sūra'];
try{var _sv=localStorage.getItem('qre_reciter');if(_sv){for(var i=0;i<rec.options.length;i++){if(rec.options[i].value==_sv){rec.value=_sv;break;}}}}catch(e){}
function src(n){return C.cdn+'/'+C.br+'/'+rec.value+'/'+(C.gstart+n-1)+'.mp3';}
function hi(n){ // best-effort: highlight + scroll the matching āyah in the page
  try{var d=window.parent.document;
    d.querySelectorAll('.rdr details.playing').forEach(function(e){e.classList.remove('playing');});
    var el=d.getElementById('qa'+C.surah+'_'+n);
    if(el){el.classList.add('playing');el.scrollIntoView({block:'center'});}
  }catch(e){}
}
function load(n,go){a=Math.max(1,Math.min(C.n,n));ref.textContent=C.surah+':'+a;err.textContent='';
  au.src=src(a);hi(a);if(go){au.play().catch(function(){});}}
function setpp(p){playing=p;pp.textContent=p?'⏸':'▶';pp.title=p?'pause':'play';}
pp.onclick=function(){if(!au.src)load(a,false);if(au.paused){au.play().catch(function(){});}else{au.pause();}};
document.getElementById('prev').onclick=function(){load(a-1,true);};
document.getElementById('next').onclick=function(){load(a+1,true);};
document.getElementById('rep').onclick=function(){repeat=(repeat+1)%3;document.getElementById('rep').textContent=REP[repeat];};
rec.onchange=function(){try{localStorage.setItem('qre_reciter',rec.value);}catch(e){}var was=!au.paused;au.src=src(a);if(was)au.play().catch(function(){});};
au.onplay=function(){setpp(true);};
au.onpause=function(){setpp(false);};
au.ontimeupdate=function(){if(au.duration)bar.style.width=(100*au.currentTime/au.duration)+'%';};
au.onerror=function(){err.textContent='audio unavailable — skipping';if(a<C.n)setTimeout(function(){load(a+1,true);},600);};
au.onended=function(){
  if(repeat==1){au.currentTime=0;au.play().catch(function(){});return;}
  if(a<C.n){load(a+1,true);}
  else if(repeat==2){load(1,true);}
  else{setpp(false);bar.style.width='0';}
};
load(a,false);
</script>
""".replace("__CFG__", cfg).replace("__OPTS__", opts)


def render(corpus, surah: int, start_ayah: int = 1, height: int = 116):
    """Render the recitation player bar for `surah`, cued to `start_ayah`."""
    df = corpus.df
    n_ayat = int((df[COL_SURAH].astype(int) == int(surah)).sum())
    gstart = _offsets(corpus).get(int(surah), 1)
    _components.html(_player_html(int(surah), gstart, n_ayat, int(start_ayah or 1)),
                     height=height)
