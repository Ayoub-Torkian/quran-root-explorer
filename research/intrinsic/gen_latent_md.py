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
def _g(f): return f.get('review',{}).get('grade',0)
def tbl(rows,hdr):
    out=["| "+" | ".join(hdr)+" |","|"+"|".join("---" for _ in hdr)+"|"]
    for f in rows:
        out.append("| %s | %s | %d | %s | %s | %s |"%(f['id'],f['name'],_g(f),
                   "/".join(f.get('dimensions',[])),f.get('plain','').replace('|','/'),f.get('user_value','').replace('|','/')))
    return out
o.append("## Discovery table — passed (≥ %d)"%PASS); o.append("")
o+=tbl(sorted(inc,key=lambda f:-_g(f)),["ID","Feature","Grade","Axes","Plain English","Why it matters"]); o.append("")
o.append("## Supplement — did not pass (< %d)"%PASS); o.append("")
o+=tbl(sorted(exc,key=lambda f:-_g(f)),["ID","Feature","Grade","Axes","Plain English","Why it matters"]); o.append("")
o.append("---"); o.append(""); o.append("## Full critical review per feature"); o.append("")
byid={f['id']:f['name'] for f in L['features']}
for f in sorted(L['features'],key=lambda f:-_g(f)):
    rv=f.get('review',{}); mark="✅" if f.get('in_table') else "⛔"
    o.append(f"### {f['id']} · {f['name']} — {mark} grade {_g(f)}/100"); o.append("")
    o.append(f"**Plain English:** {f.get('plain','')}"); o.append("")
    o.append(f"**Conceptual foundation:** {f.get('conceptual_foundation','')}"); o.append("")
    o.append(f"**Utility:** {f.get('user_value','')}"); o.append("")
    gate=("✅ NEW" if rv.get("novelty_pass",True) else "⛔ novelty-gate FAIL")
    o.append(f"- **Q0 new knowledge about the Qur’an ({gate}):** {rv.get('q0_new_knowledge','')}")
    o.append(f"- **Q1 discovers:** {rv.get('q1_discovers','')}")
    o.append(f"- **Q2 category:** {rv.get('q2_category','')}")
    o.append(f"- **Q3 relations:** {rv.get('q3_relations','')}")
    _val = rv.get('q4_validity') or rv.get('q4_arrangement_control') or ''
    if _val:
        o.append(f"- **Q4 validity:** {_val}")
    if rv.get('verdict'):
        o.append(f"- **Verdict:** {rv['verdict']}")
    o.append(f"- **Measurement:** {f.get('value','')}  ·  **Shuffle floor:** {f.get('shuffle_floor','')}  ·  **Analog:** {f.get('universe_analog','')}")
    o.append(f"- **Related:** "+", ".join(f"{r} ({byid.get(r,'?')})" for r in f.get('cross_refs',[]))); o.append("")
open(os.path.join(H,'LATENT_FEATURES.md'),'w',encoding='utf-8').write("\n".join(o))
print("regenerated LATENT_FEATURES.md ->", len(o), "lines,", len(inc), "in-table,", len(exc), "excluded")
