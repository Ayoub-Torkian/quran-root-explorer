# -*- coding: utf-8 -*-
"""Consolidate the English (technical) paper: Q1 order, dense figures, consecutive tables, + audit."""
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
 'kawthar_en_p2p.md','kawthar_en_p2m.md','kawthar_en_p2q.md','kawthar_en_p2r.md','kawthar_en_p2s.md','kawthar_en_p2x.md','kawthar_en_p_valid.md','kawthar_en_p_rarity.md','kawthar_en_p_multimodal.md','kawthar_en_p_v4.md','kawthar_en_p_grammar.md','kawthar_en_p_chronoweb.md','kawthar_en_p_capstone.md']
doc="".join(rd(f) for f in order)
doc += discussion + rd('kawthar_en_p2w.md') + rd('kawthar_en_p_theo.md') + rd('kawthar_en_p_recovery.md') + rd('kawthar_en_p2n.md') + rd('kawthar_en_p_contrib.md') + limitations \
     + rd('kawthar_en_p_future.md') + conclusion + references + rd('kawthar_en_appendixA.md') + concordance
doc=re.sub(r'^!\[.*?\]\(.*?\)\s*$','',doc,flags=re.M)
doc=doc.replace("# 7. Limitations and caveats","# 9. Limitations and caveats")
doc=doc.replace("# 8. Conclusion","# 11. Conclusion")
doc=doc.replace("# Appendix: Concordance of interpreting verses",
                "# Appendix B. Concordance of interpreting verses\n\n*@@T6@@. Concordance — verses the Qurʾān supplies to interpret al-Kawthar.*")
doc=doc.replace("## 5.1 The lexical fingerprint",
 "*Section 5 proceeds in movements: a measured lexical/structural core (5.1-5.9); interpretive thematic readings (5.10-5.21); computational analyses (5.22-5.25); a pre-registered validation (5.26); a rarity stratum (5.27); a multimodal test (5.28); and a robustness-and-generalisation pass (5.29) that tests and corrects the preceding claims.*\n\n"
 "**Part A - The measured lexical and structural core.**\n\n## 5.1 The lexical fingerprint")
doc=doc.replace('## 5.10 A closer look: why "We gave"',
 "**Part B - Interpretive thematic readings (concordance-guided; not statistically distinguished from a matched null per 5.26; illustrative close reading).**\n\n"
 '## 5.10 A closer look: why "We gave"')
doc=doc.replace("## 5.22 The surah in the web",
 "**Part C - Computational and structural analyses.**\n\n## 5.22 The surah in the web")
doc=doc.replace("Table 6 and Figures 11-12 report the result","Table 4 reports the result")
doc=doc.replace("(Figures 11-12)","(Table 4)").replace("Figures 11-12","Table 4")
doc=re.sub(r'\s*\(Figure (?:2|6|8|10)\)','',doc)
doc=re.sub(r'\bFigure (?:2|6|8|10)\b','the chart',doc)
for old,new in [(13,7),(14,8),(15,9),(9,6),(7,5),(5,4),(4,3),(3,2),(1,1)]:
    doc=re.sub(rf'\bFigure {old}\b', f'@@F{new}@@', doc)
for n in range(1,10): doc=doc.replace(f'@@F{n}@@', f'Figure {n}')
for old,new in [(7,5),(6,4),(5,3),(4,2)]:
    doc=re.sub(rf'\bTable {old}\b', f'@@T{new}@@', doc)
