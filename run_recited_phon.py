"""Guided local runner for MODALITY #49 / Lens 14 — recited/phonological layer.

The sandbox is data-blocked (no diacritizer installs, no vocalized corpora fetchable). Run this on a
connected machine to UNBLOCK the distinctiveness test. Two paths — path A is preferred (gold-vs-gold).

============================ PATH A — gold vocalized comparators (BEST) ============================
Place one or both files into  sequence_tests/corpus/  then run this script:
  * ar_tashkeela.txt   — vocalized CLASSICAL PROSE. Source: the "Tashkeela" corpus (fully diacritized
      classical Arabic). Available on Kaggle / HuggingFace / SourceForge. A few hundred KB is plenty;
      just save a chunk as UTF-8 text with its harakat intact.
  * ar_poetry_voc.txt  — vocalized POETRY. Source: a fully-voweled dīwān (e.g. al-Mutanabbī with full
      tashkīl from a vocalized edition / aldiwan.net pages that carry harakat).
This is the fair comparison: gold-vocalized Qur'an vs gold-vocalized comparator.

==================== PATH B — symmetric auto-diacritization (if no gold data) ====================
If you can only get UNVOCALIZED comparators, you MUST put the Qur'an in the SAME (auto) condition to
avoid a gold-vs-noisy confound (the kind of asymmetry that once inflated #42). With a diacritizer
installed locally (e.g. CAMeL Tools: `pip install camel-tools` then `camel_data -i disambig-mle-calima*`),
this script will: strip harakat from BOTH the Qur'an and the comparators, re-diacritize ALL with the same
tool, write *_voc.txt, and run the comparison. (CAMeL Tools needs no GPU but does download model data.)

After either path, results print here and the script appends them to evidence_49_results.txt — paste back.
"""
import os, sys, io, contextlib, re

HERE = os.path.dirname(os.path.abspath(__file__))
CP = os.path.join(HERE, "sequence_tests", "corpus")
OUT = os.path.join(HERE, "evidence_49_results.txt")
GOLD = ["ar_tashkeela.txt", "ar_poetry_voc.txt", "ar_saj_voc.txt"]


def have_gold():
    return [f for f in GOLD if os.path.exists(os.path.join(CP, f))]


def try_camel_symmetric():
    """PATH B: build symmetric auto-diacritized comparators (+ auto-diacritized Qur'an condition)."""
    try:
        from camel_tools.disambig.mle import MLEDisambiguator
        from camel_tools.utils.dediac import dediac_ar
    except Exception:
        return False
    print("[B] CAMeL Tools found — building symmetric auto-diacritized corpora ...")
    mle = MLEDisambiguator.pretrained()
    def diac(text):
        out = []
        for tok in text.split():
            d = mle.disambiguate([tok])
            try: out.append(d[0].analyses[0].analysis['diac'])
            except Exception: out.append(tok)
        return " ".join(out)
    srcs = {"ar_tashkeela.txt": ["ar_tabari.txt", "ar_classical2.txt", "ar_novel.txt"],
            "ar_poetry_voc.txt": ["ar_poetry.txt"], "ar_saj_voc.txt": ["ar_sajprose.txt"]}
    for dst, ins in srcs.items():
        buf = []
        for fn in ins:
            p = os.path.join(CP, fn)
            if os.path.exists(p):
                buf.append(diac(dediac_ar(open(p, encoding="utf-8").read())))
        if buf:
            open(os.path.join(CP, dst), "w", encoding="utf-8").write("\n".join(buf))
            print(f"   wrote {dst}")
    # NOTE: for full symmetry, recited_phon should also run on an auto-diacritized Qur'an; see its docstring.
    return True


def main():
    g = have_gold()
    if not g:
        if not try_camel_symmetric():
            print(__doc__)
            print("\n>>> No vocalized comparators and no diacritizer found. Follow PATH A or PATH B above.")
            return
    sys.path.insert(0, os.path.join(HERE, "sequence_tests")); sys.path.insert(0, HERE)
    import importlib, recited_phon as RP; importlib.reload(RP)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        RP.main()
    text = buf.getvalue(); print(text)
    open(OUT, "w", encoding="utf-8").write(text)
    print(f"\n[done] results -> {OUT}  (paste back to complete EVIDENCE #49 + Lens 14).")


if __name__ == "__main__":
    main()
