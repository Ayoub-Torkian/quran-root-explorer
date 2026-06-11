# re-deploy 1779672831
"""interpret.py — strictly data-driven session narrative.

The final synthesis of every other module. Every sentence is computed
from numbers in this session. No conjecture, no generalisation, no
theological interpretation.

Sections (in order):
  1. Headline insights — top take-aways derived across modules
  2. Session summary
  3. Per-root deep profile (for each input root)
  4. Pairwise observations (if >=2 input roots)
  5. Network structure
  6. Community structure
  7. Motif observations (triads)
  8. Temporal patterns (Meccan vs Medinan)
  9. Surface-form patterns
 10. Morphology patterns
 11. Position patterns
 12. Topic Modelling   (lazy — only if topics cache is already built)
 13. Surface-form Divergence (lazy — only if cache is already built)
 14. What this analysis does and does not say
"""
from __future__ import annotations

import math
from collections import Counter


# ─────────────────────────────────────────────────────────────────
# Tiny helpers
# ─────────────────────────────────────────────────────────────────
def _fmt_root(r: str) -> str:
    return f"`{r}`"


def _round(x, n=3):
    try:
        v = float(x)
        if math.isnan(v) or math.isinf(v):
            return None
        return round(v, n)
    except Exception:
        return None


def _safe_int(x, default=0):
    try:
        return int(x)
    except Exception:
        return default


def _pct(num, denom, decimals=1) -> str:
    try:
        if denom == 0:
            return "0%"
        return f"{round(100.0 * num / denom, decimals)}%"
    except Exception:
        return "n/a"


# ─────────────────────────────────────────────────────────────────
# Headline insights — synthesis across modules, top 3-5
# ─────────────────────────────────────────────────────────────────
def headline_facts(R, corpus) -> list[str]:
    facts: list[str] = []
    roots = R.get("input_roots") or []
    occ = R.get("occurrences")
    match_ayahs = R.get("match_ayahs", [])

    # 1. Coverage
    total_ayahs_in_corpus = len(getattr(corpus, "df", []))
    if total_ayahs_in_corpus and len(match_ayahs):
        cov = _pct(len(match_ayahs), total_ayahs_in_corpus, 2)
        facts.append(
            f"Your input root(s) appear in **{len(match_ayahs)}** ayahs — "
            f"**{cov}** of the {total_ayahs_in_corpus:,} ayahs in the corpus."
        )

    # 2. Rarity headline
    rar = R.get("rarity")
    if rar is not None and len(rar) > 0:
        for _, r in rar.iterrows():
            facts.append(
                f"{_fmt_root(r['Input Root'])} sits at the **{r['Percentile']}th** "
                f"frequency percentile ({r['Tier']}) — z-score "
                f"**{r['Z-score']}** vs. the corpus mean."
            )

    # 3. Temporal skew (single root or summary)
    if R.get("has_rev_order") and occ is not None and len(occ) > 0:
        try:
            from analysis import COL_SURAH
            df = getattr(corpus, "df", None)
            rev = getattr(corpus, "rev_order_of_surah", {}) or {}
            if df is not None and rev:
                for root in roots:
                    sub = occ[occ["Input Root"] == root] if "Input Root" in occ.columns else None
                    if sub is None or len(sub) == 0:
                        continue
                    n_mec = n_med = 0
                    for _, row in sub.iterrows():
                        s = int(row["Surah #"])
                        ro = rev.get(s)
                        if ro is None:
                            continue
                        if ro <= 86:
                            n_mec += 1
                        else:
                            n_med += 1
                    tot = n_mec + n_med
                    if tot > 0:
                        dom = "Meccan" if n_mec > n_med else ("Medinan" if n_med > n_mec else "evenly split")
                        facts.append(
                            f"{_fmt_root(root)}: **{_pct(n_mec, tot)} Meccan / "
                            f"{_pct(n_med, tot)} Medinan** "
                            f"(dominant phase: **{dom}**)."
                        )
        except Exception:
            pass

    # 4. Centrality headline
    centr = R.get("centrality")
    if centr is not None and len(centr) > 0:
        for root in roots:
            name_col = "Root" if "Root" in centr.columns else "root"
            wd_col = "Weighted Degree" if "Weighted Degree" in centr.columns else "weighted_degree"
            btw_col = "Betweenness" if "Betweenness" in centr.columns else "betweenness"
            try:
                row = centr[centr[name_col] == root]
                if len(row) > 0:
                    wd = _safe_int(row.iloc[0][wd_col])
                    btw = _round(row.iloc[0][btw_col])
                    facts.append(
                        f"{_fmt_root(root)} carries weighted degree **{wd}** "
                        f"and betweenness **{btw}** inside its session network."
                    )
            except Exception:
                continue

    # 5. Top partner pair (most-shared)
    g = R.get("graph")
    if g is not None and g.number_of_edges() > 0:
        try:
            top_edge = max(g.edges(data=True), key=lambda e: e[2].get("weight", 0))
            a, b, d = top_edge
            facts.append(
                f"Strongest pairwise link in the session: **{a} ↔ {b}** "
                f"({_safe_int(d.get('weight', 0))} shared ayahs)."
            )
        except Exception:
            pass

    return facts


# ─────────────────────────────────────────────────────────────────
# Session summary
# ─────────────────────────────────────────────────────────────────
def session_summary(R) -> list[str]:
    roots = R.get("input_roots") or []
    return [
        f"Input roots: {', '.join(_fmt_root(r) for r in roots) or '(none)'}.",
        f"Ayahs matched in corpus: **{len(R.get('match_ayahs', []))}**.",
        f"Normalisation: **{'ON (tolerant)' if R.get('normalize') else 'OFF (exact)'}**.",
        f"Top partners shown: **{R.get('top_partners', 'n/a')}**, "
        f"min edge weight: **{R.get('min_weight', 'n/a')}**.",
    ]


