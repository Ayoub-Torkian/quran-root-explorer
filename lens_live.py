"""lens_live.py — quick LIVE runs of gated detectors for the Lens Lab (v2.0 phase 2).

Reuses the EXACT logic of the filed instruments (no new statistics):
  - Lens 9  (#42): recurrence-excess net of word-shuffle, equal-P bootstrap
                   (sequence_tests/intratext_lock_fixed.py, single cell, reduced B)
  - Lens 3  (#34-37/#76): rhyme persistence = dominant last-char share per K=25
                   āyah/sentence window (sequence_tests/fusion_window_rerun.py, feature f1)
TOKENIZER RULE (locked, #76): cross-text features use nrm(COL_DIACRITIZED) — never the lemma column.
Quick cells are INDICATIVE (reduced B); the filed batteries in EVIDENCE.md remain the record.
"""
from __future__ import annotations

import os
import re
from collections import Counter
from pathlib import Path

import numpy as np
import streamlit as st

HERE = Path(__file__).resolve().parent
CP = HERE / "sequence_tests" / "corpus"

_DIA = re.compile(r"[ً-ْٰـۖ-ۭ]")
WA = re.compile(r"[^\W\d_]+", re.UNICODE)


def nl(t: str) -> str:
    t = _DIA.sub("", str(t)); t = re.sub(r"[آأإٱ]", "ا", t)
    t = re.sub(r"[ىی]", "ي", t); t = re.sub(r"[ةھ]", "ه", t)
    return t.replace("ک", "ك").replace("ؤ", "ء").replace("ئ", "ء").strip()


def tok_text(s: str):  # normalize FIRST, then split (#43 rule)
    return [w for w in WA.findall(nl(s)) if len(w) > 1]


STOP = {nl(w) for w in (
    "في من الى على عن مع و ف ب ك ل ال هذا هذه ذلك التي الذي الذين ما لا ان انه اذا قد كان"
    " هو هي هم انت انا نحن كل بعض غير عند او ثم حتى يا اي بين لم لن لو ولا فلا وما وان به له لهم"
    " هنا هناك كما لقد وقد منه منها فيها فيه عليه عليها اليه اليها"
    " علي الي ومن وما ولا لكم لهم انا اني".split())}


def content_words(toks):
    return [w for w in toks if w not in STOP and len(w) > 1]


ORD = ("ar_tabari", "ar_classical2", "ar_novel", "ar_news", "ar_news2")
SAJ = ("ar_sajprose", "ar_saj_hariri")
POE = ("ar_poetry", "ar_poetry_b", "ar_poetry_c")
_SENT = re.compile(r"[.!؟?\n،؛:]+")


def _read(names):
    out = ""
    for n in names:
        p = CP / f"{n}.txt"
        if p.exists():
            out += "\n" + p.read_text(encoding="utf-8", errors="ignore")
    return out


@st.cache_data(show_spinner=False)
def comp_words(names: tuple) -> list:
    return tok_text(_read(names))


@st.cache_data(show_spinner=False)
def comp_units(names: tuple) -> list:
    return [u for u in (tok_text(s) for s in _SENT.split(_read(names))) if len(u) >= 4]


@st.cache_data(show_spinner=False)
def quran_tokens(_df, dcol: str, key: str = "v1") -> tuple:
    """(flat word list, per-āyah unit list) from the vocalized column, locked tokenizer."""
    units = [u for u in (tok_text(str(_df.iloc[i][dcol])) for i in range(len(_df))) if len(u) >= 4]
    flat = [w for u in units for w in u]
    return flat, units


# ---------- Lens 9 / #42 — recurrence excess net of shuffle (quick cell) ----------

def _passages(tokens, K):
    return [tokens[i:i + K] for i in range(0, len(tokens) - K + 1, K)]


