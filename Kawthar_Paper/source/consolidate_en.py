# -*- coding: utf-8 -*-
"""Consolidate the English (technical) paper: Q1 order, 12 dense Arabic-labelled figures,
consecutive tables (1-10), single source of truth for numbering, + patchiness re-audit."""
import re
P="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2/research/intrinsic/papers"
FIG="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2/research/intrinsic/kawthar_figs"
def rd(f): return open(f"{P}/{f}",encoding='utf-8').read().rstrip()+"\n\n"
p3=open(f"{P}/kawthar_en_p3.md",encoding='utf-8').read()
def sect(t,a,b=None): i=t.index(a); j=t.index(b) if b else len(t); return t[i:j].rstrip()+"\n\n"
discussion = sect(p3,"# 6. Discussion","# 7. Limitations and caveats")
limitations= sect(p3,"# 7. Limitations and caveats","# 8. Conclusion")
conclusion = sect(p3,"# 8. Conclusion","# References")
references = sect(p3,"# References","# Appendix: Concordance")
concordance= sect(p3,"# Appendix: Concordance")

order=['kawthar_en_p1.md','kawthar_en_p1b.md','kawthar_en_p2.md','kawthar_en_p2b.md','kawthar_en_p2c.md',
 'kawthar_en_p2d.md','kawthar_en_p2e.md','kawthar_en_p2f.md','kawthar_en_p2g.md','kawthar_en_p2h.md',
 'kawthar_en_p2i.md','kawthar_en_p2t.md','kawthar_en_p2j.md','kawthar_en_p2k.md','kawthar_en_p2u.md','kawthar_en_p2l.md','kawthar_en_p2o.md',
 'kawthar_en_p2p.md','kawthar_en_p2m.md','kawthar_en_p2q.md','kawthar_en_p2r.md','kawthar_en_p2s.md','kawthar_en_p2x.md','kawthar_en_p_valid.md']
doc="".join(rd(f) for f in order)
doc += discussion + rd('kawthar_en_p2w.md') + rd('kawthar_en_p_theo.md') + rd('kawthar_en_p_recovery.md') + rd('kawthar_en_p2n.md') + rd('kawthar_en_p_contrib.md') + limitations \
     + rd('kawthar_en_p_future.md') + conclusion + references + rd('kawthar_en_appendixA.md') + concordance

# ---- 1) strip ALL existing image embeds (we re-insert a curated set) ----
doc=re.sub(r'^!\[.*?\]\(.*?\)\s*$','',doc,flags=re.M)

# ---- 2) post-Results section renumbering ----
doc=doc.replace("# 7. Limitations and caveats","# 9. Limitations and caveats")
doc=doc.replace("# 8. Conclusion","# 11. Conclusion")
doc=doc.replace("# Appendix: Concordance of interpreting verses",
                "# Appendix B. Concordance of interpreting verses\n\n*@@T6@@. Concordance — verses the Qurʾān supplies to interpret al-Kawthar.*")

# ---- 3) §5 reader-orientation + measured/interpretive dividers ----
doc=doc.replace("## 5.1 The lexical fingerprint",
 "*Section 5 proceeds in three movements: a **measured lexical and structural core** (5.1–5.9); "
 "**interpretive, concordance-guided thematic readings** (5.10–5.21) — close readings, not statistical claims, "
 "tested adversarially in §7–§8; and **computational / structural analyses** (5.22–5.25), then a **pre-registered validation** (5.26) that tests — and corrects — the preceding claims.*\n\n"
 "**Part A — The measured lexical and structural core.**\n\n## 5.1 The lexical fingerprint")
doc=doc.replace('## 5.10 A closer look: why "We gave"',
 "**Part B — Interpretive thematic readings (concordance-guided; not statistical — and, per the validation in §5.26, not statistically distinguished from a length/rarity-matched null; read as illustrative close reading).**\n\n"
 '## 5.10 A closer look: why "We gave"')
doc=doc.replace("## 5.22 The surah in the web",
 "**Part C — Computational and structural analyses.**\n\n## 5.22 The surah in the web")

# ---- 4) §5.22 referenced now-cut raw figures -> Table 4 ----
doc=doc.replace("Table 6 and Figures 11–12 report the result","Table 4 reports the result")
doc=doc.replace("(Figures 11–12)","(Table 4)").replace("Figures 11–12","Table 4")

# ---- 5) LEGACY figure-reference remap (original draft numbers -> final 1-9); cut figs 2,6,8,10 ----
doc=re.sub(r'\s*\(Figure (?:2|6|8|10)\)','',doc)
doc=re.sub(r'\bFigure (?:2|6|8|10)\b','the chart',doc)
for old,new in [(13,7),(14,8),(15,9),(9,6),(7,5),(5,4),(4,3),(3,2),(1,1)]:
    doc=re.sub(rf'\bFigure {old}\b', f'@@F{new}@@', doc)
for n in range(1,10): doc=doc.replace(f'@@F{n}@@', f'Figure {n}')

# ---- 6) LEGACY table renumber to consecutive (7->5,6->4,5->3,4->2; 1 stays) ----
for old,new in [(7,5),(6,4),(5,3),(4,2)]:
    doc=re.sub(rf'\bTable {old}\b', f'@@T{new}@@', doc)
for n in range(2,7): doc=doc.replace(f'@@T{n}@@', f'Table {n}')

# ---- 6.5) RESTORE new (tokenised, already-final) figure/table numbers, immune to the legacy remap ----
for n in (7,8,9,10,11,12,13): doc=doc.replace(f'{{{{F{n}}}}}', f'Figure {n}')
for n in (7,8,9,10,11,12):  doc=doc.replace(f'{{{{T{n}}}}}', f'Table {n}')