for n in range(2,7): doc=doc.replace(f'@@T{n}@@', f'Table {n}')
for n in range(7,32): doc=doc.replace('{{F%d}}'%n, 'Figure %d'%n)
for n in range(7,19): doc=doc.replace('{{T%d}}'%n, 'Table %d'%n)
EMB={
 "## 5.1 The lexical fingerprint":[("Figure 1. The lexical fingerprint of al-Kawthar - corpus frequency of its seven content roots.","f1_rarity.png")],
 "## 5.3 The surah's spine":[("Figure 2. The surah's spine: abundance and continuation against severance, read off the roots.","f2_antithesis.png")],
 "## 5.4 Defining a word used once":[("Figure 3. The hapax nahr interpreted by the Qur'an's wider sacrifice vocabulary; nahr occurs only at 108:2, with 6:162 and 22:37 supplying its sense.","f3_sacrifice.png")],
 "## 5.5 The architecture of three verses":[("Figure 4. The architecture of the three verses: the inna...inna ring, the -ka thread, and the agency progression.","f4_structure.png")],
 "## 5.7 The shortest surah":[("Figure 5. Among all 114 suras, al-Kawthar is the shortest by rasm letters; its root-twin al-Takathur (102) is marked.","f5_shortest.png")],
 "## 5.9 Lexical singularity":[("Figure 6. Lexical singularity: the distribution of hapax (used-only-once) roots per verse across the corpus.","f6_hapax.png")],
 "## 5.23 Normalized lenses":[("Figure 7. PPMI attraction network (Arabic rasm): rare roots sit on few edges; only the batr-shani bond is notable (p~0.0005, 5.26) - and even that is later demoted in 5.29.1.","fig13_ppmi_network.png"),("Figure 8. Validation: against all 430 corpus hapax, nahr binds below median (10th pct) and abtar is only moderate (66th) - the hapax are NOT 'maximally bound'.","fig14_normalization.png")],
 "## 5.24 The long sūra that elaborates":[("Figure 9. Robustness: the al-Ma'ida '#1 elaborator' rank is length-confounded (5.29.5 shows long->short elaboration is not systematic). The robust fact: shani occurs only in suras 5 and 108.","fig15_elaboration.png")],
 "## 5.25 The map of address":[("Figure 10. The map of address (Arabic rasm): al-Kawthar leads the Qur'an in personal -ka density, and which 'giving' verb reaches the Prophet.","fig_addr_map.png"),("Figure 11. Two registers of address are near-orthogonal: al-Kawthar at the extreme of the personal axis (zero qul), the qul-suras on the other arm.","fig_two_registers.png")],
 "## 5.26 Validation":[("Figure 13. Pre-registered rarity-matched null: al-Kawthar's web-binding sits at the 44th percentile (z=-0.09) - statistically ordinary; no short sura exceeds the 95th.","fig_null_validation.png")],
 "### 5.27.1 The frequency spectrum":[("Figure 14. The rarity spectrum is near-neutral: Fisher's log-series predicts ~80% of the 408 hapax; a modest 1.21x excess remains.","fig_freqspectrum.png")],
 "### 5.27.3 The rarity ladder":[("Figure 15. The rarity ladder: as a root touches more suras, specificity (mean idf) falls smoothly. al-Kawthar's roots sample every rung.","fig_rarityladder.png")],
 "### 5.27.6 The spread of the message":[("Figure 17. Spread of meaning is contained: IC-diffusion reach is ~1-2% in the real network vs 20-40x more in a degree-rewired null - thematic modularity localizes spread.","fig_spread.png")],
 "### 5.27.5 Burstiness":[("Figure 16. Burstiness rises with frequency: rare roots (5-15) are near-Poisson; only common roots cluster strongly - 'self-exciting' is a common-word property, not a rarity feature.","fig_burstiness.png")],
 "## 5.28 A multimodal test":[("Figure 18. Distinctiveness is two-dimensional: al-Kawthar sits at the joint extreme of two INDEPENDENT length-validated channels (rare words x rare letter-pairs, r=0.38); phonological entropy and compressibility were rejected as length artifacts.","fig_multimodal.png")],
 "### 5.29.1 The headline attraction bond is a single-verse artifact":[("Figure 19. The batr-shani 'bond' collapses from the 99.8th percentile (PPMI) to the 79th (count-sensitive t-score) and rests on one verse (108:3); the hapax have no vector in an independent encoder, which instead places shani in its real neighbourhood - the al-Ma'ida (5) legal vocabulary.","fig_v4_bond.png")],
 "### 5.29.2 Word-by-word":[("Figure 22. Word-by-word fittingness (cohesion vs count-matched substitutes) across the short suras: al-Kawthar scores high (z=5.3, 100th pct of its own null) but is not the maximum - a general short-sura design feature. The regulative-voice reading finds no support (p=0.99).","fig_v4_fitting.png")],
 "### 5.29.3 Dense singularity is particular":[("Figure 20. Cross-text fingerprint: dense singularity is particular, not a length effect - al-Kawthar (108) and al-Ikhlas (112) carry it (its hapax being samad and kuf'), while al-'Asr (103) and al-Nasr (110) have none; only al-Kawthar is also referentially open.","fig_v4_crosstext.png")],
 "### 5.29.4 Singularity is not openness":[("Figure 21. Singularity is not openness: an internal openness ranking of all 114 suras places al-Kawthar 1st (singular AND open) while al-Ikhlas - equally singular - ranks 57th (anchored: samad is fixed). al-'Asr/al-Nasr sit low on both.","fig_v4_openmap.png")],
 '### 5.29.5 "The long s':[("Figure 23. 'Long elaborates short' is not systematic: across all 11 short suras the top length-normalised elaborator is itself short (mean 14 roots vs 157 random; p=1.0). al-Kawthar's true partner is al-Duha (93), not al-Ma'ida.","fig_v4_elab.png")],
 "### 5.29.6 A concept-coining typology":[("Figure 24. A concept-coining typology of the short suras: al-Kawthar (108) and al-Ikhlas (112) alone carry TWO referentially-distinct hapax (nahr/abtar; samad/kuf'); al-Falaq/al-Fil coin one; al-Quraysh/al-Masad name concrete objects; five short suras coin none.","fig_v4_coining.png")],
 "## 5.30 The grammar of the gift":[("Figure 25. The grammar of the gift (rasm-WORD layer): (A) al-Kawthar's perfect aʿtaynaka is the fulfilment of al-Duha 93:5's future yuʿtika - same root ʿ-t-w, future->perfect; (B) the three verses climb a mood ladder (perfect->imperative->equational) that IS the agency ladder, the damir al-fasl huwa sealing abtar-ness onto the hater alone.","fig_grammar.png"),('Figure 26. The complete ledger of the divine prospective promises to the Prophet: six in all - three worldly ones are declared kept in the perfect (gift 93:5 -> 108:1 al-Kawthar; protection 2:137 -> 15:95; qibla 2:144, enacted in-verse), while three stay open by nature (the eschatological praised station 17:79, and the two ongoing revelation promises 87:6 and 73:5). The ridaa terminus (tarda / tardaha) marks only the gift and the qibla.',"fig_promise.png")],
 "## 5.31 From the pair to the chronology web":[("Figure 27. The chronology web: parallel developmental threads (events, the Prophet's household, three legal-ruling gradients khamr/qitāl/ribā, referent-group formation, warning to glad-tidings, heaven/hell tone, ritual and promise) braided through shared time-windows. The internal language-clocks are corpus-based; the time-coordinates come from traditional event reports (corroborative only); the whole is a human-built partial order, not a single line.","chronology_web.png")],
 "## 5.32 The inner self — where kawthar and abtar are decided":[("Figure 28. How the study fits the al-Kawthar framework: one axis, al-Kawthar (abundance that crosses) against al-abtar (severance, cut off), threaded through three layers each grounded in the text - the sura itself, the time of its revelation (the chronology web), and the inner self where the outcome is decided.","fig_kawthar_synthesis.png")],
 "### 5.32.2 The measured graph — corpus co-occurrence, with metrics":[("Figure 29. The inner-self concepts as a corpus graph: an edge where two roots co-occur in a verse, weighted by PPMI (frequency-controlled); laid out as three functional regions (apparatus / drivers / orientation) combined, within-region edges faint and the strongest cross-region bridges gold; node size = association strength. Density 0.48, 120 cycles, community structure z = +4.1 vs a degree-preserving null. Node selection and colours are interpretive; edges, weights and metrics are corpus-derived.","fig_inner_self_graph.png")],
 "### 5.32.3 The organ core — qalb, nafs, ṣadr, fuʾād":[("Figure 30. The organ core: a focused view of the four inner organs. Internal ties are solid (qalb-fuad 2.4, qalb-sadr 2.2); nafs stands apart with only a faint 0.1 tie to sadr - no edge to qalb or fuad. Each organ's strongest outward attachments are spokes coloured by the neighbour's role (qalb->sealing/disease, fuad->caprice, nafs->self-beguiling, sadr->cognition and the lodging of the whisper). Corpus PPMI edges and weights; the focused layout is for legibility.","fig_inner_self_organ_core.png")],
 "### 5.32.4 The interpretive model — the directed reading, and its one null":[("Figure 31. The inner-self network: qalb processes, nafs acts and is judged, fuad senses, sadr is the chamber; up-drivers and down-drivers feed a cognition-and-action loop; the increase operator zad amplifies whichever pole is present; dunya (the near) and akhira (the lasting) are two co-present orientations, and a self turned to the lasting crosses as kawthar while one clinging to the near is cut off as abtar. Nodes and edges are corpus-based; the spatial layout is a reading of those links.","fig_inner_self_net.png")],
 "### 5.25.2 Synthesis":[("Figure 12. Self-interpretation, directed (al-Quran yufassiru baduhu badan): an arrow a->b reads 'a reliably accompanies b' P(a|b); each hapax is fixed by its common context.","fig_selfinterp.png")],
}
for header,figs in EMB.items():
    idx=doc.index(header); endl=doc.index("\n",idx)+1
    ins="\n"+"".join("![%s](%s/%s)\n\n"%(cap,FIG,fn) for cap,fn in figs)
    doc=doc[:endl]+ins+doc[endl:]
doc=re.sub(r'\n{3,}','\n\n',doc)
open("%s/kawthar_EN_technical.md"%P,'w',encoding='utf-8').write(doc)
print("="*60); print("RE-AUDIT (patchiness / Q1 organization)"); print("="*60)
nums=re.findall(r'^#\s+(\d+)\.',doc,re.M)
print("[check] duplicate top-level numbers:", [n for n in set(nums) if nums.count(n)>1] or "none")
print("[check] missing top-level numbers:", [str(i) for i in range(1,12) if str(i) not in nums] or "none")
emb=re.findall(r'!\[(Figure \d+)',doc); refs=set(re.findall(r'\bFigure (\d+)\b',doc))
embn=sorted(int(x.split()[1]) for x in emb)
print("[check] embedded but NOT referenced:",[n for n in embn if str(n) not in refs] or "none")
print("[check] referenced but NOT embedded:",[r for r in sorted(refs,key=lambda x:int(x)) if int(r) not in embn] or "none")
print("[words]", len(re.findall(r"[A-Za-z'\-]+", doc)))
print("wrote kawthar_EN_technical.md")