# ─────────────────────────────────────────────────────────────────
# Per-root deep profile
# ─────────────────────────────────────────────────────────────────
def per_root_facts(R, corpus, root: str) -> list[str]:
    facts: list[str] = []
    occ = R.get("occurrences")
    if occ is None or len(occ) == 0 or "Input Root" not in occ.columns:
        return [f"No occurrences of {_fmt_root(root)} recorded in this session."]

    sub = occ[occ["Input Root"] == root]
    if len(sub) == 0:
        return [f"{_fmt_root(root)} did not match any ayah in this session."]

    # Coverage
    if {"Surah #", "Ayah #"}.issubset(sub.columns):
        n_ayahs = sub.drop_duplicates(["Surah #", "Ayah #"]).shape[0]
        n_surahs = sub["Surah #"].nunique()
    else:
        n_ayahs = len(sub)
        n_surahs = 0
    total_hits = int(sub["Hit Count"].sum()) if "Hit Count" in sub.columns else n_ayahs

    facts.append(
        f"**Coverage** — {_fmt_root(root)} appears in **{n_ayahs}** ayahs across "
        f"**{n_surahs} of 114** surahs ({_pct(n_surahs, 114)}). "
        f"Total token hits: **{total_hits}**."
    )
    if total_hits > n_ayahs:
        facts.append(
            f"In **{int((sub['Hit Count'] > 1).sum())}** of those {n_ayahs} ayahs "
            f"the root appears more than once (intensifier / repeated reference)."
        )

    # Top surahs by raw count + by per-ayah density
    if "Surah #" in sub.columns and n_surahs > 0:
        top = sub.groupby("Surah #").size().sort_values(ascending=False).head(5)
        items = []
        sn_col = "Surah Name" if "Surah Name" in sub.columns else None
        for s, k in top.items():
            label = f"surah {int(s)}"
            if sn_col:
                try:
                    nm = sub[sub["Surah #"] == s][sn_col].iloc[0]
                    label = f"{int(s)} {nm}"
                except Exception:
                    pass
            items.append(f"{label} ({int(k)})")
        facts.append("**Top surahs by ayah count:** " + "; ".join(items) + ".")

        # Concentration — top-3 surahs share what % of all ayahs?
        top3 = sub.groupby("Surah #").size().sort_values(ascending=False).head(3).sum()
        facts.append(
            f"Concentration: the top-3 surahs hold **{_pct(int(top3), n_ayahs)}** "
            f"of all {_fmt_root(root)} occurrences."
        )

    # Rarity context
    rar = R.get("rarity")
    if rar is not None and len(rar) > 0 and "Input Root" in rar.columns:
        row = rar[rar["Input Root"] == root]
        if len(row) > 0:
            r0 = row.iloc[0]
            facts.append(
                f"**Rarity** — frequency rank percentile **{r0['Percentile']}** "
                f"({r0['Tier']}); corpus median is **{int(r0['Corpus Median'])}** ayahs, "
                f"mean **{r0['Corpus Mean']}** (z = **{r0['Z-score']}**)."
            )

    # First / last
    fl = R.get("first_last")
    if fl is not None and len(fl) > 0 and "Input Root" in fl.columns:
        row = fl[fl["Input Root"] == root]
        if len(row) > 0:
            r0 = row.iloc[0]
            facts.append(
                f"First occurrence: **{r0['First (S:A)']}** ({r0['First Surah Name']}). "
                f"Last occurrence: **{r0['Last (S:A)']}** ({r0['Last Surah Name']})."
            )

    # Top co-occurrence partners with P(partner|root)
    g = R.get("graph")
    if g is not None and root in g.nodes:
        nbrs = sorted(g[root].items(),
                      key=lambda kv: -kv[1].get("weight", 0))[:7]
        if nbrs:
            bits = []
            for n, d in nbrs:
                w = _safe_int(d.get("weight", 0))
                pct = _pct(w, n_ayahs) if n_ayahs else "n/a"
                bits.append(f"{n} ({w}, {pct})")
            facts.append(
                "**Top co-occurrence partners** (root, shared ayahs, "
                f"P(partner|{root})): " + ", ".join(bits) + "."
            )

    # Surface-form distribution
    sf = R.get("sforms")
    if sf is not None and len(sf) > 0:
        if "Input Root" in sf.columns and "Surface Form" in sf.columns and "Count" in sf.columns:
            sub_sf = sf[sf["Input Root"] == root].sort_values("Count", ascending=False)
            total_sf = sub_sf["Count"].sum()
            top_sf = sub_sf.head(5)
            if total_sf > 0:
                bits = [f"{r['Surface Form']} ({int(r['Count'])}, "
                        f"{_pct(int(r['Count']), int(total_sf))})"
                        for _, r in top_sf.iterrows()]
                facts.append(
                    f"**Surface forms** — {len(sub_sf)} distinct realisations. "
                    f"Top 5: " + ", ".join(bits) + "."
                )

    # Position-in-ayah average
    pos = R.get("position")
    if pos is not None and len(pos) > 0 and "Input Root" in pos.columns:
        sub_p = pos[pos["Input Root"] == root]
        if len(sub_p) > 0 and "Position in ayah (0..1)" in sub_p.columns:
            avg_p = float(sub_p["Position in ayah (0..1)"].mean())
            avg_len = float(sub_p["Ayah length (roots)"].mean())
            zone = ("opening third" if avg_p < 0.33
                    else "middle third" if avg_p < 0.66 else "closing third")
            facts.append(
                f"**Position** — average appearance at position "
                f"**{avg_p:.2f}** (0 = start, 1 = end → {zone}); "
                f"average ayah length: **{avg_len:.1f}** roots."
            )

    # Meccan vs Medinan (per root)
    if R.get("has_rev_order"):
        try:
            rev = getattr(corpus, "rev_order_of_surah", {}) or {}
            n_mec = n_med = 0
            for _, row in sub.iterrows():
                ro = rev.get(int(row["Surah #"]))
                if ro is None:
                    continue
                if ro <= 86:
                    n_mec += 1
                else:
                    n_med += 1
            tot = n_mec + n_med
            if tot > 0:
                facts.append(
                    f"**Revelation phase** — Meccan **{n_mec}** "
                    f"({_pct(n_mec, tot)}), Medinan **{n_med}** "
                    f"({_pct(n_med, tot)})."
                )
        except Exception:
            pass

    # Morphology — top prefix/suffix patterns
    morph = R.get("morphology")
    if morph is not None and len(morph) > 0 and "Input Root" in morph.columns:
        sub_m = morph[morph["Input Root"] == root]
        if len(sub_m) > 0:
            for col_label, col_name in (("prefix", "Prefix"), ("suffix", "Suffix")):
                if col_name not in sub_m.columns:
                    continue
                vals = sub_m[col_name].astype(str)
                top_morph = Counter(vals).most_common(4)
                if top_morph:
                    bits = [f"{p or '(none)'} ({c})" for p, c in top_morph]
                    facts.append(f"**Top {col_label} patterns:** " + ", ".join(bits) + ".")

    # Network role
    centr = R.get("centrality")
    if centr is not None and len(centr) > 0:
        name_col = "Root" if "Root" in centr.columns else "root"
        try:
            sorted_centr = centr.sort_values(
                "Weighted Degree" if "Weighted Degree" in centr.columns else "weighted_degree",
                ascending=False
            ).reset_index(drop=True)
            rank_row = sorted_centr[sorted_centr[name_col] == root]
            if len(rank_row) > 0:
                rank = int(rank_row.index[0]) + 1
                facts.append(
                    f"**Network role** — weighted-degree rank **{rank} of "
                    f"{len(sorted_centr)}** in the session ego-network."
                )
        except Exception:
            pass

    # Community membership
    comm_raw = R.get("communities") or {}
    if isinstance(comm_raw, dict) and root in comm_raw:
        cid = comm_raw[root]
        comembers = sorted([n for n, c in comm_raw.items() if c == cid and n != root])[:8]
        if comembers:
            facts.append(
                f"**Cluster** — Louvain places {_fmt_root(root)} with "
                f"**{len(comembers)} other root(s)** in the same community: "
                f"{', '.join(comembers)}."
            )

    return facts


