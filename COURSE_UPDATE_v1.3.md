# Course-update checklist — v1.2 → v1.3

The app at https://quranproject-quran-root-explorer.hf.space/ now serves **v1.3**.
The link students already have is unchanged and still works — it just shows the
updated app. Here is everything that changed, and what (if anything) to update in
each course. Most of it is "no change needed."

---

## 1. Root course (PMI / Jaccard / network / motifs / statistics) — NO CHANGES

Every page these lectures use is byte-for-byte identical to v1.2: Per-Root Profile,
Network, Motifs, Ayah Browser, Compare & Heatmaps, Morphology, Statistics, Export.
Screenshots, click-paths, and numbers all still match. Nothing to re-record.

## 2. Disjoint-Letters course — ONE walkthrough update

The Disjoint Letters page was reorganized from 4 flat tabs into **three categories**.
Everything the lectures show still exists — it just lives one level deeper now.

OLD (v1.2): the page opened straight into 4 tabs — Explore · Contiguity ·
Organization · What it is NOT.

NEW (v1.3): the page has three category tabs first, then sub-tabs inside:
  • 🧭 **Position** → Explore the tags · Contiguity geometry · Organization · What it is NOT
  • 🔤 **Sequence** → Alphabet & letter density · Letter information theory
  • 🧩 **Semantic** → Hypothesis Lab · Root sequence & richness

So when a lecture says *"click the Contiguity tab"*, the new instruction is:
*"click the 🧭 Position category, then the Contiguity geometry tab."* Same test,
same result — just one extra click. Update the navigation wording / screenshots
for the 4 original tabs accordingly.

The validated finding is unchanged: contiguity p ≈ 2×10⁻⁵, median 85 vs 26 verses.
(These now compute live on screen rather than being printed as fixed text.)

## 3. Slides quoting the Help "Case study" numbers — TWO corrections

The Help → Case study walkthrough is now computed live, which fixed two numbers
that were wrong in the old static version. If any slide cites the old figures,
update them:
  • Network: now **18 nodes / 152 edges / 800 closed triads** (old text said 147 / 735).
  • Densest sūra for ظلم·عدل·رحم: now correctly shows **S49 (33.3%)** as the top,
    ahead of S42 (22.6%). The old table omitted S49.
The frequency / PMI / Jaccard numbers were already correct and are unchanged.

## 4. Brand-new pages — NO existing lecture references them (optional to add)

Three new analyses now appear under the 📚 Two Books group, with no prior course:
Signal, Biology, and FDR Summary. They are fully documented inside the app:
**Help → 🧭 Two Books tab** explains how to use each page and how to read the
statistics. You can point students there, or build new lectures later — nothing
is required.

---

## What to tell students (one line)

"The app has been updated. Your link is the same. The Disjoint-Letters page now
groups its tabs under Position / Sequence / Semantic — the lecture steps are the
same, just one click deeper — and there are new optional sections (Signal,
Biology) with a built-in guide under Help → Two Books."

## If you ever need the old v1.2 app back

v1.2 is preserved in the Space's history (commit 0d18139). It can be restored at
any time — just ask and it can be redeployed.
