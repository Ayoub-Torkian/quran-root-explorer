# -*- coding: utf-8 -*-
"""Audio recitation — a mobile-first player bar for the Read surface.

Source (verified live, free, no key, but STREAMED — needs an internet connection):
the Islamic Network CDN —
    https://cdn.islamic.network/quran/audio/{bitrate}/{edition}/{N}.mp3
where N is the GLOBAL āyah number 1..6236 (standard Ḥafṣ order, the same order as
Book6). We map (sūra, āyah) → N from the corpus itself.

IMPORTANT — bitrate is PER edition: not every reciter is published at every bitrate.
Each reciter below carries the bitrate at which its per-āyah files were VERIFIED to
exist (HTTP 200, audio/mpeg). Alafasy/Husary/Minshawi/Maher/Ajamy → 128 kbps;
Abdul Basit & Sudais → 64 kbps (they have no 128 per-āyah set). Using one hardcoded
bitrate is exactly what made some voices silently 404.

The player is one self-contained <iframe>: an <audio> element + touch-sized controls
(play, prev/next āyah, reciter, repeat, SPEED) + continuous auto-advance, and a
best-effort highlight/scroll of the matching āyah in the page.
"""
import json as _json
import streamlit as st
import streamlit.components.v1 as _components
from analysis import COL_SURAH, COL_AYAH