def _tf_cos(passlist):
    vocab = {}
    for p in passlist:
        for w in p:
            vocab.setdefault(w, len(vocab))
    V = np.zeros((len(passlist), len(vocab)))
    for i, p in enumerate(passlist):
        for w, ct in Counter(p).items():
            V[i, vocab[w]] = ct
    df_ = (V > 0).sum(0); idf = np.log((len(passlist) + 1) / (df_ + 1)) + 1
    V = V * idf; nrm_ = np.linalg.norm(V, axis=1, keepdims=True); nrm_[nrm_ == 0] = 1
    Vn = V / nrm_
    return Vn @ Vn.T


def _excess_one(passlist, gapfrac, topq):
    Pn = len(passlist); Cm = _tf_cos(passlist); gap = max(1, int(Pn * gapfrac))
    far = np.array([Cm[i, j] for i in range(Pn) for j in range(i + gap, Pn)])
    return float(np.quantile(far, topq) - np.median(far)) if len(far) >= 10 else None


def _rec_excess(rng, passlist, P, gapfrac, topq, B):
    if len(passlist) < P:
        return None
    vals = []
    for _ in range(B):
        idx = np.sort(rng.choice(len(passlist), P, replace=False))
        e = _excess_one([passlist[i] for i in idx], gapfrac, topq)
        if e is not None:
            vals.append(e)
    return np.array(vals)


def _g(a, b):
    if a is None or b is None or len(a) < 2 or len(b) < 2:
        return float("nan")
    return float((a.mean() - b.mean()) / (np.sqrt((a.var() + b.var()) / 2) + 1e-9))


def live_recurrence(qwords: list, K=50, gapfrac=0.25, topq=0.95, B=60) -> dict:
    """One #42 cell, word grain, equal-P, net of word-shuffle. ~1-3s warm."""
    rng = np.random.default_rng(42)
    raw = {"QURAN": qwords, "ord": comp_words(ORD),
           "poetry": comp_words(POE), "saj": comp_words(SAJ)}
    toks = {k: content_words(v) for k, v in raw.items()}
    Pcommon = min(len(_passages(t, K)) for t in toks.values())
    P = max(15, min(40, Pcommon))
    nets = {}
    for nm, t in toks.items():
        real = _rec_excess(rng, _passages(t, K), P, gapfrac, topq, B)
        sh = list(t); rng.shuffle(sh)
        shuf = _rec_excess(rng, _passages(sh, K), P, gapfrac, topq, B)
        nets[nm] = None if real is None or shuf is None else real - shuf
    base = nets["ord"]
    out = {"P": P, "K": K, "B": B,
           "g": {nm: _g(nets[nm], base) for nm in ("QURAN", "poetry", "saj")},
           "gate_ok": nets["QURAN"] is not None and float(np.mean(nets["QURAN"])) > 0}
    return out


# ---------- Lens 3 — rhyme persistence (dominant last-char share, K=25 windows) ----------

def _rp_windows(units, K=25):
    vals = []
    for a in range(0, len(units) - K + 1, K):
        w = units[a:a + K]
        ends = [u[-1] for u in w]
        vals.append(max(Counter(e[-1] for e in ends).values()) / K)
    return np.array(vals)


def live_rhyme(qunits: list, K=25, NULLS=60) -> dict:
    """#76 feature f1 per corpus + unit-shuffle null for the Qur'an. ~1s warm."""
    rng = np.random.default_rng(34)
    rp = {"QURAN": _rp_windows(qunits, K),
          "ord": _rp_windows(comp_units(ORD), K),
          "saj": _rp_windows(comp_units(SAJ), K),
          "poetry": _rp_windows(comp_units(POE), K)}
    null = []
    for _ in range(NULLS):
        sh = list(qunits); rng.shuffle(sh)
        null.append(_rp_windows(sh, K).mean())
    null = np.array(null)
    z = float((rp["QURAN"].mean() - null.mean()) / (null.std() + 1e-9))
    return {"K": K,
            "means": {k: float(v.mean()) for k, v in rp.items()},
            "n_windows": {k: int(len(v)) for k, v in rp.items()},
            "g_vs": {k: _g(rp["QURAN"], rp[k]) for k in ("ord", "saj", "poetry")},
            "null_mean": float(null.mean()), "z_shuffle": z, "gate_ok": z > 2}
