# -*- coding: utf-8 -*-
"""Audio recitation — a mobile-first player for the Read surface.

Source (verified live, free, no key, but STREAMED — needs an internet connection):
the Islamic Network CDN —
    https://cdn.islamic.network/quran/audio/{bitrate}/{edition}/{N}.mp3
where N is the GLOBAL āyah number 1..6236 (standard Ḥafṣ order, the same order as
Book6). We map (sūra, āyah) → N from the corpus itself.

IMPORTANT — bitrate is PER edition: not every reciter is published at every bitrate.
Each reciter below carries the bitrate at which its per-āyah files were VERIFIED to
exist (HTTP 200, audio/mpeg). Alafasy/Husary/Minshawi/Maher/Ajamy → 128 kbps;
Abdul Basit & Sudais → 64 kbps (they have no 128 per-āyah set).

DESIGN (2026-06-19): a permanently SLIM play strip — ⏮ ▶/⏸ ⏭ · ref · progress · ⋯ ✕ —
with a rerun-free OPTIONS SHEET behind ⋯ (reciter, speed −/+, repeat, follow). The sheet
lives in the same iframe and the iframe self-grows (window.frameElement) so it is never
clipped; everything is one tap away and nothing triggers a Streamlit rerun.

EXIT: ✕ stops playback, clears the follow-highlight, and collapses the player to a slim
"🎧 Recite" launcher so reading is unobstructed (persists in qre_exited; no auto-resume
while exited). Tapping the launcher — or any āyah's ▶ — re-enters recitation.

FOLLOW + TAP-TO-PLAY: when playback starts on any āyah the page scrolls to it (au.onplay
→ hi()), gated by a "follow" toggle. The player listens for postMessage {qre_cmd:'play',
a:N} so tapping an āyah in the reader plays from there and auto-continues. Both reach the
reader (which lives in the MAIN document) via window.parent — best-effort, wrapped in try.
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


def _player_html(surah: int, gstart: int, n_ayat: int, start_ayah: int, jumped: bool,
                 autoplay: bool = False, base_h: int = 60) -> str:
    cfg = _json.dumps({
        "cdn": _CDN, "surah": int(surah), "gstart": int(gstart),
        "n": int(n_ayat), "start": int(start_ayah) if start_ayah else 1,
        "jumped": bool(jumped), "autoplay": bool(autoplay), "baseh": int(base_h),
        "br": {e: br for e, _l, br in RECITERS},
    })
    opts = "".join(f"<option value='{e}'>{lbl}</option>" for e, lbl, _br in RECITERS)
    return """
