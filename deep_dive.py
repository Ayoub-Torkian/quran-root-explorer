#!/usr/bin/env python3
"""deep_dive.py - background worker for Qur'an CONCEPT & AYAH deep-dives.

Produces a STRUCTURED, AUDITED bundle (00_request.json, data/, findings/,
figures/, MANIFEST.json) under SpatialAnalysis/deep-dives/. Dev-only tool; NOT
deployed with the app (like precompute_spatial.py / audit_app.py).

Design (per FINDINGS_LEDGER north star - multimodal cross-level reinforcement):
multi-granularity by construction. The concept is characterised at the ROOT and
SURFACE levels and described at the MORPHOLOGY level, and co-locators are
cross-checked ACROSS granularities -> findings confirmed at >=2 levels are
VERIFIED; level-specific ones are flagged as DIVERGENCE (sense-specific or
sparsity noise). Every structural claim is compared to a frequency-matched
scramble null. No tafsir: outputs are computational descriptions only.

Reports (docx + pdf) are a SEPARATE, user-gated FINAL step - NOT produced here.

Usage:
  python deep_dive.py concept <root> [--unit surah|ayah_band] [--raw] [--k 4]
"""
import argparse
import datetime
import json
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import analysis as A          # noqa: E402
import spatial_patterns as SP  # noqa: E402

OUT_BASE = HERE.parent / "SpatialAnalysis" / "deep-dives"
CODE_VERSION = "deep_dive.v1-2026-06-04"
XLSX = None
for _c in ("Book6.xlsx", "book6.xlsx", "Book5.xlsx", "book5.xlsx"):
    if (HERE / _c).exists():
        XLSX = HERE / _c
        break