# ─────────────────────────────────────────────────────────────────
# Network structure
# ─────────────────────────────────────────────────────────────────
def network_structure_facts(R) -> list[str]:
    import networkx as nx
    facts: list[str] = []
    g = R.get("graph")
    if g is None or g.number_of_nodes() == 0:
        return ["Network is empty — no observations to report."]

    N, M = g.number_of_nodes(), g.number_of_edges()
    facts.append(
        f"Session ego-network: **{N}** nodes (input roots + their top partners) "
        f"and **{M}** edges. Density: **{_round(nx.density(g))}**."
    )

    centr = R.get("centrality")
    if centr is not None and len(centr) > 0:
        name_col = "Root" if "Root" in centr.columns else (
            "root" if "root" in centr.columns else None)
        wd_col = "Weighted Degree" if "Weighted Degree" in centr.columns else (
            "weighted_degree" if "weighted_degree" in centr.columns else None)
        btw_col = "Betweenness" if "Betweenness" in centr.columns else (
            "betweenness" if "betweenness" in centr.columns else None)
        eig_col = "Eigenvector" if "Eigenvector" in centr.columns else (
            "eigenvector" if "eigenvector" in centr.columns else None)
        if name_col and wd_col:
            top = centr.sort_values(wd_col, ascending=False).head(5)
            facts.append(
                "Highest weighted degree (most ayah-sharing): " +
                ", ".join(f"{r[name_col]} ({_safe_int(r[wd_col])})" for _, r in top.iterrows())
                + "."
            )
        if name_col and btw_col:
            sub = centr[centr[btw_col] > 0].sort_values(btw_col, ascending=False).head(5)
            if len(sub) > 0:
                facts.append(
                    "Highest betweenness (bridge roots — removing them splits subgroups): " +
                    ", ".join(f"{r[name_col]} ({_round(r[btw_col])})" for _, r in sub.iterrows())
                    + "."
                )
        if name_col and eig_col:
            top = centr.sort_values(eig_col, ascending=False).head(3)
            facts.append(
                "Highest eigenvector centrality (well-connected to other well-connected roots): " +
                ", ".join(f"{r[name_col]} ({_round(r[eig_col])})" for _, r in top.iterrows())
                + "."
            )

    ns = R.get("net_stats") or {}
    mod = ns.get("modularity")
    if mod is not None:
        facts.append(
            f"Modularity: **{_round(mod)}** (0 = no clusters; 1 = perfectly "
            f"separated clusters)."
        )
        diam = ns.get("diameter")
    if diam is not None and diam > 0:
        facts.append(f"Diameter: **{int(diam)}** (longest shortest-path between any two roots).")
    arts = ns.get("articulation_points") or []
    if arts:
        facts.append(
            f"Articulation points (removing any one disconnects the network): "
            f"{', '.join(sorted(arts))}."
        )
    bridges = ns.get("bridge_edges") or []
    if bridges:
        items = [f"{a}—{b}" for a, b in list(bridges)[:5]]
        more = "" if len(bridges) <= 5 else f" (+{len(bridges)-5} more)"
        facts.append(f"Bridge edges (the only path between subgroups): " + ", ".join(items) + more + ".")
    return facts


def community_facts(R) -> list[str]:
    facts: list[str] = []
    comm_raw = R.get("communities") or {}
    if not comm_raw:
        return facts
    groups: list[list[str]] = []
    if isinstance(comm_raw, dict):
        by_id: dict = {}
        for node, cid in comm_raw.items():
            by_id.setdefault(cid, []).append(node)
        groups = list(by_id.values())
    elif isinstance(comm_raw, list):
        groups = [list(c) for c in comm_raw]
    if not groups:
        return facts
    sizes = sorted([len(c) for c in groups], reverse=True)
    facts.append(f"Louvain detects **{len(groups)}** communities. Sizes: {', '.join(str(s) for s in sizes)}.")
    for i, c in enumerate(sorted(groups, key=len, reverse=True)[:5], 1):
        members = sorted(c)[:10]
        extra = "" if len(c) <= 10 else f", +{len(c) - 10} more"
        facts.append(f"Community {i} ({len(c)} roots): {', '.join(members)}{extra}.")
    return facts


def pairwise_facts(R) -> list[str]:
    """v1.2: also appends a [tier] label derived from lift = P(A&B)/[P(A)·P(B)].

    The tier is threshold-based only (stipulative / embedded / mild /
    independent) — no interpretation beyond what the threshold says.
    See pair_classification.py.
    """
    try:
        from pair_classification import classify_lift   # local import
    except Exception:
        classify_lift = None  # falls back to v1.1 behaviour

    facts: list[str] = []
    roots = R.get("input_roots") or []
    if len(roots) < 2:
        return facts
    overlap = R.get("overlap")
    g = R.get("graph")
    occ = R.get("occurrences")

    # corpus size for lift (best-effort)
    n_corpus = None
    try:
        from state import get_corpus
        n_corpus = get_corpus().n_ayahs
    except Exception:
        pass

    for i, a in enumerate(roots):
        for b in roots[i + 1:]:
            shared = None
            if overlap is not None and a in overlap.index and b in overlap.columns:
                try:
                    shared = int(overlap.loc[a, b])
                except Exception:
                    pass
            n_a = n_b = 0
            if occ is not None and "Input Root" in occ.columns and shared is not None:
                n_a = occ[occ["Input Root"] == a].drop_duplicates(["Surah #", "Ayah #"]).shape[0]
                n_b = occ[occ["Input Root"] == b].drop_duplicates(["Surah #", "Ayah #"]).shape[0]
            edge_w = None
            if g is not None and g.has_edge(a, b):
                edge_w = _safe_int(g[a][b].get("weight", 0))
            if (shared is None or shared == 0) and edge_w is None:
                facts.append(f"{_fmt_root(a)} <-> {_fmt_root(b)}: no shared ayahs in this session.")
                continue
            parts = []
            if shared is not None and shared > 0:
                parts.append(f"**{shared}** shared ayahs")
                if n_a > 0:
                    parts.append(f"P({b}|{a}) = **{_pct(shared, n_a)}**")
                if n_b > 0:
                    parts.append(f"P({a}|{b}) = **{_pct(shared, n_b)}**")
            if edge_w is not None and (shared is None or edge_w != shared):
                parts.append(f"edge weight **{edge_w}**")

            # v1.2 — tier label
            tier_str = ""
            if (classify_lift is not None and n_corpus
                    and n_a and n_b and shared and shared > 0):
                lift = (shared / n_corpus) / ((n_a / n_corpus) * (n_b / n_corpus))
                _, label, _, _ = classify_lift(lift)
                tier_str = f" · lift = **{lift:.2f}** · tier: **{label}**"

            facts.append(f"{_fmt_root(a)} <-> {_fmt_root(b)}: {', '.join(parts)}{tier_str}.")
    return facts


def motif_facts(R) -> list[str]:
    facts: list[str] = []
    tri = R.get("triangles")
    if tri is None or len(tri) == 0:
        return ["No closed 3-root motifs (triads) in the current network."]
    n_tri = len(tri)
    facts.append(f"Closed triads (3 roots ALL sharing the same ayah): **{n_tri}**.")
    if {"Root A", "Root B", "Root C", "Sum Weight"}.issubset(tri.columns):
        top = tri.sort_values("Sum Weight", ascending=False).head(5)
        for _, r in top.iterrows():
            a, b, c = r["Root A"], r["Root B"], r["Root C"]
            w = _safe_int(r["Sum Weight"])
            facts.append(f"Strong triad: {{{a}, {b}, {c}}} - total pairwise weight **{w}**.")
        roots = set(R.get("input_roots") or [])
        if roots:
            mask = (tri["Root A"].isin(roots) | tri["Root B"].isin(roots) | tri["Root C"].isin(roots))
            sub = tri[mask]
            if len(sub) > 0:
                facts.append(f"Triads containing one of your input roots: **{len(sub)}** of {n_tri} total ({_pct(len(sub), n_tri)}).")
    return facts


def temporal_facts(R) -> list[str]:
    facts: list[str] = []
    if not R.get("has_rev_order"):
        return facts
    gm = R.get("g_meccan")
    gd = R.get("g_medinan")
    if gm is not None and gd is not None:
        facts.append(f"Meccan-only sub-network: **{gm.number_of_nodes()}** nodes, **{gm.number_of_edges()}** edges. Medinan-only sub-network: **{gd.number_of_nodes()}** nodes, **{gd.number_of_edges()}** edges.")
    only_m = R.get("phase_only_meccan") or []
    only_d = R.get("phase_only_medinan") or []
    both = R.get("phase_in_both") or []
    total_pairs = len(only_m) + len(only_d) + len(both)
    if total_pairs > 0:
        facts.append(f"Of **{total_pairs}** root pairs in the network: **{len(only_m)}** ({_pct(len(only_m), total_pairs)}) are Meccan-only, **{len(only_d)}** ({_pct(len(only_d), total_pairs)}) Medinan-only, **{len(both)}** ({_pct(len(both), total_pairs)}) appear in both phases.")
    return facts