<style>
 *{box-sizing:border-box;font-family:'Inter',system-ui,sans-serif}
 body{margin:0;color:#10243A;background:transparent}
 .pl{background:#1D3557;border-radius:12px;padding:7px 9px;box-shadow:0 2px 8px rgba(16,36,58,.18)}
 .prow{display:flex;align-items:center;gap:5px}
 .pl button{height:40px;border:none;border-radius:9px;background:#2C4A6E;color:#fff;
   font-size:16px;font-weight:700;cursor:pointer;flex:0 0 auto;padding:0 9px}
 .pl button.pp{background:#1D9E75;font-size:16px;font-weight:800}
 .pl button:active{filter:brightness(.92)}
 #exit{background:#3A5680}
 .pl.open #more{background:#1D9E75}
 .ref{color:#fff;font-weight:800;font-size:14px;min-width:44px;text-align:center;flex:0 0 auto}
 .barwrap{flex:1 1 auto;height:6px;background:#2C4A6E;border-radius:99px;overflow:hidden;min-width:24px}
 #bar{height:100%;width:0;background:#7FD9BD}
 /* options sheet — hidden until ⋯; the iframe self-grows so it is never clipped */
 .sheet{display:none;margin-top:9px;border-top:1px solid #34547A;padding-top:9px}
 .pl.open .sheet{display:block}
 .srow{display:flex;align-items:center;gap:8px;margin:7px 0}
 .lab{color:#fff;font-size:13px;font-weight:700;flex:0 0 90px}
 select{height:40px;border-radius:9px;border:1px solid #2C4A6E;background:#fff;color:#10243A;
   font-size:13px;font-weight:700;padding:2px 6px;flex:1 1 auto;min-width:0}
 .seg{display:flex;align-items:center;gap:6px}
 .seg .val{color:#fff;font-weight:800;font-size:14px;min-width:54px;text-align:center}
 .chips{display:flex;gap:6px;flex-wrap:wrap}
 .chip{height:36px;border:none;border-radius:999px;background:#2C4A6E;color:#fff;
   font-size:13px;font-weight:700;cursor:pointer;padding:0 14px}
 .chip.on{background:#1D9E75}
 .err{color:#FFD7C2;font-size:12px;font-weight:700;margin-left:4px}
 /* EXIT launcher — shown only when recitation is exited */
 .launch{display:none;justify-content:center}
 .pl .ent{background:#1D9E75;font-size:14px;font-weight:800;flex:1 1 auto;max-width:300px}
 .pl.exited .strip{display:none}
 .pl.exited .launch{display:flex}
</style>
<div class="pl" id=pl>
  <div class=launch id=launch><button id=enter class=ent title='start recitation'>🎧 Recite</button></div>
  <div class=strip id=strip>
    <div class=prow>
      <button id=prev title='previous āyah'>⏮</button>
      <button id=pp class=pp title='play'>▶</button>
      <button id=next title='next āyah'>⏭</button>
      <span class=ref id=ref>—</span>
      <div class=barwrap><div id=bar></div></div>
      <button id=more title='options'>⋯</button>
      <button id=exit title='exit recitation'>✕</button>
    </div>
    <div class=sheet id=sheet>
      <div class=srow><span class=lab>Reciter</span><select id=rec>__OPTS__</select></div>
      <div class=srow><span class=lab>Speed</span>
        <div class=seg><button id=spdm>−</button><span class=val id=spdv>1×</span><button id=spdp>+</button></div>
        <span class=err id=err></span>
      </div>
      <div class=srow><span class=lab>Repeat</span>
        <div class=chips id=repc>
          <button class=chip data-r=0>Off</button>
          <button class=chip data-r=1>Āyah</button>
          <button class=chip data-r=2>Sūra</button>
        </div>
      </div>
      <div class=srow><span class=lab>Follow text</span>
        <div class=chips><button class=chip id=fol>On</button></div>
      </div>
    </div>
  </div>
</div>
<audio id=au preload=auto></audio>
<script>
const C = __CFG__;
function $(id){return document.getElementById(id);}
const au=$('au'),ref=$('ref'),pp=$('pp'),bar=$('bar'),err=$('err'),rec=$('rec'),
      more=$('more'),sheet=$('sheet'),pl=$('pl'),spdv=$('spdv'),repc=$('repc'),fol=$('fol');
const SPD=[0.75,1,1.25,1.5,1.75,2];
const LAUNCH_H=50;
let a=C.start, repeat=0, si=1, wantPlay=false, follow=true, sheetOpen=false, exited=false;
function LS(k){try{return localStorage.getItem(k);}catch(e){return null;}}
function setLS(k,v){try{localStorage.setItem(k,v);}catch(e){}}
// SINGLE-INSTANCE GUARD: only the newest player may sound; older instances pause on claim.
var MYID=Math.random().toString(36).slice(2)+Date.now();
function claim(){setLS('qre_owner',MYID);}
function PLAY(){claim();var p=au.play();if(p&&p.catch){p.catch(function(){});}}
window.addEventListener('storage',function(e){if(e.key=='qre_owner'&&e.newValue&&e.newValue!=MYID){try{au.pause();}catch(x){}}});
// restore saved prefs (reciter, speed, repeat, follow, exited)
var _r=LS('qre_reciter');if(_r){for(var i=0;i<rec.options.length;i++){if(rec.options[i].value==_r){rec.value=_r;break;}}}
var _sp=parseFloat(LS('qre_spd'));if(_sp>0){var bi=1,bd=9;for(var i=0;i<SPD.length;i++){var d=Math.abs(SPD[i]-_sp);if(d<bd){bd=d;bi=i;}}si=bi;}
var _rp=LS('qre_rep');if(_rp!=null){repeat=Math.max(0,Math.min(2,+_rp));}
var _fl=LS('qre_follow');if(_fl!=null){follow=(_fl=='1');}
exited=(LS('qre_exited')=='1');
function paintSpeed(){spdv.textContent=SPD[si]+'×';au.playbackRate=SPD[si];}
function paintRep(){var b=repc.querySelectorAll('.chip');for(var i=0;i<b.length;i++){b[i].classList.toggle('on',(+b[i].getAttribute('data-r'))===repeat);}}
function paintFol(){fol.classList.toggle('on',follow);fol.textContent=follow?'On':'Off';}
paintSpeed();paintRep();paintFol();
// resume across reruns (same sūra) unless this is an explicit āyah-jump
var savedSur=+LS('qre_surah'),savedPos=+LS('qre_pos'),savedPlay=(LS('qre_play')=='1');
var sameSurah=(savedSur===C.surah);
if(!C.jumped && sameSurah && savedPos){a=savedPos;}
function persist(){setLS('qre_surah',C.surah);setLS('qre_pos',a);setLS('qre_play',wantPlay?'1':'0');}
function src(n){return C.cdn+'/'+C.br[rec.value]+'/'+rec.value+'/'+(C.gstart+n-1)+'.mp3';}
// resize the iframe itself so launcher / strip / open-sheet are each shown fully (best-effort)
function fit(){try{var fe=window.frameElement;if(fe){
    fe.style.height=(exited?LAUNCH_H:(sheetOpen?(C.baseh+sheet.scrollHeight+12):C.baseh))+'px';}}catch(e){}}
function clearHi(){try{var d=window.parent.document;
    d.querySelectorAll('.rdr details.playing').forEach(function(e){e.classList.remove('playing');});}catch(e){}}
// FOLLOW: highlight + scroll the reader (lives in the MAIN doc) to the playing āyah.
// Instant scroll (NO behavior:'smooth' — cross-frame smooth scrollIntoView is unreliable on
// iOS Safari, which made the page fail to jump). Highlight always; auto-scroll only if follow.
function hi(n){try{var d=window.parent.document;
    d.querySelectorAll('.rdr details.playing').forEach(function(e){e.classList.remove('playing');});
    var el=d.getElementById('qa'+C.surah+'_'+n);
    if(el){el.classList.add('playing');if(follow)el.scrollIntoView({block:'center'});}
  }catch(e){}}
// force an instant jump to āyah n (used by an explicit tap-to-play, regardless of follow)
function gotoAy(n){try{var d=window.parent.document;var el=d.getElementById('qa'+C.surah+'_'+n);
    if(el)el.scrollIntoView({block:'center'});}catch(e){}}
function setExited(v){exited=v;setLS('qre_exited',v?'1':'0');pl.classList.toggle('exited',v);
  if(v){sheetOpen=false;pl.classList.remove('open');}fit();}
function load(n,go){a=Math.max(1,Math.min(C.n,n));ref.textContent=C.surah+':'+a;err.textContent='';
  au.src=src(a);au.playbackRate=SPD[si];hi(a);if(go){wantPlay=true;}persist();if(go){PLAY();}}
function setpp(p){pp.textContent=p?'⏸':'▶';pp.title=p?'pause':'play';}
pp.onclick=function(){if(!au.src)load(a,false);
  if(au.paused){wantPlay=true;persist();PLAY();}else{wantPlay=false;persist();au.pause();}};
$('prev').onclick=function(){load(a-1,true);};
$('next').onclick=function(){load(a+1,true);};
$('spdm').onclick=function(){si=Math.max(0,si-1);paintSpeed();setLS('qre_spd',SPD[si]);};
$('spdp').onclick=function(){si=Math.min(SPD.length-1,si+1);paintSpeed();setLS('qre_spd',SPD[si]);};
repc.onclick=function(e){var t=e.target;if(t&&t.getAttribute('data-r')!=null){repeat=+t.getAttribute('data-r');paintRep();setLS('qre_rep',repeat);}};
fol.onclick=function(){follow=!follow;paintFol();setLS('qre_follow',follow?'1':'0');if(follow)hi(a);};
rec.onchange=function(){setLS('qre_reciter',rec.value);var was=!au.paused;au.src=src(a);au.playbackRate=SPD[si];if(was)PLAY();};
// OPTIONS SHEET
more.onclick=function(){sheetOpen=!sheetOpen;pl.classList.toggle('open',sheetOpen);fit();};
// EXIT recitation → stop, clear highlight, collapse to the 🎧 launcher (reading unobstructed)
$('exit').onclick=function(){wantPlay=false;au.pause();persist();clearHi();setExited(true);};
$('enter').onclick=function(){setExited(false);};
au.onplay=function(){setpp(true);hi(a);};        // scroll to the āyah on EVERY play start
au.onpause=function(){setpp(false);};
au.ontimeupdate=function(){if(au.duration)bar.style.width=(100*au.currentTime/au.duration)+'%';};
au.onerror=function(){err.textContent='unavailable — skipping';if(a<C.n)setTimeout(function(){load(a+1,true);},600);};
au.onended=function(){
  if(repeat==1){au.currentTime=0;PLAY();return;}
  if(a<C.n){load(a+1,true);}
  else if(repeat==2){load(1,true);}
  else{wantPlay=false;persist();setpp(false);bar.style.width='0';}
};
// TAP-TO-PLAY: the reader posts {qre_cmd:'play', a:N}; this also re-enters if exited
window.addEventListener('message',function(e){var d=e.data||{};
  if(d&&d.qre_cmd==='play'&&d.a){
    if(exited)setExited(false);
    if(+d.a===a && !au.paused){wantPlay=false;persist();au.pause();}   // 2nd tap on the playing āyah → stop
    else{load(+d.a,true);gotoAy(+d.a);}                                // else play from there
  }});
pl.classList.toggle('exited',exited);
load(a,false);
// autoplay (e.g. tap-to-play / Search hand-off) overrides an exited state and re-enters;
// otherwise resume where we were (same sūra/jump) — but NOT while exited.
if(C.autoplay){if(exited)setExited(false);wantPlay=true;persist();PLAY();}
else if(!exited && savedPlay && (sameSurah || C.jumped)){wantPlay=true;persist();PLAY();}
fit();
</script>
""".replace("__CFG__", cfg).replace("__OPTS__", opts)


def render(corpus, surah: int, start_ayah: int = 1, jumped: bool = False,
           autoplay: bool = False, height: int = None):
    """Render the slim recitation strip for `surah`, cued to `start_ayah`.
    `jumped` = the āyah was explicitly chosen → cue there; otherwise resume the last
    position so a rerun doesn't stop recitation. `autoplay` = start playing immediately.
    The ⋯ options sheet, follow-scroll, and exit/launcher are handled inside the iframe
    (no Streamlit rerun)."""
    df = corpus.df
    n_ayat = int((df[COL_SURAH].astype(int) == int(surah)).sum())
    gstart = _offsets(corpus).get(int(surah), 1)
    base = 60
    _components.html(
        _player_html(int(surah), gstart, n_ayat, int(start_ayah or 1), bool(jumped),
                     bool(autoplay), base),
        height=(height or base))
