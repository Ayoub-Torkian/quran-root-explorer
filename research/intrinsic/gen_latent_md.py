import json,os
H=os.path.dirname(os.path.abspath(__file__))
L=json.load(open(os.path.join(H,'latent_features.json'),encoding='utf-8'))
PASS=L['review_rubric']['pass']
inc=[f for f in L['features'] if f.get('in_table')]
exc=[f for f in L['features'] if not f.get('in_table')]
o=[]
o.append("# "+L['title']); o.append("")
o.append("> **The one law.** "+L['law']); o.append("")
o.append(f"*Cadence **{L['cadence']}**. Updated {L['last_updated']}; next due {L['next_update_due']}. "
         f"Generated from `latent_features.json`.*"); o.append("")
o.append(f"**{len(inc)} features pass critical review (grade ≥ {PASS}); {len(exc)} excluded.** "
         "Every feature carries a four-question review (what it discovers · category · relations · validity) "
         "plus a plain-English conceptual foundation and utility."); o.append("")
o.append("**Coverage:** "+", ".join(f"{k} {v}" for k,v in L.get('coverage',{}).items())); o.append("")
o.append(f"**Open gap:** {L.get('gaps','')}"); o.append("")
def tbl(rows,hdr):
    out=["| "+" | ".join(hdr)+" |","|"+"|".join("---" for _ in hdr)+"|"]
    for f in rows:
        out.append("| %s | %s | %d | %s | %s | %s |"%(f['id'],f['name'],f['review']['grade'],
                   "/".join(f['dimensions']),f['plain'].replace('|','/'),f['user_value'].replace('|','/')))
    return out
o.append("## Discovery table — passed (≥ %d)"%PASS); o.append("")
o+=tbl(sorted(inc,key=lambda f:-f['review']['grade']),["ID","Feature","Grade","Axes","Plain English","Why it matters"]); o.append("")
o.append("## Supplement — did not pass (< %d)"%PASS); o.append("")
o+=tbl(sorted(exc,key=lambda f:-f['review']['grade']),["ID","Feature","Grade","Axes","Plain English","Why it matters"]); o.append("")
o.append("---"); o.append(""); o.append("## Full critical review per feature"); o.append("")
byid={f['id']:f['name'] for f in L['features']}
for f in sorted(L['features'],key=lambda f:-f['review']['grade']):
    rv=f['review']; mark="✅" if f['in_table'] else "⛔"
    o.append(f"### {f['id']} · {f['name']} — {mark} grade {rv['grade']}/100"); o.append("")
    o.append(f"**Plain English:** {f['plain']}"); o.append("")
    o.append(f"**Conceptual foundation:** {f['conceptual_foundation']}"); o.append("")
    o.append(f"**Utility:** {f['user_value']}"); o.append("")
    gate=("✅ NEW" if rv.get("novelty_pass",True) else "⛔ novelty-gate FAIL")
    o.append(f"- **Q0 new knowledge about the Qur\u2019an ({gate}):** {rv.get('q0_new_knowledge','')}")
    o.append(f"- **Q1 discovers:** {rv['q1_discovers']}")
    o.append(f"- **Q2 category:** {rv['q2_category']}")
    o.append(f"- **Q3 relations:** {rv['q3_relations']}")
    o.append(f"- **Q4 validity:** {rv['q4_validity']}")
    o.append(f"- **Verdict:** {rv['verdict']}")
    o.append(f"- **Measurement:** {f['value']}  ·  **Shuffle floor:** {f['shuffle_floor']}  ·  **Analog:** {f['universe_analog']}")
    o.append(f"- **Related:** "+", ".join(f"{r} ({byid.get(r,'?')})" for r in f['cross_refs'])); o.append("")
open(os.path.join(H,'LATENT_FEATURES.md'),'w',encoding='utf-8').write("\n".join(o))
print("regenerated LATENT_FEATURES.md")
