import streamlit as st
import streamlit.components.v1 as components
try:
    import state as S
except Exception:
    S = None
st.set_page_config(page_title="Correspondence Ledger", page_icon="🫀", layout="wide")
if S:
    try:
        S.log_page("correspondence")
    except Exception:
        pass
    for fn in ("inject_css", "render_grouped_nav"):
        try:
            getattr(S, fn)()
        except Exception:
            pass
HTML = r"""<!doctype html><meta charset=utf-8><title>Body ↔ Qur'ān — Correspondence Ledger</title>
<style>
 body{font-family:-apple-system,Segoe UI,Roboto,sans-serif;max-width:1180px;margin:20px auto;color:#1d1d1f;padding:0 16px;background:#fbfbfc}
 h1{font-size:22px;margin:0 0 2px}.sub{color:#666;font-size:13.5px;margin:0 0 4px;line-height:1.5}
 .path{color:#a64f12;font-size:12px;margin:0 0 14px}
 h2{font-size:15px;margin:26px 0 10px;color:#333;border-bottom:1px solid #e7e7ea;padding-bottom:4px}
 .metrics{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin:6px 0 4px}
 .m{background:#fff;border:1px solid #e2e6ea;border-radius:11px;padding:11px 8px;text-align:center}
 .m .v{font-size:26px;font-weight:850;color:#1b7837;line-height:1} .m.grey .v{color:#7f868d} .m.amber .v{color:#a64f12}
 .m .l{font-size:11px;color:#666;margin-top:5px;line-height:1.25}
 table{border-collapse:collapse;width:100%;font-size:12.4px;background:#fff;border:1px solid #e2e6ea;border-radius:10px;overflow:hidden}
 th{background:#f3f5f7;text-align:left;padding:7px 9px;font-size:11.5px;color:#555;border-bottom:1px solid #e2e6ea}
 td{padding:7px 9px;border-bottom:1px solid #eef0f2;vertical-align:top}
 tr.A td:first-child{border-left:4px solid #1b7837} tr.B td:first-child{border-left:4px solid #6aa84f} tr.D td:first-child{border-left:4px solid #c9ccd1}
 tr.D{color:#8a8f96;background:#fafafb}
 .g{font-weight:800;font-size:11px;border-radius:20px;padding:1px 8px} .gA{background:#d7ece0;color:#13592a} .gB{background:#e6efdc;color:#3a5a25} .gD{background:#e9eaec;color:#80858c}
 .q{color:#13592a} .new{background:#fff0d9;color:#a64f12;font-size:9.5px;font-weight:800;border-radius:4px;padding:1px 4px;margin-left:4px}
 .note{background:#fff4e9;border:1px solid #e7c69f;border-radius:10px;padding:12px 15px;margin:16px 0;font-size:13px;line-height:1.55}
 .cap{font-size:11.5px;color:#888;margin:4px 0 0}
</style>
<h1>The Qur'ān as a designed system — Body ↔ Qur'ān correspondence ledger</h1>
<p class=sub>Body = benchmark; we test the Qur'ān against it, intrinsically (the text's own shuffle as null). Grade <b style="color:#1b7837">A</b> = survived proper nulls, length de-confounding, <i>and</i> split-half replication.</p>
<p class=path>⏱ 7 scrutiny passes · nulls + length-control + odd/even split-half · ~34 attributes tested</p>

<div class=metrics>
 <div class=m><div class=v>7</div><div class=l>bedrock correspondences (A)</div></div>
 <div class=m><div class=v>34</div><div class=l>attributes tested</div></div>
 <div class=m><div class=v>7</div><div class=l>scrutiny passes</div></div>
 <div class="m amber"><div class=v>z=125</div><div class=l>strongest effect (propagation)</div></div>
 <div class="m grey"><div class=v>4</div><div class=l>demoted — length artifacts</div></div>
</div>

<h2>The journey — 7 scrutiny passes (where we started → where we are)</h2>
<svg viewBox="0 0 1120 140" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Roboto,sans-serif" style="width:100%;background:#fff;border:1px solid #e2e6ea;border-radius:12px">
 <line x1="70" y1="80" x2="1040" y2="80" stroke="#e2c9a8" stroke-width="3"/>
 <g text-anchor="middle">
  <g><circle cx="70" cy="80" r="8" fill="#9aa0a6"/><text x="70" y="42" font-size="11.5" font-weight="800" fill="#333">Build</text><text x="70" y="106" font-size="10" fill="#666">~34 attributes</text></g>
  <g><circle cx="208" cy="80" r="8" fill="#1b7837"/><text x="208" y="42" font-size="11.5" font-weight="800" fill="#333">Nulls</text><text x="208" y="106" font-size="10" fill="#666">proper-null bar</text></g>
  <g><circle cx="346" cy="80" r="8" fill="#c0392b"/><text x="346" y="42" font-size="11.5" font-weight="800" fill="#333">Length control</text><text x="346" y="106" font-size="10" fill="#a64141">✗ location killed</text></g>
  <g><circle cx="484" cy="80" r="8" fill="#1b7837"/><text x="484" y="42" font-size="11.5" font-weight="800" fill="#333">Recover</text><text x="484" y="106" font-size="10" fill="#666">circulation·endocrine·flow</text></g>
  <g><circle cx="622" cy="80" r="8" fill="#1b7837"/><text x="622" y="42" font-size="11.5" font-weight="800" fill="#333">Recover</text><text x="622" y="106" font-size="10" fill="#666">necessity·digestive</text></g>
  <g><circle cx="760" cy="80" r="8" fill="#1b7837"/><text x="760" y="42" font-size="11.5" font-weight="800" fill="#333">Bilateral pairs</text><text x="760" y="106" font-size="10" fill="#666">طسم·تبارك twins</text></g>
  <g><circle cx="898" cy="80" r="8" fill="#c0392b"/><text x="898" y="42" font-size="11.5" font-weight="800" fill="#333">Split-half</text><text x="898" y="106" font-size="10" fill="#a64141">✗ skeleton demoted</text></g>
  <g><text x="1040" y="68" font-size="20" fill="#a64f12">★</text><text x="1040" y="42" font-size="11.5" font-weight="800" fill="#a64f12">NOW</text><text x="1040" y="106" font-size="10" fill="#8a5200">7 bedrock core</text></g>
 </g>
</svg>

<h2>The correspondence map</h2>
<svg viewBox="0 0 1120 470" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Roboto,sans-serif" style="width:100%;background:#fff;border:1px solid #e2e6ea;border-radius:12px">
 <!-- body silhouette -->
 <g fill="#eef3ee" stroke="#a9c7b3" stroke-width="2">
  <circle cx="560" cy="74" r="36"/>
  <path d="M520,118 C520,112 600,112 600,118 L596,300 C596,316 524,316 524,300 Z"/>
  <line x1="528" y1="135" x2="468" y2="255" stroke-width="20" stroke-linecap="round"/>
  <line x1="592" y1="135" x2="652" y2="255" stroke-width="20" stroke-linecap="round"/>
  <line x1="540" y1="308" x2="530" y2="455" stroke-width="22" stroke-linecap="round"/>
  <line x1="580" y1="308" x2="590" y2="455" stroke-width="22" stroke-linecap="round"/>
 </g>
 <!-- organ markers -->
 <circle cx="548" cy="68" r="4.5" fill="#1b7837"/><circle cx="572" cy="68" r="4.5" fill="#1b7837"/>
 <circle cx="544" cy="186" r="9" fill="#c0392b"/>
 <line x1="560" y1="120" x2="560" y2="300" stroke="#7d9cc0" stroke-width="2" stroke-dasharray="3 4"/>
 <circle cx="535" cy="250" r="6" fill="#b5651d"/><circle cx="585" cy="250" r="6" fill="#b5651d"/>
 <g fill="#2f8f57"><circle cx="566" cy="215" r="3"/><circle cx="575" cy="222" r="3"/><circle cx="558" cy="225" r="3"/><circle cx="572" cy="210" r="3"/></g>
 <!-- leader lines + callouts -->
 <g font-size="12.5" fill="#222">
  <!-- left -->
  <line x1="250" y1="70" x2="528" y2="160" stroke="#cfd6dc"/><rect x="20" y="52" width="232" height="40" rx="8" fill="#f4faf6" stroke="#1b7837"/><text x="32" y="70" font-weight="800">A5 · Rhythm / pulse 🫀</text><text x="32" y="86" font-size="11" fill="#555">verse-length 1/f, DFA 0.95; flow z=+20</text>
  <line x1="252" y1="170" x2="524" y2="210" stroke="#cfd6dc"/><rect x="20" y="152" width="232" height="40" rx="8" fill="#f4faf6" stroke="#1b7837"/><text x="32" y="170" font-weight="800">A2 · Internal weave 🧶</text><text x="32" y="186" font-size="11" fill="#555">verses chained in order, t=10.9</text>
  <line x1="252" y1="270" x2="524" y2="250" stroke="#cfd6dc"/><rect x="20" y="252" width="232" height="40" rx="8" fill="#f4faf6" stroke="#1b7837"/><text x="32" y="270" font-weight="800">A1 · Membrane 🧫</text><text x="32" y="286" font-size="11" fill="#555">overlap collapses at seam, z=−5</text>
  <line x1="250" y1="370" x2="470" y2="255" stroke="#cfd6dc"/><rect x="20" y="352" width="232" height="40" rx="8" fill="#f4faf6" stroke="#1b7837"/><text x="32" y="370" font-weight="800">A3 · Propagation 🔁</text><text x="32" y="386" font-size="11" fill="#555">self-copying formulae, z=+125</text>
  <!-- right -->
  <line x1="870" y1="70" x2="584" y2="68" stroke="#cfd6dc"/><rect x="868" y="52" width="234" height="40" rx="8" fill="#f4faf6" stroke="#1b7837"/><text x="880" y="70" font-weight="800">A4 · Interface-zones 🛂</text><text x="880" y="86" font-size="11" fill="#555">outward address clusters, z=+17.6</text>
  <line x1="870" y1="170" x2="560" y2="210" stroke="#cfd6dc"/><rect x="868" y="152" width="234" height="40" rx="8" fill="#f4faf6" stroke="#1b7837"/><text x="880" y="170" font-weight="800">A6 · Connectivity 🔗</text><text x="880" y="186" font-size="11" fill="#555">44% sūra-pairs wired (length-robust)</text>
  <line x1="870" y1="262" x2="588" y2="252" stroke="#cfd6dc"/><rect x="868" y="244" width="234" height="40" rx="8" fill="#f4faf6" stroke="#1b7837"/><text x="880" y="262" font-weight="800">A7 · Bilateral pairs 👀</text><text x="880" y="278" font-size="11" fill="#555">matched twin sūras (طسم 26·28 …)</text>
 </g>
 <text x="560" y="455" text-anchor="middle" font-size="11" fill="#9aa">green dots = the seven bedrock correspondences mapped to the body</text>
</svg>

<h2>Effect sizes — what is strong, what is not</h2>
<svg viewBox="0 0 1120 360" xmlns="http://www.w3.org/2000/svg" font-family="-apple-system,Segoe UI,Roboto,sans-serif" style="width:100%;background:#fff;border:1px solid #e2e6ea;border-radius:12px">
 <text x="20" y="26" font-size="12" fill="#777">bar ∝ log effect (z or t). green = bedrock · light = B · grey = demoted/failed</text>
 <!-- bars: name, value-label, logwidth(0..1), color -->
 <g font-size="12.5">
  <!-- helper: x start 250, max width 800 -->
  <g><text x="240" y="58" text-anchor="end" font-weight="700">Propagation A3</text><rect x="250" y="46" width="800" height="16" rx="3" fill="#1b7837"/><text x="1058" y="58" font-size="11" fill="#444">z=125</text></g>
  <g><text x="240" y="84" text-anchor="end" font-weight="700">Interface-zones A4</text><rect x="250" y="72" width="560" height="16" rx="3" fill="#1b7837"/><text x="818" y="84" font-size="11" fill="#444">z=17.6</text></g>
  <g><text x="240" y="110" text-anchor="end" font-weight="700">Internal weave A2</text><rect x="250" y="98" width="500" height="16" rx="3" fill="#1b7837"/><text x="758" y="110" font-size="11" fill="#444">t=10.9</text></g>
  <g><text x="240" y="136" text-anchor="end" font-weight="700">Rhythm A5</text><rect x="250" y="124" width="540" height="16" rx="3" fill="#1b7837"/><text x="798" y="136" font-size="11" fill="#444">z≈20</text></g>
  <g><text x="240" y="162" text-anchor="end" font-weight="700">Identity (B)</text><rect x="250" y="150" width="430" height="16" rx="3" fill="#6aa84f"/><text x="688" y="162" font-size="11" fill="#444">z=7.7</text></g>
  <g><text x="240" y="188" text-anchor="end" font-weight="700">Connectivity A6</text><rect x="250" y="176" width="430" height="16" rx="3" fill="#1b7837"/><text x="688" y="188" font-size="11" fill="#444">z≈8</text></g>
  <g><text x="240" y="214" text-anchor="end" font-weight="700">Bilateral pairs A7</text><rect x="250" y="202" width="370" height="16" rx="3" fill="#1b7837"/><text x="628" y="214" font-size="11" fill="#444">z=5.4</text></g>
  <g><text x="240" y="240" text-anchor="end" font-weight="700">Membrane A1</text><rect x="250" y="228" width="350" height="16" rx="3" fill="#1b7837"/><text x="608" y="240" font-size="11" fill="#444">z=5</text></g>
  <g><text x="240" y="266" text-anchor="end" font-weight="700">Skeleton (demoted)</text><rect x="250" y="254" width="120" height="16" rx="3" fill="#c9ccd1"/><text x="378" y="266" font-size="11" fill="#888">t=1.7 even-half</text></g>
  <g><text x="240" y="292" text-anchor="end" font-weight="700">Location (demoted)</text><rect x="250" y="280" width="20" height="16" rx="3" fill="#c9ccd1"/><text x="278" y="292" font-size="11" fill="#888">resid R²=0.03</text></g>
  <g><text x="240" y="318" text-anchor="end" font-weight="700">Folding-decay (demoted)</text><rect x="250" y="306" width="14" height="16" rx="3" fill="#c9ccd1"/><text x="272" y="318" font-size="11" fill="#888">r=−0.04</text></g>
 </g>
</svg>
<p class=cap>The demoted bars are near-zero on purpose — once length is controlled, "location" and "folding-decay" essentially vanish.</p>

<h2>Full ledger — including the tested-and-rejected</h2>
<table>
<tr><th>Attribute</th><th>Body</th><th>Qur'ān finding</th><th>Stat / null</th><th>Grade</th></tr>
<tr class=A><td><b>A1 Membrane</b></td><td>organ sealed by a membrane</td><td class=q>overlap collapses at the sūra seam</td><td>0.28 vs 0.87 (z=−5)</td><td><span class="g gA">A</span></td></tr>
<tr class=A><td><b>A2 Internal weave</b></td><td>tissue fibres in order</td><td class=q>verses chained beyond vocabulary</td><td>t=10.9 vs own shuffle</td><td><span class="g gA">A</span></td></tr>
<tr class=A><td><b>A3 Propagation</b></td><td>self-replicating code</td><td class=q>formulae repeat &amp; perfuse all regions</td><td>z=+125</td><td><span class="g gA">A</span></td></tr>
<tr class=A><td><b>A4 Interface-zones</b><span class=new>NEW</span></td><td>sense organs at the surface</td><td class=q>outward address clusters in patches</td><td>z=+17.6</td><td><span class="g gA">A</span></td></tr>
<tr class=A><td><b>A5 Rhythm / pulse</b></td><td>heartbeat, 1/f</td><td class=q>verse-length long memory; flow regulated</td><td>DFA 0.95; z=+20</td><td><span class="g gA">A</span></td></tr>
<tr class=A><td><b>A6 Connectivity</b></td><td>organ↔organ wiring</td><td class=q>specific sūra-pairs; twins survive length</td><td>44% vs 1%</td><td><span class="g gA">A</span></td></tr>
<tr class=A><td><b>A7 Bilateral pairs</b><span class=new>NEW</span></td><td>two eyes, two ears — the same</td><td class=q>matched form-twins طسم 26·28, تبارك 25·67…</td><td>z=+5.4 (length-resid)</td><td><span class="g gA">A</span></td></tr>
<tr class=B><td>Identity</td><td>unique organ function</td><td class=q>verse→home-sūra recognizable</td><td>7.2% vs 4.9% (z≈7.7)</td><td><span class="g gB">B</span></td></tr>
<tr class=B><td>Necessity<span class=new>NEW</span></td><td>remove organ → body fails</td><td class=q>Fātiḥa most-isolated in function space</td><td>rank 1/114</td><td><span class="g gB">B</span></td></tr>
<tr class=B><td>Digestive loop<span class=new>NEW</span></td><td>ingest → process → output</td><td class=q>"ask" سءل → "say" قل within 2 verses</td><td>25% vs 4%</td><td><span class="g gB">B</span></td></tr>
<tr class=B><td>Polarity (head≫tail)</td><td>anterior-posterior axis</td><td class=q>marked head, faint tail</td><td>AUC 0.75 / 0.61</td><td><span class="g gB">B</span></td></tr>
<tr class=B><td>Error-correction</td><td>redundancy / repair</td><td class=q>endings recoverable from rhyme code</td><td>73% vs 50%</td><td><span class="g gB">B</span></td></tr>
<tr class=D><td>Circulation / endocrine / flow-dir</td><td>transport, slow modulation, arrow</td><td>present, but = the rhythm/formulae signals</td><td>recovered, redundant</td><td><span class="g gD">≈A3/A5</span></td></tr>
<tr class=D><td>Location</td><td>fixed organ position</td><td>just the muṣḥaf long→short ordering</td><td>resid R²=0.03</td><td><span class="g gD">OUT</span></td></tr>
<tr class=D><td>Folding contact-decay</td><td>genome-like folding curve</td><td>a length artifact (network survives via A6)</td><td>r=−0.04</td><td><span class="g gD">OUT</span></td></tr>
<tr class=D><td>Development two-classes</td><td>ontogeny</td><td>the length gradient again</td><td>—</td><td><span class="g gD">OUT</span></td></tr>
<tr class=D><td>Skeleton (muqaṭṭaʿāt)</td><td>structural frame</td><td>fails split-half replication</td><td>t=10.3 odd / 1.7 even</td><td><span class="g gD">OUT</span></td></tr>
<tr class=D><td>Respiratory · excretory · lymphatic</td><td>exchange · expel · drain</td><td>present but generic/tiny (كلا×38; 15% particles)</td><td>weak</td><td><span class="g gD">weak</span></td></tr>
</table>

<div class=note><b>What we did NOT know before:</b> the <b>bilateral form-twin pairs</b> (A7, objective criterion), the <b>zoned external interface</b> (A4), <b>Fātiḥa</b> as the functionally most-irreplaceable sūra, and the <b>ask→say digestive loop</b>. Plus the honest negatives — sūra <b>location is just length-ordering</b>, there is <b>no circulating substance</b>, and the folding-curve was a length artifact. The headline is the <b>synthesis</b>: scattered, separately-known measures cohere as one designed-system signature, of which a 7-property form-level core survives the hardest scrutiny.</div>
<p class=cap>Method (locked): body = benchmark, one-directional · PROVEN needs proper null + honest effect + reproducible script · all-or-none (refine, never "void") · re-sort/relabel by grade each pass. Ledger + scripts: <code>research/correspondence/</code>.</p>
"""
components.html(HTML, height=3200, scrolling=True)