def surface_form_facts(R) -> list[str]:
    facts: list[str] = []
    sf = R.get("sforms")
    if sf is None or len(sf) == 0:
        return facts
    if "Surface Form" not in sf.columns or "Input Root" not in sf.columns:
        return facts
    total_forms = sf.groupby("Input Root")["Surface Form"].nunique()
    if len(total_forms) > 0:
        items = [f"{r}: {n} forms" for r, n in total_forms.items()]
        facts.append("Distinct surface forms per root: " + "; ".join(items) + ".")
    return facts


def position_facts(R) -> list[str]:
    facts: list[str] = []
    pos = R.get("position")
    if pos is None or len(pos) == 0:
        return facts
    if "Input Root" not in pos.columns or "Position in ayah (0..1)" not in pos.columns:
        return facts
    grouped = pos.groupby("Input Root")["Position in ayah (0..1)"].mean()
    items = []
    for r, v in grouped.items():
        zone = ("opening" if v < 0.33 else "middle" if v < 0.66 else "closing")
        items.append(f"{r}: avg {v:.2f} ({zone} third)")
    if items:
        facts.append("Mean position in ayah (0=start, 1=end): " + "; ".join(items) + ".")
    return facts


def topic_facts(corpus, roots) -> list[str]:
    facts: list[str] = []
    try:
        import topics as T
        if not T.CACHE_PATH.exists():
            facts.append("Topic-modelling cache is not yet built. Open the **Topic Modeling** page once - the first build takes a few minutes; afterwards this section populates automatically.")
            return facts
        cache = T.compute(corpus)
        if cache.get("n_nodes", 0) == 0:
            return facts
    except Exception:
        return facts
    for r in roots:
        try:
            ti, members, mean_s = T.get_topic_for_root(cache, r)
            if ti >= 0:
                others = [m for m in members if m != r]
                shown = ", ".join(sorted(others)[:10])
                more = "" if len(others) <= 10 else f" +{len(others) - 10} more"
                facts.append(f"{_fmt_root(r)} sits inside **Topic {ti + 1}** ({len(members)} roots, mean stability {mean_s:.2f}).")
                if others:
                    facts.append(f"  Topic members: {shown}{more}.")
                quad = T.quadrant_lists(cache, r, k=5)
                if quad.get("contrastive"):
                    bits = ", ".join(f"{n} (S1={s1:.2f}, S2={s2:.2f})" for n, s1, s2 in quad["contrastive"][:3])
                    facts.append(f"  Contrastive partners of {_fmt_root(r)} (share verses but live in different contexts -> likely antithetical): {bits}.")
                if quad.get("distributional_synonym"):
                    bits = ", ".join(f"{n} (S1={s1:.2f}, S2={s2:.2f})" for n, s1, s2 in quad["distributional_synonym"][:3])
                    facts.append(f"  Distributional synonyms of {_fmt_root(r)} (rarely co-occur but share contexts -> latent semantic kin): {bits}.")
            else:
                facts.append(f"{_fmt_root(r)} is not assigned to any stable topic at the current threshold.")
        except Exception:
            continue
    return facts


def surface_split_facts(corpus, roots) -> list[str]:
    facts: list[str] = []
    try:
        import surface_divergence as SD
        if not SD.CACHE_PATH.exists():
            return facts
        cache = SD.compute(corpus)
        if cache.get("n_roots_scanned", 0) == 0:
            return facts
    except Exception:
        return facts
    for r in roots:
        s = SD.get_split(cache, r)
        if not s:
            continue
        n_clusters = len(s["clusters"])
        facts.append(f"{_fmt_root(r)} is flagged as semantically split: **{n_clusters}** surface-form clusters, max JSD **{s['max_jsd']:.2f}**, stability {s['stability']:.2f}.")
        for cl_id, forms in s["clusters"].items():
            facts.append(f"  Cluster {cl_id}: surface forms {', '.join(forms)}.")
    return facts


def caveats() -> list[str]:
    return [
        "Every line above is a count or statistic from your input session - not a theological interpretation.",
        "An edge between two roots means they share ayahs. It does **not** distinguish synonymy, contrast, or causation.",
        "P(A|B) is the share of B's ayahs in which A also appears - it is not a meaning, only a frequency.",
        "Mecca/Medina splits use the Egyptian-standard mushaf-revelation-order table; alternative orderings would change the numbers.",
        "To see **how** two roots pair (reinforcement vs. contrast), open the **Ayah Browser** page and read the actual verses where they co-occur.",
    ]


def generate(R, corpus) -> dict:
    global _NARR_R, _NARR_CORPUS
    _NARR_R = R
    _NARR_CORPUS = corpus
    roots = R.get("input_roots") or []
    sections: dict = {}
    sections["Headline insights"] = headline_facts(R, corpus)
    sections["Session summary"] = session_summary(R)
    for r in roots:
        sections[f"Deep profile - {r}"] = per_root_facts(R, corpus, r)
    if len(roots) >= 2:
        sections["Pairwise observations (your input roots)"] = pairwise_facts(R)
    sections["Network structure"] = network_structure_facts(R)
    sections["Community structure"] = community_facts(R)
    sections["Motif observations"] = motif_facts(R)
    tf = temporal_facts(R)
    if tf:
        sections["Temporal - Meccan vs. Medinan"] = tf
    sff = surface_form_facts(R)
    if sff:
        sections["Surface-form coverage"] = sff
    pf = position_facts(R)
    if pf:
        sections["Position-in-ayah"] = pf
    topic_s = topic_facts(corpus, roots)
    if topic_s:
        sections["Topic Modelling - your roots in the corpus-wide map"] = topic_s
    split_s = surface_split_facts(corpus, roots)
    if split_s:
        sections["Surface-form divergence"] = split_s
    sections["What this analysis does and does not say"] = caveats()
    sections = _attach_significance(sections)
    return sections