def _J(o):
    """Make numpy / set objects JSON-serialisable."""
    if isinstance(o, dict):
        return {str(k): _J(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_J(v) for v in o]
    if isinstance(o, set):
        return sorted(_J(v) for v in o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return None if np.isnan(o) else float(o)
    if isinstance(o, np.ndarray):
        return _J(o.tolist())
    return o


def _dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(_J(obj), fh, ensure_ascii=False, indent=2)


# ----------------------------------------------------------------------------
def concept_relations(emb, target, normalize, top=8):
    """SAME six-type multimodal fusion as the ayah pipeline, but for a CONCEPT's
    related concepts, across the 3 INDEPENDENT connectome modalities:
    semantic (distributional) ∥ co-location (territory) ∥ spatial (GIS shape).
    Each neighbour is typed: semantic / co-location / spatial (one axis) ·
    consensus (≥2 axes) · orthogonal (1 axis, others ~0) · divergent (1 high,
    another negative). This is the fusion — separate axes, synthesised."""
    idx = emb["index"]; roots = emb["roots"]
    K = A.normalize_letters if normalize else (lambda t: t)
    tk = K(target)
    if tk not in idx:
        return None
    ti = idx[tk]

    def zsim(M):
        v = M[ti]
        sim = -((M - v) ** 2).sum(1)        # higher = closer
        mu = sim.mean(); sd = sim.std() or 1e-9
        return (sim - mu) / sd

    zs, zl, zp = zsim(emb["distrib"]), zsim(emb["coloc"]), zsim(emb["spatial"])
    HI, NEG, NEAR = 1.0, -1.0, 0.5
    from collections import defaultdict
    cands = []
    for j in range(len(roots)):
        if j == ti:
            continue
        ax = {"semantic": float(zs[j]), "co-location": float(zl[j]),
              "spatial": float(zp[j])}
        highs = [k for k, v in ax.items() if v >= HI]
        negs = [k for k, v in ax.items() if v <= NEG]
        relevance = max(ax.values())
        if not highs and relevance < HI:
            continue
        if len(highs) >= 2:
            rel = "consensus"
        elif len(highs) == 1 and negs:
            rel = "divergent"
        elif len(highs) == 1:
            others = [v for k, v in ax.items() if k != highs[0]]
            rel = "orthogonal" if all(abs(v) < NEAR for v in others) else highs[0]
        else:
            rel = max(ax, key=ax.get)
        cands.append(dict(root=roots[j], relation=rel,
                          axes={k: round(v, 2) for k, v in ax.items()},
                          relevance=round(float(relevance) + len(highs), 3)))
    cands.sort(key=lambda d: -d["relevance"])
    by_type = defaultdict(list)
    for d in cands:
        by_type[d["relation"]].append(d)
    skey = {"semantic": lambda d: -d["axes"]["semantic"],
            "co-location": lambda d: -d["axes"]["co-location"],
            "spatial": lambda d: -d["axes"]["spatial"],
            "consensus": lambda d: -d["relevance"],
            "orthogonal": lambda d: -max(d["axes"].values()),
            "divergent": lambda d: -max(d["axes"].values())}
    out = {}
    for t2, lst in by_type.items():
        lst.sort(key=skey.get(t2, lambda d: -d["relevance"]))
        out[t2] = lst[:top]
    return dict(by_relation={k: len(v) for k, v in by_type.items()},
                related_by_type=out)


# ----------------------------------------------------------------------------
def concept_deep_dive(target, unit="surah", normalize=True, k=4, min_freq=8,
                      n_scramble=30, corpus=None, progress=None):
    t0 = time.time()
    if corpus is not None:
        c = corpus
    elif XLSX is None:
        raise SystemExit("No Book6/Book5 .xlsx found next to deep_dive.py")
    else:
        c = A.load_corpus(str(XLSX))
    K = A.normalize_letters if normalize else (lambda t: t)
    tk = K(target)
    freq = c.freq_norm if normalize else c.freq_exact
    f = int(freq.get(tk, 0))
    if f == 0:
        raise ValueError(f"Concept '{target}' (normalised '{tk}') is not in the corpus.")

    # 1. CONNECTOME multi-view neighbourhood (ROOT level) -> field expansion
    if progress: progress(0.10, "building multimodal embeddings…")
    emb = SP.multiview_embeddings(c, normalize, unit=unit, min_freq=min_freq)
    mv = SP.concept_multiview_neighbors(c, target, normalize, k=12, emb=emb,
                                        unit=unit, min_freq=min_freq) or {}
    if progress: progress(0.45, "computing concept relations…")
    relations = concept_relations(emb, target, normalize, top=8) or {}
    consensus = mv.get("consensus", [])
    sem_only = mv.get("sem_only", [])
    views = mv.get("views", {})

    # 2. CO-LOCATION at ROOT level (share / avoid, with permutation p-values)
    if progress: progress(0.55, "co-location territory…")
    fld_root = SP.colocation_field(c, normalize, unit=unit, min_freq=min_freq,
                                   feature="root")
    col_root = SP.colocation_neighbors(c, target, normalize, unit=unit, top=20,
                                       field=fld_root, feature="root")

    # 3. SURFACE-FORM sense map + CO-LOCATION at SURFACE level
    forms = Counter()
    for i in range(len(c.df)):
        rt = c.root_tokens[i]
        st_ = c.surface_tokens[i]
        for j, r in enumerate(rt):
            if K(r) == tk and j < len(st_):
                forms[st_[j]] += 1
    top_forms = [ff for ff, _ in forms.most_common(8)]
    fld_surf = SP.colocation_field(c, normalize, unit=unit, min_freq=min_freq,
                                   feature="surface")
    senses = []
    for ff in top_forms:
        cn = SP.colocation_neighbors(c, ff, normalize, unit=unit, top=8,
                                     field=fld_surf, feature="surface")
        senses.append(dict(form=ff, count=int(forms[ff]), share=cn["share"][:8]))

    # 3b. CROSS-GRANULARITY consensus / divergence among co-locators
    root_sig = {r for (r, a, p) in col_root["share"][:15] if p <= 0.10}
    surf_sig = Counter()
    for s in senses:
        for (r, a, p) in s["share"]:
            if p <= 0.10:
                surf_sig[r] += 1
    verified = sorted(root_sig & set(surf_sig))          # both levels -> robust
    root_only = sorted(root_sig - set(surf_sig))          # aggregation-level only
    surf_only = sorted(set(surf_sig) - root_sig)          # sense-specific / noise
    cross = dict(
        verified_both_levels=verified, root_level_only=root_only,
        surface_level_only=surf_only,
        note=("Co-locators significant (p<=0.10) at BOTH the root level and the "
              "aggregated surface-form level are VERIFIED (robust to granularity). "
              "Root-only may be an aggregation effect; surface-only is "
              "sense-specific or sparsity noise - flagged, not asserted."))

    # 4. DISTRIBUTION (root level)
    su, ay = SP.occ_surah_ayah(c, target, normalize)
    cov = SP.coverage_index(c, target, normalize, unit=unit)
    if progress: progress(0.68, "spatial archetype…")
    arch = SP.archetype_analysis(c, normalize, unit=unit, k=k)
    seed_arch, seed_feats = None, None
    if arch and tk in arch["roots"]:
        ri = arch["roots"].index(tk)
        lab = int(arch["labels"][ri])
        a_j = arch["archetypes"][lab]
        seed_feats = {nm: float(arch["X"][ri][col])
                      for col, nm in enumerate(arch["feat_names"])}
        seed_arch = dict(cluster=lab, tag=a_j["tag"], desc=a_j["desc"],
                         stability=a_j["stability"])
    surah_counts = Counter(int(s) for s in su)
    hotspots = [[int(s), int(cnt)] for s, cnt in surah_counts.most_common(10)]
    distribution = dict(
        frequency=f, n_occurrences=int(len(su)),
        coverage=_J(cov), n_surahs_present=int(len(surah_counts)),
        hotspot_surahs=hotspots, archetype=seed_arch, features=seed_feats)

    # 5. BEYOND-CHANCE null: seed's areal evenness vs frequency-matched scramble
    vals_real, _ = SP.areal_counts(c, target, normalize, unit=unit)
    W = SP.contiguity_W(len(vals_real))
    mi_real = SP.morans_I_analytic(np.asarray(vals_real, float), W)["I"]
    null_I = []
    for sd in range(n_scramble):
        if progress: progress(0.75 + 0.18 * sd / max(n_scramble, 1), f"beyond-chance null {sd + 1}/{n_scramble}…")
        sc = SP.make_scramble(c, seed=sd)
        vv, _ = SP.areal_counts(sc, target, normalize, unit=unit)
        null_I.append(SP.morans_I_analytic(np.asarray(vv, float), W)["I"])
    mu = float(np.mean(null_I))
    sdv = float(np.std(null_I) or 1e-9)
    z = (mi_real - mu) / sdv
    null = dict(metric="areal_moran_I", real=round(float(mi_real), 4),
                null_mean=round(mu, 4), null_sd=round(sdv, 4), z=round(float(z), 2),
                n_scramble=n_scramble,
                interpretation=("more even/dispersed than chance" if z < -2 else
                                "more clustered than chance" if z > 2 else
                                "indistinguishable from chance (frequency artifact)"))

    # 6. MORPHOLOGY profile (particles attached around the form)
    try:
        mdf = A.morphology_breakdown(c, [tk], normalize)
        morph_rows = mdf.to_dict("records") if mdf is not None and len(mdf) else []
    except Exception as e:
        morph_rows = [{"error": str(e)}]

    # ---- field expansion (the data-driven "concept", not just the seed root) ----
    coloc_neighbours = [r for (r, a, p) in col_root["share"][:12] if p <= 0.10]
    field = dict(
        seed=target, seed_normalized=tk, frequency=f, core=[target],
        # PRIMARY concept field = the meaning-bearing (semantic distributional)
        # neighbourhood. This is what "understand the concept using ALL the data"
        # means: the roots the corpus deploys in the same distributional company.
        semantic_field=views.get("semantic", []),
        # robustness layer: neighbours confirmed by >=2 independent views. Often
        # SPARSE because the views are near-orthogonal (Jaccard ~0.03) - an
        # honest, tested property, not a bug. A non-empty entry = robustly bonded.
        cross_view_consensus=[dict(root=r, confirmed_by_views=v, n_views=len(v))
                              for r, v in consensus],
        # territory layer: who SHARES its spatial deployment (co-location).
        co_location_neighbours=coloc_neighbours,
        method=("Concept field is built data-drivenly from ALL occurrences, not "
                "cherry-picked. PRIMARY = semantic distributional neighbours "
                "(meaning). SEPARATE layers: cross-view CONSENSUS (>=2 of "
                "semantic/spatial/co-location = robustly bonded; sparse by design) "
                "and CO-LOCATION (shared territory). Kept separate because the "
                "views are near-orthogonal - blending them dilutes meaning."))

    # ---- SEQUENCE / CHARACTER modality (the Two-Books track, kept SEPARATE) ----
    last_tok = total_occ = 0
    pos_sum = 0.0
    for i in range(len(c.df)):
        toks = c.root_tokens[i]; m = len(toks)
        for j, tt in enumerate(toks):
            if K(tt) == tk:
                total_occ += 1
                pos_sum += (j / (m - 1) if m > 1 else 0.5)
                if j == m - 1:
                    last_tok += 1
    sequence = dict(
        root_letters=list(tk),
        mean_within_ayah_position=round(pos_sum / total_occ, 3) if total_occ else None,
        ayah_final_share=round(last_tok / total_occ, 3) if total_occ else None,
        note=("Sequence/character level (Two Books): WHERE the concept sits within the "
              "ayah and how often it lands ayah-finally (rhyme/fawāṣil). A separate "
              "track from meaning — synthesised, never blended."))

    # ---- MULTIMODAL SYNTHESIS (fusion = separate tracks, integrated results) ----
    sem_top = field["semantic_field"][:6]
    terr_top = field["co_location_neighbours"][:6]
    sem_set = set(field["semantic_field"]); terr_set = set(field["co_location_neighbours"])
    overlap = sorted(sem_set & terr_set)
    spatial_real = bool(null["z"] is not None and null["z"] <= -2)
    if progress: progress(0.97, "synthesising…")
    synthesis = dict(
        modalities=dict(
            semantic=dict(role="meaning-field (what it means-with)", top=sem_top),
            co_location=dict(role="territory (what it is deployed-with)", top=terr_top),
            morphology=dict(role="sense splits across surface forms",
                            n_sense_forms=len(senses)),
            spatial=dict(role="distribution shape",
                         archetype=(seed_arch["tag"] if seed_arch else None),
                         beyond_chance=spatial_real, z=null["z"]),
            sequence=dict(role="in-ayah position / rhyme",
                          mean_position=sequence["mean_within_ayah_position"],
                          ayah_final_share=sequence["ayah_final_share"]),
        ),
        cross_modal=dict(
            convergence=overlap,
            divergence=("meaning-mates ≠ territory-mates (semantic and co-location "
                        "are orthogonal here)" if not overlap else
                        "meaning and territory partly overlap"),
            verified_bonds=cross["verified_both_levels"],
        ),
        relations_by_type=relations.get("related_by_type", {}),
        relations_counts=relations.get("by_relation", {}),
        reading=("MULTIMODAL FUSION (separate tracks, synthesised — not reduced to any "
                 "one view): SEMANTIC carries meaning; CO-LOCATION the deployment "
                 "territory; MORPHOLOGY the sense splits; SPATIAL the distribution shape "
                 + ("(a real beyond-chance signal)" if spatial_real else
                    "(null here — explained by frequency alone, NOT a finding)") +
                 "; SEQUENCE the in-ayah position. The headline is their AGREEMENT and "
                 "DIVERGENCE across levels, not the spatial statistics."))

    elapsed = round(time.time() - t0, 1)
    return dict(
        request=dict(kind="concept", target=target, normalized=tk, unit=unit,
                     normalize=normalize, k=k, min_freq=min_freq,
                     n_scramble=n_scramble),
        field=field, distribution=distribution,
        multiview=dict(views=views, consensus=consensus, sem_only=sem_only),
        colocation=col_root, senses=senses, cross_granularity=cross,
        null=null, morphology=morph_rows, sequence=sequence, synthesis=synthesis,
        relations=relations,
        occurrences=dict(surah=[int(x) for x in su], ayah=[int(x) for x in ay]),
        meta=dict(code_version=CODE_VERSION, elapsed_s=elapsed,
                  generated=datetime.datetime.now().isoformat(timespec="seconds"),
                  n_ayahs=int(len(c.df))))


def _figures(res, figdir):
    """Numeric-only figures (no Arabic labels) - hotspot + null."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    figdir.mkdir(parents=True, exist_ok=True)
    # hotspot: occurrences across surahs
    hs = res["distribution"]["hotspot_surahs"]
    if hs:
        xs = [h[0] for h in hs]
        ys = [h[1] for h in hs]
        fig, ax = plt.subplots(figsize=(7, 3.2))
        ax.bar([str(x) for x in xs], ys, color="#1D3557")
        ax.set_xlabel("surah #")
        ax.set_ylabel("occurrences")
        ax.set_title("Top surahs by occurrence")
        fig.tight_layout()
        fig.savefig(figdir / "hotspot_surahs.png", dpi=110)
        plt.close(fig)
    # scatter su vs ay
    su = res["occurrences"]["surah"]
    ay = res["occurrences"]["ayah"]
    if su:
        fig, ax = plt.subplots(figsize=(7, 3.2))
        ax.scatter(su, ay, s=8, alpha=0.45, color="#06AED5")
        ax.set_xlabel("surah #")
        ax.set_ylabel("ayah # within surah")
        ax.set_title("Occurrence map")
        fig.tight_layout()
        fig.savefig(figdir / "occurrence_map.png", dpi=110)
        plt.close(fig)


def run_concept(target, unit, normalize, k):
    res = concept_deep_dive(target, unit=unit, normalize=normalize, k=k)
    tk = res["request"]["normalized"]
    stamp = datetime.date.today().strftime("%Y%m%d")
    slug = "".join(ch for ch in tk if ch.isalnum()) or "concept"
    outdir = OUT_BASE / "concepts" / f"{slug}_{stamp}"
    (outdir / "data").mkdir(parents=True, exist_ok=True)
    (outdir / "findings").mkdir(parents=True, exist_ok=True)
    # request
    _dump(outdir / "00_request.json", res["request"])
    # findings (the substantiated results)
    _dump(outdir / "findings" / "field.json", res["field"])
    _dump(outdir / "findings" / "distribution.json", res["distribution"])
    _dump(outdir / "findings" / "multiview.json", res["multiview"])
    _dump(outdir / "findings" / "colocation.json", res["colocation"])
    _dump(outdir / "findings" / "senses.json", res["senses"])
    _dump(outdir / "findings" / "cross_granularity.json", res["cross_granularity"])
    _dump(outdir / "findings" / "null.json", res["null"])
    _dump(outdir / "findings" / "morphology.json", res["morphology"])
    _dump(outdir / "findings" / "synthesis.json", res["synthesis"])
    _dump(outdir / "findings" / "sequence.json", res["sequence"])
    _dump(outdir / "findings" / "relations.json", res["relations"])
    # raw data inputs
    _dump(outdir / "data" / "occurrences.json", res["occurrences"])
    # figures
    try:
        _figures(res, outdir / "figures")
        figs = sorted(p.name for p in (outdir / "figures").glob("*.png"))
    except Exception as e:
        figs = []
        print("  [figures skipped]", e)
    # MANIFEST
    manifest = dict(
        kind="concept", target=target, normalized=tk, slug=slug,
        unit=unit, normalize=normalize, code_version=CODE_VERSION,
        generated=res["meta"]["generated"], elapsed_s=res["meta"]["elapsed_s"],
        outputs=dict(
            request="00_request.json",
            findings=sorted(p.name for p in (outdir / "findings").glob("*.json")),
            data=sorted(p.name for p in (outdir / "data").glob("*.json")),
            figures=figs, reports=[]),
        verification=dict(
            concept_found=True,
            semantic_field_nonempty=bool(res["field"]["semantic_field"]),
            consensus_bonds=len(res["field"]["cross_view_consensus"]),
            null_computed=res["null"]["z"] is not None,
            cross_granularity_checked=True,
            multimodal_fusion=sorted(res["relations"].get("by_relation", {}).keys())
            if res.get("relations") else [],
            reports_generated=False),
        note="Reports (docx+pdf) are a separate user-gated step; not in this run.")
    _dump(outdir / "MANIFEST.json", manifest)
    return outdir, res, manifest


# ============================================================================
# BACKGROUND QUEUE  (P5)  — the app drops requests; the worker drains them.
# ============================================================================
QUEUE = OUT_BASE / "_queue"


def enqueue(kind, payload):
    """Non-blocking: drop a request into the pending queue (called by the app)."""
    import uuid
    pend = QUEUE / "pending"; pend.mkdir(parents=True, exist_ok=True)
    rid = (f"{kind}_{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}_"
           f"{uuid.uuid4().hex[:6]}")
    _dump(pend / f"{rid}.json",
          dict(id=rid, kind=kind, payload=payload,
               reports=bool(payload.get("reports", False)),
               queued=datetime.datetime.now().isoformat(timespec="seconds"),
               status="pending"))
    return rid


def queue_status():
    pend, done = QUEUE / "pending", QUEUE / "done"
    return dict(
        pending=sorted(x.stem for x in pend.glob("*.json")) if pend.exists() else [],
        done=sorted(x.stem for x in done.glob("*.json")) if done.exists() else [])


def drain_queue(make_reports=False, once=True, interval=20):
    """Process every pending request (concept/ayah), write its bundle, optionally
    its reports, then move the request to done/. The background worker:
       python deep_dive.py drain            # one pass
       python deep_dive.py watch [--interval N]   # loop forever
    """
    import time as _t
    pend, done = QUEUE / "pending", QUEUE / "done"
    done.mkdir(parents=True, exist_ok=True)
    while True:
        for rf in (sorted(pend.glob("*.json")) if pend.exists() else []):
            try:
                req = json.loads(rf.read_text("utf-8"))
                pl = req["payload"]
                if req["kind"] == "concept":
                    outdir, _, _ = run_concept(pl["target"], pl.get("unit", "surah"),
                                               pl.get("normalize", True), pl.get("k", 4))
                else:
                    outdir, _, _ = run_ayah(pl["refs"], pl.get("unit", "surah"),
                                            pl.get("normalize", True))
                if make_reports or req.get("reports"):
                    import report_dive as RP
                    RP.build_reports(outdir)
                req.update(status="done", bundle=str(outdir),
                           finished=datetime.datetime.now().isoformat(timespec="seconds"))
                _dump(done / rf.name, req)
                rf.unlink()
                print(f"[drained] {req['id']} -> {outdir}")
            except (Exception, SystemExit) as e:
                _dump(done / rf.name, dict(id=rf.stem, status="error", error=str(e)))
                try:
                    rf.unlink()
                except OSError:
                    pass
                print(f"[error] {rf.stem}: {e}")
        if once:
            break
        _t.sleep(interval)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="kind", required=True)
    pc = sub.add_parser("concept")
    pc.add_argument("target")
    pc.add_argument("--unit", default="surah", choices=["surah", "ayah_band"])
    pc.add_argument("--raw", action="store_true", help="do NOT normalise letters")
    pc.add_argument("--k", type=int, default=4)
    pa = sub.add_parser("ayah")
    pa.add_argument("refs", nargs="+", help="one or more surah:ayah (e.g. 2:255)")
    pa.add_argument("--unit", default="surah", choices=["surah", "ayah_band"])
    pa.add_argument("--raw", action="store_true", help="do NOT normalise letters")
    pdr = sub.add_parser("drain")
    pdr.add_argument("--reports", action="store_true", help="also build docx+pdf")
    pwt = sub.add_parser("watch")
    pwt.add_argument("--interval", type=int, default=20)
    pwt.add_argument("--reports", action="store_true", help="also build docx+pdf")
    args = ap.parse_args()
    if args.kind == "concept":
        outdir, res, man = run_concept(args.target, args.unit, not args.raw, args.k)
        print(f"\nwrote {outdir}")
        fld = res["field"]
        print(f"  seed={fld['seed']} freq={fld['frequency']}  unit={args.unit}")
        print(f"  MULTIMODAL FUSION counts: {res['relations'].get('by_relation', {})}")
        for _t in ["consensus", "semantic", "co-location", "spatial",
                   "orthogonal", "divergent"]:
            _l = res["relations"].get("related_by_type", {}).get(_t, [])
            if _l:
                print(f"    [{_t}] " + ", ".join(d["root"] for d in _l[:6]))
        print(f"  synthesis: {res['synthesis']['cross_modal']['divergence']}")
        print(f"  null: real I={res['null']['real']} vs {res['null']['null_mean']}"
              f" (z={res['null']['z']}) -> {res['null']['interpretation']}")
        print(f"  cross-granularity VERIFIED co-locators: "
              f"{res['cross_granularity']['verified_both_levels']}")
        print(f"  archetype: {res['distribution']['archetype']}")
        print(f"  verification: {man['verification']}")
    elif args.kind == "ayah":
        outdir, res, man = run_ayah(args.refs, args.unit, not args.raw)
        print(f"\nwrote {outdir}")
        print(f"  seed: {res['request']['seeds']}  concepts={res['seed_concepts']}")
        syn = res["synthesis"]
        print(f"  candidates={syn['n_candidates']}  by_relation={syn['by_relation']}")
        for t in ["consensus", "direct", "resonant", "co-located",
                  "orthogonal", "divergent"]:
            lst = res["related_by_type"].get(t, [])
            if not lst:
                continue
            print(f"  [{t}]")
            for d in lst[:3]:
                print(f"    {d['ref']:8} L={d['axes']['lexical']:+.1f} "
                      f"S={d['axes']['semantic']:+.1f} P={d['axes']['spatial']:+.1f} "
                      f" shared={d['shared_roots']}")
        print(f"  verification: {man['verification']}")



# ============================================================================
# PASTE-AND-MATCH  — identify which Book6 ayah(s) a pasted Arabic snippet is.
# ============================================================================
def _ayah_token_index(corpus):
    """Cached per-ayah normalised tokens + idf (built once per corpus)."""
    import math
    import re
    from collections import Counter
    key = id(corpus)
    cache = globals().setdefault("_AYAH_TOK_CACHE", {})
    if key in cache:
        return cache[key]

    def norm(x):
        x = re.sub(r"[^\u0600-\u06FF\s]", " ", str(x))
        return [t for t in (A.normalize_letters(w) for w in x.split()) if t]

    df = corpus.df
    src = (df[A.COL_DIACRITIZED] if A.COL_DIACRITIZED in df.columns
           else df[A.COL_SEGMENTED])
    su = df[A.COL_SURAH].astype(int).to_numpy()
    ay = df[A.COL_AYAH].astype(int).to_numpy()
    toklists = [norm(src.iloc[i]) for i in range(len(df))]
    docf = Counter()
    for toks in toklists:
        for t in set(toks):
            docf[t] += 1
    N = len(df)
    idf = {t: math.log(1 + N / (1 + docf[t])) for t in docf}
    data = (toklists, idf, su, ay, norm)
    cache[key] = data
    return data


def match_pasted_ayahs(corpus, text, min_overlap=0.6, min_tokens=2, top=50):
    """Identify which Book6 ayah(s) a pasted Arabic snippet contains. Robust to
    script/orthography (uthmani ٱ, imlaei pause marks), verse numbers, brackets,
    and an interleaved translation. Matches on IDF-WEIGHTED token overlap (rare
    words count, common words don't), drops sub-phrase matches, returns
    [(surah, ayah, confidence)]."""
    toklists, idf, su, ay, norm = _ayah_token_index(corpus)
    paste = set(norm(text))
    if not paste:
        return []
    cand = []
    for i, toks in enumerate(toklists):
        if len(toks) < min_tokens:
            continue
        den = sum(idf[t] for t in toks)
        if den <= 0:
            continue
        num = sum(idf[t] for t in toks if t in paste)
        frac = num / den
        if frac >= min_overlap:
            cand.append((frac, len(set(toks)), set(toks), int(su[i]), int(ay[i])))
    cand.sort(key=lambda x: (-x[1], -x[0]))             # longest first
    kept = []
    for frac, n, tset, sgu, agu in cand:
        if any(tset <= k[2] for k in kept):             # drop sub-phrase of a kept match
            continue
        kept.append((frac, n, tset, sgu, agu))
    out = [(sgu, agu, round(frac, 2)) for frac, n, tset, sgu, agu in kept]
    out.sort(key=lambda x: (x[0], x[1]))                # mushaf order
    return out[:top]


def match_pasted_concepts(corpus, text, top=30):
    """Extract the CONCEPTS (roots) present in pasted Arabic text. Book6 stores
    clitic-stripped stems, so each pasted word is lightly de-cliticised (strip
    و/ف/ب/ك/ل/س/ال prefixes and pronoun/plural suffixes), preferring the LONGEST
    stem that resolves to a known root (guards against over-stripping, e.g.
    والدين→ولد not دين). Returns [(root, count)] for the user to pick & confirm."""
    import re
    from collections import Counter
    K = A.normalize_letters
    cache = globals().setdefault("_SURF2ROOT", {})
    key = id(corpus)
    if key not in cache:
        s2r = {}
        for rt, sf in zip(corpus.root_tokens, corpus.surface_tokens):
            for r, w in zip(rt, sf):
                s2r.setdefault(K(w), Counter())[K(r)] += 1
        cache[key] = s2r
    s2r = cache[key]
    freq = corpus.freq_norm
    PRE = ["وال", "فال", "بال", "كال", "لل", "ال", "و", "ف", "ب", "ك", "ل", "س"]
    SUF = ["هما", "كما", "هم", "هن", "كم", "كن", "نا", "ها", "ون", "ين", "ات",
           "ان", "تم", "تن", "ه", "ك", "ي", "ة", "وا", "ا"]

    def resolve(tok):
        prefs = {tok}
        for _ in range(2):                   # peel up to 2 stacked prefixes (و+ب+ال)
            for base in list(prefs):
                for p in PRE:
                    if base.startswith(p) and len(base) - len(p) >= 2:
                        prefs.add(base[len(p):])
        cands = set()
        for stem in prefs:  # noqa
            cands.add(stem)
            for sf in SUF:
                if stem.endswith(sf) and len(stem) - len(sf) >= 2:
                    cands.add(stem[:-len(sf)])
        res = []
        for cand in cands:
            if cand in freq:
                res.append((cand, len(cand)))
            elif cand in s2r:
                res.append((s2r[cand].most_common(1)[0][0], len(cand)))
        if not res:
            return None
        res.sort(key=lambda x: -x[1])        # longest resolving stem wins
        return res[0][0]

    def norm_tokens(x):
        x = re.sub(r"[^\u0600-\u06FF\s]", " ", str(x))
        return [t for t in (K(w) for w in x.split()) if t]

    found = Counter()
    for tok in norm_tokens(text):
        r = resolve(tok)
        if r:
            found[r] += 1
    ranked = sorted(found, key=lambda r: (-found[r], -freq.get(r, 0)))
    return [(r, found[r]) for r in ranked][:top]


# ============================================================================
# AYAH-CONTENT DEEP-DIVE  (second first-class endeavor)
# Score each candidate ayah on 3 INDEPENDENT axes, classify into 6 relation
# types: direct / resonant / co-located / consensus / orthogonal / divergent.
# ============================================================================
def ayah_deep_dive(seeds, unit="surah", normalize=True, min_freq=8, top=30,
                   corpus=None, progress=None):
    import math
    from collections import defaultdict
    t0 = time.time()
    if corpus is not None:
        c = corpus
    elif XLSX is None:
        raise SystemExit("No Book6/Book5 .xlsx found next to deep_dive.py")
    else:
        c = A.load_corpus(str(XLSX))
    K = A.normalize_letters if normalize else (lambda t: t)
    df = c.df
    su = df[A.COL_SURAH].astype(int).to_numpy()
    ay = df[A.COL_AYAH].astype(int).to_numpy()
    seg = df[A.COL_SEGMENTED].astype(str).tolist()
    disp = (df[A.COL_DIACRITIZED].astype(str).tolist()
            if A.COL_DIACRITIZED in df.columns else seg)   # diacritized = for DISPLAY
    seed_idx = []
    for (s, a) in seeds:
        hits = [i for i in range(len(df)) if int(su[i]) == s and int(ay[i]) == a]
        if not hits:
            raise ValueError(f"ayah {s}:{a} not found in corpus")
        seed_idx.append(hits[0])

    if not any(c.root_tokens[i] for i in seed_idx):
        raise ValueError("Disjoint-letter opening (muqaṭṭaʿāt — e.g. المص). It has no "
                         "roots or concepts, so a concept-level deep-dive does not apply. "
                         "Explore these on the 🔠 Disjoint Letters page.")

    if progress: progress(0.18, "building embeddings…")
    emb = SP.multiview_embeddings(c, normalize, unit=unit, min_freq=min_freq)
    idx = emb["index"]; D = emb["distrib"]; L = emb["coloc"]
    n = len(df)
    # Treat each ayah as ONE CONTEXT ENTITY, not a bag of separate concepts.
    # The verse signature is an idf-WEIGHTED centroid of its concept vectors, so
    # DISTINCTIVE roots shape the verse's meaning more than ubiquitous ones — a
    # salience-weighted context vector, not a flat average that blurs identity.
    # ALL data is included in the analysis, independent of what the UI shows.
    # Two root sets per verse:
    #   * _full  — EVERY root of the verse (drives the lexical lens & the shared-
    #              root evidence, so even rare/below-floor roots count);
    #   * _emb   — roots that have an embedding (drive the meaning/territory
    #              centroid, since a vector-less root cannot be placed).
    ayah_roots_full = []
    ayah_roots = []                                   # embeddable subset
    for i in range(n):
        full = {K(t) for t in c.root_tokens[i] if K(t)}
        ayah_roots_full.append(full)
        ayah_roots.append({r for r in full if r in idx})

    # idf over the FULL root vocabulary (nothing dropped for the lexical lens).
    docfreq = Counter()
    for rs in ayah_roots_full:
        for r in rs:
            docfreq[r] += 1
    idf = {r: math.log(1 + n / (1 + docfreq[r])) for r in docfreq}

    def _ctx(rs, M):
        """idf-weighted context centroid of a set of roots over embedding M.
        Represents the WHOLE verse as a single salience-weighted entity, so the
        verse's DISTINCTIVE concepts define its signature."""
        rs = sorted(r for r in rs if r in idx)
        if not rs:
            return None
        w = np.array([idf[r] for r in rs], dtype=float)
        s = w.sum()
        w = (w / s) if s else (np.ones(len(rs)) / len(rs))
        return (w[:, None] * M[[idx[r] for r in rs]]).sum(0)

    A_sem = np.zeros((n, D.shape[1]))
    A_terr = np.zeros((n, L.shape[1]))
    for i in range(n):
        if ayah_roots[i]:
            A_sem[i] = _ctx(ayah_roots[i], D)
            A_terr[i] = _ctx(ayah_roots[i], L)

    seed_rows = set(seed_idx)
    # The seed entity carries ALL of its roots (full set); the meaning/territory
    # centroid uses the embeddable subset, but nothing is dropped from the
    # lexical lens or the evidence.
    seed_roots_full = set().union(*[ayah_roots_full[i] for i in seed_idx]) if seed_idx else set()
    seed_roots = {r for r in seed_roots_full if r in idx}
    if not seed_roots_full:
        raise ValueError("This ayah has no analysable roots. Pick another ayah.")
    # One entity — the idf-weighted CONTEXT of all its roots taken together —
    # rather than each concept handled in isolation.
    svec = _ctx(seed_roots, D)
    tvec = _ctx(seed_roots, L)

    def cos_all(M, v):
        if v is None:
            return np.zeros(M.shape[0])
        vn = np.linalg.norm(v) or 1e-9
        Mn = np.linalg.norm(M, axis=1); Mn[Mn == 0] = 1e-9
        return (M @ v) / (Mn * vn)

    sem = cos_all(A_sem, svec)
    spa = cos_all(A_terr, tvec)
    lex = np.zeros(n)
    for j in range(n):
        sh = seed_roots_full & ayah_roots_full[j]      # ALL shared roots count
        if sh:
            lex[j] = sum(idf[r] for r in sh)

    mask = np.array([(len(ayah_roots_full[j]) > 0 and j not in seed_rows)
                     for j in range(n)])

    def z(a):
        m = a[mask]; mu = m.mean(); sd = m.std() or 1e-9
        return (a - mu) / sd

    zl, zs, zp = z(lex), z(sem), z(spa)
    HI, NEG, NEAR = 1.0, -1.0, 0.5
    cands = []
    for j in range(n):
        if not mask[j]:
            continue
        axz = {"direct": float(zl[j]), "resonant": float(zs[j]),
               "co-located": float(zp[j])}
        highs = [k for k, v in axz.items() if v >= HI]
        negs = [k for k, v in (("resonant", zs[j]), ("co-located", zp[j]))
                if v <= NEG]
        relevance = max(zl[j], zs[j], zp[j])
        if not highs and relevance < HI:
            continue
        if len(highs) >= 2:
            rel = "consensus"
        elif len(highs) == 1 and negs:
            rel = "divergent"
        elif len(highs) == 1:
            others = [v for k, v in axz.items() if k != highs[0]]
            rel = "orthogonal" if all(abs(v) < NEAR for v in others) else highs[0]
        else:
            rel = max(axz, key=axz.get)
        sh = sorted(seed_roots_full & ayah_roots_full[j])
        cands.append(dict(
            ref=f"{int(su[j])}:{int(ay[j])}", surah=int(su[j]), ayah=int(ay[j]),
            relation=rel,
            axes=dict(lexical=round(float(zl[j]), 2),
                      semantic=round(float(zs[j]), 2),
                      spatial=round(float(zp[j]), 2)),
            shared_roots=sh, n_roots=len(ayah_roots_full[j]),
            relevance=round(float(relevance) + len(highs), 3),
            text=disp[j]))
    if progress: progress(0.88, "ranking related ayahs…")
    cands.sort(key=lambda d: -d["relevance"])
    top_c = cands[:top]

    # Group ALL candidates by relation type, then keep the top examples of EACH
    # type sorted by its DRIVING axis - so resonant / orthogonal / divergent are
    # surfaced, not buried under high-lexical consensus matches.
    all_by_type = defaultdict(list)
    for d in cands:
        all_by_type[d["relation"]].append(d)
    sort_key = {
        "direct": lambda d: -d["axes"]["lexical"],
        "resonant": lambda d: -d["axes"]["semantic"],
        "co-located": lambda d: -d["axes"]["spatial"],
        "consensus": lambda d: -d["relevance"],
        "orthogonal": lambda d: -max(d["axes"].values()),
        "divergent": lambda d: -max(d["axes"].values()),
    }
    related_by_type = {}
    for t, lst in all_by_type.items():
        lst.sort(key=sort_key.get(t, lambda d: -d["relevance"]))
        related_by_type[t] = lst[:8]
    synthesis = dict(
        n_candidates=len(cands),
        by_relation={k: len(v) for k, v in all_by_type.items()},
        examples_by_relation={k: [d["ref"] for d in v]
                              for k, v in related_by_type.items()},
        note=("Relation types are computed from 3 INDEPENDENT axes (lexical / "
              "semantic-distributional / spatial-territory), each z-standardised "
              "over all candidate ayahs. consensus=>=2 axes high; orthogonal=1 "
              "axis high & others ~0 (independent); divergent=1 axis high & "
              "another negative (anti-correlated). Counts are over ALL candidates; "
              "examples are the top of EACH type by its driving axis. No tafsir - "
              "computational cross-references with evidence (axis z + shared roots)."))
    seed_info = [dict(ref=f"{int(su[i])}:{int(ay[i])}", surah=int(su[i]),
                      ayah=int(ay[i]), text=disp[i],
                      roots=sorted(set(c.root_tokens[i])))   # COMPLETE (all roots)
                 for i in seed_idx]
    return dict(
        request=dict(kind="ayah", seeds=[f"{s}:{a}" for s, a in seeds], unit=unit,
                     normalize=normalize, min_freq=min_freq, top=top),
        seed=seed_info, seed_concepts=sorted(seed_roots),
        related=top_c, related_by_type=related_by_type, synthesis=synthesis,
        meta=dict(code_version=CODE_VERSION, elapsed_s=round(time.time() - t0, 1),
                  generated=datetime.datetime.now().isoformat(timespec="seconds"),
                  n_ayahs=n))


def run_ayah(seeds_arg, unit, normalize):
    seeds = []
    for tok in seeds_arg:
        s, a = tok.split(":")
        seeds.append((int(s), int(a)))
    res = ayah_deep_dive(seeds, unit=unit, normalize=normalize)
    stamp = datetime.date.today().strftime("%Y%m%d")
    tag = "_".join(f"S{s}A{a}" for s, a in seeds)
    outdir = OUT_BASE / "ayahs" / f"{tag}_{stamp}"
    (outdir / "data").mkdir(parents=True, exist_ok=True)
    (outdir / "findings").mkdir(parents=True, exist_ok=True)
    _dump(outdir / "00_request.json", res["request"])
    _dump(outdir / "findings" / "seed.json",
          dict(seed=res["seed"], seed_concepts=res["seed_concepts"]))
    _dump(outdir / "findings" / "related.json", res["related"])
    _dump(outdir / "findings" / "related_by_type.json", res["related_by_type"])
    _dump(outdir / "findings" / "synthesis.json", res["synthesis"])
    _dump(outdir / "data" / "full.json", res)
    manifest = dict(
        kind="ayah", seeds=res["request"]["seeds"], slug=tag, unit=unit,
        normalize=normalize, code_version=CODE_VERSION,
        generated=res["meta"]["generated"], elapsed_s=res["meta"]["elapsed_s"],
        outputs=dict(request="00_request.json",
                     findings=sorted(p.name for p in (outdir / "findings").glob("*.json")),
                     data=sorted(p.name for p in (outdir / "data").glob("*.json")),
                     figures=[], reports=[]),
        verification=dict(
            seeds_found=True, related_found=len(res["related"]) > 0,
            relation_types_present=sorted(res["related_by_type"].keys()),
            reports_generated=False),
        note="Reports (docx+pdf) are a separate user-gated step; not in this run.")
    _dump(outdir / "MANIFEST.json", manifest)
    return outdir, res, manifest


if __name__ == "__main__":
    main()