# (edition, label, VERIFIED bitrate). Order = picker order; default first.
RECITERS = [
    ("ar.alafasy", "Mishary Alafasy", 128),
    ("ar.husary", "Mahmoud Al-Husary", 128),
    ("ar.minshawi", "Al-Minshawi", 128),
    ("ar.mahermuaiqly", "Maher Al-Muaiqly", 128),
    ("ar.ahmedajamy", "Ahmed Al-Ajamy", 128),
    ("ar.abdulbasitmurattal", "Abdul Basit (Murattal)", 64),
    ("ar.abdurrahmaansudais", "Abdurrahman As-Sudais", 64),
]
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
        "cdn": _CDN, "surah": int(surah), "gstart": int(gstart),
        "n": int(n_ayat), "start": int(start_ayah) if start_ayah else 1,
        "br": {e: br for e, _l, br in RECITERS},
    })
    opts = "".join(f"<option value='{e}'>{lbl}</option>" for e, lbl, _br in RECITERS)
    return """
<style>
 *{box-sizing:border-box;font-family:'Inter',system-ui,sans-serif}
 body{margin:0;color:#10243A;background:transparent}
 .pl{display:flex;flex-direction:column;gap:6px;background:#1D3557;border-radius:12px;
   padding:7px 9px;box-shadow:0 2px 8px rgba(16,36,58,.18)}
 .prow{display:flex;align-items:center;gap:6px}
 .pl button{height:40px;border:none;border-radius:9px;background:#2C4A6E;color:#fff;
   font-size:16px;font-weight:700;cursor:pointer;flex:0 0 auto;padding:0 10px}
 .pl button.pp{background:#1D9E75;font-size:14px;font-weight:800;white-space:nowrap}
 .pl button:active{filter:brightness(.92)}
 .ref{color:#fff;font-weight:800;font-size:14px;min-width:46px;text-align:center;flex:0 0 auto}
 .barwrap{flex:1 1 auto;height:6px;background:#2C4A6E;border-radius:99px;overflow:hidden;min-width:40px}
 #bar{height:100%;width:0;background:#7FD9BD}
 select{height:40px;border-radius:9px;border:1px solid #2C4A6E;background:#fff;color:#10243A;
   font-size:13px;font-weight:700;padding:2px 6px;flex:1 1 auto;min-width:0}
 .err{color:#FFD7C2;font-size:12px;font-weight:700;flex:0 0 auto}
</style>
<div class=pl>
  <div class=prow>
    <button id=prev title='previous āyah'>⏮</button>
    <button id=pp class=pp title='play'>▶ Play</button>
    <button id=next title='next āyah'>⏭</button>
    <span class=ref id=ref>—</span>
    <div class=barwrap><div id=bar></div></div>
  </div>
  <div class=prow>
    <button id=rep title='repeat'>↻ off</button>
    <button id=spd title='speed'>1×</button>
    <select id=rec title='reciter'>__OPTS__</select>
    <span class=err id=err></span>
  </div>
</div>
<audio id=au preload=auto></audio>
<script>
const C = __CFG__;
const au=document.getElementById('au'), ref=document.getElementById('ref'),
      pp=document.getElementById('pp'), bar=document.getElementById('bar'),
      err=document.getElementById('err'), rec=document.getElementById('rec'),
      spdB=document.getElementById('spd'), repB=document.getElementById('rep');
let a=C.start, repeat=0, si=0;                 // repeat: 0 off·1 āyah·2 sūra ; si=speed index
const REP=['↻ off','↻ āyah','↻ sūra'], SPD=[1,1.25,1.5,0.75];
try{var _sv=localStorage.getItem('qre_reciter');if(_sv){for(var i=0;i<rec.options.length;i++){if(rec.options[i].value==_sv){rec.value=_sv;break;}}}}catch(e){}
function src(n){return C.cdn+'/'+C.br[rec.value]+'/'+rec.value+'/'+(C.gstart+n-1)+'.mp3';}
function hi(n){try{var d=window.parent.document;
    d.querySelectorAll('.rdr details.playing').forEach(function(e){e.classList.remove('playing');});
    var el=d.getElementById('qa'+C.surah+'_'+n);
    if(el){el.classList.add('playing');el.scrollIntoView({block:'center'});}
  }catch(e){}}
function load(n,go){a=Math.max(1,Math.min(C.n,n));ref.textContent=C.surah+':'+a;err.textContent='';
  au.src=src(a);au.playbackRate=SPD[si];hi(a);if(go){au.play().catch(function(){});}}
function setpp(p){pp.textContent=p?'⏸ Pause':'▶ Play';pp.title=p?'pause':'play';}
pp.onclick=function(){if(!au.src)load(a,false);if(au.paused){au.play().catch(function(){});}else{au.pause();}};
document.getElementById('prev').onclick=function(){load(a-1,true);};
document.getElementById('next').onclick=function(){load(a+1,true);};
repB.onclick=function(){repeat=(repeat+1)%3;repB.textContent=REP[repeat];};
spdB.onclick=function(){si=(si+1)%SPD.length;au.playbackRate=SPD[si];spdB.textContent=SPD[si]+'×';};
rec.onchange=function(){try{localStorage.setItem('qre_reciter',rec.value);}catch(e){}var was=!au.paused;au.src=src(a);au.playbackRate=SPD[si];if(was)au.play().catch(function(){});};
au.onplay=function(){setpp(true);};
au.onpause=function(){setpp(false);};
au.ontimeupdate=function(){if(au.duration)bar.style.width=(100*au.currentTime/au.duration)+'%';};
au.onerror=function(){err.textContent='unavailable — skipping';if(a<C.n)setTimeout(function(){load(a+1,true);},600);};
au.onended=function(){
  if(repeat==1){au.currentTime=0;au.play().catch(function(){});return;}
  if(a<C.n){load(a+1,true);}
  else if(repeat==2){load(1,true);}
  else{setpp(false);bar.style.width='0';}
};
load(a,false);
</script>
""".replace("__CFG__", cfg).replace("__OPTS__", opts)


def render(corpus, surah: int, start_ayah: int = 1, height: int = 104):
    """Render the recitation player bar for `surah`, cued to `start_ayah`."""
    df = corpus.df
    n_ayat = int((df[COL_SURAH].astype(int) == int(surah)).sum())
    gstart = _offsets(corpus).get(int(surah), 1)
    _components.html(_player_html(int(surah), gstart, n_ayat, int(start_ayah or 1)),
                     height=height)