# ─────────────────────────────────────────────────────────────────
# Plain-English significance footers for each section
# ─────────────────────────────────────────────────────────────────
_SIGNIFICANCE: dict[str, str] = {
    "Headline insights":
        "**What this means.** These lines compress the rest of the page. "
        "If a reader only saw this section they would still know: how much of "
        "the corpus your root touches, how rare it is, which revelation "
        "phase dominates, how central it is in its network, and who its "
        "single strongest verse-companion is. Use it as a 30-second elevator "
        "summary of the analysis.",

    # Session summary is pure metadata — no narrative needed.

    "Pairwise observations (your input roots)":
        "**What this means.** P(B|A) is the share of A's ayahs in which B "
        "also appears. It is *not* symmetric: if P(B|A)=80% but P(A|B)=10%, "
        "B almost always rides along with A, but A is just one of many "
        "companions B has. That asymmetry is the key signal — it tells you "
        "which root is the *anchor* in the pair and which is the *follower*.",

    "Network structure":
        "**What this means.** Density measures how interconnected the "
        "partner roots are with each other (not just with you). "
        "**Modularity** says whether the network breaks cleanly into "
        "sub-clusters — a high value means several distinct semantic "
        "neighbourhoods coexist around your root, suggesting it serves "
        "multiple thematic registers. **Betweenness** identifies *bridge* "
        "roots whose removal would split the network — those bridges "
        "frequently carry semantic pivot meaning (a single root linking "
        "otherwise-separate registers, e.g. mercy linking justice to "
        "guidance).",

    "Community structure":
        "**What this means.** A community is a tight knot of roots that "
        "appear together more often than chance. Each one usually "
        "corresponds to a *thematic register* — e.g. legal terminology "
        "clusters, devotional terms cluster, eschatology clusters. The "
        "communities your root belongs to define its semantic family.",

    "Motif observations":
        "**What this means.** A closed triad is three roots that ALL "
        "appear together in the same ayah. Triads are the smallest "
        "non-trivial unit of conceptual combination — they show recurring "
        "three-way associations the text returns to. A high triad count "
        "containing your root means it participates in many "
        "well-integrated concept clusters; a low count means it tends to "
        "appear in pairs but not in tightly-knit groups.",

    "Temporal — Meccan vs. Medinan":
        "**What this means.** Meccan revelation focuses on creed, "
        "warnings, and reorientation; Medinan revelation focuses on law, "
        "community, and statecraft. A root that lives predominantly in "
        "Meccan verses is doing early-revelation theological work; a "
        "root predominantly Medinan is doing legal or communal work. "
        "Roots that appear robustly in both bridge the two phases and "
        "often carry the deepest conceptual continuity.",

    "Surface-form coverage":
        "**What this means.** The same triliteral root can produce "
        "dozens of surface forms — verb conjugations, masdars, active "
        "and passive participles, plural nouns. The count tells you how "
        "*morphologically diverse* the root is in the corpus. A root "
        "with few surface forms is grammatically narrow (often a name or "
        "a fixed term); a root with many forms is conceptually elastic "
        "and used in many syntactic roles.",

    "Position-in-ayah":
        "**What this means.** Position is meaningful in oral recitation. "
        "Roots in the *opening third* often set the topic of the ayah; "
        "roots in the *closing third* often carry emphasis or rhyme "
        "function. A consistent position pattern across many ayahs is "
        "evidence of a stable rhetorical role.",

    "Topic Modelling — your roots in the corpus-wide map":
        "**What this means.** Topic modelling uses two independent "
        "signals: co-occurrence (do they share verses?) and *distributional* "
        "similarity (do they appear in similar verse-contexts even when "
        "they don't co-occur?). The cross of the two reveals two findings "
        "you cannot get from co-occurrence alone:\n\n"
        "  • **Contrastive partners** (share verses, different contexts) "
        "are likely *antithetical* pairings — opposites the text "
        "deliberately places side-by-side.\n\n"
        "  • **Distributional synonyms** (different verses, similar "
        "contexts) are *latent semantic kin* — roots that mean closely "
        "related things even though they almost never appear together. "
        "These are invisible to reading alone and are the single most "
        "valuable output of this module.",

    "Surface-form divergence":
        "**What this means.** When the same triliteral root produces "
        "surface forms that travel with completely different partner "
        "roots, treating it as one node averages two distinct meanings. "
        "A flagged split means the root is genuinely *polysemous* in "
        "this corpus — each cluster is effectively a different concept "
        "wearing the same letters. Surface divergence is the empirical "
        "check on lexicographers' polysemy lists.",
}


def _significance_for(section_title: str) -> str | None:
    """Return the significance paragraph for a section. Per-root profile
    sections are matched by prefix so each input root gets the same footer."""
    if section_title in _SIGNIFICANCE:
        return _SIGNIFICANCE[section_title]
    if section_title.startswith("📍 Deep profile") or section_title.startswith("Deep profile"):
        return (
            "**What this means.** This block answers WHERE this root "
            "lives in the corpus, WHO it travels with, and HOW it is "
            "expressed. Concentration shows whether the root is a "
            "recurring theme of a few surahs or scattered everywhere; "
            "top partners show who it argues with or alongside; the "
            "Meccan/Medinan split places it in revelation history. The "
            "centrality rank tells you whether your root is a star "
            "(connects to many others) or a follower (connects to few)."
        )
    if section_title == "What this analysis does and does not say":
        return None  # caveats already explain themselves
    return None


_NARR_R = None
_NARR_CORPUS = None


def _attach_significance(sections: dict) -> dict:
    """Append a context-aware 'What this means' paragraph to each section
    based on the actual numbers for the current input root(s)."""
    out: dict = {}
    R, corpus = _NARR_R, _NARR_CORPUS
    roots = (R.get("input_roots") if R else None) or []
    for title, facts in sections.items():
        narr = _narrative_for(title, R, corpus, roots) if R is not None else None
        if not narr:
            narr = _significance_for(title)  # fallback to generic
        if narr and facts:
            out[title] = list(facts) + ["", f"_{narr}_"]
        else:
            out[title] = facts
    return out


# =====================================================================
# CONTEXT-AWARE NARRATIVE GENERATION
# Each section's "What this means" paragraph is built from the actual
# numbers in this session, not a generic description of the technique.
# =====================================================================

def _narrative_for(title, R, corpus, roots):
    if title is None or R is None or corpus is None:
        return None
    t = title.lower()
    if "headline" in t:
        return _narr_headline(R, corpus, roots)
    if "deep profile" in t:
        # Extract the root name after the dash
        for sep in (" - ", " — "):
            if sep in title:
                cand = title.split(sep)[-1].strip()
                if cand:
                    return _narr_deep(R, corpus, cand)
        return _narr_deep(R, corpus, roots[0] if roots else "")
    if "network structure" in t:
        return _narr_network(R, corpus, roots)
    if "community structure" in t:
        return _narr_community(R, corpus, roots)
    if "motif" in t:
        return _narr_motifs(R, corpus, roots)
    if "temporal" in t or "meccan" in t:
        return _narr_temporal(R, corpus, roots)
    if "pairwise" in t:
        return _narr_pairwise(R, corpus, roots)
    if "topic modelling" in t:
        return _narr_topics(R, corpus, roots)
    if "surface-form divergence" in t:
        return _narr_divergence(R, corpus, roots)
    return None


def _root_phase_split(R, corpus, root):
    occ = R.get("occurrences")
    if occ is None or "Input Root" not in occ.columns:
        return None, None, 0
    sub = occ[occ["Input Root"] == root]
    if len(sub) == 0 or "Surah #" not in sub.columns:
        return None, None, 0
    rev = getattr(corpus, "rev_order_of_surah", {}) or {}
    n_mec = n_med = 0
    for _, row in sub.iterrows():
        ro = rev.get(int(row["Surah #"]))
        if ro is None:
            continue
        if ro <= 86:
            n_mec += 1
        else:
            n_med += 1
    return n_mec, n_med, n_mec + n_med


def _root_centrality(R, root):
    centr = R.get("centrality")
    if centr is None or len(centr) == 0:
        return None, None
    name_col = "Root" if "Root" in centr.columns else "root"
    wd_col = "Weighted Degree" if "Weighted Degree" in centr.columns else "weighted_degree"
    btw_col = "Betweenness" if "Betweenness" in centr.columns else "betweenness"
    row = centr[centr[name_col] == root]
    if len(row) == 0:
        return None, None
    try:
        wd = _safe_int(row.iloc[0][wd_col])
    except Exception:
        wd = None
    try:
        btw = float(row.iloc[0][btw_col])
    except Exception:
        btw = None
    return wd, btw


def _root_top_partner(R, root):
    g = R.get("graph")
    if g is None or root not in g.nodes:
        return None, 0
    nbrs = sorted(g[root].items(), key=lambda kv: -kv[1].get("weight", 0))
    if not nbrs:
        return None, 0
    return nbrs[0][0], _safe_int(nbrs[0][1].get("weight", 0))


def _root_ayahs(R, root):
    occ = R.get("occurrences")
    if occ is None or "Input Root" not in occ.columns:
        return 0
    sub = occ[occ["Input Root"] == root]
    if len(sub) == 0:
        return 0
    if {"Surah #", "Ayah #"}.issubset(sub.columns):
        return sub.drop_duplicates(["Surah #", "Ayah #"]).shape[0]
    return len(sub)


