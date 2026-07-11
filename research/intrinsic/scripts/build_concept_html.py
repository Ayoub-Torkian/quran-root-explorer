# -*- coding: utf-8 -*-
import json
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
DATA=open(R+"/research/intrinsic/anatomy_figs/concept_rearrange_data.json",encoding='utf-8').read()
HTML=r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
 :root{--ink:#10243A;--navy:#1D3557;--green:#1D9E75;--line:#E2E8F1;}
 *{box-sizing:border-box} body{margin:0;font-family:Vazirmatn,'Segoe UI',Tahoma,sans-serif;color:var(--ink);background:#FAFBFD}
 .wrap{max-width:1180px;margin:0 auto;padding:10px 14px}
 .title{font-size:18px;font-weight:800;color:var(--navy)}
 .sub{font-size:13px;color:var(--ink);margin:2px 0 10px}
 .bar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:8px}
 .lens{font-size:13px;font-weight:700;border:1px solid #CFE0F2;background:#fff;color:var(--navy);border-radius:18px;padding:6px 14px;cursor:pointer}
 .lens.on{background:var(--navy);color:#fff;border-color:var(--navy)}
 .badge{font-size:12px;font-weight:700;border-radius:6px;padding:3px 9px;margin-left:auto}
 .b-div{background:#EAF2FB;color:#1D3557;border:1px solid #CFE0F2}
 .b-hum{background:#FBF1E6;color:#8a5a16;border:1px solid #EAD3B6}
 .b-prop{background:#EFF6F2;color:#0F6E56;border:1px solid #CFE4DC}
 .stage{display:flex;gap:12px;flex-wrap:wrap}
 .canvas{flex:1 1 660px;min-width:560px;background:#fff;border:1px solid var(--line);border-radius:12px}
 .panel{flex:1 1 280px;min-width:240px;background:#fff;border:1px solid var(--line);border-radius:12px;padding:12px 14px}
 .cap{font-size:12px;color:var(--ink);margin-top:6px;line-height:1.7}
 .nlab{font-size:13px;font-weight:700}
 .node{cursor:pointer}
 .node text{font-size:13px;font-weight:700;fill:var(--ink);paint-order:stroke;stroke:#fff;stroke-width:3px}
 g.node{transition:transform .85s cubic-bezier(.4,0,.2,1)}
 .pk{font-size:13px} .pk b{color:var(--navy)}
 table{border-collapse:collapse;width:100%;margin-top:6px} td,th{font-size:12px;padding:3px 5px;text-align:right;border-bottom:1px solid #EEF2F7}
 th{color:var(--navy);font-weight:700}
 .hint{font-size:12px;color:var(--ink);opacity:.85}
</style></head><body><div class="wrap">
<div class="title">Concept Rearrangement Explorer — al-Kawthar's words + the inner self</div>
<div class="sub">The same concepts, re-laid under different <b>lenses</b>. Watch which interrelationships appear under each. Edges &amp; positions are <b>measured on the rasm</b>; the layout only organizes known meaning for reading — it is not a claim about the text's order.</div>
<div class="bar">
 <button class="lens on" data-l="meaning">Meaning · co-occurrence</button>
 <button class="lens" data-l="form">Form · edit-distance</button>
 <button class="lens" data-l="rarity">Rarity · frequency</button>
 <span id="badge" class="badge b-div">divine substrate (rasm co-occurrence)</span>
</div>
<div class="stage">
 <svg class="canvas" id="svg" viewBox="0 0 760 520" xmlns="http://www.w3.org/2000/svg"></svg>
 <div class="panel" id="panel"><div class="pk"><b>Click a concept</b> to see how the Qur'an interprets it — its strongest grounded interpreters (root · distinctiveness PPMI · reliability P).</div>
  <div id="detail"></div></div>
</div>
<div class="cap" id="cap"></div>
</div>
<script>
const DATA=__DATA__;
const NODES=DATA.nodes, EDGES=DATA.edges;
const W=760,H=520, X0=70,X1=620, Y0=460,Y1=46;
const svg=document.getElementById('svg');
const px=p=>X0+p[0]*(X1-X0), py=p=>Y0-p[1]*(Y0-Y1);
function r_of(df){return Math.max(8, 7+2.4*Math.sqrt(df));}
let lens='meaning', sel=null;
// edge layer + node layer
const eLayer=document.createElementNS('http://www.w3.org/2000/svg','g'); svg.appendChild(eLayer);
const nLayer=document.createElementNS('http://www.w3.org/2000/svg','g'); svg.appendChild(nLayer);
const gById={};
NODES.forEach((nd,i)=>{
 const g=document.createElementNS('http://www.w3.org/2000/svg','g'); g.setAttribute('class','node'); g.dataset.i=i;
 const c=document.createElementNS('http://www.w3.org/2000/svg','circle'); c.setAttribute('r',r_of(nd.df)); c.setAttribute('fill',nd.color); c.setAttribute('stroke','#fff'); c.setAttribute('stroke-width','2');
 const t=document.createElementNS('http://www.w3.org/2000/svg','text'); t.setAttribute('text-anchor','middle'); t.setAttribute('dy',-r_of(nd.df)-5); t.textContent=nd.label;
 g.appendChild(c); g.appendChild(t); g.onclick=()=>pick(i); nLayer.appendChild(g); gById[i]=g;
});
function place(){NODES.forEach((nd,i)=>{const p=nd.pos[lens]; gById[i].setAttribute('transform',`translate(${px(p)},${py(p)})`);});}
function drawEdges(){
 eLayer.innerHTML='';
 if(lens==='rarity') return;
 const es=EDGES[lens]||[];
 es.forEach(e=>{const a=NODES[e[0]].pos[lens],b=NODES[e[1]].pos[lens];
  const ln=document.createElementNS('http://www.w3.org/2000/svg','line');
  ln.setAttribute('x1',px(a));ln.setAttribute('y1',py(a));ln.setAttribute('x2',px(b));ln.setAttribute('y2',py(b));
  if(lens==='meaning'){ln.setAttribute('stroke','#1D9E75');ln.setAttribute('stroke-width',(0.6+3*e[2]).toFixed(2));ln.setAttribute('opacity','0.5');}
  else{ln.setAttribute('stroke','#EF9F27');ln.setAttribute('stroke-width','2');ln.setAttribute('stroke-dasharray','4 3');}
  eLayer.appendChild(ln);});
}
const BADGE={meaning:['divine substrate (rasm co-occurrence)','b-div'],form:['HUMAN CONSTRUCT (spelling / edit-distance)','b-hum'],rarity:['property (corpus frequency)','b-prop']};
const CAP={
 meaning:"Meaning lens: distance = 1−cosine of whole-corpus co-occurrence. Clusters that emerge are real interpretive company — e.g. <b>کوثر · ربب · صلو</b> (abundance–Lord–prayer). <b>أبتر</b> and <b>نحر</b> drift to the edge: singular, low-shared (the severance isolates even here).",
 form:"Form lens [HUMAN CONSTRUCT]: distance = letter edit-distance of the roots. Only <b>1</b> of 231 pairs is spelling-near — the map scatters, because spelling does not track meaning.",
 rarity:"Rarity lens: ordered by how many verses each root touches (rare → frequent). <b>ربب</b> (871) and <b>کثر</b> (162) are common; <b>نحر · بتر</b> are hapax (1)."
};
function setLens(l){lens=l;document.querySelectorAll('.lens').forEach(b=>b.classList.toggle('on',b.dataset.l===l));
 const bd=document.getElementById('badge');bd.textContent=BADGE[l][0];bd.className='badge '+BADGE[l][1];
 document.getElementById('cap').innerHTML=`Form vs Meaning correlation across all pairs: <b>r = ${DATA.corr_form_meaning}</b> (near 0 — meaning is its own axis, independent of spelling and of canonical position). &nbsp; ${CAP[l]}`;
 place();drawEdges();}
document.querySelectorAll('.lens').forEach(b=>b.onclick=()=>setLens(b.dataset.l));
function pick(i){sel=i;const nd=NODES[i];let h=`<div class="nlab" style="color:${nd.color}">${nd.label}</div>`;
 h+=`<div class="hint">role: ${nd.role} · appears in ${nd.df} verse(s)</div>`;
 if(nd.interp.length){h+=`<table><tr><th>interpreter</th><th>PPMI</th><th>P</th><th>co</th></tr>`;
  nd.interp.forEach(x=>{h+=`<tr><td style="font-weight:700">${x.r}</td><td>${x.ppmi>=0?'+':''}${x.ppmi}</td><td>${x.P}</td><td>${x.co}</td></tr>`;});h+=`</table>`;
  h+=`<div class="hint" style="margin-top:6px">PPMI = distinctiveness; P = reliability (share of this concept's verses the interpreter co-occurs in).</div>`;}
 else h+=`<div class="hint" style="margin-top:8px">Hapax — appears once; defined by its semantic field, not by co-occurrence.</div>`;
 document.getElementById('detail').innerHTML=h;
 NODES.forEach((_,k)=>gById[k].querySelector('circle').setAttribute('stroke',k===i?'#10243A':'#fff'));
}
setLens('meaning');
</script></body></html>"""
HTML=HTML.replace("__DATA__",DATA)
open(R+"/assets/concept_rearrange.html","w",encoding='utf-8').write(HTML)
print("wrote assets/concept_rearrange.html", len(HTML),"bytes")
