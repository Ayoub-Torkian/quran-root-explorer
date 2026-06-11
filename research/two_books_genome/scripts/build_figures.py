#!/usr/bin/env python3
"""Build manuscript figures F1-F5 from the recorded data (CPU, matplotlib only).
All numbers trace to pipeline_results.json / ledger.json / RESULTS.md / the draft.
Outputs PNGs to ../figures/.
"""
import os, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "figures")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 10, "axes.spysolid": True} if False else {"font.size": 10})

INK = "#1a1a1a"; ACC = "#b5651d"; GEN = "#2e6e4e"; GREY = "#888"; RED = "#b22222"

# ---------- F1: MI-decay gamma, languages vs genome ----------
# (label, family, gamma, ci) from RESULTS.md multi-language table
rows = [
    ("Human genome (CDS)", "—",            0.915, 0.006, GEN),
    ("Finnish (Kalevala)", "Finno-Ugric",  1.393, 0.045, INK),
    ("Spanish (Quijote)",  "Romance",      1.929, 0.031, INK),
    ("German (Kafka)",     "Germanic",     1.932, 0.130, INK),
    ("English (Moby-Dick)","Germanic",     2.249, 0.052, INK),
    ("Arabic (Qur'an)",    "Semitic",      2.285, 0.107, ACC),
    ("French (Les Mis.)",  "Romance",      2.295, 0.037, INK),
    ("English (Pride)",    "Germanic",     2.336, 0.069, INK),
    ("Greek (Iliad)",      "Hellenic",     2.486, 0.059, INK),
]
rows = sorted(rows, key=lambda r: r[2])
fig, ax = plt.subplots(figsize=(7.2, 4.4))
ys = np.arange(len(rows))
for y, (lab, fam, g, ci, c) in zip(ys, rows):
    ax.errorbar(g, y, xerr=ci, fmt="o", color=c, ecolor=c, capsize=3, ms=7)
    ax.text(g + ci + 0.04, y, lab, va="center", fontsize=9,
            color=c, fontweight="bold" if c in (GEN, ACC) else "normal")
ax.axvspan(1.39, 2.49, color="#dddddd", alpha=0.45, zorder=0)
ax.text(1.94, len(rows)-0.4, "language cluster (γ ≈ 1.4–2.5)", ha="center",
        fontsize=8.5, color=GREY, style="italic")
ax.set_yticks([]); ax.set_xlim(0.7, 3.05); ax.set_ylim(-0.7, len(rows)-0.1)
ax.set_xlabel("MI-decay exponent γ   (lower = longer-range memory)")
ax.set_title("Fig. 1  Structural pre-check: the genome stands apart from all language",
             fontsize=10.5, fontweight="bold", loc="left")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout(); fig.savefig(os.path.join(OUT, "F1_structural_gamma.png"), dpi=160)
plt.close(fig)

# ---------- F2: pipeline schematic ----------
fig, ax = plt.subplots(figsize=(8.6, 3.0)); ax.axis("off")
ax.set_xlim(0, 10); ax.set_ylim(0, 3)
def box(x, y, w, h, text, fc, tc="white"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                 fc=fc, ec="none")); ax.text(x+w/2, y+h/2, text, ha="center", va="center",
                 color=tc, fontsize=9, fontweight="bold")
def arrow(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                 mutation_scale=14, color=INK, lw=1.4))
box(0.1, 1.2, 1.7, 0.7, "Text\n(Qur'ān / control)", "#444")
box(2.3, 1.2, 2.0, 0.7, "char→codon/AA\nmap (sim. annealing)", ACC)
box(4.8, 1.2, 1.6, 0.7, "sequence", "#444")
box(6.9, 1.95, 3.0, 0.6, "objective: dipeptide / Markov", GEN)
box(6.9, 1.15, 3.0, 0.6, "k-mer / tblastx vs CCDS", GEN)
box(6.9, 0.30, 3.0, 0.6, "FLOOR: shuffled + random", GREY, "white")
for (x1,y1,x2,y2) in [(1.8,1.55,2.3,1.55),(4.3,1.55,4.8,1.55),
                       (6.4,1.55,6.9,2.25),(6.4,1.55,6.9,1.45),(6.4,1.55,6.9,0.6)]:
    arrow(x1,y1,x2,y2)
