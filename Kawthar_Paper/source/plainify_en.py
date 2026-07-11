# -*- coding: utf-8 -*-
"""Derive the PLAIN-English paper from the technical one: drop calibration tags & confidence wrap-ups,
remove meta dividers, plainer abstract/title. Keep findings, analogies, figures, tables, structure."""
import re
P="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2/research/intrinsic/papers"
t=open(f"{P}/kawthar_EN_technical.md",encoding='utf-8').read()

# 1) drop the YAML title block -> replace with plain title block
t=re.sub(r'^---.*?---\n','',t,count=1,flags=re.S)
title='''---
title: "The Abundance and the Cut-Off: How the Qur'an Explains Its Own Rarest Words — a Plain-Language Study of Sūrat al-Kawthar"
subtitle: "Plain-language edition for the general reader"
date: "June 2026"
---

'''

# 1.5) PLAIN: rewrite the method paragraph (no tag labels) + convert inline bold tags to clean prose
t=t.replace(
 "A word on method and honesty, since both are easy to abuse. Throughout, we tag every claim. A claim marked **[TEXT]** is something the Qur'an itself says or displays. A claim marked **[REPORT]** is an external transmission — an occasion-of-revelation narrative, a traditional gloss — which we treat as corroborative at most and never as fact. A claim marked **[INFERENCE]** is our own reasoning. Separately, for the quantitative findings, **[MEASURED]** marks a number actually produced by counting the corpus, while **[INFERRED]** marks our interpretation of what that number means.",
 "A word on method and honesty, since both are easy to abuse. Throughout, we keep two honest distinctions visible. The first concerns *claims*: between what the Qur'an itself says or displays, an external transmission (an occasion-of-revelation narrative or a traditional gloss, which we treat as corroborative at most and never as fact), and our own reasoning. The second concerns *numbers*: between a figure actually produced by counting the corpus and our interpretation of what that figure means.")
_inline=[
 ("claims attributed to commentators are **[REPORT]**:","claims attributed to commentators are reports of their positions:"),
 ("an occasion-report is **[REPORT]**, not **[TEXT]**","an occasion-report is a transmission, not the text itself"),
 ("We survey both as **[REPORT]** — positions held","We survey both as positions held"),
 ("is a count we actually ran; we mark it **[MEASURED]**.","is a count we actually ran, and we label it as such."),
 ("we mark the move **[INFERRED]** and","we flag the move as interpretation and"),
 ("we note it only as a **[REPORT]** resonance","we note it only as a corroborative resonance"),
 ("We mark it honestly: this is **[INFERRED]** — a reconstruction","We mark it honestly: this is our inference — a reconstruction"),
 ("So: **[INFERRED, moderate]** that 39:18","So, with moderate confidence, we read that 39:18"),
 ("of conciliation. **[INFERRED, moderate]** for the unifying","of conciliation. This is our inference (moderate confidence) for the unifying"),
 ("which we record only as **[REPORT]**, neither used","which we record only as a reported position, neither used"),
 ("so any computed binary is a **[HUMAN CONSTRUCT]** proxy","so any computed binary is a human-construct proxy"),
 ("but strictly as a **[HUMAN CONSTRUCT]** ranking","but strictly as a human-construct ranking"),
]
for a,b in _inline: t=t.replace(a,b)
# catch-all: remove any remaining bolded tag tokens cleanly (bold + bracket content)
t=re.sub(r"\s*\*\*\[(?:TEXT|REPORT|INFERENCE|MEASURED|INFERRED|HUMAN CONSTRUCT)[^\]]*\][:\s]*\*\*","",t)

# 2) remove inner single-token tags, then any bracketed note containing a calibration keyword
t=re.sub(r'\s*\[(?:MEASURED|INFERRED|INFERENCE|TEXT|REPORT)\]','',t)
for _ in range(3):
    t=re.sub(r'\s*\[[^\[\]]*(?:MEASURED|INFERRED|INFERENCE|TEXT|REPORT|CONSTRUCT|construct|conceded|flagged|attested|measured|inferred|de-circular)[^\[\]]*\]','',t)

# 3) remove the calibration wrap-up paragraphs ("We mark/state the confidence ...")
t=re.sub(r'(?m)^We (?:mark|state) the confidence.*?(?=\n\n)','',t,flags=re.S)

# 4) remove the meta "Section 5 proceeds in three movements" framing + Part A/B/C dividers
t=re.sub(r"\*Section 5 proceeds in three movements:.*?\*\n\n","",t,flags=re.S)
t=t.replace("**Part A — The measured lexical and structural core.**\n\n","")
t=re.sub(r"\*\*Part B — Interpretive thematic readings.*?\*\*\n\n","*The next group of sections looks closely at the surah's individual word-choices; note (per §5.26) they are illustrative close readings, not statistically distinguished from a matched null.*\n\n",t,flags=re.S)
t=t.replace("**Part C — Computational and structural analyses.**\n\n",
            "*The final group views the surah with network tools.*\n\n")

# 5) soften a few technical phrases
repl={
 "PPMI (Pointwise Mutual Information)":"a frequency-controlled association score",
 "idf-weighted":"rarity-weighted",
 "(PPMI)":"(association strength)",
 "rasm":"consonantal text (rasm)",
}
for a,b in repl.items(): t=t.replace(a,b)

# collapse any residual empty bold and stray markers
t=re.sub(r'\*\*\s*\*\*','',t); t=re.sub(r'\*\*\s*:\s*','',t)
# tidy blank lines
t=re.sub(r'\n{3,}','\n\n',t)
assert '****' not in t, 'empty-bold **** still present'
open(f"{P}/kawthar_EN_plain.md",'w',encoding='utf-8').write(title+t)

# word count
body='\n'.join(l for l in t.split('\n') if not l.strip().startswith('>') and not l.strip().startswith('!['))
print("PLAIN-EN words (excl verses/figs):", len(re.findall(r"[A-Za-zÀ-ɏ][\w'\-]*",body)))
print("remaining bracket-tags:", len(re.findall(r'\[(?:MEASURED|INFERRED|TEXT|REPORT|INFERENCE)\]',t)))
print("sections:", [s for s in re.findall(r'^#\s+(.*)$',t,re.M)][:14])