# ---- 7) insert the 12 curated figure embeds after their section headers ----
EMB={
 "## 5.1 The lexical fingerprint":[("Figure 1. The lexical fingerprint of al-Kawthar — corpus frequency of its seven content roots.","f1_rarity.png")],
 "## 5.3 The surah's spine":[("Figure 2. The surah's spine: abundance and continuation against severance, read off the roots.","f2_antithesis.png")],
 "## 5.4 Defining a word used once":[("Figure 3. The hapax naḥr interpreted by the Qurʾān's wider sacrifice vocabulary; naḥr occurs only at 108:2, with 6:162 and 22:37 supplying its sense.","f3_sacrifice.png")],
 "## 5.5 The architecture of three verses":[("Figure 4. The architecture of the three verses: the innā…inna ring, the -ka thread, and the agency progression.","f4_structure.png")],
 "## 5.7 The shortest surah":[("Figure 5. Among all 114 sūras, al-Kawthar is the shortest by rasm letters; its root-twin al-Takāthur (102) is marked.","f5_shortest.png")],
 "## 5.9 Lexical singularity":[("Figure 6. Lexical singularity: the distribution of hapax (used-only-once) roots per verse across the corpus.","f6_hapax.png")],
 "## 5.23 Normalized lenses":[("Figure 7. PPMI attraction network (Arabic rasm): rare roots sit on few edges; only the بتر–شنء bond is strong and statistically notable (p≈0.0005, §5.26).","fig13_ppmi_network.png"),
                               ("Figure 8. Validation: against all 430 corpus hapax, naḥr binds below median (10th pct) and abtar is only moderate (66th) — the hapax are NOT 'maximally bound'.","fig14_normalization.png")],
 "## 5.24 The long sūra that elaborates":[("Figure 9. Robustness: the al-Māʾida '#1 elaborator' rank is length-confounded (falls to 3–49 once length-normalized). The robust fact: شنء occurs only in sūras 5 and 108.","fig15_elaboration.png")],
 "## 5.25 The map of address":[("Figure 10. The map of address (Arabic rasm): al-Kawthar leads the Qurʾān in personal -ka density, and which 'giving' verb reaches the Prophet.","fig_addr_map.png"),
                               ("Figure 11. Two registers of address are near-orthogonal: al-Kawthar at the extreme of the personal axis (zero qul), the qul-suras on the other arm.","fig_two_registers.png")],
 "## 5.26 Validation":[("Figure 13. Pre-registered rarity-matched null: al-Kawthar's web-binding sits at the 44th percentile (z=−0.09) — statistically ordinary; no short sūra exceeds the 95th. The 'designed coherence' reading is not supported.","fig_null_validation.png")],
 "### 5.25.2 Synthesis":[("Figure 12. Self-interpretation, directed (al-Quran yufassiru baduhu badan): an arrow a->b reads 'a reliably accompanies b' P(a|b); each hapax is fixed by its common context, not the reverse.","fig_selfinterp.png")],
}
for header,figs in EMB.items():
    idx=doc.index(header); endl=doc.index("\n",idx)+1
    ins="\n"+"".join(f"![{cap}]({FIG}/{fn})\n\n" for cap,fn in figs)
    doc=doc[:endl]+ins+doc[endl:]

doc=re.sub(r'\n{3,}','\n\n',doc)
open(f"{P}/kawthar_EN_technical.md",'w',encoding='utf-8').write(doc)

# ================= PATCHINESS / ORGANIZATION RE-AUDIT =================
print("="*60); print("RE-AUDIT (patchiness / Q1 organization)"); print("="*60)
secs=re.findall(r'^#\s+(.*)$',doc,re.M)
print("TOP-LEVEL SECTIONS:")
for s in secs: print("   #",s)
nums=re.findall(r'^#\s+(\d+)\.',doc,re.M)
dups=[n for n in set(nums) if nums.count(n)>1]
print("\n[check] duplicate top-level section numbers:", dups or "none")
want=[str(i) for i in range(1,12)]
print("[check] missing top-level numbers:", [n for n in want if n not in nums] or "none")
emb=re.findall(r'!\[(Figure \d+)',doc)
refs=set(re.findall(r'\bFigure (\d+)\b',doc))
embn=sorted(int(x.split()[1]) for x in emb)
print("\n[figures] embedded:",embn)
print("[figures] in-text refs:",sorted(int(x) for x in refs))
print("[check] embedded but NOT referenced:",[n for n in embn if str(n) not in refs] or "none")
print("[check] referenced but NOT embedded:",[int(n) for n in refs if int(n) not in embn] or "none")
print("[check] 'the chart' casualties:",doc.count('the chart'))
capt=sorted(set(int(x) for x in re.findall(r'\*?Table (\d+)\.',doc)))
tref=set(re.findall(r'\bTable (\d+)\b',doc))
print("\n[tables] captioned:",capt)
print("[tables] referenced:",sorted(int(x) for x in tref))
print("[check] captioned but NOT referenced:",[n for n in capt if str(n) not in tref] or "none")
print("[check] referenced but NOT captioned:",[int(n) for n in tref if int(n) not in capt] or "none")
print("\n[check] leftover {{tokens}}:", re.findall(r'\{\{[^}]+\}\}',doc) or "none")
print("\nAPPROX WORD COUNT:", len(re.sub(r'\|.*?\|','',doc).split()))