ax.text(5, 2.75, "Fig. 2  The pipeline — real input and the matched floor run in parallel",
        ha="center", fontsize=10.5, fontweight="bold")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "F2_pipeline.png"), dpi=160); plt.close(fig)

# ---------- F3: saturation / floor (k-mer match) ----------
# recorded endpoints: Step2 k=5 real 99.96 / floor 100 ; Step3 k=6 real 99.9 / floor 100
fig, ax = plt.subplots(figsize=(7.0, 4.0))
it = np.linspace(0, 8000, 200)
def sat(end, rate): return end*(1-np.exp(-it/rate))
ax.plot(it, sat(99.96, 1500), color=ACC, lw=2.2, label="real Qur'ān")
ax.plot(it, sat(100.0, 1400), color=GREY, lw=2.0, ls="--", label="shuffled (floor)")
ax.plot(it, sat(99.7, 1700), color=INK, lw=1.6, ls=":", label="English (floor)")
ax.axhline(100, color=RED, lw=0.8, alpha=0.6)
ax.text(7600, 100.6, "ceiling", color=RED, fontsize=8, ha="right")
ax.scatter([8000, 8000], [99.96, 100], color=[ACC, GREY], zorder=5, s=30)
ax.set_ylim(0, 104); ax.set_xlabel("simulated-annealing iterations")
ax.set_ylabel("best proteome k-mer match (%)")
ax.set_title("Fig. 3  Saturation: a free mapping drives ANY text to the ceiling (k=5–6)",
             fontsize=10.5, fontweight="bold", loc="left")
ax.text(500, 12, "floor sits at the ceiling →\nsimilarity-over-floor ≈ 0",
        fontsize=9, color=GREY, style="italic")
ax.legend(loc="center right", frameon=False, fontsize=9)
ax.spines[["top", "right"]].set_visible(False)
fig.text(0.5, 0.005, "Curves illustrative; endpoints are the measured values (Steps 2–3).",
         ha="center", fontsize=7.5, color=GREY)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(os.path.join(OUT, "F3_saturation.png"), dpi=160); plt.close(fig)

# ---------- F4: the cautionary false positive (3 panels) ----------
fig, axs = plt.subplots(1, 3, figsize=(10.2, 3.7))
# (a) single pair
a = axs[0]
a.bar([0, 1], [0.58, 0.056], color=[ACC, GREY], width=0.6)
a.set_xticks([0, 1]); a.set_xticklabels(["single pair", "chance"])
a.set_ylim(0, 0.7); a.set_ylabel("cross-set convergence")
a.set_title("(a) n=1: looks real\n(survives 3 controls)", fontsize=9.5)
a.text(0, 0.60, "0.58", ha="center", fontsize=9, fontweight="bold")
a.text(1, 0.09, "0.056", ha="center", fontsize=9)
a.spines[["top", "right"]].set_visible(False)
# (b) replication
b = axs[1]
labs = ["real\n+proteome", "shuffled\n+proteome", "real\n+random", "synthetic\nrepeat"]
vals = [0.22, 0.22, 0.03, 0.05]; errs = [0.13, 0.16, 0, 0]
cols = [ACC, GREY, "#bbb", "#bbb"]
b.bar(range(4), vals, yerr=errs, color=cols, width=0.62, capsize=4)
b.axhline(0.055, color=RED, ls="--", lw=1, label="chance 0.055")
b.set_xticks(range(4)); b.set_xticklabels(labs, fontsize=8)
b.set_ylim(0, 0.45); b.set_title("(b) replication kills it\nreal = shuffled (z=0.00)", fontsize=9.5)
b.legend(frameon=False, fontsize=8, loc="upper right")
b.spines[["top", "right"]].set_visible(False)
# (c) letter dissection
c = axs[2]
c.bar([0, 1], [0.31, 0.14], color=["#7a5230", "#cbb9a8"], width=0.6)
c.set_xticks([0, 1]); c.set_xticklabels(["frequent\nletters", "rare\nletters"])
c.set_ylim(0, 0.4); c.set_title("(c) residual = composition\n(not order, not meaning)", fontsize=9.5)
c.text(0, 0.32, "0.31", ha="center", fontsize=9, fontweight="bold")
c.text(1, 0.15, "0.14", ha="center", fontsize=9)
c.spines[["top", "right"]].set_visible(False)
fig.suptitle("Fig. 4  A signal that passes single-instance controls and still dies under replication",
             fontsize=10.5, fontweight="bold", x=0.02, ha="left")
