<!-- PRESERVED: original application README (also used as the Hugging Face Space card).
     During the tree migration this becomes app/README.md. The Hugging Face front-matter
     below is HF-specific and will be dropped once the app moves to GitHub-based hosting. -->

---
title: Quran Root Explorer
emoji: 📖
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
license: mit
short_description: Arabic roots in the Quran — networks & motifs
---

# Quran Root Explorer

An interactive web app for exploring the **6,236 ayahs and 1,701 unique Arabic
roots of the Quran**. Type any root and get:

- A per-root profile (surah distribution, position-in-ayah, surface forms)
- A co-occurrence network with up to 16 different graph visualizations
  (force-directed, chord, adjacency matrix, MST backbone, k-core layers,
  community subnetworks, ego networks, Sankey flow, arc diagrams, …)
- Meccan vs. Medinan temporal analysis (revelation-order aware)
- Pairwise overlap heatmaps and metric cross-references (PMI, Jaccard, P(B|A))
- Motif galleries (dyads, triads, tetrads, pentads)
- Morphology breakdowns (particle prefixes/suffixes)
- A full statistics page with TF-IDF, hypergeometric enrichment,
  cumulative trajectories, and more
- One-click export to **PDF** (works on every OS), interactive HTML zip
  (best on desktop), and a 13-sheet Excel workbook
- A **📚 Two Books** section reading the same corpus as an ordered *signal* and a
  *genome*-style object: al-Muqaṭṭaʿāt as a positional pointer (Disjoint Letters),
  signal analysis (autocorrelation, dispersion, FFT + wavelet), biology-style
  base/codon composition, and a cross-domain Benjamini–Hochberg FDR summary —
  every test validated against a permutation null, computed live from the corpus

## How to use

1. Open the app in any browser — iPhone, iPad, Android phone, laptop, desktop
2. Type one or more Arabic roots in the input box (e.g. `رحم` or `عدل قسط`)
3. Browse the analysis pages from the left sidebar — the root-tools pages plus the new **📚 Two Books** section (Disjoint Letters · Signal · Biology · FDR Summary)
4. Click **⬇️ Export** to download everything as PDF / HTML / Excel

No installation, no login. Everything runs in your browser.

## Privacy

The app counts anonymous visits to help guide future improvements.  Only an
opaque per-browser UUID and a two-letter ISO country code are stored — no
IP addresses, no names, no emails, no precise locations.  Visitors can
clear their UUID at any time by clearing browser localStorage.  The
admin-only `📊 Usage` page in the sidebar is password-protected.

## License

The application code is released under CC0 / public domain along with the rest
of the author's own work (see ../LICENSE). (The original Space card stated MIT;
the project has since standardized on CC0 for the author's own material.)

## Tech stack

Streamlit · Plotly · NetworkX · pandas · openpyxl · kaleido + Chromium ·
SQLite + Hugging Face Datasets (analytics)
