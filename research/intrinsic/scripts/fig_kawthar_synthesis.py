# -*- coding: utf-8 -*-
"""Capstone synthesis: ONE axis (kawthar <-> abtar) threaded through THREE measured layers of the study —
TEXT (al-Kawthar 108) -> TIME (chronology web) -> SOUL (inner-self network) -> OUTCOME.
Shows the temporal journey. Bare Arabic terms; MEASURED vs INFERRED tagged."""
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import re, arabic_reshaper
from bidi.algorithm import get_display
_resh = arabic_reshaper.ArabicReshaper(configuration={'delete_harakat': False, 'support_ligatures': False})
_AR = re.compile(r'[؀-ۿ]+(?:\s+[؀-ۿ]+)*')
def A(s):
    return _AR.sub(lambda m: get_display(_resh.reshape(m.group().replace('ک','ك').replace('ی','ي'))), s) if s else s
INK='#10243A'; NAVY='#1D3557'; GREEN='#0F6E56'; RED='#C1121F'; BLUE='#378ADD'; PURP='#7A5AA6'; BORD='#E2E8F1'
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':INK})
fig, ax = plt.subplots(figsize=(14.8, 9.4)); ax.set_xlim(0, 1480); ax.set_ylim(0, 940); ax.axis('off'); ax.invert_yaxis()
ax.text(30, 34, "How it all fits the al-Kawthar framework — one axis through three measured layers",
        fontsize=18, fontweight='bold', color=NAVY)
ax.text(30, 62, "kawthar (abundance that CROSSES) vs abtar (SEVERANCE, cut off) is the study's master axis; each layer below was measured on the rasm.   "
                "[M] = measured   ·   [I] = inferred reading", fontsize=12.5, color=INK)
# master axis + outcome fork
ax.add_patch(FancyArrowPatch((70, 150), (1150, 150), arrowstyle='-|>', mutation_scale=20, lw=3, color=NAVY))
ax.text(70, 132, "THE AXIS", fontsize=12.5, fontweight='bold', color=NAVY)
ax.add_patch(Circle((1230, 96), 30, fc=GREEN, ec='#fff', lw=2)); ax.text(1230, 96, A('کوثر'), ha='center', va='center', fontsize=14, color='#fff', fontweight='bold')
ax.text(1275, 96, "kawthar — crosses", fontsize=12.5, color=GREEN, va='center', fontweight='bold')
ax.add_patch(Circle((1230, 204), 30, fc=RED, ec='#fff', lw=2)); ax.text(1230, 204, A('أبتر'), ha='center', va='center', fontsize=14, color='#fff', fontweight='bold')
ax.text(1275, 204, "abtar — cut off", fontsize=12.5, color=RED, va='center', fontweight='bold')
ax.add_patch(FancyArrowPatch((1150, 150), (1200, 104), arrowstyle='-|>', mutation_scale=15, lw=2, color=GREEN))
ax.add_patch(FancyArrowPatch((1150, 150), (1200, 196), arrowstyle='-|>', mutation_scale=15, lw=2, color=RED))

def layer(y, tag, title, tint, ec, blurb, anchors):
    ax.add_patch(FancyBboxPatch((60, y), 1300, 178, boxstyle='round,pad=3,rounding_size=12', fc=tint, ec=ec, lw=1.8))
    ax.text(85, y+34, title, fontsize=15.5, fontweight='bold', color=ec)
    ax.text(1335, y+34, tag, fontsize=12.5, fontweight='bold', color=ec, ha='right')
    ax.text(85, y+64, blurb, fontsize=12.5, color=INK)
    bx = 95
    for head, body, col in anchors:
        ax.add_patch(FancyBboxPatch((bx, y+86), 392, 80, boxstyle='round,pad=2,rounding_size=8', fc='#FFFFFF', ec=BORD, lw=1.2))
        ax.text(bx+14, y+112, head, fontsize=13, fontweight='bold', color=col)
        ax.text(bx+14, y+140, body, fontsize=11, color=INK)
        bx += 410

layer(268, "[M] measured core", "1 · TEXT — Surat al-Kawthar (108), the seed",
      '#EAF2FB', BLUE,
      "The shortest sura names the axis directly and aims it at one addressee (-ka): a gift given, set against the enemy's severance.",
      [("kawthar vs abtar", "the two poles, named (108)", BLUE),
       ("aʿtayna -> -ka", "gift + peak -ka address", BLUE),
       ("shaniʾ bond", "only in suras 5 & 108", BLUE)])
layer(478, "[M] clocks · [report] dates", "2 · TIME — the chronology web (WHEN)",
      '#F4F7F4', GREEN,
      "Where 108 sits in revealed time: a partial-order web of parallel gradients, not a line. Language-clocks measured; event dates corroborative only.",
      [("verse-length clock", "Meccan 14 -> Medinan 30; r=0.66", GREEN),
       ("warning -> tidings", "nadhir-share 100% -> 53%", GREEN),
       ("partial order [I]", "threads braided, not a line", GREEN)])
layer(688, "[M] skeleton · [I] roof", "3 · SOUL — the inner-self network (HOW)",
      '#F7F3FB', PURP,
      "The mechanism: faculties dissociate; a cognition<->action loop; zad amplifies whichever pole is present -> the self crosses (kawthar) or is cut off (abtar).",
      [("faculties dissociate", "155:4 turn; fuʾad-sense OR 8.8", PURP),
       ("zad amplifier", "disease OR 16.2 -> either pole", PURP),
       ("processor reading [I]", "coupled qalb+nafs, held lightly", PURP)])
for y0 in (446, 656):
    ax.add_patch(FancyArrowPatch((700, y0), (700, y0+32), arrowstyle='-|>', mutation_scale=16, lw=2.2, color=NAVY, alpha=.6))
ax.text(712, 462, "the same axis runs down...", fontsize=11.5, color=NAVY, fontstyle='italic')
ax.text(712, 672, "...into where it is decided", fontsize=11.5, color=NAVY, fontstyle='italic')
ax.text(60, 905, "Honest bound: the within-Medinan fine order and the heart-state gradation are NULLs (instrument-limited); "
                 "computation localises & ranks for human reading — it does not generate the meaning.", fontsize=11.5, color=INK, fontstyle='italic')
plt.tight_layout()
out = "/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2/research/intrinsic/kawthar_figs/fig_kawthar_synthesis.png"
plt.savefig(out, dpi=150, bbox_inches='tight', facecolor='white'); print("wrote", out)