def _narr_headline(R, corpus, roots):
    if not roots:
        return None
    root = roots[0]
    n_ayahs = _root_ayahs(R, root)
    total = len(getattr(corpus, "df", []))
    cov = (100.0 * n_ayahs / total) if total else 0.0
    tier = ("ubiquitous" if cov > 5 else "common" if cov > 1
            else "moderately rare" if cov > 0.3 else "rare")

    n_mec, n_med, n_phase = _root_phase_split(R, corpus, root)
    wd, btw = _root_centrality(R, root)
    partner, p_w = _root_top_partner(R, root)
    p_share = (100.0 * p_w / n_ayahs) if n_ayahs else 0.0

    parts = []
    parts.append(
        f"For `{root}`, the numbers above paint a consistent picture: a "
        f"**{tier}** root that touches {n_ayahs} ayahs ({cov:.1f}% of the corpus)."
    )

    if n_phase > 0:
        mec_pct = 100.0 * n_mec / n_phase
        med_pct = 100.0 * n_med / n_phase
        if abs(mec_pct - med_pct) < 15:
            parts.append(
                f"Its {mec_pct:.0f}/{med_pct:.0f} Meccan-Medinan split is "
                f"relatively balanced, meaning `{root}` carries weight across "
                f"both the early creedal phase and the later legal/communal phase."
            )
        elif mec_pct > med_pct:
            parts.append(
                f"Its {mec_pct:.0f}% Meccan dominance ({med_pct:.0f}% Medinan) "
                f"signals that `{root}` does primarily early-revelation work — "
                f"creed, warning, reorientation — rather than legal terminology."
            )
        else:
            parts.append(
                f"Its {med_pct:.0f}% Medinan dominance ({mec_pct:.0f}% Meccan) "
                f"signals that `{root}` does primarily later-revelation work — "
                f"law, community, statecraft — rather than early creedal teaching."
            )

    if wd is not None:
        if btw is not None and btw < 0.01 and wd > 50:
            parts.append(
                f"Weighted degree **{wd}** is substantial but the near-zero "
                f"betweenness ({btw:.2f}) is the key tell: `{root}` shares "
                f"verses with central concepts, but those concepts are already "
                f"well-connected to each other. `{root}` does not introduce "
                f"new connectivity — it rides existing routes rather than building them."
            )
        elif btw is not None and btw > 0.1:
            parts.append(
                f"Both its weighted degree ({wd}) and its betweenness "
                f"({btw:.2f}) are high — `{root}` is a structural **bridge** "
                f"root, sitting on paths that connect subgroups which would "
                f"otherwise be separated."
            )
        else:
            parts.append(
                f"Weighted degree of {wd} places `{root}` among the heavier "
                f"hitters in its session network."
            )

    if partner and p_w > 0:
        if p_share > 30:
            parts.append(
                f"The single most defining feature of `{root}`'s network "
                f"footprint is its tie to `{partner}`: they share **{p_w}** ayahs, "
                f"meaning `{partner}` appears in about **{p_share:.0f}%** of "
                f"all `{root}` verses — an unusually tight pairing worth "
                f"reading verse-by-verse in the Ayah Browser."
            )
        elif p_share > 10:
            parts.append(
                f"Its strongest single tie is to `{partner}` ({p_w} shared "
                f"ayahs, {p_share:.0f}% of `{root}` verses). This pairing is "
                f"the firmest anchor in `{root}`'s neighbourhood and the "
                f"natural first place to look for shared semantic territory."
            )
        else:
            parts.append(
                f"Its top partner is `{partner}` ({p_w} shared, {p_share:.0f}% "
                f"of `{root}` verses) — but no single root dominates `{root}`'s "
                f"company: the term is **distributed** across many partners "
                f"rather than concentrated on one."
            )

    return "**What this means.** " + " ".join(parts)


def _narr_deep(R, corpus, root):
    if not root:
        return None
    n_ayahs = _root_ayahs(R, root)
    if n_ayahs == 0:
        return None
    occ = R.get("occurrences")
    sub = occ[occ["Input Root"] == root] if occ is not None and "Input Root" in occ.columns else None

    parts = []
    if sub is not None and "Surah #" in sub.columns:
        n_surahs = sub["Surah #"].nunique()
        top3 = sub.groupby("Surah #").size().sort_values(ascending=False).head(3).sum()
        concentration = 100.0 * top3 / n_ayahs if n_ayahs else 0
        if n_surahs >= 30 and concentration < 50:
            parts.append(
                f"`{root}` is **broadcast across the corpus** ({n_surahs} of 114 "
                f"surahs) with no single surah dominating — only {concentration:.0f}% "
                f"of its occurrences fall in the top-3 surahs. This is a sign "
                f"of a *recurring theme*, not a *localised topic*."
            )
        elif concentration > 60:
            parts.append(
                f"`{root}` is **heavily concentrated**: {concentration:.0f}% of "
                f"its {n_ayahs} occurrences fall in just three surahs. The text "
                f"treats `{root}` as a localised concern of those passages rather "
                f"than a universal background term."
            )
        else:
            parts.append(
                f"`{root}` appears in {n_surahs} of 114 surahs with moderate "
                f"concentration ({concentration:.0f}% in the top-3). Wide enough "
                f"to be a recurring theme, focused enough that those surahs "
                f"shape its meaning."
            )

    # Partner analysis
    partner, p_w = _root_top_partner(R, root)
    if partner and p_w > 0:
        p_share = 100.0 * p_w / n_ayahs if n_ayahs else 0
        parts.append(
            f"Its strongest partner `{partner}` accounts for {p_share:.0f}% of "
            f"`{root}`'s verses — read those shared ayahs in the Ayah Browser "
            f"to feel the texture of the pairing."
        )

    # Phase
    n_mec, n_med, n_phase = _root_phase_split(R, corpus, root)
    if n_phase > 0:
        mec_pct = 100.0 * n_mec / n_phase
        if mec_pct > 65:
            parts.append(f"Predominantly **Meccan** ({mec_pct:.0f}%) — "
                         f"`{root}` belongs to the early-revelation creedal vocabulary.")
        elif mec_pct < 35:
            parts.append(f"Predominantly **Medinan** ({100-mec_pct:.0f}%) — "
                         f"`{root}` belongs to the later-revelation legal/communal vocabulary.")
        else:
            parts.append(f"A **balanced** Meccan/Medinan split — `{root}` "
                         f"spans both early and later phases of revelation.")

    # Rarity
    rar = R.get("rarity")
    if rar is not None and "Input Root" in rar.columns:
        row = rar[rar["Input Root"] == root]
        if len(row) > 0:
            pct = row.iloc[0].get("Percentile")
            tier = str(row.iloc[0].get("Tier", "")).lower()
            if "ubiquitous" in tier or (pct and pct > 95):
                parts.append(
                    f"In the corpus baseline, `{root}` sits at the top — "
                    f"more frequent than {pct}% of all roots. It is part of "
                    f"the Quran's core working vocabulary."
                )
            elif "rare" in tier or (pct and pct < 10):
                parts.append(
                    f"`{root}` is rare in baseline terms (only {pct}th "
                    f"percentile of root frequencies) — every occurrence "
                    f"carries proportionally more weight."
                )

    return "**What this means.** " + " ".join(parts) if parts else None


