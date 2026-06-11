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
HTML = r"""<!doctype html><meta charset=utf-8><title>Correspondence Ledger</title>
<style>
 body{font-family:-apple-system,Segoe UI,Roboto,sans-serif;max-width:1180px;margin:18px auto;color:#16243B;padding:0 16px;background:#fbfbfc}
 h1{font-size:22px;margin:0 0 2px}.sub{color:#46505F;font-size:13.5px;margin:0 0 12px;line-height:1.5}
 h2{font-size:15px;margin:24px 0 10px;color:#1D3557;border-bottom:1px solid #E7ECF3;padding-bottom:4px}
 .metrics{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin:6px 0}
 .m{background:#fff;border:1px solid #E7ECF3;border-radius:11px;padding:11px 8px;text-align:center}
 .m .v{font-size:25px;font-weight:850;color:#1D9E75;line-height:1}.m.grey .v{color:#7f868d}.m.amber .v{color:#E9A23B}
 .m .l{font-size:11px;color:#46505F;margin-top:5px;line-height:1.25}
 .card{border:1px solid #E7ECF3;border-radius:11px;padding:11px 14px;background:#fff;margin:9px 0}
 .card.A{border-left:5px solid #1D9E75}.card.B{border-left:5px solid #7FB069}.card.D{border-left:5px solid #C4CBD3;background:#f7f8f9}
 .ct{font-weight:800;font-size:14px;margin:0 0 2px;display:flex;align-items:center;gap:8px}
 .badge{font-size:11px;font-weight:800;border-radius:20px;padding:1px 8px;margin-left:auto}
 .A .badge{background:#E7F6EF;color:#13592a}.B .badge{background:#EAF2E2;color:#3a5a25}.D .badge{background:#E9EAEC;color:#80858c}
 .look{font-size:13px;color:#46505F;margin:3px 0;line-height:1.45}.look b{color:#1D3557}
 .found{font-size:13px;color:#13592a;margin:3px 0;line-height:1.45}.found b{color:#0B3F2A}
 .rej{font-size:13px;color:#9a4a4a;margin:3px 0;line-height:1.45}
 .stat{font-size:11.5px;color:#5B6675;margin-top:2px}
 .ebar{height:7px;border-radius:4px;background:#EDF1F6;margin:5px 0 1px;overflow:hidden}.ebar i{display:block;height:100%;background:linear-gradient(90deg,#2A9D8F,#1D9E75)}
 .note{background:#FFF8EC;border:1px solid #E7C69F;border-radius:10px;padding:11px 14px;margin:14px 0;font-size:13px;line-height:1.55}
 .cap{font-size:11.5px;color:#7f868d;margin:5px 0 0}
 .col2{display:grid;grid-template-columns:1fr 1fr;gap:9px}
 @media(max-width:720px){.col2{grid-template-columns:1fr}.metrics{grid-template-columns:repeat(2,1fr)}}
</style>
<h1>Correspondence Ledger — the Qur'ān as a designed system</h1>
<p class=sub>The <b>body</b> is the benchmark. For each property a body has, we ask: does the Qur'ān correspond? Each entry shows <b>what we looked for</b> and <b>what we found</b>, measured against the text's own shuffle. Grade <b style="color:#1D9E75">A</b> = survived proper nulls, length de-confounding, <i>and</i> split-half replication.</p>

<div class=metrics>
 <div class=m><div class=v>7</div><div class=l>bedrock (A)</div></div>
 <div class=m><div class=v>34</div><div class=l>attributes tested</div></div>
 <div class=m><div class=v>7</div><div class=l>scrutiny passes</div></div>
 <div class="m amber"><div class=v>z=125</div><div class=l>strongest (propagation)</div></div>
 <div class="m grey"><div class=v>4</div><div class=l>demoted (length)</div></div>
</div>

<h2>The journey — 7 scrutiny passes (where we started → where we are)</h2>
<svg viewBox="0 0 1120 140" xmlns="http://www.w3.org/2000/svg" style="width:100%;background:#fff;border:1px solid #E7ECF3;border-radius:12px" font-family="-apple-system,Segoe UI,Roboto,sans-serif">
 <line x1="70" y1="80" x2="1040" y2="80" stroke="#e2c9a8" stroke-width="3"/>
 <g text-anchor="middle">
  <g><circle cx="70" cy="80" r="8" fill="#9AA4B2"/><text x="70" y="42" font-size="11.5" font-weight="800" fill="#16243B">Build</text><text x="70" y="106" font-size="10" fill="#5B6675">~34 attributes</text></g>
  <g><circle cx="208" cy="80" r="8" fill="#1D9E75"/><text x="208" y="42" font-size="11.5" font-weight="800" fill="#16243B">Nulls</text><text x="208" y="106" font-size="10" fill="#5B6675">proper-null bar</text></g>
  <g><circle cx="346" cy="80" r="8" fill="#C0392B"/><text x="346" y="42" font-size="11.5" font-weight="800" fill="#16243B">Length control</text><text x="346" y="106" font-size="10" fill="#a64141">✗ location killed</text></g>
  <g><circle cx="484" cy="80" r="8" fill="#1D9E75"/><text x="484" y="42" font-size="11.5" font-weight="800" fill="#16243B">Recover</text><text x="484" y="106" font-size="10" fill="#5B6675">circulation·endocrine·flow</text></g>
  <g><circle cx="622" cy="80" r="8" fill="#1D9E75"/><text x="622" y="42" font-size="11.5" font-weight="800" fill="#16243B">Recover</text><text x="622" y="106" font-size="10" fill="#5B6675">necessity·digestive</text></g>
  <g><circle cx="760" cy="80" r="8" fill="#1D9E75"/><text x="760" y="42" font-size="11.5" font-weight="800" fill="#16243B">Bilateral pairs</text><text x="760" y="106" font-size="10" fill="#5B6675">طسم·تبارك twins</text></g>
  <g><circle cx="898" cy="80" r="8" fill="#C0392B"/><text x="898" y="42" font-size="11.5" font-weight="800" fill="#16243B">Split-half</text><text x="898" y="106" font-size="10" fill="#a64141">✗ skeleton demoted</text></g>
  <g><text x="1040" y="68" font-size="20" fill="#E9A23B">★</text><text x="1040" y="42" font-size="11.5" font-weight="800" fill="#E9A23B">NOW</text><text x="1040" y="106" font-size="10" fill="#8a5200">7 bedrock core</text></g>
 </g>
</svg>

<h2>The correspondence map (the 7 bedrock, on the body)</h2>
<svg viewBox="0 0 1120 430" xmlns="http://www.w3.org/2000/svg" style="width:100%;background:#fff;border:1px solid #E7ECF3;border-radius:12px" font-family="-apple-system,Segoe UI,Roboto,sans-serif">
 <g fill="#eef3ee" stroke="#a9c7b3" stroke-width="2">
  <circle cx="560" cy="70" r="34"/>
  <path d="M522,112 C522,106 598,106 598,112 L594,286 C594,300 526,300 526,286 Z"/>
  <line x1="530" y1="128" x2="474" y2="240" stroke-width="19" stroke-linecap="round"/>
  <line x1="590" y1="128" x2="646" y2="240" stroke-width="19" stroke-linecap="round"/>
  <line x1="540" y1="292" x2="532" y2="392" stroke-width="21" stroke-linecap="round"/>
  <line x1="580" y1="292" x2="588" y2="392" stroke-width="21" stroke-linecap="round"/>
 </g>
 <circle cx="549" cy="64" r="4.5" fill="#1D9E75"/><circle cx="571" cy="64" r="4.5" fill="#1D9E75"/>
 <circle cx="545" cy="172" r="8" fill="#C0392B"/>
 <line x1="560" y1="112" x2="560" y2="286" stroke="#7d9cc0" stroke-width="2" stroke-dasharray="3 4"/>
 <circle cx="536" cy="232" r="6" fill="#b5651d"/><circle cx="584" cy="232" r="6" fill="#b5651d"/>
 <g fill="#2f8f57"><circle cx="566" cy="200" r="3"/><circle cx="575" cy="207" r="3"/><circle cx="558" cy="210" r="3"/></g>
 <g font-size="12.5" fill="#16243B">
  <line x1="252" y1="66" x2="526" y2="160" stroke="#cfd6dc"/><rect x="22" y="48" width="230" height="38" rx="8" fill="#f4faf6" stroke="#1D9E75"/><text x="34" y="65" font-weight="800">A5 · Rhythm 🫀</text><text x="34" y="80" font-size="10.5" fill="#5B6675">1/f pulse · z=+20</text>
  <line x1="252" y1="168" x2="524" y2="200" stroke="#cfd6dc"/><rect x="22" y="150" width="230" height="38" rx="8" fill="#f4faf6" stroke="#1D9E75"/><text x="34" y="167" font-weight="800">A2 · Internal weave 🧶</text><text x="34" y="182" font-size="10.5" fill="#5B6675">t=10.9</text>
  <line x1="252" y1="262" x2="526" y2="232" stroke="#cfd6dc"/><rect x="22" y="244" width="230" height="38" rx="8" fill="#f4faf6" stroke="#1D9E75"/><text x="34" y="261" font-weight="800">A1 · Membrane 🧫</text><text x="34" y="276" font-size="10.5" fill="#5B6675">seam · z=−5</text>
  <line x1="252" y1="356" x2="476" y2="240" stroke="#cfd6dc"/><rect x="22" y="338" width="230" height="38" rx="8" fill="#f4faf6" stroke="#1D9E75"/><text x="34" y="355" font-weight="800">A3 · Propagation 🔁</text><text x="34" y="370" font-size="10.5" fill="#5B6675">formulae · z=+125</text>
  <line x1="868" y1="66" x2="584" y2="64" stroke="#cfd6dc"/><rect x="866" y="48" width="232" height="38" rx="8" fill="#f4faf6" stroke="#1D9E75"/><text x="878" y="65" font-weight="800">A4 · Interface-zones 🛂</text><text x="878" y="80" font-size="10.5" fill="#5B6675">clustered · z=+17.6</text>
  <line x1="868" y1="168" x2="560" y2="200" stroke="#cfd6dc"/><rect x="866" y="150" width="232" height="38" rx="8" fill="#f4faf6" stroke="#1D9E75"/><text x="878" y="167" font-weight="800">A6 · Connectivity 🔗</text><text x="878" y="182" font-size="10.5" fill="#5B6675">44% pairs</text>
  <line x1="868" y1="244" x2="586" y2="234" stroke="#cfd6dc"/><rect x="866" y="226" width="232" height="38" rx="8" fill="#f4faf6" stroke="#1D9E75"/><text x="878" y="243" font-weight="800">A7 · Bilateral pairs 👀</text><text x="878" y="258" font-size="10.5" fill="#5B6675">طسم 26·28 · z=+5.4</text>
 </g>
</svg>
<p class=cap>Green dots = the seven bedrock correspondences, mapped to the body (eyes, heart, spine, cells, skin).</p>

<h2>Bedrock — what we looked for, what we found (grade A)</h2>
<div class=col2>
 <div class="card A"><p class=ct>A1 · Membrane <span class=badge>A</span></p><p class=look><b>Looked for:</b> a real edge to each sūra — a membrane that seals it off from its neighbours.</p><p class=found><b>Found:</b> root-overlap collapses at the seam.</p><div class=ebar><i style="width:60%"></i></div><p class=stat>0.28 vs 0.87 expected · z=−5 · vs random adjacency</p></div>
 <div class="card A"><p class=ct>A2 · Internal weave <span class=badge>A</span></p><p class=look><b>Looked for:</b> whether a sūra is woven tissue (ordered) or a loose pile of verses.</p><p class=found><b>Found:</b> verses are chained beyond their shared vocabulary.</p><div class=ebar><i style="width:78%"></i></div><p class=stat>t=10.9 · vs the sūra's own verse-order shuffle</p></div>
 <div class="card A"><p class=ct>A3 · Propagation <span class=badge>A</span></p><p class=look><b>Looked for:</b> self-replication — does the text copy its own forms, like cells copying code?</p><p class=found><b>Found:</b> fixed formulae repeat and reach every region.</p><div class=ebar><i style="width:100%"></i></div><p class=stat>z=+125 · max dry-gap 93 / 51,024 tokens · vs shuffle</p></div>
 <div class="card A"><p class=ct>A4 · Interface-zones <span class=badge>A</span></p><p class=look><b>Looked for:</b> an outward-facing surface (sense organs / skin) — and whether it is localized.</p><p class=found><b>Found:</b> outward address (28% of verses) clusters into patches.</p><div class=ebar><i style="width:85%"></i></div><p class=stat>z=+17.6 · vs label shuffle</p></div>
 <div class="card A"><p class=ct>A5 · Rhythm / pulse <span class=badge>A</span></p><p class=look><b>Looked for:</b> a pulse across many scales at once, like a heartbeat.</p><p class=found><b>Found:</b> verse-length long memory; information delivered smoothly.</p><div class=ebar><i style="width:88%"></i></div><p class=stat>DFA 0.95, 1/f · flow z=+20 · vs shuffle</p></div>
 <div class="card A"><p class=ct>A6 · Connectivity <span class=badge>A</span></p><p class=look><b>Looked for:</b> specific wiring between sūras, like vessels between organs.</p><p class=found><b>Found:</b> specific pairs linked; twins survive length control.</p><div class=ebar><i style="width:70%"></i></div><p class=stat>44% of pairs significant · vs degree-preserving null</p></div>
 <div class="card A"><p class=ct>A7 · Bilateral pairs <span class=badge>A</span></p><p class=look><b>Looked for:</b> matched identical pairs, like two eyes or two ears.</p><p class=found><b>Found:</b> form-twin sūras sharing an opening template — طسم 26·28, تبارك 25·67, والسماء 85·86.</p><div class=ebar><i style="width:62%"></i></div><p class=stat>z=+5.4 · on the length-residual</p></div>
</div>

<h2>Second tier — real but modest (grade B)</h2>
<div class=col2>
 <div class="card B"><p class=ct>Identity <span class=badge>B</span></p><p class=look><b>Looked for:</b> a unique function per sūra — no two organs do the same job.</p><p class=found><b>Found:</b> a held-out verse traces to its home sūra. <span class=stat>7.2% vs 4.9% arbitrary (z≈7.7)</span></p></div>
 <div class="card B"><p class=ct>Necessity <span class=badge>B</span></p><p class=look><b>Looked for:</b> irreplaceability — remove an organ and the body loses a function.</p><p class=found><b>Found:</b> Fātiḥa is the most isolated sūra in function space. <span class=stat>rank 1/114</span></p></div>
 <div class="card B"><p class=ct>Digestive loop <span class=badge>B</span></p><p class=look><b>Looked for:</b> intake → processing → output (ingest a claim, respond to it).</p><p class=found><b>Found:</b> "ask" (سءل) is followed by "say" (قل) within 2 verses. <span class=stat>25% vs 4% base</span></p></div>
 <div class="card B"><p class=ct>Polarity <span class=badge>B</span></p><p class=look><b>Looked for:</b> a head–tail axis (anterior-posterior differentiation).</p><p class=found><b>Found:</b> a marked head, a faint tail (asymmetric). <span class=stat>head AUC 0.75 / tail 0.61</span></p></div>
 <div class="card B"><p class=ct>Error-correction <span class=badge>B</span></p><p class=look><b>Looked for:</b> redundancy that lets a damaged part be repaired.</p><p class=found><b>Found:</b> endings recoverable from the rhyme code. <span class=stat>73% vs 50%</span></p></div>
 <div class="card B"><p class=ct>Signal propagation <span class=badge>B</span></p><p class=look><b>Looked for:</b> content carrying from one verse to the next (a nervous signal).</p><p class=found><b>Found:</b> adjacent verses share content far above chance. <span class=stat>0.087 vs 0.009</span></p></div>
</div>

<h2>Tested &amp; rejected — what we looked for, why it failed (OUT)</h2>
<div class=col2>
 <div class="card D"><p class=ct>Location <span class=badge>OUT</span></p><p class=look><b>Looked for:</b> a fixed position per sūra, like the heart fixed in the chest.</p><p class=rej><b>Rejected:</b> position is just the muṣḥaf's long→short ordering — once length is removed, nothing's left (residual R²=0.03).</p></div>
 <div class="card D"><p class=ct>Folding contact-decay <span class=badge>OUT</span></p><p class=look><b>Looked for:</b> the linear text folding into a network with a contact-decay curve, like the genome (Hi-C).</p><p class=rej><b>Rejected:</b> the decay was a length artifact (residual r=−0.04). The network itself survives via Connectivity (A6).</p></div>
 <div class="card D"><p class=ct>Development <span class=badge>OUT</span></p><p class=look><b>Looked for:</b> developmental classes (ontogeny — early vs late forms).</p><p class=rej><b>Rejected:</b> the two "classes" are just the length gradient again.</p></div>
 <div class="card D"><p class=ct>Skeleton (muqaṭṭaʿāt) <span class=badge>OUT</span></p><p class=look><b>Looked for:</b> a structural frame — the disjoint-letter sūras as a skeleton.</p><p class=rej><b>Rejected:</b> strong in odd sūras (t=10.3) but failed split-half replication (t=1.7 in even).</p></div>
 <div class="card D"><p class=ct>Circulation (substance) <span class=badge>OUT</span></p><p class=look><b>Looked for:</b> a circulating substance reaching every region, like blood.</p><p class=rej><b>Rejected:</b> the core message clumps (no perfusion). The real "flow" is the recitation itself (= Rhythm + Propagation).</p></div>
 <div class="card D"><p class=ct>Respiratory · excretory · lymphatic <span class=badge>weak</span></p><p class=look><b>Looked for:</b> exchange with the environment · expulsion of error (كلا "Nay!") · pervasive connective tissue.</p><p class=rej><b>Result:</b> present but generic or tiny — kept honestly as weak, not bedrock.</p></div>
</div>

<div class=note><b>What we did not know before:</b> the matched <b>bilateral form-twins</b> (A7), the <b>zoned</b> external interface (A4), <b>Fātiḥa</b> as the most-irreplaceable sūra, and the <b>ask→say</b> loop. And the honest negatives — location is just length-ordering; there is no circulating substance; the folding-curve was a length artifact. The headline is the <b>synthesis</b>: scattered, separately-known measures cohere as one designed-system signature, with a 7-property form-level core that survives the hardest scrutiny.</div>
<p class=cap>Method (locked): body = benchmark, one-directional · PROVEN needs a proper null + honest effect + reproducible script · all-or-none (refine the instrument, never "void") · re-sort/relabel by grade each pass. Full ledger &amp; scripts: research/correspondence/.</p>
"""
components.html(HTML, height=3200, scrolling=True)
