# Concept Atlas — Reorganization Plan (apply + test in a LOCAL dev session)

**Goal:** every section must clearly STAND OUT and be NUMBERED; the flagship (concept profile) must not be buried;
the page must be navigable, not one long scroll. Do this locally (`streamlit run app.py`) so each step is tested.

---

## 1. Target structure — five NUMBERED tabs (st.tabs)

Replace the single long scroll with tabs. Numbered labels so they stand out and orient the user:

```
1 · 🗺️ Map      2 · 🧬 Concept profile      3 · 🗂️ Families & themes      4 · 🌐 Sūra map      5 · 🔬 Metrics
```

- **Tab 1 · Map** — scope radio + KPIs + map-mode + the 2-D/3-D network (the whole / elephant). Default tab.
- **Tab 2 · Concept profile** — THE FLAGSHIP, surfaced here (not buried). The `🔍 Pick a concept` selectbox +
  the registry-driven profile panel (breadcrumb whole›family›concept, structural type, multi-layer reading,
  measured attributes, close-up button).
- **Tab 3 · Families & themes** — the ranked "theme sizes" landscape + Map-at-a-glance + per-theme detail expander.
- **Tab 4 · Sūra map** — the 114-sūra semantic map + cluster-metrics (whole scope); footprint + related (sūra scope).
- **Tab 5 · Metrics** — the centrality data-table + its column guide.

## 2. Make each section STAND OUT (design spec)

- **Numbered section header component** — one helper, used at the top of each tab:
  ```python
  def section_header(num, title, subtitle=""):
      st.markdown(
          f"<div style='background:linear-gradient(90deg,#1D3557,#274b73);border-radius:10px;"
          f"padding:10px 16px;margin:2px 0 10px'>"
          f"<span style='font-size:20px;font-weight:800;color:#fff'>{num} · {title}</span>"
          + (f"<div style='font-size:13px;color:#EAF2FB;margin-top:2px'>{subtitle}</div>" if subtitle else "")
          + "</div>", unsafe_allow_html=True)
  ```
  Big, coloured, numbered — impossible to miss. Replaces the thin `layer()` pills inside tabs.
- **Dividers** (`st.divider()`) between sub-blocks within a tab.
- **Generous spacing** — a blank `st.write("")` between sub-sections; don't stack headers on content.
- **Colour accent per tab** (optional): a thin left-border tint matching the section (navy/green/blue) so tabs feel distinct.

## 3. Engineering approach (why it's safe locally, not remotely)

The blocker remotely was re-indenting big nested blocks with no compile check. Locally you run + see errors instantly.

1. **Hoist all computation above the tabs.** Move the metrics block (`_tG = nx.Graph()… _deg… _bet… _clo… _clu…`,
   currently ~line 1017) to right AFTER `build_atlas`/`d = …` (top). Then every tab can use `_deg/_bet` regardless of order.
   *(Test: no `NameError`; the data table still renders.)*
2. **Create tabs once, after computation:** `t_map, t_prof, t_fam, t_sura, t_met = st.tabs(["1 · 🗺️ Map", "2 · 🧬 Concept profile", "3 · 🗂️ Families & themes", "4 · 🌐 Sūra map", "5 · 🔬 Metrics"])`.
3. **Wrap each existing render block in `with t_X:`** (indent the block +4). Streamlit lets you write into tabs out of
   order, so you do NOT need to reorder — just wrap in place. Do ONE tab at a time; run the app after each.
4. **Scope-conditionals stay inside their tab** — e.g. the `if _scope == "A sūra"` footprint/related blocks live inside
   `with t_sura:`; the `if _scope == "Whole Qur'ān"` 114-map lives there too. The `if` stays; only the wrapper is added.
5. **Delete the old `layer(n, …)` pills** inside tabs (replaced by `section_header`), and remove the "On this page"
   line (tabs replace it).

## 4. Apply + test checklist (local)

- [ ] `streamlit run app.py` → open Concept Atlas.
- [ ] Hoist metrics compute; confirm no NameError, data table intact.
- [ ] Add the 5 tabs; wrap Tab 1 (Map) first → run → map renders under Tab 1.
- [ ] Wrap Tab 2 (Concept profile) → run → picking قلب/رحم shows the profile under Tab 2.
- [ ] Wrap Tabs 3/4/5 one at a time → run after each.
- [ ] Switch Scope (Whole ↔ A sūra ↔ Position band) in each tab → confirm the right conditional content shows.
- [ ] Confirm 3-D toggle still works in Tab 1; CSV download in Tab 5.
- [ ] Visual pass: each tab opens with a big numbered `section_header`; dividers between sub-blocks; no dead space.

## 5. Result
A page where the five sections are numbered tabs that stand out, the concept profile is one click (not a deep scroll),
and the 3-D map is the centerpiece — the "sections stand out / user never lost" fix, done safely with live testing.