fig.tight_layout(rect=(0, 0, 1, 0.94))
fig.savefig(os.path.join(OUT, "F4_false_positive.png"), dpi=160); plt.close(fig)

# ---------- F5: folding null ----------
fig, axs = plt.subplots(1, 2, figsize=(8.4, 3.8))
# pLDDT
a = axs[0]
a.axhspan(0, 50, color="#f2dede", alpha=0.7); a.axhspan(70, 100, color="#dff0df", alpha=0.7)
a.text(1.5, 25, "disordered / random", ha="center", fontsize=8.5, color=RED)
a.text(1.5, 85, "real proteins", ha="center", fontsize=8.5, color=GEN)
a.bar([0, 1], [49.6, 34], color=ACC, width=0.55)
a.set_xticks([0, 1]); a.set_xticklabels(["Al-Ikhlas\n(47 aa)", "An-Nas\n(80 aa)"])
a.set_ylim(0, 100); a.set_ylabel("pLDDT"); a.set_title("(a) confidence per residue", fontsize=9.5)
a.spines[["top", "right"]].set_visible(False)
# pTM
b = axs[1]
b.axhspan(0.5, 1.0, color="#dff0df", alpha=0.7)
b.text(0.5, 0.75, "folded (pTM > 0.5)", ha="center", fontsize=8.5, color=GEN)
b.bar([0, 1], [0.30, 0.15], color=ACC, width=0.55)
b.set_xticks([0, 1]); b.set_xticklabels(["Al-Ikhlas", "An-Nas"])
b.set_ylim(0, 1.0); b.set_ylabel("pTM"); b.set_title("(b) global fold confidence", fontsize=9.5)
b.spines[["top", "right"]].set_visible(False)
fig.suptitle("Fig. 5  Qur'ān-derived proteins do not fold (ESMFold)",
             fontsize=10.5, fontweight="bold", x=0.02, ha="left")
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.savefig(os.path.join(OUT, "F5_folding.png"), dpi=160); plt.close(fig)

# ---------- F6: positive control (instrument validation) ----------
fig, ax = plt.subplots(figsize=(7.6, 4.2))
groups = ["planted cipher\n(letters)", "planted cipher\n(roots)", "REAL\nroot→genome"]
recovery = [1.00, 0.867, np.nan]      # recovery only defined for planted
conv =     [1.00, 0.567, 0.015]
chance =   [0.032, 0.033, 0.017]
x = np.arange(len(groups)); w = 0.36
ax.bar(x - w/2, [r if not np.isnan(r) else 0 for r in recovery], w, color=GEN, label="recovery")
ax.bar(x + w/2, conv, w, color=ACC, label="cross-portion convergence")
for i, c in enumerate(chance):
    ax.plot([x[i]-0.5, x[i]+0.5], [c, c], color=RED, ls="--", lw=1)
ax.text(x[0]-0.5, 0.07, "chance", color=RED, fontsize=8)
ax.set_xticks(x); ax.set_xticklabels(groups); ax.set_ylim(0, 1.08)
ax.set_ylabel("agreement")
ax.set_title("Fig. 6  Instrument validation: it fires on a true mapping, is null on the genome",
             fontsize=10.5, fontweight="bold", loc="left")
ax.legend(frameon=False, fontsize=9, loc="upper right")
ax.spines[["top", "right"]].set_visible(False)
ax.text(2, 0.10, "flat-target\nceiling", ha="center", fontsize=8, color=GREY, style="italic")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "F6_positive_control.png"), dpi=160)
plt.close(fig)

print("wrote:", sorted(os.listdir(OUT)))