def _narr_network(R, corpus, roots):
    import networkx as nx
    g = R.get("graph")
    if g is None or g.number_of_nodes() == 0:
        return None
    if not roots:
        return None
    root = roots[0]
    N = g.number_of_nodes()
    density = nx.density(g)
    ns = R.get("net_stats") or {}
    mod = ns.get("modularity")
    diam = ns.get("diameter")
    centr = R.get("centrality")

    def _top_list(col, k=5):
        if centr is None or len(centr) == 0:
            return []
        name_col = "Root" if "Root" in centr.columns else "root"
        if col not in centr.columns:
            return []
        try:
            return [(row[name_col], float(row[col])) for _, row in
                    centr.sort_values(col, ascending=False).head(k).iterrows()]
        except Exception:
            return []

    deg_top = _top_list("Weighted Degree", 5) or _top_list("weighted_degree", 5)
    btw_top = _top_list("Betweenness", 5) or _top_list("betweenness", 5)
    eig_top = _top_list("Eigenvector", 5) or _top_list("eigenvector", 5)

    def _rank_of(top_list, target):
        for i, (n, _) in enumerate(top_list):
            if n == target:
                return i + 1
        return None

    deg_rank = _rank_of(deg_top, root)
    btw_rank = _rank_of(btw_top, root)
    eig_rank = _rank_of(eig_top, root)

    parts = []

    # ─── Paragraph 1: Where does the input root sit on each ranking?
    if deg_rank == 1 and eig_rank == 1:
        para1 = (
            f"`{root}` tops both the **weighted-degree** and **eigenvector** "
            f"rankings: it is not only the busiest node in this network but "
            f"is also surrounded by *other* busy nodes — a centre-of-centres. "
            f"That is structurally the strongest position a root can hold. "
        )
    elif deg_rank == 1:
        eig_root = eig_top[0][0] if eig_top else None
        para1 = (
            f"`{root}` is **#1 by raw weighted degree** (sheer volume of "
            f"shared ayahs) but the eigenvector ranking is led by "
            f"{('`'+eig_root+'`') if eig_root else 'another root'} — meaning "
            f"`{root}` talks to MANY roots, but the most influential talkers "
            f"talk to {('`'+eig_root+'`') if eig_root else 'others'}. "
        )
    elif eig_rank == 1:
        deg_root = deg_top[0][0] if deg_top else None
        para1 = (
            f"`{root}` is **#1 by eigenvector centrality** (well-connected "
            f"to other well-connected roots) but does not have the highest "
            f"raw degree. It is more *strategic* than *busy*: it surrounds "
            f"itself with the central roots even if it doesn't share the "
            f"most verses. "
        )
    else:
        deg_root = deg_top[0][0] if deg_top else None
        para1 = (
            f"`{root}` is not #1 on degree or eigenvector — "
            f"{('`'+deg_root+'`') if deg_root else 'another root'} occupies "
            f"the structural centre of `{root}`'s session network. `{root}` "
            f"is a participant, not the hub. "
        )

    # Bridge analysis — is the root a bridge?
    if btw_rank is None:
        btw_names = ", ".join(f"`{n}`" for n, _ in btw_top[:3])
        para2 = (
            f"On the **bridge** axis (betweenness), `{root}` does not appear "
            f"in the top 5. The bridge roots — {btw_names} — are different "
            f"roots that sit on the shortest paths between sub-groups. "
            f"In plain terms: `{root}` lives *inside* a tight neighbourhood, "
            f"while those other roots act as *gateways* between neighbourhoods. "
            f"Removing `{root}` would barely change the topology; removing "
            f"a bridge root would split the network. "
        )
    elif btw_rank == 1:
        para2 = (
            f"`{root}` is also **#1 on betweenness** — not just a centre but "
            f"a *gateway*. It sits on the shortest path between subgroups. "
            f"Removing `{root}` would fragment the network. "
        )
    else:
        para2 = (
            f"`{root}` ranks #{btw_rank} on betweenness — it is partly a "
            f"bridge but not the strongest. The actual gateway roots are "
            f"{', '.join('`'+n+'`' for n, _ in btw_top[:3])}, which sit on "
            f"more shortest paths than `{root}` does. "
        )

    # ─── Paragraph 3: Cohesion / topology summary
    para3_bits = []
    if density > 0.7:
        para3_bits.append(
            f"density **{density:.2f}** says the partners of `{root}` mostly "
            f"share ayahs with each *other*, not just with `{root}`"
        )
    elif density > 0.3:
        para3_bits.append(
            f"density **{density:.2f}** is moderate — partners share some "
            f"ayahs with each other but the network is not exhaustively "
            f"interconnected"
        )
    else:
        para3_bits.append(
            f"density **{density:.2f}** is low — the network is **star-shaped** "
            f"around `{root}`: partners come to `{root}` but do not all meet each other"
        )
    if mod is not None:
        if mod < 0.15:
            para3_bits.append(
                f"modularity **{mod:.2f}** is essentially zero, confirming "
                f"there are no clean sub-groups — `{root}`'s neighbourhood is "
                f"a single cohesive register"
            )
        elif mod < 0.30:
            para3_bits.append(
                f"modularity **{mod:.2f}** is low — there are nominal "
                f"communities but the boundaries between them are soft"
            )
        else:
            para3_bits.append(
                f"modularity **{mod:.2f}** is meaningful — the partners of "
                f"`{root}` split into genuine sub-registers; the colours in "
                f"the network chart above are not arbitrary"
            )
    if diam is not None and diam > 0:
        para3_bits.append(
            f"diameter **{int(diam)}** means any partner reaches any other "
            f"in at most {int(diam)} hop{'s' if diam > 1 else ''} — this is a "
            f"shallow, intimate neighbourhood, not a long thin chain"
        )

    para3 = "**Topology synthesis.** " + "; ".join(para3_bits) + "."

    return "**What this means.**\n\n" + para1 + "\n\n" + para2 + "\n\n" + para3


def _narr_temporal(R, corpus, roots):
    if not R.get("has_rev_order"):
        return None
    only_m = R.get("phase_only_meccan") or []
    only_d = R.get("phase_only_medinan") or []
    both = R.get("phase_in_both") or []
    total = len(only_m) + len(only_d) + len(both)
    if total == 0:
        return None
    m_pct = 100.0 * len(only_m) / total
    d_pct = 100.0 * len(only_d) / total
    b_pct = 100.0 * len(both) / total
    root = roots[0] if roots else None

    para1_bits = []
    if b_pct > 50:
        para1_bits.append(
            f"Over half ({b_pct:.0f}%) of root-pairs appear in **both** "
            f"phases. The pairings around `{root}` are not phase-locked: "
            f"the same conceptual companions travel with `{root}` whether "
            f"the verse is Meccan creed or Medinan legislation."
        )
    elif m_pct > 50:
        para1_bits.append(
            f"{m_pct:.0f}% of pairs are **Meccan-only**. The companions "
            f"of `{root}` were largely fixed in the early-revelation phase; "
            f"only {b_pct:.0f}% of pair-relationships survived into "
            f"Medinan verses. This is a creedal/warning-era vocabulary "
            f"that did not get re-used much in later legal contexts."
        )
    elif d_pct > 50:
        para1_bits.append(
            f"{d_pct:.0f}% of pairs are **Medinan-only**. The conceptual "
            f"connections around `{root}` are mostly a later-revelation "
            f"phenomenon — legal, communal, statecraft contexts. The "
            f"Meccan companions of `{root}` were fewer and different."
        )
    else:
        para1_bits.append(
            f"Pairs split fairly evenly: **{m_pct:.0f}% Meccan-only**, "
            f"**{d_pct:.0f}% Medinan-only**, **{b_pct:.0f}% both**. "
            f"`{root}` has distinct partner sets in each phase plus a "
            f"persistent shared core — a sign of a concept that gets "
            f"re-anchored as revelation progresses."
        )

    # Cross-reference: which input pairs survive both phases?
    para2_bits = []
    if root:
        try:
            mec_partners = [p for p in only_m if root in p][:3]
            med_partners = [p for p in only_d if root in p][:3]
            both_partners = [p for p in both if root in p][:5]
        except Exception:
            mec_partners = med_partners = both_partners = []
        if both_partners:
            names = [b for a, b in [(p[0], p[1]) for p in both_partners] if a == root] + \
                    [a for a, b in [(p[0], p[1]) for p in both_partners] if b == root]
            names = list(dict.fromkeys(names))[:5]
            if names:
                para2_bits.append(
                    f"`{root}`'s **phase-spanning anchors** "
                    f"(co-occur in both Meccan and Medinan verses): "
                    f"{', '.join('`'+n+'`' for n in names)}. These are "
                    f"the pairings most central to `{root}`'s identity — "
                    f"they survived the shift from creed to law."
                )
        if mec_partners:
            names = [b for a, b in [(p[0], p[1]) for p in mec_partners] if a == root] + \
                    [a for a, b in [(p[0], p[1]) for p in mec_partners] if b == root]
            names = list(dict.fromkeys(names))[:3]
            if names:
                para2_bits.append(
                    f"Meccan-only partners of `{root}`: "
                    f"{', '.join('`'+n+'`' for n in names)} — "
                    f"these pairings dissolved or migrated by the Medinan phase."
                )
        if med_partners:
            names = [b for a, b in [(p[0], p[1]) for p in med_partners] if a == root] + \
                    [a for a, b in [(p[0], p[1]) for p in med_partners] if b == root]
            names = list(dict.fromkeys(names))[:3]
            if names:
                para2_bits.append(
                    f"Medinan-only partners of `{root}`: "
                    f"{', '.join('`'+n+'`' for n in names)} — "
                    f"these connections are later-revelation novelties around `{root}`."
                )

    para1 = " ".join(para1_bits)
    para2 = " ".join(para2_bits) if para2_bits else ""
    if para2:
        return "**What this means.**\n\n" + para1 + "\n\n" + para2
    return "**What this means.** " + para1


def _narr_motifs(R, corpus, roots):
    tri = R.get("triangles")
    if tri is None or len(tri) == 0:
        return None
    n = len(tri)
    g = R.get("graph")
    N = g.number_of_nodes() if g is not None else 0
    max_possible = N * (N - 1) * (N - 2) // 6 if N >= 3 else 0
    density = 100.0 * n / max_possible if max_possible else 0.0

    if density > 30:
        return (f"**What this means.** {n} closed triads is "
                f"**high** ({density:.0f}% of all possible 3-subsets) — your "
                f"network is rich in three-way conceptual combinations. The "
                f"text repeatedly weaves these three-root patterns together "
                f"rather than relying on pairs alone.")
    elif density > 5:
        return (f"**What this means.** {n} closed triads ({density:.0f}% of "
                f"possible) is a **moderate** count — there are clear three-way "
                f"recurring patterns but they are not the dominant structure.")
    else:
        return (f"**What this means.** Only {n} closed triads ({density:.0f}%) "
                f"means the network is **pairwise-dominated** — concepts travel "
                f"in pairs rather than triples. Few three-way combinations "
                f"recur often enough to leave a trace.")


def _narr_community(R, corpus, roots):
    comm = R.get("communities") or {}
    if not isinstance(comm, dict) or not comm:
        return None
    groups: dict = {}
    for n, c in comm.items():
        groups.setdefault(c, []).append(n)
    if not groups:
        return None
    sizes = sorted([len(g) for g in groups.values()], reverse=True)
    n_comm = len(groups)
    biggest = sizes[0]
    total_nodes = sum(sizes)
    big_share = 100.0 * biggest / total_nodes if total_nodes else 0

    if n_comm == 1:
        return ("**What this means.** All your partner roots fell into a "
                "single Louvain community — the neighbourhood reads as one "
                "cohesive semantic register, not several. Your root is not "
                "splitting attention across different conceptual worlds.")
    if big_share > 70:
        return (f"**What this means.** {n_comm} communities exist on paper, "
                f"but **{big_share:.0f}%** of the network sits in the largest "
                f"one. Effectively one dominant semantic register with a few "
                f"satellite roots — not a balanced multi-register footprint.")
    return (f"**What this means.** {n_comm} balanced sub-clusters (largest "
            f"{biggest} roots, smallest {sizes[-1]}). Your root participates "
            f"in **multiple distinct semantic registers** simultaneously — "
            f"each community is a different thematic family it touches.")


def _narr_pairwise(R, corpus, roots):
    if len(roots) < 2:
        return None
    overlap = R.get("overlap")
    if overlap is None:
        return None
    pairs = []
    for i, a in enumerate(roots):
        for b in roots[i+1:]:
            if a in overlap.index and b in overlap.columns:
                try:
                    pairs.append((a, b, int(overlap.loc[a, b])))
                except Exception:
                    pass
    if not pairs:
        return None
    pairs.sort(key=lambda x: -x[2])
    a, b, n = pairs[0]
    if n == 0:
        return ("**What this means.** None of your input roots share ayahs "
                "with each other - they live in separate semantic worlds "
                "within this corpus.")
    return (f"**What this means.** Strongest tie among inputs is `{a}` -- `{b}` "
            f"at {n} shared ayahs. Read those verses in the Ayah Browser first.")


def _narr_topics(R, corpus, roots):
    if not roots:
        return None
    try:
        import topics as T
        if not T.CACHE_PATH.exists():
            return None
        cache = T.compute(corpus)
        if cache.get("n_nodes", 0) == 0:
            return None
    except Exception:
        return None
    root = roots[0]
    ti, members, mean_s = T.get_topic_for_root(cache, root)
    quad = T.quadrant_lists(cache, root, k=3)
    contra = quad.get("contrastive", [])
    syn = quad.get("distributional_synonym", [])
    parts = []
    if ti >= 0 and members:
        others = sorted([m for m in members if m != root])[:4]
        parts.append(
            f"`{root}` clusters with {len(members)-1} other roots "
            f"({', '.join(others)}) at stability {mean_s:.2f}. These "
            f"are `{root}`'s core semantic family."
        )
    if contra:
        names = ", ".join(f"`{n}`" for n, _, _ in contra[:3])
        parts.append(
            f"Contrastive partners ({names}) co-occur with `{root}` but "
            f"inhabit different contexts overall -- read those shared verses "
            f"to confirm whether the text places them as antitheses."
        )
    if syn:
        names = ", ".join(f"`{n}`" for n, _, _ in syn[:3])
        parts.append(
            f"Distributional synonyms ({names}) almost never share verses "
            f"with `{root}` yet appear in the same contexts -- latent "
            f"semantic kin invisible to verse-reading alone."
        )
    if not parts:
        return None
    return "**What this means.** " + " ".join(parts)


def _narr_divergence(R, corpus, roots):
    if not roots:
        return None
    try:
        import surface_divergence as SD
        if not SD.CACHE_PATH.exists():
            return None
        cache = SD.compute(corpus)
    except Exception:
        return None
    flagged = [r for r in roots if SD.get_split(cache, r)]
    if not flagged:
        return None
    if len(flagged) == 1:
        s = SD.get_split(cache, flagged[0])
        cs = [", ".join(forms) for forms in s["clusters"].values()]
        return (f"**What this means.** `{flagged[0]}` is empirically split "
                f"into {len(s['clusters'])} clusters ({') vs. ('.join(cs)}). "
                f"Each cluster travels with different partner roots -- "
                f"treating `{flagged[0]}` as one node averages two distinct "
                f"meanings.")
